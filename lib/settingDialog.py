#!/usr/bin/env python3
# encoding: utf-8

import sys

import netifaces

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import Config

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
  dia.show()
  app.exec_()
