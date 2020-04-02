# -*- coding: CP1251 -*-
import csv,pickleIPC,subprocess,datetime

csv_file=open("results.csv", "wb") # CSV файл результатів
writer = csv.writer(csv_file,delimiter = ';') # об'єкт для запису у файл CSV
for h in [0.04,0.05]: # для значень h у списку
    pickleIPC.writeTempFile(h) # записати дані в тимчасовий файл для передачі їх скрипту
    print datetime.datetime.now().isoformat() # час початку
    
    print "Abaqus CAE started. Please wait"
    # виконує скрипт в Abaqus та чекає завершення
    AbaqusPath=r"d:\SIMULIA\Abaqus\6.12-3\code\bin\abq6123.exe"
    subprocess.Popen(AbaqusPath+' cae noGUI=script.py').communicate()    
    print datetime.datetime.now().isoformat() # час завершення
    print "Abaqus CAE finished"
    
    data=pickleIPC.readTempFile() # прочитати дані, які повернув скрипт
    writer.writerow(data) # записати у файл CSV
    csv_file.flush() # очистити буфер
csv_file.close() # закрити файл CSV
