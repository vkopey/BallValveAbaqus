# -*- coding: CP1251 -*-
"""��������� ��� IPC.
̳����� �������, �� ���������� �������� ����������� ��'������ python
����� ������ �� �������� �����"""
import os, pickle, tempfile

def writeSocket(_socket, data):
    """³����� ��'��� python (data) ����� �����"""
    f = _socket.makefile('wb') #,buffer_size # �������� ����
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL) # �������������� ��� � ����
    f.close() # ������� ����

def readSocket(_socket):
    """������� ��'��� python ��������� � ������"""
    f = _socket.makefile('rb') #,buffer_size # �������� ����
    data = pickle.load(f) # ��������������� ��� � �����
    f.close() # ������� ����
    return data

def writeTempFile(data, tmpFileName="data4AbaqusScript.tmp"):
    """������ ��'��� python (data) � ����������� ���� � ��������� �����""" 
    name=os.path.join(tempfile.gettempdir(),tmpFileName)
    f=open(name, "wb") #������� �������� ���� ��� ������
    pickle.dump(data,f) #�������������� ��� � ����
    f.close() #������� ����

def readTempFile(tmpFileName="data4AbaqusScript.tmp"):
    """������� ��'��� python ������ ������� ����������� ����� � ��������� �����"""
    name=os.path.join(tempfile.gettempdir(),tmpFileName)
    f=open(name, "rb") #������� �������� ���� ��� �������
    data=pickle.load(f) #��������������� ��� � �����
    f.close() #������� ����
    return data