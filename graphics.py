
from CalcFunctions import *

import math
import matplotlib.pyplot as plt


def showGraphics(image, width, height, title):
    xArray = []
    maxCheckPoints = 400
    xArray.insert(0, math.floor((-0.5) * maxCheckPoints))

    for i in range(1, maxCheckPoints):
        xArray.insert(i, i - (maxCheckPoints / 2))
        xArray[i] = int(math.floor(xArray[i]))
    yArray = [-10, -5, 0, 5, 10]

    plt.figure()
    for y in yArray:
        autoCorrelation = []
        for x in xArray:
            autoCorrelation.append(getRAuto(image, width, height, x, y))

        plt.title(title)
        plt.plot(xArray, autoCorrelation(image, xArray, y), label='$y = %i$' % y)
        plt.legend()

    plt.show()


def getRAuto(fullImage, width, height, deltaX, deltaY):
    def correctX(x):
        res = x
        if x < 0:
            res = 0
        elif x > len(fullImage):
            res = len(fullImage)
        return res

    def correctY(y):
        res = y
        if y < 0:
            res = 0
        elif y > len(fullImage[0]):
            res = len(fullImage[0])
        return res

    image1 = [[]]
    image2 = [[]]
    currentRow = 0

    firstStartRow = correctX(0 + deltaX)
    firstStartColumn = correctY(0 + deltaY)
    firstEndRow = correctX(len(fullImage) + deltaX)
    firstEndColumn = correctY(len(fullImage[0]) + deltaY)

    secondStartRow = correctX(0 - deltaX)
    secondStartColumn = correctY(0 - deltaY)
    secondEndRow = correctX(len(fullImage) - deltaX)
    secondEndColumn = correctY(len(fullImage[0]) - deltaY)

    for i in range(firstStartRow, firstEndRow):
        currentColumn = 0
        image1.insert(currentRow, [])
        for j in range(firstStartColumn, firstEndColumn):
            image1[currentRow].insert(currentColumn, fullImage[i][j])
            currentColumn += 1
        currentRow += 1

    if len(image1) > 0:
        image1.pop(len(image1) - 1)

    currentRow = 0
    for i in range(secondStartRow, secondEndRow):
        currentColumn = 0
        image2.insert(currentRow, [])
        for j in range(secondStartColumn, secondEndColumn):
            image2[currentRow].insert(currentColumn, fullImage[i][j])
            currentColumn += 1
        currentRow += 1
    if len(image2) > 0:
        image2.pop(len(image2) - 1)

    return getCorrelation(image1, image2, width, height)


def createBarChart(componentArray, label, rangeValues):
    fig = plt.figure()
    plt.title(label)
    plt.hist(componentArray, bins=255, range=rangeValues)
    plt.show()