from PIL import Image, ImageTk, ImageFont, ImageDraw
import inspect
import code

def check():
    current_frame = inspect.currentframe()
    caller_frame = current_frame.f_back
    caller_locals = caller_frame.f_locals
    caller_globals = caller_frame.f_globals
    for key in caller_globals:
        if key not in globals():
            globals()[key] = caller_globals[key]
    code.interact(local=dict(globals(), **caller_locals))

default_rgb = (79, 121, 66)

def code_rgb(rgb=default_rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb   

def create_clock_textimg(text):
    img = Image.new('RGB', (350, 100), color=default_rgb)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("src/radioland.ttf", 100)
    dotfont = ImageFont.truetype("src/radioland.ttf", 140)
    
    num_list = list(map(lambda x:int(text[x]), [0,1,3,4]))
    pos_list = [(-2, -5), (68, -5), (173, -5), (242, -5)]

    newtext = ''.join([text[x] if text[x]!='1' else '.1' for x in range(5)])
    # num37 = sum([1 for x in num_list if x in [3,7]])
    draw.text((5, 20), newtext, font=font, fill ="black")

    num37 = 0
    for num, pos in zip(num_list, pos_list):
        px, py = pos
        if num in [3, 7]:
            num37 += 1
        if num == 1:
            draw.text((px-num37*4, py), '.', font=dotfont, fill=default_rgb)
    phimg = ImageTk.PhotoImage(img)
    return phimg

if __name__ == '__main__':
    # x = 3
    # text = f'{x}{x}:{x}1'
    text = '33:13'
    # img = Image.new('RGB', (350, 100), color='white')
    img = Image.new('RGB', (350, 100), color=default_rgb)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("radioland.ttf", 100)
    dotfont = ImageFont.truetype("radioland.ttf", 140)
    
    
    num_list = list(map(lambda x:int(text[x]), [0,1,3,4]))
    pos_list = [(0, -5), (70, -5), (175, -5), (242, -5)]

    newtext = ''.join([text[x] if text[x]!='1' else '.1' for x in range(5)])
    # num37 = sum([1 for x in num_list if x in [3,7]])
    draw.text((5, 20), newtext, font=font, fill ="black")

    num37 = 0
    for num, pos in zip(num_list, pos_list):
        px, py = pos
        if num in [3, 7]:
            num37 += 1
        if num == 1:
            draw.text((px-num37*4, py), '.', font=dotfont, fill=default_rgb)

    img.show()