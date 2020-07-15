from pathlib import Path
import io
import zipfile
import requests


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
                 zipped=False,
                 descr_url=None,
                 lic=None):
        self.dst = dst
        self._payload = payload
        self._zipped = zipped

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

    @property
    def zipped(self):
        return self._zipped

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

        if not self.dst.is_dir():
            self.dst.mkdir(parents=True)

        if target == 'data' and self.zipped:
            zipped = zipfile.ZipFile(io.BytesIO(res.content))
            zipped.extractall(self.dst)
        elif target == 'license':
            with open(self.dst / dst_fname, 'w') as fd:
                fd.write(res)
        else:
            with open(self.dst / dst_fname, 'wb') as fd:
                for chunk in res.iter_content(chunk_size=128):
                    fd.write(chunk)
