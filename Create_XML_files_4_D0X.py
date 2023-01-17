from utils import get_boxes_from_txt, convert_bboxes, get_images_data, check_directory
from Add_inside_or_closes_boxes import add_bboxes
from get_info_from_xlsx import process_xlsx
import xml.etree.ElementTree as ET
from pathlib import Path
from os import path
import pdb
import cv2
import os

def delete_txt():
    
    folder_with_txt_folders = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/frames"
    sub_folders = [name for name in os.listdir(folder_with_txt_folders) if os.path.isdir(os.path.join(folder_with_txt_folders, name))]
    for each_folder in sub_folders: #Do all the folders of the txt's files
        txts = []
        print("========== folder: ", each_folder, " ==========")
        array = process_xlsx(each_folder) #Get the temporal anotations from the excel file
        for obj in array:
            for time in range(obj[3], obj[4]): #Read each line of the excel file depending of the gesture 
                if obj[1] == "D0X":
                    actual_txt_path = "C:/Users/Luis Bringas/Desktop/yolo_txts_test/" + each_folder + "/" + each_folder + "_" + str(time).rjust(6, '0') + ".txt" #Path of the actual txt file
                    file_exists = Path(actual_txt_path)
                    if file_exists.is_file() == False:
                        continue
                    else:
                        txt_name = actual_txt_path.split("/")[6]
                        txt_number = txt_name.split("_")[4]
                        txt = txt_number.split(".")[0]
                        txts.append(int(txt))
                        res = [[txts[0]]]    # start/init with the 1st item/number
                        for i in range(1, len(txts)):
                            if txts[i] - res[-1][-1] > 1:  # compare current and previous item
                                res.append([])
                            res[-1].append(txts[i])
                else:
                    continue
        print(txts)
        print(res)
        for i in range(len(res)):
            if len(res[i]) < 4:
                print(res[i])
                for e in res[i]:
                    txt_2_delete = "C:/Users/Luis Bringas/Desktop/yolo_txts_test/" + each_folder + "/" + each_folder + "_" + str(e).rjust(6, "0") + ".txt" #Path of the actual txt file
                    os.remove(txt_2_delete) #Delete the txt file.
                    print("The file ",txt_2_delete, " was deleted.")

if __name__ == "__main__":

    #delete_txt()

    folder_with_txt_folders = "C:/Users/Luis Bringas/Documents/Databases/IPN_Hand/frames"
    sub_folders = [name for name in os.listdir(folder_with_txt_folders) if os.path.isdir(os.path.join(folder_with_txt_folders, name))]
    for each_folder in sub_folders: #Do all the folders of the txt's files
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
                    
                    #if xml_file_exists.is_file() == True: #Check if we already created the xml file
                        # print("The file: ", save_path_of_xml, " already exists")
                    #    continue
                    file_exists = Path(actual_txt_path)
                    if path.exists(actual_txt_path) == False:
                        get_images_data(frame, obj[1], obj[2], obj[6], "")
                    else:
                        bounding_boxes = get_boxes_from_txt(actual_txt_path)
                        # print(bounding_boxes)
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
