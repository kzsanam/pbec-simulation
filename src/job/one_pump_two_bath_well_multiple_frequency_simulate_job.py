import numpy as np

from config.config import Config
from job.simulate_job import SimulateJob
from simulator.one_pump_two_batch_double_well_ode_simulator import \
    OnePumpTwoBatchDoubleWellOdeSimulator
from simulator.simulator import Simulator
from view.double_well_multiple_frequency_plot_view import DoubleWellMultipleFrequencyPlotter


class OnePumpTwoBathWellMultipleFrequencySimulateJob(SimulateJob):
    frequencies = np.arange(.1, 1, .01)

    def run(self):
        different_pump_configs = list(map(
            lambda frequency:
            Config(
                time_range=np.arange(0, 50, 0.01),
                molecule_number=2*6*1e9,
                perturbation=.1 * 1e-6,
                cw_pump=5.23 * 1e-3,
                well_coupling=.002,
                # pulse_func=lambda x: 0 * x,
                pulse_func=lambda x: np.sin(frequency * 2 * np.pi * x),
            ),
            np.array(self.frequencies)
        ))

        solvers = list(map(
            lambda config: OnePumpTwoBatchDoubleWellOdeSimulator(config),
            different_pump_configs
        ))

        res = list(map(solve_func, solvers))

        plotter = DoubleWellMultipleFrequencyPlotter(res, self.frequencies)
        plotter.show()


def solve_func(solver: Simulator):
    t, z, n1_init, n2_init, m_exited1_init, m_exited2_init = solver.run()
    return t, z
