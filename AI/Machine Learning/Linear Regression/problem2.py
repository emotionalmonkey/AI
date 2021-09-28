# numpy, scipy, pandas, matplotlib , scikit-learn
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy 
import sys
import os

def gradient_descent(X, y, epoch, l):
        weights = np.zeros((X.shape[1], 1))
        population = len(X)  
        cost = 0        
        for i in range(epoch):
            #print("Epoch ",i,end=" ")         
            weights = weights - l / population * np.dot(X.T,(np.dot(X,weights) - y))        
            loss = (y - np.dot(X,weights)) ** 2
            cost = sum(loss) / (2 * population)
            #print("Weights", weights, "Cost", cost)
        
        #print("Overall Weights", weights, "Overall Cost", cost)
        return weights, cost

def scale(x):
    num = len(x)    
    mean = sum(x) / num
    variance = sum([(i - mean) ** 2 for i in x]) / num
    deviation = variance ** 0.5 # or numpy.std(x)

    # scale = (x - mean)/standard deviation
    scale_x = [(i - mean) / deviation for i in x]    
    return np.array(scale_x)

def plot(weights,X,Scale_X,y):
    age, w = np.meshgrid(X[:, 0], X[:, 1])    
    age_scale, w_scale = np.meshgrid(Scale_X[:,0], Scale_X[:,1])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')    
    ax.scatter(X[:,0],X[:,1],y)
    ax.plot_surface(age, w, weights[0] + weights[1] * age_scale + weights[2] * w_scale, cmap='nipy_spectral', alpha=0.2)
    ax.set_xlabel('Age (Years)')
    ax.set_ylabel('Weight (Kilograms)')
    ax.set_zlabel('Height (Meters)')
    plt.show() 

def main():
    learning_rates = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 1.3]
    epoch = 100

    #df = pd.read_csv(os.path.join(os.path.dirname(__file__),"input2.csv"),header=None)   
    #ds = df.values 
    
    ds = np.genfromtxt(sys.argv[1], delimiter=',', skip_header=0)
    
    X = ds[:,:-1]
    scaled_X = (X - np.mean(X, axis=0)) / np.std(X, axis=0) # Scale
    X_new = np.ones((X.shape[0], X.shape[1] + 1)) # Add the vector 1 (intercept) ahead of your data matrix
    X_new[:,1:] = scaled_X

    y = ds[:,-1]
    y_new = y.reshape((y.shape[0]), 1)    

    #f = open(os.path.join(os.path.dirname(__file__),"output2.csv"),"w")
    f = open(sys.argv[2],"w")

    for l in learning_rates:        
        weights, cost = gradient_descent(X_new,y_new, epoch, l)
        
        # write alpha, number_of_iterations, b_0, b_age, and b_weight
        #f.write(str(l) + "," + str(epoch) + "," + ",".join(str(w) for w in weights) + "," + str(cost) + "\n")

        f.write(str(l) + "," + str(epoch) + "," + ",".join(str(w) for w in weights.flatten()) + "\n")
    f.close() 
    plot(weights, X, scaled_X, y_new) # weights, X, y

if __name__ == '__main__':
    main()