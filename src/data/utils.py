from pathlib import Path
import io
import zipfile
import pickle
import requests

import csv
import numpy as np
import pandas as pd

from src.definitions import ROOT_DIR


class DataDownloader():
    '''
    Download data using URL, destination directory, and file type.

    Parameters
    ----------
    url : str
          Target URL with data to be downloaded.
    dst : str
          Destination directory to save downloaded content.
    payload: dict, optional
          Parameters to be used with the URL in the get request.
          (default is None)
    zip: bool, optional
          Does the target URL retrieves a zipped file?
          (default is False)
    descr_url: str
          Target metadata description URL to be downloaded.
    lic: str
          Target metadata license text.
    '''

    def __init__(self,
                 url,
                 dst,
                 payload=None,
                 descr_url=None,
                 lic=None):
        self.dst = dst
        self._payload = payload

        self.url = url
        self._res = None

        self.descr_url = descr_url
        self._descr_res = None

        self._lic = lic

    @property
    def dst(self):
        return self._dst

    @dst.setter
    def dst(self, new_dst):
        dst = Path(new_dst)
        self._dst = dst

    def check_url(self, url, params=None):
        return requests.head(url, params=params)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, new_url):
        res = self.check_url(new_url, params=self._payload)
        res.raise_for_status()
        self._url = new_url

    @property
    def res(self):
        return self._res

    def get_url(self):
        self._res = requests.get(self.url, params=self._payload)
        return self.res

    @property
    def descr_url(self):
        return self._descr_url

    @descr_url.setter
    def descr_url(self, new_url):
        if new_url is None:
            self._descr_url = None
        else:
            descr_res = self.check_url(new_url)
            descr_res.raise_for_status()
            self._descr_url = new_url

    @property
    def descr_res(self):
        return self._descr_res

    def get_descr_url(self):
        if self.descr_url is None:
            self._descr_res = 'No metadata description URL was provided'
        else:
            self._descr_res = requests.get(self.descr_url)
        return self.descr_res

    @property
    def lic(self):
        if self._lic is None:
            return 'No license file was provided'
        else:
            return self._lic

    def write(self, target, dst_fname=''):
        target_res = {'data': self.res,
                      'description': self.descr_res,
                      'license': self.lic}

        res = target_res[target]

        if res is None:
            msg = """response is None:
            Don't forget to run get_descr_url or get_url before
            attempting to write the response"""
            raise TypeError(msg)

        url_path = Path(self.url)
        if dst_fname == '':
            dst_fname = url_path.stem

        zipped = False
        if url_path.suffix.lower() == '.zip':
            zipped = True

        if not self.dst.is_dir():
            self.dst.mkdir(parents=True)

        if target == 'data' and zipped:
            zipped = zipfile.ZipFile(io.BytesIO(res.content))
            zipped.extractall(self.dst / dst_fname)
        elif target == 'license':
            with open(self.dst / dst_fname, 'w') as fd:
                fd.write(res)
        else:
            with open(self.dst / dst_fname, 'wb') as fd:
                for chunk in res.iter_content(chunk_size=128):
                    fd.write(chunk)


class Table():
    def __init__(self, table_fn, year):
        self.table_fn = Path(table_fn)
        self.year = year

        self.table_name = self.table_fn.stem

        self.df = None

    def get_header(self):
        headers_fn = Path(ROOT_DIR) / 'data/external' / self.year
        headers_fn = headers_fn / 'Layout_and_Length.txt'

        column_names = []
        with open(headers_fn, 'r', encoding="ISO-8859-1") as fh:
            for line in fh:
                if line.startswith(self.table_name + ' '):
                    _, column_name, _ = line.split()
                    column_name = column_name.strip()
                    column_names.append(column_name)
        return column_names

    def get_df(self):
        names = self.get_header()

        df = pd.read_csv(self.table_fn,
                         sep='\t',
                         names=names,
                         encoding="ISO-8859-1",
                         low_memory=False,
                         quoting=csv.QUOTE_NONE,
                         )
        self.df = df
        return self.df

    def get_code(self, codes_fn, code_name, split_parts=1):
        codes = {}
        with open(codes_fn, 'r', encoding="ISO-8859-1") as fh:
            for line in fh:
                if line.startswith(code_name):
                    break
            next(fh)
            next(fh)
            next(fh)
            for line in fh:
                if line.strip() == '':
                    break
                if split_parts == 1:
                    code, descr = line.split(' ', split_parts)
                    codes[int(code)] = descr.strip()
                else:
                    code, second_code, descr = line.split(None, split_parts)
                    codes[code] = descr.strip()
        return codes

    def map_codes_to_column(self, colname, code):
        self.df[colname].replace(code, inplace=True)
        return self.df


def save_pickle(obj, dst_fn):
    if not dst_fn.parent.is_dir():
        dst_fn.parent.mkdir(parents=True)
    with open(dst_fn, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
