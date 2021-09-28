import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import sys
#import pandas as pd
#import os

def main():
    #df = pd.read_csv(os.path.join(os.path.dirname(__file__),"input3.csv"))   
    #ds = df.values 
    
    ds = np.genfromtxt(sys.argv[1], delimiter=',', skip_header=1)
    
    X = ds[:,:-1]
    y = ds[:,-1]
    C = [0.1, 0.5, 1, 5, 10, 50, 100]
    
    models = [{'estimator' : svm.SVC() , 'param_grid':{'kernel':["linear"], 'C' : C},"method":"svm_linear"},
             {'estimator' : svm.SVC() , 'param_grid':{'kernel':["poly"], 'C' : [0.1, 1, 3], 'degree' : [4, 5, 6], 'gamma' : [0.1, 0.5]},"method":"svm_polynomial"},
             {'estimator' : svm.SVC() , 'param_grid':{'kernel':["rbf"], 'C' : C, 'gamma' : [0.1, 0.5, 1, 3, 6, 10]},"method":"svm_rbf"},
             {'estimator' : LogisticRegression() , 'param_grid':{'C' : C},"method":"logistic"},
             {'estimator' : KNeighborsClassifier() , 'param_grid':{'n_neighbors': list(range(1,51)) , 'leaf_size' : list(range(5,61,5))},"method":"knn"},
             {'estimator': DecisionTreeClassifier(), 'param_grid':{'max_depth' : list(range(1,51)) , 'min_samples_split' : list(range(2,11))},"method":"decision_tree"},
             {'estimator': RandomForestClassifier(), 'param_grid':{'max_depth' : list(range(1,51)) , 'min_samples_split' : list(range(2,11))},"method":"random_forest"}]

    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size= 0.4, stratify=y)

    #f = open(os.path.join(os.path.dirname(__file__),"output3.csv"),"w")
    f = open(sys.argv[2],"w")
    
    for m in models:
        clf = GridSearchCV(m.get("estimator"), m.get("param_grid"), cv=5) 
        clf.fit(X_train,y_train)
        #print(m.get("method"))
        #print("Best Estimator : ",str(clf.best_estimator_))
        #print("Best Score : ",str(clf.best_score_))  
        #print("Test Score : ",str(clf.score(X_test,y_test)))      
        
        f.write(m.get("method") + "," + str(clf.best_score_) + "," + str(clf.score(X_test,y_test)) + "\n")
         
        #plot(clf,m.get("method"),X,y) # clf, method name, dataset
    f.close()   

if __name__ == '__main__':
    main()
