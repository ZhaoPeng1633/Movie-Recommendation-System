#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import re
import sys
import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit,QHBoxLayout

from new_user_window import NewMainWindow


class NewUser(QWidget):
    def __init__(self, user, password):
        super(NewUser, self).__init__()  # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("电影推荐系统")
        self.setWindowIcon(QIcon('../movie.jpg'))  # 设置窗口图标
        self.resize(400, 400)
        self.user = user
        self.password = password
        self.movies_df = pd.read_csv('../dataset/new_movies.csv', encoding='utf-8')
        self.movies_df = self.movies_df.iloc[:, [0, 1, 2, 5, 6, 9, 10, 12]]

        self.movies_df = self.movies_df.rename(columns={'Unnamed: 0': 'Movie_ID'})

        self.movies_df['genres'] = self.movies_df['genres'].fillna('0')  # 缺失值填充

        self.new_user_label1 = QLabel("<h2>由于您是新用户</h2>")
        self.new_user_label2 = QLabel("<h2>我们在此诚挚地询问您喜欢的电影类型,以便我们更好地向您推荐电影:</h2>")
        self.new_user_label3 = QLabel("<h3>请选择一项您感兴趣的电影类型</h3>")

        self.label1 = QPushButton("剧情", self)
        self.label2 = QPushButton("动作", self)
        self.label3 = QPushButton("喜剧", self)
        self.label4 = QPushButton("科幻", self)
        self.label5 = QPushButton("悬疑", self)
        self.label6 = QPushButton("爱情", self)
        self.label7 = QPushButton("惊悚", self)
        self.label8 = QPushButton("动画", self)
        self.label9 = QPushButton("犯罪", self)
        self.label10 = QPushButton("奇幻", self)

        self.v_layout = QVBoxLayout()
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()

        self.h1_layout.addWidget(self.label1)
        self.h1_layout.addWidget(self.label2)
        self.h1_layout.addWidget(self.label3)
        self.h1_layout.addWidget(self.label4)
        self.h1_layout.addWidget(self.label5)

        self.h2_layout.addWidget(self.label6)
        self.h2_layout.addWidget(self.label7)
        self.h2_layout.addWidget(self.label8)
        self.h2_layout.addWidget(self.label9)
        self.h2_layout.addWidget(self.label10)

        self.v_layout.addWidget(self.new_user_label1)
        self.v_layout.addWidget(self.new_user_label2)
        self.v_layout.addWidget(self.new_user_label3)
        self.v_layout.addLayout(self.h1_layout)
        self.v_layout.addLayout(self.h2_layout)

        self.setLayout(self.v_layout)

        self.label1.clicked.connect(lambda: self.submit_like("剧情"))
        self.label2.clicked.connect(lambda: self.submit_like("动作"))
        self.label3.clicked.connect(lambda: self.submit_like("喜剧"))
        self.label4.clicked.connect(lambda: self.submit_like("科幻"))
        self.label5.clicked.connect(lambda: self.submit_like("悬疑"))
        self.label6.clicked.connect(lambda: self.submit_like("爱情"))
        self.label7.clicked.connect(lambda: self.submit_like("惊悚"))
        self.label8.clicked.connect(lambda: self.submit_like("动画"))
        self.label9.clicked.connect(lambda: self.submit_like("犯罪"))
        self.label10.clicked.connect(lambda: self.submit_like("奇幻"))

    def submit_like(self, genre):
        with open('../dataset/new_user_info.csv', 'a+', encoding='utf-8') as f:
            info = self.user + ',' + self.password + ','+ genre +'\n'
            f.write(info)
        f.close()
        self.new_user_like = self.movies_df[self.movies_df['genres'].str.contains(genre)]
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
        self.new_user_rec_movies = self.new_user_rec_movies[:15]
        print(self.new_user_rec_movies)
        self.new = NewMainWindow(self.new_user_rec_movies, self.user, genre)
        self.new.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    new = NewUser("caiyifan", '123456')
    new.show()
    sys.exit(app.exec_())
