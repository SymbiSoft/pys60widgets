# -*- coding: cp1252 -*-
# (c) Marcelo Barros de Almeida
# marcelobarrosalmeida@gmail.com
# License: GPL3

from graphics import Image

def canvas_split_text(self, text, width, font="normal", line_break=u" .;:\\/-"):
    """ Split a text in several line given the desired size and fonts.
        Modified version of TextRenderer.chop for splitting text
        http://discussion.forum.nokia.com/forum/showthread.php?t=124666
    """
    lines = []
    text_left = text
    while len(text_left) > 0: 
        bounding, to_right, fits = Image.new((1,1)).measure_text(text_left,
                                                                 font=font,
                                                                 maxwidth=width,
                                                                 maxadvance=width)
        if fits <= 0:
            lines.append(text_left)
            break

        slice = text_left[0:fits]
        adjust = 0 # (preserve or not whitespaces at the end of the row)
    
        if len(slice) < len(text_left):
            # find the separator character closest to the right
            rindex = -1
            for sep in line_break:
                idx = slice.rfind(sep)
                if idx > rindex:
                    rindex = idx
            if rindex > 0:
                if slice[rindex] == u' ':
                    adjust = 1
                slice = slice[0:rindex]

        lines.append(slice)
        text_left = text_left[len(slice)+adjust:]
    
    return lines
