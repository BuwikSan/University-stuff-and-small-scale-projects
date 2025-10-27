
# quick sort

#1. vybírám pivot př 3
#2. dva seznamy menší a větší než pivot (naplnim)
#3. return 
list = [3,1,5,2,4,9,8,7,4,3,2,6,0]
def q_sort(s):
    if len(s) < 2: return s
    p = s.pop(0)
    mnp = [obj for obj in s if obj < p]
    vnp = [obj for obj in s if obj >= p]
    return q_sort(mnp) + [p] + q_sort(vnp) # změna pořadí KDYŽ PROHODIM STRANY MNP A VNP

def hepa_sort(list):
    def hop_up(list, i):
        if list[i] > list[(i - 1)//2] and i > 0:
            list[i], list[(i - 1)//2] = list[(i - 1)//2], list[i]
            return hop_up(list, (i - 1)//2)
        
    def hop_down(list, i, sorted_elements):
        if (i*2 + 2) < (len(list) - sorted_elements):
            if list[i*2 + 1] > list[i*2 + 2]: b = 1 
            else: b = 2
            
            if list[i] < list[i*2 + b]:
                list[i], list[i*2 + b] = list[i*2 + b], list[i]
                return hop_down(list, i*2 + b, sorted_elements)

    for i in range(1, len(list)):
        hop_up(list, i)
    
    sorted_elements = 0

    while (sorted_elements) < len(list):
        hop_down(list, 0, sorted_elements)
        sorted_elements += 1
        list[0], list[-sorted_elements] = list[-sorted_elements], list[0]

    return list
print(hepa_sort(list))
list = [3,1,5,2,4,9,8,7,4,3,2,6,0]
print(q_sort(list))


def m_sort(list):
    ...