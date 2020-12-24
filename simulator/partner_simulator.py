import partners.partner_data_reader
import partners.partners_profiles
import simulator.simulation_config
import simulator.simulation_results
import optimizer.optimizer
import typing
import pandas
import datetime

class partner_simulator:
    config: simulator.simulation_config.simulation_config
    partner_id: str
    data_reader: partners.partner_data_reader
    partner_profile: dict
    average_click_cost: float

    optimizer: optimizer.optimizer.optimizer
    products_to_exclude: typing.List[str]
    actually_excluded_products: typing.List[str]
    products_seen_so_far: typing.List[str]

    results: typing.List[simulator.simulation_results.simulation_result_model]
    products_exclusion_history: typing.List[simulator.simulation_results.products_exclusion_history]
    profit_history: typing.List[dict]

    def __init__(self, partner_id: str, config: simulator.simulation_config.simulation_config):
        self.partner_id = partner_id
        self.config = config
        self.data_reader = partners.partner_data_reader.partner_data_reader(partner_id)
        self.partner_profile = partners.partners_profiles.profiles[partner_id]
        self.average_click_cost = (self.config.click_cost_ratio * self.partner_profile["total_sales_value"])\
                                  / self.partner_profile["total_number_of_clicks"]
        self.optimizer = optimizer.optimizer.optimizer(config)
        self.products_to_exclude = []
        self.products_seen_so_far = []
        self.results = []
        self.products_exclusion_history = []
        self.profit_history = []


    def next_day(self):
        today_date = self.data_reader.get_actual_date()
        data = self.data_reader.get_actual_day_data()

        all_todays_products = self.data_reader.get_actual_day_product_list()
        if len(all_todays_products) > 0:
            self.products_to_exclude = self.optimizer.get_excluded_products()
            self.products_seen_so_far = self.optimizer.get_product_seen_so_far_list()
        self.actually_excluded_products = self.__get_actually_excluded_products(all_todays_products)
        products_seen_today = self.__get_products_seen_today(all_todays_products)

        result = simulator.simulation_results.simulation_result_model()
        result.clicks_savings = self.__calculate_click_savings(data, self.actually_excluded_products)
        result.profit_gain = self.__calculate_profit_gain_with_log(data, self.actually_excluded_products, today_date)
        result.profit_losses = self.__calculate_profit_losses(data, self.actually_excluded_products)
        result.sale_losses = self.__calculate_sale_losses(data, self.actually_excluded_products)

        self.results.append(result)
        history = simulator.simulation_results.products_exclusion_history(today_date,
                                                                          products_seen_today,
                                                                          self.products_seen_so_far,
                                                                          self.products_to_exclude,
                                                                          self.actually_excluded_products)
        self.products_exclusion_history.append(history)
        self.optimizer.update_product_list(all_todays_products)
        self.data_reader.next_day()


    def get_results(self):
        partner_results = simulator.simulation_results.partner_simulation_results_model(self.partner_id)
        partner_results.results = self.results
        return partner_results


    def __get_actually_excluded_products(self, all_todays_products: typing.List[str]):
        actually_excluded_products = []
        for product in self.products_to_exclude:
            if product in all_todays_products:
                actually_excluded_products.append(product)
        return actually_excluded_products


    def __get_products_seen_today(self, all_todays_products: typing.List[str]):
        products_seen_today = []
        for product in all_todays_products:
            if product not in self.actually_excluded_products:
                products_seen_today.append(product)
        products_seen_today.sort()
        return products_seen_today


    def __calculate_profit_gain(self, data: pandas.DataFrame, products_excluded: typing.List[str]):
        total_profit_gain = 0
        for product in products_excluded:
            excluded_product_data = data.loc[data['product_id'] == product]
            excluded_product_sale_data = excluded_product_data.loc[excluded_product_data["sale"] == 1]
            excluded_product_total_sales_value = excluded_product_sale_data["sales_amount_in_euro"].sum()
            excluded_product_number_of_clicks = len(excluded_product_data.index)

            profit_gain = excluded_product_number_of_clicks * self.average_click_cost \
                          - excluded_product_total_sales_value * (self.config.npm + self.config.click_cost_ratio)

            total_profit_gain += profit_gain
        print(f"total: {total_profit_gain}")
        return total_profit_gain


    def __calculate_profit_gain_with_log(self, data: pandas.DataFrame, products_excluded: typing.List[str], date: datetime):
        total_profit_gain = 0
        total_number_of_excluded_products_clicks = 0
        total_number_of_sold_products = 0
        total_sales_amount_in_euro = 0
        profit_log = dict()
        profit_log['date'] = date.strftime("%d/%m/%Y")
        for product in products_excluded:
            excluded_product_data = data.loc[data['product_id'] == product]
            excluded_product_sale_data = excluded_product_data.loc[excluded_product_data["sale"] == 1]
            excluded_product_total_sales_value = excluded_product_sale_data["sales_amount_in_euro"].sum()
            excluded_product_number_of_clicks = len(excluded_product_data.index)

            profit_gain = excluded_product_number_of_clicks * self.average_click_cost \
                          - excluded_product_total_sales_value * (self.config.npm + self.config.click_cost_ratio)
            total_profit_gain += profit_gain
            total_number_of_excluded_products_clicks += excluded_product_number_of_clicks
            total_number_of_sold_products += len(excluded_product_sale_data.index)
            total_sales_amount_in_euro += excluded_product_total_sales_value
            profit_log[product] = \
                {
                    'number_of_clicks': excluded_product_number_of_clicks,
                    'number_of_sold_products': len(excluded_product_sale_data.index),
                    'sales_amount_in_euro': excluded_product_total_sales_value,
                    'profit_gain': profit_gain
                }
        profit_log['total_profit_gain'] = total_profit_gain
        profit_log['total_number_of_excluded_products_clicks'] = total_number_of_excluded_products_clicks
        profit_log['total_number_of_sold_excluded_products'] = total_number_of_sold_products
        profit_log['total_excluded_products_sales_amount_in_euro'] = total_sales_amount_in_euro
        self.profit_history.append(profit_log)
        return total_profit_gain


    def __calculate_click_savings(self, data: pandas.DataFrame, products_excluded: typing.List[str]):
        total_click_savings = 0
        for product in products_excluded:
            excluded_product_data = data.loc[data['product_id'] == product]
            excluded_product_number_of_clicks = len(excluded_product_data.index)

            click_savings = excluded_product_number_of_clicks * self.average_click_cost

            total_click_savings += click_savings

        return total_click_savings


    def __calculate_sale_losses(self, data: pandas.DataFrame, products_excluded: typing.List[str]):
        total_sale_losses = 0
        for product in products_excluded:
            excluded_product_data = data.loc[data['product_id'] == product]
            excluded_product_sale_data = excluded_product_data.loc[excluded_product_data["sale"] == 1]
            excluded_product_total_sales_value = excluded_product_sale_data["sales_amount_in_euro"].sum()

            sale_losses = excluded_product_total_sales_value

            total_sale_losses += sale_losses

        return total_sale_losses


    def __calculate_profit_losses(self, data: pandas.DataFrame, products_excluded: typing.List[str]):
        total_profit_losses = 0
        for product in products_excluded:
            excluded_product_data = data.loc[data['product_id'] == product]
            excluded_product_sale_data = excluded_product_data.loc[excluded_product_data["sale"] == 1]
            excluded_product_total_sales_value = excluded_product_sale_data["sales_amount_in_euro"].sum()

            profit_losses = excluded_product_total_sales_value * self.config.npm

            total_profit_losses += profit_losses

        return total_profit_losses
