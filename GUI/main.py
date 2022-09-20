#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication

from Login import Login

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Login = Login()
    Login.show()
    sys.exit(app.exec_())