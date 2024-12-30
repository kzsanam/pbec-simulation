import numpy as np

from config.config import Config
from job.simulate_job import SimulateJob
from simulator.one_pump_two_batch_double_well_ode_simulator import \
    OnePumpTwoBatchDoubleWellOdeSimulator
from simulator.simulator import Simulator
from view.pretty_different_bath_couplings_double_well_multiple_frequency_plot_view import \
    PrettyDifferentBathCouplingsDoubleWellMultipleFrequencyPlotter


class DiffBathCouplingOnePumpTwoBathWellMultipleFrequencySimulateJob(SimulateJob):
    # adding value on the right side so it does not hit 0 frequency
    frequencies_array = np.arange(.0, 1, .01) + .015
    # bath_couplings_array = np.arange(0, 10, 3) * 1e-11
    bath_couplings_array = np.array([0.01, .1, .5]) * 1e-9

    # creating an array of frequencies and couplings as
    # [frequency_1, coupling_1, bath_coupling_1, ..., frequency_n, coupling_1, batch_coupling_1,
    #  frequency_1, coupling_n,  ..., frequency_n, coupling_n, bath_coupling_n]
    frequencies = np.tile(frequencies_array, bath_couplings_array.size)
    batch_couplings = np.repeat(bath_couplings_array, frequencies_array.size)

    def run(self):
        different_pump_configs = list(map(
            lambda frequency, bath_coupling:
            Config(
                time_range=np.arange(0, 50, 0.01),
                molecule_number=2 * 6 * 1e9,
                perturbation=.1 * 1e-6,
                # cw_pump=5.227 * 1e-3,
                cw_pump=5.217 * 1e-3,
                well_coupling=0,
                molecular_bath_coupling=bath_coupling,
                pulse_func=lambda x: np.sin(frequency * 2 * np.pi * x),
            ),
            np.array(self.frequencies), np.array(self.batch_couplings)
        ))

        solvers = list(map(
            lambda config: OnePumpTwoBatchDoubleWellOdeSimulator(config),
            different_pump_configs
        ))

        res = list(map(solve_func, solvers))

        plotter = PrettyDifferentBathCouplingsDoubleWellMultipleFrequencyPlotter(
            res,
            self.frequencies_array,
            self.bath_couplings_array
        )
        plotter.show()


def solve_func(solver: Simulator):
    t, z, n1_init, n2_init, m_exited1_init, m_exited2_init = solver.run()
    return t, z, n1_init, n2_init
