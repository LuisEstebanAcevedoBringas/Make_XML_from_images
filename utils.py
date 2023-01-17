import xml.etree.ElementTree as ET
import cv2
import os

def check_directory(path):
    check_folder = (path)

    if not os.path.exists(check_folder): #Check is the folder exist
        os.makedirs(check_folder)
        print("created folder: ", check_folder)

    else:
        print("The folder " + check_folder + " already exists.")

def get_images_data(path, gesture, gesture_id, hand, bounding_boxes):

    img_path = path  #Get the path of the image.
    img_path = img_path.replace(os.path.sep, "/")
    img = cv2.imread(path)  #Read the image.
    img_height = img.shape[0]  #Get height.
    img_width = img.shape[1]  #Get width.
    img_name = os.path.basename(path) #Get the name with extention of the image.
    folder_name = img_path.split("/")[7]  #Get the name of the folder
    generate_XML(folder_name, img_path, img_name, img_width, img_height, hand, gesture, gesture_id, bounding_boxes)

def generate_XML(folder_name, img_path, img_name, img_width, img_height, hand, gesture, gesture_id, bounding_boxes):
    '''
    Params:
    img_path -> (str)
    img_name -> (str)
    img_width -> (int)
    img_height -> (int)
    num_hands -> (int) of the number of hands in the images. 
    obj_names -> List of the object names (left or right)
    bounding_boxes -> List of arrays with the bounding boxes of the image.
    '''
    file_name = img_name.split('.')[0]
    save_path = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/annotations/xml_files/" + folder_name + "/" + file_name + ".xml"
    annotation = ET.Element("annotation")
    add_folder = ET.SubElement(annotation, "folder")
    add_folder.text = folder_name
    add_filename = ET.SubElement(annotation, "filename")
    add_filename.text = os.path.basename(img_name)
    add_path = ET.SubElement(annotation, "path")
    add_path.text = img_path
    if gesture == "D0X":
        add_gesture = ET.SubElement(annotation, "gesture")
        add_gesture.text = "0"
    elif gesture == "B0A" or gesture == "B0B":
        add_gesture = ET.SubElement(annotation, "gesture")
        add_gesture.text = "1"
    else:
        add_gesture = ET.SubElement(annotation, "gesture")
        add_gesture.text = "2"

    # Source section
    add_source = ET.SubElement(annotation, "source")
    add_database = ET.SubElement(add_source, "database")
    add_database.text = "IPN Hand"

    # Size section
    add_size = ET.SubElement(annotation, "size")
    add_width = ET.SubElement(add_size, "width")
    add_width.text = str(img_width)
    add_height = ET.SubElement(add_size, "height")
    add_height.text = str(img_height)
    add_dimension = ET.SubElement(add_size, "depth")
    add_dimension.text = "3"

    if len(bounding_boxes) == 0:
        add_object = ET.SubElement(annotation, "object")
        add_name = ET.SubElement(add_object, "class")
        add_name.text = gesture
        add_label = ET.SubElement(add_object, "id")
        add_label.text = str(gesture_id)

    # Object section
    for i in range(len(bounding_boxes)):
        add_object = ET.SubElement(annotation, "object")
        add_name = ET.SubElement(add_object, "class")
        add_name.text = gesture
        add_label = ET.SubElement(add_object, "id")
        add_label.text = str(gesture_id)
        add_hand = ET.SubElement(add_object, "hand")
        add_hand.text = hand
        add_bndbox = ET.SubElement(add_object, "bndbox")

        # Get the properties "xmin", "ymin", "xmax", "ymax"
        xmin = str(bounding_boxes[i][0])
        ymin = str(bounding_boxes[i][1])
        xmax = str(bounding_boxes[i][2])
        ymax = str(bounding_boxes[i][3])
        add_xmin = ET.SubElement(add_bndbox, "xmin")
        add_xmin.text = str(xmin)
        add_ymin = ET.SubElement(add_bndbox, "ymin")
        add_ymin.text = str(ymin)
        add_xmax = ET.SubElement(add_bndbox, "xmax")
        add_xmax.text = str(xmax)
        add_ymax = ET.SubElement(add_bndbox, "ymax")
        add_ymax.text = str(ymax)

        if i >= len(bounding_boxes) - 1:
            break

    file_content = ET.tostring(annotation, encoding='unicode')
    new_file = open(save_path, "w")
    new_file.write(file_content)

def get_boxes_from_txt(txt_path):
    width = 640
    height = 480
    bboxes_yolo = []
    bboxes_VOC = []
    with open(txt_path) as file:
        for line in file:
            bboxes_yolo.append(line.split()[1:5]) #get the bboxes of the txt file

    for box in range(len(bboxes_yolo)):
        w_half_len = (float(bboxes_yolo[box][2]) * width) / 2
        h_half_len = (float(bboxes_yolo[box][3]) * height) / 2
        xmin = int((float(bboxes_yolo[box][0]) * width) - w_half_len)
        ymin = int((float(bboxes_yolo[box][1]) * height) - h_half_len)
        xmax = int((float(bboxes_yolo[box][0]) * width) + w_half_len)
        ymax = int((float(bboxes_yolo[box][1]) * height) + h_half_len)
    
        bboxes_VOC.append([[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]])

    return(bboxes_VOC)

def convert_bboxes(bboxes):
    bounding_boxes = []
    try:
        for x in range(len(bboxes)):
            xmin = bboxes[x][0][0]
            ymin = bboxes[x][0][1]
            xmax = bboxes[x][1][0]
            ymax = bboxes[x][2][1]
            bounding_boxes.append([xmin, ymin, xmax, ymax])
    except:
        for x in range(len(bboxes)):
            xmin = bboxes[x][0]
            ymin = bboxes[x][1]
            xmax = bboxes[x][2]
            ymax = bboxes[x][3]
            bounding_boxes.append([xmin, ymin, xmax, ymax])
    return bounding_boxes