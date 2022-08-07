## Generate XML files with the annotations of segmented images from de IPN Hand dataset.

### XML Structure:
```
<annotation>
    <folder> folder_name </folder>
    <filename> filename.jpg </filename>
    <hands> num_hands </hands>
    <path> path/filename.jpg </path>
    <source>
        <database> IPN_Hand </database>
        <keyword> keyword </keyword>
        <date> date </date>
    </source>
    <size>
        <width> width </width>
        <height> height </height>
        <depth> 3 </depth>
    </size>
    <object>
        <name> left or right </name>
        <label> 1 for left - 2 for right </label>
        <properly> 0 </properly>
        <bndbox>
            <xmin> xmin </xmin>
            <ymin> ymin </ymin>
            <xmax> xmax </xmax>
            <ymax> ymax </ymax>
            <obj_size> obj_size </obj_size>
        </bndbox>
        <size> size </size>
    </object>
</annotation>
```