import unittest

import numpy as np

from kalman import KalmanFilter


class TestKalmanFilter(unittest.TestCase):

    def test_kalman_filter(self):
        x = np.array([0, 0]) # initial state
        P = np.eye(2) # initial covariance
        F = np.array([[1, 1], [0, 1]]) # state transition matrix
        Q = np.array([[0.1, 0], [0, 0.1]]) # process noise covariance
        H = np.array([1, 0]).reshape(1, 2) # observation matrix
        R = np.array([1]).reshape(1, 1) # observation noise covariance

        kf = KalmanFilter(x, P, F, Q, H, R)

        # Test with one observation
        z = np.array([1])
        kf.predict()
        kf.update(z)

        self.assertEqual(kf.x[0], 0.4)
        self.assertEqual(kf.x[1], 0.2)

        # Test with multiple observations
        z = np.array([1, 2, 3, 4, 5])
        for observation in z:
            kf.predict()
            kf.update(observation)

        self.assertAlmostEqual(kf.x[0], 4.492, delta=0.001)
        self.assertAlmostEqual(kf.x[1], 1.177, delta=0.001)


if __name__ == '__main__':
    unittest.main()