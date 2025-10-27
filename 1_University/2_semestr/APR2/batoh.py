from random import randint
dva_batohy = [[],[]]
for batoh in dva_batohy:
    for j in range(10):
        rand = randint(0, 1)
        batoh.append(rand)

print(dva_batohy[0], dva_batohy[1])

def promixuj_batohy(dva_batohy):
    # promíchej batohy
    # vrátí dva nové batohy
    # batoh1L + batoh2R, batoh2L + batoh1R
    rand = randint(0, 10)
    batoh1L = dva_batohy[0][rand:]
    batoh2L = dva_batohy[1][rand:]
    batoh1R = dva_batohy[0][:rand]
    batoh2R = dva_batohy[1][:rand]