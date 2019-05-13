import cv2
import numpy as np
import matplotlib.pyplot as plt
filenameIMG = 'IMG_5136' #IMGの画像
filenameIR = 'IR_6854' #IRの画像

imgIMG = cv2.imread(filenameIMG+'.jpg')

# 画像の座標上から4角を切り出す
pts1_IMG = np.float32([[831.552, 502.136],  [2734.02, 498.435], [864.864, 2360.19],  [2715.51, 2378.69]]) #pts1 = np.float32([[左上の座標],[右上の座標],[左下の座標],[右下の座標]]) #step0で抽出したのを入れる
pts2_IMG = np.float32([[0,0],[600,0],[0,520],[600,520]]) #resize

# 透視変換の行列を求める
M_IMG = cv2.getPerspectiveTransform(pts1_IMG,pts2_IMG)

# 変換行列を用いて画像の透視変換
rstIMG = cv2.warpPerspective(imgIMG,M_IMG,(600,520))
print(str(type(rstIMG)))
# 透視変換後の画像を保存
cv2.imwrite(filenameIMG+'_henkango.png',rstIMG)

imgIR = cv2.imread(filenameIR+'.jpg')

# 画像の座標上から4角を切り出す
pts1_IR = np.float32([[126.643, 96.1234], [466.903, 101.318], [123.396, 440.279], [471.448, 448.721]]) #pts1 = np.float32([[左上の座標],[右上の座標],[左下の座標],[右下の座標]])
pts2_IR = np.float32([[0,0],[600,0],[0,520],[600,520]]) #resize

# 透視変換の行列を求める
M_IR = cv2.getPerspectiveTransform(pts1_IR,pts2_IR)

# 変換行列を用いて画像の透視変換
rst = cv2.warpPerspective(imgIR,M_IR,(600,520))
# 透視変換後の画像を保存
cv2.imwrite(filenameIR+'_henkango.png',rst)

#%matplotlib inline
#filenameIMG = 'IMG_0918_pot22_henkango'
#filenameIR = 'IR_6082_pot22_gray_henkango'
#im = cv2.imread(filenameIMG+".png") #緑＋土の画像 デジカメ撮影
print(rstIMG)
hsv = cv2.cvtColor(rstIMG, cv2.COLOR_BGR2HSV)
hsv_gaus = cv2.GaussianBlur(hsv, (3,3),0)
hsv_min = np.array([30, 80, 60])
hsv_max = np.array([255, 255, 255])
mask = cv2.inRange(hsv_gaus, hsv_min,  hsv_max)
im_list = np.asarray(mask)
plt.imshow(im_list)
plt.show()
print("type is " + str(type(im_list)))
#cv2.imwrite('color1_mask.png',im_list) #緑のみ ノイズあり
kernel = np.ones((5,5),np.uint8) #かっこの数字が大きいほど大きいノイズが除去される。
result = cv2.morphologyEx(im_list, cv2.MORPH_OPEN, kernel)
plt.imshow(result)
plt.show()
cv2.imwrite(filenameIMG+'_mask_minusNoize.png',result) #緑のみでノイズがなくなった画像 これがフィルター的な画像となる

from PIL import Image, ImageDraw, ImageFilter
im_rgb = Image.open(filenameIMG+'_henkango.png')#緑＋土の画像 デジカメ撮影
im_a = Image.open(filenameIMG+'_mask_minusNoize.png').convert('L')#緑のみでノイズがなくなった画像
im_rgba = im_rgb.copy()
im_rgba.putalpha(im_a)
im_rgba.save(filenameIMG+'_mask_minusNoize_alpha.png') #アラビのみの部分が切り出され他は透明になった画像

im_rgb = Image.open(filenameIR+'_henkango.png')#IRの画像
#im_a = Image.open('IMG_0944_pot33_henkango_mask_minusNoize.png').convert('L') #緑のみでノイズがなくなった画像 これがフィルター的な画像となる
im_rgb_c = im_rgb.copy()
im_rgb_c.putalpha(im_a)
im_rgb_c.save(filenameIR+'_alpha.png') #IR画像からアラビのみが切り出された他は透明になった画像
