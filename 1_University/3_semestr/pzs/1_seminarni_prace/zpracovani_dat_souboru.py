from pathlib import Path

import numpy as np
import pandas as pd
import wfdb  # local import to avoid hard dependency if not installed


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
        fs = fields.get("fs", fs_default)
        cols = fields.get("sig_name") or channel_names or [f"ch{i}" for i in range(sig.shape[1])]
        df = pd.DataFrame(sig, columns=cols)
        df.index = pd.RangeIndex(start=0, stop=len(df)) / float(fs)
        df.index.name = "time_s"
        print("wfdb", fs)
        return df
    except Exception:
        pass


    # tohle neřeš se to stejně nepoužije
    # -------------------------------------------------------------------------------------------------------------------------
    print("načtení pomocí wfdb selhalo")
    # fallback: read raw bytes and interpret as little-endian signed 16-bit
    raw = path.read_bytes()
    # skip BOM if present (some .dat from download may include BOM/text header)
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff") or raw.startswith(b"\xef\xbb\xbf"):
        # remove common BOMs
        if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
            raw = raw[2:]
        elif raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]

    try:
        arr = np.frombuffer(raw, dtype="<i2")  # little-endian int16
    except Exception:
        arr = np.frombuffer(raw, dtype=np.int16)

    if arr.size == 0:
        return pd.DataFrame()

    # determine number of channels
    if n_channels is None:
        # try to guess common channel counts: 3 or 2
        for guess in (3, 2, 1):
            if arr.size % guess == 0:
                n_channels = guess
                break
        else:
            n_channels = 1

    n_samples = (arr.size // n_channels) * n_channels
    if n_samples != arr.size:
        arr = arr[:n_samples]

    arr = arr.reshape(-1, n_channels)
    names = channel_names if channel_names and len(channel_names) == n_channels else [f"ch{i}" for i in range(n_channels)]
    df = pd.DataFrame(arr, columns=names)
    df.index = pd.RangeIndex(start=0, stop=len(df)) / float(fs_default)
    df.index.name = "time_s"
    return df
    # -----------------------------------------------------------------------------------------------------------





if __name__ == "__main__":
    
    current_dat_file = "charis6"
    base = Path(__file__).resolve().parent
    file_path = base / "data" / f"{current_dat_file}.dat"
    
    # example: provide channel names if known for this dataset
    try:
        df = read_record_to_df(file_path, channel_names=["ecg", "abp", "icp"], fs_default=250)
        print(df.head(10))
        print(df.tail(10))
        print(df.describe().loc[["min", "max"]])
    except Exception as e:
        print("read error:", e)
