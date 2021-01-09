import random
import typing
import simulator.simulation_config

class optimizer:
    __product_sales_info: dict
    __excluded_products: typing.List[str]

    __config: simulator.simulation_config.simulation_config
    __click_cost: float

    def __init__(self, config: simulator.simulation_config.simulation_config, click_cost: float):
        self.__config = config
        self.__click_cost = click_cost
        self.__excluded_products = []
        self.__product_sales_info = dict()


    def get_excluded_products(self):
        if self.__config.exclusion_strategy == "pseudorandom":
            self.__exclude_products_pseudorandomly()
        elif self.__config.exclusion_strategy == "history-based":
            self.__exclude_loss_making_products()
        self.__excluded_products.sort()
        return self.__excluded_products


    def __exclude_products_pseudorandomly(self):
        potentially_excluded_products = list(self.__product_sales_info.keys())
        potentially_excluded_products.sort()

        number_of_products_to_exclude = round(len(potentially_excluded_products) / self.__config.how_many_ratio)
        random.seed(self.__config.pseudorandom_seed)

        self.__excluded_products = random.sample(potentially_excluded_products, number_of_products_to_exclude)


    def __exclude_loss_making_products(self):
        products = self.__product_sales_info.copy()
        excluded_products = []
        for product in products.keys():
            profit = products[product]['total_number_of_clicks'] * self.__click_cost\
                     - products[product]['total_sales_amount_in_euro'] * (self.__config.npm + self.__config.click_cost_ratio)
            if profit > self.__config.profit_threshold:
                excluded_products.append(product)

        self.__excluded_products = excluded_products


    def update_product_list(self, products_info: dict):
        for product in products_info.keys():
            if product not in self.__product_sales_info.keys():
                self.__product_sales_info[product] = dict()
                self.__product_sales_info[product]['total_number_of_clicks'] = 0
                self.__product_sales_info[product]['total_sales_amount_in_euro'] = 0
            self.__product_sales_info[product]['total_number_of_clicks'] += products_info[product]['total_number_of_clicks']
            self.__product_sales_info[product]['total_sales_amount_in_euro'] += products_info[product]['total_sales_amount_in_euro']


    def get_product_seen_so_far_list(self):
        products = list(self.__product_sales_info.keys())
        products.sort()
        return products