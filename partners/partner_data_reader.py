import os
import pandas
import typing
import app_config
import csd_dataset.dataset_header
import datetime

class partner_data_reader:
    _columns: typing.List[str]
    _first_day_date: datetime
    _actual_day_date: datetime

    partner_id: str


    def __init__(self, partner_id):
        self.partner_id = partner_id
        self._columns = csd_dataset.dataset_header.columns
        self.data = pandas.read_csv(os.path.join(app_config.app_config['split_partners_data_dir'], partner_id),
                                    sep='\t', header=0, skiprows=1, names=self._columns,
                                    low_memory=False)
        self.data['click_timestamp'] = [datetime.datetime.fromtimestamp(x).replace(hour=0, minute=0, second=0, microsecond=0)
                                        for x in self.data['click_timestamp']]
        self._first_day_date = self.data['click_timestamp'].min()
        self._actual_day_date = self._first_day_date


    def _next_day_date(self):
        return self._actual_day_date + datetime.timedelta(days=1)


    def next_day(self):
        actual_day_data = self.data.loc[(self.data['click_timestamp'] == self._next_day_date())]
        self._actual_day_date += datetime.timedelta(days=1)
        return actual_day_data


    def get_day_data(self, date: datetime):
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.data.loc[self.data['click_timestamp'] == date]


    def get_product_data(self, product_id: str):
        return self.data.loc[self.data['product_id'] == product_id]


    def get_day_product_data(self, date: datetime, product_id: str):
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.data.loc[(self.data['click_timestamp'] == date + datetime.timedelta(days=1))
                             & (self.data['product_id'] == product_id)]


    def get_all_data(self):
        return self.data