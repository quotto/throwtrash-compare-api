# app/dataset/taigigo.csvの1カラム目と2カラム目の対義語を入れ替えて元のファイルに追記する
import sys
import csv
import os
import pandas as pd

def swap(taigo_csv_file):
    df = pd.read_csv(taigo_csv_file)
    df_swap = pd.DataFrame(columns=df.columns)
    for index,rows in df.iterrows():
        series = pd.Series([rows.iloc[1],rows.iloc[0]],index=df.columns)
        df_swap = pd.concat([df_swap,series.to_frame().T])
    df_swap.to_csv(taigo_csv_file,mode='a',header=False,index=False)
    print(f"complete swap {df_swap.size} pairs")

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print("Usage: python swap_taigigo.py taigigo.csv")
        quit()
    print(f"start swap {args[1]}...")
    taigo_csv_file = args[1]
    swap(taigo_csv_file)