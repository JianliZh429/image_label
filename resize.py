import argparse

import cv2
import os

from utils import images_in_dir, f_name


def resize(in_dir, out_dir, dsize):
    img_files = images_in_dir(in_dir)

    for img in img_files:
        fname = f_name(img, without_ext=False)
        image_path = os.path.join(out_dir, fname)
        im = cv2.imread(img)
        resized = cv2.resize(im, dsize)
        cv2.imwrite(image_path, resized)
        print('{} done.'.format(img))

    print("All done, {} images.".format(len(img_files)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images_dir", required=True, help="Directories of the images")
    ap.add_argument("-o", "--output_dir", required=True, help="Directories of output")
    ap.add_argument("-s", "--scale", required=True, help="scale to resize")

    args = vars(ap.parse_args())

    images_dir = args['images_dir']
    output_dir = args['output_dir']
    scale = args['scale']
    x, y = scale.split(':')

    resize(images_dir, output_dir, (int(x), int(y)))
