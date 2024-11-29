import cv2
import numpy as np

roi_bad_pixel_number = 500  # the number of pixel where 3 values are zero in RGB channel on ROI image
roi_aspect_ratio_threshold = 200  # the passable aspect ratio threshold of ROI image
cupped_pose_threshold = 3  # this value determines if hand is cupped or not
frame_margin = 300  # the extra marine size of the frame inputted into Google Mediapipe Graph (this value must be a
# multiple of two)
roi_size_threshold = 0.23

def img_crop(img_original, x2, x1, y2, y1, label):
    
    h, w, _ = img_original.shape
    img = np.zeros((h + 20, w + 20, 3), np.uint8)
    img[10:-10, 10:-10, :] = img_original

    if label == "Left":
        v1 = np.array([x2, y2])
        v2 = np.array([x1, y1])
    else:
        v2 = np.array([x2, y2])
        v1 = np.array([x1, y1])
    
    theta = np.arctan2((v2 - v1)[1], (v2 - v1)[0]) * 180 / np.pi
    R = cv2.getRotationMatrix2D(tuple([int(v2[0]), int(v2[1])]), theta, 1)
    
    v1 = (R[:, :2] @ v1 + R[:, -1]).astype(int)
    v2 = (R[:, :2] @ v2 + R[:, -1]).astype(int)
    img_r = cv2.warpAffine(img, R, (w, h))
    
    if 1:
        ux = int(v1[0] - (v2 - v1)[0] * 0.05)
        uy = int(v1[1] + (v2 - v1)[0] * 0.05)
        lx = int(v2[0] + (v2 - v1)[0] * 0.05)
        ly = int(v2[1] + (v2 - v1)[0] * 1)
    else:
        ux = int(v1[0] - (v2 - v1)[0] * 0.1)
        uy = int(v1[1] + (v2 - v1)[0] * 0.1)
        lx = int(v2[0] + (v2 - v1)[0] * 0.1)
        ly = int(v2[1] + (v2 - v1)[0] * 1.2)

    # delta_y is movement value in y ward
    delta_y = (ly - uy) * 0.15

    ly = int(ly - delta_y)
    uy = int(uy - delta_y)

    delta_x = (lx - ux) * 0.01
    lx = int(lx + delta_x)
    ux = int(ux + delta_x)
    
    if label == "Right":
        delta_x = (lx - ux) * 0.05
        lx = int(lx + delta_x)
        ux = int(ux + delta_x)
    # roi = img_r
    roi = img_r[uy:ly, ux:lx]
    if roi.shape[0] == 0 or roi.shape[1] == 0:
        print("error 1")
        return None, 3
    if abs(roi.shape[0] - roi.shape[1]) > roi_aspect_ratio_threshold:
        print("error 2", abs(roi.shape[0] - roi.shape[1]))
        return None, 4
    if roi.shape[1] / w < roi_size_threshold:
        print("error 3", roi.shape[1] / w)
        return None, 7

    n_zeros = np.count_nonzero(roi == 0)
    # if n_zeros > roi_bad_pixel_number:
        # print("error 4", n_zeros)
        # return None, 5
    return roi, 0
            
def get_roi(path, hand_type, x1, y1, x2, y2):
    img = cv2.imread(path)
    
    if hand_type == 0:
        label = "Left"
    else:
        label = "Right"
    roi, _ = img_crop(img, x1, x2, y1, y2, label)
    cv2.imwrite('test.jpg', roi)
    return roi
