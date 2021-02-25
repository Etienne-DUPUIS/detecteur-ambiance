import os
import time

import pandas as pd

log_root = "log/"
log_path = os.path.join(log_root, time.ctime())
data_file_name = "sensor_data.csv"


def write_data(df):
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    file_path = os.path.join(log_path, data_file_name)
    with open(file_path, 'w+') as file:
        file.write(df.to_csv())
    return file_path

record = False


def record_and_save(recordMethod):
    global record
    if not record:
        record = True
        data = recordMethod
        write_data(data)
        print("Data written at {}".format(log_path))
        record = False
    else:
        print("Recording is already in progress")


def record_data(timeout_s, sensor_read_callback, ids, other_callback=None, target=None, target_ids=None):
    tic = time.time()
    df = None
    while time.time() - tic < timeout_s:
        timestamp, data = sensor_read_callback()
        if other_callback:
            other_callback()
        df = append_data(
            df, {
                **{"timestamp": timestamp},
                **{ids[i]: value for i, value in enumerate(data)},
                **{target_ids[i]: t_i() for i, t_i in enumerate(target)}
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
