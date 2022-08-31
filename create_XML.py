# Generate the xml files from images in a folder
from get_info_from_xlsx import process_xlsx
import xml.etree.ElementTree as ET
import cv2
import os

def check_directory():
    annotation_dir = ("annotation")
    check_folder = os.path.isdir("./4CM11_2_R_#37/" + annotation_dir)

    if not check_folder:
        os.makedirs(annotation_dir)
        print("created folder : ", annotation_dir)

    else:
        print(annotation_dir, "the folder" + annotation_dir + " already exists.")


def get_image_data(path, gesture, gesture_id):
    img_path = path  # Get the path of the image.
    img_path = img_path.replace(os.path.sep, "/")
    img = cv2.imread(path)  # Read the image.
    # Convert image into gray.
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_height = img.shape[0]  # Get height.
    img_width = img.shape[1]  # Get width.
    # Get the name with extention of the image.
    img_name = os.path.basename(path)
    folder_name = img_path.split("/")[1]  # Get the name of the folder
    hand = folder_name.split("_")[2]

    colors_right = [179, 111, 130, 150, 16, 29]
    colors_left = []

    #choosen_imgs = ["4CM11_2_R_#37_000069.png", "4CM11_2_R_#37_000169.png", "4CM11_2_R_#37_001500.png", "4CM11_2_R_#37_003685.png", "4CM11_2_R_#37_004021.png"]

    # Declare all the lists.
    obj_names, bboxes, x_left, y_left, x_right, y_right = ([] for i in range(6))

    for y in range(grayscale.shape[0]):  # Columns
        for x in range(grayscale.shape[1]):  # Rows
            r = grayscale[y, x]
            if r == colors_right[0] or r == colors_right[1] or r == colors_right[2] or r == colors_right[3] or r == colors_right[4] or r == colors_right[5]:
                x_right.append(x)
                y_right.append(y)
            elif(r) == colors_left:  # Look for the light gray color.
                x_left.append(x)
                y_left.append(y)

    try:
        xmin_left = min(x_left)
        ymin_left = min(y_left)
        xmax_left = max(x_left)
        ymax_left = max(y_left)
        obj_names.append("left")
        bboxes.append([xmin_left, ymin_left, xmax_left, ymax_left])
        cv2.rectangle(img, (xmin_left, ymin_left), (xmax_left, ymax_left), (255, 255, 255), 2)
    except:
        print("No left hand")

    try:
        xmin_right = min(x_right)
        ymin_right = min(y_right)
        xmax_right = max(x_right)
        ymax_right = max(y_right)
        obj_names.append("right")
        bboxes.append([xmin_right, ymin_right, xmax_right, ymax_right])
        cv2.rectangle(img, (xmin_right, ymin_right), (xmax_right, ymax_right), (255, 255, 255), 2)
    except:
        print("No right hand")

    #if img_name in choosen_imgs:
        # cv2.putText(img, (gesture + " - " + hand), (xmin_right, ymin_right - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2) #Show the label and the hand over the bounding box.
        #cv2.imshow(img_name, img)  # Show img with the bounding boxes.
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

    generate_XML(folder_name, img_path, img_name, img_width, img_height, obj_names, hand, bboxes, gesture, gesture_id)

# Generate the xml files
def generate_XML(folder_name, img_path, img_name, img_width, img_height, obj_names, hand, bounding_boxes, gesture, gesture_id):
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
    save_path = "./" + folder_name + "/annotation/" + file_name + ".xml"
    annotation = ET.Element("annotation")
    add_folder = ET.SubElement(annotation, "folder")
    add_folder.text = "segment"
    add_filename = ET.SubElement(annotation, "filename")
    add_filename.text = os.path.basename(img_name)
    add_path = ET.SubElement(annotation, "path")
    add_path.text = img_path
    add_numHands = ET.SubElement(annotation, "hands")
    add_numHands.text = str(len(obj_names))

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

    if len(obj_names) == 0:
        add_name = ET.SubElement(annotation, "name")
        add_name.text = gesture
        add_label = ET.SubElement(annotation, "label")
        add_label.text = str(gesture_id)

    # Object section
    for i in range(len(obj_names)):
        add_object = ET.SubElement(annotation, "object")
        add_name = ET.SubElement(add_object, "name")
        add_name.text = gesture
        add_label = ET.SubElement(add_object, "label")
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

        if i >= len(obj_names) - 1:
            break

    file_content = ET.tostring(annotation, encoding='unicode')
    new_file = open(save_path, "w")
    new_file.write(file_content)


def main():
    array = process_xlsx('4CM11_2_R_#37')
    path = "./4CM11_2_R_#37/4CM11_2_R_#37_"
    for obj in array:
        for time in range(obj[3], obj[4] + 1):
            frame = path + str(time).rjust(6, '0') + '.png'
            get_image_data(frame, obj[1], obj[2])
    #get_image_data("./4CM11_2_R_#37/4CM11_2_R_#37_004047.png", "D0X", 1)

if __name__ == "__main__":
    main()