#!/usr/bin/env python3
# encoding: utf-8

import sys

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

def _doGetIP(interface):
  try:
    return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
  except KeyError:
    return None
