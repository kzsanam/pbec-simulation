from config.config import Config
from job.simulate_job import SimulateJob
from simulator.ode_simulator import OdeSimulator
from view.single_plot_view import SinglePlotter


class SingleSimulateJob(SimulateJob):
    def run(self):
        config = Config()

        solver = OdeSimulator(config)

        t, z, n_init, meff_init = solver.run()

        plotter = SinglePlotter(t, z[:, 1])
        plotter.show()
