# -*- coding: utf-8 -*-
"""
TO RUN:
python coco_generator.py
--Bkg_path "./files_for_test_pratique/background.png"
--Obj_path "./files_for_test_pratique/object.png"
--size_dataset 1000 (default)

@author: ajulyav@gmail.com
"""

import json
import random
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy
import os
import argparse
import numpy as np
import cv2 


def TransformForeground(foreground):
    
  """
    This function applies foreground transformations
    
    :param foreground: a valid foreground image  
    :return frgImage: the final image after transformations
  """

  # Rotate the foreground
  angle = random.randint(0, 359)  
  frgImage = foreground.rotate(angle, resample=Image.BICUBIC, expand=True)

  # Scale the foreground
  #scale = random.random() * 0.5 + 0.5
  #newSize = (int(frgImage.size[0] * scale), int(frgImage.size[1] * scale))
  #transfImage = frgImage.resize(newSize, resample=Image.BICUBIC)

  # Possible to add other transformations 
  # . . . 

  return frgImage

def CreateImgInfo(num, h, w):
    
    """
    This function creates info on image
    
    :param num: image number
    :param h, w: height and weight of image
    :return images_info: dictionary of image info
    """    
    
    images_info = dict()
  
    images_info["id"] = num
    images_info["width"] = h
    images_info["height"] = w
    images_info["file_name"] = "img_"+ str(num) + '.png'
    
    return images_info

def CreateAnnotation(num, annotationId, x, y, xEnd, yEnd):

  """
  This function writes obj annotation
    
  :param num: image number
  :param annotationId: id associated with the object
  :param x, y, xEnd, yEnd: object location
  :return annotate_image: dictionary of object info
  """  
  
  annotate_image = dict()
  annotate_image["id"] = annotationId
  annotate_image["bbox"] = [x, y, xEnd, yEnd]
  annotate_image["image_id"] = num
  annotate_image["segmentation"] = [[x, y, x, (y + yEnd), (x + xEnd), (y + yEnd), (x + xEnd), y]]
  annotate_image["category_id"] = 1
  
  return annotate_image
 

def basicInformation(annotation):
    
    """
    This function writes the main information of the annotation file
    
    :param Annotation: dictionary
    :return Annotation: dictionary with the main information
    """
    
    annotation["info"] = {"description": "Coco Trash",
              "version": "1.0",
              "year": 2021,
              "date_created": "2021/08/16"}
    
    annotation["categories"] = [{"supercategory": "trash", "id": 1, "name": "plasticBottle"}]
    
    return annotation

    
def GenerateImages(foreground, background, numGenerations):
    
    
  """
  This function generates an image and writes json
    
  :param foreground: a valid foreground image path
  :param background: a valid background image path
  :param numGenerations: number of images to generate (1000 by default)
  """
  
    # try to open  files
  try: 
      background = Image.open(background)
      foreground = Image.open(foreground)
  except FileNotFoundError:
      print("Make sure that both files are in the folder.")



  # folders for saving  
  if not os.path.isdir("./GeneratedData"):
      os.mkdir("./GeneratedData")
  if not os.path.isdir("./GeneratedData/masks"):
      os.mkdir("./GeneratedData/masks")      
        
  # initialize dictionaries and lists
  annotation = dict()
  annotation = basicInformation(annotation)
  annotatedImages = []
  infoImages = []
    
  # convert it to the RGBA space
  background = background.convert('RGBA')
  h, w = background.size[0], background.size[1]
  
  # init unique id
  annotationId = 1

  for num in range(numGenerations):
    # mask init 
    mask = Image.new('RGB', (h, w), (0, 0, 0))
      
    # deep copy of bkg for each of 1000 synthetic images  
    final = copy.deepcopy(background)

    # random from 0 to 4 objects
    numObj = random.randint(0, 4)
    
    if numObj == 0:

      # as it was asked to generate 0 foreground obj, store this type of annotations
      data = CreateAnnotation(num, annotationId, 0,0,0,0)
      annotatedImages.append(data)
       
      final = background
      
      # create masks of obj and save them
      mask = np.array(mask)
      mask[mask > 0] = 255
      
      cv2.imwrite(f"./GeneratedData/masks/mask_image{num}.png", mask) 
      
      annotationId += 1
     
    for obj in range(numObj):
      
      # call a function to transform the foreground obj
      frgImage = TransformForeground(foreground)

      # choose a random x,y position for the foreground
      maxX = final.size[0] - frgImage.size[0]
      maxY = final.size[1] - frgImage.size[1]

      # generate a new postion for the object
      objPosition = (random.randint(0, maxX), random.randint(0, maxY))
      

      # create annotation, save the obj position
      data = CreateAnnotation(num, annotationId, objPosition[0], objPosition[1], frgImage.size[0], frgImage.size[1])
      annotatedImages.append(data)
      annotationId += 1 
     
      # place the foreground object on the background
      newFgObj = Image.new('RGBA', final.size, color = (0, 0, 0, 0))
      newFgObj.paste(frgImage, objPosition)

      # extract the alpha channel from the foreground and paste it into a new image the size of the composite
      alpha_mask = frgImage.getchannel(3)
      new_alpha_mask = Image.new('L', final.size, color = 0)
      new_alpha_mask.paste(alpha_mask, objPosition)
      final = Image.composite(newFgObj, final, new_alpha_mask)
      
      # create masks of obj
      mask.paste(alpha_mask,objPosition,alpha_mask)

        
    name = './GeneratedData/img_' + str(num) + '.png'
    final.save(name, 'PNG')
    
    #save masks
    mask = np.array(mask)
    mask[mask > 0] = 255
    cv2.imwrite(f"./GeneratedData/masks/mask_image{num}.png", mask) 
    
    imgInfo =  CreateImgInfo(num, h, w)
    infoImages.append(imgInfo)

  annotation["annotations"] = annotatedImages
  annotation["images"] = infoImages

        
  with open('./GeneratedData/data_annotations.json', 'w') as outfile:
      json.dump(annotation, outfile)


##################### MAIN PART #####################

if __name__ == '__main__':

    ap = argparse.ArgumentParser()

    ap.add_argument("-Bkg_path", "--path_bkg", type=str,
                    default="./files_for_test_pratique/background.png",
                    help="path to the bkg.")

    ap.add_argument("-Obj_path", "--path_obj", type=str,
                    default="./files_for_test_pratique/object.png",
                    help="path to the object.")

    ap.add_argument("-size_dataset", "--size_of_dataset", type = int, default = 1000,
                    help="size of dataset, 1000 by default")

    args = vars(ap.parse_args())

    bkgPath = args["path_bkg"]
    objPath = args["path_obj"]
    size = args["size_of_dataset"]
    
    
    # call the function to generate 1000 images
    GenerateImages(objPath, bkgPath, size)
