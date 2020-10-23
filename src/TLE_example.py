# small program for getting a state at epoch from TLEs 
#
#
# author: Carolin Frueh
# date: 06/11/2020
# dependencies: sgp4 module, no subroutines
#
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
from sgp4.propagation import sgp4
from sgp4.ext import jday


### INPUTS
# TLE file
tlefile='tle_sample.txt'
linespertle=3 # lines per object of the TLE file, either two or three

# define desired reference epoch UTC
year=2020 
month=6
day=10
hour=1
minute=3
second=0.45
jd_epoch=jday(year, month, day, hour, minute, second) # julianian date

###



# setup for reading TLE file all at once
tles = open(tlefile, 'r')
tlelines = tles.readlines()
nolines=len(tlelines)
tles.close()
satrec=[]
    
# generate satrec, here one for all, but can also do one at a time (satrec1)
startline=linespertle-2
for i in range(startline,nolines,linespertle):
    # create satellite object
    satrec1=twoline2rv(tlelines[i], tlelines[i+1], wgs84)
    # append until all objects are read in
    satrec.append(satrec1)
print(satrec)
# obtain position and velocity at reference epoch
minday=1440.0 #minutes per day, input in minutes needed (see sgp4)        
posvel = [sgp4(n,(jd_epoch - n.jdsatepoch) * minday) for n in satrec]    # state in km and km/s
    
nobj=len(posvel) # how many objects    
r=[posvel[i][0] for i in range(nobj)] # position at epoch in km
v=[posvel[i][1] for i in range(nobj)] # velocity at epoch in km/s

print(r)
print(v)

# those are the position and velocity at the epoch you have defined, for multiple epochs you can make a vector or a for loop
# which then give you the full orbit
    
   