'''简单处理下图片，空白区域灰度值255，matlab弄不好，通道分离和合成用ENVI做的。。。'''
import numpy as np
from PIL import Image

image_path = r""

image = Image.open(image_path)
matrix = np.array(image)
print(matrix.shape)

matrix[matrix==0] = 255

im = Image.fromarray(matrix)

im.save(r"")