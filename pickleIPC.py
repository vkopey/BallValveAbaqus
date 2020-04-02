# -*- coding: CP1251 -*-
"""Бібліотека для IPC.
Містить функції, які дозволяють процесам обмінюватись об'єктами python
через сокети та тимчасові файли"""
import os, pickle, tempfile

def writeSocket(_socket, data):
    """Відсилає об'єкт python (data) через сокет"""
    f = _socket.makefile('wb') #,buffer_size # створити файл
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL) # законсервувати дані в файлі
    f.close() # закрити файл

def readSocket(_socket):
    """Повертає об'єкт python отриманий з сокета"""
    f = _socket.makefile('rb') #,buffer_size # створити файл
    data = pickle.load(f) # розконсервувати дані з файлу
    f.close() # закрити файл
    return data

def writeTempFile(data, tmpFileName="data4AbaqusScript.tmp"):
    """Записує об'єкт python (data) у тимчасовому файлі в тимчасовій папці""" 
    name=os.path.join(tempfile.gettempdir(),tmpFileName)
    f=open(name, "wb") #відкрити бінариний файл для запису
    pickle.dump(data,f) #законсервувати дані у файлі
    f.close() #закрити файл

def readTempFile(tmpFileName="data4AbaqusScript.tmp"):
    """Повертає об'єкт python шляхом читання тимчасового файлу у тимчасовій папці"""
    name=os.path.join(tempfile.gettempdir(),tmpFileName)
    f=open(name, "rb") #відкрити бінариний файл для читання
    data=pickle.load(f) #розконсервувати дані з файлу
    f.close() #закрити файл
    return data