#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
预处理数据集，获取数据集有用的数据并拆分为训练集和测试集
"""
import pandas as pd
import csv


def get_usable_data():
    """
    获取有用数据
    :return:
    """
    movies = pd.read_csv('../dataset/movies.csv', encoding='utf-8')
    movie_ids = list(movies['id'])
    index = 0
    num = 1
    print(movie_ids[1])
    effective = []
    with open('../dataset/new_user_behaviour.csv', 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            lis = []
            if index == 0:
                index += 1
                continue
            if int(i[2]) in movie_ids:
                print(num)
                num += 1
                lis.append(i[1])
                lis.append(i[2])
                lis.append(i[3])
                effective.append(lis)
    columns = ['user_id', 'movie_id', 'rating']
    new_file = pd.DataFrame(columns=columns, data=effective)
    new_file.to_csv('../dataset/behaviours_new.csv')


def split_dataset():
    """
    将数据集拆分为训练集和测试集
    :return:
    """
    users = pd.read_csv('../dataset/new_user_info.csv',encoding='utf-8')
    train = []
    test = []
    all_user = list(users['user_id'])
    dicts = {}
    index = -1
    for each in all_user:
        dicts[each] = 0
    with open('../dataset/behaviours_new.csv', 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            if index == -1:
                index += 1
                continue
            if i[1] not in dicts.keys():
                print(i[1])
                print(index)
                dicts[i[1]] = 0
                dicts[i[1]] = dicts[i[1]] + 1
                i.remove(str(index))
                train.append(i)
                index += 1
            else:
                if dicts[i[1]] % 2 == 0:
                    print(index)
                    dicts[i[1]] = dicts[i[1]] + 1
                    print(dicts[i[1]])
                    i.remove(str(index))
                    train.append(i)
                    index += 1
                else:
                    print(index)
                    dicts[i[1]] = dicts[i[1]] + 1
                    print(dicts[i[1]])
                    i.remove(str(index))
                    test.append(i)
                    index += 1
    columns = ['user_id', 'movie_id', 'rating']
    train_set = pd.DataFrame(columns=columns, data=train)
    train_set.to_csv('../dataset/train.csv')

    test_set = pd.DataFrame(columns=columns, data=test)
    test_set.to_csv('../dataset/test.csv')


def addIndex():
    result = []
    with open("../dataset/movies.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        index = 0
        for line in reader:
            if(index == 0):
                index += 1
                continue
            else:
                result.append(line)
                print(index)
                index += 1
    f.close()
    columns = ['id', 'title', 'director', 'screenwriter', 'star', 'rating', 'rating_number',
               'summary', 'genres', 'duration', 'language', 'year', 'othername', 'comments', 'cover_url']
    new_movie = pd.DataFrame(columns=columns, data=result)
    new_movie.to_csv('../dataset/new_movies.csv', encoding='utf-8')


if __name__ == '__main__':
    #get_usable_data()
    #split_dataset()
    addIndex()
