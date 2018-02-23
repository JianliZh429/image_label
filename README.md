# image_label
A tool to help label images

# How to use

```
$python cv2_label.py --i $images_dir -o $output_dir
```

## keyboard shortcut
- `n`: go to next image
- `c`: abort
- `esc`: stop
- `backspace`: cancel the latest drawn rectangle

Use mouse to draw rectangles for labeled region, mouse down to decide the first point of a
rectangle, mouse up to decide the second point of the rectangle

## merge json file into one
Sometimes you need a json file with all labeled json
```
$python merge_json_file.py $json_files_dir
```
This tool will merge the json files in a directory into one, merged.json.