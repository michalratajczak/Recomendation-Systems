import partners.partner_data_reader
import partners.partners_profiles
import simulator.simulation_config
import simulator.simulation_results
import optimizer.optimizer
import typing
import random

class partner_simulator:
    config: simulator.simulation_config.simulation_config
    partner_id: str
    data_reader: partners.partner_data_reader
    partner_profile: dict
    average_click_cost: float

    optimizer: optimizer.optimizer.optimizer

    results: typing.List[simulator.simulation_results.simulation_result_model]

    def __init__(self, partner_id: str, config: simulator.simulation_config.simulation_config):
        self.partner_id = partner_id
        self.config = config
        self.data_reader = partners.partner_data_reader.partner_data_reader(partner_id)
        self.partner_profile = partners.partners_profiles.profiles[partner_id]
        self.average_click_cost = (self.config.click_cost_ratio * self.partner_profile["total_sales_value"]) \
                                  / self.partner_profile["total_number_of_clicks"]
        self.optimizer = optimizer.optimizer.optimizer()
        self.results = []


    def next_day(self):
        data = self.data_reader.next_day()
        result = simulator.simulation_results.simulation_result_model()

        #TODO

        self.results.append(result)


    def get_results(self):
        partner_results = simulator.simulation_results.partner_simulation_results_model(self.partner_id)
        partner_results.results = self.results
        return partner_results