from abc import ABC, abstractmethod

import numpy as np


class Plotter(ABC):
    """
    This guy is showing results as a plot
    """
    @abstractmethod
    def show(self):
        """Method that must be implemented by all subclasses."""
        pass

    def get_opacity(self, coupling_index: int, opacity_lower_limit: float = 0.6) -> float:
        """get opacity percentage, adding some lower limit to make the lowest value visible"""
        couplings_size = self.couplings.size
        return round(
            (coupling_index + opacity_lower_limit) / (couplings_size + opacity_lower_limit)
            , 2
        )

    def get_amplitude(self, single_res, index: int, start_point = 1000):
        # assume that amplitude is abs(max - min)
        n = single_res[1][:, index][start_point:]
        return np.abs(np.max(n) - np.min(n)) / 2
