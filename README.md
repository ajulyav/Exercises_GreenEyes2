# Exercises_GreenEyes2

## Basic Image Processing and Coco Data Generation

*image_processor.py*: The exercise consist of two problems - image segmentation and transformation;

<img src="https://github.com/ajulyav/Exercises_GreenEyes2/blob/main/img/Segmented_image.png" width="300" height="200"> <img src="https://github.com/ajulyav/Exercises_GreenEyes2/blob/main/img/Transformed_image.png" width="300" height="200">

*coco_generator.py*: Coco-style dataset generation.

<img src="https://github.com/ajulyav/Exercises_GreenEyes2/blob/main/img/img_0.png" width="200" height="200"> <img src="https://github.com/ajulyav/Exercises_GreenEyes2/blob/main/img/mask_image0.png" width="200" height="200">

More details can be found in the PDF.



_________________________________________

How to Run:

**python image_processor.py**

-- input_path './files_for_test_pratique/salads.png'

-- shrink_or_stretch:  1 - stretch ; 2 - shrink

Sample:
```
python image_processor.py -input_path C:/Users/ajulyav/files_for_test_pratique/salads.png -shrink_or_stretch 2
```

**python coco_generator.py**

--Bkg_path "./files_for_test_pratique/background.png"

--Obj_path "./files_for_test_pratique/object.png"

--size_dataset 1000

