# import the necessary packages
import argparse
import json

import cv2
import os

from utils import images_in_dir

ref_pnt = []
drawing = False
cropping = False
rectangles = []
image = None
im = None


def click_and_crop(event, x, y, flags, param):
    global ref_pnt, drawing, image, im
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_pnt = [(x, y)]
        drawing = True
        im = image.copy()
    elif event == cv2.EVENT_MOUSEMOVE and drawing is True:
        copied = im.copy()
        cv2.rectangle(copied, ref_pnt[0], (x, y), (0, 0, 255), 1)
        image = copied

    elif event == cv2.EVENT_LBUTTONUP and drawing is True:
        drawing = False
        ref_pnt.append((x, y))
        (x1, y1) = ref_pnt[0]
        (x2, y2) = ref_pnt[1]
        if x2 - x1 > 1 and y2 - y1 > 1:
            rectangles.append({
                'x1': x1,
                'x2': x2,
                'y1': y1,
                'y2': y2
            })
            _update_image()


def _next():
    im_file = next(images)
    return cv2.imread(im_file), im_file


def _create_image_json():
    f_name = img_file.split(os.sep)[-1]
    f_name = f_name.split('.')[0]
    out = os.path.join(output_dir, '{}.json'.format(f_name))
    print(out)
    with open(out, mode='w', encoding='utf-8') as f:
        j = {
            "image_path": img_file,
            "rects": rectangles
        }
        json.dump(j, f)


def _save_json():
    global rectangles
    if rectangles:
        print("Rects of {}: {}".format(img_file, rectangles))
        _create_image_json()
        rectangles = []


def _update_image():
    cloned = im.copy()
    for r in rectangles:
        cv2.rectangle(cloned, (r['x1'], r['y1']), (r['x2'], r['y2']), (0, 0, 255), 2)
    global image
    image = cloned


def _save_image():
    f_name = img_file.split(os.sep)[-1]
    out = os.path.join(output_dir, '{}.png'.format(f_name))
    cv2.imwrite(out, image)


if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images_dir", required=True, help="Directories of the images")
    ap.add_argument("-o", "--output_dir", required=True, help="Directories of output")
    args = vars(ap.parse_args())

    images_dir = args['images_dir']
    output_dir = args['output_dir']

    images = iter(images_in_dir(images_dir))

    cv2.namedWindow("Label", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Label", click_and_crop)
    image, img_file = _next()

    while True:
        try:
            cv2.setWindowTitle("Label", img_file)
            cv2.imshow("Label", image)
        except StopIteration as e:
            _save_json()
            _save_image()
            break

        key = cv2.waitKey(1) & 0xFF
        if key == ord("n"):
            _save_json()
            _save_image()
            image, img_file = _next()
        # if the 'c' key is pressed, break from the loop
        elif key == 8:
            if rectangles:
                rectangles.pop()
                _update_image()
        elif key == ord("c"):
            _save_json()
            _save_image()
            break

    # close all open windows
    cv2.destroyAllWindows()
