#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pandas as pd
import random
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from recommendalgorithm.recommend import ItemCF
from movie_detailed_search import MovieDetailedSearch
from user_center import UserCenter


class NewMainWindow(QWidget):
    def __init__(self, movies, user_name, label):
        super(NewMainWindow, self).__init__()  # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("电影推荐系统")
        self.setWindowIcon(QIcon('../movie.jpg'))  # 设置窗口图标
        self.resize(1400, 800)
        self.itemCF = ItemCF('../dataset/behaviours_new.csv','../dataset/new_movies.csv')
        self.user_df = pd.read_csv('../dataset/behaviours_new.csv')
        self.user_df = self.user_df.iloc[:, [1, 2, 3]]
        self.movies_df = pd.read_csv('../dataset/new_movies.csv', encoding='utf-8')
        self.movies_df = self.movies_df.iloc[:, [0, 2, 5, 6, 9, 10]]
        self.movies_df = self.movies_df.drop_duplicates(subset='title')
        self.movies_df = self.movies_df.rename(columns={'Unnamed: 0': 'Movie_ID'})
        self.user = user_name
        self.user_movie_num = len(list(self.user_df[self.user_df['user_id'] == self.user].movie_id))
        self.user_movie_num_show = str(self.user_movie_num)

        self.welcome_label = QLabel(self)
        self.user_label = label

        self.welcome_label.setText("<h1>欢迎您! " + self.user + "</h1>")
        self.recommend_label = QLabel("<h1>为您推荐以下电影:</h1>", self)

        self.recommend_table = QTableWidget(self)
        self.hot_movies_label = QLabel("<h1>热门电影:</h1>", self)
        self.hot_movies_table = QTableWidget(self)

        self.user_center = QPushButton("个人主页", self)
        self.user_center.clicked.connect(lambda: self.show_user_center(self.user, self.user_movie_num_show, self.user_label))
        self.movie_detailed_button = QPushButton("电影详细页面", self)
        self.movie_detailed_button.clicked.connect(self.movie_detailed)
        self.hot_rec_movies = self.itemCF.rec_hot_movies(2018, 2022)  # 热门电影
        self.rec_movies = movies

        self.rec_refresh = QPushButton("重新推荐", self)
        self.rec_refresh.clicked.connect(self.refresh)

        self.option_label = QLabel(self)
        self.option_label.setText("选择年代:")

        self.year1 = QPushButton("2017至今", self)
        self.year2 = QPushButton("2010-2017", self)
        self.year3 = QPushButton("00年代", self)
        self.year4 = QPushButton("90年代", self)
        self.year5 = QPushButton("更早", self)

        # 选择不同年份推荐不同热门电影
        self.year1.clicked.connect(self.select1)
        self.year2.clicked.connect(self.select2)
        self.year3.clicked.connect(self.select3)
        self.year4.clicked.connect(self.select4)
        self.year5.clicked.connect(self.select5)

        self.v1_layout = QVBoxLayout()
        self.v2_layout = QVBoxLayout()
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.h3_layout = QHBoxLayout()
        self.h4_layout = QHBoxLayout()
        self.h_layout = QHBoxLayout()

        self.h1_layout.addWidget(self.welcome_label)
        self.h1_layout.addWidget(self.user_center)
        self.v1_layout.addLayout(self.h1_layout)
        self.h3_layout.addWidget(self.recommend_label)
        self.h3_layout.addWidget(self.rec_refresh)
        self.v1_layout.addLayout(self.h3_layout)
        self.v1_layout.addWidget(self.recommend_table)

        # 右边
        self.h2_layout.addWidget(self.hot_movies_label)
        self.h2_layout.addWidget(self.movie_detailed_button)

        self.h4_layout.addWidget(self.option_label)
        self.h4_layout.addWidget(self.year1)
        self.h4_layout.addWidget(self.year2)
        self.h4_layout.addWidget(self.year3)
        self.h4_layout.addWidget(self.year4)
        self.h4_layout.addWidget(self.year5)

        self.v2_layout.addLayout(self.h2_layout)
        self.v2_layout.addLayout(self.h4_layout)
        self.v2_layout.addWidget(self.hot_movies_table)

        self.h_layout.addLayout(self.v1_layout)
        self.h_layout.addLayout(self.v2_layout)

        self.setLayout(self.h_layout)

        self.rec_movies_table_init()
        self.hot_movies_table_init()
        self.set_hot_movie_table(self.hot_rec_movies)
        self.set_rec_movies_table(self.rec_movies)

    def rec_movies_table_init(self):
        self.recommend_table.setColumnCount(5)
        self.recommend_table.setHorizontalHeaderLabels(['电影名称', '主演', '电影类型', '电影评分', '电影时长'])
        self.recommend_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.recommend_table.setRowCount(0)

    def hot_movies_table_init(self):
        self.hot_movies_table.setColumnCount(6)
        self.hot_movies_table.setHorizontalHeaderLabels(['电影名称', '主演', '评分', '电影类型', '上映时间', '电影时长'])
        self.hot_movies_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hot_movies_table.setRowCount(0)

    def set_rec_movies_table(self, movies):
        row = self.recommend_table.rowCount()
        print("傻逼")
        for i in range(len(movies)):
            print(movies[i])
            self.recommend_table.insertRow(row)
            self.name = "《" + movies[i][0] + "》"
            if pd.isna(movies[i][1]):
                self.actors = "无"
            else:
                self.actors = movies[i][1]
            self.genres = movies[i][2]
            self.rating = str(movies[i][3])
            self.duration = str(movies[i][4])

            self.recommend_table.setItem(row, 0, QTableWidgetItem(self.name))
            self.recommend_table.setItem(row, 1, QTableWidgetItem(self.actors))
            self.recommend_table.setItem(row, 2, QTableWidgetItem(self.genres))
            self.recommend_table.setItem(row, 3, QTableWidgetItem(self.rating))
            self.recommend_table.setItem(row, 4, QTableWidgetItem(self.duration))

    def set_hot_movie_table(self, hot_rec_movies):
        row = self.hot_movies_table.rowCount()

        for i in range(len(self.hot_rec_movies)):
            self.hot_movies_table.insertRow(row)
            self.hot_movies_name = "《" + self.hot_rec_movies[i][0] + "》"
            self.hot_movies_actors = self.hot_rec_movies[i][1]
            self.hot_movies_rating = str(self.hot_rec_movies[i][2])
            self.hot_movies_genres = self.hot_rec_movies[i][3]

            self.hot_movies_year = str(int(self.hot_rec_movies[i][4]))
            self.hot_movies_duration = str(self.hot_rec_movies[i][5])

            self.hot_movies_table.setItem(row, 0, QTableWidgetItem(self.hot_movies_name))
            self.hot_movies_table.setItem(row, 1, QTableWidgetItem(self.hot_movies_actors))
            self.hot_movies_table.setItem(row, 2, QTableWidgetItem(self.hot_movies_rating))
            self.hot_movies_table.setItem(row, 3, QTableWidgetItem(self.hot_movies_genres))
            self.hot_movies_table.setItem(row, 4, QTableWidgetItem(self.hot_movies_year))
            self.hot_movies_table.setItem(row, 5, QTableWidgetItem(self.hot_movies_duration))

    def movie_detailed(self):
        self.movie_detailed_fun = MovieDetailedSearch(self.user)
        self.movie_detailed_fun.show()

    def show_user_center(self, user, num, label):
        self.show_user = UserCenter(user, num, label)
        self.show_user.show()

    def select1(self):
        self.hot_rec_movies = self.itemCF.rec_hot_movies(2017, 2021)  # 热门电影
        self.hot_movies_table_init()
        self.set_hot_movie_table(self.hot_rec_movies)

    def select2(self):
        self.hot_rec_movies = self.itemCF.rec_hot_movies(2010, 2017)  # 热门电影
        self.hot_movies_table_init()
        self.set_hot_movie_table(self.hot_rec_movies)

    def select3(self):
        self.hot_rec_movies = self.itemCF.rec_hot_movies(2000, 2009)  # 热门电影
        self.hot_movies_table_init()
        self.set_hot_movie_table(self.hot_rec_movies)

    def select4(self):
        self.hot_rec_movies = self.itemCF.rec_hot_movies(1990, 1999)  # 热门电影
        self.hot_movies_table_init()
        self.set_hot_movie_table(self.hot_rec_movies)

    def select5(self):
        self.hot_rec_movies = self.itemCF.rec_hot_movies(1900, 1989)  # 热门电影
        self.hot_movies_table_init()
        self.set_hot_movie_table(self.hot_rec_movies)

    def refresh(self):
        self.movies_df1 = pd.read_csv('../dataset/new_movies.csv', encoding='utf-8')
        self.movies_df1 = self.movies_df1.iloc[:, [0, 1, 2, 5, 6, 9, 10, 12]]

        self.movies_df1 = self.movies_df1.drop_duplicates(subset='id')
        self.movies_df1 = self.movies_df1.rename(columns={'Unnamed: 0': 'Movie_ID'})

        self.movies_df1['genres'] = self.movies_df1['genres'].fillna('0')  # 缺失值填充
        self.new_user_like = self.movies_df1[self.movies_df1['genres'].str.contains(self.user_label)]
        self.new_user_rec = self.new_user_like[self.new_user_like.rating >= 7]

        self.new_user_rec = self.new_user_rec.iloc[:, [2, 3, 4, 5, 6, 7]]

        self.new_user_rec_movies = []  # 存储新用户推荐电影

        for each in list(self.new_user_rec['title']):
            self.temp = []
            self.temp.append(each)
            self.movie_stars = ""
            for every in list(self.new_user_rec[self.new_user_rec.title == each]['star'])[0]:
                if every != '"' and every != ',' and every != '[' and every != ']':
                    self.movie_stars += every
                elif every == ',':
                    self.movie_stars += ' '
            self.temp.append(self.movie_stars)
            self.movie_genres = ""
            for every in list(self.new_user_rec[self.new_user_rec.title == each].genres)[0]:
                if every != '"' and every != ',' and every != '[' and every != ']':
                    self.movie_genres += every
                elif every == ',':
                    self.movie_genres += ' '
            self.temp.append(self.movie_genres)
            self.temp.append(list(self.new_user_rec[self.new_user_rec.title == each].rating)[0])  # 电影评分
            self.temp.append(list(self.new_user_rec[self.new_user_rec.title == each].duration)[0])  # 电影时长
            self.new_user_rec_movies.append(self.temp)

        self.new_user_rec_movies_refresh = []
        for i in range(15):
            self.new_user_rec_movies_refresh.append(random.choice(self.new_user_rec_movies))

        self.rec_movies_table_init()
        self.set_rec_movies_table(self.new_user_rec_movies_refresh)

