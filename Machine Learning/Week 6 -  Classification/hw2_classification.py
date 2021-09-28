from __future__ import division
import numpy as np
import sys

X_train = np.genfromtxt(sys.argv[1], delimiter=",")
y_train = np.genfromtxt(sys.argv[2])
X_test = np.genfromtxt(sys.argv[3], delimiter=",")

X_train = np.matrix(X_train)
X_test = np.matrix(X_test)

## can make more functions if required
# asset-v1 ColumbiaX+CSMM.102x+2T2021+type@asset+block@ML_lecture7 22-26

def maximumLikelihood(X_train, y_train):
    n = len(y_train)
    classes = set(y_train)

    # Class priors:
    pi = []
    mean = []
    sigma = []
    
    for c in classes:
        pi.append(np.sum(y_train == c)/n)

        x = X_train[y_train==c]
        mu = np.mean(x, axis=0).T
        mean.append(mu)        
        sigma.append(covariance(x, mu))

    return pi, mean, sigma

def covariance(x, mu):
    length = len(x)
    sigma = 0
    for xi in x:     
        diff = xi.T-mu
        sigma += diff * diff.T / length

    return sigma

def pluginClassifier(X_train, y_train, X_test):    
    # this function returns the required output
    """
    Plug-in classifier:
    f(x) = arg max pi_y * |sigma|^-0.5 * exp {-0.5 * (x-mu).T * sigma^-1 * (x-mu)}
    """    
    pi, mean, sigma = maximumLikelihood(X_train, y_train)
    sigma_inv = np.linalg.inv(sigma)
    sigma_det_inv = abs(np.linalg.det(sigma)) ** -0.5
    
    # Plug-in classifier f(x)
    plug_in_classifier = []
    classes = len(set(y_train))
    for x in X_test:
        classifier = np.zeros(classes)
        for c in range(classes):
            diff = x.T - mean[c]
            classifier[c] = pi[c] * sigma_det_inv[c] * np.exp(-0.5 * diff.T * sigma_inv[c] * diff)
                   
        plug_in_classifier.append(classifier/np.sum(classifier))
        
    return plug_in_classifier
    
 

final_outputs = pluginClassifier(X_train, y_train, X_test) # assuming final_outputs is returned from function

np.savetxt("probs_test.csv", final_outputs, delimiter=",") # write output to file