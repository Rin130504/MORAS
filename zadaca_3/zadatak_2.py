class Parser:
    
     def __init__(self, filename):
        # Otvaramo input asemblersku datoteku.
        try:
            self._file = open(filename + ".asm", "r")
        except:
            Parser._error("File", -1, "Cannot open source file")
            return

        # Linije iz input datoteke upisujuemo u ovu listu.
        self._lines = []
        
        # Citamo input datoteku.
        try:
            self._read_lines()
        except:
            Parser._error("File", -1, "Cannot read source file.")
            return

        # Pogreske prilikom parsiranja.
        self._flag = True # Ukoliko je flag postavljen na False, parsiranje je neuspjesno.
        self._line = -1   # lokacija (broj linije) na kojoj se pogreska nalazi.
        self._errm = ""   # Poruka koja opisuje pogresku.

        self._nest = 0

        # Parsiramo linije izvornog koda.
        self._parse_lines()
        if self._flag == False:
            Parser._error("PL", self._line, self._errm)
            return
        
        # oznake
        self._labels = {}
        self._variables = {}


        self._parse_macros()
        if self._flag == False:
            Parser._error("$", self._line, self._errm)
            return

        
        self._parse_symbols()
        if self._flag == False:
            Parser._error("SYM", self._line, self._errm)
            return
            
        self._parse_commands()
        if self._flag == False:
            Parser._error("COM", self._line, self._errm)
            return
            
        # Na kraju parsiranja strojni kod upisujemo u ".hack" datoteku.
        try:
            self._outfile = open(filename + ".hack", "w")
        except:
            Parser._error("File", -1, "Cannot open output file")
            return

        try:
            self._write_file()
        except:
            Parser._error("File", -1, "Cannot write to output file")
            return          

    # Funkcija koja cita input datoteku te svaki redak sprema u listu uredjenih
    # trojki kojima su koordinate
    #   1. originalna linija iz datoteke
    #   2. broj linije u parsiranoj datoteci (u pocetku isti kao 3.)
    #   3. broj linije u originalnoj datoteci
    def _read_lines(self):
        n = 0
        for line in self._file:
            self._lines.append((line, n, n));
            n += 1

    # Funkcija upisuje parsirane linije u output ".hack" datoteku.
    def _write_file(self):
        for (line, p, o) in self._lines:
            self._outfile.write(line)
            if (line[-1] != "\n"):
                self._outfile.write("\n")

    # Funkcija iterira procitanim linijama i na svaku primjenjuje funkciju
    # "func". Funkcija "func" vraća string koji odgovara vrijednosti parsirane
    # linije.
    #
    # Primjer:
    # ("@END", 4, 4) postaje ("@3", 3, 4)
    #
    # Ukoliko je duljina vracene linije 0, tu liniju brisemo. Takodjer, svaka
    # funkcija "func" mora se brinuti o pogreskama na koje moze naici (npr.
    # viselinijski komentari koji nisu zatvoreni ili pogresna naredba M=B+1).


def _iter_lines(self, func):
    newlines = []
    i = 0
    for (line, p, o) in self._lines:
        _func = func(line, p, o)
        if (self._flag == False):
                break
       
        if isinstance(_func, list):
            for l in _func:
                if len(l) > 0:
                    newlines.append((l, i, o))
                    if l[0] != "(":
                        i += 1

        else:
            newline = _func
            if len(newline) > 0:
                newlines.append((newline, i, o))
                if newline[0] != "(":
                    i += 1
    
    self._lines = newlines
    
        
    @staticmethod
    def _error(src, line, msg):
        if len(src) > 0 and line > -1:
            print("[" + src + ", " + str(line) + "] " + msg)
        elif len(src) > 0:
            print("[" + src + "] " + msg)
        else:
            print(msg)  








#Macros
def _parse_macros(self):
    """Iterira kroz linije koda i procesira makro naredbe."""
    self._iter_lines(self._parse_macro)

def _mv(self, A, B):
    """Kopira vrijednost iz A u B."""
    return [
        "@" + A, "D=M", 
        "@" + B, "M=D"
    ]

def _swp(self, A, B):
    """Zamjenjuje sadržaj između A i B."""
    return [
        "@temp", "M=0", 
        "@" + A, "D=M", 
        "@temp", "M=D", 
        "@" + B, "D=M", 
        "@" + A, "M=D", 
        "@temp", "D=M", 
        "@" + B, "M=D"
    ]

def _add(self, A, B, D):
    """Zbraja A i B i sprema rezultat u D."""
    return [
        "@" + A, "D=M", 
        "@" + B, "D=D+M", 
        "@" + D, "M=D"
    ]

def _while(self, A):
    """Pokreće WHILE petlju koja se ponavlja dok RAM[A] nije 0."""
    self._nest += 1
    return [
        "(WHILE" + str(self._nest) + ")", 
        "@" + A, "D=M", 
        "@END" + str(self._nest), "D;JEQ"
    ]

def _parse_macro(self, line, o, p):
    """Razdvaja makro naredbe i pretvara ih u asemblerski kod."""
    if line[0] == "$":
        command = line[1:].split("(")
        macro = command[0]

        if len(command) > 1:
            args = command[1]
            args_list = args.replace(")", "").split(",")
            
            if macro == "MV":
                return self._mv(args_list[0], args_list[1])
            
            elif macro == "SWP":
                return self._swp(args_list[0], args_list[1])
            
            elif macro == "ADD":
                return self._add(args_list[0], args_list[1], args_list[2])

            elif macro == "WHILE":
                return self._while(args_list[0])

            else:
                self._flag = False
                self._line = o
                self._errm = "No command named '" + macro + "'"
                return ""
        
        if macro == "END":
            lines = [
                "@WHILE" + str(self._nest), 
                "0;JMP",
                "(END" + str(self._nest) + ")"
            ]
            self._nest -= 1
            return lines
    else:
        return line
