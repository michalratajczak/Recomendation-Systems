import os
import pandas
import config
import csd_dataset.dataset_header
import datetime

class partner_data_reader:
    _columns = csd_dataset.dataset_header.columns
    _first_day_date: datetime
    _actual_day_date: datetime

    partner_id: str
    data: pandas.DataFrame


    def __init__(self, partner_id):
        self.partner_id = partner_id
        self._columns.insert(0, 'id')
        self.data = pandas.read_csv(os.path.join(config.config['root_dir'], 'partners', 'data', partner_id),
                                    sep='\t', header=0, skiprows=1, names=self._columns,
                                    low_memory=False, index_col='id')
        self.data['click_timestamp'] = [datetime.datetime.fromtimestamp(x) for x in self.data['click_timestamp']]
        self._first_day_date = self.data['click_timestamp'].min().replace(hour=0, minute=0, second=0, microsecond=0)
        self._actual_day_date = self._first_day_date


    def _next_day_date(self):
        return self._actual_day_date + datetime.timedelta(days=1)


    def next_day(self):
        actual_day_data = self.data.loc[(self.data['click_timestamp'] >= self._actual_day_date)
                                        & (self.data['click_timestamp'] <= self._next_day_date())]
        self._actual_day_date += datetime.timedelta(days=1)
        return actual_day_data


    def get_day_data(self, date: datetime):
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.data.loc[(self.data['click_timestamp'] >= date)
                             & (self.data['click_timestamp'] <= date + datetime.timedelta(days=1))]


    def get_product_data(self, product_id: str):
        return self.data.loc[(self.data['product_id'] == product_id)]


    def get_day_product_data(self, date: datetime, product_id: str):
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.data.loc[(self.data['click_timestamp'] >= date)
                             & (self.data['click_timestamp'] <= date + datetime.timedelta(days=1))
                             & (self.data['product_id'] == product_id)]