import csv
from datetime import datetime
import os
import pandas as pd

import numpy as np

import matplotlib.pyplot as plt


def form_patient_data(dataframe):
    patient_data = dict()  # nparray (patient)x(features)
    print(f"[{datetime.now()}] Processing started")
    row_cnt = 0
    for index, row in dataframe.iterrows():
        if (row_cnt + 1) % 28013 == 0:
            percent = 100 * (row_cnt + 1) / dataframe.shape[0]
            print(f"[{datetime.now()}] Processing {row_cnt + 1} of {dataframe.shape[0]} ({percent:.5f}%)")

        if row.patient_id not in patient_data:
            patient_data[row.patient_id] = {"data": row, "date": index}
        else:
            data = patient_data[row.patient_id]["data"]
            r = row[5:-1]

            for i, item in enumerate(r):
                if not np.isnan(item):
                    data[i+5] = item  # глянуть если много занимает памяти/времени

            patient_data[row.patient_id] = {"data": data, "date": index}
        row_cnt += 1
    return patient_data


def normalize(data):
    with open("data3.csv", mode="w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")
        csv_writer.writerow(["id", "patient_id", "gender", "birthday", "age", "glucose_blood",
                             "glucose_urine", "HbA1C", "bilirubin_common", "bilirubin_direct", "bilirubin_indirect",
                             "systolic_bp", "diastolic_bp", "weight", "height", "real_target"])
        for i, patient in enumerate(data):
            data = data[patient]["data"].values.tolist()
            row = [i + 1, patient] + data
            csv_writer.writerow(row)


def show_df_info(file_name):
    df = pd.read_csv(file_name, delimiter=";", index_col="time_stamp").sort_values(by=['patient_id', 'time_stamp'])
    # print(df.head(100))
    df_isnull = df.isnull().astype(int)
    df_isnull[df_isnull.columns[5:-1]].hist()
    plt.legend(labels=df_isnull.columns[5:-1])
    plt.show()
    return df


# ,parse_dates=[11]
start = datetime.now()
df = show_df_info('data1.csv')
# print(df_isnull[df_isnull.columns[5:-1]].describe())
patient_data = form_patient_data(df)
normalize(patient_data)
# df = show_df_info('data3.csv')
diff = (datetime.now() - start)
print("stopped in ", diff.total_seconds(), "s")
