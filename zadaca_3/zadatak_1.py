def _parse_lines(self):
    self._comment = False    
    self._iter_lines(self._parse_line)



def _parse_line(self, line, p, o):
    l = ""
    i = 0
    while i < len(line) - 1:
        p = line[i] + line[i + 1]

        if (self._comment == False and p == "/*") or (self._comment and p == "*/"):
            self._comment = not self._comment
            i += 1
        elif self._comment == False and p == "*/":
            self._flag = False
            self._line = o
            self._errm = "Unbalanced comment delimiter"
        elif (p == "//"):
            break
        elif line[i].isspace() == False and self._comment == False:
            l += line[i]
        


        if line[0] == "@" & line[1] in "0123456789":
            if int(line[1:])  > 24576:
                self._flag = False
                self._line = 0
                self._errm = "Number is not in the range of avalible adresses."

        i += 1
    return l 