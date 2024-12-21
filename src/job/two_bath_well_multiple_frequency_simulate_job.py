import numpy as np

from config.config import Config
from job.simulate_job import SimulateJob
from simulator.simulator import Simulator
from simulator.two_batch_double_well_ode_simulator import TwoBatchDoubleWellOdeSimulator
from view.multiple_frequency_plot_view import MultipleFrequencyPlotter


class TwoBathWellMultipleFrequencySimulateJob(SimulateJob):
    frequencies = np.arange(.05, .5, .05)

    def run(self):
        different_pump_configs = list(map(
            lambda frequency:
            Config(
                cw_pump=5.232 * 1e-3,
                well_coupling=5,
                pulse_func=lambda x: np.sin(frequency * 2 * np.pi * x),
            ),
            np.array(self.frequencies)
        ))

        solvers = list(map(
            lambda config: TwoBatchDoubleWellOdeSimulator(config),
            different_pump_configs
        ))

        res = list(map(solve_func, solvers))

        plotter = MultipleFrequencyPlotter(res, self.frequencies)
        plotter.show()


def solve_func(solver: Simulator):
    t, z, n1_init, n2_init, m_exited1_init, m_exited2_init = solver.run()
    return t, z[:, 1]
