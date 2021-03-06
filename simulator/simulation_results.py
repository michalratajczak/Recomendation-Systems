import os
import random
import app_config
import datetime
import typing
import json
import helpers.console_logger
import simulator.simulation_config
import simulator.simulation_results_visualization as srv

#region models
class simulation_result_model:
    clicks_savings: float
    sale_losses: float
    profit_losses: float
    profit_gain: float

    def __init__(self):
        self.clicks_savings = 0
        self.sale_losses = 0
        self.profit_losses = 0
        self.profit_gain = 0

    def to_dict(self):
        return \
            {
                'clicks_savings': self.clicks_savings,
                'sale_losses': self.sale_losses,
                'profit_losses': self.profit_losses,
                'profit_gain': self.profit_gain
            }


class aggregated_partner_simulation_results_model(simulation_result_model):
    partner_id: str

    def __init__(self, partner_id):
        super().__init__()
        self.partner_id = partner_id


class partner_simulation_results_model:
    partner_id: str
    results: typing.List[simulation_result_model]

    def __init__(self, partner_id):
        self.partner_id = partner_id
        self.results = []

    def to_dict(self):
        return [result.to_dict() for result in self.results]


class reoriented_partner_simulation_results_model:
    partner_id: str
    clicks_savings: typing.List[float]
    sale_losses: typing.List[float]
    profit_losses: typing.List[float]
    profit_gain: typing.List[float]

    def __init__(self, partner_id):
        self.partner_id = partner_id
        self.clicks_savings = []
        self.sale_losses = []
        self.profit_losses = []
        self.profit_gain = []

    def to_dict(self):
        return \
            {
                'clicks_savings': self.clicks_savings,
                'sale_losses': self.sale_losses,
                'profit_losses': self.profit_losses,
                'profit_gain': self.profit_gain
            }


class aggregated_all_partners_simulation_results_model:
    clicks_savings: typing.List[float]
    sale_losses: typing.List[float]
    profit_losses: typing.List[float]
    profit_gain: typing.List[float]

    def __init__(self):
        self.clicks_savings = []
        self.sale_losses = []
        self.profit_losses = []
        self.profit_gain = []

    def to_dict(self):
        return \
            {
                'clicks_savings': self.clicks_savings,
                'sale_losses': self.sale_losses,
                'profit_losses': self.profit_losses,
                'profit_gain': self.profit_gain
            }


class products_exclusion_history:
    date: datetime
    products_seen_today: typing.List[str]
    products_seen_so_far: typing.List[str]
    products_to_exclude: typing.List[str]
    products_actually_excluded: typing.List[str]

    def __init__(self, date: datetime,
                 products_seen_today: typing.List[str],
                 products_seen_so_far: typing.List[str],
                 products_to_exclude: typing.List[str],
                 products_actually_excluded: typing.List[str]):
        self.date = date
        self.products_seen_today = products_seen_today
        self.products_seen_so_far = products_seen_so_far
        self.products_to_exclude = products_to_exclude
        self.products_actually_excluded = products_actually_excluded
#endregion


#region functions
def __reorient_partner_simulation_results(results: partner_simulation_results_model):
    reoriented_results = reoriented_partner_simulation_results_model(results.partner_id)
    for result in results.results:
        reoriented_results.clicks_savings.append(result.clicks_savings)
        reoriented_results.sale_losses.append(result.sale_losses)
        reoriented_results.profit_losses.append(result.profit_losses)
        reoriented_results.profit_gain.append(result.profit_gain)
    return reoriented_results


def __aggregate_partner_simulation_results(results: reoriented_partner_simulation_results_model):
    aggregated_results = aggregated_partner_simulation_results_model(results.partner_id)
    aggregated_results.clicks_savings = sum(results.clicks_savings)
    aggregated_results.sale_losses = sum(results.sale_losses)
    aggregated_results.profit_losses = sum(results.profit_losses)
    aggregated_results.profit_gain = sum(results.profit_gain)
    return aggregated_results


def __aggregate_all_partners_simulation_results(results: typing.List[aggregated_partner_simulation_results_model]):
    aggregated_results = aggregated_all_partners_simulation_results_model()
    for partner_results in results:
        aggregated_results.clicks_savings.append(partner_results.clicks_savings)
        aggregated_results.sale_losses.append(partner_results.sale_losses)
        aggregated_results.profit_losses.append(partner_results.profit_losses)
        aggregated_results.profit_gain.append(partner_results.profit_gain)
    return aggregated_results


def __sum_all_partners_simulation_results(results: aggregated_all_partners_simulation_results_model):
    summed_results = simulation_result_model()
    summed_results.clicks_savings = sum(results.clicks_savings)
    summed_results.sale_losses = sum(results.sale_losses)
    summed_results.profit_losses = sum(results.profit_losses)
    summed_results.profit_gain = sum(results.profit_gain)
    return summed_results


def generate_results_report(partner_results: typing.List[partner_simulation_results_model]):
    report = dict()
    report['for_individual_partners'] = dict()
    report['reoriented_for_each_partner'] = dict()
    report['aggregated_for_each_partner'] = dict()
    aggregated_partner_results_list = []
    logger = helpers.console_logger.console_logger("Generating report")
    for partner in partner_results:
        logger.log(f"processing partner {partner.partner_id}")
        reoriented_results = __reorient_partner_simulation_results(partner)
        aggregated_partner_result = __aggregate_partner_simulation_results(reoriented_results)
        aggregated_partner_results_list.append(aggregated_partner_result)

        report['for_individual_partners'][partner.partner_id] = partner.to_dict()
        report['reoriented_for_each_partner'][partner.partner_id] = reoriented_results.to_dict()
        report['aggregated_for_each_partner'][partner.partner_id] = aggregated_partner_result.to_dict()

    logger.log("merging")
    aggregated_all_partners_results = __aggregate_all_partners_simulation_results(aggregated_partner_results_list)
    report['aggregated_for_all_partners'] = aggregated_all_partners_results.to_dict()
    report['summed_for_all_partners'] = __sum_all_partners_simulation_results(aggregated_all_partners_results).to_dict()
    logger.log_total_time()
    return report


def save_results_report(report: dict, simulation_config: dict,
                        exclusion_history: dict = None,
                        profit_history: dict = None,
                        render_charts: bool = False):
    if not os.path.exists(app_config.app_config['results_dir']):
        os.makedirs(app_config.app_config['results_dir'])

    logger = helpers.console_logger.console_logger("Saving report")
    name = datetime.datetime.now().strftime("%d%m%y_%H%M%S")
    if not os.path.exists(os.path.join(app_config.app_config['results_dir'], name)):
        os.makedirs(os.path.join(app_config.app_config['results_dir'], name))
    with open(os.path.join(app_config.app_config['results_dir'], name, 'results.json'), 'w') as f:
        logger.log("saving results report")
        f.write(json.dumps(report, indent=4))
    with open(os.path.join(app_config.app_config['results_dir'], name, 'config.json'), 'w') as f:
        logger.log("saving simulation configuration")
        f.write(json.dumps(simulation_config, indent=4))
    if exclusion_history is not None:
        for partner in exclusion_history.keys():
            logger.log(f"saving products exclusion history for partner {partner}")
            path = os.path.join(app_config.app_config['results_dir'], name, partner, 'products_exclusion_history')
            if not os.path.exists(path):
                os.makedirs(path)
            #notation A reports:
            with open(os.path.join(path, 'notation_A_short_report.json'), 'w') as f:
                f.write(json.dumps(notation_A_short_report(exclusion_history[partner]), indent=4))
            with open(os.path.join(path, 'notation_A_medium_report.json'), 'w') as f:
                f.write(json.dumps(notation_A_medium_report(exclusion_history[partner]), indent=4))
            with open(os.path.join(path, 'notation_A_full_report.json'), 'w') as f:
                f.write(json.dumps(notation_A_full_report(exclusion_history[partner]), indent=4))
            #notation B reports:
            with open(os.path.join(path, 'notation_B_short_report.json'), 'w') as f:
                f.write(json.dumps(notation_B_short_report(exclusion_history[partner]), indent=4))
            with open(os.path.join(path, 'notation_B_medium_report.json'), 'w') as f:
                f.write(json.dumps(notation_B_medium_report(exclusion_history[partner]), indent=4))
            with open(os.path.join(path, 'notation_B_full_report.json'), 'w') as f:
                f.write(json.dumps(notation_B_full_report(exclusion_history[partner]), indent=4))
    if profit_history is not None:
        for partner in profit_history.keys():
            logger.log(f"saving products profit history for partner {partner}")
            path = os.path.join(app_config.app_config['results_dir'], name, partner)
            if not os.path.exists(path):
                os.makedirs(path)
            with open(os.path.join(path, 'profit_gain_history.json'), 'w') as f:
                f.write(json.dumps(profit_history[partner], indent=4))
    if render_charts is True:
        for partner in report['for_individual_partners'].keys():
            logger.log(f"rendering and saving charts for partner {partner}")
            path = os.path.join(app_config.app_config['results_dir'], name, partner, 'charts')
            if not os.path.exists(path):
                os.makedirs(path)
            srv.render_profit_gain_chart(report, partner, os.path.join(path, 'profit_gain.png'))
            srv.render_accumulated_profit_gain_chart(report, partner, os.path.join(path, 'accumulated_profit_gain.png'))
            srv.render_clicks_savings_chart(report, partner, os.path.join(path, 'clicks_savings.png'))
            srv.render_profit_losses_chart(report, partner, os.path.join(path, 'profit_losses.png'))
            srv.render_sale_losses_chart(report, partner, os.path.join(path, 'sale_losses.png'))
    logger.log_total_time()


#endregion


#region variants of the generated report
def notation_A_short_report(history: typing.List[products_exclusion_history]):
    report = dict()
    for day in history:
        key = day.date.strftime('%d/%m/%Y')
        report[key] = dict()
        report[key]['products_to_exclude'] = day.products_to_exclude
        report[key]['products_actually_excluded'] = day.products_actually_excluded
    return report


def notation_A_medium_report(history: typing.List[products_exclusion_history]):
    report = dict()
    for day in history:
        key = day.date.strftime('%d/%m/%Y')
        report[key] = dict()
        report[key]['products_seen_so_far'] = day.products_seen_so_far
        report[key]['products_to_exclude'] = day.products_to_exclude
        report[key]['products_actually_excluded'] = day.products_actually_excluded
    return report


def notation_A_full_report(history: typing.List[products_exclusion_history]):
    report = dict()
    for day in history:
        key = day.date.strftime('%d/%m/%Y')
        report[key] = dict()
        report[key]['products_seen_so_far'] = day.products_seen_so_far
        report[key]['products_seen_today'] = day.products_seen_today
        report[key]['products_to_exclude'] = day.products_to_exclude
        report[key]['products_actually_excluded'] = day.products_actually_excluded
    return report


def notation_B_short_report(history: typing.List[products_exclusion_history]):
    report = dict()
    report['days'] = []
    for day in history:
        r = dict()
        r['day'] = day.date.strftime('%Y-%m-%d')
        r['productsToExclude'] = day.products_to_exclude
        r['productsActuallyExcluded'] = day.products_actually_excluded
        report['days'].append(r)
    return report


def notation_B_medium_report(history: typing.List[products_exclusion_history]):
    report = dict()
    report['days'] = []
    for day in history:
        r = dict()
        r['day'] = day.date.strftime('%Y-%m-%d')
        r['productsSeenSoFar'] = day.products_seen_so_far
        r['productsToExclude'] = day.products_to_exclude
        r['productsActuallyExcluded'] = day.products_actually_excluded
        report['days'].append(r)
    return report


def notation_B_full_report(history: typing.List[products_exclusion_history]):
    report = dict()
    report['days'] = []
    for day in history:
        r = dict()
        r['day'] = day.date.strftime('%Y-%m-%d')
        r['productsSeenSoFar'] = day.products_seen_so_far
        r['productsSeenToday'] = day.products_seen_today
        r['productsToExclude'] = day.products_to_exclude
        r['productsActuallyExcluded'] = day.products_actually_excluded
        report['days'].append(r)
    return report

#endregion


#region example results report generator
def example_result_report_generator(config: simulator.simulation_config.simulation_config):
    partners_results: typing.List[partner_simulation_results_model] = []
    for partner_id in config.partners_to_involve_in_simulation:
        partner_result = partner_simulation_results_model(partner_id)
        for x in range(config.number_of_simulation_steps):
            result = simulation_result_model()
            result.clicks_savings = random.random()
            result.sale_losses = random.random()
            result.profit_losses = random.random()
            result.profit_gain = random.random()
            partner_result.results.append(result)
        partners_results.append(partner_result)

    report = generate_results_report(partners_results)
    save_results_report(report, config.to_dict())


if __name__ == "__main__":
    config = simulator.simulation_config.simulation_config(['C0F515F0A2D0A5D9F854008BA76EB537',
                                                            'BD01BAFAE73CF38C403978BBB458300C',
                                                            'C4D189327BD87FEB3BF896DA716C6995',
                                                            '440255DF62CFD36FBC0206828FC488E0'],
                                                            10, 0.1, 3.1, 12, 0.12)
    example_result_report_generator(config)
#endregion