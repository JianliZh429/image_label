import glob

import os


def file_in_dir(directory, extends):
    files = []
    for ext in extends:
        files.extend(glob.glob(os.path.join(directory, ext)))
    return files


def f_name(file_path, without_ext=False):
    fname = file_path.split(os.sep)[-1]
    if not without_ext:
        return fname
    else:
        return fname.split(os.extsep)[0]


def images_in_dir(image_dir):
    return file_in_dir(image_dir, ('*.png', '*.gif', '*.jpg', '*.jpeg'))


def json_in_dir(json_file_dir):
    return file_in_dir(json_file_dir, ['*.json'])
