import os
import glob
from PIL import Image
import PIL
import cv2
import numpy as np

def saveimage(path_label, path_original, dest_L, dest_O, identificador, cont =0):

    imgL = cv2.imread(path_label, cv2.IMREAD_GRAYSCALE)
    title_L = dest_L + str(identificador) + '.png'
    imgO = cv2.imread(path_original, cv2.IMREAD_COLOR)
    img_L, img_O = modifycolor(imgL, cont, imgO)
    title_O = dest_O + str(identificador) + '.png'
    cv2.imwrite(title_L, img_L)
    cv2.imwrite(title_O, img_O)
    identificador = identificador + 1
    title_L = dest_L + str(identificador) + '.png'
    title_O = dest_O + str(identificador) + '.png'
    cv2.imwrite(title_L, img_L)
    imgO = cv2.imread(path_original, cv2.IMREAD_COLOR)
    cv2.imwrite(title_O, imgO)

def modifycolor(picture, cont, O_picture):
    width, height =  np.shape(picture)
    fondo_Img = fondo()
    #print("fondo: ", np.shape(fondo_Img))
    #print("imagen: ", np.shape(O_picture))
    # Process every pixel
    for x in range(width):
        for y in range(height):
            current_color = picture[x][y]
            if current_color < 255:
                picture[x][y] = cont
            else:
                O_picture[x][y][0] = fondo_Img[x][y][0]
                O_picture[x][y][1] = fondo_Img[x][y][1]
                O_picture[x][y][2] = fondo_Img[x][y][2]
    return picture, O_picture


def rezise(pathImg, basewidth = 1080):
    img = Image.open(pathImg)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    newPath = pathImg.split('pbm')
    img.save(pathImg)

def fondo ():
    lista_fondos = sorted(glob.glob('../Dataset/background/*.jpg'))
    Num = np.random.randint(len(lista_fondos))
    rezise(lista_fondos[Num], 1420)
    #print(lista_fondos[Num])
    image = cv2.imread(lista_fondos[Num] , cv2.IMREAD_COLOR)
    return image


list = []
cont = 0
path = '../Dataset/Original_Dataset/'
for x in os.walk(path):
    if cont == 0:
        list.append(x)
        cont = cont + 1
Carpetas = list[0][1]

identificador = 0
cont = 0
for b in range(len(Carpetas)):
    lista_Datos = sorted(glob.glob(path + Carpetas[b] + '/*.jpg'))
    for i in range(len(lista_Datos)):
        temp = lista_Datos[i].split("/")
        label = temp[0] + "/" + temp[1] + "/" + temp[2] + "/" + temp[3] + '/masks/' + temp[4].split(".")[0] + "_mask.pbm"
        #print("------------------------------------------")
        #print(label)
        #print(lista_Datos[i])
        rezise(lista_Datos[i])
        rezise(label)
        num = np.random.rand()
        if (num > 0.3):
            saveimage(label, lista_Datos[i], '../Dataset/Split2/train/labels/',
                      '../Dataset/Split2/train/images/', identificador, cont)
            identificador = identificador + 2
        elif (num > 0.15):
            saveimage(label, lista_Datos[i], '../Dataset/Split2/test/labels/',
                      '../Dataset/Split2/test/images/', identificador, cont)
            identificador = identificador + 2
        else:
            saveimage(label, lista_Datos[i], '../Dataset/Split2/valid/labels/',
                      '../Dataset/Split2/valid/images/', identificador, cont)
            identificador = identificador + 2


    cont = cont + 1
    print("------------------------------------------")
    print("Cambio a clase: ", cont)
print("------------------------------------------")
print("Orden clases: ", Carpetas)

