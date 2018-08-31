import pandas as pd
from datetime import datetime
import numpy as np
import sys

windowPath    = './input/window.txt'
actualPath    = './input/actual.txt'
predictedPath = './input/predicted.txt'
comparisonFile= './output/comparison.txt'


def preProcess(actualData, predictedData, windowsize):
    ''' 
    This function preprocesses the dataset to delete unuseful rows, 
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
    data = actualData.merge(predictedData, on = ['time', 'stock'], suffixes = ['Actu', 'Pred'], how = 'left')
    
    # Converting the timestep data to datetime data
    data['time'] = pd.to_datetime(data['time'] * 3600, unit = 's')

    # Set 'time' column as index of the dataframe
    data.set_index(['time'], inplace = True)

    # Check whether the windowsize is larger that the number of time steps
    # Aborts the program if this is True
    if data.index.nunique() < windowsize:
        sys.exit('Error: Window size (%s) is larger than the number of time steps (%s). Aborting ...'
                %(str(windowsize), str(data.index.nunique())))
    
    return data

def averageErrorCalc(data, windowsize):
    '''
    This function calculates the 'average error' as described in the README file, 
    and writes the results in ../output/comparison.txt file.
    '''
    # Compute 'error' as the absolute different of actial and predicted data
    data['error'] = abs(data['priceActu'] - data['pricePred'])

    # Compute the sum and # of valid 'error' data for each hour
    data_sum_count = data.groupby('time')['error'].agg(['sum','count'])
    del (data)

    # Calculate the sum and the total # of the valid error data for sliding windows of size 'windowsize'
    # Delete data_sum_count to prevent memory issues
    data_sum    = data_sum_count.rolling('%sh'%str(windowsize), min_periods=1)['sum'].sum()
    data_count  = data_sum_count.rolling('%sh'%str(windowsize), min_periods=1)['count'].sum()
    del (data_sum_count)
    
    # Calculate the 'average error'
    data_final = pd.DataFrame((data_sum/data_count).iloc[windowsize-1:], columns = ['averageError'])

    # Prepare the dataset to be written into the output file
    # Add the start and end of the corresponding time period for 'averageError'
    data_final['start']   = np.arange(1, len(data_final)+1)
    data_final['end']     = np.arange(windowsize, len(data_final)+windowsize)

    # Write the result into the output file with the described format 
    data_final.to_csv(comparisonFile, sep='|', index=False, na_rep='NA', 
            columns = ['start', 'end', 'averageError'], header=False, float_format='%.2f')

if __name__ == '__main__':

    # Read the input files 
    windowFile = open(windowPath)
    windowsize = int(windowFile.readlines()[0])
    actualData    = pd.read_csv(actualPath   , sep = '|', names = ['time', 'stock', 'price'])
    predictedData = pd.read_csv(predictedPath, sep = '|', names = ['time', 'stock', 'price'])

    # Preprocess the datasets and merge them into 'data' dataset
    data = preProcess(actualData, predictedData, windowsize)
    
    # Delete the original dataset to prevent memory shortage issue
    del (actualData)
    del (predictedData)
    
    # Take the average eroor for the time period of the size windowsize 
    averageErrorCalc(data, windowsize)
