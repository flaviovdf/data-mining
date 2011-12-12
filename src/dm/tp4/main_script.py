# -*- coding: utf8
'''Magic script that does ALL of the TP. In this one I did not have time to
modularize'''

from __future__ import division

import Image
import numpy as np
import os
import sys

from matplotlib import pyplot as plt
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.decomposition import RandomizedPCA
from sklearn.svm import SVC
import itertools

def load_pictures(base_dir):
    '''Returns a list of arrays, one for each bmp image for each individual'''
    
    X = np.ndarray((150, 10000), dtype='i')
    y = np.ndarray(150, dtype='i')
    
    i = 0
    for sub_fold_num in xrange(1, 16):
        for img_num in xrange(1, 11):
            img_name = 's%d.bmp' % img_num
            img_fpath = os.path.join(base_dir, str(sub_fold_num), img_name)
             
            img = Image.open(img_fpath)
            data = np.array(img.getdata()).reshape(img.size[::-1])
            data_as_array = data.reshape((1, data.shape[0] * data.shape[1]))
            
            assert len(data_as_array[0]) == X.shape[1]
            
            X[i] = data_as_array[0]
            y[i] = sub_fold_num
            i += 1
            
    return X, y

def find_best_num_pca(X, y):
    '''Finds the best number of components to use for PCA'''
    
    best_metric = 0
    best_objs = None
    
    #classifier to use
    cross_fold = StratifiedKFold(y, k=10)
    param_grid = {
                  'C': [1, 5, 10, 50, 100],
                  'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1],
                  }
    clf = GridSearchCV(SVC(kernel='rbf'), param_grid,
                       fit_params={'class_weight': 'auto'}, 
                       n_jobs=2)
    
    #search
    x_vals = [1, 5, 25, 50, 75, 100]
    y_vals = []
    for n_components in [1, 5, 25, 50, 75, 100]:
        print "Extracting the top %d eigenfaces" % (n_components)
        
        #do the pca
        pca = RandomizedPCA(n_components=n_components, whiten=True).fit(X)
        eigenfaces = pca.components_
        X_pca = pca.transform(X)
        
        #train and test classifier
        clf = clf.fit(X_pca, y)
        best_clf = clf.best_estimator
        cv_f1s = cross_val_score(best_clf, X_pca, y, cv=cross_fold, 
                                 score_func=f1_score)
        
        #update best PCA
        metric = np.mean(cv_f1s)
        y_vals.append(metric)
        if metric > best_metric:
            best_metric = metric
            best_objs = X_pca, eigenfaces, best_clf
    
    plt.plot(x_vals, y_vals, 'bo')
    plt.ylabel('Mean F1 for 10 folds')
    plt.xlabel('Number of PCA components')
    plt.show()
    
    return best_objs

def plot_faces(eigenfaces, num_faces):
    
    n_row = 1
    n_col = num_faces
    
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    for i in xrange(num_faces):
        plt.subplot(n_row, n_col, i)
        plt.imshow(eigenfaces[i].reshape((100, 100)), 
                   cmap=plt.get_cmap('Greys'))
        plt.xticks(())
        plt.yticks(())
            
    plt.show()
    plt.close()

def pessoa_matricula(X, y, clf, eigenfaces, cls=9):
    '''Gera os resultados para a pessoa escolhida para minha matricula'''
    
    print "Escolhendo a pessoa 3 e removendo todas combinacoes 3 fotos da mesma"
    fotos_for_class = np.where(y == cls)[0][:3]

    f1s = []
    for three_fotos_for_class in itertools.combinations(fotos_for_class, 3):    
        train = np.ones(y.shape[0], dtype='i')
        test = np.zeros(y.shape[0], dtype='i')
        for idx in three_fotos_for_class:
            train[idx] = 0
            test[idx] = 1
        
        #Classificando
        X_train = X[train]
        y_train = y[train]
        
        X_test = X[test]
        y_test = y[test]
        
        model = clf.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
        f1s.append(f1_score(y_test, y_pred))
        
    return np.mean(f1s)
    
def main(argv):
    
    base_dir = argv[1]

    X, y = load_pictures(base_dir)
    n_classes = len(np.unique(y))
    n_samples, n_features = X.shape
    
    print "Total dataset size:"
    print "n_samples: %d" % n_samples
    print "n_features: %d" % n_features
    print "n_classes: %d" % n_classes

    #Find best number of components
    print "Finding best number of eigenfaces to use"
    X_pca, eigenfaces, clf = find_best_num_pca(X, y)
    print "Best number of components = %d" % eigenfaces.shape[0]
    print "Best classifier", clf

    #F1 score for each for each func
    print "Performing 10 fold"
    cross_fold = StratifiedKFold(y, k=10)
    i = 0
    mean_f1 = 0
    for train, test in cross_fold:
        X_train = X_pca[train]
        y_train = y[train]
        
        X_test = X_pca[test]
        y_test = y[test]
        
        model = clf.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        print "Fold %d - report" % i
        print classification_report(y_test, y_pred)
        print "Fold %d - confusion matrix" % i
        print confusion_matrix(y_test, y_pred)
        print
        
        mean_f1 += f1_score(y_test, y_pred)
        i += 1
    
    #Mean F1
    mean_f1 /= 10
    print "Mean F1 score = %f" % mean_f1
    
    #Resultados para a Pessoa = 3
    f1_pessoa = pessoa_matricula(X_pca, y, clf, eigenfaces)
    print "F1 para pessoa da minha matricula = %f" % f1_pessoa
    plot_faces(eigenfaces, 5)
    
if __name__ == '__main__':
    main(sys.argv)