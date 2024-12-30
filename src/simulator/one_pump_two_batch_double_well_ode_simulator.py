import numpy as np
from scipy.integrate import odeint

from config.config import Config
from simulator.simulator import Simulator


class OnePumpTwoBatchDoubleWellOdeSimulator(Simulator):
    def __init__(self, config: Config):
        self.config = config

    def run(self):
        # define variables with shorter names for convenience
        bd, M, b_abs, kappa, b_emission, P0, p00, t = self._config_to_vars(self.config)

        m_exited1_init, m_exited2_init, n1_init, n2_init = self.define_initial_conditions()

        # solve ode i need
        fit_model_func = lambda z, t: (
            self.fit_model(z, t, [bd, kappa, b_emission, M, P0, b_abs, p00])
        )
        z0 = [m_exited1_init, m_exited2_init, n1_init, n2_init]

        z = odeint(fit_model_func, z0, t)
        return t, z, n1_init, n2_init, max(z[:, 0]) - m_exited1_init, max(z[:, 1]) - m_exited2_init

    def define_initial_conditions(self):
        # define variables with shorter names for convenience
        bd, M, b_abs, kappa, b_emission, P0, p00, t = self._config_to_vars(self.config)

        # define preliminary initial conditions
        m_exited1_init = (M * P0 * (M * b_abs + kappa)
                          / (b_emission * (M * P0 + kappa) + b_abs * P0 * M + P0 * kappa))

        m_exited2_init = (M * P0 * (M * b_abs + kappa)
                          / (b_emission * (M * P0 + kappa) + b_abs * P0 * M + P0 * kappa))

        n1_init = P0 / kappa * M
        n2_init = P0 / kappa * M

        # solve ode to find real initial conditions
        fit_model_func = lambda z, t: self.fit_model(
            z,
            t,
            [bd, kappa, b_emission, M, P0, b_abs, p00]
        )
        z_init = [m_exited1_init, m_exited2_init, n1_init, n2_init]
        t = np.arange(-100, 0, 0.01)

        solution = odeint(fit_model_func, z_init, t)
        m_exited1_init_final = solution[-1, 0]
        m_exited2_init_final = solution[-1, 1]
        n1_init_final = solution[-1, 2]
        n2_init_final = solution[-1, 3]
        return m_exited1_init_final, m_exited2_init_final, n1_init_final, n2_init_final

    def fit_model(self, z, t, params):
        dm_exited1_dt = self.m_exited1_func(z[0], z[1], z[2], z[3], t, params)
        dm_exited2_dt = self.m_exited2_func(z[0], z[1], z[2], z[3], t, params)
        dn1_dt = self.n1_func(z[0], z[1], z[2], z[3], t, params)
        dn2_dt = self.n2_func(z[0], z[1], z[2], z[3], t, params)
        dz_dt = [dm_exited1_dt, dm_exited2_dt, dn1_dt, dn2_dt]
        return dz_dt

    def n1_func(self, Me1, Me2, n1, n2, t, params):
        bD, kappa, B21, M, P0, B12, p00 = self._params_to_vars(params)

        J = self.config.well_coupling
        return -(B12 * M + kappa) * n1 + Me1 * (B21 + (B12 + B21) * n1) - J * n1 + J * n2

    def n2_func(self, Me1, Me2, n1, n2, t, params):
        bD, kappa, B21, M, P0, B12, p00 = self._params_to_vars(params)

        J = self.config.well_coupling
        return -(B12 * M + kappa) * n2 + Me2 * (B21 + (B12 + B21) * n2) - J * n2 + J * n1

    def m_exited1_func(self, Me1, Me2, n1, n2, t, params):
        bD, kappa, B21, M, P0, B12, p00 = self._params_to_vars(params)

        return ((M * (B12 * n1 + (self.config.pulse_func(t) * p00 + P0))
                 - Me1 * (B21 + (B12 + B21) * n1 + (self.config.pulse_func(t) * p00 + P0)))
                - Me1 * self.config.spontaneous_loss
                + self.config.molecular_bath_coupling * n2 * (M - Me1)
                )

    def m_exited2_func(self, Me1, Me2, n1, n2, t, params):
        bD, kappa, B21, M, P0, B12, p00 = self._params_to_vars(params)

        return ((M * (B12 * n2 + (P0))
                 - Me2 * (B21 + (B12 + B21) * n2 + (P0)))
                - Me2 * self.config.spontaneous_loss
                + self.config.molecular_bath_coupling * n1 * (M - Me2)
                )
