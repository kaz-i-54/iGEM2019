from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

from Young.Young_pattern import Young_Pattern


class Young_Finger(Young_Pattern):
    r_fn = 0.01
    r_rd = 5

    def __init__(self, r1, r2, w1, w2, init_alive_prob=0.5):
        super().__init__(r1, r2, w1, w2, init_alive_prob)
        self.img_finger = self.state
        self.__noise = np.zeros((self.width, self.height))
        self.noise()
        # print(self.__noise)

    def noise(self):
        N = self.width * self.height
        v = np.array(np.random.rand(N), dtype=float)
        self.__noise = v.reshape(self.height, self.width)
        return self.__noise

    def load_text(self, filename):
        self.img_finger = super().load_text(filename)

    def load_ndarray(self, ndarray):
        self.img_finger = super().load_ndarray(ndarray)

    def next_generation(self):
        """
        次の世代にstateを更新する
        :return: ndarray  state
        """
        N = signal.correlate2d(self.state, self.mask, mode="same", boundary="wrap")
        N = N * (1 - self.r_fn) + self.img_finger * self.r_fn + self.noise() * self.r_rd
        self.state = N > 0
        self.generation += 1
        return self.state

    def show_ini_end(self, load_filename, save_filename, gen=30):
        fig, ax = plt.subplots(ncols=2,
                               sharex="col", sharey="all",
                               facecolor="lightgray")
        fig.suptitle(
            'r1={0:.2g} r2={1:.2g} w1={2:.2g} w2={3:.2g} r_fn={4:.2g} r_rd={5:.2g} gen={6:.2g}'.format(self.r1, self.r2,
                                                                                                       self.w1, self.w2,
                                                                                                       self.r_fn,
                                                                                                       self.r_rd,
                                                                                                       gen), fontsize=9)
        ax[0].imshow(self.init_state(), cmap='pink')
        ax[0].set_title("initial state ", fontsize=7)
        ax[1].imshow(self.far_generation(gen), cmap='pink')
        ax[1].set_title("generation={0:.2g} ".format(gen), fontsize=7)
        plt.savefig("../data/compare_finger_" + save_filename + ".png")
        plt.show()


BackendError = type('BackendError', (Exception,), {})


def change(r_fn, r_rd):
    gen = 30
    r1 = 3
    r2 = 6
    w1 = 16.0
    w2 = -5.0
    fig, ax = plt.subplots(ncols=r_rd.size, nrows=r_fn.size,
                           sharex="col", sharey="all",
                           facecolor="lightgray")
    fig.suptitle('r1={0:.2g} r2={1:.2g} w1={2:.2g} w2={3:.2g} gen={4:.2g}'.format(r1, r2, w1, w2, gen), fontsize=9)
    for aline, r1 in zip(ax, r_fn):
        for elem, r2 in zip(aline, r_rd):
            YP = Young_Finger(3, 6, 16.0, -5.0, 0.08)
            YP.set_r_fn(r1)
            YP.set_r_rd(r2)
            elem.imshow(YP.far_generation(gen), cmap='pink')
            elem.set_title("r_fn={0:.2g} r_rd={1:.2g}".format(r1, r2), fontsize=7)
    plt.savefig("finger_rfn_rrd.png")
    plt.show()


def main():
    # ここには書かないようにする
    filename = "../data/save.txt"
    file = "fing01"
    YP = Young_Finger(filename, 3, 6, 16.0, -5.0, 0.08)
    YP.check_plot(file)
    # YP.show_ini_end("big")
    # gen = 30
    # r1 = 3
    # r2 = 6
    # w1 = 16.0
    # w2 = -5.0
    # YF = Young_Finger(r1, r2, w1, w2, 0.08)
    # #
    # # YF = Young_Finger(3, 6, 1.0, -0.3, 0.08)
    # YF.set_r_fn(0.1)
    # YF.set_r_rd(30)
    # YF.far_generation(30)
    # YF.show()
    # # YF.check_plot()
    # YF.show_cv2()
    #
    # r = np.array([20.0, 5.0, 1.0])
    # r2 = np.array([0.5, 0.2, 0.1])
    # change(r2, r)


if __name__ == "__main__":
    main()
    exit()
