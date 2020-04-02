# -*- coding: CP1251 -*-
import csv,pickleIPC,subprocess,datetime

csv_file=open("results.csv", "wb") # CSV ���� ����������
writer = csv.writer(csv_file,delimiter = ';') # ��'��� ��� ������ � ���� CSV
for h in [0.04,0.05]: # ��� ������� h � ������
    pickleIPC.writeTempFile(h) # �������� ��� � ���������� ���� ��� �������� �� �������
    print datetime.datetime.now().isoformat() # ��� �������
    
    print "Abaqus CAE started. Please wait"
    # ������ ������ � Abaqus �� ���� ����������
    AbaqusPath=r"d:\SIMULIA\Abaqus\6.12-3\code\bin\abq6123.exe"
    subprocess.Popen(AbaqusPath+' cae noGUI=script.py').communicate()    
    print datetime.datetime.now().isoformat() # ��� ����������
    print "Abaqus CAE finished"
    
    data=pickleIPC.readTempFile() # ��������� ���, �� �������� ������
    writer.writerow(data) # �������� � ���� CSV
    csv_file.flush() # �������� �����
csv_file.close() # ������� ���� CSV
