import numpy as np

from config.config import Config
from job.simulate_job import SimulateJob
from simulator.one_batch_double_well_ode_simulator import OneBatchDoubleWellOdeSimulator
from simulator.simulator import Simulator
from view.multiple_frequency_plot_view import MultipleFrequencyPlotter


class WellMultipleFrequencySimulateJob(SimulateJob):
    frequencies = np.arange(.05, .5, .025)

    def run(self):
        different_pump_configs = list(map(
            lambda frequency:
            Config(
                pulse_func=lambda x: np.sin(frequency * 2 * np.pi * x),
            ),
            np.array(self.frequencies)
        ))

        solvers = list(map(
            lambda config: OneBatchDoubleWellOdeSimulator(config),
            different_pump_configs
        ))

        res = list(map(solve_func, solvers))

        plotter = MultipleFrequencyPlotter(res, self.frequencies)
        plotter.show()


def solve_func(solver: Simulator):
    t, z, n1_init, n2_init, m_exited_init = solver.run()
    return t, z[:, 1]
