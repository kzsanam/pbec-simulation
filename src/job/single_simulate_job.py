import numpy as np

from config.config import Config
from job.simulate_job import SimulateJob
from simulator.ode_simulator import OdeSimulator
from view.single_plot_view import SinglePlotter


class SingleSimulateJob(SimulateJob):
    def run(self):
        config = Config(
            bd=3.87,
            kappa=5.4,
            b_emission=2.5 * 1e-5,
            molecule_number=6 * 1e9,
            cw_pump=5.2 * 1e-3,
            perturbation=27 * 1e-6,
            time_range=np.arange(0, 50, 0.1),
            pulse_func=lambda x: np.sin(0.1 * np.pi * 3 * x)
        )

        solver = OdeSimulator(config)

        t, z, n_init, meff_init = solver.run()

        plotter = SinglePlotter(t, z[:, 1])
        plotter.show()
