'''
Created on 27 Nov 2017

@author: jwe
'''

class PotsdamSun(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.dates = []
        self.sunrises = []
        self.middays = []
        self.sunsets = []
        self.daylengths = []
        

    def calctime(self):    
        import ephem
        import datetime
        import numpy as np
        
        potsdam = ephem.Observer()
        
        potsdam.date = '2017/01/01 00:00:00' 
        potsdam.lat = '52.405032' #52.405032, 13.104349
        potsdam.lon = '13.104349'
        #potsdam.lat = '-24:35:53'
        #potsdam.lon = '-70:11:47'
        
        potsdam.horizon =  '30:00'#'-0:34'
        
        sun = ephem.Sun(potsdam)  # @UndefinedVariable
        
        #set astronomical dawn
        #potsdam.horizon = '-19:00'
        for _ in range(365):
            try:
                sunrise = potsdam.next_rising(sun)
            except ephem.NeverUpError:
                self.sunrises.append(np.NaN)
                potsdam.date = 0 #TODO: date plus 1 day
            else:
                sunrisetime = datetime.datetime.replace(sunrise.datetime(), year=2017, month=01, day=01)
                self.sunrises.append(sunrisetime)
                    
            potsdam.date = str(sunrise)
            midday = potsdam.next_transit(sun)
            potsdam.date = str(midday) 
            sunset =  potsdam.next_setting(sun)
            potsdam.date = str(sunset)
            
            date = datetime.datetime.date(sunrise.datetime())
            self.dates.append(date)
            
            
            middaytime = datetime.datetime.replace(midday.datetime(), year=2017, month=01, day=01)
            self.middays.append(middaytime)
            
            sunsettime = datetime.datetime.replace(sunset.datetime(), year=2017, month=01, day=01)
            self.sunsets.append(sunsettime)
            
            #self.daylengths.append(sunset.datetime()-sunrise.datetime())
            #print date, sunrisetime , sunset
        assert(len(self.dates)==len(self.sunrises))
        print max([datetime.datetime.time(sr) for sr in self.sunrises])
        print min([datetime.datetime.time(st) for st in self.sunsets])
        #print max(self.sunsets)

    def plot(self):
        from matplotlib import pyplot
        #print self.dates
        pyplot.plot(self.dates, self.sunrises)
        pyplot.plot(self.dates, self.middays, linestyle = '--')
        pyplot.plot(self.dates, self.sunsets)
        pyplot.show()

if __name__ == '__main__':
    ps = PotsdamSun()
    ps.calctime()
    ps.plot()