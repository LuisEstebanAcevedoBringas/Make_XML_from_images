from utils import get_boxes_from_txt, convert_bboxes, get_images_data, check_directory
from Add_inside_or_closes_boxes import add_bboxes
from get_info_from_xlsx import process_xlsx
from shapely.geometry import Polygon
import xml.etree.ElementTree as ET
from pathlib import Path
from os import path
import os.path
import pdb
import os

def analyze_txt():

    folder_with_txt_folders = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/frames"
    sub_folders = [name for name in os.listdir(folder_with_txt_folders) if os.path.isdir(os.path.join(folder_with_txt_folders, name))]
    for each_folder in sub_folders: #Do all the folders of the txt's files
        
        list_of_errors = []
        folder_path = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/annotations/xml_files/" + each_folder
        #if path.exists(folder_path) == True:
        #    continue
        check_directory(folder_path)
        imgs_path = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/frames/" + each_folder + "/" + each_folder + "_"
        array = process_xlsx(each_folder) #Get the temporal anotations from the excel file
        flag = 0
        last_frame_with_txt = ""
        for obj in array:
            for time in range(obj[3], obj[4] + 1): #Read each line of the excel file depending of the gesture 
                frame = imgs_path + str(time).rjust(6, '0') + '.jpg'
                bounding_boxes = []
                if obj[1] == "D0X":
                    continue

                else:
                    print("Class: ", obj[1], "Image: ", str(time).rjust(6, '0') + ".jpg")
                    save_path_of_xml = folder_path + "/" + each_folder + "_" + str(time).rjust(6, '0') + '.xml' #path to save the xml
                    actual_txt_path = "C:/Users/Luis Bringas/Desktop/yolo_txts_test/" + each_folder + "/" + each_folder + "_" + str(time).rjust(6, '0') + ".txt" #Path of the actual txt file
                    previous_txt_path = "C:/Users/Luis Bringas/Desktop/yolo_txts_test/" + each_folder + "/" + each_folder + "_" + str(time - 1).rjust(6, '0') + ".txt" #Path of the previous txt file
                    
                    file_exists = Path(save_path_of_xml)
                    if file_exists.is_file() == True: #Check if we already created the xml file
                        continue

                    else:
                        if path.exists(actual_txt_path) == False: #Check if YOLO created a txt file
                            if path.exists(previous_txt_path) == False and flag == 1:
                                bounding_boxes = get_boxes_from_txt(last_frame_with_txt)
                            elif path.exists(previous_txt_path) == True:
                                bounding_boxes = get_boxes_from_txt(previous_txt_path)
                                last_frame_with_txt = "C:/Users/Luis Bringas/Desktop/yolo_txts_test/" + each_folder + "/" + each_folder + "_" + str(time - 1).rjust(6, '0') + ".txt"
                                flag = 1
                            else:
                                x = str((actual_txt_path))
                                list_of_errors.append(x)
                                continue
                        else:
                            bounding_boxes = get_boxes_from_txt(actual_txt_path)
                            flag = 0

                    #Delete bounding boxes that are far from the previous box.
                    previous_xml_path = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/annotations/xml_files/" + each_folder + "/" + each_folder + "_" + str(time - 1).rjust(6, '0') + ".xml"

                    if path.exists(previous_xml_path) == True:

                        tree = ET.parse(previous_xml_path)
                        root = tree.getroot()
                        xmin =int(root.find("object").find("bndbox").find("xmin").text)
                        ymin =int(root.find("object").find("bndbox").find("ymin").text)
                        xmax =int(root.find("object").find("bndbox").find("xmax").text)
                        ymax =int(root.find("object").find("bndbox").find("ymax").text)

                        previous_boxes = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]
                        poly_1 = Polygon(previous_boxes)
                        if len(bounding_boxes) == 1:
                            poly_2 = Polygon(bounding_boxes[0])
                            if (poly_1.intersection(poly_2).area) < 100:
                                bounding_boxes.pop(0)
                        elif len(bounding_boxes) >= 2:
                            for i in range(len(bounding_boxes), 0, -1):
                                poly_2 = Polygon(bounding_boxes[i-1])
                                if (poly_1.intersection(poly_2).area) < 100:
                                    bounding_boxes.pop(i-1)
                                else:
                                    pass

                        if len(bounding_boxes) == 0: #If all the bounding boxes are deleted, copy the bounding boxes of the previous txt
                            aux = []
                            aux.append(previous_boxes)
                            bounding_boxes = aux

                    #Delete bounding boxes that are inside or super close to a bigger box.
                    if len(bounding_boxes) > 1:
                        final_bbox = add_bboxes(bounding_boxes)
                        get_images_data(frame, obj[1], obj[2], obj[6], final_bbox)                        
                        if len(final_bbox) > 1:  
                            bounding_boxes_norm = convert_bboxes(final_bbox)
                            get_images_data(frame, obj[1], obj[2], obj[6], bounding_boxes_norm)
                    else:
                        bounding_boxes_norm = convert_bboxes(bounding_boxes)
                        get_images_data(frame, obj[1], obj[2], obj[6], bounding_boxes_norm) #We pass the frame path, the label, the id label, the hand a the bboxes for each images.

        if len(list_of_errors) == 0:
            continue

        else:
            with open('./xml_with_errors/'+ each_folder +'.txt', 'w') as f:
                for line in list_of_errors:
                    f.write(line)
                    f.write('\n')

if __name__ == "__main__":

    analyze_txt()