import cv2
import os 
import os.path as osp
import argparse
import glob

parser = argparse.ArgumentParser(description="Arguments for resize \
                                                videos process")
parser.add_argument("--root_dir", default="/Users/hainguyen/Documents/deep_learning_projects/mtmc_annotate/generate_top_view/sence3/", type=str)
parser.add_argument("--out_dir", default="/Users/hainguyen/Documents/deep_learning_projects/mtmc_annotate/generate_top_view/sence3/'", type=str)

parser.add_argument("--out_shape", default=(1920, 1080), type=tuple)
parser.add_argument("--out_fps", default=5, type=int)

args = parser.parse_args()

def resize_videos(root_dir, out_shape, out_fps, out_dir):
    # for video in os.listdir(root_dir):
    for video in glob.glob('{}/*.mp4'.format(root_dir)):

        name = osp.basename(video)[:-4]

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        cap = cv2.VideoCapture(video)

        out_path = osp.join(out_dir, '{}_fullhd.mp4'.format(name))

        out = cv2.VideoWriter(out_path, fourcc, out_fps, out_shape)

        while True:
            ret, frame = cap.read()
            if ret == True:
                b = cv2.resize(frame, out_shape, fx=0, fy=0, 
                                interpolation = cv2.INTER_CUBIC)
                out.write(b)
            else:
                break

        cap.release()
        out.release()

        cv2.destroyAllWindows()

resize_videos(root_dir = args.root_dir,
              out_shape = args.out_shape,
              out_fps = args.out_fps,
              out_dir = args.out_dir)