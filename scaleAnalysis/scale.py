import os
import csv
import glob

from natsort import natsorted

import numpy as np
from PIL import ImageGrab, Image, ImageFilter, ImageDraw
from matplotlib import image
import matplotlib.pyplot as plt
import cv2

"""
・matplotlibでスクショから最高温度と最低温度の座標を打ち込んでトリミングして新しい画像を作成
・画像名を元のアラビ画像と対応させる（IMG_5555_max_temp.pngなど）
・画像のグレースケールを解析してcsvに保存
・作成したファイルを新規作成したフォルダに挿入
・

"""
