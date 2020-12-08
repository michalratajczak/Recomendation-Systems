import random
import typing
import simulator.simulation_config

class optimizer:
    products: typing.List[str]
    config: simulator.simulation_config.simulation_config

    def __init__(self, config: simulator.simulation_config.simulation_config):
        self.config = config
        self.products = []

    def next_day(self):
        pass

    def get_products_seen_today(self):
        pass

    def get_excluded_products(self):
        return self.__get_excluded_products_pseudorandomly()

    def __get_excluded_products_pseudorandomly(self):
        dummy_list_of_potentially_excluded_products = self.products

        dummy_list_of_potentially_excluded_products = list(dummy_list_of_potentially_excluded_products)
        dummy_list_of_potentially_excluded_products.sort()
        dummy_how_many_products = round(len(dummy_list_of_potentially_excluded_products) / self.config.how_many_ratio)

        random.seed(self.config.pseudorandom_seed)
        excluded_products = random.sample(dummy_list_of_potentially_excluded_products, dummy_how_many_products)
        return excluded_products