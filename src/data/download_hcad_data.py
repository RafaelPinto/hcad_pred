from pathlib import Path

from src.data.utils import DataDownloader


dst = Path('data/external/2016')

url_base = 'https://pdata.hcad.org/data/cama/2016'

files = [
    'Real_acct_owner.zip',
    'Real_building_land.zip',
    'Real_jur_exempt.zip',
    'PP_files.zip',
    'Hearing_files.zip',
    'code_desc_real.txt',
    'code_nh_numbers.txt',
    'code_nh_numbers_adj.txt',
    'code_desc_personal.txt',
    'code_jur_list.txt',
]

for item in files:
    url = url_base + '/' + item

    data = DataDownloader(url, dst)

    data.get_url()
    data.write('data')

# Get the metadata
descr_url = 'https://pdata.hcad.org/Desc/Definition_help.pdf'
lic = """Public Data. See https://pdata.hcad.org/index.html"""

data = DataDownloader(
    url,
    dst,
    descr_url=descr_url,
    lic=lic
)
data.get_descr_url()
data.write('description', 'README.pdf')
data.write('license', 'LICENSE.txt')

# Get table column names
columns_url = 'https://pdata.hcad.org/Desc/Layout_and_Length.txt'
data = DataDownloader(columns_url, dst, descr_url=columns_url)
data.get_descr_url()
data.write('description', 'Layout_and_Length.txt')
