#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys

import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from recommendalgorithm.recommend import ItemCF
from recommendalgorithm.recommend2 import PersonalKnnRecommender
from recommendalgorithm.recommend3 import slope_one


from movie_detailed_search import MovieDetailedSearch
from recommendalgorithm.recommend4 import SVD
from user_center import UserCenter


class MainWindow(QWidget):
    def __init__(self, user):
        super(MainWindow, self).__init__()  # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("电影推荐系统")
        self.setWindowIcon(QIcon('../movie.jpg'))  # 设置窗口图标
        self.resize(1400, 800)

        self.itemCF = ItemCF('../dataset/behaviours_new.csv', '../dataset/new_movies.csv')
        self.knn = PersonalKnnRecommender('../dataset/behaviours_new.csv', '../dataset/new_movies.csv')
        self.so = slope_one()
        self.SVD = SVD()
        self.user_df = pd.read_csv('../dataset/behaviours_new.csv')
        self.user_df = self.user_df.iloc[:, [1, 2, 3]]
        self.movies_df = pd.read_csv('../dataset/new_movies.csv', encoding='utf-8')
        self.movies_df = self.movies_df.iloc[:, [0, 2, 5, 6, 9, 10]]
        self.movies_df = self.movies_df.drop_duplicates(subset='title')
        self.movies_df = self.movies_df.rename(columns={'Unnamed: 0': 'Movie_ID'})
        self.user = user        # # # key
        self.user_movie_num = len(list(self.user_df[self.user_df['user_id'] == user].movie_id))   # 该用户所看过(评论过)的电影数量
        self.user_movie_num_show = str(self.user_movie_num)

        self.USER_PWD = dict()
        self.USER_Label = dict()
        f = open('../dataset/new_user_info.csv', 'a+')
        f.seek(0)  # 文件指针指向开头
        for line in f:
            self.USER_PWD[line.split(',')[0]] = line.split(',')[1].strip()  # 存入用户名密码
            try:
                self.USER_Label[line.split(',')[0]] = line.split(',')[2].strip()  # 存入用户标签
            except:
                self.USER_Label[line.split(',')[2]] = None
        f.close()

        self.user_label = self.USER_Label[user]
        self.welcome_label = QLabel(self)

        self.recommend_table = QTableWidget(self)

        self.welcome_label.setText("<h1>欢迎您! " + self.user + "</h1>")
        self.recommend_label = QLabel("<h1>为您推荐以下电影:</h1>", self)
        self.rec1 = QPushButton("推荐1", self)
        self.rec2 = QPushButton("推荐2", self)
        self.rec3 = QPushButton("推荐3", self)
        self.rec4 = QPushButton("推荐4", self)

        self.rec1.clicked.connect(lambda: self.refresh_one())
        self.rec2.clicked.connect(lambda: self.refresh_two())
        self.rec3.clicked.connect(lambda: self.refresh_three())
        self.rec4.clicked.connect(lambda: self.refresh_four())

        self.option_label = QLabel(self)
        self.option_label.setText("选择年代:")

        self.year1 = QPushButton("2017至今", self)
        self.year2 = QPushButton("2010-2017", self)
        self.year3 = QPushButton("00年代", self)
        self.year4 = QPushButton("90年代", self)
        self.year5 = QPushButton("更早", self)

        self.hot_movies_label = QLabel("<h1>热门电影:</h1>", self)
        self.hot_movies_table = QTableWidget(self)

        # 选择不同年份推荐不同热门电影
        self.year1.clicked.connect(self.select1)
        self.year2.clicked.connect(self.select2)
        self.year3.clicked.connect(self.select3)
        self.year4.clicked.connect(self.select4)
        self.year5.clicked.connect(self.select5)

        self.user_center = QPushButton("个人主页", self)
        self.user_center.clicked.connect(lambda: self.show_user_center(user, self.user_movie_num_show, self.user_label))
        self.movie_detailed_button = QPushButton("电影详细页面", self)
        self.movie_detailed_button.clicked.connect(self.movie_detailed)     # 调用movie_detailed模块弹出电影详细信息
        self.hot_rec_movies = self.itemCF.rec_hot_movies(2018, 2022)  # 热门电影
        self.rec_movies = self.itemCF.find_user_like(self.user, 7)  # 推荐电影

        self.v1_layout = QVBoxLayout()
        self.v2_layout = QVBoxLayout()
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.h3_layout = QHBoxLayout()
        self.h4_layout = QHBoxLayout()
        self.h_layout = QHBoxLayout()
        # 左侧部分
        self.h1_layout.addWidget(self.welcome_label)
        self.h1_layout.addWidget(self.user_center)
        self.v1_layout.addLayout(self.h1_layout)
        self.h3_layout.addWidget(self.recommend_label)
        self.h3_layout.addWidget(self.rec1)
        self.h3_layout.addWidget(self.rec2)
        self.h3_layout.addWidget(self.rec3)
        self.h3_layout.addWidget(self.rec4)

        self.v1_layout.addLayout(self.h3_layout)
        self.v1_layout.addWidget(self.recommend_table)
        # 右侧部分
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
        self.recommend_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   # 均匀拉直表头
        self.recommend_table.setRowCount(0)

    def hot_movies_table_init(self):
        self.hot_movies_table.setColumnCount(6)
        self.hot_movies_table.setHorizontalHeaderLabels(
            ['电影名称', '主演', '评分', '电影类型', '上映时间', '时长'])
        self.hot_movies_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 均匀拉直表头
        self.hot_movies_table.setRowCount(0)

    def set_rec_movies_table(self, rec_movies):
        row = self.recommend_table.rowCount()
        try:
            for i in range(len(self.rec_movies)):
                self.recommend_table.insertRow(row)
                self.name = "《" + self.rec_movies[i][0] + "》"
                if pd.isna(self.rec_movies[i][1]):
                    self.actors = "无"
                else:
                    self.actors = self.rec_movies[i][1]
                self.style = self.rec_movies[i][2]
                self.rating = str(self.rec_movies[i][3])
                self.duration = str(self.rec_movies[i][4])

                self.recommend_table.setItem(row, 0, QTableWidgetItem(self.name))
                self.recommend_table.setItem(row, 1, QTableWidgetItem(self.actors))
                self.recommend_table.setItem(row, 2, QTableWidgetItem(self.style))
                self.recommend_table.setItem(row, 3, QTableWidgetItem(self.rating))
                self.recommend_table.setItem(row, 4, QTableWidgetItem(self.duration))
        except:
            pass

    def refresh_one(self):
        self.rec_movies = self.itemCF.find_user_like(self.user, 7)  # 推荐电影
        self.rec_movies_table_init()
        self.set_rec_movies_table(self.rec_movies)

    def refresh_two(self):
        self.rec_movies = self.knn.recommend_for_user(self.user, 15)  # 推荐电影
        self.rec_movies_table_init()
        self.set_rec_movies_table(self.rec_movies)

    def refresh_three(self):
        self.rec_movies = self.so.recommend_for_user(self.user, 15)  # 推荐电影
        self.rec_movies_table_init()
        self.set_rec_movies_table(self.rec_movies)

    # 待修改： 第四个算法
    def refresh_four(self):
        self.rec_movies = self.SVD.recommend_svd(self.user, 15)  # 只需要修改这一行
        self.rec_movies_table_init()
        self.set_rec_movies_table(self.rec_movies)

    def set_hot_movie_table(self, hot_rec_movies):
        row = self.hot_movies_table.rowCount()

        for i in range(len(self.hot_rec_movies)):
            print(self.hot_rec_movies[i])
            self.hot_movies_table.insertRow(row)
            self.hot_movies_name = "《" + self.hot_rec_movies[i][0] + "》"
            self.hot_movies_actors = self.hot_rec_movies[i][1]
            self.hot_movies_rating = str(self.hot_rec_movies[i][2])
            self.hot_movies_style = self.hot_rec_movies[i][3]

            self.hot_movies_year = str(int(self.hot_rec_movies[i][4]))
            self.hot_movies_duration = str(self.hot_rec_movies[i][5])

            self.hot_movies_table.setItem(row, 0, QTableWidgetItem(self.hot_movies_name))
            self.hot_movies_table.setItem(row, 1, QTableWidgetItem(self.hot_movies_actors))
            self.hot_movies_table.setItem(row, 2, QTableWidgetItem(self.hot_movies_rating))
            self.hot_movies_table.setItem(row, 3, QTableWidgetItem(self.hot_movies_style))
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow('doskevin407')
    main.show()
    sys.exit(app.exec_())
