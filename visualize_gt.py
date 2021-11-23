import cv2
import argparse

parser = argparse.ArgumentParser(description="Arguments for generate video \
                                              with bounding boxes from \
                                              original video")
parser.add_argument("--video_path", default="/Users/hainguyen/Documents/deep_learning_projects/mtmc_annotate/annotation_utils/scene3_videos/4125_fullhd.mp4", type=str)
parser.add_argument("--gt_path", default="/Users/hainguyen/Documents/deep_learning_projects/mtmc_annotate/annotation_utils/test_gt/view_1.txt", type=str)
parser.add_argument("--out_path", default="test.mp4", type=str)

args = parser.parse_args()

def compute_color_for_labels(label):

    """
    Simple function that adds fixed color depending on the class
    """
    palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)
    
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)

def gen_dict_gt(gt_path):
    frame_boxes = {}
    with open(gt_path, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line.split(",") for line in lines]

        for line in lines:
            frame_id, obj_id = line[0], line[1]

            bb_left, bb_top = line[2], line[3]
            width, height = line[4], line[5]

            point_x, point_y = line[7], line[8]

            if frame_id not in frame_boxes:
                frame_boxes[frame_id] = {
                    "identities": [obj_id],
                    "bboxes": [(bb_left, bb_top, width, height)],
                    "points": [(point_x, point_y)],
                }

            else:
                frame_boxes[frame_id]["identities"].append(obj_id)
                frame_boxes[frame_id]["bboxes"].append((bb_left, bb_top,
                                                        width, height))
                frame_boxes[frame_id]["points"].append((point_x, point_y))

    return frame_boxes

def draw_boxes(img: str, bbox: list, identities=None, offset=(0, 0)):
    for i, box in enumerate(bbox):
        # x1, y1, x2, y2 = [int(float(i)) for i in box]

        x1, y1, w, h = [int(float(i)) for i in box]
        x2, y2 = x1 + w, y1 + h

        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        id = int(identities[i]) if identities is not None else 0
        color = compute_color_for_labels(id)
        label = "{}{:d}".format("", id)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2, 2)[0]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
        cv2.rectangle(
            img, (x1, y1), (x1 + t_size[0] + 3, y1 + t_size[1] + 4), color, -1
        )
        cv2.putText(
            img,
            label,
            (x1, y1 + t_size[1] + 4),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            [255, 255, 255],
            2,
        )
    return img

def get_view_with_gt(video_path, gt_path, out_path): 
    cap= cv2.VideoCapture(video_path)

    frame_idx = 1

    width, height = 1920, 1080

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 5
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
    gt_dict = gen_dict_gt(gt_path)

    while(cap.isOpened()):
        ret, frame = cap.read()

        if ret == False:
            break

        # gt_dict = gen_dict_gt(gt_path)

        if str(frame_idx) in gt_dict:
            draw_boxes(frame, bbox=gt_dict[str(frame_idx)]["bboxes"], 
                        identities=gt_dict[str(frame_idx)]["identities"])

        # sychrone time
        if int(frame_idx) > 3:
            out.write(frame)
        
        # cv2.imwrite(os.path.join(out_folder, str(idx) + '.jpg'), frame)
        frame_idx += 1
    
    cap.release()

    out.release()

    cv2.destroyAllWindows()

get_view_with_gt(args.video_path, args.gt_path, args.out_path)