import os
from PIL import Image, ImageDraw
from random import randint

IMG_WIDTH = 328
IMG_HEIGHT = 406

SPEED = 40

def load_images():
    path = os.path.dirname(__file__)
    path = os.path.join(path, "png")
    files = [os.path.join(path, f) for f in os.listdir(path)]
    files = [f for f in files if os.path.splitext(f)[1].upper() != ".DB"]

    imgs = []
    for f in files:
        img = Image.open(f)
        img = img.copy()

        w = int(IMG_HEIGHT / img.size[1] * img.size[0])
        img = img.resize((w, IMG_HEIGHT), Image.ANTIALIAS)
        #img.thumbnail((w, IMG_HEIGHT), Image.ANTIALIAS)
        if w > IMG_WIDTH:
            # neeed to crop the sides of the image, centering it (height is alread correct)
            border = (w - IMG_WIDTH) / 2
            area = (border, 0, w - border, IMG_HEIGHT)
            img = img.crop(area)

        #img = img.convert('RGB')

        imgs.append(img)

    return imgs


def save_gif(imgs):
    path = os.path.dirname(__file__)
    gif_path = os.path.join(path, "image.gif")

    imgs[0].save(fp=gif_path, format='GIF', append_images=imgs[1:],save_all=True, duration=SPEED, loop=0, disposal=2, optimize=True)

imgs = load_images()
save_gif(imgs)
print ("Done!")
