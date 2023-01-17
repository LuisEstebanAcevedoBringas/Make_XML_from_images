## Generate XML files with the annotations of segmented images from the IPN Hand dataset.

### XML Structure (left and right classes):
```
<annotation>
    <folder> segment </folder>
    <filename> filename.jpg </filename>
    <path> path/filename.jpg </path>
    <gesture> 0 = D0X , 1 = B0A or B0B , 2 = G01 ~ G11 </gesture>
    <source>
        <database> IPN_Hand </database>
    </source>
    <size>
        <width> width </width>
        <height> height </height>
        <depth> 3 </depth>
    </size>
    <object>
        <class> D0X, B0A, B0B, G01, G02, G03, ... , G011 </class>
        <id> 1 - 14 </id>
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