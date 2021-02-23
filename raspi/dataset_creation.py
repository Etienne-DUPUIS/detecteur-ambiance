import os
import time

import pandas as pd

log_root = "log/"
log_path = os.path.join(log_root, time.ctime() + ".csv")


def write_data(df):
    if not os.path.exists(log_root):
        os.makedirs(log_root)
    with open(log_path, 'w+') as file:
        file.write(df.to_csv())
    return log_path


def record_data(timeout_s, sensor_read_callback, ids):
    tic = time.time()
    df = None
    while time.time() - tic < timeout_s:
        timestamp, data = sensor_read_callback()
        df = append_data(
            df, {
                **{"timestamp": timestamp},
                **{ids[i]: value for i, value in enumerate(data)}
            }
        )
    return df


def append_data(data, data_dict):
    return pd.concat(
        [
            data, pd.DataFrame(
            data_dict, index=[0]
        )
        ], ignore_index=True
    )
