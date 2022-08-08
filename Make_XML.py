import xml.etree.ElementTree as ET
from PIL import Image
import numpy as np
import glob
import cv2
import os

def get_image_data(path):
    img_path = path #Get the path of the image.
    img = Image.open(path)
    img_width, img_height = img.size #Get width & height of the image.
    img_name = os.path.basename(path) #Get the name with extention of the image.
    num_hands = 2 #Total of hands in the image.

    return img_path, img_name ,img_width, img_height, num_hands

def generate_XML(img_path, img_name, img_width, img_height, num_hands, obj_names, obj_labels):
    annotation = ET.Element("annotation")
    add_folder = ET.SubElement(annotation,"folder")
    add_folder.text = "segment"
    add_filename = ET.SubElement(annotation,"filename")
    add_filename.text = os.path.basename(img_name)
    add_numHands = ET.SubElement(annotation,"hands")
    add_numHands.text = num_hands
    add_path = ET.SubElement(annotation, "path")
    add_path.text = img_path

    #Source section
    add_source = ET.SubElement(annotation,"source")
    add_database = ET.SubElement(add_source, "database")
    add_database.text="IPN Hand"

    #Size section
    add_size = ET.SubElement(annotation,"size")
    add_width = ET.SubElement(add_size,"width")
    add_width.text = img_width
    add_height = ET.SubElement(add_size,"height")
    add_height.text = img_height
    add_dimension = ET.SubElement(add_size,"depth")
    add_dimension.text = "3"

    #Object section
    for i in range(obj_names):
        add_object = ET.SubElement(annotation,"object")
        add_mame = ET.SubElement(add_object, "name")
        add_mame.text = obj_names[i]
        add_label = ET.SubElement(add_object,"label")
        add_label.text = obj_labels[i]
        add_bndbox = ET.SubElement(add_object,"bndbox")
        #Get the properties  "xmin", "ymin", "xmax", "ymax"


if __name__ == "__main__":
    Paths = glob("/*.jpg") 
    for path in Paths:
        get_image_data(path)