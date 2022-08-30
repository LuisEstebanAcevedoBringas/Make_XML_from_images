import openpyxl

def process_xlsx(folder_name):
    theFile = openpyxl.load_workbook("./Annotation_List.xlsx")
    allSheetNames = theFile.sheetnames

    folder = folder_name
    metadata = []

    for sheet in allSheetNames:
        #print("Current sheet name is {}" .format(sheet))
        currentSheet = theFile[sheet]
        for row in range(1, currentSheet.max_row + 1):
            first_cell = "{}{}".format("A",row)
            if currentSheet[first_cell].value == folder:
                aux = []
                for column in "ABCDEF":  # Columns that is going to scan.
                    cell_name = "{}{}".format(column, row)
                    #print("cell position {} has value {}".format(cell_name, currentSheet[cell_name].value))
                    aux.append(currentSheet[cell_name].value)
                metadata.append(aux)
            else:
                continue
    
    return metadata

if __name__ == "__main__":
    x = process_xlsx("4CM11_2_R_#37")
    print (x)
    print(len(x))