import numpy as np
import pandas as pd
import matplotlib as plt

cut_1 = np.array([1040,3260]) # the cut of mechapod_FT_data for forward_Aug_30
freq = 125.0 # the frequency of FT data in Hz

file_name = '/home/birds/pyckbot/Sun/mechapod_FT/data/' + 'mechapod_FT_forward_Aug_30.csv'
raw_FT_data = pd.read_csv(file_name) # read the whole data
FT_index = np.ndarray.astype(np.concatenate((np.zeros(1),np.linspace(6,14,9)),axis=0),int) 
# the column index of the FT data with time stamp
FT_data = raw_FT_data.values[cut_1[0]:cut_1[1],FT_index[1:]]
time_stamp_FT = np.linspace(0,shape(FT_data)[0]-1,shape(FT_data)[0])/freq


file_name = '/home/birds/pyckbot/Sun/mechapod_FT/data/' + 'mechapod_POS_forward_Aug_30.tsv'
raw_POS_data = pd.read_csv(file_name, skiprows=10, sep='\t')
POS_data = raw_POS_data.values[:,0:120] # the last column are nan
POS_data[POS_data==0]=np.nan # replace all missing marker info to be nan
time_stamp_POS = np.linspace(0,time_stamp_FT[-1],shape(POS_data)[0])