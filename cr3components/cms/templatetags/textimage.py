from django import template
from django.template import Node, NodeList, Template, RequestContext, Variable
from PIL import ImageFont, ImageDraw, Image
import os
from django.conf import settings

register = template.Library()


FONT_DIR = getattr(settings,"FONT_DIR",settings.MEDIA_ROOT)


def _textimage(text, width, height, bg_color, color, font_name, font_size, upload_to, transpose):
    font_size = int(font_size)
    try:
        f_transpose = int(transpose)
    except:
        f_transpose = None
    
    safe_bg_color = bg_color.split("#")[1]
    safe_color = color.split("#")[1]
    
    textimage_dir = os.path.join(settings.MEDIA_ROOT, upload_to)
    font_filename = os.path.join(FONT_DIR,font_name)
    textimage_filename = "%sx%s-%s-%s-%s-%i-%s-%s.jpeg" % (width,height,safe_bg_color,safe_color,font_name,font_size,transpose,text)
    textimage_path = os.path.join(textimage_dir, textimage_filename)
    textimage_url = "%s%s/%s" % (settings.MEDIA_URL,upload_to,textimage_filename)  
    

    if not os.path.exists(textimage_dir):
        os.mkdir(textimage_dir)

    if not os.path.exists(textimage_path):
        font = ImageFont.truetype(font_filename, font_size)
        (t_width,t_height) = font.getsize(text)
        if width == "x":
            f_width = t_width
        else:
            f_width = int(width)
        if height == "x":
            f_height = t_height
        else:
            f_height = int(height)

        image = Image.new("RGBA",[f_width,f_height],bg_color)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font,fill=color)
        if f_transpose is not None:
            image = image.transpose(f_transpose)
        (f_width,f_height) = image.size
        image.save(textimage_path, "PNG")
    else:
        image = Image.open(textimage_path)
        (f_width,f_height) = image.size

    return (textimage_url,f_width,f_height)
    

@register.filter
def textimage(text, arg):  
    width, height, bg_color, color, font_name, font_size, upload_to, transpose = [a.strip() for a in  arg.split(',')]
    return _textimage(text, width, height, bg_color, color, font_name, font_size, upload_to, transpose)[0]



class TextImageNode(template.Node):
    
    def __init__(self, text, width, height, bg_color, color, font_name, font_size, upload_to, transpose):
        self.text = text
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.color = color
        self.font_name = font_name
        self.font_size = font_size
        self.upload_to = upload_to
        self.transpose = transpose


    def render(self, context):
        if self.text[0] == self.text[-1] == '"' or self.text[0] == self.text[-1] == "'":
            text = self.text[1:-1]
        else:
            text = Variable(self.text).resolve(context)
        (textimage_url,f_width,f_height) = _textimage(text, self.width, self.height, self.bg_color, self.color, self.font_name, self.font_size, self.upload_to, self.transpose)
        return '<img width="%i" height="%i" alt="%s" border="0" src="%s"/>' % (f_width,f_height,text,textimage_url)


@register.tag("textimage")
def textimage_tag(parser, token):
    """
    {% textimage text width height bg_color color font_name font_size upload_to %}
    """
    bits = token.contents.split()
    try:
        (tag_name, text, width, height, bg_color, color, font_name, font_size, upload_to, transpose) = bits
        return TextImageNode(text, width, height, bg_color, color, font_name, font_size, upload_to, transpose)
    except:
        raise template.TemplateSyntaxError, "%r tag requires 8 arguments" % token.contents.split()[0]
    
