




def getCorrelation(image1, image2, width, height):
    FirstMathExpect = sum(image1) / (width * height)
    SecondMathExpect = sum(image2) / (width * height)

    cov = sum([(image1[i] - FirstMathExpect) * (image2[i] - SecondMathExpect) for i in range(len(image1))]) / (width * height)

    std1 = math.sqrt(sum([(image1[i] - FirstMathExpect) ** 2 for i in range(len(image1))]) / (width * height - 1))
    std2 = math.sqrt(sum([(image2[i] - SecondMathExpect) ** 2 for i in range(len(image2))]) / (width * height - 1))

    correlation = cov / (std1 * std2)
    return correlation