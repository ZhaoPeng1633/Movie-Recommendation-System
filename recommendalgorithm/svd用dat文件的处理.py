#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import time

import pandas as pd
import csv
start = time.time()
dic_user = {}  #字典存储映射
dic_movie ={}
#movies = pd.read_csv("../dataset/new_movies.csv")
rating = pd.read_csv("../dataset/behaviours_new.csv")

quchong_user = rating.drop_duplicates('user_id')
quchong_movies = rating.drop_duplicates('movie_id')
#movie_list = list(movies['id'])
movie_list = list(quchong_movies['movie_id'])
user_id = list(quchong_user['user_id'])  #存储了不重复的用户

seen_movies = list(rating['movie_id'])
users = list(rating['user_id'])
ratings =list(rating['rating'])

user_index = []
movie_index =[]
for i in range(len(user_id)):
    dic_user[user_id[i]] = i  # i是int从0——用户数量-1
for i in range(len(movie_list)):
    dic_movie[movie_list[i]] = i

for each in users:
    user_index.append(dic_user[each])
for each in seen_movies:
    movie_index.append((dic_movie[each]))

print("编号成功")
all = []
for i in range(len(list(rating['user_id']))):
        info = []
        info.append(movie_index[i])
        info.append(seen_movies[i])
        info.append(user_index[i])
        info.append(users[i])
        info.append(ratings[i])
        all.append(info)
        # print('存入' + str(i+1))
columns = ['Movie_NUM','movie_id','USER_NUM','user_id','rating']
new_movie = pd.DataFrame(columns=columns, data=all)
new_movie.to_csv('../dataset/niubi.csv')
new_movie.astype(str).to_csv('../dataset/niubi.dat', header=None, index=None, sep=',')
end = time.time()
# print(str(end-start) + 's')
