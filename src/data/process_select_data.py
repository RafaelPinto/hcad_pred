from datetime import datetime
import papermill as pm

from src.definitions import ROOT_DIR


root = ROOT_DIR / 'notebooks/01_Exploratory'
out_dir = root / 'output'

if not out_dir.is_dir():
    out_dir.mkdir(parents=True)

today = datetime.now().strftime('%Y%m%d')

in_file = str(root / '1.0-rp-hcad-data-view-building-res.ipynb')
out_file = '1.0-rp-hcad-data-view-building-res_' + today + '.ipynb'
out_file = str(out_dir / out_file)
pm.execute_notebook(in_file,
                    out_file,
                    )


in_file = str(root / '1.1-rp-hcad-data-view-fixtures.ipynb')
out_file = '1.1-rp-hcad-data-view-fixtures_' + today + '.ipynb'
out_file = str(out_dir / out_file)
pm.execute_notebook(in_file,
                    out_file,
                    )


in_file = str(root / '1.2-rp-hcad-data-view-real-acct.ipynb')
out_file = '1.2-rp-hcad-data-view-real-acct_' + today + '.ipynb'
out_file = str(out_dir / out_file)
pm.execute_notebook(in_file,
                    out_file,
                    )


in_file = str(root / '1.3-rp-hcad-data-view-extra_features.ipynb')
out_file = '1.3-rp-hcad-data-view-extra_features_' + today + '.ipynb'
out_file = str(out_dir / out_file)
pm.execute_notebook(in_file,
                    out_file,
                    )


in_file = str(root / '1.4-rp-hcad-data-view-exterior.ipynb')
out_file = '1.4-rp-hcad-data-view-exterior_' + today + '.ipynb'
out_file = str(out_dir / out_file)
pm.execute_notebook(in_file,
                    out_file,
                    )


in_file = str(root / '1.5-rp-hcad-data-view-structural_elem1.ipynb')
out_file = '1.5-rp-hcad-data-view-structural_elem1_' + today + '.ipynb'
out_file = str(out_dir / out_file)
pm.execute_notebook(in_file,
                    out_file,
                    )


in_file = str(root / '1.6-rp-hcad-data-view-join-selected-data.ipynb')
out_file = '1.6-rp-hcad-data-view-join-selected-data_' + today + '.ipynb'
out_file = str(out_dir / out_file)
pm.execute_notebook(in_file,
                    out_file,
                    )
