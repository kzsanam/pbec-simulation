from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray, dtype, floating

from view.plot_view import Plotter


class DifferentCouplingsDoubleWellMultipleFrequencyPlotter(Plotter):
    def __init__(
            self,
            res: list[tuple[Any, Any, Any, Any]],
            frequencies: ndarray[tuple[int], dtype[floating]],
            couplings: ndarray[tuple[int], dtype[floating]]
    ):
        self.res = res
        # do not show first points because it is not stabilised yet
        self.start_point = 1000
        self.frequencies = frequencies
        self.couplings = couplings

    def show(self):
        self.different_couplings_amplitude_show()
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

    def different_couplings_amplitude_show(self):
        i = 0
        for coupling in self.couplings:
            self.amplitude_show(self.res[i:i + self.frequencies.size], coupling)
            i += self.frequencies.size

        avg_n1 = np.round(np.mean(self.res[2][1][:, 2]), 1)
        avg_n2 = np.round(np.mean(self.res[3][1][:, 3]), 1)

        plt.title(f"photon number in 1 and 2 wells {avg_n1} and {avg_n2}")
        plt.ylabel("normalised module of amplitude")
        plt.xlabel("frequency, GHz/2pi")
        plt.legend()
        plt.show()

    def amplitude_show(self, coupling_res, coupling):
        first_well_amplitude = np.array(list(map(lambda x: self.get_amplitude(x, 2, self.start_point), coupling_res)))
        second_well_amplitude = np.array(
            list(map(lambda x: self.get_amplitude(x, 3), coupling_res)))

        normalized_first_well_amplitude = first_well_amplitude / np.max(first_well_amplitude)
        normalized_second_well_amplitude = second_well_amplitude / np.max(second_well_amplitude)

        # plt.plot(self.frequencies, first_well_amplitude, label="1 well amplitude")
        # plt.plot(self.frequencies, second_well_amplitude, label="2 well amplitude")

        plt.plot(
            self.frequencies,
            normalized_first_well_amplitude,
            label=f"1 well, coupling {np.round(coupling, 1)}"
        )
        plt.plot(
            self.frequencies,
            normalized_second_well_amplitude,
            label=f"2 well, coupling {np.round(coupling, 1)}"
        )
