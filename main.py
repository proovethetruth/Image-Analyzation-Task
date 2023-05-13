
from CalcFunctions import *
from graphics import *

import numpy as np

def saveInFileAndGetComponents(image, filename, position, startPos):
    step = 0
    storeImage = []
    for i in range(startPos, len(image)):
        if step != position:
            image[i] = 0
        else:
            storeImage.append(image[i])
        step = (step + 1) % 3

    imageFile = open(filename, 'wb')
    imageFile.write(bytes(image)) 
    imageFile.close()
    return storeImage


if __name__ == "__main__":
    filename = 'kodim07.bmp'

    imageFile = open(filename, 'rb')
    header = imageFile.read(54)
    pixelOffset = int.from_bytes(header[10:14], byteorder='little')
    width = int.from_bytes(header[18:22], byteorder='little')
    height = int.from_bytes(header[22:26], byteorder='little')

    print('--------------- add ----------------------')
    rowSize = (width * 3 + 3) // 4 * 4
    pixelData = imageFile.read(rowSize * height)
    
    rotatedData = bytearray()
    for row in range(height - 1, -1, -1):
        for pixel in range(width):
            i = row * rowSize + pixel * 3
            rotatedData += pixelData[i:i+3]
    
    with open(filename[0:-4] + "_Rotated.bmp", "wb") as rotatedImageFile:
        rotatedImageFile.write(header + rotatedData)

    imageFile.seek(0)
    fullImage = bytearray(imageFile.read())
    imageFile.close()

    imageR = saveInFileAndGetComponents(fullImage.copy(), 'components/' + filename[0:-4] + '_Red.bmp', 2, pixelOffset)
    imageG = saveInFileAndGetComponents(fullImage.copy(), 'components/' + filename[0:-4] + '_Green.bmp', 1, pixelOffset)
    imageB = saveInFileAndGetComponents(fullImage.copy(), 'components/' + filename[0:-4] + '_Blue.bmp', 0, pixelOffset)

    print('---------------- 4 -----------------------')
    print('r(red, green) = ', getCorrelation(imageR, imageG, width, height))
    print('r(red, blue) = ', getCorrelation(imageR, imageB, width, height))
    print('r(blue, green) = ', getCorrelation(imageB, imageG, width, height))

    # showGraphics(imageR, width, height, "image_r")
    # showGraphics(imageB, width, height, "image_b")
    # showGraphics(imageG, width, height, "image_g")

    yFile = bytearray(fullImage[:pixelOffset])
    cbFile = bytearray(fullImage[:pixelOffset])
    crFile = bytearray(fullImage[:pixelOffset])

    yArray = []
    cbArray = []
    crArray = []
    for i in range(pixelOffset, len(fullImage), 3):
        y = 0.299 * fullImage[i + 2] + 0.587 * fullImage[i + 1] + 0.114 * fullImage[i]
        cb = 0.5643 * (fullImage[i] - y) + 128
        cr = 0.7132 * (fullImage[i + 2] - y) + 128
        yArray.append(y)
        cbArray.append(cb)
        crArray.append(cr)

        yFile.extend(bytearray([int(y),int(y),int(y)]))
        crFile.extend(bytearray([int(cr),int(cr),int(cr)]))
        cbFile.extend(bytearray([int(cb),int(cb),int(cb)]))

    print('--------------- 5, 6 ---------------------')

    print('R(y, Cb) = ', getCorrelation(yArray, cbArray, width, height))
    print('R(y, Cr) = ', getCorrelation(yArray, crArray, width, height))
    print('R(Cb, Cr) = ', getCorrelation(cbArray, crArray, width, height))

    imageFile = open('components/' + filename[0:-4] + '_y.bmp', 'wb')
    imageFile.write(bytes(yFile))
    imageFile.close()

    imageFile = open('components/' + filename[0:-4] + '_Cb.bmp', 'wb')
    imageFile.write(bytes(cbFile))
    imageFile.close()

    imageFile = open('components/' + filename[0:-4] + '_Cr.bmp', 'wb')
    imageFile.write(bytes(crFile))
    imageFile.close()

    print('---------------- 7 -----------------------')
    yFile = bytearray(fullImage[:pixelOffset])
    sumR, sumG, sumB = 0, 0, 0

    for i in range(len(yArray)):
        g = roundCrop(yArray[i] - 0.714 * (crArray[i] - 128) - 0.334 * (cbArray[i] - 128))
        r = roundCrop(yArray[i] + 1.402 * (crArray[i] - 128))
        b = roundCrop(yArray[i] + 1.772 * (cbArray[i] - 128))
        sumR = sumR + (imageR[i] - int(r)) ** 2
        sumG = sumG + (imageG[i] - int(g)) ** 2
        sumB = sumB + (imageB[i] - int(b)) ** 2 
        yFile.append(int(b))
        yFile.append(int(g))
        yFile.append(int(r))

    print('PSNR(blue) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumB))
    print('PSNR(green) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumG))
    print('PSNR(red) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumR))

    imageFile = open('components/' + filename[0:-4] + '_Restored.bmp', 'wb')
    imageFile.write(bytes(yFile)) 
    imageFile.close()
  
    yArray = [round(yArray[i]) for i in range(len(yArray))]
    yArray = np.array(yArray)
    cbArray = [round(cbArray[i]) for i in range(len(cbArray))]
    cbArray = np.array(cbArray)
    crArray = [round(crArray[i]) for i in range(len(crArray))]
    crArray = np.array(crArray)

    imageR = [round(imageR[i]) for i in range(len(imageR))]
    imageR = np.array(imageR)
    imageG = [round(imageG[i]) for i in range(len(imageG))]
    imageG = np.array(imageG)
    imageB = [round(imageB[i]) for i in range(len(imageB))]
    imageB = np.array(imageB)

    print('---------------- 12 ----------------------')
    
    createBarChart(yArray, "(Y_comp) frequency", (0, 255))
    createBarChart(cbArray, "(Cb_comp) frequency", (0, 255))
    createBarChart(crArray, "(Cr_comp) frequency", (0, 255))
    createBarChart(imageR, "(R_comp) frequency", (0, 255))
    createBarChart(imageG, "(G_comp) frequency", (0, 255))
    createBarChart(imageB, "(B_comp) frequency", (0, 255))

    print('--------------- 8-11 ---------------------')

    cbRestored = decimationEvenNumbered(cbArray, width, height)
    crRestored = decimationEvenNumbered(crArray, width, height)
    print("Even-numbered decimation (x2)")
    yFile = convertForDecimation(yArray, crRestored, cbRestored, 
                                 fullImage, pixelOffset, width, height, imageR, imageG, imageB, crArray, cbArray)
    
    imageFile = open('components/After Even-Numbered Decimation (x2).bmp', 'wb')
    imageFile.write(bytes(yFile)) 
    imageFile.close()

    cbRestored = decimationAriphmeticMean(cbArray, width, height)
    crRestored = decimationAriphmeticMean(crArray, width, height)
    print("\nAriphmetic Mean Decimation (x2)")
    yFile = convertForDecimation(yArray, crRestored, cbRestored, 
                                 fullImage, pixelOffset, width, height, imageR, imageG, imageB, crArray, cbArray)
    
    imageFile = open('components/After Ariphmetic Mean Decimation (x2).bmp', 'wb')
    imageFile.write(bytes(yFile)) 
    imageFile.close()

    cbRestored2 = decimationEvenNumbered(cbArray, width, height, times=2)
    crRestored2 = decimationEvenNumbered(crArray, width, height, times=2)
    print("\nEven-numbered decimation decimation (x4)")
    yFile = convertForDecimation(yArray, crRestored2, cbRestored2, 
                                 fullImage, pixelOffset, width, height, imageR, imageG, imageB, crArray, cbArray)

    imageFile = open('components/After Even-Numbered Decimation (x4).bmp', 'wb')
    imageFile.write(bytes(yFile))
    imageFile.close()


    cbRestored2 = decimationAriphmeticMean(cbArray, width, height, times=2)
    crRestored2 = decimationAriphmeticMean(crArray, width, height, times=2)
    print("\nAriphmetic mean decimation (x4)")
    yFile = convertForDecimation(yArray, crRestored2, cbRestored2,
                                 fullImage, pixelOffset, width, height, imageR, imageG, imageB, crArray, cbArray)

    imageFile = open('components/After Ariphmetic  Decimation (x4).bmp', 'wb')
    imageFile.write(bytes(yFile))
    imageFile.close()

    print('----------------- 13 -----------------------')
    print('H(B) = ' + str(calcEntropy(imageB)))
    print('H(G) = ' + str(calcEntropy(imageG)))
    print('H(R) = ' + str(calcEntropy(imageR)))
    print('H(Y) = ' + str(calcEntropy(yArray)))
    print('H(Cb) = ' + str(calcEntropy(cbArray)))
    print('H(Cr) = ' + str(calcEntropy(crArray)))

    print('---------------- 14-16 ---------------------')
    print('H(dB^1), H(dB^2), H(dB^3), H(dB^4) = ' + str(calcDiffMod(imageB, width, height))[1:-1])
    print('H(dG^1), H(dG^2), H(dG^3), H(dG^4) = ' + str(calcDiffMod(imageG, width, height))[1:-1])
    print('H(dR^1), H(dR^2), H(dR^3), H(dR^4) = ' + str(calcDiffMod(imageR, width, height))[1:-1])
    print('H(dY^1), H(dY^2), H(dY^3), H(dY^4) = ' + str(calcDiffMod(yArray, width, height))[1:-1])
    print('H(dCb^1), H(dCb^2), H(dCb^3), H(dCb^4) = ' + str(calcDiffMod(cbArray, width, height))[1:-1])
    print('H(dCr^1), H(dCr^2), H(dCr^3), H(dCr^4) = ' + str(calcDiffMod(crArray, width, height))[1:-1])