import glob

import os


def images_in_dir(image_dir):
    images = []
    for ext in ('*.png', '*.gif', '*.jpg', '*.jpeg'):
        images.extend(glob.glob(os.path.join(image_dir, ext)))

    return images
