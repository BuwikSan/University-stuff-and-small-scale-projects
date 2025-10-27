# magicke metody (__add__)
# iterátorové metody (__iter__, __next__)
class SFXFightSound:
    def __init__(self):
        self.zvuky = ["Bang", "prásk", "říz"]
        self.index = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.zvuky):
            zvuk = self.zvuky[self.index]
            self.index += 1 
            return zvuk
        else:
            self.index = 0
            raise StopIteration
        
def sfx_fight_sound(n):
    zvuky = ["Bang", "prásk", "říz"]
    index = 0
    akt_zvuk = 0
    while akt_zvuk < n:
        yield zvuky[index]
        index = (index + 1) % len(zvuky)
        akt_zvuk += 1

def main():   
    print("OOP zvuky ----")

    zvuky = SFXFightSound()

    for zvuk in zvuky:
        print(zvuk)

    print("Functional zvuky ----")

    for zvuk in sfx_fight_sound(10):
        print(zvuk)

if __name__ == "__main__":
    main()