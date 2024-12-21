from abc import ABC, abstractmethod

from config.config import Config


class Simulator(ABC):
    """
    This guy is the main part simulating life
    """
    @abstractmethod
    def run(self):
        """Method that must be implemented by all subclasses."""
        pass

    def _config_to_vars(self, config: Config):
        """extract variables from config with shorter names for convenience"""
        bd = config.bd
        M = config.molecule_number
        b_abs = config.b_abs
        kappa = config.kappa
        b_emission = config.b_emission
        P0 = config.cw_pump
        p00 = config.perturbation
        t = config.time_range
        return bd, M, b_abs, kappa, b_emission, P0, p00, t

    def _params_to_vars(self, params):
        """ extracts variables from params for fitting"""
        bD = params[0]
        kappa = params[1]
        B21 = params[2]
        M = params[3]
        P0 = params[4]
        B12 = params[5]
        p00 = params[6]
        return bD, kappa, B21, M, P0, B12, p00
