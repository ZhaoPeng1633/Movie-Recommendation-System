#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys
import random
import pandas as pd
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton


class MovieDetailed(QWidget):
    def __init__(self, name, username):
        super(MovieDetailed, self).__init__()  # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("电影详细信息")
        self.setWindowIcon(QIcon('../movie.jpg'))  # 设置窗口图标
        self.resize(1400, 800)
        self.name = name
        self.user_name = username           # 用户名存储信息用
        # 用户看过电影
        self.user_behaviour = pd.read_csv('../dataset/behaviours_new.csv')
        self.movies_seen = list(self.user_behaviour[self.user_behaviour.user_id == "{}".format(self.user_name)]['movie_id'])
        # 电影详细信息
        self.movies_detailed = pd.read_csv('../dataset/new_movies.csv', encoding='utf-8')
        self.movies_detailed = self.movies_detailed.iloc[:, [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]]
        if name in list(self.movies_detailed['title']):
            length = len(self.movies_detailed['title'])
            for i in range(length):
                if self.movies_detailed['title'][i] == name:
                    self.movie_id = self.movies_detailed['id'][i]
                    break

            # 电影别名
            if pd.isna(list(self.movies_detailed[self.movies_detailed.title == "{}".format(self.name)].othername)[0]):
                self.other_name = ''
            else:
                self.other_name = list(self.movies_detailed[self.movies_detailed.title == "{}".format(self.name)].othername)[0]

            # 导演
            self.director = list(self.movies_detailed[self.movies_detailed.title == "{}".format(self.name)].director)[0]

            # 编剧
            self.writer = list(self.movies_detailed[self.movies_detailed.title == "{}".format(self.name)].screenwriter)[0]

            # 主演
            stars = ''
            self.actors = list(self.movies_detailed[self.movies_detailed.title == "{}".format(self.name)].star)[0]
            for every in self.actors:
                if every != '"' and every != '[' and every != ']':
                    stars += every
            self.actors = stars

            # 评分
            self.rating = list(self.movies_detailed[self.movies_detailed.title == "{}".format(self.name)].rating)[0]

            # 电影种类
            self.genres = ''
            self.genres_str = list(self.movies_detailed[self.movies_detailed.title == "{}".format(self.name)]['genres'])[0]
            for every in self.genres_str:
                if every != '"' and every != ',' and every != '[' and every != ']':
                    self.genres += every
                elif every == ',':
                    self.genres += ' '

            # 电影语言
            self.language = list(self.movies_detailed[self.movies_detailed.title == "{}".format(self.name)].language)[0]

            # 上映年代
            self.year = list(self.movies_detailed[self.movies_detailed.title == "{}".format(self.name)].year)[0]

            # 电影时长
            self.duration = list(self.movies_detailed[self.movies_detailed.title == "{}".format(self.name)].duration)[0]

            # 电影简介
            self.summary = list(self.movies_detailed[self.movies_detailed.title == "{}".format(self.name)].summary)[0]

            self.name_label = QLabel("<font size=10><b>" + self.name + " 别名：" + self.other_name.split('/')[0] + "</b></font>")
            self.directors_label = QLabel("<h2>" + "导演: " + self.director + "</h2>")
            self.writer_label = QLabel("<h2>" + "编剧: " + self.writer + "</h2>")
            self.actors_label = QLabel("<h2>" + "主演: " + self.actors.split(',')[0] + "</h2>")
            self.style_label = QLabel("<h2>" + "类型: " + self.genres + "</h2>")

            self.language_label = QLabel("<h2>" + "语言: " + self.language + "</h2>")
            self.year_label = QLabel("<h2>" + "上映时间: " + str(int(self.year)) + "</h2>")
            self.duration_label = QLabel("<h2>" + "片长: " + str(int(self.duration)) + "分钟" + "</h2>")

            self.rate_label = QLabel("<h1>" + "评分: " + str(self.rating) + "</h1>")

            # 为电影评分
            self.tip_label = QLabel("<h2>"+ "请为该电影评分(若按钮不可点击则代表您已评分)" +"</h2>")
            self.one_button = QPushButton("1")
            self.two_button = QPushButton("2")
            self.three_button = QPushButton("3")
            self.four_button = QPushButton("4")
            self.five_button = QPushButton("5")
            self.button_init()

            self.summary_label = QLabel("<h1><b>电影简介:</b></h1>", self)
            self.summary_browser = QTextBrowser(self)
            self.summary_browser.setText("<h2>" + self.summary + "</h2>")

            # 控件布局间的嵌套
            self.v1_layout = QVBoxLayout()
            self.v2_layout = QVBoxLayout()
            self.v3_layout = QVBoxLayout()
            self.h_layout = QHBoxLayout()
            self.h1_layout = QHBoxLayout()
            self.v_layout = QVBoxLayout()
            # 垂直布局
            self.v1_layout.addWidget(self.directors_label)
            self.v1_layout.addWidget(self.writer_label)
            self.v1_layout.addWidget(self.actors_label)
            self.v1_layout.addWidget(self.style_label)
            # 垂直布局
            self.v2_layout.addWidget(self.language_label)
            self.v2_layout.addWidget(self.year_label)
            self.v2_layout.addWidget(self.duration_label)
            #水平布局
            self.h1_layout.addWidget(self.one_button)
            self.h1_layout.addWidget(self.two_button)
            self.h1_layout.addWidget(self.three_button)
            self.h1_layout.addWidget(self.four_button)
            self.h1_layout.addWidget(self.five_button)

            # 垂直布局
            self.v3_layout.addWidget(self.rate_label)
            self.v3_layout.addWidget(self.tip_label)
            self.v3_layout.addLayout(self.h1_layout)
            # 水平布局
            self.h_layout.addLayout(self.v1_layout)
            self.h_layout.addLayout(self.v2_layout)
            self.h_layout.addLayout(self.v3_layout)
            # 垂直布局
            self.v_layout.addWidget(self.name_label)
            self.v_layout.addLayout(self.h_layout)
            self.v_layout.addWidget(self.summary_label)
            self.v_layout.addWidget(self.summary_browser)

            self.setLayout(self.v_layout)   # 将大的布局实现

        else:
            self.resize(200, 200)
            self.no_find = QLabel("<h1>对不起, 没有找到相关电影!</h1>", self)
            self.h_layout = QHBoxLayout()
            self.h_layout.addWidget(self.no_find)
            self.setLayout(self.h_layout)

    def add_behaviour(self, user_id, movie_id, rating):
        # 存储用户行为
        rating = int(rating)
        f = open('../dataset/behaviours_new.csv', 'a+', encoding='utf-8')
        info = ',' + user_id + ',' + str(movie_id) + ',' + str(rating) + '\n'
        f.write(info)
        f.close()

    def whether_enable(self):
        # 判断按钮是否可点击
        if self.movie_id in self.movies_seen:
            self.one_button.setEnabled(False)
            self.two_button.setEnabled(False)
            self.three_button.setEnabled(False)
            self.four_button.setEnabled(False)
            self.five_button.setEnabled(False)

    def button_init(self):
        self.whether_enable()
        self.one_button.clicked.connect(lambda: self.add_behaviour(self.user_name, self.movie_id, int(self.one_button.text())))
        self.two_button.clicked.connect(lambda: self.add_behaviour(self.user_name, self.movie_id, int(self.two_button.text())))
        self.three_button.clicked.connect(lambda: self.add_behaviour(self.user_name, self.movie_id, int(self.three_button.text())))
        self.four_button.clicked.connect(lambda: self.add_behaviour(self.user_name, self.movie_id, int(self.four_button.text())))
        self.five_button.clicked.connect(lambda: self.add_behaviour(self.user_name, self.movie_id, int(self.five_button.text())))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    detailed = MovieDetailed("西虹市首富", 'doskevin407')
    detailed.show()
    sys.exit(app.exec_())
