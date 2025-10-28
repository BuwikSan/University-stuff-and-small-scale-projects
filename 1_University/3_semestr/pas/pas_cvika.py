
import matplotlib.pyplot as plt
import numpy as np
import pas_file_handling as pasfh



def cvika_2():
    duvera_data_raw = pasfh.read_RData_file(fr'1_University\3_semestr\pas\data\Duvera_24.RData')
    #okresy_data = pyreadr.read_r(fr'1_University\3_semestr\pas\Okresy03.RData')
    print(duvera_data_raw)
    print(duvera_data_raw.keys())
    duvera_data = duvera_data_raw["Duvera"]
    print(type(duvera_data))


    sloupecky = duvera_data.keys()
    print(sloupecky)
    """
    Index(['ID', 'IDE_2', 't_VEK_6', 'IDE_8', 'B2', 'VZD', 'VSO', 'NUTS2', 'NUTS3',
        't_ZIVUR', 'OV_1', 'IDE_1', 'PI_1a', 'PI_1b', 'PI_1c', 'PI_1d', 'PI_1e',
        'PI_1f', 'PI_1p', 'PI_1q', 'PI_1z', 'PI_1aa', 'PI_1ab', 'PO_45a'],
        dtype='object')
    """

    uniqe_dict = dict()
    def frekvencni_rozdeleni():
        print(duvera_data["t_VEK_6"])
        for data in duvera_data["t_VEK_6"]:
            if data not in uniqe_dict.keys():
                uniqe_dict[f"{data}"] = [0, 0, 0, 0]
            else:
                uniqe_dict[f"{data}"] += 1
        datacount = 0
        for data in uniqe_dict.values():
            data[1] = datacount + data[0]
            datacount += 1

        for data in uniqe_dict.values():
            data[2] = data[0]/uniqe_dict[-1][1]
            data[3] = data[1]/uniqe_dict[-1][1]

def cvika_4():
    ...
#print(okresy_data)

if __name__ == "__main__":
    path = fr'1_University\3_semestr\pas\data\Okresy03.RData'
    try:
        results = pasfh.read_RData_file(path)
        print(results)
    except Exception as e:
        print("Error:", e)