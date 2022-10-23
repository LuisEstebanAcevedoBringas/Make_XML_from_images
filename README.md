## Generate XML files with the annotations of segmented images from the IPN Hand dataset.

### XML Structure (left and right classes):
```
<annotation>
    <folder> segment </folder>
    <filename> filename.jpg </filename>
    <path> path/filename.jpg </path>
    <source>
        <database> IPN_Hand </database>
    </source>
    <size>
        <width> width </width>
        <height> height </height>
        <depth> 3 </depth>
    </size>
    <object>
        <name> D0X, B0A, B0B, G01, G02, G03, ... , G011 </name>
        <label> 1 - 14 </label>
        <hand> left or right </hand>
        <bndbox>
            <xmin> xmin </xmin>
            <ymin> ymin </ymin>
            <xmax> xmax </xmax>
            <ymax> ymax </ymax>
        </bndbox>
    </object>
</annotation>
```