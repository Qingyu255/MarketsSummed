import plotly.graph_objects as go
from plotly.subplots import make_subplots
import chart_studio.plotly as py
import chart_studio
import yfinance as yf
import os
import json
import requests
from requests.auth import HTTPBasicAuth

API_KEY = os.environ["API_KEY"]
chart_studio.tools.set_credentials_file(username="qy25555", api_key=API_KEY)
auth = HTTPBasicAuth("qy25555", API_KEY)
headers = {'Plotly-Client-Platform': 'python'}

class Charts:
    def get_one_chart(self, symbol):
        data = yf.download(symbol, start='2022-01-01')
        fig = go.Figure(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'])
        )
        fig.update_xaxes(rangeslider_visible=False)
        fig.update_yaxes(title_text=f"{symbol} Price")
        chart_href = py.plot(fig, auto_open=False)
        return chart_href

    def get_charts(self, symbol1, symbol2):
        symbol1_data = yf.download(symbol1, start='2022-12-01')
        symbol1_chart = go.Candlestick(
            x=symbol1_data.index,
            open=symbol1_data['Open'],
            high=symbol1_data['High'],
            low=symbol1_data['Low'],
            close=symbol1_data['Close'],
            increasing_line_color='#144272',
            decreasing_line_color='gray',)

        symbol2_data = yf.download(symbol2, start='2022-12-01')
        symbol2_chart = go.Candlestick(
            x=symbol2_data.index,
            open=symbol2_data['Open'],
            high=symbol2_data['High'],
            low=symbol2_data['Low'],
            close=symbol2_data['Close'])

        chart = make_subplots(specs=[[{"secondary_y": True}]])
        chart.add_trace(symbol1_chart, secondary_y=False,)
        chart.add_trace(symbol2_chart, secondary_y=True)
        # chart.update_layout(
        #     title_text=f"{symbol1} against {symbol2}"
        # )
        # Set x-axis title
        chart.update_xaxes(title_text="", rangeslider_visible=False)
        # Set y-axes titles
        chart.update_yaxes(title_text=f"<b>{symbol1}</b> (Blue and Gray)", secondary_y=False)
        chart.update_yaxes(title_text=f"<b>{symbol2}</b> (Green and Red)", secondary_y=True)
        chart.update_traces(showlegend=False)
        # chart_studio.tools.set_credentials_file(username="qy2555", api_key="vlB1UmTcyIg5Dy0JXgax")
        chart_href = py.plot(chart, auto_open=False)
        return chart_href


    def get_ratio_chart(self, symbol1, symbol2):
        symbol1_data = yf.download(symbol1, start='2022-12-01')
        symbol2_data = yf.download(symbol2, start='2022-12-01')
        chart = go.Figure(go.Candlestick(
            x=symbol2_data.index,
            open=symbol1_data['Open'] / symbol2_data['Open'],
            high=symbol1_data['High'] / symbol2_data['High'],
            low=symbol1_data['Low'] / symbol2_data['Low'],
            close=symbol1_data['Close'] / symbol2_data['Close'])
        )
        # chart.update_layout(
        #     title_text=f"{symbol1}/{symbol2} ratio chart"
        # )
        # Set x-axis title
        chart.update_xaxes(rangeslider_visible=False)
        # Set y-axes titles
        chart.update_yaxes(title_text=f"{symbol1}/{symbol2}")
        chart_href = py.plot(chart, auto_open=False)
        return chart_href

    def get_pages(self, username, page_size):
        url = 'https://api.plot.ly/v2/folders/all?user=' + username + '&page_size=' + str(page_size)
        response = requests.get(url, auth=auth, headers=headers)
        if response.status_code != 200:
            return
        page = json.loads(response.content)
        yield page
        while True:
            resource = page['children']['next']
            if not resource:
                break
            response = requests.get(resource, auth=auth, headers=headers)
            if response.status_code != 200:
                break
            page = json.loads(response.content)
            yield page


    def permanently_delete_files(self, username, page_size=500, filetype_to_delete='plot'):
        for page in self.get_pages(username, page_size):
            for x in range(0, len(page['children']['results'])):
                fid = page['children']['results'][x]['fid']
                res = requests.get('https://api.plot.ly/v2/files/' + fid, auth=auth, headers=headers)
                res.raise_for_status()
                if res.status_code == 200:
                    json_res = json.loads(res.content)
                    if json_res['filetype'] == filetype_to_delete:
                        # move to trash
                        requests.post('https://api.plot.ly/v2/files/' + fid + '/trash', auth=auth, headers=headers)
                        # permanently delete
                        requests.delete('https://api.plot.ly/v2/files/' + fid + '/permanent_delete', auth=auth,
                                        headers=headers)


