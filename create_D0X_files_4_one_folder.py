from utils import get_boxes_from_txt, convert_bboxes, get_images_data, check_directory
from Add_inside_or_closes_boxes import add_bboxes
from get_info_from_xlsx import process_xlsx
import xml.etree.ElementTree as ET
from pathlib import Path
from os import path

each_folder = "1CM42_11_R_#206"

folder_path = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/annotations/xml_files/" + each_folder
check_directory(folder_path)
imgs_path = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/frames/" + each_folder + "/" + each_folder + "_"
array = process_xlsx(each_folder) #Get the temporal anotations from the excel file
for obj in array:
    for time in range(obj[3], obj[4] + 1): #Read each line of the excel file depending of the gesture 
        frame = imgs_path + str(time).rjust(6, '0') + '.jpg'
        bounding_boxes = []
        if obj[1] == "D0X":
            save_path_of_xml = folder_path + "/" + each_folder + "_" + str(time).rjust(6, '0') + '.xml' #path to save the xml
            actual_txt_path = "C:/Users/Luis Bringas/Desktop/yolo_txts_test/" + each_folder + "/" + each_folder + "_" + str(time).rjust(6, '0') + ".txt" #Path of the actual txt file
            xml_file_exists = Path(save_path_of_xml)

            file_exists = Path(actual_txt_path)
            if path.exists(actual_txt_path) == False:
                get_images_data(frame, obj[1], obj[2], obj[6], "")
            else:
                bounding_boxes = get_boxes_from_txt(actual_txt_path)
                if len(bounding_boxes) > 1:
                    final_bbox = add_bboxes(bounding_boxes)
                    print("bbox", final_bbox)
                    if len(final_bbox) > 1:  
                        bounding_boxes_norm = convert_bboxes(final_bbox)
                        print(bounding_boxes_norm)
                        get_images_data(frame, obj[1], obj[2], obj[6], bounding_boxes_norm)
                    else:
                        get_images_data(frame, obj[1], obj[2], obj[6], final_bbox)
                else:
                    bounding_boxes_norm = convert_bboxes(bounding_boxes)
                    get_images_data(frame, obj[1], obj[2], obj[6], bounding_boxes_norm) #We pass the frame path, the label, the id label, the hand a the bboxes for each images.
        else:
            continue