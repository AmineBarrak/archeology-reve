#!/usr/bin/env python3

import PyPDF2
import sys
import os
from pathlib import Path
import pandas as pd





def main():
    PATH="../extracted_text/"
    files_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames if os.path.splitext(f)[1] == '.txt']
    my_df = []
    for file_path in files_paths:
        filename = Path(file_path).stem

        print("****************************************")
        print(filename)
        with open(file_path) as f:
            lines = f.read()


        d = {
            'filename' : filename,  # some formula for obtaining values
            'text' : lines,
        }
        my_df.append(d)

    my_df = pd.DataFrame(my_df)

    my_df.to_csv('../all_dataset.csv', index=False)



if __name__ == '__main__':
    main()