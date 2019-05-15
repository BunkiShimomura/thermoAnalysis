import os
import csv
import glob
from pathlib import Path

from natsort import natsorted

import numpy as np
from PIL import ImageGrab, Image, ImageFilter, ImageDraw
from matplotlib import image
import matplotlib.pyplot as plt
import cv2



#IRと普通の画像の葉っぱをぴったり重ね合わせるために座標を調べるプログラム
#射影変換のための４すみの取得、カーソルを手で動かし、目で見て調べるfrom PIL import Image
#画像のファイル名のリストと座標をオリジナルとIRそれぞれについて返す
def extractCoordinate(pathToOriginal, pathToIR):

    originalImages = glob.glob(pathToOriginal + '/*')
    IRImages = glob.glob(pathToIR + '/*')

    originalImages = natsorted(originalImages)
    IRImages= natsorted(IRImages)


    coordinateOriginal = [] #list object to store obtained coordinate of original image
    coordinateIR = []

    for i in range(len(originalImages)):
        im = Image.open(originalImages[i])
        im_list = np.asarray(im)
        plt.imshow(im_list)
        coordinate = plt.ginput(n=4)
        coordinateOriginal.append(coordinate)
        plt.close()

    for i in range(len(IRImages)):
        im = Image.open(IRImages[i])
        im_list = np.asarray(im)
        plt.imshow(im_list)
        coordinate = plt.ginput(n=4)
        coordinateIR.append(coordinate)
        plt.close()

    return [originalImages, IRImages, coordinateOriginal, coordinateIR]

#アラビの元画像とIR画像を重ね合わせるためにサイズを統一する処理
def resize(filenameIMG, coordinate):
    imgIMG = cv2.imread(filenameIMG)

    # 画像の座標上から4角を切り出す
    pts1_IMG = np.float32(coordinate) #pts1 = np.float32([[左上の座標],[右上の座標],[左下の座標],[右下の座標]])
    pts2_IMG = np.float32([[0,0],[600,0],[0,520],[600,520]]) #resize

    # 透視変換の行列を求める
    M_IMG = cv2.getPerspectiveTransform(pts1_IMG,pts2_IMG)
    # 変換行列を用いて画像の透視変換
    rstIMG = cv2.warpPerspective(imgIMG,M_IMG,(600,520))
    # 透視変換後の画像を保存
    cv2.imwrite(filenameIMG[:-4]+'_henkango.png',rstIMG)

#アラビの元画像とIR画像を重ね合わせる処理
def superpose(filenameIMG, filenameIR, IMG_henkango, IR_henkango): #argruments are original images and transformed images
    im_henkango = cv2.imread(IMG_henkango) #im_henkangoに変換後の画像を代入する
    hsv = cv2.cvtColor(im_henkango, cv2.COLOR_BGR2HSV)
    hsv_gaus = cv2.GaussianBlur(hsv, (3,3),0)
    hsv_min = np.array([30, 80, 60])
    hsv_max = np.array([255, 255, 255])
    mask = cv2.inRange(hsv_gaus, hsv_min,  hsv_max)
    im_list = np.asarray(mask)
    kernel = np.ones((5,5),np.uint8) #かっこの数字が大きいほど大きいノイズが除去される。
    result = cv2.morphologyEx(im_list, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(filenameIMG[:-4]+'_mask_minusNoize.png',result) #緑のみでノイズがなくなった画像 これがフィルター的な画像となる

    im_rgb = Image.open(IMG_henkango)#緑＋土の画像 デジカメ撮影
    im_a = Image.open(filenameIMG[:-4]+'_mask_minusNoize.png').convert('L')#緑のみでノイズがなくなった画像
    im_rgba = im_rgb.copy()
    im_rgba.putalpha(im_a)
    im_rgba.save(filenameIMG[:-4]+'_mask_minusNoize_alpha.png') #アラビのみの部分が切り出され他は透明になった画像

    im_rgb = Image.open(IR_henkango)#IRの画像
    im_rgb_c = im_rgb.copy()
    im_rgb_c.putalpha(im_a)
    im_rgb_c.save(filenameIR[:-4]+'_alpha.png') #IR画像からアラビのみが切り出された他は透明になった画像

#IR画像上の温度スケールバーから最高温度と最低温度の画像をトリミングするプログラム
#pathにはIR画像のパスをいれる
def scaleBar(path, max_folder, min_folder):
    img = Image.open(path) #画像の取得
    name = os.path.basename(path) #元画像のファイル名をパスら抽出

    max_crop = img.crop((620, 30, 634, 34))
    max_crop.save(max_folder + "/" + str(name)[:-4] + '_max.png')
    min_crop = img.crop((620, 445, 634, 448))
    min_crop.save(min_folder + "/" + str(name)[:-4] + '_min.png')


#グレースケールを測定して保存するプログラム
#pathには画像のパスをいれる
def calcGrey(path):
    im = cv2.imread(path)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray_min = np.array([0])
    gray_max = np.array([254])
    mask = cv2.inRange(gray, gray_min,  gray_max)
    plt.imshow(mask)
    mean_val = cv2.mean(gray,mask=mask)

    return [path, mean_val]


#実行プログラム

#obtain path to image folder
#folder must include both original and IR images
pathToOriginal = input('Enter path to original images: ')
pathToIR = input('Enter path to IR images: ')

coordinate_data = []
coordinate_header = ['originalPath', 'IRPath', 'originalCoordinate', 'IRCoordinate']

temp_data =[]
temp_header = ['path', 'max_temp', 'min_temp']

p =  Path(pathToIR).parent #画像の親ディレクトリを取得
max_folder = os.mkdir(str(p) + '/max_temp')
min_folder = os.mkdir(str(p) + '/min_temp')
max_folder = str(p) + '/max_temp'
min_folder = str(p) + '/min_temp'

print(max_folder)
res = extractCoordinate(pathToOriginal, pathToIR)

#リサイズ
for i in range(len(res[0])):
    resize(res[0][i], res[2][i])
    resize(res[1][i], res[3][i])
    coordinate_data.append([res[0][i], res[1][i], res[2][i], res[3][i]])

IRImages = []

#重ね合わせ
for  i in range(len(res[0])):
    superpose(res[0][i], res[1][i], res[0][i][:-4]+'_henkango.png', res[1][i][:-4]+'_henkango.png')
    IRImages.append(res[1][i])

#スケールバーから画像作成
IRImages = natsorted(IRImages)
for i in range(len(IRImages)):
    scaleBar(IRImages[i], max_folder, min_folder)

#スケールバーの画像からグレースケールを測定
max_im = natsorted(glob.glob(str(max_folder) + '/*'))
min_im = natsorted(glob.glob(str(min_folder) + '/*'))

#スケールバーのmean値の測定とデータセット形成
for i in range(len(max_im)):
    max_grey = calcGrey(max_im[i])
    min_grey = calcGrey(min_im[i])
    data = [max_grey[0], max_grey[1], min_grey[1]]
    temp_data.append(data)

with open('pathAndCoodinate.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(coordinate_header)
    for i in range(len(coordinate_data)):
        writer.writerow(coordinate_data[i])

with open('pathAndTemp.csv', 'w') as c:
    writer = csv.writer(c, lineterminator='\n')
    writer.writerow(temp_header)
    for i in range(len(temp_data)):
        writer.writerow(temp_data[i])
