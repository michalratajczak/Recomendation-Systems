import os
import pandas
import typing
import app_config
import csd_dataset.dataset_header
import datetime

class partner_data_reader:
    __columns: typing.List[str]
    __first_day_date: datetime
    __actual_day_date: datetime

    partner_id: str
    counter: int


    def __init__(self, partner_id):
        self.partner_id = partner_id
        self.__columns = csd_dataset.dataset_header.columns
        self.data = pandas.read_csv(os.path.join(app_config.app_config['split_partners_data_dir'], partner_id),
                                    sep='\t', header=0, skiprows=0, names=self.__columns,
                                    low_memory=False)
        self.data['click_timestamp'] = [datetime.datetime.utcfromtimestamp(x).replace(hour=0, minute=0, second=0, microsecond=0)
                                        for x in self.data['click_timestamp']]
        self.__first_day_date = self.data['click_timestamp'].min()
        self.__actual_day_date = self.__first_day_date


    def get_actual_date(self):
        return self.__actual_day_date


    def get_actual_day_data(self):
        return self.data.loc[(self.data['click_timestamp'] == self.__actual_day_date)]


    def next_day(self):
        self.__actual_day_date += datetime.timedelta(days=1)


    def get_actual_day_product_list(self):
        return self.get_actual_day_data()['product_id'].unique()


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