import time
import pdb
import console
import PIL
from PIL import Image, ImageFilter
import cclabel as cc
import numpy as np
import manu_pic as mp
import ui

def rescale(im_in, basewidth=100):
    wpercent = (basewidth / float(im_in.size[0]))
    hsize = int((float(im_in.size[1]) * float(wpercent)))
    im_in = im_in.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    return im_in


def count_blobs(thr):
    count = 0
    img = Image.open("sample.jpg")
    img = rescale(img, 800)
    img = img.filter(ImageFilter.BLUR)
    img = img.convert('L')
    img = img.point(lambda p: p > thr and 255)
    labels = cc.run(img)
    sizes = []
    for i, key in enumerate(labels.keys()):
        if len(labels[key][0]) > 10:
            sizes.append(len(labels[key][0]))
    med = np.median(sizes)
    count = np.sum((sizes < 2.5 * med) & (sizes > 0.5 * med))
    img.save("processed.jpg")
    return count, ui.Image("processed.jpg")



def main():
    mp.camera(True)
    console.quicklook('sample.jpg')
    time.sleep(0.3)

    img = Image.open("sample.jpg")

    img = rescale(img, 300)

    img = img.filter(ImageFilter.BLUR)

    img = img.convert('L')
    #im.show()
    img = img.point(lambda p: p > 150 and 255)
    img.show()

    #img.show()

    labels = cc.run(img)

    sizes = []
    for i, key in enumerate(labels.keys()):
        if len(labels[key][0]) > 10:
            sizes.append(len(labels[key][0]))
    med = np.median(sizes)
    count = np.sum((sizes < 2.5 * med) & (sizes > 0.5 * med))
    img.save('processed.jpg')
    print(count)
    return count


if __name__ == '__main__':
    #main()
    main()

