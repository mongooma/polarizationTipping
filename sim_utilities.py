import numpy as np

class polarization:

    def __init__(self):
        pass

    @staticmethod
    def polarization_std(Z):
        """
        Extremism
        the last dimension of Z is the party dimension, binary: {-1, 1}
        :param Z:
        :param kwargs:
        :return:
        """
        return np.mean([np.std(Z[:, i]) for i in range(0, Z.shape[1]-1)])

    @staticmethod
    def polarization_party_diff(Z):
        """
        Partisan Difference
        the last dimension of Z is the party dimension, binary: {-1, 1}
        :param Z:
        :param kwargs:
        :return:
        """
        return np.average([abs(np.mean(Z[Z[:, -1] == -1][:, i]) - np.mean(Z[Z[:, -1] == 1][:, i]))
                          for i in range(0, Z.shape[1]-1)
                          ])
