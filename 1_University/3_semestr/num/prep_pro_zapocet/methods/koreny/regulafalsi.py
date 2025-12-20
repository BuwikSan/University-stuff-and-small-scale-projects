def regula_falsi(self, f, a, b, eps=0.0000001, max_iter=100000): 
    #pěkně na piču když kořen je zároveň inflexní bod to řeší třeba varianty Illinois, Pegasus, nebo Anderson-Björk
    if f(a)*f(b) > 0:
        raise Exception("Funkce nemá v intervalu kořen")
    
    iterace = 0
    while abs(b-a) > eps and iterace < max_iter:
        c = (a*f(b) - b*f(a)) / (f(b) - f(a))
        if abs(f(c)) < eps:  # Oprava: kontrola na malou hodnotu místo přesné nuly
            return c
        elif f(a)*f(c) < 0:
            b = c
        else:
            a = c
        iterace += 1
    # Oprava: přidán návrat nejlepší aproximace
    if iterace == max_iter:
        print("Nekonverguje v rozumném počtu iterací, ale vracím nejlepší aproximaci")
        return (a+b)/2
    else:
        return (a+b)/2