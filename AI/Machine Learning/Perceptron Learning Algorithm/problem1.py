import matplotlib.pyplot as plt
import numpy as np
import sys
#import pandas as pd
#import os

def train(ds, outputfile):
    weights = np.zeros(len(ds[0]))
    error = True
    f = open(outputfile,"w")
    while error:
        error = False
        for row in ds:        
            prediction = predict(weights, row[:-1])        
            
            if row[-1] * prediction <= 0: 
                error = True
                weights[0] += row[-1] # base             
                weights[1:] = weights[1:] + row[-1] * row[:-1]  #weight[i] = weight[i] + yi xi

        # write weights 
        f.write(str(weights[1])+","+str(weights[2])+","+str(weights[0])+"\n")
    plot(weights,ds[:,:2],ds[:,-1]) # weights, X, y

    f.close()
    return weights

def predict(weights,x):   
    f = weights[0] + np.dot(weights[1:], x)
    return 1 if f >= 0 else -1

def writeOutput(weights, outputfile):
    f = open(outputfile,"a")
    f.write(",".join(str(w) for w in np.flip(weights))+"\n")
    f.close()

def plot(weights,X,y):
    #x-intercept = (0, -b / w2)
    #y-intercept = (-b / w1, 0)
    #m = -(b / w2) / (b / w1)
    #y = (-(b / w2) / (b / w1))x + (-b / w2) <= mx + c, m is slope and c is intercept     

    plt.scatter(X[:,0],X[:,1], color=['blue' if value == 1 else 'red' for value in y])
    min1, max1 = X[:, 0].min()-1, X[:, 0].max()+1
    min2, max2 = X[:, 1].min()-1, X[:, 1].max()+1    

    xx = [min1, max1]
    # y = X * slope + intercept
    yy = (np.array(xx) * -weights[1] / weights[2])+(-weights[0]/weights[2])
    plt.plot(xx, yy, 'k')
    plt.axis([min1, max1, min2, max2])    
    plt.show()

def main():
    #df = pd.read_csv(os.path.join(os.path.dirname(__file__),"input1.csv"),header=None)   
    #ds = df.values 
    #train(ds, "output1.csv")
    ds = np.genfromtxt(sys.argv[1], delimiter=',', skip_header=0)
    train(ds, sys.argv[2])  
    
if __name__ == '__main__':
    main()
