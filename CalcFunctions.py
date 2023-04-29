
import math

def getCorrelation(image1, image2, width, height):
    FirstMathExpect = sum(image1) / (width * height)
    SecondMathExpect = sum(image2) / (width * height)

    cov = sum([(image1[i] - FirstMathExpect) * (image2[i] - SecondMathExpect) for i in range(len(image1))]) / (width * height)

    std1 = math.sqrt(sum([(image1[i] - FirstMathExpect) ** 2 for i in range(len(image1))]) / (width * height - 1))
    std2 = math.sqrt(sum([(image2[i] - SecondMathExpect) ** 2 for i in range(len(image2))]) / (width * height - 1))

    correlation = cov / (std1 * std2)
    return correlation

def roundCrop(value):
    if value < 0:
        return 0
    elif value > 255:
        return 255
    return value


def decimationEvenNumbered(array, width, height, times=1):
    wDownSampled, hDownSampled = width, height
    for time in range(times):
        aDownSampled = []
        for i in range(1, hDownSampled + 1, 2):
            for j in range(1, wDownSampled + 1, 2):
                aDownSampled.append(array[i * wDownSampled + j])
        array = aDownSampled
        hDownSampled, wDownSampled = hDownSampled // 2, wDownSampled // 2

    aRestored = []
    for time in range(times):
        aRestored = [[0 for j in range(wDownSampled * 2)] for i in range(hDownSampled * 2)]
        for i in range(hDownSampled):
            for j in range(wDownSampled):
                iNew = i * 2 + 1
                jNew = j * 2 + 1

                aRestored[iNew][jNew] = aDownSampled[i * wDownSampled + j]
                if jNew > 0:
                    aRestored[iNew][jNew - 1] = aDownSampled[i * wDownSampled + j]
                if iNew > 0:
                    aRestored[iNew - 1][jNew] = aDownSampled[i * wDownSampled + j]
                if iNew > 0 and jNew > 0:
                    aRestored[iNew - 1][jNew - 1] = aDownSampled[i * wDownSampled + j]
        aDownSampled = []
        for sublist in aRestored:
            for item in sublist:
                aDownSampled.append(item)
        hDownSampled *= 2
        wDownSampled *= 2
    return aRestored


def convertForDecimation(yArray, crRestored, cbRestored, fullImage, pixelOffset, width, height, imageR, imageG, imageB, crArray, cbArray):
    yFile = bytearray(fullImage[:pixelOffset])
    sumR = 0
    sumG = 0
    sumB = 0
    sumCr = 0
    sumCb = 0
    for i in range(height):
        for j in range(width):
            g = roundCrop(yArray[i * width + j] - 0.714 * (crRestored[i][j] - 128) - 0.334 * (cbRestored[i][j] - 128))
            r = roundCrop(yArray[i * width + j] + 1.402 * (crRestored[i][j] - 128))
            b = roundCrop(yArray[i * width + j] + 1.772 * (cbRestored[i][j] - 128))
            sumR = sumR + (imageR[i * width + j] - int(r)) ** 2
            sumG = sumG + (imageG[i * width + j] - int(g)) ** 2
            sumB = sumB + (imageB[i * width + j] - int(b)) ** 2
            sumCr = sumCr + (int(crRestored[i][j]) - int(crArray[i * width + j])) ** 2
            sumCb = sumCb + (int(cbRestored[i][j]) - int(cbArray[i * width + j])) ** 2
            yFile.append(int(b))
            yFile.append(int(g))
            yFile.append(int(r))
    print('PSNR( Blue ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumB))
    print('PSNR( Green ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumG))
    print('PSNR( Red ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumR))
    print('PSNR( Cb ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumCb))
    print('PSNR( Cr ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumCr))
    return yFile


def decimationAriphmeticMean(array, width, height, times=1):
    wDownSampled, hDownSampled = width, height
    for time in range(times):
        aDownSampled = []
        for i in range(1, hDownSampled + 1, 2):
            for j in range(1, wDownSampled + 1, 2):
                aDownSampled.append((array[i * wDownSampled + j] + array[(i - 1) * wDownSampled + j] + array[i * wDownSampled + j - 1] + array[(i - 1) * wDownSampled + j - 1]) // 4)
        array = aDownSampled
        hDownSampled, wDownSampled = hDownSampled // 2, wDownSampled // 2

    aRestored = []
    for time in range(times):
        aRestored = [[0 for j in range(wDownSampled * 2)] for i in range(hDownSampled * 2)]
        for i in range(hDownSampled):
            for j in range(wDownSampled):
                iNew = i * 2 + 1
                jNew = j * 2 + 1

                aRestored[iNew][jNew] = aDownSampled[i * wDownSampled + j]
                if jNew > 0:
                    aRestored[iNew][jNew - 1] = aDownSampled[i * wDownSampled + j]
                if iNew > 0:
                    aRestored[iNew - 1][jNew] = aDownSampled[i * wDownSampled + j]
                if iNew > 0 and jNew > 0:
                    aRestored[iNew - 1][jNew - 1] = aDownSampled[i * wDownSampled + j]
        aDownSampled = []
        for sublist in aRestored:
            for item in sublist:
                aDownSampled.append(item)
        hDownSampled *= 2
        wDownSampled *= 2
    return aRestored

def calcEntropy(arrayValues):
    valueToAmount = {}
    for i in arrayValues:
        value = int(i)
        temp = valueToAmount.get(value)
        valueToAmount[value] = 1 if temp == None else valueToAmount[value] + 1
    entropy = 0
    all = 0
    for key in valueToAmount.keys():
        all += valueToAmount[key]
    for key in valueToAmount.keys():
        px = valueToAmount[key] / all
        entropy = entropy - px * math.log2(px)
    return entropy

def calcDiffMod(componentArray, width, height):
    diffModulation1 = []
    diffModulation2 = []
    diffModulation3 = []
    diffModulation4 = []
    for i in range(1, height):
        for j in range(1, width):
            diffModulation1.append(componentArray[i * width + j] - componentArray[i * width + j - 1])
            diffModulation2.append(componentArray[i * width + j] - componentArray[(i - 1) * width + j])
            diffModulation3.append(componentArray[i * width + j] - componentArray[(i - 1) * width + j - 1])          
            average = (componentArray[i * width + j - 1] + componentArray[(i - 1) * width + j] + componentArray[(i - 1) * width + j - 1]) / 3
            diffModulation4.append(componentArray[i * width + j] - average)

    return [calcEntropy(diffModulation1), calcEntropy(diffModulation2), calcEntropy(diffModulation3), calcEntropy(diffModulation4)]