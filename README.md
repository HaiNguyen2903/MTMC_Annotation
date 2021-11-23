# Running tutorial

## Setup
To install pip dependencies: 
```bash
pip install -r requirements.txt
```

## Resize video
```bash
python resize_video.py --root_dir {path/to/video/dir} --out_dir {path/to/output/dir} --out_shape {resize_shape} --out_fps {out_fps}
```

Where `root_dir` is the directory that contains all videos need to be resized. `out_dir` is the directory that contains all resized videos

## Convert list of MOT ground truth files into one unique MOT ground truth file
```bash
python mot_gt_to_merge_gt.py --gt_dir {path/to/gt/dir} --out_path {path/to/out/gt/file}
```

Where `gt_dir` is the directory that contains list of MOT ground truth files 

The MOT ground truth list should be in order of `[view_1, view_2, view_3, view_4]`, which will be represented as: 

```bash
view_1 | view_2
       | 
-------|--------
       | 
view_3 | view_4
```

## Convert merge json ground truth file (Datumaru format) to seperate MOT ground truth files for each view 
```bash
python merge_gt_to_mot_gt.py --merge_gt {path/to/json/file} --output_dir {path/to/directory/save/output}
```

Where `output_dir` is the directory that contains list of MOT output files, which has the following format 
```bash
output_dir
    |
    |__view_1.txt
    |__view_2.txt
    |__view_3.txt
    |__view_4.txt
```

## Generate video with bounding boxes 
```bash
python visualize_gt --video_path {path/to/original/video} --gt_path {path/to/video/gt/file} --out_path {path/to/save/output/video}
```
