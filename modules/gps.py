#pip install pyserial

import serial

import timeUtil
from database import mothDBSingle as mothDB

class DataRMC:
    def __init__(self, time, date, status, latt, lattD, longit, longD, speedOG, trackAgl, magVar, magVarD):
        self.time = time
        self.date = date
        self.status = status
        self.latt = latt
        self.lattD = lattD
        self.longit = longit
        self.longD = longD
        self.speedOG = speedOG
        self.trackAgl = trackAgl
        self.magVar = magVar
        self.magVarD = magVarD

class DataGGA:
    def __init__(self, time, latt, lattD, longit, longD, fix, satNum, hDilution, altMSL, hautMSL):
        self.time = time
        self.latt = latt
        self.lattD = lattD
        self.longit = longit
        self.longD = longD
        self.fix = fix
        self.satNum = satNum
        self.hDilution = hDilution
        self.altMSL = altMSL
        self.hautMSL = hautMSL

class DataGPS:
    def __init__(self, time, date, latt, lattD, longit, longD, speedOG, trackAgl, hDilution, altMSL, hautMSL):
        self.time = time
        self.date = date
        self.latt = latt
        self.lattD = lattD
        self.longit = longit
        self.longD = longD
        self.speedOG = speedOG
        self.trackAgl = trackAgl
        self.hDilution = hDilution
        self.altMSL = altMSL
        self.hautMSL = hautMSL

class Nmea_GPS:

    def __init__(self, port):
        self.serPort = port
        self.pooling = True
        self.debug = False
        self.serCon = serial.Serial(self.serPort, 4800, timeout=5)    
        self.paquets = 0

    #This function will lock your software until self.pooling = False
    def poolData(self):
        while self.pooling:
            line = self.serCon.readline()
            splitline = line.decode().split(',')
            
            if self.debug:
                self.debugPrint(line)

            if (splitline[0] == "$GPGGA"):
                self.gga = self.extractGGA(line)
                self.paquets += 1

            elif (splitline[0] == "$GPRMC"):
                self.rmc = self.extractRMC(line)
                self.paquets += 1

            #agregating paquets to gps data
            if (self.paquets > 1):
                self.gps = self.extractGPS(self.gga, self.rmc)
                if self.debug:
                    print("--- paquet: ", self.gps.__dict__)
                self.paquets = 0
                self.writeDataToDB(self.gps)


    def extractGPS(self, gga, rmc):
        return DataGPS(gga.time, rmc.date, gga.latt, gga.lattD, gga.longit, gga.longD, rmc.speedOG, rmc.trackAgl, gga.hDilution, gga.altMSL, gga.hautMSL)

    def extractRMC(self, line):
        #time = line[1], date = line[9]
        return DataRMC(timeUtil.getTimeNowAsNMEA(), timeUtil.getDateNowAsNMEA(), line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[10], line[11])

    def extractGGA(self, line):
        #time = line[1]
        return DataGGA(timeUtil.getTimeNowAsNMEA(), line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[11])
        
    def writeDataToDB(self, gpsData):
        mothDB.addGPSData(gpsData)

    def debugPrint(self, line):
        print(line)

        #f = open("../debugGPSData.txt", "a+")
        #f.write(line)
        #f.close()
