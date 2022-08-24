## Generate XML files with the annotations of segmented images from the IPN Hand dataset.

### XML Structure:
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
        <name> left or right </name>
        <label> 1 for left - 2 for right </label>
        <bndbox>
            <xmin> xmin </xmin>
            <ymin> ymin </ymin>
            <xmax> xmax </xmax>
            <ymax> ymax </ymax>
        </bndbox>
    </object>
</annotation>
```