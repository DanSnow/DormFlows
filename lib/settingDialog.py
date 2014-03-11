#!/usr/bin/env python3
# encoding: utf-8

import sys

import netifaces

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import Config
import util

from settingDialog_ui import Ui_settingDia

class SettingDialog(QDialog):
  def __init__(self, parent = None):
    super().__init__(parent)
    self.ui = Ui_settingDia()
    self.ui.setupUi(self)
    self.ui.contentList.addItem("一般")
    self.ui.contentList.addItem("進階")
    self.ui.buttonBox.accepted.connect(self.applyAndExit)
    self.ui.buttonBox.rejected.connect(self.reject)
    self.validator = QIntValidator()
    self.validator.setBottom(0)
    self.ui.checkTimeLE.setValidator(self.validator)
    self.ui.notifyTimeLE.setValidator(self.validator)
    self.changeConfig = {}

  def setConfig(self, config):
    self.config = config
    if self.config["firstRun"]:
      self._defaultSetting()
    self.fillSetting()

  def _defaultSetting(self):
    self.config["checkDelay"] = 10000
    self.config["notifyShowTime"] = 5000
    self.config["interface"] = "eth0"
    self.config["disconnectCommand"] = "nmcli d disconnect iface %s --nowait"
    self.config["connectCommand"] = "nmcli c up %s --nowait"
    self.config["connectUuid"] = util.getConnectUUID("eth0")
    print(self.config["connectUuid"])

  def fillSetting(self):
    self.ui.checkTimeLE.setText(str(self.config["checkDelay"] // 1000))
    self.ui.notifyTimeLE.setText(str(self.config["notifyShowTime"] // 1000))
    interfaceList = util.getInterfaceList()
    self.ui.interfaceCB.addItems(interfaceList)
    idx = interfaceList.index(self.config["interface"])
    self.ui.interfaceCB.setCurrentIndex(idx)
    self.ui.disconnectCmdLE.setText(self.config["disconnectCommand"])
    self.ui.connectCmdLE.setText(self.config["connectCommand"])
    self.ui.connectUuidLE.setText(self.config["connectUuid"])

  @pyqtSlot()
  def applyAndExit(self):
    self.applySetting()
    self.accept()

  @pyqtSlot()
  def applySetting(self):
    self.config.update(self.changeConfig)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  dia = SettingDialog()
  c = Config()
  c["firstRun"] = True
  dia.setConfig(c)
  dia.show()
  app.exec_()
