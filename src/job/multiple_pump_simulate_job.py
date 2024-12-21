from config.config import Config
from job.simulate_job import SimulateJob
from simulator.ode_simulator import OdeSimulator
from view.multiple_plot_view import MultiplePlotter


class MultiplePumpSimulateJob(SimulateJob):
    def run(self):
        different_pump_configs = list(map(
            lambda pump:
            Config(
                cw_pump=pump,
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
