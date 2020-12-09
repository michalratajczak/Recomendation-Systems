import random
import typing
import simulator.simulation_config

class optimizer:
    products: typing.List[str]
    config: simulator.simulation_config.simulation_config

    def __init__(self, config: simulator.simulation_config.simulation_config):
        self.config = config
        self.products = []


    def get_excluded_products(self, daily_products: typing.List[str]):
        for product in daily_products:
            if product not in self.products:
                self.products.append(product)

        return self.__get_excluded_products_pseudorandomly()

    def __get_excluded_products_pseudorandomly(self):
        potentially_excluded_products = self.products
        potentially_excluded_products = list(potentially_excluded_products)
        potentially_excluded_products.sort()

        number_of_products_to_exclude = round(len(potentially_excluded_products) / self.config.how_many_ratio)
        random.seed(self.config.pseudorandom_seed)

        excluded_products = random.sample(potentially_excluded_products, number_of_products_to_exclude)
        return excluded_products