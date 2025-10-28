import pyreadr
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
