import pyreadr
import matplotlib.pyplot as plt
import numpy as np
import pandas
import os


def read_RData_file(relative_path):
    def recursive_dataframe_search(obj, path=None, results=None, _depth=0, _max_depth=20):
        """
        DFS: najde všechny pandas.DataFrame nebo pandas.Series v zadaném objektu.
        Vrací seznam tuple (path_str, dataframe_or_series).
        """
        if results is None:
            results = []
        if path is None:
            path = []

        if _depth > _max_depth:
            return results

        # přímý DataFrame nebo Series
        if isinstance(obj, pandas.DataFrame) or isinstance(obj, pandas.Series):
            results.append((".".join(path) if path else "<root>", obj))
            return results

        # dict-like (pyreadr vrací OrderedDict)
        if isinstance(obj, dict):
            for k, v in obj.items():
                recursive_dataframe_search(v, path + [str(k)], results, _depth + 1, _max_depth)
            return results

        # list/tuple/set/ndarray: procházej podle indexu
        if isinstance(obj, (list, tuple, set)):
            for idx, v in enumerate(obj):
                recursive_dataframe_search(v, path + [f"[{idx}]"], results, _depth + 1, _max_depth)
            return results

        # numpy arrays nebo jiné primitivní typy ignorujeme
        try:
            # zkusíme inspekci atributů pouze bezpečně (vyhnout se callables)
            attrs = [a for a in dir(obj) if not a.startswith("_")]
        except Exception:
            attrs = []

        for attr in attrs:
            try:
                val = getattr(obj, attr)
            except Exception:
                continue
            if callable(val):
                continue
            # omezit průzkum velkých/běžných typů
            if isinstance(val, (str, bytes, int, float, bool)):
                continue
            recursive_dataframe_search(val, path + [str(attr)], results, _depth + 1, _max_depth)

        return results




    if not os.path.exists(relative_path):
        raise FileNotFoundError(f"File not found: {relative_path}")

    raw_output = pyreadr.read_r(relative_path)
    print("raw_output keys:", list(raw_output.keys()))

    found = recursive_dataframe_search(raw_output)
    if not found:
        print("No pandas DataFrame/Series found in the RData structure.")
        return []

    # výpis nalezených položek
    for path, df in found:
        print(f"Found at: {path}  type={type(df)}  shape={getattr(df, 'shape', None)}")
        print(f"with keys:{df.keys()}")

    return found

# def read_RData_file(relative_path):
#     def recursive_dataframe_search(collection):
#         for key in raw_output.keys():
#             output = raw_output[key]
#             if isinstance(output, pandas.core.frame.DataFrame) == True:
#                 print(type(output))
#                 break
#     raw_output = pyreadr.read_r(relative_path)
#     print("currently displaying: raw")
#     print(raw_output)
#     print(raw_output.keys())

#     print("currently displaying: clean")
#     print(fr"{output}")
#     print(output.keys())
#     return output




def cvika_2():
    duvera_data_raw = pyreadr.read_r(fr'1_University\3_semestr\pas\data\Duvera_24.RData')
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
    path = fr'1_University\3_semestr\pas\data\Policie.RData'
    try:
        results = read_RData_file(path)
        print(results)
    except Exception as e:
        print("Error:", e)