import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray, dtype, floating


class MultipleFrequencyPlotter:
    def __init__(
            self,
            res: list[tuple[ndarray[tuple[int], dtype[floating]], tuple]],
            frequencies: ndarray[tuple[int], dtype[floating]]
    ):
        self.res = res
        # do not show first points because it is not stabilised yet
        self.start_point = 1000
        self.frequencies = frequencies

    def show(self):
        self.amplitude_show()

        ii = 0
        for single_res in self.res:
            plt.plot(
                single_res[0][self.start_point:],
                single_res[1][self.start_point:],
                label=self.frequencies[ii]
            )
            ii += 1

        plt.ylabel("n")
        plt.xlabel("time, ns")
        plt.legend()
        plt.show()

    def amplitude_show(self):
        amplitudes = list(map(self.get_amplitude, self.res))

        plt.plot(self.frequencies, amplitudes)
        plt.ylabel("amplitude")
        plt.xlabel(r"frequency, Hz/2pi")
        plt.show()

    def get_amplitude(self, single_res):
        # assume that amplitude is max - mean
        n = single_res[1][self.start_point:]
        return np.abs(np.max(n) - np.mean(n))
