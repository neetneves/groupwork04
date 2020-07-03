# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 20:32:49 2020

@author: Administrator
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import cluster
import matplotlib.pyplot as plt

frog_data = pd.read_csv("finaldata.csv")
data = frog_data[['distance', 'fixes_percent']]
kmodel = cluster.KMeans(n_clusters=4, max_iter=100, init="k-means++")
kmodel.fit(data)
## 模型可视化##


plt.figure()
plt.scatter(data['distance'],data['fixes_percent'], c=kmodel.labels_)#原始数据散点图，按照分类查看
centroids = kmodel.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='r', zorder=10)#重心红色X进行突出

    #用来存放设置不同簇数时的SSE值
labels=kmodel.labels_

x_train,x_test,y_train,y_test = train_test_split(data.values,labels,
                                       test_size=0.2,random_state=12)
model = LogisticRegression().fit(x_train,y_train)
y_predict = model.predict(x_test)
print(y_predict)
print(" Prediction accuracy:",end=' ')
print(sum(y_test == y_predict) / len(y_predict))

def test_validate(x_test, y_test, y_predict, classifier):
    x = range(len(y_test))
    plt.figure()
    plt.plot(x, y_test, "ro", markersize=8, zorder=3, label=u"true_v")
    plt.plot(x, y_predict, "go", markersize=14, zorder=2, label=u"predict_v,$R^2$=%.3f" % classifier.score(x_test, y_test))
    plt.legend(loc="center left")
    plt.xlabel("number")
    plt.ylabel("true?")
    plt.show()



def SSE(data):
    distortions = []
    for i in range(1,11):
        km = cluster.KMeans(n_clusters=i, max_iter=100, init="k-means++")
        km.fit(data)
        #获取K-means算法的SSE
        distortions.append(km.inertia_)
    #绘制曲线
    plt.figure()
    plt.plot(range(1,11),distortions,marker="o")
    plt.xlabel("clusters_number")
    plt.ylabel("SSE")
    plt.show()
SSE(data)
test_validate(x_test, y_test, y_predict, model)
