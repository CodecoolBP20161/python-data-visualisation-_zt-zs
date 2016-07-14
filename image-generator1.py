from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random
from connect_db import sql_queries
from hex_to_rgb import hex_to_rgb


# very 'in progress'
class Text():
    QUERIES = [sql_queries()[0], sql_queries()[1]]
    def __init__(self, queries):
        self.fill = queries[2]
        self.size = queries[1]
        self.text = queries[0]
        # self.text_size = (1, 1)

    @classmethod
    def output_first(cls, queries):
        return [Text(queries) for queries in cls.QUERIES[0]]
    def output_second(cls, queries):
        return [Text(queries) for queries in cls.QUERIES[1]]



companiess = Text.output_first(sql_queries()[0])
projects = Text.output_first(sql_queries()[1])

img = Image.new("RGBA", (512, 512), "black")
draw = ImageDraw.Draw(img)

default_size = 10
try:
    font_path = "/usr/share/fonts/FreeSans.ttf"
    # font = ImageFont.truetype(font_path, default_size)
    font = ImageFont.truetype(font_path)

except:
    font = ImageFont.load_default()


# generating an x coordinate
def get_x(i):
    text_size = draw.textsize(i, font=font)  # text size according to the font size
    x = random.randint(0, (img.size[0]-text_size[0]))  # full width - horizontal size of text
    return x


# generating a y coordinate
def get_y(i):
    text_size = draw.textsize(i, font=font)
    y = random.randint(0, (img.size[1]-text_size[1]))  # full width - vertical size of text
    return y


# pasting doge in the center of the word cloud
def doge(img):
    import requests
    from io import BytesIO
    response = requests.get('http://i.imgur.com/P5t9JNF.png')
    doge = Image.open(BytesIO(response.content))
    # doge = Image.open("doge.png")
    doge.convert('RGBA')
    img.paste(doge, (img.size[0]//2-doge.size[0]//2, img.size[1]//2-doge.size[1]//2))


def print_text(datas):
    doge(img)
    x, y = 0, 0

    # a list for already used coordinates
    not_empty = []

    for i in datas:
        text_size = draw.textsize(i.text, font=font)
        x = get_x(i.text)
        y = get_y(i.text)
        # fill = i.fill
        try:
            if len(i.fill)==4:  # change when the colors are converted properly!!
                fill = i.fill
            else:
                fill = hex_to_rgb(i.fill)
        except:
            fill = "white"
        # fill = hex_to_rgb(i.fill)
        for dictionary in not_empty:
            keys = list(dictionary.keys())
            values = list(dictionary.values())
            while x in keys and y in values:  # checking whether the current x,y is already in use
                x = get_x(i.text)             # if yes, generating a new x, y
                y = get_y(i.text)

        draw.text((x, y), i.text, fill=fill, font=ImageFont.truetype(font_path, default_size+5*(i.size)))  # the actual drawing of the text

        xr = range(x, x+text_size[0])  # all x coordinates of a single piece of text
        yr = range(y, y+text_size[1])  # all y coordinates ~
        not_empty.append({xr: yr})  # saving all used coordinates to a list
    img.save('out.png')
    return img                      # keys are the range for x, values for y

# print_text(companiess)
print_text(projects)

img.show()
