import typing
import simulator.partner_simulator
import simulator.simulation_config
import simulator.simulation_results

class simulator_core:
    partner_simulators: typing.List[simulator.partner_simulator.partner_simulator]
    config: simulator.simulation_config.simulation_config

    def __init__(self, config: simulator.simulation_config.simulation_config):
        self.config = config
        self.partner_simulators = []

        for partner_id in config.partners_to_involve_in_simulation:
            sim = simulator.partner_simulator.partner_simulator(partner_id, config)
            self.partner_simulators.append(sim)


    def run_simulation(self):
        for day in range(0, self.config.number_of_simulation_steps):
            for simulator in self.partner_simulators:
                simulator.next_day()


    def save_results(self):
        results = []
        for partner_simulator in self.partner_simulators:
            result = partner_simulator.get_results()
            results.append(result)

        report = simulator.simulation_results.generate_results_report(results)
        simulator.simulation_results.save_results_report(report, self.config.to_dict())