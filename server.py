from flask import Flask, render_template
import schedule
import time
import json


def load_data():
    with open("charts_data.json", "r") as file:
        charts_hashmap_ = json.load(file)

    with open("brain_data.json", "r") as file:
        brain_hashmap_ = json.load(file)
    return [charts_hashmap_, brain_hashmap_]


charts_hashmap = load_data()[0]
brain_hashmap = load_data()[1]
schedule.every().day.at("05:05").do(load_data)

chart_array_HYG = charts_hashmap["chart_array_HYG"]
chart_array_VIX = charts_hashmap["chart_array_VIX"]
chart_array_VXN = charts_hashmap["chart_array_VXN"]
chart_array_indexes = charts_hashmap["chart_array_indexes"]
chart_array_volatility = charts_hashmap["chart_array_volatility"]

summary_report = brain_hashmap["summary_report"]
VIX_VXN_report = brain_hashmap["VIX_VXN_report"]
divergence_explain_array = brain_hashmap["divergence_explain_array"]


def divergence_summary():
    i = 0
    for n in range(3):
        if divergence_explain_array[n][0] == "Bearish":
            i -= 1
        elif divergence_explain_array[n][0] == "Bullish":
            i += 1
        else:
            i += 0
    if i >= 2:
        summary = "The bullish divergences point towards a bullish few trading days ahead."
    elif i <= -2:
        summary = "The bearish divergences point towards a bearish few trading days ahead."
    else:
        summary = "There is no significant bearish or bullish divergences in the market."
    return summary


divergence_summary = divergence_summary()


app = Flask(__name__)


@app.route('/')
def blog():
    return render_template("index.html",
                           chart_array_HYG=chart_array_HYG,
                           chart_array_VIX=chart_array_VIX,
                           chart_array_VXN=chart_array_VXN,
                           summary_report=summary_report,
                           chart_array_indexes=chart_array_indexes,
                           chart_array_volatility=chart_array_volatility,
                           VIX_VXN_report=VIX_VXN_report,
                           divergence_explain_array=divergence_explain_array,
                           divergence_summary=divergence_summary)


@app.route("/<pageName>")
def choosePage(pageName):
    page = "404.html"
    if pageName == "":
        page = "index.html"
        return render_template(page, HYG_charts=chart_array_HYG, VIX_charts=chart_array_VIX)
    elif pageName == "fearandgreed":
        page = "https://edition.cnn.com/markets/fear-and-greed"
    elif pageName == "about":
        page = "about.html"
    elif pageName == "divergences":
        page = "divergences.html"
    return render_template(page,
                           chart_array_HYG=chart_array_HYG,
                           chart_array_VIX=chart_array_VIX,
                           chart_array_VXN=chart_array_VXN,
                           summary_report=summary_report,
                           chart_array_indexes=chart_array_indexes,
                           chart_array_volatility=chart_array_volatility,
                           VIX_VXN_report=VIX_VXN_report,
                           divergence_explain_array=divergence_explain_array,
                           divergence_summary=divergence_summary)


if __name__ == "__main__":
    app.run(debug=True)

while True:
    schedule.run_pending()
    time.sleep(1)
