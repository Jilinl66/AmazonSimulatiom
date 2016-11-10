#!/usr/bin/python
'''
Created on May 10, 2016

@author: Jilin Liu
'''

import logging
import logging.handlers
import os
import sys

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "../..")))

from spacetime_local.frame import frame
from applications.amazon_simulation.amazonTrafficsim import AmazonTrafficSimulation


logger = None

class Simulation(object):
  '''
  classdocs
  '''
  def __init__(self):
    '''
    Constructor
    '''
    frame_car = frame(time_step = 1000)
    frame_car.attach_app(AmazonTrafficSimulation(frame_car))
        
    frame_car.run()

def SetupLoggers():
  global logger
  logger = logging.getLogger()
  logging.info("testing before")
  logger.setLevel(logging.DEBUG)

  #logfile = os.path.join(os.path.dirname(__file__), "../../logs/CADIS.log")
  #flog = logging.handlers.RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=50, mode='w')
  #flog.setFormatter(logging.Formatter('%(levelname)s [%(name)s] %(message)s'))
  #logger.addHandler(flog)
  logging.getLogger("requests").setLevel(logging.WARNING)
  clog = logging.StreamHandler()
  clog.addFilter(logging.Filter(name='CADIS'))
  clog.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
  clog.setLevel(logging.DEBUG)
  logger.addHandler(clog)

if __name__== "__main__":
  SetupLoggers()
  sim = Simulation()
