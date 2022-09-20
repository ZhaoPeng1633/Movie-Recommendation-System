#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Slope One 算法
预测用户对未看过电影的评分
"""
import csv
import random
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm
import math
from multiprocessing import Process, Manager
import threading

class slope_one:
    def __init__(self):
        self.dictionary = Manager().dict()

    def get_avg_rating(self, user_id):
        # 需修改
        # 计算某用户的平均rating
        behaviours = pd.read_csv('../dataset/behaviours_new.csv')
        user_behaviour = list(behaviours[behaviours['user_id'] == user_id].rating)
        rating_sum = 0.0
        for each in user_behaviour:
            rating_sum += float(each)
        avg = rating_sum / len(user_behaviour)
        return avg


    def generate_matrix(self):
        # 生成矩阵(二维字典)
        matrix = {}
        behaviours = pd.read_csv('../dataset/behaviours_new.csv')
        user_list = list(behaviours['user_id'])
        movie_list = list(behaviours['movie_id'])
        rating_list = list(behaviours['rating'])
        for i in range(len(rating_list)):
            # print("用户：" + str(user_list[i]) + " 电影：" + str(movie_list[i]) + " 评分：" + str(rating_list[i]))
            if user_list[i] not in matrix.keys():
                matrix[user_list[i]] = {movie_list[i]: rating_list[i]}
            else:
                matrix[user_list[i]][movie_list[i]] = rating_list[i]
        return matrix


    def cal_slope_one(self,matrix, test_user, test_movie):
        # 预测分数
        suppose_list = []
        movie_list_of_test_user = matrix[test_user]
        # 对于每一部电影，都计算它和test_movie的差值(b)，最终算出相对于它的test_movie的rating
        for movie in movie_list_of_test_user:
            if movie == test_movie:
                continue
            diff_sum = 0.0
            user_num = 0
            for user in matrix:
                user_movie = matrix[user]
                if test_movie in user_movie and movie in user_movie:
                    diff_sum += user_movie[test_movie] - user_movie[movie]
                    user_num += 1
            if user_num:
                diff_avg = diff_sum / user_num
                suppose_rate = movie_list_of_test_user[movie] + diff_avg
                suppose_list.append((suppose_rate, user_num))

        # 如果没人看过，取这个人的平均分
        if not suppose_list:
            avg = self.get_avg_rating(test_user)
            # print avg
            return avg

        # 否则算出它的rating
        molecusar = 0.0
        denominator = 0.0
        for suppose in suppose_list:
            molecusar += suppose[0] * suppose[1]
            denominator += suppose[1]
        # return int(round(molecusar / denominator))
        return molecusar / denominator


    def createOutput(self):
        mae_sum = 0
        rmae_sum = 0
        number = 0
        matrix = self.generate_matrix()
        wf = open("output.txt", 'w')
        with open('../dataset/behaviours_new.csv', 'r') as f:
            users_behaviours = csv.reader(f)
            index = 0
            for each in users_behaviours:
                if index == 0:
                    index += 1
                    continue
                rating1 = self.cal_slope_one(matrix, each[1], each[2])
                rating2 = self.userbased_cal_matrix(matrix, each[1], each[2])
                rating = float(round((rating1+rating2)/2))
                string = str(each[1]) + "\t" + str(each[2]) + "\t" + str(rating) + "\t" + str(each[3]) + "\n"
                wf.write(string)
                t = rating - int(each[3])
                mae_sum += abs(t)
                rmae_sum += t * t
                number += 1
                index += 1
                print(number)
                if index == 2000:
                    break
        f.close()
        wf.close()
        print("MAE: " + str(mae_sum * 1.0 / number))
        print("RMAE: " + str(math.sqrt(rmae_sum * 1.0 / number)))

    def recommend(self, user_id, n):
        start =time.time()
        rec_movies = []
        num = 0
        matrix = self.generate_matrix()
        movies = pd.read_csv("../dataset/new_movies.csv")
        movies = list(movies['id'])
        movies_seen = matrix[user_id]
        movie_lists = self.split_list(movies)
        movie_lists = self.split_list(movie_lists[int(random.random()*10)])  # 测试MAE等值时应注释掉
        p0 = Process(target=self.calculate_, args=(matrix, user_id, movie_lists[0], movies_seen,))
        p0.start()
        p1 = Process(target=self.calculate_, args=(matrix, user_id, movie_lists[1], movies_seen,))
        p1.start()
        p2 = Process(target=self.calculate_, args=(matrix, user_id, movie_lists[2], movies_seen,))
        p2.start()
        p3 = Process(target=self.calculate_, args=(matrix, user_id, movie_lists[3], movies_seen,))
        p3.start()
        p4 = Process(target=self.calculate_, args=(matrix, user_id, movie_lists[4], movies_seen,))
        p4.start()
        p5 = Process(target=self.calculate_, args=(matrix, user_id, movie_lists[5], movies_seen,))
        p5.start()
        p6 = Process(target=self.calculate_, args=(matrix, user_id, movie_lists[6], movies_seen,))
        p6.start()
        p7 = Process(target=self.calculate_, args=(matrix, user_id, movie_lists[7], movies_seen,))
        p7.start()
        p8 = Process(target=self.calculate_, args=(matrix, user_id, movie_lists[8], movies_seen,))
        p8.start()
        p9 = Process(target=self.calculate_, args=(matrix, user_id, movie_lists[9], movies_seen, ))
        p9.start()

        while p0.is_alive() | p1.is_alive() | p2.is_alive() | p3.is_alive() | p4.is_alive() | p5.is_alive() | p6.is_alive() | p7.is_alive() | p8.is_alive() | p9.is_alive():
            num = 0

        print("开始排序")
        print(self.dictionary)
        new_list = sorted(self.dictionary.items(), key=lambda x: x[1], reverse=True)
        print("排序结束")
        for each in new_list:
            print("编号: "+str(each[0])+" 预测分数: "+str(each[1]))
        for each in new_list:
            if each[1] >= 4.5:
                rec_movies.append(each[0])
        if len(rec_movies) > n:
            rec_movies = random.sample(rec_movies, n)
        print(rec_movies)
        end = time.time()
        print(end-start)
        return rec_movies

    def recommend_for_user(self, user_id, n):
        movies_df = pd.read_csv('../dataset/new_movies.csv', encoding='utf-8')
        movies = self.recommend(user_id, n)
        movie_list = []
        for each in movies:
            movie_info = []
            title = list(movies_df[movies_df.id == each]['title'])[0]
            movie_info.append(title)

            stars = ""
            star = list(movies_df[movies_df.id == each]['star'])[0]
            for every in star:
                if every != '"' and every != ',' and every != '[' and every != ']':
                    stars += every
                elif every == ',':
                    stars += ' '
            movie_info.append(stars)

            genres = ""
            genres_str = list(movies_df[movies_df.id == each]['genres'])[0]
            for every in genres_str:
                if every != '"' and every != ',' and every != '[' and every != ']':
                    genres += every
                elif every == ',':
                    genres += ' '
            movie_info.append(genres)

            rating = list(movies_df[movies_df.id == each].rating)[0]
            movie_info.append(rating)

            duration = list(movies_df[movies_df.id == each].duration)[0]
            movie_info.append(duration)

            movie_list.append(movie_info)

        return movie_list



    def split_list(self,list1):
        sum_list = []
        each = []
        num = 0
        length = len(list1)
        for i in range(length):
            if (i % int(length/10) == 0) & (i != 0) & (num != 9):
                num += 1
                sum_list.append(each)
                each = []
            each.append(list1[i])
        sum_list.append(each)
        return sum_list


    def calculate_(self,um_matrix, user_id, movie_list, movies_seen: dict):
        for each in movie_list:
            if each in movies_seen.keys():
                continue
            else:
                k = self.cal_slope_one(um_matrix, user_id, each)
                self.dictionary[each] = k
                print(str(each) +": "+str(self.dictionary[each]))



if __name__ == "__main__":
    #matrix = generate_matrix()
    #print(cal_slope_one(matrix, 'woyang', 1358421))
    # createOutput()
    iu = slope_one()
    iu.recommend('woyang', 10)