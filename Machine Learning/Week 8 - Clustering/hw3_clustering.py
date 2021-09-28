import numpy as np
import pandas as pd
import scipy as sp
import sys

k = 5 # number of clusters
iterations = 10
def KMeans(data):
	# initialize the K-means centroids by randomly selecting 5 data points
	k_means = data[np.random.choice(data.shape[0], k, replace = False)] # Default is True, meaning that a value of a can be selected multiple times.

	#perform the algorithm with 5 clusters and 10 iterations...you may try others
    #for testing purposes, but submit 5 and 10 respectively
	for i in range(iterations):		
		clusters = []
		for d in data:
			min_cluster_index = np.argmin([np.linalg.norm(d - m) for m in k_means]) # min mean for each data point
			clusters.append(min_cluster_index)
		
		for j in range(k):
			k_clusters = [index for index, c in enumerate(clusters) if c == j]
			k_means[j] = np.mean(data[k_clusters],axis=0)

		filename = "centroids-" + str(i + 1) + ".csv" #"i" would be each iteration
		np.savetxt(filename, k_means, delimiter=",")

def multivariateGaussian(pi, mean, sigma, x):
	sigma_inv = np.linalg.inv(sigma)
	sigma_det_inv = abs(np.linalg.det(sigma)) ** -0.5
	diff = x.T - mean.T	
	return pi * sigma_det_inv * np.exp(-0.5 * diff.T * sigma_inv * diff)

def EMGMM(data):
	n, col = data.shape	
	pi = np.ones(k) / k # uniform distribution
	mu = data[np.random.choice(n, k, replace = False)] # selecting 5 data points randomly

	sigma = [np.identity(col) for i in range(k)]	

	for i in range(iterations):
		phi_k = np.zeros((n, k))
		# E-step:
		for index, d, in enumerate(data):		
			q = np.zeros(k)
			for j in range(k):
				q[j] = multivariateGaussian(pi[j], mu[j], sigma[j], d)
			phi_k[index] = q / np.sum(q)
			
		# M-step:
		for j in range(k):
			n_k = np.sum(phi_k[:, j])
			pi[j] = n_k / n
			mu[j] = phi_k[:, j] * data / n_k				
			
			covariance = np.zeros((col, col))
			for index, d, in enumerate(data):	
				diff = d.T - mu[j].T
				covariance += phi_k[index, j] * diff * diff.T
				
			sigma[j] = covariance / n_k
			
		filename = "pi-" + str(i + 1) + ".csv" 
		np.savetxt(filename, pi, delimiter=",") 
		filename = "mu-" + str(i + 1) + ".csv"
		np.savetxt(filename, mu, delimiter=",")  #this must be done at every iteration

		for j in range(k): #k is the number of clusters
			filename = "Sigma-" + str(j + 1) + "-" + str(i + 1) + ".csv" #this must be done 5 times (or the number of clusters) for each iteration
			np.savetxt(filename, sigma[j], delimiter=",")


if __name__ == '__main__':
	data = np.genfromtxt(sys.argv[1], delimiter = ",")
	data = np.matrix(data)
	KMeans(data)	
	EMGMM(data)
