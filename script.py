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
    �������� �������� ����������
    �������:
    par={'h1':0.0002,'h2':0.00004}
    set_values(part='Al',feature='Shell planar-1',par=par)
    '''
    p=model.parts[part] #������
    f=p.features[feature] #�������
    s=model.ConstrainedSketch(name='__edit__', objectToCopy=f.sketch) #���������� ����
    p.projectReferencesOntoSketch(filter=COPLANAR_EDGES, sketch=s, upToFeature=f) #������������
    for k,v in par.iteritems(): #��� ��� ���������
        s.parameters[k].setValues(expression=str(v)) #���������� ��������
    f.setValues(sketch=s) #���������� ����
    del s #�������
    p.regenerate() #������������ ������

def readODB_set2(set,step,var,pos=NODAL):
    '''���� ���������� � ���������� ������ ����� �� ������ ������
    (���� ����������� ������������ readODB_set())
    set - �������
    step - ����
    var - �����:
    ('S','Mises')
    ('S','Pressure')
    ('U','Magnitude')
    ('U','U1')
    ('CPRESS','')
    ('D','') #���������� ������ ������ ������
    pos - �������: NODAL - ��� �����,INTEGRATION_POINT - ��� ��������
    �������: readODB_set2(set='Cont',step='Step-1',var=('S','Mises'))
    '''
    if pos==NODAL:    
        s=odb.rootAssembly.nodeSets[set.upper()] #������� �����
    if pos==INTEGRATION_POINT:
        s=odb.rootAssembly.elementSets[set.upper()] #������� ��������
    fo=odb.steps[step].frames[-1].fieldOutputs[var[0]].getSubset(region=s,position=pos) #���
    #openOdb(r'C:/Temp/Model-1.odb').steps['Step-1'].frames[4].fieldOutputs['CPRESS'].getSubset(position=NODAL, region=openOdb(r'C:/Temp/Model-1.odb').rootAssembly.nodeSets['CONT']).values[0].data
    res=[] #������ ����������
    for v in fo.values: #��� ������� �����/��������
        if var[1]=='Mises': res.append(v.mises)#������ �� ������ ����������
        if var[1]=='Pressure': res.append(v.press)
        if var[0]=='U' and var[1]=='Magnitude': res.append(v.magnitude)
        if var[1]=='U1': res.append(v.data.tolist()[0])
        if var[1]=='U2': res.append(v.data.tolist()[1])
        if var[0]=='CPRESS': res.append(v.data)
        if var[0]=='D': res.append(v.data)
        if var[0]=='PRESSURE': res.append(v.data)
    return res #�������� ������ �������

import pickleIPC,shutil,os
os.chdir('C:/Abaqus') # ������ ������� �������
openMdb(pathName='C:/Abaqus/testCFD.cae') # ������� ������
model=mdb.models['Model-1'] # �������� ��'��� �����
h=pickleIPC.readTempFile() # ��������� ���, �� ������� ������
# ������ �������� ��������� 'h' �� ������������ ��������
#!!!!!!!!!!!!!!!!!!!'Solid revolve-1'
set_values(part='Part-1',feature='Solid extrude-1',par={'h':h})
model.parts['Part-1'].generateMesh() # ���������� ���� ��������
mdb.jobs['Model-1'].submit() #�������� ������
mdb.jobs['Model-1'].waitForCompletion() # ������ ���� ������ �� ���� ����'�����
# �������� ���� ���������� .odb �� ��������� ������
shutil.copyfile(r'C:/Abaqus/Model-1.odb', r'C:/Abaqus/results_'+str(h)+'.odb')
odb=openOdb(r'C:/Abaqus/Model-1.odb') # ������� ���� ����� ����������
results=readODB_set2(set='bot',step='Step-1',var=('PRESSURE','')) # �������� ����������
pickleIPC.writeTempFile([h, sum(results)/len(results)]) # �������� ��� ��� �������� �� �������
odb.close() # ������� ���� ����� ����������

