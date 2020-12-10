import random
import typing
import simulator.simulation_config

class optimizer:
    __products: typing.List[str]
    __excluded_products: typing.List[str]
    __config: simulator.simulation_config.simulation_config

    def __init__(self, config: simulator.simulation_config.simulation_config):
        self.__config = config
        self.__products = []
        self.__excluded_products = []


    def get_excluded_products(self):
        self.__exclude_products_pseudorandomly()
        return self.__excluded_products


    def __exclude_products_pseudorandomly(self):
        potentially_excluded_products = self.__products
        potentially_excluded_products = list(potentially_excluded_products)
        potentially_excluded_products.sort()

        number_of_products_to_exclude = round(len(potentially_excluded_products) / self.__config.how_many_ratio)
        random.seed(self.__config.pseudorandom_seed)

        self.__excluded_products = random.sample(potentially_excluded_products, number_of_products_to_exclude)


    def update_product_list(self, products_seen_today):
        for product in products_seen_today:
            if product not in self.__products:
                self.__products.append(product)


    def get_product_list(self):
        return self.__products