import typing
import helpers.console_logger
import simulator.partner_simulator
import simulator.simulation_config
import simulator.simulation_results
import simulator.simulation_results_visualization

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
        logger = helpers.console_logger.console_logger("Simulation")
        logger.log("starting...")
        counter = 1
        for day in range(0, self.config.number_of_simulation_steps):
            logger.log(f"day {counter}/{self.config.number_of_simulation_steps}")
            for simulator in self.partner_simulators:
                simulator.next_day()
            counter+=1
        logger.log_total_time()


    def save_results(self):
        results = []
        partners_product_exclusion_history = dict()
        partners_profit_gain_history = dict()
        logger = helpers.console_logger.console_logger("Collecting data")
        for partner_simulator in self.partner_simulators:
            logger.log(f"partner {partner_simulator.partner_id}")
            result = partner_simulator.get_results()
            results.append(result)
            partners_product_exclusion_history[partner_simulator.partner_id] = partner_simulator.products_exclusion_history
            partners_profit_gain_history[partner_simulator.partner_id] = partner_simulator.profit_history
        report = simulator.simulation_results.generate_results_report(results)
        simulator.simulation_results.save_results_report(report,
                                                         self.config.to_dict(),
                                                         exclusion_history=partners_product_exclusion_history,
                                                         profit_history=partners_profit_gain_history,
                                                         render_charts=True)