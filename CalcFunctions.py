
def roundCrop(value):
    if value < 0:
        return 0
    elif value > 255:
        return 255
    return value


def decimationEvenNumbered(array, width, height, times=1):
    w_downsampled, h_downsampled = width, height
    for time in range(times):
        A_downsampled = []
        for i in range(1, h_downsampled + 1, 2):
            for j in range(1, w_downsampled + 1, 2):
                A_downsampled.append(array[i * w_downsampled + j])
        array = A_downsampled
        h_downsampled, w_downsampled = h_downsampled // 2, w_downsampled // 2

    A_restored = []
    for time in range(times):
        A_restored = [[0 for j in range(w_downsampled * 2)] for i in range(h_downsampled * 2)]
        for i in range(h_downsampled):
            for j in range(w_downsampled):
                i_new = i * 2 + 1
                j_new = j * 2 + 1

                A_restored[i_new][j_new] = A_downsampled[i * w_downsampled + j]
                if j_new > 0:
                    A_restored[i_new][j_new - 1] = A_downsampled[i * w_downsampled + j]
                if i_new > 0:
                    A_restored[i_new - 1][j_new] = A_downsampled[i * w_downsampled + j]
                if i_new > 0 and j_new > 0:
                    A_restored[i_new - 1][j_new - 1] = A_downsampled[i * w_downsampled + j]
        A_downsampled = [] # A_downsampled = A_restored
        for sublist in A_restored:
            for item in sublist:
                A_downsampled.append(item)
        h_downsampled *= 2
        w_downsampled *= 2
    return A_restored


def convertForDecimation(yArray, Cr_restored, Cb_restored, label):
    yFile = bytearray(fullImage[:pixel_offset])
    sumR = 0
    sumG = 0
    sumB = 0
    sumCr = 0
    sumCb = 0
    for i in range(height):
        for j in range(width):
            g = cadr(yArray[i * width + j] - 0.714 * (Cr_restored[i][j] - 128) - 0.334 * (Cb_restored[i][j] - 128))
            r = cadr(yArray[i * width + j] + 1.402 * (Cr_restored[i][j] - 128))
            b = cadr(yArray[i * width + j] + 1.772 * (Cb_restored[i][j] - 128))
            sumR = sumR + (imageR[i * width + j] - int(r)) ** 2
            sumG = sumG + (imageG[i * width + j] - int(g)) ** 2
            sumB = sumB + (imageB[i * width + j] - int(b)) ** 2
            sumCr = sumCr + (int(Cr_restored[i][j]) - int(crArray[i * width + j])) ** 2
            sumCb = sumCb + (int(Cb_restored[i][j]) - int(cbArray[i * width + j])) ** 2
            yFile.append(int(b))
            yFile.append(int(g))
            yFile.append(int(r))
    print(label)
    print('PSNR( Blue ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumB))
    print('PSNR( Green ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumG))
    print('PSNR( Red ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumR))
    print('PSNR( Cb ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumCb))
    print('PSNR( Cr ) = ', 10 * math.log10((width * height * (255 ** 2)) / sumCr))
    return yFile