import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Finds noisy data points in the experimental measurements of the cell's OCV
# input: a list with x,y values in each list object (the output of csvToList)
# returns: the indices of any anomalies, stored in a sequential list
def findAnomalyIndex(dataList):
    anomalyIndexList = list()
    for i in range(len(dataList)):
        if i != 0:
            if dataList[i][1] - dataList[i-1][1] > .01:
                anomalyIndexList.append(i)
    return anomalyIndexList


# Corrects a noisy data point by taking the average of the 2 adjacent data points
# input: the index of the anomaly (int), and list of x,y values in each list object (the output of csvToList)
# returns: none
def fixSingleAnomaly(anomalyIndex, dataSet):
    surroundingAverage = abs(
        (dataSet[anomalyIndex + 1][1] + dataSet[anomalyIndex - 1][1])/2)
    # print(surroundingAverage)
    dataSet[anomalyIndex][1] = surroundingAverage
    # print(dataSet[anomalyIndex][0])


# Reverses the order of a list
# input: any list
# returns: the reversed-order list
def flipList(inputList):
    flippedList = list()
    for i in range(len(inputList)):
        flippedList.append(inputList[len(inputList) - i - 1])
    return flippedList


# Combines two lists to form a np.array
# inputs: two lists of x and y values
# returns: the np.array of the x and y values
def createArray(listX, listY):
    newList = list()
    for i in range(len(listX)):
        newList.append([listX[i], listY[i]])
    return np.array(newList)


# Creates a list of values between min and max with defined spacing, similar to range but can do non-int spacing
# inputs: the min value, the max value, and the spacing
# returns: a list of values between min and max separated by spacing
def createSpacedList(min, max, spacing):
    currentVal = min
    spacedList = list()
    i = 0
    while currentVal < max:
        currentVal = min + (i * spacing)
        spacedList.append(currentVal)
        i += 1
    return spacedList


# Creates a list of the modeled nth order polynomial fit values
# input: order n of the polynomial fit, list of experimental x values, list of experimental y values
# returns: a list of the modeled y-values using the polynomial fit
def getPolyFitValues(order, xList, yList):
    coefficients = np.polyfit(xList, yList, order)
    modeledValues = list()
    for x in xList:
        yVal = 0
        i = 0
        while order - i >= 0:
            yVal += coefficients[i] * x ** (order - i)
            i += 1
        modeledValues.append(yVal)
    return modeledValues


# Finds the mean-square value for experimental and modeled values
# inputs: list of experimental x-values, list of experimental y-values, list of modeled y-values
# returns: the mean-squared value
def getMeanSquaredValue(experimentalValues, modeledValues):
    # Calculate the mean-squared value
    return np.mean((np.array(experimentalValues) - np.array(modeledValues))**2)


# Finds the optimal order n of a polynomial fit using minimum chi-square analysis
# inputs: a list of experimental x values (OCV measurements) and list of experimental y values (normalized SoC)
# returns: a list object of [order n, mean-squared value of the nth order fit], where n is the optimal order fit
def findOptimalOrderFit(xValues, yValues):
    # Only checks order n=1:8 to minimize compute time
    n = 1
    meanSquaredResults = list()
    while n <= 8:
        currentMeanSquared = getMeanSquaredValue(
            yValues, getPolyFitValues(n, xValues, yValues)) #yValues are the actual SOC values and getPolyFitValues are the predicted ones. 
        meanSquaredResults.append([n, currentMeanSquared])
        n += 1
    # find the minimum order n
    minIndex = 0
    minMeanSquared = 1000000000.0
    for i in range(len(meanSquaredResults)):
        if meanSquaredResults[i][1] < minMeanSquared:
            minMeanSquared = meanSquaredResults[i][1]
            minIndex = i
    # the returned object is of the form [order n, chi-squared value]
    return meanSquaredResults[minIndex]

#main function

def main():

    
    batteryData = pd.read_csv(
        "./OCV_Data.csv")
    batteryData1 = np.c_[[x for x in batteryData['Data Point']], [x for x in batteryData['Voltage']]]

    # Separate measurement numbers and OCV readings into separate lists
    measurementNumbers1 = list()
    voltageReading1 = list()
    for data in batteryData1:
        measurementNumbers1.append(data[0])
        voltageReading1.append(data[1])

    # Find anomalies - used if discharge is interrupted or there are isolated noisy data points
    anomalies = findAnomalyIndex(batteryData1)

    # Fix any anomalies
    for anomaly in anomalies:
        fixSingleAnomaly(anomaly - 1, batteryData1)

    # Refresh the lists with the corrected noisy data points
    measurementNumbers1 = list()
    voltageReading1 = list()
    for data in batteryData1:
        measurementNumbers1.append(data[0])
        voltageReading1.append(data[1])

    # Flip the order of the lists to allow for the SoC vs OCV plot
    measurementsAdjusted = flipList(measurementNumbers1)
    voltageReadingFinal = flipList(voltageReading1)

    # Normalize the data measurement numbers on a 0 to 100% scale
    numMeasurements = len(measurementsAdjusted)
    increment = 100.0/numMeasurements
    normalizedSoC = list()
    tempI = 0
    while tempI < numMeasurements:
        normalizedSoC.append(tempI*increment)
        tempI += 1


    # Finds the optimal order n of a polynomial fit of the data using minimum mean-square analysis
    optimalFitValues = findOptimalOrderFit(voltageReadingFinal, normalizedSoC)
    optimalOrder = optimalFitValues[0]

    # Creates a list of modeled SoC values using the optimal polynomial fit, used for plotting
    modeledValues = getPolyFitValues(
        optimalOrder, voltageReadingFinal, normalizedSoC)

   
    # PLOTTING

    # Plots the experimental SoC vs OCV
    plt.plot(voltageReadingFinal, normalizedSoC, label='Experimental Data')
    # Plots the modeled values using the polynomial fit for SoC vs OCV
    plt.plot(voltageReadingFinal, modeledValues, label='Polynomial Fit')
    plt.legend(loc='best')
    plt.ylabel('State of Charge (%)')
    plt.xlabel('Cell Voltage (V)')
    plt.title(
            "Battery State of Charge (SoC) vs\nOpen Circuit Voltage (OCV)", fontweight='bold')
    plt.grid(True)
    # Adjust spacing of subplots
    plt.subplots_adjust(wspace=0.35)

    plt.show()


main()
