#!/usr/bin/env python
# encoding: utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SystemTrayIcon(QSystemTrayIcon):
  def __init__(self, icon, parent = None):
    super().__init__(icon, parent)
    self.createMenu()
    self.setContextMenu(self.menu)

  def createMenu(self):
    self.menu = QMenu()
    self.showAction = self.menu.addAction("&Show")
    self.setAction = self.menu.addAction("Settings")
    self.exitAction = self.menu.addAction("&Exit")
    # self.exitAction.triggered.connect(QApplication.quit)
