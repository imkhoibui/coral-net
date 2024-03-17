import cv2
import argparse

def extract_frames(vid_path: str, img_path: str):
    """
        This function extracts frames from the given video paths

        ----------
        Parameters:
        - vid_path (str):
        - img_path (str):

        ----------
        Returns:

    """
    frame_count = 0
    capture = cv2.VideoCapture(vid_path)
    frame_end = False
    fps = capture.get(cv2.CAP_POP)
    while not frame_end:
        success, img = capture.read()
        if not success:
            continue
        cv2.imwrite(f"{img_path}/frame_{frame_count:04d}.jpg", img)
        frame_count += 1
        if frame_count == capture.get(cv2.)

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--vid_path", help="path to video")
    a.add_argument("--img_path", help="path to image extracted")
    args = a.parse_args()
    extract_frames(args.vid_path, args.img_path)

