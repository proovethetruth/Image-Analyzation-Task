
import math

def saveInFileAndGetComponents(image, filename, position, startPos, width, height):
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


def getCorrelation(image1, image2, width, height):
    FirstMathExpect = sum(image1) / (width * height)
    SecondMathExpect = sum(image2) / (width * height)

    cov = sum([(image1[i] - FirstMathExpect) * (image2[i] - SecondMathExpect) for i in range(len(image1))]) / (width * height)

    std1 = math.sqrt(sum([(image1[i] - FirstMathExpect) ** 2 for i in range(len(image1))]) / (width * height - 1))
    std2 = math.sqrt(sum([(image2[i] - SecondMathExpect) ** 2 for i in range(len(image2))]) / (width * height - 1))

    correlation = cov / (std1 * std2)
    return correlation