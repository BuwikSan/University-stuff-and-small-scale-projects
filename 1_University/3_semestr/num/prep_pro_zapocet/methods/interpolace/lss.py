from ..lin_rovnice.gausspivot import gauss_pivot
from ..lin_rovnice.gausssiedel import multiply_matrix_vector
from ..obecne_operace import transpose, multiply_matrices

def lss(a, y):
    """
    Řeší problém nejmenších čtverců pro soustavu Ax = y.
    Vrací vektor x, který minimalizuje ||Ax - y||^2.
    """
    # 1. Transpozice matice A -> A^T
    at = transpose(a)
    
    # 2. Součin A^T * A (vytvoří čtvercovou matici)
    ata = multiply_matrices(at, a)
    
    # 3. Součin A^T * y (vytvoří vektor pravé strany)
    aty = multiply_matrix_vector(at, y) # Funkce definovaná u Jacobiho/Gauss-Seidela
    
    # 4. Vyřešení soustavy (A^T * A) * x = A^T * y pomocí Gausse s pivotací
    return gauss_pivot(ata, aty)