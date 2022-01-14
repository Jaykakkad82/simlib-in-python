import pandas as pd
import os
import sys
import csv

def read_csv(file_location):
    df = pd.read_csv(file_location)
    return df


def write_csv(output_file_name):
    open(output_file_name, 'w+', newline='')