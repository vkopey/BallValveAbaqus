# -*- coding: CP1251 -*-
from part import *
from material import *
from section import *
from optimization import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import * 

# from abaqus import *
# from abaqusConstants import * 
# from caeModules import *

def set_values(part,feature,par):
    '''
    Присвоює значення параметрам
    Приклад:
    par={'h1':0.0002,'h2':0.00004}
    set_values(part='Al',feature='Shell planar-1',par=par)
    '''
    p=model.parts[part] #деталь
    f=p.features[feature] #елемент
    s=model.ConstrainedSketch(name='__edit__', objectToCopy=f.sketch) #тимчасовий ескіз
    p.projectReferencesOntoSketch(filter=COPLANAR_EDGES, sketch=s, upToFeature=f) #спроектувати
    for k,v in par.iteritems(): #для всіх параметрів
        s.parameters[k].setValues(expression=str(v)) #установити значення
    f.setValues(sketch=s) #установити ескіз
    del s #знищити
    p.regenerate() #регенерувати деталь

def readODB_set2(set,step,var,pos=NODAL):
    '''Читає результати з останнього фрейму кроку на заданій множині
    (менш універсальна альтернатива readODB_set())
    set - множина
    step - крок
    var - змінна:
    ('S','Mises')
    ('S','Pressure')
    ('U','Magnitude')
    ('U','U1')
    ('CPRESS','')
    ('D','') #коефіцієнт запасу втомної міцності
    pos - позиція: NODAL - для вузлів,INTEGRATION_POINT - для елементів
    Приклад: readODB_set2(set='Cont',step='Step-1',var=('S','Mises'))
    '''
    if pos==NODAL:    
        s=odb.rootAssembly.nodeSets[set.upper()] #множина вузлів
    if pos==INTEGRATION_POINT:
        s=odb.rootAssembly.elementSets[set.upper()] #множина елементів
    fo=odb.steps[step].frames[-1].fieldOutputs[var[0]].getSubset(region=s,position=pos) #дані
    #openOdb(r'C:/Temp/Model-1.odb').steps['Step-1'].frames[4].fieldOutputs['CPRESS'].getSubset(position=NODAL, region=openOdb(r'C:/Temp/Model-1.odb').rootAssembly.nodeSets['CONT']).values[0].data
    res=[] #список результатів
    for v in fo.values: #для кожного вузла/елемента
        if var[1]=='Mises': res.append(v.mises)#додати до списку результатів
        if var[1]=='Pressure': res.append(v.press)
        if var[0]=='U' and var[1]=='Magnitude': res.append(v.magnitude)
        if var[1]=='U1': res.append(v.data.tolist()[0])
        if var[1]=='U2': res.append(v.data.tolist()[1])
        if var[0]=='CPRESS': res.append(v.data)
        if var[0]=='D': res.append(v.data)
        if var[0]=='PRESSURE': res.append(v.data)
    return res #повертае список значень

import pickleIPC,shutil,os
os.chdir('C:/Abaqus') # задати робочий каталог
openMdb(pathName='C:/Abaqus/testCFD.cae') # відкрити модель
model=mdb.models['Model-1'] # створити об'єкт моделі
h=pickleIPC.readTempFile() # прочитати дані, які передав сервер
# задати значення параметру 'h' та перебудувати геометрію
#!!!!!!!!!!!!!!!!!!!'Solid revolve-1'
set_values(part='Part-1',feature='Solid extrude-1',par={'h':h})
model.parts['Part-1'].generateMesh() # генерувати сітку елементів
mdb.jobs['Model-1'].submit() #виконати задачу
mdb.jobs['Model-1'].waitForCompletion() # чекати поки задача не буде розв'язана
# зберегти файл результатів .odb під унікальною назвою
shutil.copyfile(r'C:/Abaqus/Model-1.odb', r'C:/Abaqus/results_'+str(h)+'.odb')
odb=openOdb(r'C:/Abaqus/Model-1.odb') # відкрити базу даних результатів
results=readODB_set2(set='bot',step='Step-1',var=('PRESSURE','')) # отримати результати
pickleIPC.writeTempFile([h, sum(results)/len(results)]) # записати дані для передачі їх серверу
odb.close() # закрити базу даних результатів

