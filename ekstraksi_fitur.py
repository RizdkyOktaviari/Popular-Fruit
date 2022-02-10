import cv2
import numpy as np
from numpy.core.fromnumeric import mean
from numpy.lib.function_base import angle
import math
from scipy import stats
from skimage.feature import greycomatrix, greycoprops
import xlsxwriter as xls
import os

book = xls.Workbook('F:/Kampus/Workshop Citra dan Cerdas/data_fitur.xlsx')
sheet = book.add_worksheet()
sheet.write(0, 0, 'File')

column = 1

# glcm_feature = ['contrast', 'dissimilarity', 'homogeneity', 'ASM', 'energy', 'correlation']
# angle = [0, 45, 90, 135]
# for i in range(len(glcm_feature)):
#     for j in range(len(angle)):
#         sheet.write(0, column, glcm_feature[i] + '_' + str(angle[j]))
#         column += 1

shape_feature = ['luas','keliling','metric']
for i in range(len(shape_feature)):
    sheet.write(0, column, shape_feature[i])
    column += 1

# # fitur warna hsv
# hsv_feature = ['hue', 'saturation', 'value']
# for i in range(len(hsv_feature)):
#     sheet.write(0, column, hsv_feature[i])
#     column += 1

# fitur warna rgb
hsv_feature = ['red', 'green', 'blue']
for i in range(len(hsv_feature)):
    sheet.write(0, column, hsv_feature[i])
    column += 1

row = 1
path_dataset = 'F:/Kampus/Workshop Citra dan Cerdas/FruitsDB'


for folder in os.listdir(path_dataset):
    sub_folder_files = os.listdir(os.path.join(path_dataset, folder))
    len_sub_folder = len(sub_folder_files)
    for i, filename in enumerate(sub_folder_files):
        column = 0
        print(filename)
        sheet.write(row, column, filename)
        column += 1

        # preprosesing citra
        img = cv2.imread(os.path.join(path_dataset, folder, filename))
        img = cv2.resize(img, (500, 500))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ret, mg = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
        # mg = cv2.dilate(mg.copy(), None, iterations=1)
        # mg = cv2.erode(mg.copy(), None, iterations=15)

        blurred = cv2.GaussianBlur(gray, (15, 15), 0)
        cany = cv2.Canny(blurred, 0, 100)

        b, g, r = cv2.split(img)
        rgba = [b,g,r,cany]
        dst = cv2.merge(rgba, 4)

        contours, hierarchy = cv2.findContours(cany, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        select = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(select)

        png = dst[y:y+h, x:x+w]

        png_gray = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
        ret, mg = cv2.threshold(png_gray, 40, 255, cv2.THRESH_BINARY_INV)

        # cany = cv2.Canny(png, 100, 200)

        grayscale = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)
        # grayscale_gabor = cv2.cvtColor(png, cv2.COLOR_BGR2GRAY)

        # g_kernel = cv2.getGaborKernel((23, 23), 8.0, 3*np.pi/4, 10.0, 0.5, 0, ktype=cv2.CV_32F)
        # filtered_img = cv2.filter2D(grayscale_gabor, cv2.CV_8UC3, g_kernel)

        # glcm
        # distance = [5]
        # angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        # level = 256
        # symetric = True
        # normed = True

        # glcm = greycomatrix(grayscale, distance, angles, level, symmetric=symetric, normed=normed)

        # glcm_props = [property for name in glcm_feature for property in greycoprops(glcm, name)[0]]
        # for item in glcm_props:
        #     sheet.write(row, column, item)
        #     column += 1
        
        # fitur bentuk
        # dimensions = png.shape
        # height = png.shape[0]
        # width = png.shape[1]
        # mayor = max(height, width)
        # minor = min(height, width)
        # eccentricity = math.sqrt(1 - ((minor*minor) / (mayor*mayor)))

        # fitur metric
        height1=img.shape[0]
        width1=img.shape[1]
        height2=png.shape[0]
        width2=png.shape[1]

        blurred2 = cv2.GaussianBlur(gray, (15, 15), 0)
        edge = cv2.Canny(blurred2, 0, 100)

        k=0
        keliling = 0
        while k < height1:
            j=0
            while j < width1:
                if edge[k][j] == 255:
                    keliling += 1
                j += 1
            k += 1
        
        k = 0

        luas = 0
        while k < height2:
            j = 0
            while j < width2:
                if mg[k][j] == 0:
                    luas += 1
                j += 1
            k += 1
        
        metric = (4*math.pi*luas)/(keliling*keliling)
        shape_props = [luas,keliling, metric]
        for item in shape_props:
            sheet.write(row, column, item)
            column += 1

        # # fitur warna hsv
        # hsv = cv2.cvtColor(png, cv2.COLOR_BGR2HSV)
        # height = hsv.shape[0]
        # width = hsv.shape[1]
        # H = hsv[:, :, 0]
        # S = hsv[:, :, 1]
        # V = hsv[:, :, 2]

        # hue = np.reshape(H, (1, height*width))
        # mode_hue = stats.mode(hue)[0][0]
        # if int(mode_hue[0]) == 0:
        #     mode_hue = np.mean(H)
        # else:
        #     mode_hue = int(mode_hue[0])
        
        # mean_s = np.mean(S)
        # mean_v = np.mean(V)

        # color_props = [mode_hue, mean_s, mean_v]
        # for item in color_props:
        #     sheet.write(row, column, item)
        #     column += 1
        
        # fitur warna rgb
        height = png.shape[0]
        width = png.shape[1]
        R = png[:, :, 0]
        G = png[:, :, 1]
        B = png[:, :, 2]

        mean_r = np.mean(R)
        mean_g = np.mean(G)
        mean_b = np.mean(B)
        # mean_r = R/R+G+B)
        # mean_g = G/R+G+B)
        # mean_b = B/R+G+B

        color_props = [mean_r, mean_g, mean_b]
        for item in color_props:
            sheet.write(row, column, item)
            column += 1
        row+=1

book.close()


