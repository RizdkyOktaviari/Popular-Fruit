import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

df = pd.read_csv('F:/Kampus/Workshop Citra dan Cerdas/ProjekCitra/RGB_METRIC_FEATURES_2.csv')

# memisahkan atribut dan label
X = df[['metric','red','green','blue' ]]
y = df['buah']

# from sklearn.model_selection import train_test_split

# x_train, x_test, y_train, y_test = train_test_split(X,y,test_size=0.3)


# import numpy as np
# from sklearn.neighbors import KNeighborsClassifier

# K = np.arange(1,22)
# akurasi = []
# for k in K:
knn = KNeighborsClassifier(n_neighbors=7).fit(X,y)
#     acc2 = knn.score(x_test,y_test)
#     akurasi.append(acc2)
# print(akurasi)
# import pickle as pc

# with open('knn_pickle_final','wb') as r:
#     pc.dump(knn,r)
