# Downloads_ClinicalTrials_Data
Downloads_ClinicalTrials_Data

# 前言

下載美國 [clinicaltrials.gov](https://clinicaltrials.gov/) 臨床試驗資料
使用官方提供[Use URL Parameters to Display and Save Data](https://clinicaltrials.gov/ct2/resources/download#UseURL) 將資料下載下來後合併成單一檔案

# 使用套件
- pandas
- requests
- BeautifulSoup
- tqdm

# 檔案更新時間
隨時更新(一有最新資料，會直接於官網更新)

# 支援輸出

- .csv
- .json (records)
- .xlsx (Excel)
- .msgpack
- .feather
- .parquet

基於 pandas 的檔案格式
http://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-tools-text-csv-hdf5