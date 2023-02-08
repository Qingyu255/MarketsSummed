from charts import Charts
from brain import Brain
import schedule
import time
import json

charts = Charts()
brain = Brain()


def get_chart_data():
    hashmap = {
        "chart_array_HYG": [charts.get_charts("SPY", "HYG"), charts.get_ratio_chart("SPY", "HYG")],
        "chart_array_VIX": [charts.get_charts("^VIX", "SPY"), charts.get_ratio_chart("SPY", "^VIX")],
        "chart_array_VXN": [charts.get_charts("^VXN", "QQQ"), charts.get_ratio_chart("QQQ", "^VXN")],
        "chart_array_indexes": [charts.get_one_chart(symbol="^GSPC"), charts.get_one_chart(symbol="^IXIC"),
                                charts.get_one_chart(symbol="^DJI")],
        "chart_array_volatility": [charts.get_one_chart(symbol="^VIX"), charts.get_one_chart(symbol="^VXN")],
    }
    with open("charts_data.json", "w") as file:
        json.dump(hashmap, file)
    return


def get_brain_data():
    hashmap = {
        "spy_summary": brain.stock_report(symbol="SPY"),
        "hyg_summary": brain.stock_report(symbol="HYG"),
        "summary_report": brain.summary_report(),
        "VIX_VXN_report": f" Volatility for the S and P 500 Index {brain.stock_report(symbol='^VIX', percent_change_only=True)}"
                 f" whilst volatility for the Nasdaq Index {brain.stock_report(symbol='^VXN', percent_change_only=True)}"
                 f" in the last trading day.",
        "divergence_explain_array": [brain.divergence("SPY", "HYG")[1], brain.divergence_volatility("SPY", "^VIX")[1], brain.divergence_volatility("QQQ", "^VXN")[1]],
    }
    with open("brain_data.json", "w") as file:
        json.dump(hashmap, file)


schedule.every().day.at("05:03").do(get_chart_data)
schedule.every().day.at("05:03").do(get_brain_data)

while True:
    schedule.run_pending()
    time.sleep(60)
    # wait one minute




