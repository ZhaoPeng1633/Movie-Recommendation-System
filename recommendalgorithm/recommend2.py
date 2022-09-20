#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import random

import pandas as pd
import numpy as np
import os
from surprise import Reader, Dataset
from surprise.model_selection import cross_validate
from surprise import KNNBaseline
from surprise import KNNWithMeans
from surprise import KNNBasic
import csv

"""
针对用户相似度的推荐算法
使用KNN去度量用户之间的相似度
"""


class PersonalKnnRecommender:
    def __init__(self, behaviour_path, movie_path, mode = 0):
        self.movies = pd.read_csv(movie_path, encoding='utf-8')
        self.reader = Reader()
        self.ratings = pd.read_csv(behaviour_path)  #
        self.testings = pd.read_csv('../dataset/test.csv')  #
        data = Dataset.load_from_df(self.ratings[['user_id', 'movie_id', 'rating']], self.reader)
        trainset = data.build_full_trainset()
        # 基于用户的协同过滤，使用皮尔逊相关系数计算相似度
        sim_options = {'name': 'pearson_baseline', 'user_based': True}
        if mode == 0:
            self.algo = KNNBaseline(sim_options=sim_options)
        elif mode == 1:
            self.algo = KNNWithMeans(sim_options=sim_options)
        elif mode == 2:
            self.algo = KNNBasic(sim_options=sim_options)
        else:
            exit(0)

        self.user_id = []
        for i in range(len(self.testings['user_id'])):
            if not self.testings['user_id'][i] in self.user_id:
                self.user_id.append(self.testings['user_id'][i])
        self.algo.fit(trainset)

    def get_similar_users(self, usrID, num=10):
        user_inner_id = self.algo.trainset.to_inner_uid(usrID)
        user_neighbors = self.algo.get_neighbors(user_inner_id, k=num)
        user_neighbors = [self.algo.trainset.to_raw_uid(inner_id) for inner_id in user_neighbors]
        print(user_neighbors)
        return user_neighbors

    def recommend(self, usrID, num):
        existed_movie = list(self.ratings[self.ratings.user_id == usrID]['movie_id'])
        similar_users = self.get_similar_users(usrID, num)
        movies_dict = {}
        for i in similar_users:
            movie = list(self.ratings[self.ratings.user_id == i]['movie_id'])
            vote = list(self.ratings[self.ratings.user_id == i]['rating'])
            for j in range(len(vote)):
                if not (movie[j] in existed_movie):
                    if movie[j] in movies_dict.keys():
                        movies_dict[movie[j]] += vote[j]
                    else:
                        movies_dict[movie[j]] = vote[j]  # 从最相似的用户中挑选出没看过的电影，评分相加
        result = sorted(movies_dict.items(), key=lambda x: x[1], reverse=True)  # 对评分进行排序
        result = result[:2*num]  # 挑选出最高评分的10部电影
        result = random.sample(result, num)
        # print(result)
        recommending = []
        recommending_id = []
        ids = list(self.movies['id'])
        for i in result:
            title = list(self.movies[self.movies.id == i[0]]['title'])
            if i[0] in ids:
                recommending.append(title[0])
                recommending_id.append(i[0])

        return recommending_id  # 返回推荐的电影id

    def recommend_for_user(self, userID, num):
        movies_ids = self.recommend(userID, num)
        movie_list = []
        for each in movies_ids:
            movie_info = []
            title = list(self.movies[self.movies.id == each]['title'])[0]
            movie_info.append(title)

            stars = ""
            star = list(self.movies[self.movies.id == each]['star'])[0]
            for every in star:
                if every != '"' and every != ',' and every != '[' and every != ']':
                    stars += every
                elif every == ',':
                    stars += ' '
            movie_info.append(stars)

            genres = ""
            genres_str = list(self.movies[self.movies.id == each]['genres'])[0]
            for every in genres_str:
                if every != '"' and every != ',' and every != '[' and every != ']':
                    genres += every
                elif every == ',':
                    genres += ' '
            movie_info.append(genres)

            rating = list(self.movies[self.movies.id == each].rating)[0]
            movie_info.append(rating)

            duration = list(self.movies[self.movies.id == each].duration)[0]
            movie_info.append(duration)

            movie_list.append(movie_info)

        return movie_list

    def evaluate(self):
        print("开始！")
        index = 0
        sum = 0
        self.test_set = pd.read_csv('../dataset/test.csv', encoding='utf-8')
        self.users = self.ratings.drop_duplicates(subset='user_id')
        self.users = list(self.users['user_id'])
        # self.users = ['doskevin407']
        user_num = len(self.users)
        for each in self.users:
            num = 0
            self.actually_like = list(
                self.test_set[(self.test_set.user_id == each) & (self.test_set.rating >= 4)].movie_id)
            # print(self.actually_like)
            self.user_rec = self.recommend(each, 50)
            if len(self.user_rec) != 0:
                if len(self.actually_like) == 0:
                    user_num -= 1
                else:
                    for every in self.user_rec:
                        if every in self.actually_like:
                            num += 1
                    print(str(each) + ": " + " 查准率: " + str(float(num / len(self.user_rec))))
                    sum += float(num / len(self.user_rec))
                    # index +=1
                    # if index ==20:
                    #     break
            else:
                user_num -= 1
        # return sum / index
        return sum / user_num
if __name__ == '__main__':
    test = PersonalKnnRecommender('../dataset/train.csv', '../dataset/new_movies.csv',)
    # test.recommend_for_user('cyrus_wong', 20)
    print(test.evaluate())