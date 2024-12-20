from matplotlib import pyplot as plt


class SinglePlotter:
    def __init__(self, t, n):
        self.n = n
        self.t = t

    def show(self):
        plt.plot(self.t, self.n)
        plt.ylabel("n")
        plt.xlabel("time, ns")
        plt.show()