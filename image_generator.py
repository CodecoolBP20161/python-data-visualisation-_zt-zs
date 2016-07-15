from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random
from connect_db import sql_queries


# very 'in progress'
class Text():
    QUERIES = sql_queries()
    def __init__(self, queries):
        self.fill = queries[2]
        self.size = queries[1]
        self.text = queries[0]


    @classmethod
    def output(cls, queries, number):
        return [Text(queries) for queries in cls.QUERIES[number]]


    @staticmethod
    def sizing(resize_list):
        if len(resize_list) < 100:  # for shorter lists -> bigger letters
            for d in resize_list:
                if d.size is not None:
                    if d.size <= 10:
                        d.size = int(d.size*10)
                    elif d.size > 10 and d.size <= 100:
                        d.size = int(d.size//135)
                    elif d.size > 100 and d.size <= 1000:
                        d.size = int(d.size // 150)
                    elif d.size > 1000:
                        d.size = int(d.size//150)
                else:
                    d.size = 11
        else:  # for longer lists -> smaller letters
            for d in resize_list:
                if d.size is not None:
                    if d.size <= 10:
                        d.size = int(d.size * 5)
                    elif d.size > 10 and d.size <= 100:
                        d.size = int(d.size // 10)
                    elif d.size > 100 and d.size <= 1000:
                         d.size = int(d.size // 20)
                else:
                    d.size = 11
        return resize_list


# generating an empty image
img = Image.new("RGB", (712, 712), "black")
draw = ImageDraw.Draw(img)


# initializing the font size and path/type
default_size = 10
try:
    font_path = "ComicSansMS3.ttf"
    font = ImageFont.truetype(font_path)
except:
    font = ImageFont.load_default()


# generating an x coordinate
def get_x(text_size):
    if text_size[0] >= img.size[0]:
        x = 0
    else:
        x = random.randint(0, (img.size[0]-text_size[0]))  # full width - horizontal size of text
    return x


# generating a y coordinate
def get_y(text_size):
    if text_size[1] >= img.size[1]:
        y = 0
    else:
        y = random.randint(0, (img.size[1] - text_size[1]))  # full width - horizontal size of text
    return y


# pasting doge in the center of the word cloud
def doge(img):
    import requests
    from io import BytesIO
    response = requests.get('http://i.imgur.com/P5t9JNF.png')  # getting the picture from the internet
    doge = Image.open(BytesIO(response.content))
    # doge = Image.open("doge.png")  # local file
    doge.convert('RGB')
    img.paste(doge, (img.size[0]//2-doge.size[0]//2, img.size[1]//2-doge.size[1]//2))
    return img


# drawing the texts onto the image
def print_text(datas, filename):
    doge(img) #  image with doge

    # a list for already used coordinates
    not_empty = []

    for i in datas:
        font = ImageFont.truetype(font_path, default_size+i.size)
        text_size = draw.textsize(i.text, font=font)
        fill = i.fill
        x = get_x(text_size)
        y = get_y(text_size)
        for dictionary in not_empty:
            keys = list(dictionary.keys())
            values = list(dictionary.values())
            while x in keys and y in values:  # checking whether the current x,y is already in use
                x = get_x(text_size)       # if yes, generating a new x, y
                y = get_y(text_size)
        draw.text((x, y), i.text, fill=fill, font=font)  # the actual drawing of the text
        xr = range(x, x+text_size[0])  # all x coordinates of a single piece of text
        yr = range(y, y+text_size[1])  # all y coordinates ~
        not_empty.append({xr: yr})  # saving all used coordinates to a list

    name = 'out_{}.png'.format(filename)  # every generated image is saved with the name the function is called
    img.save(name)
    img.show()
    return img
