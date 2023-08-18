from PIL import Image, ImageDraw, ImageFilter, ImageOps
import random

from utils import get_document,decide_where_to_paste,decide_resize,create_yolo_doc,resize_prop

class CreateInstance():
    def __init__(self,file_name,background_name,angle,blur=0,gray=0,final_width=None,background_size=(1920,1080)):
        self.file_name = file_name
        self.background_name = background_name
        self.final_width = final_width
        self.angle = angle
        self.blur = blur
        self.gray = gray
        self.background_size = background_size

    def create_with_yolo(self):

        # CROP DOCUMENT
        document,classe = get_document('original_imgs/{}'.format(self.file_name),'original_imgs/{}.txt'.format(self.file_name.split('.')[0]))

        print(document.size)

        mask = Image.new('L', document.size, 255)
        document = document.rotate(self.angle, expand=True)
        mask = mask.rotate(self.angle, expand=True)

        if self.blur != 0:
            document = document.filter(ImageFilter.GaussianBlur(self.blur))

        if self.gray != 0:
            document = ImageOps.grayscale(document)

        # GET BACKGROUND
        background = get_document('background/{}'.format(self.background_name))

        background = background.resize(self.background_size)

        resize_bool, i, j = decide_resize(document,background)
        if resize_bool:
            background = background.resize((i,j))

        center_w,center_h,posicao_insercao = decide_where_to_paste(document,background)

        background.paste(document, posicao_insercao, mask)

        yolo_txt = create_yolo_doc(classe,center_w,center_h,document,background)

        name_to_save = '{}_{}'.format(self.file_name.split('.')[0],self.background_name)

        if self.final_width is not None:
            background = resize_prop(background,self.final_width)

        background.save("created_imgs/{}".format(name_to_save))

        with open("created_imgs/{}.txt".format(name_to_save.split('.')[0]), 'w') as f:
            f.write(yolo_txt)

        print('DOCUMENT CREATED:',name_to_save)



    def create_without_yolo(self,classe):

        # CROP DOCUMENT
        document = get_document('original_imgs/{}'.format(self.file_name))

        mask = Image.new('L', document.size, 255)
        document = document.rotate(self.angle, expand=True)
        mask = mask.rotate(self.angle, expand=True)

        if self.blur != 0:
            document = document.filter(ImageFilter.GaussianBlur(self.blur))

        if self.gray != 0:
            document = ImageOps.grayscale(document)

        # GET BACKGROUND
        background = get_document('background/{}'.format(self.background_name))

        background = background.resize(self.background_size)

        resize_bool, i, j = decide_resize(document,background)
        if resize_bool:
            background = background.resize((i,j))
        
        center_w,center_h,posicao_insercao = decide_where_to_paste(document,background)

        background.paste(document, posicao_insercao, mask)

        yolo_txt = create_yolo_doc(classe,center_w,center_h,document,background)

        name_to_save = '{}_{}'.format(self.file_name.split('.')[0],self.background_name)

        if self.final_width is not None:
            background = resize_prop(background,self.final_width)

        background.save("created_imgs/{}".format(name_to_save))

        with open("created_imgs/{}.txt".format(name_to_save.split('.')[0]), 'w') as f:
            f.write(yolo_txt)

        print('DOCUMENT CREATED:',name_to_save)


if __name__ == "__main__":

    FILE_NAME = 'image.jpg'
    BACKGROUND_NAME = 'fuzzy_2.jpg'

    ANGLE_DOC = -25
    BLUR_DOC = 0
    GRAY_DOC = 0
    BACKGROUND_SIZE = (1920,1080)
    FINAL_WIDTH = 1080
    
    CreateInstance(FILE_NAME,BACKGROUND_NAME,ANGLE_DOC,BLUR_DOC,GRAY_DOC,FINAL_WIDTH,BACKGROUND_SIZE).create_without_yolo('0')
    