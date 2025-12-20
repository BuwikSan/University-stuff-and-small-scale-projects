import copy

def gauss_lu(m):
    """
    Provede LU rozklad matice m v místě (in-place).
    Vrací matici, kde pod diagonálou je matice L a na diagonále + nad ní je matice U.
    """
    # Vytvoření hluboké kopie matice (odpovídá m.Copy() v Go)
    # Abychom nezměnili původní matici, kterou jsme do funkce poslali
    a = [row[:] for row in m]
    
    n = len(a)
    if n == 0 or n != len(a[0]):
        print("Error: Mismatched lengths (matrix must be square)")
        return None

    for k in range(n - 1):
        # Kontrola nulového pivota (dělení nulou)
        if a[k][k] == 0:
            print("Error: zero pivot encountered in GaussLU")
            return None

        for i in range(k + 1, n):
            # Výpočet multiplikátoru
            c = -a[i][k] / a[k][k]
            
            # Uložení prvku matice L (původně tam byla nula)
            # Všimni si, že v Go máš a[i][k] = -c
            a[i][k] = -c
            
            # Úprava zbytku řádku pro matici U
            for j in range(k + 1, n):
                a[i][j] += c * a[k][j]
                
    return a