import numpy as np

from config.config import Config
from job.simulate_job import SimulateJob
from simulator.one_pump_two_batch_double_well_ode_simulator import \
    OnePumpTwoBatchDoubleWellOdeSimulator
from simulator.simulator import Simulator
from view.pretty_different_couplings_double_well_multiple_frequency_plot_view import \
    PrettyDifferentCouplingsDoubleWellMultipleFrequencyPlotter


class DiffCouplingOnePumpTwoBathWellMultipleFrequencySimulateJob(SimulateJob):
    # adding value on the right side so it does not hit 0 frequency
    frequencies_array = np.arange(.0, 0.5, .01) + .015
    couplings_array = np.arange(0.1, 1, .4)

    # creating an array of frequencies and couplings as
    # [frequency_1, coupling_1, frequency_2, coupling_1, ..., frequency_n, coupling_1,
    #  frequency_1, coupling_2, frequency_2, coupling_2, ..., frequency_n, coupling_2,
    #  frequency_1, coupling_n, frequency_2, coupling_n, ..., frequency_n, coupling_n]
    frequencies = np.tile(frequencies_array, couplings_array.size)
    couplings = np.repeat(couplings_array, frequencies_array.size)

    def run(self):
        different_pump_configs = list(map(
            lambda frequency, coupling:
            Config(
                time_range=np.arange(0, 50, 0.01),
                molecule_number=2 * 6 * 1e9,
                perturbation=.1 * 1e-6,
                cw_pump=5.227 * 1e-3,
                well_coupling=coupling,
                pulse_func=lambda x: np.sin(frequency * 2 * np.pi * x),
                molecular_bath_coupling=0
            ),
            np.array(self.frequencies), np.array(self.couplings)
        ))

        solvers = list(map(
            lambda config: OnePumpTwoBatchDoubleWellOdeSimulator(config),
            different_pump_configs
        ))

        res = list(map(solve_func, solvers))

        plotter = PrettyDifferentCouplingsDoubleWellMultipleFrequencyPlotter(
            res,
            self.frequencies_array,
            self.couplings_array
        )
        plotter.show()


def solve_func(solver: Simulator):
    t, z, n1_init, n2_init, m_exited1_init, m_exited2_init = solver.run()
    return t, z, n1_init, n2_init
