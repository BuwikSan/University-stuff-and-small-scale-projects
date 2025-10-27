#already made (nebudu importovat z poznámkovýho souboru a novej dělat nebudu)
class QueueStackAbstract:
    def __init__(self):
        self.data = []
    
    def _front(self):
        return self.data[-1] 
    def _rear(self):
        return self.data[0]
    def _size(self):
        return len(self.data)
    def is_empty(self):
        return True if self._size() == 0 else False
    
    def dequeue(self):
        if self._size() >= 0:
            return self.data.pop()
    
class Queue(QueueStackAbstract):
    def enqueue(self, item):
        self.data.insert(0, item)
    
    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"Queue({self.data})"
 
class Stack(QueueStackAbstract):
    def enstack(self, item):
        self.data.append(item)
    
    def __repr__(self):
        return f"Stack({self.data})"
#already made







class UzelStromu():
    def __init__(self, data, rodic=None, kolikate_dite=None, vztah_s_rodicem=None, deti=None):
        self.payload = data
        self.rodic = rodic
        #self.kolikate_dite = kolikate_dite
        self.edge_data = vztah_s_rodicem
        self.deti = deti if deti is not None else list()
    
    #metody pouze pro metody
    def iteruj_skrz_deti_a_udelej(self, metoda):
        for dite in self.deti:
            if dite.deti == [] or dite.deti == None:
                dite.metoda
            else:
                for dite_ditete in dite.deti:
                    dite_ditete.metoda
                dite.metoda

    def bf_fill_queue(self, queue):
        for dite in self.deti:
            if dite.edge_data == None:
                queue.enqueue(dite)
                dite.edge_data = False
            else:
                dite.bf_fill_queue(queue)


    #output metody
    def pridej_informace_do_hrany():
        ...

    def pridej_nove_dite(self, data):
        self.deti.append(UzelStromu(data, self, len(self.deti)))
        return self.deti[len(self.deti)-1]
    
    def pridej_strom(self, strom):
        self.deti.append(strom)
        strom.rodic = self
        strom.kolikate_dite = len(self.deti)


    def vrat_rodice(self):
        return self.rodic
    
    def vrat_predchudce(self, predchudci=None):
        if predchudci == None:
            predchudci = list()
        if self.vrat_rodice() == None:
            return predchudci
        else:
            predchudci.append(self.rodic)
            self.rodic.vypis_predchudce(predchudci)
    
    def vrat_deti(self):
        return self.deti

    def vrat_potomky(self, potomci=None):
        if potomci == None:
            potomci = list()
        if self.vrat_deti == []:
            return potomci
        else:
            potomci += self.vrat_deti()
            for dite in self.vrat_deti():
                dite.vrat_potomky(potomci)


    def odpoj_a_vrat_dite(self, index=None, data=None):
        if data == None and index == None:
            return self.deti.pop()
        elif index != None and index != None:
            raise Exception("Asi jsi nečetl dokumentaci kterou jsem neudělal, nevadí. nedávej tam index i data")
        elif index != None:
            return self.deti.pop(index)
        elif data != None:
            for dite in self.deti:
                if dite.data == data:
                    returning_data = dite
                    self.deti.remove(data)
                    return returning_data

    def odstran_hranovou_informaci(self):
        self.edge_data = None

    def odstan_vsechny_hranove_informace(self):
        self.iteruj_skrz_deti_a_udelej(self.odstran_hranovou_informaci())

    def odpal_se(self):
        self.payload = None
        self.rodic = None
        self.edge_data = None
        self.deti = None
        self.rodic.deti.remove(self)

    def odpal_rekurzivne_dite(self, jaky): #FIXME jaky je atm objekt, ale jaky by se mělo spíš vyhledat pomocí už hotové funkce
        jaky.iteruj_skrz_deti_a_udelej(self.odpal_se())
        jaky.odpal_se()
    
    ##search metody
    def df_search(self, co_hledam, root=None):
        if root == None:
            root = self
            root.edge_data = list()
        if co_hledam == self.payload:
            root.edge_data.append(self)
        
        if self.deti != None and self.deti != []:
            for dite in self.deti:
                if root.edge_data != []:
                    vysledek = root.edge_data[:]
                    root.edge_data = None
                    return vysledek[0]
                dite.df_search(co_hledam, root)

    def bf_search(self, co_hledam):
        if co_hledam == self.payload:
            return self
        nalezeno = False
        queue = Queue()
        while not nalezeno:
            self.bf_fill_queue(queue)
            print(queue)
            if len(queue) == 0:
                break
            while len(queue) > 0:
                item = queue.dequeue()
                if item.payload == co_hledam:
                    #self.odstan_vsechny_hranove_informace()
                    return item
                
        #self.odstan_vsechny_hranove_informace()
        return None
            

    def __repr__(self):
        return self.payload
        #TODO jo, tohle je k hovnu kod zatim
        #return str(self.data) + "," + str(self.rodic) + "," + str(self.vrat_deti)
        ...
    def konstrukce_ze_Stringu(self):
        #TODO nejdrive repr, pak nad tim muzu uvazovat
        ...


prvniuzlik = UzelStromu(data="a")
print(list())
print(prvniuzlik.vrat_predchudce())
print(prvniuzlik.vrat_potomky())

b = prvniuzlik.pridej_nove_dite("b")
c = prvniuzlik.pridej_nove_dite("c")
d = prvniuzlik.pridej_nove_dite("d")
e = b.pridej_nove_dite("e")
f = b.pridej_nove_dite("f")
g = b.pridej_nove_dite("g")
h = c.pridej_nove_dite("h")
i = c.pridej_nove_dite("i")
j = c.pridej_nove_dite("j")
k = d.pridej_nove_dite("k")
l = d.pridej_nove_dite("l")
m = d.pridej_nove_dite("m")
print("testy")
print(prvniuzlik.vrat_deti())
print(b.vrat_deti())
print(c.vrat_deti())
print(d.vrat_deti())
print("df test")
print(prvniuzlik.df_search("j"))
print("bf test")
print(prvniuzlik.bf_search("j"))

## du - jak budu mit strom done, tak:
    ## prohledávání do hloubky a prohledávání do šířky (DFS a BFS)


### "Testy... K čemu?!" - Burymuru 2025