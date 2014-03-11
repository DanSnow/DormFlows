#!/usr/bin/env python3
# encoding: utf-8

import sys
import subprocess
import re

import netifaces

def getInterfaceList():
  return netifaces.interfaces()

def checkConnect(interface):
  if _doGetIP(interface) is None:
    return False
  else:
    return True

def getIP(interface):
  return _doGetIP(interface)

def getConnectUUID(interface):
  pipe = subprocess.Popen(['nmcli', 'c', 'status'], stdout = subprocess.PIPE)
  string = pipe.communicate()[0]
  lst = string.decode("utf-8").splitlines()
  res = re.split(r"\s\s+", lst[1])
  try:
    idx = res.index(interface)
    uuid = res[idx - 1]
    return uuid
  except ValueError:
    return None

def _doGetIP(interface):
  try:
    return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
  except KeyError:
    return None
