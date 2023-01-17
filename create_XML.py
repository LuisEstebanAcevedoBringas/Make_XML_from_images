# Generate the xml files from images in a folder
from get_info_from_xlsx import process_xlsx
import xml.etree.ElementTree as ET
from pathlib import Path
import glob
import cv2
import os

def check_directory(path):
    annotation_dir = ("annotation")
    check_folder = (path + "/annotation/")

    if not os.path.exists(check_folder): #Check is the folder exist
        os.makedirs(check_folder)
        print("created folder: ", check_folder)

    else:
        print("The folder " + check_folder + " already exists.")


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
    folder_name = img_path.split("/")[8]  # Get the name of the folder
    hand = img_name.split("_")[2]

    colors_right = [179, 111, 130, 150, 16, 29]
    colors_left = [76, 159, 190, 227, 43, 99]

    # Declare all the lists.
    obj_names, bboxes, x_left, y_left, x_right, y_right = ([] for i in range(6))

    for y in range(grayscale.shape[0]):  # Columns
        for x in range(grayscale.shape[1]):  #Rows
            r = grayscale[y, x]
            if r == colors_right[0] or r == colors_right[1] or r == colors_right[2] or r == colors_right[3] or r == colors_right[4] or r == colors_right[5]:
                x_right.append(x)
                y_right.append(y)
            elif r == colors_left[0] or r == colors_left[1] or r == colors_left[2] or r == colors_left[3] or r == colors_left[4] or r == colors_left[5]:  # Look for the light gray color.
                x_left.append(x)
                y_left.append(y)

    if hand == "L":
        try:
            xmin_left = min(x_left)
            ymin_left = min(y_left)
            xmax_left = max(x_left)
            ymax_left = max(y_left)
            obj_names.append("left")
            bboxes.append([xmin_left, ymin_left, xmax_left, ymax_left])
            #cv2.rectangle(img, (xmin_left, ymin_left), (xmax_left, ymax_left), (255, 255, 255), 2)
        except:
            print("No left hand")

    elif hand == "R":
        try:
            xmin_right = min(x_right)
            ymin_right = min(y_right)
            xmax_right = max(x_right)
            ymax_right = max(y_right)
            obj_names.append("right")
            bboxes.append([xmin_right, ymin_right, xmax_right, ymax_right])
            #cv2.rectangle(img, (xmin_right, ymin_right), (xmax_right, ymax_right), (255, 255, 255), 2)
        except:
            print("No right hand")

    #cv2.putText(img, (gesture + " - " + hand), (xmin_right, ymin_right - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2) #Show the label and the hand over the bounding box.
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
    save_path = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/extension/anotation_files_yolo/" + folder_name + "/annotation/" + file_name + ".xml"
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
    
    folder_with_img_folders = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/extension/frames_original_res"
    sub_folders = [name for name in os.listdir(folder_with_img_folders) if os.path.isdir(os.path.join(folder_with_img_folders, name))]
    print("Number of folder: ",len(sub_folders))
    sub_folders_pos = 0
    
    for each_folder in sub_folders:
        print("folder name: ",each_folder)
        array = process_xlsx(each_folder)
        path = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/extension/anotation_files_yolo/" + each_folder
        check_directory(path)
        imgs = (glob.glob(path + "/*.png")) #Get all the images names in the folder
        #print("Imgs paths: ", imgs)
        imgs_path = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/extension/anotation_files_yolo/" + each_folder + "/" + each_folder + "_"
        choosen_img_numbers = []
        img_position = 0

        for i in range(len(imgs)):
            #print(x[i])
            name_img = Path(imgs[i]).stem #Get the name of the img
            num_img = name_img.split("_")[4] #Get the name without the extension
            num_img = num_img.lstrip("0") #Remove all the zeros on the name
            choosen_img_numbers.append(num_img)
        print("Images numers: ",choosen_img_numbers)
        print("number of images: ", len(choosen_img_numbers))

        for obj in array:
            for time in range(obj[3], obj[4] + 1):
                print("time",time)
                frame = imgs_path + str(time).rjust(6, '0') + '.png'
                #print("Frame: ", frame)
                #print("Frame inicial: ", obj[3])
                #print("Frame final: ", obj[4])
                name_img = Path(frame).stem #Get the name of the img
                num_img = name_img.split("_")[4] #Get the name without the extension
                num_img = num_img.lstrip("0") #Remove all the zeros on the name
                print("Numero de frame real: ", num_img)
                print("Numero de frame choosen: ", choosen_img_numbers[img_position])
                if int(choosen_img_numbers[img_position]) >= int(obj[3]) and int(choosen_img_numbers[img_position]) <= int(obj[4]) and int(choosen_img_numbers[img_position]) == int(num_img):
                    #print(img_position)
                    print("Img #",img_position," pass: ", frame)
                    get_image_data(frame, obj[1], obj[2])
                    img_position += 1
                else:
                    #print("Imagen no seleccionada.")
                    continue
        sub_folders_pos += 1
    #get_image_data("./4CM11_2_R_#37/4CM11_2_R_#37_004047.png", "D0X", 1)

if __name__ == "__main__":
    main()