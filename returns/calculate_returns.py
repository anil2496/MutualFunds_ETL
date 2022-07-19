from datetime import date, datetime, timedelta
from main import Mftool


class FundReturns:
    def __init__(self):
        self.curr_date = datetime.today().strftime("%d-%m-%Y")

    def calculate_trailing_returns(self, code):
        date_1_yrs_ago = (datetime.today() - timedelta(days=365 * 1)).strftime("%d-%m-%Y")
        date_3_yrs_ago = (datetime.today() - timedelta(days=365 * 3)).strftime("%d-%m-%Y")
        date_5_yrs_ago = (datetime.today() - timedelta(days=365 * 5)).strftime("%d-%m-%Y")
        date_7_yrs_ago = (datetime.today() - timedelta(days=365 * 7)).strftime("%d-%m-%Y")

        print(date_1_yrs_ago, date_3_yrs_ago, date_5_yrs_ago, date_7_yrs_ago)

        returns = {}
        mf = Mftool()
        response_1_year_ago = mf.get_scheme_historical_nav_for_dates(code, date_1_yrs_ago, self.curr_date)
        initial_nav = float(response_1_year_ago['data'][-1]['nav'])
        final_nav = float(response_1_year_ago['data'][0]['nav'])
        trailing_returns = ((final_nav - initial_nav) / initial_nav) * 100
        returns['1_year_returns'] = round(trailing_returns, 2)

        response_3_year_ago = mf.get_scheme_historical_nav_for_dates(code, date_3_yrs_ago, self.curr_date)
        initial_nav = float(response_3_year_ago['data'][-1]['nav'])
        final_nav = float(response_3_year_ago['data'][0]['nav'])
        trailing_returns = ((final_nav - initial_nav) / initial_nav) * 100
        returns['3_year_returns'] = round(trailing_returns, 2)

        response_5_year_ago = mf.get_scheme_historical_nav_for_dates(code, date_5_yrs_ago, self.curr_date)
        initial_nav = float(response_5_year_ago['data'][-1]['nav'])
        final_nav = float(response_5_year_ago['data'][0]['nav'])
        trailing_returns = ((final_nav - initial_nav) / initial_nav) * 100
        returns['5_year_returns'] = round(trailing_returns, 2)

        response_7_year_ago = mf.get_scheme_historical_nav_for_dates(code, date_7_yrs_ago, self.curr_date)
        initial_nav = float(response_7_year_ago['data'][-1]['nav'])
        final_nav = float(response_7_year_ago['data'][0]['nav'])
        trailing_returns = ((final_nav - initial_nav) / initial_nav) * 100
        returns['7_year_returns'] = round(trailing_returns, 2)
        print(returns)

    def calculate_calendar_returns(self, code, year):
        mf = Mftool()

        response = mf.get_scheme_historical_nav_year(code, year)

        initial_nav = float(response['data'][-1]['nav'])
        final_nav = float(response['data'][0]['nav'])

        print(initial_nav, final_nav)

        calendar_returns = ((final_nav - initial_nav) / initial_nav) * 100
        print(round(calendar_returns, 2))


fr = FundReturns()
# fr.calculate_calendar_returns(119551, 2022)
fr.calculate_trailing_returns(119551)
