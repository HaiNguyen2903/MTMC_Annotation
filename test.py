import cv2
import os.path as osp
import argparse

parser = argparse.ArgumentParser(description="Arguments for resize \
                                                videos process")
parser.add_argument("--numbers", default=(1,2), nargs="+", type=tuple)

dict = {'view_1': 10, 'view_2': 2}

print(dict['view_{}'.format(1)])