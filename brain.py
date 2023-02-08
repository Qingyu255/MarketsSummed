import yfinance as yf


class Brain:
    def stock_report(self, symbol, **percent_change_only):
        change = "Error"
        new_low = None
        new_high = None
        data = yf.download(symbol, start='2022-12-01')
        data_list = data["Close"].to_list()
        data_15_days = data_list[-15:]
        print(data_15_days)
        data_15_days_high = data["High"].to_list()[-15:]
        data_15_days_low = data["Low"].to_list()[-15:]
        percent_change = round(((data_15_days[-1]-data_15_days[-2])/data_15_days[-2]) * 100, 2)
        if percent_change > 0:
            change = "rose"
        elif percent_change < 0:
            change = "dropped"
        if data_15_days_low[-1] < min(data_15_days_low):
            new_low = True
        if data_15_days_high[-1] > max(data_15_days_high):
            new_high = True

        if percent_change_only:
            return f"{change} {abs(percent_change)}%"
        else:
            summary = f"{symbol} {change} {abs(percent_change)}% in the latest trading day."
            if new_low is True:
                summary += f" Also, the {symbol} has made a new 15-day low of {round(data_15_days_low[-1], 2)}."
            elif new_high is True:
                summary += f" Also, the {symbol} has made a new 15-day high of {round(data_15_days_high[-1], 2)}."
            return summary

    def summary_report(self):
        array = []
        for symbol in ["^GSPC", "^IXIC", "^DJI"]:
            array.append(self.stock_report(symbol, percent_change_only=True))
        report = "With regards to major indices, the S and P 500 Index " + array[0] + ", the Nasdaq Index " + array[1] + \
                 " and the Dow Jones Industrial Index " + array[2] + " in the last trading day."
        return report

    def divergence(self, index, symbol_2):
        # This function tracks for divergences over a 3 trading day span (Used for HYG NOT VIX)
        data_1 = yf.download(index, start='2023-01-01')
        data_list_1 = data_1["High"].to_list()[-3:]
        data_2 = yf.download(symbol_2, start='2023-01-01')
        data_list_2 = data_2["High"].to_list()[-3:]
        if data_list_1.index(max(data_list_1)) > data_list_1.index(min(data_list_1)) and data_list_2.index(max(data_list_2)) < data_list_2.index(min(data_list_2)):
            divergence = "Bearish"
            report = f"A bearish Divergence was formed over the past 3 trading days" \
                     f" as the {index} index was in an up trend whilst {symbol_2} was in a down trend."
        elif data_list_1.index(max(data_list_1)) < data_list_1.index(min(data_list_1)) and data_list_2.index(max(data_list_2)) > data_list_2.index(min(data_list_2)):
            divergence = "Bullish"
            report = f"A bullish Divergence was formed over the past 3 trading days" \
                     f" as the {index} index was in an down trend whilst {symbol_2} was in a up trend."
        else:
            divergence = "No Divergence"
            report = f"No divergence was formed over the past 3 trading days."
        return [divergence, report]

    def divergence_volatility(self, index, volatility_index):
        # This function tracks for divergences over a 3 trading day span (Used for VIX only)
        data_1 = yf.download(index, start='2023-01-01')
        data_list_1 = data_1["High"].to_list()[-3:]
        data_2 = yf.download(volatility_index, start='2023-01-01')
        data_list_2 = data_2["High"].to_list()[-3:]
        if data_list_1.index(max(data_list_1)) > data_list_1.index(min(data_list_1)) and data_list_2.index(
                max(data_list_2)) > data_list_2.index(min(data_list_2)):
            divergence = "Bearish"
            report = f"A bearish Divergence was formed over the past 3 trading days" \
                     f" as the {index} index was in an up trend whilst the {volatility_index} Volatility index was also in an up trend."
        elif data_list_1.index(max(data_list_1)) < data_list_1.index(min(data_list_1)) and data_list_2.index(
                max(data_list_2)) < data_list_2.index(min(data_list_2)):
            divergence = "Bullish"
            report = f"A bullish Divergence was formed over the past 3 trading days" \
                     f" as the {index} index was in an down trend whilst the {volatility_index} Volatility index was also in a down trend."
        else:
            divergence = "No Divergence"
            report = f"No divergence was formed over the past 3 trading days."
        return [divergence, report]







        # day_today = dt.datetime.now(timezone("EST")).strftime('%A')
        # def is_weekday(date):
        #     if date in ["Saturday", "Sunday"]:
        #         return False
        #     return True
        #
        #
        # for symbol in ["^SPX", "^IXIC", "^DJI"]:
        #     if is_weekday(day_today) is True:
        #         date_today = dt.datetime.now(timezone("EST")).date()
        #         date_yesterday = date_today - dt.timedelta(1)
        #         date_day_before_yesterday = date_today - dt.timedelta(2)
        #         data = yf.download(symbol, start=date_day_before_yesterday, end=date_yesterday)
        #         data_list = data["Close"].to_list()
        #         percent_change = round(((data_list[1] - data_list[0]) / data_list[0]) * 100, 2)
        #     else:
        #         if day_today == "Saturday":
        #             x = 1
        #         else:
        #             x = 2
        #         date_friday = dt.datetime.now().date() - dt.timedelta(x)
        #         date_thursday = dt.datetime.now().date() - dt.timedelta(x + 1)


# data2 = yf.download("HYG", start='2022-12-01')
# date_list = data.index.to_list()
#
# high2_list = data2["High"].to_list()
# hashmap = {}
#
# for n in range(len(date_list)):
#     hashmap[date_list[n]] = high_list[n]
# print(hashmap)
# print(date_list)
# print(high_list)

# print(data.loc[:,["Open", "High"]].to_dict())
# print(data.loc[:,"High"])
# print(data.keys())
# print(data.to_dict())