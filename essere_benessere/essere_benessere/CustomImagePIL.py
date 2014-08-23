# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageDraw
import re

class CustomImagePIL:
        
        image_name = ""
        image_raw = ""
        source_type = { "type" : None }

        def __init__(self, file_path=None, image_raw=None):
                if (file_path):
                        self.image_name = file_path
                        self.source_type["type"] = "path"
                elif (image_raw):
                        self.image_raw = image_raw
                        self.source_type["type"] = "raw"

        def resize_image(self, filename=None):
                # valid format list
                valid_format = [ "PNG", "JPEG", "GIF" ]
                max_box_size = { "width" : 300, "height" : 300 }
                try:
                        # checking source type
                        if (self.source_type["type"] == "path"):
                                # open image from path
                                im=Image.open(self.image_name)
                        elif (self.source_type["type"] == "raw"):
                                # create image from raw string
                                im=Image.open(self.image_name)
                        else:
                                raise Exception("Image source type error")

                        # get image height and width
                        nl=im.size[0]
                        nh=im.size[1]

                        # init of new image size
                        res_h=nh
                        res_l=nl

                        if (nl > nh):
                                if (nl > max_box_size["width"]):
                                        # Caso 1 -> h:l=nh:nl -> h=?
                                        print("caso 1")
                                        res_h = self.calculate_image_h(max_box_size["width"], nh, nl)
                                        res_l = max_box_size["width"]
                                elif (nh > max_box_size["height"]):
                                        # Caso 2 -> h:l=nh:nl l=?
                                        print("caso 2")
                                        res_h = max_box_size["height"]
                                        res_l = self.calculate_image_l(max_box_size["height"], nh, nl)
                        elif (nh > nl):
                                if (nh > max_box_size["height"]):
                                        # Caso 2 -> h:l=nh:nl l=?
                                        print("caso 2")
                                        res_h = max_box_size["height"]
                                        res_l = self.calculate_image_l(max_box_size["height"], nh, nl)
                                elif (nl > max_box_size["width"]):
                                        # Caso 1 -> h:l=nh:nl -> h=?
                                        print("caso 1")
                                        res_h = self.calculate_image_h(max_box_size["width"], nh, nl)
                                        res_l = max_box_size["width"]

                        if (im.format in valid_format):
                                # resize image
                                image_resized = im.resize((res_l,res_h), Image.ANTIALIAS)

                                # save resized image
                                self.save_resized_image(image_resized, old_filename=im.filename, new_filename=filename)
                        else:
                                print("Image format not supported")
                except(IOError):
                        print("Image source error")

                return True

        def calculate_image_h(self, box_width, image_h, image_l):
                """
                Function to calculate image width proportionality
                """
                return_var = False

                if (box_width and image_h and image_l):
                        return_var = (box_width * image_h) / image_l

                return return_var

        def calculate_image_l(self, box_height, image_h, image_l):
                """
                Function to calculate image width proportionality
                """
                return_var = False

                if (box_height and image_h and image_l):
                        return_var = (box_height * image_l) / image_h

                return return_var

        def save_resized_image(self, image, old_filename, new_filename=None):
                """
                Function to save a resized copy of image
                If a directory has a structure like this:
                dir_struct = "/folder1/folder.test/image.png"
                NOTICE: this function will break the directory structure.
                Es: dir_struct will be: "/folder1/folder_lXh.png"
                """

                return_var = None

                if (image):
                    if (not new_filename):
                            # removing dot
                            filename_no_ext = re.sub('\..*$', '', old_filename)
                            # append height and width in image name
                            new_filename=filename_no_ext + "_" + str(image.size[0]) + "X" + "" + str(image.size[1])
                            new_filename=new_filename + ".png"

                    # saving resized image
                    image.save(new_filename, "PNG")
                    return_var = new_filename + ".png"

                return return_var

"""
HOW resize_image WORKS
======================

    Area massima per le immagini
      300px
    |-------|

    +-------+ -
    |       | |
    |       | | 300px
    |       | |
    +-------+ -


Caso 1  (im.l > box.l) or (im.l > im.h and im.l > box.l):
        Se largezza immagine > altezza immagine
        Fisso larghezza trovo altezza (im.width > 300)
                       +----------------+ 
    +-------+          +-------+        |
    |       |          |       |        | <- l'immagine caricata ha sia altezza che
    +------------+  O  |       |        |    larghezza maggiori del box
    |            |     |       |        |
    +------------+     +-------+--------+

    h:l=nh:nl
    h:300=2320:3280
    h = (l*nh) / nl


Caso 2:  (im.h > box.h) or (im.h > im.l and im.h > box.h)
        Fisso altezza trovo larghezza (im.height > 300)
    +-----+         +---------+
    |     |         |         |
    +-----|-+       +-------+ |  <- l'immagine caricata ha sia altezza che
    |     | |   O   |       | |     larghezza maggiori del box
    |     | |       |       | |
    |     | |       |       | |
    +-----+-+       +-------+-+

    h:l=nh:nl
    300:l=2320:3280
    l = (300*3280) / 2320

Caso 3:
        Non tocco l'immagine perchè è inferiore o uguale all'area massima
    +-------+
    | +---+ |
    | |   | |
    | +---+ |
    +-------+

HOW TO USE
==========

# class init
custom_image_PIL_obj = CustomImagePIL("image3.png")
# resize and saving with custom name
custom_image_PIL_obj.resize_image(filename="prova.png")

TODO
====

- Custom box width and height form class instance
"""
