import random as rd
from abc import ABC, abstractmethod

class IVojak(ABC):
    @abstractmethod
    def __init__(self, jmeno, hp, atk, def_):
        pass

    @abstractmethod
    def bojuj(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

class Vojak(IVojak):
    def __init__(self, jmeno, hp, atk, def_):
        self.jmeno = jmeno
        self.hp = hp
        self.atk = atk
        self.def_ = def_

class Kopijnik(Vojak):
    def __init__(self, jmeno, hp, atk, def_):
        super().__init__(jmeno, hp, atk, def_)
    
    def bojuj(self):
        print(f"{self.jmeno} útočí s kopím!")
        if rd.random() < 0.33:
            return rd.randint(self.atk + 6 - 2, self.atk + 6 + 2)
        else:
            return rd.randint(self.atk - 2, self.atk + 2)
        
class Lucisnik(Vojak):
    def __init__(self, jmeno, hp, atk, def_):
        super().__init__(jmeno, hp, atk, def_)
        self.sipy = rd.randint(5, 10)  # Počet šípů
    
    def bojuj(self):
        if self.sipy > 0:
            print(f"{self.jmeno} útočí s lukem!")
            self.sipy -= 1
            return rd.randint(self.atk - 1, self.atk + 1)
        else:
            print(f"{self.jmeno} nemá žádné šípy!")
            return self.atk // 3

class Mag(Vojak):
    def __init__(self, jmeno, hp, atk, def_):
        super().__init__(jmeno, hp, atk, def_) 
    
    def bojuj(self):
        print(f"{self.jmeno} útočí s magií!")
        return rd.randint(self.atk - 5, self.atk + 5)


class bojiste():
    def __init__(self, seznam_vojaku):
        self.seznam_vojaku = seznam_vojaku
        self.vitez = None
        self.porazeny = None

    def bitva(self):
        print("Bitva začíná!")
        while len(vojak1.seznam_vojaku) > 1:
            # Vyber náhodné dva vojáky
            vojak1 = rd.choice(self.seznam_vojaku.seznam_vojaku)
            vojak2 = rd.choice(self.seznam_vojaku.seznam_vojaku)
            while vojak1 == vojak2:
                vojak2 = rd.choice(self.seznam_vojaku.seznam_vojaku)

            # Vojáci bojují

            print(f"{vojak1.jmeno} bojuje s {vojak2.jmeno}")
            while vojak1.hp > 0 and vojak2.hp > 0:
                print(f"{vojak1.jmeno} útočí na {vojak2.jmeno}")
                if vojak1.atk > vojak2.def_:
                    vojak2.hp -= (vojak1.atk - vojak2.def_)
                    print(f"{vojak1.jmeno} zasáhl {vojak2.jmeno}, zbývá mu {vojak2.hp} HP")
                else:
                    print(f"{vojak1.jmeno} nezasáhl {vojak2.jmeno}")
                
                if vojak2.hp <= 0:
                    print(f"{vojak2.jmeno} byl poražen!")
                    self.seznam_vojaku.remove(vojak2)
                    break
                
                print(f"{vojak2.jmeno} útočí na {vojak1.jmeno}")
                if vojak2.atk > vojak1.def_:
                    vojak1.hp -= (vojak2.atk - vojak1.def_)
                    print(f"{vojak2.jmeno} zasáhl {vojak1.jmeno}, zbývá mu {vojak1.hp} HP")
                else:
                    print(f"{vojak2.jmeno} nezasáhl {vojak1.jmeno}")
                
                if vojak1.hp <= 0:
                    print(f"{vojak1.jmeno} byl poražen!")
                    self.seznam_vojaku.remove(vojak2)
                    break

            # Odstraň poraženého z bitvy


        
        print(f"{vojak1.porazeny.jmeno} byl poražen!")
        print(f"Bitva skončila! Vítězem je {vojak1.vitez.jmeno} s {vojak1.vitez.hp} HP.")