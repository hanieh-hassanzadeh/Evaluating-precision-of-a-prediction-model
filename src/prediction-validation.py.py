import pandas as pd
from datetime import datetime
import numpy as np
#from info import report
#from preProcess import preProcess
#from io import BytesIO, TextIOWrapper, StringIO  # Python3
import sys

windowPath    = '../input/window.txt'
actualPath    = '../input/actual.txt'
predictedPath = '../input/predicted.txt'
comparisonFile= './output/comparison3.txt'


def preProcess(actualData, predictedData, windowsize, reportNeede, stockRep):
    ''' This function preprocesses the dataset to delete unuseful rows, 
    merges the two datasets, and sets 'time' as the index of the dataset
    in datetime units. If the windowsize is larger than the number of 
    timesteps, the program aborts.
    '''

    # Drop rows with missing values and drop duplicate
    actualData.dropna(inplace = True)
    actualData.drop_duplicates(inplace = True)    
    predictedData.dropna(inplace = True)
    predictedData.drop_duplicates(inplace = True)    
    
    # Combine the two datasets
    data = actualData.merge(predictedData, on = ['time', 'stockName'], suffixes = ['Actu', 'Pred'], how = 'left')
    
    # Converting the timestep data to datetime data
    data['time'] = pd.to_datetime(data['time'] * 3600, unit = 's')

    # Set 'time' column as index of the dataframe
    data.set_index(['time'], inplace = True)

    # Check wkether the windowsize is larger that the number of time steps
    if data.index.nunique() < windowsize:
        sys.exit('Error: Window size (%s) is larger than the number of time steps (%s). Aborting ...'%(str(windowsize), str(data.index.nunique())))
    
    return data

def precisionCalc( data, windowsize):
        data['absDiff'] = abs(data['valActu'] - data['valPred'])
        data = data.groupby('time')['absDiff'].agg(['sum','count'])
        data_sum = data.rolling('%sh'%str(windowsize), min_periods=1)['sum'].sum()
        data_count = data.rolling('%sh'%str(windowsize), min_periods=1)['count'].sum()
        data = pd.DataFrame((data_sum/data_count).iloc[windowsize-1:], columns = ['modelPrecision'])
        data['start']   = np.arange(1, len(data)+1)
        data['end']     = np.arange(windowsize, len(data)+windowsize)
        data.to_csv(comparisonFile, sep='|', index=False, columns = ['start', 'end', 'modelPrecision'], header=False, float_format='%.2f')

if __name__ == '__main__':

    startTime = datetime.now()
    reportNeeded = False
    stockRep    = []

    windowFile = open(windowPath)
    windowsize = int(windowFile.readlines()[0])
    actualData    = pd.read_csv(actualPath   , sep = '|', names = ['time', 'stockName', 'val'])
    predictedData = pd.read_csv(predictedPath, sep = '|', names = ['time', 'stockName', 'val'])

    data = preProcess(actualData, predictedData, windowsize, reportNeeded, stockRep)
    del (actualData)
    del (predictedData)
    precisionCalc(data, windowsize)
    print (datetime.now() - startTime )
