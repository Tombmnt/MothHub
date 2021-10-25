import sqlite3



class MothDB:
    def __init__(self):
        self.dbPath = "data.db"
        self.conn = sqlite3.connect(self.dbPath)
        self.cursor = self.conn.cursor()

        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS gps
                (   
                ID      INTEGER PRIMARY KEY     AUTOINCREMENT,
                TIME    INTEGER             ,
                DATE    INTEGER             ,
                LATT    REAL                ,
                LATD    TEXT                ,
                LONG    REAL                ,
                LOND    TEXT                ,
                SPDG    REAL                ,
                TAGL    REAL                ,
                HDIL    REAL                ,
                AMSL    REAL                ,
                HMSL    REAL                
                );''')
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS acc
                (
                ID      INTEGER PRIMARY KEY     AUTOINCREMENT,
                TIME    INTEGER             ,
                DATE    INTEGER             ,
                X       REAL                ,
                Y       REAL                ,
                Z       REAL                
                );''')
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS gyr
                (
                ID      INTEGER PRIMARY KEY     AUTOINCREMENT,
                TIME    INTEGER             ,
                DATE    INTEGER             ,
                PITCH   REAL                ,
                YAW     REAL                ,
                ROLL    REAL                
                );''')
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS tem
                (
                ID      INTEGER PRIMARY KEY     AUTOINCREMENT,
                TIME    INTEGER             ,
                DATE    INTEGER             ,
                TEMP    REAL                
                );''')
        self.conn.execute(
            '''CREATE TABLE IF NOT EXISTS win
                (
                ID      INTEGER PRIMARY KEY     AUTOINCREMENT,
                TIME    INTEGER             ,
                DATE    INTEGER             ,
                WSPD    REAL                ,
                WDIR    REAL                
                );
            ''')
        self.conn.commit()

    def __del__(self):
        print("closing Database.")
        self.conn.close()

    def addToDB(self, request):
        self.conn.execute(request)
        self.conn.commit()

    def addGPSData(self, gps):
        self.addToDB("INSERT INTO gps (TIME, DATE, LATT, LATD, LONG, LOND, SPDG, TAGL, HDIL, AMSL, HMSL) VALUES("+ \
            str(gps.time) + ", "+ \
            str(gps.date) + ", "+ \
            str(gps.latt) + ", \'"+ \
            str(gps.lattD) + "\', "+ \
            str(gps.longit) + ", \'"+ \
            str(gps.longD) + "\', "+ \
            str(gps.speedOG) + ", "+ \
            str(gps.trackAgl) + ", "+ \
            str(gps.hDilution) + ", "+ \
            str(gps.altMSL) + ", "+ \
            str(gps.hautMSL) +")" \
        )


    def addACCData(self, acc):
        self.addToDB("INSERT INTO acc (TIME, DATE, X, Y, Z) VALUES("+ \
            str(acc.time) + ", "+ \
            str(acc.date) + ", "+ \
            str(acc.x) + ", "+ \
            str(acc.y) + ", "+ \
            str(acc.z) + ")" \
        )

    def addGYRData(self, gyr):
        self.addToDB("INSERT INTO gyr (TIME, DATE, PITCH, YAW, ROLL) VALUES("+ \
            str(gyr.time) + ", "+ \
            str(gyr.date) + ", "+ \
            str(gyr.pitch) + ", "+ \
            str(gyr.yaw) + ", "+ \
            str(gyr.roll) + ")" \
        )
        
    def addTEMData(self, tem):
        self.addToDB("INSERT INTO tem (TIME, DATE, TEMP) VALUES("+ \
            str(tem.time) + ", "+ \
            str(tem.date) + ", "+ \
            str(tem.temp) + ")" \
        )
        
    def addWINData(self, win):
        self.addToDB("INSERT INTO win (TIME, DATE, WSPD, WDIR) VALUES("+ \
            str(win.time) + ", "+ \
            str(win.date) + ", "+ \
            str(win.speed) + ", "+ \
            str(win.direc) + ")" \
        )
        
mothDBSingle = MothDB()
