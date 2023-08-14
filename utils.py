from PIL import Image
import random

def get_document(path,text=None):
    img = Image.open(path)

    if text is not None:
        W, H = img.size

        with open(text, 'r') as arquivo:
            # Lê a primeira linha do arquivo
            primeira_linha = arquivo.readline()
            
            # Remove caracteres de quebra de linha, se necessário
            primeira_linha = primeira_linha.strip()

        list_primeira_linha = primeira_linha.split()

        classe,Xw,Xh,w,h = [float(i) for i in list_primeira_linha]

        w_doc = w * W
        h_doc = h * H

        xw_doc = Xw * W
        xh_doc = Xh * H

        print(w_doc,h_doc,xw_doc,xh_doc)

        x_min = xw_doc - w_doc/2
        x_max = xw_doc + w_doc/2

        y_min = xh_doc - h_doc/2
        y_max = xh_doc + h_doc/2

        img = img.crop((x_min, y_min, x_max, y_max))

        return img,classe
    else:
        return img


def decide_where_to_paste(document,background):
    w_document, h_document = document.size
    w_background, h_background = background.size

    pad_w = int(w_document/2)
    center_w = random.randint(0+pad_w, w_background-pad_w)
    # center_w = random.randrange(start=0+pad_w,stop=w_background-pad_w)
    pad_h = int(h_document/2)
    center_h = random.randint(0+pad_h, h_background-pad_h)
    # center_h = random.randrange(start=0+pad_h,stop=h_background-pad_h)

    posicao_insercao = (center_w-pad_w,center_h-pad_h)

    return center_w,center_h,posicao_insercao

def decide_resize(document,background):
    w_document, h_document = document.size
    w_background, h_background = background.size
    if w_document>w_background or h_document>h_background:
        i = (random.random() + 1) * w_document
        j = (random.random() + 1) * h_document
        return True, int(i), int(j)
    return False, w_document, h_document

def resize_prop(imagem, width):
    # Abre a imagem usando a biblioteca Pillow
    
    # Calcula a proporção de redimensionamento
    proporcao = width / float(imagem.width)
    
    # Calcula a nova altura mantendo a proporção
    altura_desejada = int(imagem.height * proporcao)
    
    # Redimensiona a imagem
    nova_imagem = imagem.resize((width, altura_desejada), Image.ANTIALIAS)
    
    return nova_imagem

def create_yolo_doc(classe,center_w,center_h,document,background):
    w_document, h_document = document.size
    w_background, h_background = background.size

    yolo_Xw = center_w/w_background
    yolo_Xh = center_h/h_background

    yolo_W = w_document/w_background
    yolo_H = h_document/h_background

    yolo_txt = ' '.join([str(i) for i in [int(classe),yolo_Xw,yolo_Xh,yolo_W,yolo_H]])

    return yolo_txt