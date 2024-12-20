from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class Config:
    """
        defines cavity parameters, pump parameters
    """
    bd: float
    kappa: float
    b_emission: float
    molecule_number: float
    cw_pump: float
    perturbation: float
    time_range: np.ndarray[tuple[int], np.dtype[np.floating]]
    spontaneous_loss: float = 0.25
    pulse_func: Callable[[float], float] = lambda x: np.sin(x)
    well_coupling: float = 0

    @property
    def b_abs(self) -> float:
        return self.b_emission * np.exp(-self.bd)
