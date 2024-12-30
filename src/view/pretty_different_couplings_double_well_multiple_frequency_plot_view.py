from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray, dtype, floating

from view.plot_view import Plotter


class PrettyDifferentCouplingsDoubleWellMultipleFrequencyPlotter(Plotter):
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
        line_1_list = []
        line_2_list = []
        for coupling in self.couplings:
            coupling_index = i/self.frequencies.size
            line_1, line_2 = self.amplitude_show(self.res[i:i + self.frequencies.size], coupling, coupling_index)
            i += self.frequencies.size
            line_1_list.append(line_1)
            line_2_list.append(line_2)

        avg_n1 = np.round(np.mean(self.res[2][1][:, 2]), 1)
        avg_n2 = np.round(np.mean(self.res[3][1][:, 3]), 1)

        # plot config
        plt.gcf().set_size_inches(5, 4)
        plt.tick_params(direction='in', top=True, right=True, bottom=True, left=True)
        plt.xlim(0, 1)
        plt.ylim(0, 1.1)

        plt.title(f"photon number in 1 and 2 wells {avg_n1} and {avg_n2}")
        plt.ylabel(r'Normalised response, $\mathrm{A/A_{max}}$')
        plt.xlabel(r'Frequency, $\Omega/2\pi$ (GHz)')
        self.set_legend(line_1_list, line_2_list)
        plt.show()

    def amplitude_show(self, coupling_res, coupling, coupling_index):
        first_well_amplitude = np.array(list(map(lambda x: self.get_amplitude(x, 2), coupling_res)))
        second_well_amplitude = np.array(
            list(map(lambda x: self.get_amplitude(x, 3), coupling_res)))

        normalized_first_well_amplitude = first_well_amplitude / np.max(first_well_amplitude)
        normalized_second_well_amplitude = second_well_amplitude / np.max(second_well_amplitude)

        opacity_percentage = self.get_opacity(coupling_index)

        line_1, = plt.plot(
            self.frequencies,
            normalized_first_well_amplitude,
            label=f"1 well, $\Gamma=$ {np.round(coupling, 1)} GHz",
            color="red",
            alpha=opacity_percentage
        )
        # fill the area below
        # plt.fill_between(
        #     self.frequencies,
        #     normalized_first_well_amplitude,
        #     color="red",
        #     alpha=opacity_percentage/30
        # )

        line_2, = plt.plot(
            self.frequencies,
            normalized_second_well_amplitude,
            label=f"2 well, $\Gamma=$ {np.round(coupling, 1)} GHz",
            color="blue",
            alpha=opacity_percentage
        )
        # fill the area below
        # plt.fill_between(
        #     self.frequencies,
        #     normalized_second_well_amplitude,
        #     color="blue",
        #     alpha=opacity_percentage/30
        # )
        return line_1, line_2

    def set_legend(self, line_1_list, line_2_list):
        # use standard legend
        # plt.legend()

        # use table legend
        label_names = list(map(
            lambda coupling: f"{np.round(coupling, 1)} GHz",
            self.couplings
        ))

        names_leg = plt.legend(
            labels=label_names,
            title=r'$\Gamma$',
            handlelength=0,
            handletextpad=0,
            loc="upper right",
            bbox_to_anchor=(.7, 1)
        )

        lines_1_leg = plt.legend(
            handles=line_1_list,  # * len(line_2_list),
            labels=[''] * len(line_1_list),
            title='Well 1',
            loc="upper right",
            bbox_to_anchor=(0.85, 1)
        )

        lines_2_leg = plt.legend(
            # lines,  # Handles for the lines
            handles=line_2_list,  # * len(line_2_list),
            labels=[''] * len(line_2_list),
            title='Well 2',
            loc="upper right",
            bbox_to_anchor=(1, 1)
        )

        plt.gca().add_artist(names_leg)
        plt.gca().add_artist(lines_1_leg)
        plt.gca().add_artist(lines_2_leg)
