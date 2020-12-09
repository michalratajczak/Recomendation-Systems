import partners.partner_data_reader
import partners.partners_profiles
import simulator.simulation_config
import simulator.simulation_results
import optimizer.optimizer
import typing
import pandas

class partner_simulator:
    config: simulator.simulation_config.simulation_config
    partner_id: str
    data_reader: partners.partner_data_reader
    partner_profile: dict
    average_click_cost: float

    optimizer: optimizer.optimizer.optimizer
    excluded_products: typing.List[str]

    results: typing.List[simulator.simulation_results.simulation_result_model]
    products_exclusion_history: dict

    def __init__(self, partner_id: str, config: simulator.simulation_config.simulation_config):
        self.partner_id = partner_id
        self.config = config
        self.data_reader = partners.partner_data_reader.partner_data_reader(partner_id)
        self.partner_profile = partners.partners_profiles.profiles[partner_id]
        self.average_click_cost = (self.config.click_cost_ratio * self.partner_profile["total_sales_value"])\
                                  / self.partner_profile["total_number_of_clicks"]
        self.optimizer = optimizer.optimizer.optimizer(config)
        self.excluded_products = []
        self.results = []
        self.products_exclusion_history = dict()


    def next_day(self):
        today_date = self.data_reader.get_actual_date()
        all_todays_products = self.data_reader.get_actual_day_product_list()
        products_seen_today = self.__get_products_seen_today(all_todays_products)
        data = self.data_reader.next_day()
        if len(data.index) == 0:
            return

        result = simulator.simulation_results.simulation_result_model()
        result.clicks_savings = 0
        result.profit_gain = self.__calculate_profit_gain(data, self.excluded_products)
        result.profit_losses = 0
        result.sale_losses = 0

        self.results.append(result)
        self.products_exclusion_history[today_date.strftime('%d/%m/%y')] = self.excluded_products
        self.excluded_products = self.optimizer.get_excluded_products(all_todays_products)


    def get_results(self):
        partner_results = simulator.simulation_results.partner_simulation_results_model(self.partner_id)
        partner_results.results = self.results
        return partner_results


    def __get_products_seen_today(self, products: typing.List[str]):
        products_seen_today = []
        for product in products:
            if product not in self.excluded_products:
                products_seen_today.append(product)

        return products_seen_today


    def __calculate_profit_gain(self, data: pandas.DataFrame, products_excluded: typing.List[str]):
        total_profit_gain = 0
        for product in products_excluded:
            excluded_product_data = data.loc[data['product_id'] == product]
            excluded_product_total_sales_value = excluded_product_data["sales_amount_in_euro"].sum()
            excluded_product_number_of_clicks = len(excluded_product_data.index)

            profit_gain = excluded_product_number_of_clicks * self.average_click_cost \
                          - excluded_product_total_sales_value * 0.22

            total_profit_gain += profit_gain

        return total_profit_gain


