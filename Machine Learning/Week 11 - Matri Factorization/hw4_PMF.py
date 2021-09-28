from __future__ import division
import numpy as np
import sys
from os import path

lam = 2
sigma2 = 0.1
d = 5
iterations = 50

#train_data = np.genfromtxt(sys.argv[1], delimiter = ",")
tpath = path.join(path.dirname(__file__),"ratings.csv")
train_data = np.genfromtxt(tpath, delimiter = ",")
train_data = train_data[:500] # For testing - as there are many records in ratings.csv

# Implement function here
def PMF(train_data):
    # this is for inserting data(i,j) pair into M.
    # why this - because 
    # (1) users or object index may not start from 0
    # (2) their indinces may not be in proper order eg.  0,3,19,25,.. because every user may not rate every object
    users = {}
    for index, u in enumerate(set(train_data[:,0])):
        users[u] = index
    objects = {}
    for index, v in enumerate(set(train_data[:,1])):
        objects[v] = index

    N_u = len(users)
    N_v = len(objects)

    I = np.identity(d)

    L = np.zeros((iterations, 1))
    U_matrices = np.zeros((iterations, N_u, d))
    V_matrices = np.zeros((iterations, N_v, d))
    
    U = np.zeros((N_u, d))
    V = np.random.normal(0, 1 / lam, (d, N_v))

    #np.savetxt("Vrandom.csv", V, delimiter=",")
    #vpath = path.join(path.dirname(__file__),"Vrandom_s.csv")
    #V = np.genfromtxt(vpath, delimiter = ",")

    M = np.zeros((N_u, N_v))    
    for data in train_data:
        i = int(data[0]) # user
        j = int(data[1]) # obj        
        M[users[i], objects[j]] = data[2]        
    
    for k in range(iterations):                
        for i in range(N_u):
            v = np.zeros((d, d))
            m = np.zeros((d, 1))
            for j in range(N_v):
                if M[i,j] > 0:
                    v_j = V[:, [j]]
                    v += np.dot(v_j, v_j.T)
                    m += M[i, j] * v_j            
            U[i, :] = np.dot(np.linalg.inv(lam * sigma2 * I + v), m).reshape(-1)

        for j in range(N_v):
            u = np.zeros((d, d))
            m = np.zeros((d, 1))
            for i in range(N_u):
                if M[i,j] > 0:
                    u_i = U[i, :].reshape(d, 1)
                    u += np.dot(u_i, u_i.T)
                    m += M[i, j] * u_i
            V[:, j] = np.dot(np.linalg.inv(lam * sigma2 * I + u), m).reshape(-1)

        #for i in range(N_u):
        #    V_j = V[:, M[i,:] > 0]
        #    U[:, i] = np.dot(np.linalg.inv(lam * sigma2 * I + np.dot(V_j, V_j.T)), np.dot(M[i, M[i,:] > 0], V_j.T))

        #for j in range(N_v):
        #    U_i = U[:, M[:,j] > 0]
        #    V[:, j] = np.dot(np.linalg.inv(lam * sigma2 * I + np.dot(U_i, U_i.T)), np.dot(M[M[:,j] > 0, j], U_i.T))

        # objective
        UV_ij = np.dot(U, V)   
        M_ij = (M[M > 0] - UV_ij[M > 0]) #(M_ij - u_i.T v_j)
        L_map = -0.5 * (1 / sigma2 * np.sum(np.linalg.norm(M_ij)**2) + lam * np.sum(np.linalg.norm(U)**2) + lam * np.sum(np.linalg.norm(V)**2))

        L[k] = L_map
        U_matrices[k] = U
        V_matrices[k] = V.T

    return L, U_matrices, V_matrices

# Assuming the PMF function returns Loss L, U_matrices and V_matrices (refer to
# lecture)
L, U_matrices, V_matrices = PMF(train_data)

np.savetxt("objective.csv", L, delimiter=",")

np.savetxt("U-10.csv", U_matrices[9], delimiter=",")
np.savetxt("U-25.csv", U_matrices[24], delimiter=",")
np.savetxt("U-50.csv", U_matrices[49], delimiter=",")
np.savetxt("V-10.csv", V_matrices[9], delimiter=",")
np.savetxt("V-25.csv", V_matrices[24], delimiter=",")
np.savetxt("V-50.csv", V_matrices[49], delimiter=",")