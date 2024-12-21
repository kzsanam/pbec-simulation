from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class Config:
    """
        defines cavity parameters, pump parameters
    """
    bd: float = 3.87
    kappa: float = 7.4
    b_emission: float = 2.5 * 1e-5
    molecule_number: float = 6 * 1e9
    cw_pump: float = 5.235 * 1e-3
    perturbation: float = .1 * 1e-6
    time_range: np.ndarray[tuple[int], np.dtype[np.floating]] = np.arange(0, 50, 0.01)
    spontaneous_loss: float = 0.25
    pulse_func: Callable[[float], float] = lambda x: np.sin(x)
    well_coupling: float = 0

    @property
    def b_abs(self) -> float:
        return self.b_emission * np.exp(-self.bd)
