from Bild import Bild


class Artikel:
    code = None
    beschreibung = None
    anzahl = None
    einkaufspreis = None
    verkaufspreis = None
    einfuehrungsdatum = None
    bilder = list()
    json = None

    def __init__(self, json):
        self.code = json['code']
        self.beschreibung = json['beschreibung']
        self.anzahl = json['anzahl']
        self.einkaufspreis = json['einkaufspreis']
        self.verkaufspreis = json['verkaufspreis']
        self.einfuehrungsdatum = json['einfuehrungsdatum']
        self.json=json
        for b in json['bilder']:
            self.bilder.append(b)
            print(self.bilder)

    def hatFehler(self):
        ret = False;
        print(ret)
        if self.code is not None:
            print("k")
            self.code = self.code.upper()
        if self.beschreibung is None:
            ret = True
        if self.anzahl is None:
            ret = True
        if self.einkaufspreis is None:
            ret = True
        if self.verkaufspreis is None:
            ret = True
        if self.einfuehrungsdatum is None:
            ret = True
        if self.bilder is None:
            ret = True
        ret = ret | len(self.code) == 0 | (self.code.startswith("IT") & len(self.code) != 8) |(self.code.startswith("DE") & len(self.code) != 10);

        #ret = ret | (not self.code.startswith("IT") and not self.code.startswith("DE"))
        #print("hier?"+str(ret)) ToDO
        ret = ret | len(self.beschreibung) == 0

        ret = ret | self.anzahl < 0

        ret = ret | int(self.einkaufspreis) < 0

        ret = ret | int(self.verkaufspreis) < 0

        ret = ret | int(self.einkaufspreis) > self.verkaufspreis

        ret = ret | len(self.bilder) == 0


        if not ret:
            for bild in self.bilder:
                if len(bild['url']) == 0:
                    ret = True
                elif bild is None:
                    ret = True
                #todo
        return ret
