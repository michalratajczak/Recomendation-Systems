import matplotlib.pyplot as plt

def render_profit_gain_chart(report: dict, partner_id: str):
    profit_list = report["reoriented_for_each_partner"][partner_id]["profit_gain"]
    days = list(range(0, len(profit_list)))

    plt.plot(days, profit_list, color='orange')
    plt.xlabel('Day of simulation')
    plt.ylabel('EURO')
    plt.title(f'Profit gain for partner {partner_id}')
    plt.show()

def render_accumulated_profit_gain_chart(report: dict, partner_id: str):
    profit_list = report["reoriented_for_each_partner"][partner_id]["profit_gain"]
    days = list(range(0, len(profit_list)))
    accumulated_profits = []
    for i in range(0, len(profit_list)):
        sum = 0
        for j in range(0, i):
            sum+=profit_list[j]
        accumulated_profits.append(sum)

    plt.plot(days, accumulated_profits, color='orange')
    plt.xlabel('Day of simulation')
    plt.ylabel('EURO')
    plt.title(f'Accumulated profit gain for partner {partner_id}')
    plt.show()