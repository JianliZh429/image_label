# import the necessary packages
import argparse
import json

import cv2
import os

from utils import images_in_dir

ref_pnt = []
drawing = False
cropping = False
rects = []

im = None


def click_and_crop(event, x, y, flags, param):
    global ref_pnt, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_pnt = [(x, y)]
        drawing = True
        global im
        im = image.copy()
    elif event == cv2.EVENT_MOUSEMOVE and drawing is True:
        cv2.rectangle(im, ref_pnt[0], (x, y), (0, 0, 255), 1)
        cv2.imshow("Label", im)
    elif event == cv2.EVENT_LBUTTONUP and drawing is True:
        drawing = False
        ref_pnt.append((x, y))
        (x1, y1) = ref_pnt[0]
        (x2, y2) = ref_pnt[1]
        if x2 - x1 > 1 and y2 - y1 > 1:
            rects.append({
                'x1': x1,
                'x2': x2,
                'y1': y1,
                'y2': y2
            })
            _show_image()


def _next():
    img_file = next(images)
    return cv2.imread(img_file), img_file


def _create_image_json():
    f_name = img_file.split(os.sep)[-1]
    f_name = f_name.split('.')[0]
    out = os.path.join(output_dir, '{}.json'.format(f_name))
    print(out)
    with open(out, mode='w', encoding='utf-8') as f:
        j = {
            "rects": rects,
            "image_path": img_file
        }
        json.dump(j, f)


def _save_json():
    global rects
    if rects:
        print("Rects of {}: {}".format(img_file, rects))
        _create_image_json()
        rects = []


def _show_image():
    cloned = image.copy()
    for r in rects:
        cv2.rectangle(cloned, (r['x1'], r['y1']), (r['x2'], r['y2']), (0, 0, 255), 2)
    cv2.imshow("Label", cloned)


if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images_dir", required=True, help="Directories of the images")
    ap.add_argument("-o", "--output_dir", required=True, help="Directories of output")
    args = vars(ap.parse_args())

    images_dir = args['images_dir']
    output_dir = args['output_dir']

    images = iter(images_in_dir(images_dir))

    cv2.namedWindow("Label")
    cv2.setMouseCallback("Label", click_and_crop)

    image, img_file = _next()
    while True:
        try:
            _show_image()
        except StopIteration as e:
            _save_json()
            break

        key = cv2.waitKey(1) & 0xFF
        if key == ord("n"):
            _save_json()
            image, img_file = _next()
        # if the 'c' key is pressed, break from the loop
        elif key == 8:
            if rects:
                rects.pop()
                _show_image()
        elif key == ord("c"):
            _save_json()
            break

    cv2.waitKey(0)

    # close all open windows
    cv2.destroyAllWindows()
