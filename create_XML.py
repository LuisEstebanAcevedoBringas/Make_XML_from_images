#Generate the xml files from images with the clases "left" and "right".
import xml.etree.ElementTree as ET
from glob import glob
import cv2
import os

def get_image_data(path):
    img_path = path #Get the path of the image.
    img = cv2.imread(path) #Read the image.
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Convert image into gray.
    img_height = img.shape[0] #Get height.
    img_width = img.shape[1] #Get width.
    img_name = os.path.basename(path) #Get the name with extention of the image.

    colors = [0, 255, 172, 105] #{black, white, light_gray, gray}

    obj_labels, obj_names, bboxes, x_left, y_left, x_right, y_right = ([] for i in range(7)) #Declare all the lists.

    for y in range(grayscale.shape[0]):  # Columns
        for x in range(grayscale.shape[1]):  # Rows
            r = grayscale[y, x]
            if(r) == colors[3]: #Look for the gray color.
                x_right.append(x)
                y_right.append(y)
            elif(r) == colors[2]: #Look for the light gray color.
                x_left.append(x)
                y_left.append(y)

    try:
        xmin_left = min(x_left)
        ymin_left = min(y_left)
        xmax_left = max(x_left)
        ymax_left = max(y_left)
        obj_labels.append("1")
        obj_names.append("left")
        bboxes.append([xmin_left, ymin_left, xmax_left, ymax_left])
        #cv2.rectangle(img, (xmin_left, ymin_left), (xmax_left, ymax_left), (0, 255, 0), 2)
    except:
        print("No left hand")

    try:
        xmin_right = min(x_right)
        ymin_right = min(y_right)
        xmax_right = max(x_right)
        ymax_right = max(y_right)
        obj_labels.append("2")
        obj_names.append("right")
        bboxes.append([xmin_right, ymin_right, xmax_right, ymax_right])
        #cv2.rectangle(img, (xmin_right, ymin_right), (xmax_right, ymax_right), (255, 0, 0), 2)
    except:
        print("No right hand")

    #cv2.imshow(img_name, img) #Show img with the bounding boxes
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    generate_XML(img_path, img_name, img_width, img_height, obj_names, obj_labels, bboxes)

def generate_XML(img_path, img_name, img_width, img_height, obj_names, obj_labels, bounding_boxes):
    '''
    Params:
    img_path -> (str)
    img_name -> (str)
    img_width -> (int)
    img_height -> (int)
    num_hands -> (int) of the number of hands in the images. 
    obj_names -> List of the object names (left or right)
    obj_labels -> List of the object labels (1 for left - 2 for right)
    bounding_boxes -> List of arrays with the bounding boxes of the image.
    '''
    file_name = img_name.split('.')[0]
    save_path = "./test/annotation/" + file_name + ".xml"
    annotation = ET.Element("annotation")
    add_folder = ET.SubElement(annotation,"folder")
    add_folder.text = "segment"
    add_filename = ET.SubElement(annotation,"filename")
    add_filename.text = os.path.basename(img_name)
    add_path = ET.SubElement(annotation, "path")
    add_path.text = img_path
    add_numHands = ET.SubElement(annotation,"hands")
    add_numHands.text = str(len(obj_names))

    #Source section
    add_source = ET.SubElement(annotation,"source")
    add_database = ET.SubElement(add_source, "database")
    add_database.text = "IPN Hand"

    #Size section 
    add_size = ET.SubElement(annotation,"size")
    add_width = ET.SubElement(add_size,"width")
    add_width.text = str(img_width)
    add_height = ET.SubElement(add_size,"height")
    add_height.text = str(img_height)
    add_dimension = ET.SubElement(add_size,"depth")
    add_dimension.text = "3"

    #Object section
    for i in range(len(obj_names)):
        add_object = ET.SubElement(annotation,"object")
        add_mame = ET.SubElement(add_object, "name")
        add_mame.text = obj_names[i]
        add_label = ET.SubElement(add_object,"label")
        add_label.text = str(obj_labels[i])
        add_bndbox = ET.SubElement(add_object,"bndbox")

        #Get the properties "xmin", "ymin", "xmax", "ymax"
        xmin = str(bounding_boxes[i][0])
        ymin = str(bounding_boxes[i][1])
        xmax = str(bounding_boxes[i][2])
        ymax = str(bounding_boxes[i][3])
        add_xmin = ET.SubElement(add_bndbox,"xmin")
        add_xmin.text = str(xmin)
        add_ymin = ET.SubElement(add_bndbox,"ymin")
        add_ymin.text = str(ymin)
        add_xmax = ET.SubElement(add_bndbox,"xmax")
        add_xmax.text = str(xmax)
        add_ymax = ET.SubElement(add_bndbox,"ymax")
        add_ymax.text = str(ymax)

        if i >= len(obj_names) - 1:
            break

    file_content = ET.tostring(annotation, encoding='unicode')
    new_file = open(save_path, "w")
    new_file.write(file_content) 

if __name__ == "__main__":
    Paths = glob("./test/*.jpg") 
    for path in Paths:
        get_image_data(path)