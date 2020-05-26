# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import os
from PIL import Image, ImageDraw
from random import randint
import json

IMG_WIDTH = 328
IMG_HEIGHT = 406

debug = False

def load_image(img_file):
    print ("Loading: ", os.path.basename(img_file))
    img = Image.open(img_file)
    w = int(IMG_HEIGHT / img.size[1] * img.size[0])
    img = img.resize((w, IMG_HEIGHT), Image.ANTIALIAS)
    #img.thumbnail((w, IMG_HEIGHT), Image.ANTIALIAS)
    if w > IMG_WIDTH:
        # neeed to crop the sides of the image, centering it (height is alread correct)
        border = (w - IMG_WIDTH) / 2
        area = (border, 0, w - border, IMG_HEIGHT)
        img = img.crop(area)

    img = img.convert('RGB')
    img = np.array(img)
    img = img[:, :, ::-1].copy()

    parts = detect_face_parts(img)
    #slices =  convert_parts_to_slices(parts, img.size[1])

    result = {
        'name': os.path.basename(img_file),
        'img': img,
        'parts': parts
        #'slices':slices
    }

    return result

#b = load_image(r"D:\git_hub\aporto\python.git\face_mixer_photos_pcg\pics\mediciner.png")
#d = load_image(r"D:\git_hub\aporto\python.git\face_mixer_photos_pcg\pics\daniel.png")

def main():
    path = os.path.dirname(__file__)
    pics_path = os.path.join(path, "pics")
    files = [os.path.join(pics_path, f) for f in os.listdir(pics_path)]
    files = [f for f in files if os.path.splitext(f)[1].upper() != ".DB"]

    imgs = []
    for f in files:
        img = load_image(f)
        if len(img['slices']) > 0:
            imgs.append(img)

    for dst in imgs:
        for s in dst['slices']:
            dpart = dst['slices'][s]

            spart = None
            while spart is None:
                # find a random image that has the same part detected as the part we
                # are drawing now
                src = imgs[randint(0, len(imgs)-1)]
                try:
                    spart = src['slices'][s]
                except:
                    spart = None

            scrop = src['img'].crop(spart)
            if dpart[2]-dpart[0] <= 0 or dpart[3]-dpart[1] <= 0:
                print ("erro")
                print (dst)
                continue

            scrop = scrop.resize((dpart[2]-dpart[0], dpart[3]-dpart[1]),  Image.ANTIALIAS)
            dst['img'].paste(scrop, dpart)

        filename = os.path.join(os.path.join(path, "dest"), dst['name'])
        dst['img'].save(filename)


def mixImages(imgNameSrc, imgNameDst):
    imgSrc = cv2.imread(os.path.join(r'D:\git_hub\aporto\python.git\face_mixer_photos_pcg_v2\pics', imgNameSrc))
    imgDst = cv2.imread(os.path.join(r'D:\git_hub\aporto\python.git\face_mixer_photos_pcg_v2\pics', imgNameDst))

    imgDstOriginal = cv2.imread(os.path.join(r'D:\git_hub\aporto\python.git\face_mixer_photos_pcg_v2\pics', imgNameDst))

    srcH, srcW, channels = imgSrc.shape
    dstH, dstW, channels = imgSrc.shape

    factorW = float(srcW) / float(dstW)
    factorH = float(srcH) / float(dstH)

    imgSrc = imgSrc / 255
    imgDst = imgDst / 255
    print ("%s -> %s" % (imgNameSrc, imgNameDst))

    for part in imgs[imgNameSrc]['parts']:
        if not part in imgs[imgNameDst]['parts']:
            continue

        #if part != 'left_eye':
        #    continue


        if part in ['jaw', 'nose', 'inner_mouth', 'left_eyebrow', 'right_eyebrow']:
            continue

        #print ("\t%s -> %s: %s" % (imgNameSrc, imgNameDst, part))

        px = imgs[imgNameSrc]['parts'][part]['rect'][0]
        py = imgs[imgNameSrc]['parts'][part]['rect'][1]
        pw = imgs[imgNameSrc]['parts'][part]['rect'][2] - px
        ph = imgs[imgNameSrc]['parts'][part]['rect'][3] - py

        srcROI = imgSrc[py:py+ph, px:px+pw]

        # get image part from src
        part_pts = [[p[0]-px, p[1]-py] for p in imgs[imgNameSrc]['parts'][part]['shape']]
        part_pts = np.array(part_pts, np.int32)
        part_pts = part_pts.reshape((-1,1,2))
        #cv2.polylines(imgSrc,[pts],True,(0,255,255))

        mask = np.zeros((ph, pw, 3), np.float)

        cv2.fillConvexPoly(mask,part_pts,(255,255,255))

        mask = cv2.GaussianBlur(mask,(11,11),0)
        mask = mask / 255

        srcPart = srcROI * mask
        srcPart = srcPart.copy()

        # get image shape from dst
        dx = imgs[imgNameDst]['parts'][part]['rect'][0]
        dy = imgs[imgNameDst]['parts'][part]['rect'][1]
        dw = imgs[imgNameDst]['parts'][part]['rect'][2] - dx
        dh = imgs[imgNameDst]['parts'][part]['rect'][3] - dy


        partFactorW = float(dw) / float(pw)
        partFactorH = float(dh) / float(ph)
        mask = cv2.resize(mask, None, fx=partFactorW, fy=partFactorH, interpolation=cv2.INTER_AREA)
        srcPart = cv2.resize(srcPart, None, fx=partFactorW, fy=partFactorH, interpolation=cv2.INTER_AREA)


        #imgDstZero = np.zeros((dstH, dstW, 3), np.uint8)
        imgDstROI = imgDst[dy:dy+dh, dx:dx+dw]
        imgDst[dy:dy+dh, dx:dx+dw] = imgDst[dy:dy+dh, dx:dx+dw] * (1-mask) + srcPart * mask

    if debug:
        cv2.imshow("image", imgSrc)
        cv2.imshow("srcPart", srcPart)
        cv2.imshow("mask", mask)
        cv2.imshow("dst", imgDst)
        cv2.imshow("dst_original", imgDstOriginal)
        cv2.waitKey(0)

    imgDst = imgDst * 256
    dstName = os.path.splitext(imgNameSrc)[0] + "_" + os.path.splitext(imgNameDst)[0] + ".jpg"
    cv2.imwrite('output/' + dstName, imgDst)


with open("image_data.json", "r") as f:
    imgs = json.load(f)

if debug:
    imgNameSrc = 'aline.png'
    imgNameDst= 'homero.png'
    mixImages(imgNameSrc, imgNameDst)
else:
    for imgNameSrc in imgs:
        for imgNameDst in imgs:
            if imgNameSrc != imgNameDst:
                mixImages(imgNameSrc, imgNameDst)


"""
imgSrc = cv2.imread(os.path.join(r'D:\git_hub\aporto\python.git\face_mixer_photos_pcg_v2\pics', imgNameSrc))


height, width, channels = imgSrc.shape
mask = np.zeros((height, width, 3), np.float)
#mask = cv2.cvtColor(mask, cv2.COLOR_RGB2BGR)

for part in imgs[imgNameSrc]['parts']:
    if part in ['jaw', 'nose']:
        continue
    pts = np.array(imgs[imgNameSrc]['parts'][part]['shape'], np.int32)
    pts = pts.reshape((-1,1,2))
    #cv2.polylines(imgSrc,[pts],True,(0,255,255))
    cv2.fillConvexPoly(mask,pts,(255,255,255))

mask = cv2.GaussianBlur(mask,(35,35),0)
mask = mask / 255
imgSrc = imgSrc / 255
imgDst = imgSrc * mask

#imgDst = np.zeros((height, width, 3), np.uint8)
#imgSrc.copyTo(imgDst, mask_image);
#imgDst = cv2.bitwise_and(imgSrc, mask)

cv2.imshow("image", imgSrc)
cv2.imshow("dst", imgDst)
cv2.imshow("mask", mask)
cv2.waitKey(0)
"""
