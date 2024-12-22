from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray, dtype, floating


class DoubleWellMultipleFrequencyPlotter:
    def __init__(
            self,
            res:  list[tuple[Any, Any]],
            frequencies: ndarray[tuple[int], dtype[floating]]
    ):
        self.res = res
        # do not show first points because it is not stabilised yet
        self.start_point = 1000
        self.frequencies = frequencies

    def show(self):
        self.amplitude_show()
        # self.time_dependency_show()


    def time_dependency_show(self):
        ii = 0
        for single_res in self.res:
            plt.plot(
                single_res[0][self.start_point:],
                single_res[1][:, 2][self.start_point:],
                label=f"first well, frequency {np.round(self.frequencies[ii], 1)} GHz"
            )

            plt.plot(
                single_res[0][self.start_point:],
                single_res[1][:, 3][self.start_point:],
                label=f"second well, frequency {np.round(self.frequencies[ii], 1)} GHz"
            )
            ii += 1

        plt.ylabel("n")
        plt.xlabel("time, ns")
        plt.legend()
        plt.show()

    def amplitude_show(self):
        first_well_amplitude = np.array(list(map(lambda x: self.get_amplitude(x, 2), self.res)))
        second_well_amplitude = np.array(list(map(lambda x: self.get_amplitude(x, 3), self.res)))

        normalized_first_well_amplitude = first_well_amplitude / np.max(first_well_amplitude)
        normalized_second_well_amplitude = second_well_amplitude / np.max(second_well_amplitude)

        # plt.plot(self.frequencies, first_well_amplitude, label="1 well amplitude")
        # plt.plot(self.frequencies, second_well_amplitude, label="2 well amplitude")

        plt.plot(self.frequencies, normalized_first_well_amplitude, label="1 well amplitude")
        plt.plot(self.frequencies, normalized_second_well_amplitude, label="2 well amplitude")

        plt.ylabel("amplitude")
        plt.xlabel(r"frequency, GHz/2pi")
        plt.legend()
        plt.show()

    def get_amplitude(self, single_res, index: int):
        # assume that amplitude is abs(max - mean)
        n = single_res[1][:, index][self.start_point:]
        return np.abs(np.max(n) - np.mean(n))
