list = [0,5,1,2,4,1,6,9,8, 88, 654, 4657, 98, 12, 34, 75, 64, 445, 874, 345, 994, 654]

list.sort()
print(list)
def bin_search(sequence, object, anchor, iteration):
    iteration += 1
    print(len(sequence), anchor, sequence[anchor], object)

    if sequence[anchor] == object:
        print(anchor)
        return anchor
    elif object > sequence[anchor]:
        return bin_search(sequence, object, anchor + len(sequence)//((iteration+1)*2), iteration)
    else:
        return bin_search(sequence, object, anchor - len(sequence)//((iteration+1)*2), iteration)
        
    
print(bin_search(list, 9, len(list)//2, 0))