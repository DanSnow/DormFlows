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

  def _checkIsNone(func):
    def warpper(self, *args, **kwargs):
      if self._config is not None:
        try:
          return func(self, *args, **kwargs)
        except KeyError:
          return None
    return warpper

  @_checkIsNone
  def __getitem__(self, name):
    return self._config[name]

  @_checkIsNone
  def __setitem__(self, name, value):
      self._config[name] = value

  @_checkIsNone
  def __delitem__(self, name):
      del self._config[name]

  def update(self, other):
    self._config.update(other)


