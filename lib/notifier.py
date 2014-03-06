#!/usr/bin/env python3
# encoding: utf-8

import os
from datetime import datetime

import notify2

class Notifier:
  def __init__(self, timeout):
    self.flowPicUrl = "file://" + os.path.join(os.path.dirname(os.path.realpath(__file__)), "flow.png")
    notify2.init("DormFlows")
    self._notify = notify2.Notification("DormFlows", "", self.flowPicUrl)
    self._notify.timeout = timeout

  def notify(self, message):
    self._notify.update("DormFlows", message, self.flowPicUrl)
    self._notify.show()

if __name__ == '__main__':
  n = Notifier(5000)
  n.notify("Hello")
