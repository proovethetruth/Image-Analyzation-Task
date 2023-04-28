
from FileIO import *

if __name__ == "__main__":
    filename = 'kodim07.bmp'
    
    with open(filename, 'rb') as imageFile:
        header = imageFile.read(54)
        pixelOffset = int.from_bytes(header[10:14], byteorder='little')
        width = int.from_bytes(header[18:22], byteorder='little')
        height = int.from_bytes(header[22:26], byteorder='little')

        imageFile.seek(0)
        fullImage = bytearray(imageFile.read())

        imageR = saveInFileAndGetComponents(fullImage.copy(), 'components/' + filename[0:-4] + '_Red.bmp', 2, pixelOffset, width, height)
        imageG = saveInFileAndGetComponents(fullImage.copy(), 'components/' + filename[0:-4] + '_Green.bmp', 1, pixelOffset, width, height)
        imageB = saveInFileAndGetComponents(fullImage.copy(), 'components/' + filename[0:-4] + '_Blue.bmp', 0, pixelOffset, width, height)
        imageFile.close()

    print('r(red, green) = ', getCorrelation(imageR, imageG, width, height))
    print('r(red, blue) = ', getCorrelation(imageR, imageB, width, height))
    print('r(blue, green) = ', getCorrelation(imageB, imageG, width, height))