'''
Created on 31 Dec 2017

@author: Joerg Weingrill <jweingrill@gmail.com>
'''
import ephem
import datetime
import numpy as np

class ObservationCalender(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.dates = []
        self.sunrises = []
        self.sunsets = []
        
        self.moon = []
        self.potsdam = ephem.Observer()
        self.potsdam.date = datetime.datetime.today() #'2018/01/01 00:00:00' 
        self.potsdam.lat = '52.405032' #52.405032, 13.104349
        self.potsdam.lon = '13.104349'
    
    def calcdates(self):
        date = datetime.datetime(2018,1,1,0,0,0)
        for _ in range(365):
            self.dates.append(date)
            date = date + datetime.timedelta(days=1)
            
        
    
    def calcSun(self):    
        
        self.potsdam.horizon =  '30:00'#'-0:34'
        
        sun = ephem.Sun(self.potsdam)  # @UndefinedVariable
        
        #set astronomical dawn
        #potsdam.horizon = '-19:00'
        for date in self.dates:
            self.potsdam.date = str(date)
            sunrisetime = None
            sunsettime = None
            try:
                sunrise = self.potsdam.next_rising(sun)
            except ephem.NeverUpError:
                self.sunrises.append(np.NaN)
                sunrisetime = ''
            else:
                sunrisetime = sunrise.datetime()
                self.sunrises.append(sunrisetime)
                    
            try:
                sunset = self.potsdam.next_setting(sun)
            except ephem.NeverUpError:
                self.sunsets.append(np.NaN)
                sunsettime = ''
            else:
                sunsettime = sunset.datetime()
                self.sunsets.append(sunsettime)
            
            print str(date), sunrisetime, sunsettime

    def calcMoon(self):    
        
        self.potsdam.horizon =  '30:00'#'-0:34'
        
        moon = ephem.Moon(potsdam)  # @UndefinedVariable
        
        #set astronomical dawn
        #potsdam.horizon = '-19:00'
        for _ in range(365):
            try:
                moonrise = self.potsdam.next_rising(moon, start=self.potsdam.date)
            except ephem.NeverUpError:
                moonrisetime = 'never rises'
                self.potsdam.date = self.potsdam.date.datetime() + datetime.timedelta(days=1)
                continue
            else:
                moonrisetime = moonrise.datetime()
                    
            try:
                moonset = self.potsdam.next_setting(moon, start=moonrise)
            except ephem.NeverUpError:
                moonsettime = 'never sets'
            else:
                moonsettime = moonset.datetime()
                self.potsdam.date = moonset
            
            print str(self.potsdam.date), moonrisetime, moonsettime
            self.moon.append((moonrisetime,moonsettime))
        
    def calcMars(self):
        
        self.potsdam.horizon =  '00:00'#'-0:34'
        
        mars = ephem.Mars(self.potsdam)  # @UndefinedVariable
        
        #set astronomical dawn
        #potsdam.horizon = '-19:00'
        for _ in range(365):
            try:
                marsrise = self.potsdam.next_rising(mars, start=self.potsdam.date)
            except ephem.NeverUpError:
                marsrisetime = 'never rises'
                self.potsdam.date = self.potsdam.date.datetime() + datetime.timedelta(days=1)
                continue
            else:
                marsrisetime = marsrise.datetime()
            
            
            transit = self.potsdam.next_transit(mars, start=self.potsdam.date) 
            self.potsdam.date = transit
            alt = mars.alt       
            try:
                marsset = self.potsdam.next_setting(mars, start=marsrise)
            except ephem.NeverUpError:
                marssettime = 'never sets'
            else:
                marssettime = marsset.datetime()
                self.potsdam.date = marsset
            
            print str(self.potsdam.date), marsrisetime, marssettime, mars.size, alt
            #self.moon.append((marsrisetime, marssettime))
        
        
if __name__ == '__main__':
    oc = ObservationCalender()
    oc.calcdates()
    oc.calcMars()
