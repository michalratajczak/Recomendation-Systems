import typing

class simulation_config:
    partners_to_involve_in_simulation: typing.List[str]
    number_of_simulation_steps: int
    npm: float
    how_many_ratio: float
    pseudorandom_seed: int
    click_cost_ratio: float

    def __init__(self,
                 partners: typing.List[str],
                 number_of_steps: int,
                 npm: float,
                 how_many_ratio: float,
                 random_seed: int,
                 click_cost_ratio: float):
        self.partners_to_involve_in_simulation = partners
        self.number_of_simulation_steps = number_of_steps
        self.npm = npm
        self.how_many_ratio = how_many_ratio
        self.pseudorandom_seed = random_seed
        self.click_cost_ratio = click_cost_ratio

    def to_dict(self):
        return \
            {
                'partners_to_involve_in_simulation': self.partners_to_involve_in_simulation,
                'number_of_simulation_steps': self.number_of_simulation_steps,
                'NPM': self.npm,
                'how_many_ratio': self.how_many_ratio,
                'pseudorandom_seed': self.pseudorandom_seed,
                'click_cost_ratio': self.click_cost_ratio
            }