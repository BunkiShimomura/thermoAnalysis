#IRと普通の画像の葉っぱをぴったり重ね合わせるために座標を調べるプログラム
#別ウィンドウででできた座標を記録

#jupyterではなく、普通のpython3で。
#射影変換のための４すみの取得、カーソルを手で動かし、目で見て調べるfrom PIL import Image
import numpy as np
from PIL import ImageGrab, Image
import matplotlib.pyplot as plt

im = Image.open('IR_6854non.JPG')
im_list = np.asarray(im)
plt.imshow(im_list)
coordinate = plt.ginput(n=4)
print(coordinate)
