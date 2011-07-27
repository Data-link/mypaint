import re, os
# is importing os too heavyweight here? move the file test/open code into
# gui/filehandler?

from helpers import rgb_to_hsv, hsv_to_rgb

class GimpPalette(list):
    # loads a given gimp palette and makes it queriable
    # Would 'save' functionality be useful at some stage? 
    def __init__(self, filename=None):
        self.columns = 0
        self.scheme = "RGB"
        if filename:
            self.load(filename)

    def load(self, filename):
        if os.path.isfile(filename):
            fp = open(filename, "r")
            header = fp.readline()
            if header[:12] != "GIMP Palette":
                raise SyntaxError, "not a valid GIMP palette"
            
            limit = 500    # not sure what the max colours are in a Gimp Palette

            while (limit != 0):
                color_line = fp.readline()
            
                if not color_line:
                    # Empty line = EOF?
                    break
                # Skip comments
                if re.match("#", color_line):
                    continue

                # Name: value pairs
                if re.match("\w+:", color_line):
                    tokens = color_line.split(":")
                    if len(tokens) == 2:
                        if tokens[0].lower().startswith("columns"):
                            try:
                                val = int(tokens[1].strip())
                                self.columns = val
                            except ValueError, e:
                                print "Bad Column value: %s" % tokens[1]
                    continue
                try:
                    triple = tuple(map(int, re.split("\s+", color_line.strip())[:3]))
                    if len(triple) != 3:
                        # could be index
                        print "Is index?"
                        raise ValueError
                    self.append(triple)
                except ValueError,e:
                    # Bad Data will not parse as Int
                    print "Bad line in palette: '%s'" % color_line[:-1]

                limit -= 1
            fp.close()
            print "Loaded %s colors from palette %s" % (len(self), filename)

    def hsv(self, index):
        if index < 0 or index > (len(self)-1):
            return None  # should be Exception perhaps?
        else:
            return rgb_to_hsv(*map(lambda x: x / 255.0, self[index]))

    def rgb(self, index):
        if index < 0 or index > (len(self)-1):
            return None  # should be Exception perhaps?
        else:
            return map(lambda x: x / 255.0, self[index])
