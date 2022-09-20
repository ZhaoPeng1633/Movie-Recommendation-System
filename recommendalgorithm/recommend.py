# -*- coding: utf-8 -*-
import random

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity  # 计算余弦相似度

"""
基于电影相似度的协同过滤
"""

# 用户信息
class ItemCF:
    def __init__(self, behaviour_path, movie_path):
        self.user_df = pd.read_csv(behaviour_path)
        self.user_df = self.user_df.iloc[:, [1, 2, 3]]   # 选取第2，3，4列(user_id、movie_id、rating)

        # 电影信息
        self.movies_df = pd.read_csv(movie_path, encoding='utf-8')
        # 0 1 2 3 5 6 9 10 12
        self.movies_df = self.movies_df.iloc[:, [0, 1, 2, 3, 5, 6, 9, 10, 12]]  # 选取若干列名字、演员、评分、种类、年份、电影ID等信息
        self.movies_df = self.movies_df.drop_duplicates(subset='id')
        self.movies_df = self.movies_df.rename(columns={'Unnamed: 0': 'Movie_ID'})

        # 用户ID映射
        self.usersMap = dict(enumerate(list(self.user_df['user_id'].unique())))  # 用户id与其对应索引的映射关系(不重复)
        self.usersMap = dict(zip(self.usersMap.values(), self.usersMap.keys()))  # 键值互换  索引-评分用户 ——> 用户—索引

        # 电影ID映射
        self.moviesMap_raw = dict(enumerate(list(self.movies_df['id'])))  # 电影id与其对应索引的映射关系
        self.moviesMap = dict(zip(self.moviesMap_raw.values(), self.moviesMap_raw.keys()))  # 键值互换

        self.n_users = self.user_df.user_id.unique().shape[0]  # 用户总数 shape[0]返回的是行数
        self.n_movies = self.movies_df.Movie_ID.unique().shape[0]  # 电影总数 shape[0]返回的是行数

        self.data_matrix = np.zeros((self.n_users, self.n_movies))  # 用户-物品矩阵雏形

        # 构造用户-物品矩阵
        for line in self.user_df.itertuples():
            try:
                self.data_matrix[self.usersMap[str(line[1])],self. moviesMap[int(line[2])]] = line[3]
                # usersMap[str(line[1])]为0开始的索引值为矩阵的行(对应用户ID)
                # moviesMap[line[2]]为0开始的索引值为矩阵的列(对应电影ID)
                # 故行号对应用户ID,列号对应电影ID,该位置上的值对应该用户对该电影的评分
            except:
                pass
        # 电影余弦相似度矩阵(n×n阶矩阵)
        self.item_similarity = cosine_similarity(self.data_matrix.T)  # 转置之后计算的才是电影的相似度


    def rec_hot_movies(self, year1, year2):    # 通过输入相应年份来推荐对应年份至现在的热门电影
        """
        @功能: 获取热门推荐电影
        @参数: 无
        @返回: 热门推荐电影列表
        """
        self.hot_movies_raw = self.movies_df[(self.movies_df.year >= year1) & (self.movies_df.year <= year2)]
        self.hot_movies_raw = self.hot_movies_raw[self.hot_movies_raw.rating >= 8.7]
        #0 1 2 3 5 6 9 10 12
        self.hot_movies_raw = self.hot_movies_raw.iloc[:, [2, 4, 5, 6, 7, 8]] #名称 主演 评分 电影类型 上映时间 电影时长
        self.hot_rec_movies = []  # 存储热门推荐电影

        for each in list(self.hot_movies_raw['title']):
            self.hot_movies_info = []
            self.hot_movies_info.append(each)
            self.stars = ""
            self.star = list(self.hot_movies_raw[self.hot_movies_raw.title == each]['star'])[0]
            for every in self.star:
                if every != '"' and every != ',' and every != '[' and every != ']':
                    self.stars += every
                elif every == ',':
                    self.stars += ' '
            self.hot_movies_info.append(self.stars)

            self.rating = list(self.hot_movies_raw[self.hot_movies_raw.title == each].rating)[0]
            self.hot_movies_info.append(self.rating)

            self.genres = ""
            self.genres_str = list(self.hot_movies_raw[self.hot_movies_raw.title == each]['genres'])[0]
            for every in self.genres_str:
                if every != '"' and every != ',' and every != '[' and every != ']':
                    self.genres += every
                elif every == ',':
                    self.genres += ' '
            self.hot_movies_info.append(self.genres)

            self.year = list(self.hot_movies_raw[self.hot_movies_raw.title == each].year)[0]
            self.hot_movies_info.append(self.year)

            self.duration = list(self.hot_movies_raw[self.hot_movies_raw.title == each].duration)[0]
            self.hot_movies_info.append(self.duration)
            self.hot_rec_movies .append(self.hot_movies_info)

        return self.hot_rec_movies


    def Recommend(self, movie_id, k):  # movie_id:电影名关键词，k:为最相似的k部电影
        """
        @功能: 获得推荐电影列表
        @参数: 电影ID、每部电影选取最相似的数目
        @返回: 推荐电影列表
        """
        self.movie_list = []  # 存储结果
        # 过滤电影数据集，搜索找到对应的电影的id
        self.movieid = list(self.movies_df[self.movies_df['id'] == int(movie_id)].Movie_ID)[0]
        # 获取该电影的余弦相似度数组  (数组存储的是该电影与其他电影的相似度)
        self.movie_similarity = self.item_similarity[self.movieid]
        # 返回前k个最高相似度的索引位置
        self.movie_similarity_index = np.argsort(-self.movie_similarity)[1:k + 1]  # 此处将相似度按降序排列，返回对应的索引数组
        for i in list(self.movie_similarity_index):
            self.rec_movies = []  # 每部推荐的电影

            self.rec_movies.append(list(self.movies_df[self.movies_df.Movie_ID == i].id)[0])    # id
            self.rec_movies.append(list(self.movies_df[self.movies_df.Movie_ID == i].title)[0])  # 电影名

            self.rec_stars = ""
            self.rec_star = list(self.movies_df[self.movies_df.Movie_ID == i]['star'])[0]
            for every in self.rec_star:
                if every != '"' and every != ',' and every != '[' and every != ']':
                    self.rec_stars += every
                elif every == ',':
                    self.rec_stars += ' '
            self.rec_movies.append(self.rec_stars)

            self.rec_genres = ""
            self.rec_genres_str = list(self.movies_df[self.movies_df.Movie_ID == i].genres)[0]
            for each in self.rec_genres_str:
                if each != '"' and each != ',' and each != '[' and each != ']':
                    self.rec_genres += each
                elif each == ',':
                    self.rec_genres += ' '

            self.rec_movies.append(self.rec_genres)  # 电影类型
            self.rec_movies.append(list(self.movies_df[self.movies_df.Movie_ID == i].rating)[0])  # 电影评分
            self.rec_movies.append(list(self.movies_df[self.movies_df.Movie_ID == i].duration)[0])  # 电影时长
            self.movie_list.append(self.rec_movies)  # 列表中的元素为列表，存储相关信息

        return self.movie_list


    def find_user_like(self, user_id, num):
        self.user_seen_movies = self.user_df[self.user_df['user_id'] == '{}'.format(user_id)].movie_id  # 用户看过的电影的ID
        self.userlike_movies = []  # 储存用户比较喜欢的电影ID

        for i in list(self.user_seen_movies):
            if int(float(list(self.user_df[self.user_df['movie_id'] == i].rating)[0])) >= 4:
                self.userlike_movies.append(list(self.user_df[self.user_df['movie_id'] == i].movie_id)[0])  # 找出用户比较喜欢的电影的ID

        self.user_like_movies = []  # 储存用户喜欢的随机5部
        if len(self.userlike_movies) != 0:
            for i in range(5):
                self.user_like_movies.append(random.choice(self.userlike_movies))

        self.rec = []
        self.rec1 = []
        for each in self.user_like_movies:
            self.rec.extend(self.Recommend(each, num))
        for each in self.rec:
            if each not in self.rec1:
                each.remove(each[0])
                self.rec1.append(each)
        return self.rec1

    def evaluate(self):
        print("开始！")
        sum = 0
        self.test_set = pd.read_csv('../dataset/test.csv', encoding='utf-8')
        self.users = self.user_df.drop_duplicates(subset='user_id')
        self.users = list(self.users['user_id'])
        # self.users = ['doskevin407']
        user_num = len(self.users)
        for each in self.users:
            num = 0
            self.actually_like = list(self.test_set[(self.test_set.user_id == each) & (self.test_set.rating >= 4)].movie_id)
            # print(self.actually_like)
            self.user_rec = self.find_user_like(each, 10)
            # print(self.user_rec)
            if len(self.user_rec) != 0:
                if len(self.actually_like) == 0:
                    user_num -= 1
                else:
                    for every in self.user_rec:
                        if every[0] in self.actually_like:
                            num += 1
                    print(str(each)+": " + " 查准率: " +str(float(num/len(self.user_rec))))
                    sum += float(num/len(self.user_rec))
            else:
                user_num -= 1
        return sum/user_num


if __name__ == '__main__':
    # 对算法做评估：查准率和查全率
    itemCF = ItemCF('../dataset/train.csv', '../dataset/new_movies.csv')
    print("平均查准率为：" + str(itemCF.evaluate()))
