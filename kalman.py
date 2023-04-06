import numpy as np

class KalmanFilter:
    def __init__(self, F, H, Q, R, P, x):
        """
        F: state transition matrix
        H: observation matrix
        Q: process noise covariance matrix
        R: observation noise covariance matrix
        P: error covariance matrix
        x: initial state
        """
        self.F = F
        self.H = H
        self.Q = Q
        self.R = R
        self.P = P
        self.x = x

    def predict(self, u=0):
        # Predict the state estimate and error covariance matrix
        self.x = np.dot(self.F, self.x) + u
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def update(self, z):
        # Update the state estimate and error covariance matrix
        y = z - np.dot(self.H, self.x)
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x = self.x + np.dot(K, y)
        I = np.identity(self.P.shape[0])
        self.P = np.dot((I - np.dot(K, self.H)), self.P)