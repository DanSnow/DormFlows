#!/usr/bin/env python3
# encoding: utf-8

import sys

import netifaces

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from dromflows_ui import Ui_DromFlows
from FlowsGetter import FlowsGetter
from SysTray import SystemTrayIcon
from config import Config


class DromFlows(QDialog):
  def __init__(self, parent = None):
    super().__init__(parent)
    self.ui = Ui_DromFlows()
    self.ui.setupUi(self)

    #init
    self.initInterfaceInfo()
    self.loadThemeIcon()
    self.limit = 0

    #init tray icon
    self.trayIcon = SystemTrayIcon(QIcon(":img/flow.png"))
    self.trayIcon.showAction.triggered.connect(self.show)
    self.trayIcon.exitAction.triggered.connect(self.accept)
    self.trayIcon.show()

    # init ui
    self.ui.imgL.setPixmap(self.okPic)
    self.ui.disL.setText("M時停用\"{0}\"".format(self.interface))
    self.ui.limitLE.setValidator(QIntValidator(0, 9999, self))

    # connect signal
    self.ui.disableChk.stateChanged.connect(self.checkStateChanged)
    self.ui.limitLE.editingFinished.connect(self.updateLimit)

    self.showIP()

  def checkStateChanged(self, stat):
    self.chkStat = True if stat == Qt.Checked else False

  def updateLimit(self):
    limit = self.ui.limitLE.text()
    if limit:
      try:
        self.limit = int(limit)
      except ValueError:
        self.ui.limitLE.clear()
        QMessageBox.information(self, "Error", "請輸入一些正常的東西 OK？")


  def initInterfaceInfo(self):
    self.interface = "eth0"
    self.interfacesList = netifaces.interfaces()

  def loadThemeIcon(self):
    self.okPic = QIcon.fromTheme("emblem-default").pixmap(150)
    self.urgentPic = QIcon.fromTheme("emblem-urgent").pixmap(150)
    self.deadPic = QIcon.fromTheme("emblem-noread").pixmap(150)

  def showFlows(self):
    flowsGetter = FlowsGetter(self.ip)
    flows = flowsGetter.flows
    if flows:
      self.ui.flowsL.setText("目前流量： {0} MB".format(flows))
      self.ui.flowsProg.setValue(flows)
      if not self.limit and self.chkStat:
        print("disable")
    else:
      self.ui.flowsL.setText("不明原因錯誤(有可能是IP位置錯了)")
      self.ui.imgL.setPixmap(self.deadPic)

  def showIP(self):
    try:
      self.ip = netifaces.ifaddresses(self.interface)[netifaces.AF_INET][0]['addr']
      self.ui.ipLE.setText(self.ip)
      self.showFlows()
      self.timer = QTimer()
      self.timer.timeout.connect(self.showFlows)
      self.timer.start(300000)
    except KeyError:
      self.ip = None
      self.ui.imgL.setPixmap(self.deadPic)
      self.ui.flowsL.setText("\"{0}\" isn't connect".format(self.interface))

  def closeEvent(self, e):
    if self.isVisible():
      self.hide()
    e.ignore()


if __name__ == "__main__":
  app = QApplication(sys.argv)
  dialog = DromFlows()
  dialog.show()
  app.exec_()
