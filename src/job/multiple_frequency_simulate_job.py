import numpy as np
from matplotlib import pyplot as plt

from config.config import Config
from job.simulate_job import SimulateJob
from simulator.ode_simulator import OdeSimulator
from simulator.simulator import Simulator
from view.multiple_frequency_plot_view import MultipleFrequencyPlotter


class MultipleFrequencySimulateJob(SimulateJob):
    # frequencies = [0.1, 0.2, .3, .4, .5, .6]
    frequencies = np.arange(.05, .5, .05)

    def run(self):
        different_pump_configs = list(map(
            lambda frequency:
            Config(
                bd=3.87,
                kappa=7.4,
                b_emission=2.5 * 1e-5,
                molecule_number=6 * 1e9,
                cw_pump=5.235 * 1e-3,
                perturbation=.1 * 1e-6,
                time_range=np.arange(0, 50, 0.01),
                pulse_func=lambda x: np.sin(frequency * 2 * np.pi * x)
            ),
            np.array(self.frequencies)
        ))

        solvers = list(map(
            lambda config: OdeSimulator(config),
            different_pump_configs
        ))

        res = list(map(solve_func, solvers))

        plotter = MultipleFrequencyPlotter(res, self.frequencies)
        plotter.show()


def solve_func(solver: Simulator):
    t, z, n_init, meff_init = solver.run()
    return t, z[:, 1]