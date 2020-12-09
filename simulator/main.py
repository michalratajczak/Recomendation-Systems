import simulator.simulator_core
import simulator.simulation_config

configuration = \
    {
        "partners_to_involve_in_simulation": [
            "C0F515F0A2D0A5D9F854008BA76EB537"
        ],
        "number_of_simulation_steps": 40,
        "NPM": 0.1,
        "how_many_ratio": 20,
        "pseudorandom_seed": 12,
        "click_cost_ratio": 0.12
    }


def run():
    config = simulator.simulation_config.from_dict(configuration)
    s = simulator.simulator_core.simulator_core(config)
    s.run_simulation()
    s.save_results()

if __name__ == "__main__":
    run()