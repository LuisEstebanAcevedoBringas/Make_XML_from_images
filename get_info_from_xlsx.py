import pandas as pd

def process_xlsx(excel_path):
    annot_file = pd.read_excel(excel_path) #Path of the xlsx file with the annotations
    print(annot_file.head())

if __name__ == "__main__":
    process_xlsx("C:/Bringas/MISTI/Final_Proyect/Make_XML_from_images/Annotation_List.xlsx")