
import os
import cx_Oracle
from config.config import settings


class DbOperations():

    def __init__(self):
        self.username = settings.username
        self.password = settings.password
        self.conn_url = self.username + "/" + self.password + "@localhost:1521/service_sid"
        self.conn = cx_Oracle.connect(self.conn_url)
        self.cursor = self.conn.cursor()

    def insert_data(self, dataframe, table_name):
        dataframe.to_sql(name=table_name, con=self.conn, if_exists='append', index=False)

    def query_data(self, code, start_date, end_date):
        query = "select * from NAV where code = {} and date>={} and date<={}".format(code, start_date,
                                                                                               end_date)

        data = self.cursor.execute(query)
        response = []

        for res in data:
            response.append(res)
        return response

