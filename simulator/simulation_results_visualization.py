import matplotlib.pyplot as plt

def render_profit_gain_chart(report: dict, partner_id: str, path: str):
    _list = report["reoriented_for_each_partner"][partner_id]["profit_gain"]
    days = list(range(0, len(_list)))

    plt.plot(days, _list, color='orange')
    plt.xlabel('Day of simulation')
    plt.ylabel('EURO')
    plt.title(f'Profit gain for partner {partner_id}')
    plt.savefig(path)
    plt.clf()

def render_accumulated_profit_gain_chart(report: dict, partner_id: str, path: str):
    _list = report["reoriented_for_each_partner"][partner_id]["profit_gain"]
    days = list(range(0, len(_list)))
    accumulated_list = []
    for i in range(0, len(_list)):
        sum = 0
        for j in range(0, i):
            sum+=_list[j]
        accumulated_list.append(sum)

    plt.plot(days, accumulated_list, color='orange')
    plt.xlabel('Day of simulation')
    plt.ylabel('EURO')
    plt.title(f'Accumulated profit gain for partner {partner_id}')
    plt.savefig(path)
    plt.clf()

def render_clicks_savings_chart(report: dict, partner_id: str, path: str):
    _list = report["reoriented_for_each_partner"][partner_id]["clicks_savings"]
    days = list(range(0, len(_list)))

    plt.plot(days, _list, color='orange')
    plt.xlabel('Day of simulation')
    plt.ylabel('EURO')
    plt.title(f'Clicks savings for partner {partner_id}')
    plt.savefig(path)
    plt.clf()

def render_sale_losses_chart(report: dict, partner_id: str, path: str):
    _list = report["reoriented_for_each_partner"][partner_id]["sale_losses"]
    days = list(range(0, len(_list)))

    plt.plot(days, _list, color='orange')
    plt.xlabel('Day of simulation')
    plt.ylabel('EURO')
    plt.title(f'Sale losses for partner {partner_id}')
    plt.savefig(path)
    plt.clf()

def render_profit_losses_chart(report: dict, partner_id: str, path: str):
    _list = report["reoriented_for_each_partner"][partner_id]["profit_losses"]
    days = list(range(0, len(_list)))

    plt.plot(days, _list, color='orange')
    plt.xlabel('Day of simulation')
    plt.ylabel('EURO')
    plt.title(f'Profit losses for partner {partner_id}')
    plt.savefig(path)
    plt.clf()