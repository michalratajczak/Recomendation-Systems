import typing

class simulation_config:
    partners_to_involve_in_simulation: typing.List[str]
    number_of_simulation_steps: int
    npm: float
    click_cost_ratio: float
    exclusion_strategy: str
    how_many_ratio: float
    pseudorandom_seed: int
    profit_threshold: float

    def __init__(self,
                 partners: typing.List[str],
                 number_of_steps: int,
                 npm: float,
                 click_cost_ratio: float,
                 exclusion_strategy: str,
                 how_many_ratio: float,
                 random_seed: int,
                 profit_threshold: float):
        self.partners_to_involve_in_simulation = partners
        self.number_of_simulation_steps = number_of_steps
        self.npm = npm
        self.click_cost_ratio = click_cost_ratio
        self.exclusion_strategy = exclusion_strategy
        self.how_many_ratio = how_many_ratio
        self.pseudorandom_seed = random_seed
        self.profit_threshold = profit_threshold


    def to_dict(self):
        return \
            {
                'partners_to_involve_in_simulation': self.partners_to_involve_in_simulation,
                'number_of_simulation_steps': self.number_of_simulation_steps,
                'NPM': self.npm,
                'click_cost_ratio': self.click_cost_ratio,
                'exclusion_strategy': self.exclusion_strategy,
                'how_many_ratio': self.how_many_ratio,
                'pseudorandom_seed': self.pseudorandom_seed,
                'profit_threshold': self.profit_threshold
            }

def from_dict(dictionary: dict):
    config = simulation_config(
        dictionary["partners_to_involve_in_simulation"],
        dictionary["number_of_simulation_steps"],
        dictionary["NPM"],
        dictionary["click_cost_ratio"],
        dictionary["exclusion_strategy"],
        dictionary["how_many_ratio"],
        dictionary["pseudorandom_seed"],
        dictionary["profit_threshold"])
    return config