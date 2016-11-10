'''
Created on May 10, 2016

@author: Jilin Liu
'''

import logging
import ast
from datamodel.amazoncar.mydatamodel import Car, AmazonInactiveCar, AmazonActiveCar, Vector3
from spacetime_local.IApplication import IApplication
from spacetime_local.declarations import Producer, GetterSetter

logger = logging.getLogger(__name__)
LOG_HEADER = "[TRAFFIC]"


@Producer(Car)
@GetterSetter(AmazonInactiveCar, AmazonActiveCar)
class AmazonTrafficSimulation(IApplication):
  '''
  classdocs
  '''

  frame = None
  ticks = 0
  TICKS_BETWEEN_CARDELIVERY = 10
  cars = []
  #nodes = [2600, 2610, 2620]
  #dict = {2600: [608.5, 592.875], 2610: [606.5, 600.1875], 2620: [599.0, 608.625]}
  nodesList = []
  numOfCars = 1
  nodeNum = 1

  def __init__(self, frame):
    '''
    Constructor
    '''
    self.frame = frame

  def initialize(self):
    logger.debug("%s Initializing", LOG_HEADER)
    for i in xrange(self.numOfCars):
      self.frame.add(Car())
    logger.debug("********** read route info ***********")
    f = open("applications/amazon_simulation/route/car-4.rd")
    for line in f.readlines():
      x, y = line.split(",") #x and y are string with \r\n, should convert to number
      coordinateList = [ast.literal_eval(x),ast.literal_eval(y)]
      #self.coordinateList.extend((x,y))
      self.nodesList.append(coordinateList)
    f.close()
    print self.nodesList
    # self.frame.add(Car("1d4883f3-b8f7-11e5-a78c-acbc327e1743")) # Valid uuid Example
    # self.frame.add(Car(10)) # Valid int Example
    # self.frame.add(Car("1d4883f3")) Invalid  Example - Crashes

    #self.cars = self.frame.get(Car)
    #print type(self.cars)
    #print type(self.cars[0])
    #print type(self.cars[0][0])
    #for car in self.cars:
      #car.becomeAmazonCar()
      #car.Aflag = True
      #car.Position(self.dict[self.nodes[0]][0], self.dict[self.nodes[0]][1], 0)


  def update(self):
    logger.info("%s Tick", LOG_HEADER)
    if self.ticks % self.TICKS_BETWEEN_CARDELIVERY == 0:
      try:
        inactivesA = self.frame.get(AmazonInactiveCar)
        logger.debug("%s ************** InactiveAmazonCars: %s", LOG_HEADER, len(inactivesA))
        logger.debug("%s ************** ActiveAmazonCars: %s", LOG_HEADER, self.numOfCars - len(inactivesA))
        if inactivesA != None and len(inactivesA) > 0:
          logger.debug("%s ************** Starting car %s", LOG_HEADER, inactivesA[0].ID)
          inactivesA[0].Position = Vector3(self.nodesList[0][0], self.nodesList[0][1], 0)
          inactivesA[0].start()
          print(inactivesA[0].ID, inactivesA[0].Position.X, inactivesA[0].Position.Y, inactivesA[0].Position.Z)

      except Exception:
        logger.exception("Error: ")

    print self.ticks
    for car in self.frame.get(AmazonActiveCar):
      if self.nodeNum < len(self.nodesList):
        if car.Position.X == self.nodesList[self.nodeNum][0] and car.Position.Y == self.nodesList[self.nodeNum][1]:
          logger.debug("Amazon car %s reached new node: %s, %s", car.ID, self.nodesList[self.nodeNum][0], self.nodesList[self.nodeNum][1])
          self.nodeNum = self.nodeNum + 1
        car.move(self.nodesList[self.nodeNum - 1], self.nodesList[self.nodeNum])
        print(car.ID, car.Position.X, car.Position.Y, car.Position.Z)
      else:
        logger.debug("car %s Reach destination", car.ID)
        exit(0)
    self.ticks += 1


  def shutdown(self):
    pass