import numpy as np

from config.config import Config
from job.simulate_job import SimulateJob
from simulator.ode_simulator import OdeSimulator
from view.multiple_plot_view import MultiplePlotter


class MultiplePumpSimulateJob(SimulateJob):
    def run(self):
        different_pump_configs = list(map(
            lambda pump:
            Config(
                bd=3.87,
                kappa=5.4,
                b_emission=2.5 * 1e-5,
                molecule_number=6 * 1e9,
                cw_pump=pump,
                perturbation=27 * 1e-6,
                time_range=np.arange(0, 50, 0.1),
                pulse_func=lambda x: np.sin(x)
            ),
            [5.2 * 1e-3, 5.201 * 1e-3, 5.202 * 1e-3, 5.203 * 1e-3, 5.204 * 1e-3]
        ))

        solvers = list(map(
            lambda config: OdeSimulator(config),
            different_pump_configs
        ))

        res = list(map(solve_func, solvers))

        plotter = MultiplePlotter(res)
        plotter.show()


def solve_func(solver: OdeSimulator):
    t, z, n_init, meff_init = solver.run()
    return t, z[:, 1]
