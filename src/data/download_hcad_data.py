from pathlib import Path

from src.data.utils import DataDownloader


dst_base = Path('data/external/2016')

url_base = 'https://pdata.hcad.org/data/cama/2016'

files = [
    'Real_acct_owner.zip',
    'Real_building_land.zip',
    'Real_jur_exempt.zip',
    'Real_jur_exempt.zip',
    'PP_files.zip',
    'Hearing_files.zip',
    'code_desc_real.txt',
    'code_nh_numbers.txt',
    'code_nh_numbers_adj.txt',
    'code_desc_personal.txt',
    'code_jur_list.txt',
]

descr_url = 'https://pdata.hcad.org/Desc/Definition_help.pdf'

lic = """Public Data. See https://pdata.hcad.org/index.html"""