#プレビュー上で投げ縄で場所を選んでコピーし、PhotoShopでクリップボードを介して開き、pngで保存する。
#そのpngファイルを以下に投げる
import cv2
import numpy as np
from PIL import ImageGrab, Image
import matplotlib.pyplot as plt
#im = ImageGrab.grabclipboard() #直接的なクリップボード経由はどうもいまいち！！
#im.save('im.png')

im1 = cv2.imread('1.png') #左上の植物
im2 = cv2.imread('2.png') #左下の植物
im3 = cv2.imread('3.png') #右上の植物
im4 = cv2.imread('4.png') #右下の植物

gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
gray_min = np.array([0])
gray_max = np.array([254])
mask = cv2.inRange(gray, gray_min,  gray_max)
#im = np.array(mask)
plt.imshow(mask)
plt.show()
mean_val = cv2.mean(gray,mask=mask)
print('左上')
print(mean_val)
#mean_val2 = cv2.mean(im)
#print(mean_val2)

gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
gray_min = np.array([0])
gray_max = np.array([254])
mask = cv2.inRange(gray, gray_min,  gray_max)
#im = np.array(mask)
plt.imshow(mask)
plt.show()
mean_val = cv2.mean(gray,mask=mask)
print('左下')
print(mean_val)
#mean_val2 = cv2.mean(im)
#print(mean_val2)

gray = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)
gray_min = np.array([0])
gray_max = np.array([254])
mask = cv2.inRange(gray, gray_min,  gray_max)
#im = np.array(mask)
plt.imshow(mask)
plt.show()
mean_val = cv2.mean(gray,mask=mask)
print('右上')
print(mean_val)
#mean_val2 = cv2.mean(im)
#print(mean_val2)

gray = cv2.cvtColor(im4, cv2.COLOR_BGR2GRAY)
gray_min = np.array([0])
gray_max = np.array([254])
mask = cv2.inRange(gray, gray_min,  gray_max)
#im = np.array(mask)
plt.imshow(mask)
plt.show()
mean_val = cv2.mean(gray,mask=mask)
print('右下')
print(mean_val)
#mean_val2 = cv2.mean(im)
#print(mean_val2)