#プレビュー上で投げ縄で場所を選んでコピーし、PhotoShopでクリップボードを介して開き、pngで保存する。
#そのpngファイルを以下に投げる
import cv2
import numpy as np
from PIL import ImageGrab, Image
import matplotlib.pyplot as plt
#im = ImageGrab.grabclipboard() #直接的なクリップボード経由はどうもいまいち！！
#im.save('im.png')

#name each image as number+.png
name = ['左上', '左下', '右上', '右下', 'max_temp', 'min_temp']

for i, w in enumerate(name):
    im = cv2.imread(str(i) + '.png')
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray_min = np.array([0])
    gray_max = np.array([254])
    mask = cv2.inRange(gray, gray_min,  gray_max)
    #im = np.array(mask)
    plt.imshow(mask)
    #plt.show()
    mean_val = cv2.mean(gray,mask=mask)
    print(w)
    print(mean_val)
    #mean_val2 = cv2.mean(im)
    #print(mean_val2)
