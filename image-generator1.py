from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random
from connect_db import sql_querys


# # very 'in progress'
# class Text():
#     outputs = sql_querys()
#     def __init__(self, outputs):
#         self.fill = outputs[0]
#         self.font = outputs[1]
#         self.size = outputs[2]
#         self.text = outputs[3]
#
#     @classmethod
#     def output(cls):
#         return [Text(output) for output in cls.outputs]

# all colors from the sql file for testing
colors = ['#852', '#d86', '#016', '#f98', '#3bb', '#77e', '#707', '#230', '#092',
          '#fd9', '#2fc', '#1e9', '#6ca', '#0dd', '#7ec', '#ad2', '#dc3', '#23c',
          '#bfe', '#f5b', '#831', '#f2f', '#79a', '#749', '#242', '#4c7', '#680',
          '#415', '#569', '#020', '#b9d', '#76b', '#781', '#09f', '#820', '#c2a',
          '#06c', '#e2f', '#7e8', '#063', '#2e4', '#acf', '#937', '#81e', '#048',
          '#b13', '#50c', '#b1f', '#fdc', '#8a8', '#9c7', '#083', '#f21', '#56f',
          '#c06', '#f9a', '#357', '#2d2', '#07e', '#807', '#3ae', '#34d', '#762',
          '#0c1', '#75a', '#dfc', '#d68', '#aee', '#66d', '#b24', '#1b1', '#b60',
          '#beb', '#ddf', '#030', '#d53', '#bc8', '#c43', '#d0e', '#67c', '#e04',
          '#42b', '#ba4', '#64c', '#953', '#c58', '#a67', '#23f', '#830', '#670',
          '#786', '#aa6', '#1ce', '#af7', '#4d6', '#679', '#263', '#d38', '#22a',
          '#296', '#f80']

img = Image.new("RGB", (512, 512), "white")
draw = ImageDraw.Draw(img)

# fix font size for now
size = 50
try:
    font_path = "/usr/share/fonts/FreeSans.ttf"
    font = ImageFont.truetype(font_path, size)
except:
    font = ImageFont.load_default()


# text_options = {
#     'fill': (255, 255, 255)
# }
#
# text_content = "Sample Text"
# text_size = draw.textsize(text_content)
# # draw.text((x, y),text_content,(r,g,b))
# draw.text((0, 0), text_content, **text_options)
# draw.text((0, text_size[1]), text_content, **text_options)
# draw.text((text_size[0], 0), text_content, **text_options)
# draw.text(text_size, text_content, **text_options)
# img.save('sample-out.png')


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

# a list for already used coordinates
not_empty = []
test_list = ["1company", "2project", "3budget", "4status"]
x, y = 0, 0

def print_text():
    for i in test_list:
        # font.size += 200
        text_size = draw.textsize(i, font=font)
        x = get_x(i)
        y = get_y(i)
        fill = colors[random.randint(0, len(colors)-1)]
        for d in not_empty:
            k = list(d.keys())
            v = list(d.values())
            if x in k or x in range(x, text_size[0]):  # checking whether the current x is already in use
                x = get_x(i)                           # if yes, generating a new x
            elif y in v or y in range(y, text_size[1]):  # same for y
                y = get_y(i)

        draw.text((x, y), i, fill=fill, font=font)  # the actual drawing of the text

        xr = range(x, x+text_size[0])  # all x coordinates of a single piece of text
        yr = range(y, y+text_size[1])  # all y coordinates ~
        not_empty.append({xr: yr})  # saving all used coordinates to a list
    return img                      # keys are the range for x, values for y

print_text()

img.save('out.png')
img.show()
