# Evaluating accuracy of a prediction model

Assume that we have a model to predict the stock price. This model outputs various stocks price every hour, in the form of 

`timestep|stockname|price`

In this project, I evaluate the accuracy of the model by calculating `average error` for an sliding time window of `windowsize`, which is provided in `./input/window.txt` file.

##  Dependencies and run instructions

Thos code is written in Python 3, and uses the following packages:
pandas
datetime 
numpy
sys

To run the code, simply use run `./run.sh` from the project's root directory. To change the input or output path please modify the header of `./src/prediction-validation.py`.

## Overview

The data from `window.txt` , `actial.txt`, and `predicted.txt` are read in the main function. Then the data is preprocessed, and finally the average error is calculated and the result is written into the output file. Bellow are some detailes procedures.

## Preprocessing

The first step to prepare the data is to remove unuseful rows; e.g. drop rows with missing values and drop duplicate.

Second, I combine the two dataframes. Thirsd, I convert the timestep data to datetime data, and set the column as dataframe index. I will use this index later to roll over 'windowsize-hour' time period.

Finally, I check whether the windowsize is larger that the number of time steps, which is an invalid condition. If this condition is True, the program aborts.

These steps are done in `preProcess` function, which output is a cleaned dataframe called `data`.

## Calculating the average error

To calculate the `average error`, I, first, calculate `error` which is the absolute difference between actial and predicted data. Second, I start sliding a time window with `windowsize` size over the data and calculate the `sum` and the number of the data (`count`) corresponding to each time perid. Third, I divide `sum` to `count`, to get the average for each time window data. 

These steps are done in `averageErrorCalc` function.

## Outputting 

Finally, I output the data in `./output/comparison.txt` file. I set the output to be in this

`begining-of-time-window|end-of-time-window|average-error`

format. Also, I set the `average error` to be rounded off to 2 decimal places, and if its value is NaN, to be written as `NA`.


### Note: Whenever possible, I delete the variables (dataframes) that would not be used in the remaining of the program. This is done to prevent any limited memory issues.

