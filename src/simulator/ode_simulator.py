import numpy as np
from scipy.integrate import odeint

from config.config import Config
from simulator.simulator import Simulator


class OdeSimulator(Simulator):
    def __init__(self, config: Config):
        self.config = config

    def run(self):
        # define variables with shorter names for convenience
        bd = self.config.bd
        M = self.config.molecule_number
        b_abs = self.config.b_abs
        kappa = self.config.kappa
        b_emission = self.config.b_emission
        P0 = self.config.cw_pump
        p00 = self.config.perturbation
        t = self.config.time_range

        m_exited_init, n_init = self.define_initial_conditions()

        # solve ode i need
        fit_model_func = lambda z, t: (
            self.fit_model(z, t, [bd, kappa, b_emission, M, P0, b_abs, p00])
        )
        z0 = [m_exited_init, n_init]

        z = odeint(fit_model_func, z0, t)
        return t, z, n_init, max(z[:, 0]) - m_exited_init

    def define_initial_conditions(self):
        # define variables with shorter names for convenience
        bd = self.config.bd
        M = self.config.molecule_number
        b_abs = self.config.b_abs
        kappa = self.config.kappa
        b_emission = self.config.b_emission
        P0 = self.config.cw_pump
        p00 = self.config.perturbation

        m_exited_init = (M * P0 * (M * b_abs + kappa)
                         / (b_emission * (M * P0 + kappa) + b_abs * P0 * M + P0 * kappa))

        n_init = P0 / kappa * M

        # solve ode to find real initial conditions
        fit_model_func = lambda z, t: self.fit_model(
            z,
            t,
            [bd, kappa, b_emission, M, P0, b_abs, p00]
        )
        z_init = [m_exited_init, n_init]
        t = np.arange(-100, 0, 0.01)

        solution = odeint(fit_model_func, z_init, t)
        m_exited_init_final = solution[-1, 0]
        n_init_final = solution[-1, 1]
        return m_exited_init_final, n_init_final

    def fit_model(self, z, t, params):
        dmeff_dt = self.meff_func(z[0], z[1], t, params)
        dn_dt = self.n_func(z[0], z[1], t, params)
        dz_dt = [dmeff_dt, dn_dt]
        return dz_dt

    def n_func(self, Me, n, t, params):
        bD = params[0]
        kappa = params[1]
        B21 = params[2]
        M = params[3]
        P0 = params[4]
        B12 = params[5]
        p00 = params[6]
        return -(B12 * M + kappa) * n + Me * (B21 + (B12 + B21) * n)

    def meff_func(self, Me, n, t, params):
        bD = params[0]
        kappa = params[1]
        B21 = params[2]
        M = params[3]
        P0 = params[4]
        B12 = params[5]
        p00 = params[6]
        return ((M * (B12 * n + (self.config.pulse_func(t) * p00 + P0))
                 - Me * (B21 + (B12 + B21) * n + (self.config.pulse_func(t) * p00 + P0)))
                - Me * self.config.spontaneous_loss)
