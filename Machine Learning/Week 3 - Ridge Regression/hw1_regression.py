import numpy as np
import sys

lambda_input = int(sys.argv[1])
sigma2_input = float(sys.argv[2])
X_train = np.genfromtxt(sys.argv[3], delimiter = ",")
y_train = np.genfromtxt(sys.argv[4])
X_test = np.genfromtxt(sys.argv[5], delimiter = ",")

X = np.matrix(X_train)
I = np.matrix(np.identity(X.shape[1]))

## Solution for Part 1
# python3 hw1_regression.py lambda sigma2 X_train.csv y_train.csv X_test.csv
def part1():
    ## Input : Arguments to the function
    ## Return : wRR, Final list of values to write in the file
    """
    # To see >>> asset-v1 ColumbiaX+CSMM.102x+2T2021+type@asset+block@ML_lecture3 - 15, 16, 17
    wRR =  arg_min_w ||y-Xw||^2 + λ||w||^2 
      L   = (y - Xw)T (y - Xw) +  λ wTw
     wRR = (λI + XTX)^-1 XTy
    """
    y = np.matrix(y_train).T
    # wRR
    return np.linalg.inv(lambda_input * I + X.T * X) * (X.T * y)
     

wRR = part1()  # Assuming wRR is returned from the function
np.savetxt("wRR_" + str(lambda_input) + ".csv", wRR, delimiter="\n") # write output to file


## Solution for Part 2
def part2():
    ## Input : Arguments to the function
    ## Return : active, Final list of values to write in the file
    """
    To see >>> Week 3_asset-v1_ColumbiaX+CSMM.102x+2T2021+type@asset+block@week3-lecture1 18, 20
    Prior : (λI + σ-2 XTX)-1 ≡ ∑ 
    Posterior : (λI + σ-2(x0x0T + XTX))-1 ≡ (∑-1 + σ-2 x0x0T )-1
    """
    x0 = np.matrix(X_test)
    x0_indices = list(range(x0.shape[0]))
    sigma = np.linalg.inv(lambda_input * I + (sigma2_input**-1) * X.T * X)
    locations = []    
    for i in range(10):
        posterior = np.linalg.inv(np.linalg.inv(sigma) +  (sigma2_input**-1) * x0.T * x0 )
        sigma2_0 = sigma2_input + x0 * posterior * x0.T

        # get the largest σ2 (sigma2_0) index
        max_sigma2_0_index = np.argmax(sigma2_0.diagonal())

        # update posterior
        max_x0 = x0[max_sigma2_0_index]
        sigma = np.linalg.inv(np.linalg.inv(sigma) +  (sigma2_input**-1) * max_x0.T * max_x0)  
        
        # Remove measured x0
        x0 = np.delete(x0, max_sigma2_0_index, axis=0)

        locations.append(x0_indices[max_sigma2_0_index]+1)
        x0_indices.pop(max_sigma2_0_index)
   
    return locations
    #return ",".join([str(l) for l in locations])

active = part2()  # Assuming active is returned from the function
np.savetxt("active_" + str(lambda_input) + "_" + str(int(sigma2_input)) + ".csv", active, delimiter=",") # write output to file

