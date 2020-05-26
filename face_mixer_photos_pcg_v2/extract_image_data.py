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

def detect_face_parts(image):
    # construct the argument parser and parse the arguments
    '''ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=True,
    	help="path to facial landmark predictor")
    ap.add_argument("-i", "--image", required=True,
    	help="path to input image")
    args = vars(ap.parse_args())
    '''

    parts = {}
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    # load the input image, resize it, and convert it to grayscale
    #image = cv2.imread(pil_image)
    #image = np.array(pil_image)
    # Convert RGB to BGR
    #open_cv_image = open_cv_image[:, :, ::-1].copy()
    #image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale image
    rects = detector(gray, 1)
    # loop over the face detections
    for (i, rect) in enumerate(rects):
    	# determine the facial landmarks for the face region, then
    	# convert the landmark (x, y)-coordinates to a NumPy array
    	shape = predictor(gray, rect)
    	shape = face_utils.shape_to_np(shape)
    	# loop over the face parts individually
    	for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
            pos = cv2.boundingRect(np.array([shape[i:j]]))
            parts[name] = {
                'shape': [[int(p[0]), int(p[1])] for p in shape[i:j]],
                'rect': (pos[0], pos[1], pos[0] + pos[2], pos[1] + pos[3])
            }

    		# clone the original image so we can draw on it, then
    		# display the name of the face part on the image
    		#clone = image.copy()
    		#cv2.putText(clone, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
    		#	0.7, (0, 0, 255), 2)
    		# loop over the subset of facial landmarks, drawing the
    		# specific face part
    		#for (x, y) in shape[i:j]:
    		#	cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)


            # extract the ROI of the face region as a separate image
            '''
    		(x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
    		roi = image[y:y + h, x:x + w]
    		roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)
    		# show the particular face part
    		cv2.imshow("ROI", roi)
    		cv2.imshow("Image", clone)
    		cv2.waitKey(0)
            '''

    	# visualize all facial landmarks with a transparent overlay

    	#output = face_utils.visualize_facial_landmarks(image, shape)
    	#cv2.imshow("Image", output)
    	#cv2.waitKey(0)

    return parts

def convert_parts_to_slices(parts, w):
    slices = {}
    try:
        if parts['left_eye'][1] < parts['right_eye'][1]:
            y1a = parts['left_eye'][1]
        else:
            y1a = parts['right_eye'][1]
        if parts['left_eye'][3] > parts['right_eye'][3]:
            y2a = parts['left_eye'][3]
        else:
            y2a = parts['right_eye'][3]
    except:
        y1a = w * 2
        y2a = 0

    try:
        if parts['left_eyebrow'][1] < parts['right_eyebrow'][1]:
            y1b = parts['left_eyebrow'][1]
        else:
            y1b = parts['right_eyebrow'][1]
        if parts['left_eyebrow'][3] > parts['right_eyebrow'][3]:
            y2b = parts['left_eyebrow'][3]
        else:
            y2b = parts['right_eyebrow'][3]
        #slices['eye_brow'] = (0, y1, w, y2)
    except:
        y1b = w * 2
        y2b = 0

    if not(y2a == 0 and y2b == 0):
        if y1a > y1b:
            y1a = y1b
        if y2b > y2a:
            y2a = y2b
        slices['eye'] = (0, y1a, w, y2a)

    try:
        slices['mouth'] = (0, parts['mouth'][1], w, parts['mouth'][3])
    except:
        pass
    #slices['nose'] = (0, parts['nose'][1], w, parts['nose'][3])
    try:
        slices['nose'] = parts['nose']
    except:
        pass

    return slices

def load_image(img_file):
    print ("Loading: ", os.path.basename(img_file))
    img = Image.open(img_file)
    """
    w = int(IMG_HEIGHT / img.size[1] * img.size[0])
    img = img.resize((w, IMG_HEIGHT), Image.ANTIALIAS)
    #img.thumbnail((w, IMG_HEIGHT), Image.ANTIALIAS)
    if w > IMG_WIDTH:
        # neeed to crop the sides of the image, centering it (height is alread correct)
        border = (w - IMG_WIDTH) / 2
        area = (border, 0, w - border, IMG_HEIGHT)
        img = img.crop(area)
    """
    img = img.convert('RGB')
    img = np.array(img)
    img = img[:, :, ::-1].copy()

    parts = detect_face_parts(img)
    #slices =  convert_parts_to_slices(parts, img.size[1])

    result = {
        #'name': os.path.basename(img_file),
        #'img': img,
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

    imgs = {}
    for f in files:
        img = load_image(f)
        if len(img['parts']) > 0:
            imgs[os.path.basename(f)] = img

    with open ("image_data.json", "w") as f:
        s = json.dumps(imgs, indent=4, sort_keys=True)
        f.write(s)

main()