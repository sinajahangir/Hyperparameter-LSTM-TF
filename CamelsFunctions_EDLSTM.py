# -*- coding: utf-8 -*-
"""
Sample code for pre-processing Daymet data
"""


#%%
#import necessary libraries
from pandas import read_csv
import numpy as np
#importing plot functions
import matplotlib.pyplot as plt
import pandas as pd
import csv
#%%
def read_camels_met(id_basin):
    reader = csv.reader(open("%s_lump_cida_forcing_leap.txt"%(id_basin)), delimiter="\t")
    data=[]
    for row in reader:
        data.append(row)
    frame=np.asarray(pd.DataFrame(data[4:]))
    date=data[4][0].split(' ')
    area=int(data[2][0])
    year=int(date[0])
    month=int(date[1])
    day=int(date[2])
    array=frame[:,2:].astype('float')
    return [day,month,year],area,array
#%%
def write_camels_met(array_data,date_list,iid,delete_var=None,write_csv=True):
    new_array=np.copy(array_data)
    met_vars_all=['pr mm/d','srad w/m2','swe','tmax c','tmin c','vp pa']
    #axis 1 for column
    if delete_var!=None:
        array=np.delete(new_array,delete_var,1)
        met_vars_all.pop(delete_var)
    else:
        array=new_array
    met_vars=met_vars_all
    dati=pd.date_range(start=r'%d-%d-%d'%(date_list[2],date_list[1],date_list[0]),\
        periods=len(array),normalize=True)
    df_data=pd.DataFrame(array,index=dati,columns=met_vars)
    if write_csv==True:
        df_data.to_csv('%s_CAMELS_metData.csv'%(iid))
    return df_data,array
#%%
def read_camels_q(iid):
    reader = csv.reader(open("%s_streamflow_qc.txt"%(iid)), delimiter="\t")
    data=[]
    for row in reader:
        data.append(row[0].split(' '))
    q=np.zeros(len(data))
    for ii in range(0,len(data)):
        q[ii]=float(data[ii][-2])
    year=int(data[0][1])
    month=int(data[0][2])
    day=int(data[0][3])
    return [day,month,year],q.reshape((-1,1))
#%%
def write_camels_q(array_q,date_list,iid,write_csv=True):
    new_array=np.copy(array_q)
    met_vars_all=['Q m3/sec']
    array=new_array
    dati=pd.date_range(start=r'%d-%d-%d'%(date_list[2],date_list[1],date_list[0]),\
        periods=len(array),normalize=True)
    df_data=pd.DataFrame(array,index=dati,columns=met_vars_all)
    if write_csv==True:
        df_data.to_csv('%s_CAMELS_Q.csv'%(iid))
    return df_data,array
#%%
def split_sequence_forecast(sequence_x,sequence_y, n_steps_in, n_steps_out,mode='seq'):
    X, y = list(), list()
    k=0
    sequence_x=np.copy(np.asarray(sequence_x))
    sequence_y=np.copy(np.asarray(sequence_y))
    for _ in range(len(sequence_x)):
		# find the end of this pattern
        end_ix = k + n_steps_in
        out_end_ix = end_ix + n_steps_out
		# check if we are beyond the sequence
        if out_end_ix > len(sequence_x):
            break
		# gather input and output parts of the pattern
        seq_x = sequence_x[k:end_ix]
        #mode single is used for one output
        if n_steps_out==0:
            seq_y= sequence_y[end_ix-1:out_end_ix]
        elif mode=='single':
            seq_y= sequence_y[out_end_ix-1]
        else:
            seq_y= sequence_y[end_ix:out_end_ix]
        X.append(seq_x)
        y.append(seq_y.flatten())
        if n_steps_out==0:
            k=k+1
        else:
            k=k+n_steps_out
    XX,YY= np.asarray(X), np.asarray(y)
    if (n_steps_out==0 or n_steps_out==1):
        YY=YY.reshape((len(XX),1))
    return XX,YY
#%%
def split_sequence_multi_train(sequence_x,sequence_y, n_steps_in, n_steps_out,mode='seq'):
    X, y = list(), list()
    k=0
    sequence_x=np.copy(np.asarray(sequence_x))
    sequence_y=np.copy(np.asarray(sequence_y))
    for _ in range(len(sequence_x)):
		# find the end of this pattern
        end_ix = k + n_steps_in
        out_end_ix = end_ix + n_steps_out
		# check if we are beyond the sequence
        if out_end_ix > len(sequence_x):
            break
		# gather input and output parts of the pattern
        seq_x = sequence_x[k:end_ix]
        #mode single is used for one output
        if n_steps_out==0:
            seq_y= sequence_y[end_ix-1:out_end_ix]
        elif mode=='single':
            seq_y= sequence_y[out_end_ix-1]
        else:
            seq_y= sequence_y[end_ix:out_end_ix]
        X.append(seq_x)
        y.append(seq_y.flatten())
        k=k+1
    
    XX,YY= np.asarray(X), np.asarray(y)
    if (n_steps_out==0 or n_steps_out==1):
        YY=YY.reshape((len(XX),1))
    return XX,YY