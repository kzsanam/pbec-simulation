from matplotlib import pyplot as plt
from numpy import ndarray, dtype, floating


class MultiplePlotter:
    def __init__(
            self,
            res: list[tuple[ndarray[tuple[int], dtype[floating]], tuple]],
    ):
        self.res = res
        # do not show first points because it is not stabilised yet
        self.start_point = 1000

    def show(self):
        for single_res in self.res:
            plt.plot(single_res[0][self.start_point:], single_res[1][self.start_point:])
        plt.ylabel("n")
        plt.xlabel("time, ns")
        plt.show()
