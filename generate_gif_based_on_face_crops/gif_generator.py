import os
from PIL import Image, ImageDraw
from random import randint

IMG_WIDTH = 328
IMG_HEIGHT = 406
SPEED = 60
PERCENTAGES = [40, 17, 18,25]

HEIGHTS_COUNT = 4

def get_area(n):

    h1 = 0
    for i in range(n):
        h1 = h1 + PERCENTAGES[i]

    h2 = h1 + PERCENTAGES[n]

    h1 = int(float(h1) * float(IMG_HEIGHT) / 100.0)
    h2 = int(float(h2) * float(IMG_HEIGHT) / 100.0)

    return (0, int(h1), IMG_WIDTH, int(h2))

def load_images():
    path = os.path.dirname(__file__)
    path = os.path.join(path, "pics")
    files = [os.path.join(path, f) for f in os.listdir(path)]
    files = [f for f in files if os.path.splitext(f)[1].upper() != ".DB"]

    imgs = []
    for f in files:
        img = Image.open(f)
        # resize based on height
        w = int(IMG_HEIGHT / img.size[1] * img.size[0])
        img = img.resize((w, IMG_HEIGHT), Image.ANTIALIAS)
        #img.thumbnail((w, IMG_HEIGHT), Image.ANTIALIAS)
        if w > IMG_WIDTH:
            # neeed to crop the sides of the image, centering it (height is alread correct)
            border = (w - IMG_WIDTH) / 2
            area = (border, 0, w - border, IMG_HEIGHT)
            img = img.crop(area)
        imgs.append(img.copy())

    return imgs


def save_gif(imgs):
    path = os.path.dirname(__file__)
    path_aux = os.path.join(path, "aux_images")
    gif_path = os.path.join(path, "image.gif")

    # create gif frames using random crops
    gif_images = []
    for i in range(len(imgs)):
        img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color = (0, 0, 0))
        for c in range(len(PERCENTAGES)):
            src = imgs[randint(0, len(imgs)-1)]
            region = src.crop(get_area(c))
            img.paste(region, get_area(c))
        gif_images.append(img)

    # Insert full images in random frames of the gif
    for idx, img in enumerate(imgs):
        gif_images.insert(randint(2, len(gif_images)-1), img)

    gif_images[0].save(fp=gif_path, format='GIF', append_images=gif_images[1:],save_all=True, duration=SPEED, loop=0, disposal=2)

    # Save auxiliary images for reference of crop areas
    for idx, img in enumerate(imgs):
        draw = ImageDraw.Draw(img)
        for c in range(len(PERCENTAGES)):
            h = get_area(c)[1]
            draw.line((0, h, IMG_WIDTH, h), fill=255, width=3)
        img.save(fp=os.path.join(path_aux, "img_%d.PNG" % idx))


imgs = load_images()
save_gif(imgs)
print ("Done!")

