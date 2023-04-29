
from FileIO import *
from CalcFunctions import *

import math

class ImageTask:
    imageFile = 0
    fullImage = 0
    pixelOffset = 0
    width = 0
    height = 0

    def __init__(self, filename) -> None:
        self.imageFile = open(filename, 'rb')
        header = self.imageFile.read(54)
        self.pixelOffset = int.from_bytes(header[10:14], byteorder='little')
        self.width = int.from_bytes(header[18:22], byteorder='little')
        self.height = int.from_bytes(header[22:26], byteorder='little')
        self.imageFile.seek(0)
        self.fullImage = bytearray(self.imageFile.read())
        self.imageFile.close()

    def solve(self):
        self.task2()
        self.task3()
        return
    

    def task2(self):
        imageR = self.saveInFileAndGetComponents(self.fullImage.copy(), 'components/' + self.filename[0:-4] + '_Red.bmp', 2)
        imageG = self.saveInFileAndGetComponents(self.fullImage.copy(), 'components/' + self.filename[0:-4] + '_Green.bmp', 1)
        imageB = self.saveInFileAndGetComponents(self.fullImage.copy(), 'components/' + self.filename[0:-4] + '_Blue.bmp', 0)

        print('r(red, green) = ', self.getCorrelation(imageR, imageG))
        print('r(red, blue) = ', self.getCorrelation(imageR, imageB))
        print('r(blue, green) = ', self.getCorrelation(imageB, imageG))
    
    def task3(self)

    def saveInFileAndGetComponents(self, copyImage, filename, startPos):
        step = 0
        storeImage = []
        for i in range(startPos, len(copyImage)):
            if step != self.pixelOffset:
                copyImage[i] = 0
            else:
                storeImage.append(copyImage[i])
            step = (step + 1) % 3

        tempImageFile = open(filename, 'wb')
        tempImageFile.write(bytes(copyImage)) 
        tempImageFile.close()

        return storeImage


    def getCorrelation(self, image1, image2):
        FirstMathExpect = sum(image1) / (self.width * self.height)
        SecondMathExpect = sum(image2) / (self.width * self.height)

        cov = sum([(image1[i] - FirstMathExpect) * (image2[i] - SecondMathExpect) for i in range(len(image1))]) / (self.width * self.height)

        std1 = math.sqrt(sum([(image1[i] - FirstMathExpect) ** 2 for i in range(len(image1))]) / (self.width * self.height - 1))
        std2 = math.sqrt(sum([(image2[i] - SecondMathExpect) ** 2 for i in range(len(image2))]) / (self.width * self.height - 1))

        correlation = cov / (std1 * std2)
        return correlation
    
