#!/usr/bin/env python3
# encoding: utf-8

import math
from lxml import etree

class FlowsGetter():
  def __init__(self, ip):
    self.ip = ip
    self.rounded = False

  def setRound(self, r):
    self.rounded = r

  @property
  def flows(self):
    try:
      parser = etree.HTMLParser()
      tree = etree.parse("http://netflow.dorm.ccu.edu.tw/flows/{0}".format(self.ip), parser)
      res = tree.xpath("//*[@id=\"content\"]/h2/font")[0].text
      if self.rounded:
        return round(float(res))
      else:
        return math.ceil(float(res))
    except OSError:
      return None
