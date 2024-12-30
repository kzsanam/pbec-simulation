from typing import Any, Tuple

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from numpy import ndarray, dtype, floating

from view.plot_view import Plotter


class PrettyDifferentAllCouplingsDoubleWellMultipleFrequencyPlotter(Plotter):
    def __init__(
            self,
            res: list[tuple[Any, Any, Any, Any]],
            frequencies: ndarray[tuple[int], dtype[floating]],
            couplings: ndarray[tuple[int], dtype[floating]],
            bath_couplings: ndarray[tuple[int], dtype[floating]],
    ):
        self.res = res
        # do not show first points because it is not stabilised yet
        self.start_point = 1000
        self.frequencies = frequencies
        self.couplings = couplings
        self.bath_couplings = bath_couplings

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
            coupling_index = int(i / self.frequencies.size)
            bath_coupling = self.bath_couplings[coupling_index]
            line_1, line_2 = self.amplitude_show(
                self.res[i:i + self.frequencies.size],
                coupling,
                coupling_index,
                bath_coupling
            )
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

        # plt.title(f"photon number in 1 and 2 wells {avg_n1} and {avg_n2}")
        plt.ylabel(r'Normalized response, $\mathrm{|A|/|A_{max}}|$')
        plt.xlabel(r'Frequency, $\Omega/2\pi$ (GHz)')
        self.set_legend(line_1_list, line_2_list)
        plt.show()

    def amplitude_show(self, coupling_res, coupling, coupling_index, bath_coupling) -> Tuple[list[Line2D], list[Line2D]]:
        first_well_amplitude = np.array(list(map(lambda x: self.get_amplitude(x, 2), coupling_res)))
        second_well_amplitude = np.array(
            list(map(lambda x: self.get_amplitude(x, 3), coupling_res)))

        normalized_first_well_amplitude = first_well_amplitude / np.max(first_well_amplitude)
        normalized_second_well_amplitude = second_well_amplitude / np.max(second_well_amplitude)

        opacity_percentage = self.get_opacity(coupling_index)

        line_1, = plt.plot(
            self.frequencies,
            normalized_first_well_amplitude,
            label=fr'1 well, $\Gamma^\prime=${np.round(bath_coupling * 1e9, 2)} Hz, $\Gamma=${np.round(coupling, 2)} GHz',
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
            label=fr'2 well, $\Gamma^\prime=${np.round(bath_coupling * 1e9, 2)} Hz, $\Gamma=${np.round(coupling, 2)} GHz',
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

        photon_coupling_label_names = list(map(
            lambda coupling: f"{np.round(coupling, 1)} GHz",
            self.couplings
        ))

        photon_coupling_names_leg = plt.legend(
            labels=photon_coupling_label_names,  # ['some'] * len(line_2_list),
            title=r'$\Gamma$',
            handlelength=0,
            handletextpad=0,
            loc="upper right",
            bbox_to_anchor=(.53, 1)
        )

        molecular_coupling_label_names = list(map(
            lambda coupling: f"{np.round(coupling * 1e9, 2)} Hz",
            self.bath_couplings
        ))

        molecular_coupling_names_leg = plt.legend(
            labels=molecular_coupling_label_names,  # ['some'] * len(line_2_list),
            title=r'$\Gamma ^\prime$',
            handlelength=0,
            handletextpad=0,
            loc="upper right",
            bbox_to_anchor=(.70, 1)
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

        plt.gca().add_artist(molecular_coupling_names_leg)
        plt.gca().add_artist(photon_coupling_names_leg)
        plt.gca().add_artist(lines_1_leg)
        plt.gca().add_artist(lines_2_leg)
