"""
Nomenclador para hospitales públicos de gestión descentralizada de Argentina
"""
import csv
import json
import os
import requests


class Drive:

    def _init__(self, name, uid, gid, force_re_download=False):
        """ starts with Unique Doc ID and page/tab ID """
        self.uid = uid
        self.gid = gid
        self.url_csv = 'https://docs.google.com/spreadsheets/d/{uid}/export?format=csv&gid={gid}'
        # download if not exists
        here = os.path.dirname(os.path.realpath(__file__))
        self.data_folder = os.path.join(here, 'tmpdata')
        self.local_csv = os.path.join(self.data_folder, f'{name}.csv')
        if force_re_download or not os.path.isfile(self.local_csv):
            self.download()
        self.read_csv()
    
    def download(self):
        req = requests.get(self.url_csv)
        if not os.path.isdir(self.data_folder):
            os.mkdir(self.data_folder)
        f = open(self.local_csv, 'wb')
        f.write(req.content)
        f.close()

    def read_csv(self):
        # read CSV and transfor to a useful JSON
        tree = {}   # results
        f = open(self.local_csv, 'r')
        reader = csv.DictReader(f)
        
        c = 0  # codigo unico (no hay otro)
        
        for row in reader:
            # fix all shit
            for k, v in row.items():
                row[k] = v.strip()

            tree[c] = row
            c += 1

        f.close()

        self.tree = tree
        return tree
