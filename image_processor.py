# -*- coding: utf-8 -*-
"""
TO RUN:
python image_processor.py
-input_path './files_for_test_pratique/salads.png'
-shrink_or_stretch:  1 - stretch ; 2 - shrink

@author: ajulyav@gmail.com
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import argparse


def segmentImg(inPath):
    
    """
    This function performs color-based segmentation in the HSV space
    :param inpath: path to the png image (salads.png)
    :return img: 3-D array of the original image
    """
    
    # read the image
    try: 
        img = cv.imread(inPath)
    except FileNotFoundError:
        print("Make sure that the file is in the folder.")
    
    # convert it to HSV
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    # set low and high bound values for H, S, V
    low = np.array([9, 3, 77])
    high = np.array([107, 255, 255])
    
    # get the mask in the low < range < high 
    mask = cv.inRange(hsv, low, high)
    
    # apply mask on the image
    segmentRes = cv.bitwise_and(img, img, mask= mask)
    
    # simple plot part
    plt.imshow(segmentRes)
    plt. axis('off')
    plt.title('Segmented image')
    plt.show()
    
    # save img to file
    cv.imwrite('Segmented_image.png', segmentRes)
    print('Done! Segmented image is saved to the same folder with the scripts')
    
    return img

def transformImg(img, optionView):
    
    """
    This function performs the Perspective Transform (a part of the image)
    :param img: 3-D array of the original image
    :param optionView: 1 - stretch view; 2 - shrink view
    """
    
    h, w = img.shape[0],img.shape[1]

    # point coordinates for Perspective Transform (just a part of the image)
    src = np.float32([[0,0],[300,100],[0,h],[300,393]])
    
    # coordinates for the transformed points
    
    if optionView == 1:
        dst = np.float32([[0,0],[w,0],[0,h],[w,h]])
    else:  
        dst = np.float32([[0,100],[300,100],[0,393],[300,393]])

    # transformation matrix
    M = cv.getPerspectiveTransform(src,dst)
    
    # warp image with the M matrix
    warpImg = cv.warpPerspective(img, M, (w,h))
    
    # simple plot part
    plt.imshow(warpImg.astype(int))
    plt. axis('off')
    plt.title('Transformed image')
    plt.show()
    
    # save img to file
    cv.imwrite('Transformed_image.png', warpImg)
    print('Done! Transformed image is saved to the same folder with the scripts')


##################### MAIN PART #####################

if __name__ == '__main__':
    
    # the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    
    ap.add_argument("-input_path", "--path_input_salad_image", type = str,
                    default='./files_for_test_pratique/salads.png',
                    help="path to the png image (salads.png)")
    
    ap.add_argument("-shrink_or_stretch", "--shrink_stretch", type = int, default = 2,
                    help="Shrink or stretch view: 1 - stretch ; 2 - shrink")

    args = vars(ap.parse_args())
    path = args["path_input_salad_image"]
    optionView = args["shrink_stretch"]

# Part 1: segmentation
    img = segmentImg(path)
    
# Part 2: transformation    
    transformImg(img, optionView)
