import os
import random
import config
import datetime
import typing
import json

#region models
from partners.partners_list import partners


class simulation_result_model:
    clicks_savings: float
    sale_losses: float
    profit_losses: float
    profit_gain: float

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
#endregion


#region functions
def _reorient_partner_simulation_results(results: partner_simulation_results_model):
    reoriented_results = reoriented_partner_simulation_results_model(results.partner_id)
    for result in results.results:
        reoriented_results.clicks_savings.append(result.clicks_savings)
        reoriented_results.sale_losses.append(result.sale_losses)
        reoriented_results.profit_losses.append(result.sale_losses)
        reoriented_results.profit_gain.append(result.profit_gain)
    return reoriented_results


def _aggregate_partner_simulation_results(results: reoriented_partner_simulation_results_model):
    aggregated_results = aggregated_partner_simulation_results_model(results.partner_id)
    aggregated_results.clicks_savings = sum(results.clicks_savings)
    aggregated_results.sale_losses = sum(results.sale_losses)
    aggregated_results.profit_losses = sum(results.profit_losses)
    aggregated_results.profit_gain = sum(results.profit_gain)
    return aggregated_results


def _aggregate_all_partners_simulation_results(results: typing.List[aggregated_partner_simulation_results_model]):
    aggregated_results = aggregated_all_partners_simulation_results_model()
    for partner_results in results:
        aggregated_results.clicks_savings.append(partner_results.clicks_savings)
        aggregated_results.sale_losses.append(partner_results.sale_losses)
        aggregated_results.profit_losses.append(partner_results.profit_losses)
        aggregated_results.profit_gain.append(partner_results.profit_gain)
    return aggregated_results


def _sum_all_partners_simulation_results(results: aggregated_all_partners_simulation_results_model):
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

    for partner in partner_results:
        reoriented_results = _reorient_partner_simulation_results(partner)
        aggregated_partner_result = _aggregate_partner_simulation_results(reoriented_results)
        aggregated_partner_results_list.append(aggregated_partner_result)

        report['for_individual_partners'][partner.partner_id] = partner.to_dict()
        report['reoriented_for_each_partner'][partner.partner_id] = reoriented_results.to_dict()
        report['aggregated_for_each_partner'][partner.partner_id] = aggregated_partner_result.to_dict()

    aggregated_all_partners_results = _aggregate_all_partners_simulation_results(aggregated_partner_results_list)
    report['aggregated_for_all_partners'] = aggregated_all_partners_results.to_dict()
    report['summed_for_all_partners'] = _sum_all_partners_simulation_results(aggregated_all_partners_results).to_dict()
    return report


def save_results_report(report: dict, simulation_config: dict):
    if not os.path.exists(os.path.join(config.config['root_dir'], 'results')):
        os.makedirs(os.path.join(config.config['root_dir'], 'results'))

    name = datetime.datetime.now().strftime("%d%m%y_%H%M%S")
    if not os.path.exists(os.path.join(config.config['root_dir'], 'results', name)):
        os.makedirs(os.path.join(config.config['root_dir'], 'results', name))
        with open(os.path.join(config.config['root_dir'], 'results', name, 'results.txt'), 'w') as f:
            f.write(json.dumps(report, indent=4))
        with open(os.path.join(config.config['root_dir'], 'results', name, 'config.txt'), 'w') as f:
            f.write(json.dumps(simulation_config, indent=4))
#endregion


#region example results report generator
def _example_result_report_generator():
    partners_ids = partners.partners_list.partners[:3]
    partners_results: typing.List[partner_simulation_results_model] = []
    for partner_id in partners_ids:
        partner_result = partner_simulation_results_model(partner_id)
        for x in range(5):
            result = simulation_result_model()
            result.clicks_savings = random.random()
            result.sale_losses = random.random()
            result.profit_losses = random.random()
            result.profit_gain = random.random()
            partner_result.results.append(result)
        partners_results.append(partner_result)

    report = generate_results_report(partners_results)
    save_results_report(report, report)

if __name__ == "__main__":
    _example_result_report_generator()
#endregion