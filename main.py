

from ImageTask import *

from FileIO import *
from CalcFunctions import *

import numpy as np

if __name__ == "__main__":
    filename = 'kodim07.bmp'

    imageFile = open(filename, 'rb')
    header = imageFile.read(54)
    pixelOffset = int.from_bytes(header[10:14], byteorder='little')
    width = int.from_bytes(header[18:22], byteorder='little')
    height = int.from_bytes(header[22:26], byteorder='little')
    imageFile.seek(0)
    fullImage = bytearray(imageFile.read())
    imageFile.close()


    imageR = saveInFileAndGetComponents(fullImage.copy(), 'components/' + filename[0:-4] + '_Red.bmp', 2, pixelOffset, width, height)
    imageG = saveInFileAndGetComponents(fullImage.copy(), 'components/' + filename[0:-4] + '_Green.bmp', 1, pixelOffset, width, height)
    imageB = saveInFileAndGetComponents(fullImage.copy(), 'components/' + filename[0:-4] + '_Blue.bmp', 0, pixelOffset, width, height)

    print('r(red, green) = ', getCorrelation(imageR, imageG, width, height))
    print('r(red, blue) = ', getCorrelation(imageR, imageB, width, height))
    print('r(blue, green) = ', getCorrelation(imageB, imageG, width, height))


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

    print('--------------------------------------------')
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

    print('--------------------------------------------')
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


    cbRestored = decimationEvenNumbered(cbArray, width, height)
    crRestored = decimationEvenNumbered(crArray, width, height)

    yFile = convertForDecimation(yArray, crRestored, cbRestored, "even_numbered decimation x2")