# Harris County Appraisal District (HCAD) property value prediction
Harris County is the [third-most](https://en.wikipedia.org/wiki/List_of_the_most_populous_counties_in_the_United_States) populous county in the USA. Its appraisal district (HCAD) provides a [fantastic dataset](https://pdata.hcad.org/download/index.html) with each appraised property characteristics (appraised value, fixtures, features) reported yearly.

Using these data, I'll follow the [Data Science Method](https://medium.com/@aiden.dataminer/the-data-science-method-dsm-a-framework-on-how-to-take-your-data-science-projects-to-the-next-91f9fd81e5d1) to understand if my house was fairly appraised in 2016. Then, I'll construct a statistical model for predicting house appraised values based on the house features (area, number of rooms, pool, etc.).

# Set up
Concerning file organization, I'm mostly following the [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) template with [some modifications](https://github.com/RafaelPinto/simplified_project_cookiecutter). Chiefly among them are using a `tasks.py` file and `invoke` as a substitute for `make`, to enable compatibility on systems without access to `make`. Also, I took the liberty of writing new executing commands as I found the ones in the original template a bit cryptic.

Additionally, I repurposed the data folders to follow this flow:
1. External: The original, immutable data dump. All available data is here (or linked here) first.
2. Raw: The external data after the cleaning step.
3. Interim: Intermediate data that has been transformed (normalized, scaled, etc.).
4. Processed: The final, canonical data sets for modeling.

# Downloading the data
`invoke download-data`

> **_NOTE:_**  Although the actual function name is def `download_data` to run in the terminal, we must replace the underscore (`_`) with a dash (`-`). This applies to all of my invoke functions.

This command will run script `src/data/download_hcad_data.py`, which will fecth all the available data from the year 2016, and save it to the `data/external/2016` directory.

# Process: select data
`invoke select-data`

The downloaded data is numerous and comes in multiple files, representing different kinds of data. I took the first look and stab at data preparation with the suite of notebooks `notebooks/01_Exploratory/1.[0-6]`. In the process of converting these exploratory notebooks to a proper `.py` file, I discovered the [papermill library](https://papermill.readthedocs.io/en/latest/). This package allows me to focus on the DS part of the project, so I only abstract away recurring tasks in my notebooks to the `src` local package, and skip translating the notebooks sequence to a `.py` file. This way, we keep the delicate balance between reproducibility and allotted time to accomplish this project.

In the first five files in the `select_data` suite of notebooks, I inspect, decode, and clean the columns, and then I run a summary statistics for each. The resulting cleaned version of the data is saved to `data/raw/2016` directory. The sixth notebook on this series is for joining the results of the previous five into a single file: `data/interim/2016/comps.pickle`
