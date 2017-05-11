import serial
from datetime import datetime
import mysql.connector

MAX_COUNT = 10
ser = serial.Serial('COM14', 9600)
count = 0
sumOfData = [0.0, 0.0, 0.0, 0, 0.0]
meanval = []
con = mysql.connector.connect(user="roma",
                              password="2424sdsd",
                              host="127.0.0.1",
                              database="projectdb",
                              port='3306')
cur = con.cursor()
querry = "INSERT INTO sensor_data (hum, temp1, temp2, pres, dust, send_time)\
        VALUES (%s, %s, %s, %s, %s, %s)"
while True:
    if (ser.inWaiting()>0):
        mydata = ser.readline()
        mydata = mydata.rstrip("\r\n")
        mydata = mydata.split(";")
        mydata = [float(mydata[0]), float(mydata[1]), float(mydata[2]), int(mydata[3]), float(mydata[4])]
        sumOfData = map(lambda x, y: x + y, sumOfData, mydata)
        count += 1
        if count == MAX_COUNT:
            meanval = map(lambda x: round(x/count, 3) if type(x) == float else x/count, sumOfData)
            count = 0
            sumOfData = [0] * 5
            data = meanval + [datetime.now()]
            print data
            cur.execute(querry,data)
            con.commit()
