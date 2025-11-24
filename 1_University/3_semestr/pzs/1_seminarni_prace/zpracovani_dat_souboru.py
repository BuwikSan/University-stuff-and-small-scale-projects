from pathlib import Path

import numpy as np
import pandas as pd
import wfdb  # local import to avoid hard dependency if not installed

#------------------------------------- data extraction ----------------------------------------
def data_frequency_check(current_frequency, default_frequency):
    if current_frequency != default_frequency: raise Exception("frequency doesn't match the default value")

def read_record_to_df(path, channel_names=None, fs_default=500, n_channels=None):
    """
    Read a WFDB record (preferred) or fallback to raw interleaved int16 binary.
    Returns pandas.DataFrame with time index in seconds.
    - path: Path to the .dat file (or record base)
    - channel_names: optional list of names
    - fs_default: fallback sampling frequency if header missing
    - n_channels: if specified, override number of channels for binary fallback
    """
    path = Path(path)
    # try wfdb first
    try:
        record_base = str(path.with_suffix(""))
        sig, fields = wfdb.rdsamp(record_base)
        fs = fields.get("fs")
        data_frequency_check(fs, 50)
        cols = fields.get("sig_name") or channel_names or [f"ch{i}" for i in range(sig.shape[1])]
        df = pd.DataFrame(sig, columns=cols)
        df.index = pd.RangeIndex(start=0, stop=len(df)) / float(fs)
        df.index.name = "time_s"
        return df
    except Exception:
        raise Exception("I CAN'T READ T_T")


# ------------------------------------------------data operations -------------------------------------------------------






# ----------------------------------------------- main -----------------------------------------------------------------
if __name__ == "__main__":
    
    current_dat_file = "charis6"
    base = Path(__file__).resolve().parent
    file_path = base / "data" / f"{current_dat_file}.dat"

    try:
        df = read_record_to_df(file_path, channel_names=["ecg", "abp", "icp"], fs_default=250)
        print(df.head(10))
        print(df.tail(10))
        print(df.describe().loc[["min", "max"]])
        print(df.keys())
    except Exception as e:
        print("read error:", e)
