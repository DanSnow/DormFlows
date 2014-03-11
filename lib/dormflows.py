#!/usr/bin/env python3
# encoding: utf-8

import sys
import os
import subprocess
from datetime import datetime

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import util
from dormflows_ui import Ui_DormFlows
from FlowsGetter import FlowsGetter
from SysTray import SystemTrayIcon
from config import Config
from notifier import Notifier


class NotifyFlow:
  NotifyFlows = [7000, 7500, 8000, 8300]
  def __init__(self):
    self.flowIter = iter(self.NotifyFlows)
    self.notifyFlows = next(self.flowIter)
    self.notifier = Notifier()
    self.needUpdate = True

  def checkAndNotify(self, flow):
    if datetime.now().hour == 0 and self.needUpdate:
      self.flowIter = iter(self.NotifyFlows)
      self.needUpdate = False
      self._nextFlow()
    else:
      self.needUpdate = True
    if flow > self.notifyFlows:
      self.notifier.notify("Notice: Now flow is {0}".format(flow))
      self._nextFlow()

  def _nextFlow(self):
    try:
      self.notifyFlows = next(self.flowIter)
    except StopIteration:
      pass

class DromFlows(QDialog):
  def __init__(self, parent = None):
    super().__init__(parent)
    self.ui = Ui_DormFlows()
    self.ui.setupUi(self)

    #init
    self.initInterfaceInfo()
    self.loadThemeIcon()
    self.limit = 0
    self.chkStat = False
    self._config = Config(os.path.join(os.environ["HOME"], ".dormflows"))
    if self._config["firstRun"] is None:
      self._defaultSetting()

    #init tray icon
    self.trayIcon = SystemTrayIcon(QIcon(":img/flow.png"))
    self.trayIcon.showAction.triggered.connect(self.show)
    self.trayIcon.exitAction.triggered.connect(self._appExit)
    self.trayIcon.show()

    #init notifier
    self.notify = NotifyFlow()

    # init ui
    self.ui.imgL.setPixmap(self.okPic)
    self.ui.disL.setText("M時停用\"{0}\"".format(self._config["interface"]))
    self.ui.limitLE.setValidator(QIntValidator(0, 9999, self))

    # connect signal
    self.ui.disableChk.stateChanged.connect(self.checkStateChanged)
    self.ui.limitLE.editingFinished.connect(self.updateLimit)

    self.showIP()

  @pyqtSlot(int)
  def checkStateChanged(self, stat):
    self.chkStat = True if stat == Qt.Checked else False
    self._disableInterface()

  @pyqtSlot()
  def updateLimit(self):
    limit = self.ui.limitLE.text()
    if limit:
      try:
        self.limit = int(limit)
      except ValueError:
        self.ui.limitLE.clear()
        QMessageBox.information(self, "Error", "請輸入一些正常的東西 OK？")
    self._disableInterface()


  def initInterfaceInfo(self):
    self.interface = "eth0"

  def loadThemeIcon(self):
    self.okPic = QIcon.fromTheme("emblem-default").pixmap(150)
    self.urgentPic = QIcon.fromTheme("emblem-urgent").pixmap(150)
    self.deadPic = QIcon.fromTheme("emblem-noread").pixmap(150)

  def showFlows(self):
    flowsGetter = FlowsGetter(self.ip)
    self.flows = flowsGetter.flows
    if self.flows is not None:
      self.ui.flowsL.setText("目前流量： {0} MB".format(self.flows))
      self.ui.flowsProg.setValue(self.flows)
      self.notify.checkAndNotify(self.flows)
      if self.flows > 7000:
        self.ui.imgL.setPixmap(self.urgentPic)
      else:
        self.ui.imgL.setPixmap(self.okPic)
      self._disableInterface()
    else:
      if util.checkConnect(self._config["interface"]):
        self.ui.flowsL.setText("\"{0}\" isn't connect".format(self._config["interface"]))
      else:
        self.ui.flowsL.setText("不明原因錯誤(有可能是IP位置錯了)")
      self.ui.imgL.setPixmap(self.deadPic)

  def showIP(self):
    if util.checkConnect(self._config["interface"]):
      self.ip = util.getIP(self._config["interface"])
      self.ui.ipLE.setText(self.ip)
      self.showFlows()
      self.timer = QTimer()
      self.timer.timeout.connect(self.showFlows)
      self.timer.start(self._config["checkDelay"])
    else:
      self.ip = None
      self.ui.imgL.setPixmap(self.deadPic)
      self.ui.flowsL.setText("\"{0}\" isn't connect".format(self._config["interface"]))

  def _disableInterface(self):
    if self.limit and self.chkStat:
      if self.flows > self.limit:
        subprocess.call(["nmcli", "d", "disconnect", "iface", self._config["interface"], "--nowait"], shell = False)

  def _appExit(self):
    """call when application exit
    :returns: None

    """
    self.hide()
    if self._config["firstRun"]:
      self._config["firstRun"] = False
    self._saveSetting()
    self.accept()

  def _defaultSetting(self):
    self._config["firstRun"] = True
    self._config["interface"] = "eth0"
    self._config["checkDelay"] = 10000

  def _saveSetting(self):
    """Save the setting
    :returns: None

    """
    self._config.save(os.path.join(os.environ["HOME"], ".dormflows"))

  def closeEvent(self, e):
    if self.isVisible():
      self.hide()
    e.ignore()


if __name__ == "__main__":
  app = QApplication(sys.argv)
  dialog = DromFlows()
  dialog.show()
  app.exec_()
