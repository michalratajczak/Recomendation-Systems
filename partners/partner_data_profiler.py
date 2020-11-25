import json
import partners.partner_data_reader
import pandas
import partners.partners_list
import typing
import helpers.console_logger
import os
import app_config

class partner_data_profiler:
    partner_id: str
    total_number_of_clicks: int
    total_sales_value: float
    total_number_of_sold_products: int

    def __init__(self, partner_id: str):
        self.partner_id = partner_id
        self.data = partners.partner_data_reader.partner_data_reader(partner_id).get_all_data()

    def calculate_statistics(self):
        self.total_number_of_clicks = len(self.data.index)
        sales_data = self.data.loc[self.data["sale"] == 1]
        self.total_number_of_sold_products = len(sales_data.index)
        self.total_sales_value = sales_data["sales_amount_in_euro"].sum()

    def to_dict(self):
        return \
            {
                "total_number_of_clicks": self.total_number_of_clicks,
                "total_sales_value": self.total_sales_value,
                "total_number_of_sold_products": self.total_number_of_sold_products
            }


def _process_all_partners():
    logger = helpers.console_logger.console_logger("Creating profiles")
    logger.log("Starting operation...")
    counter = 1
    profiles: dict = dict()

    for partner in partners.partners_list.partners:
        logger.run_execution_timer()
        profiler = partner_data_profiler(partner)
        profiler.calculate_statistics()
        profiles[partner] = profiler.to_dict()
        logger.log_with_execution_time(f'{counter} / {len(partners.partners_list.partners)}')
        counter += 1

    with open(os.path.join(app_config.app_config['root_dir'], 'partners', 'partners_profiles.py'), 'w') as f:
        f.write('profiles = \\\n')
        f.write(json.dumps(profiles, indent=4))
    logger.log_total_time()


if __name__ == "__main__":
    _process_all_partners()
