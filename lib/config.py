#!/usr/bin/env python3
# encoding: utf-8

import yaml

class Config(object):
  """a hash like config"""

  def __init__(self, fileName = None):
    """Initialize config it can assign a file name to load

    :fileName: file name to load

    """
    self._config = {}
    self.load(fileName)


  def load(self, fileName):
    self._fileName = fileName
    if self._fileName is not None:
      try:
        with open(self._fileName) as f:
          self._config = yaml.load(f)
      except EnvironmentError as e:
        print(e)

  def save(self, fileName):
    """save the config

    :fileName: file name to save
    :returns: None

    """
    if self._config is None: return
    try:
      with open(fileName, "w") as f:
        f.write(yaml.dump(self._config))
    except EnvironmentError as e:
      print(e)

  def __getitem__(self, name):
    if self._config is not None:
      return self._config[name]

  def __setitem__(self, name, value):
    if self._config is not None:
      self._config[name] = value

  def __delitem__(self, name):
    if self._config is not None:
      del self._config[name]

