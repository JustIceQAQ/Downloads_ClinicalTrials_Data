import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime
import os
import io

def main():
    allCTData = []
    allCTDataDF = pd.DataFrame()
    x = datetime.now()
    DateTimeSTR = '{}{}{}'.format(
        x.year,
        str(x.month).zfill(2) if len(str(x.month)) < 2 else str(x.month),
        str(x.day).zfill(2) if len(str(x.day)) < 2 else str(x.day))
    try:
        path = './{}_ClinicalTrialsData'.format(DateTimeSTR)
        if not os.path.isdir(path):
            os.mkdir(path)
            os.chdir(path)
        else:
            os.chdir(path)
        req = requests.get('https://clinicaltrials.gov/ct2/results?cond=&term=&cntry=&state=&city=&dist=')
        soup = BeautifulSoup(req.text, 'html5lib')
        CTDataCounts = int(''.join(list(filter(str.isdigit, soup.findAll('div', {'class': 'sr-search-terms'})[1].text))))
        for n in tqdm(range(1, CTDataCounts // 10000 + 2 - 29), ascii=True, desc='Downloads Data -> ', ncols=69):
            url = "https://clinicaltrials.gov/ct2/results/download_fields?down_count=10000&down_flds=all&down_fmt=csv&down_chunk={}".format(n)
            s = requests.get(url).content
            allCTData.extend(pd.read_csv(io.StringIO(s.decode('utf-8')), encoding='utf-8').to_dict('records'))
        allCTDataDF = pd.DataFrame(allCTData)
        allCTDataDF = allCTDataDF.rename(
            dict(zip(allCTDataDF.columns, [i.replace(' ', '') for i in allCTDataDF.columns])),
            axis=1)
        allCTDataDF_Columns = ['NCTNumber', 'Title', 'Acronym', 'Status', 'Conditions'
            , 'Interventions', 'OutcomeMeasures', 'Sponsor/Collaborators', 'Gender', 'Age'
            , 'Phases', 'Enrollment', 'FundedBys', 'StudyType', 'StudyDesigns'
            , 'OtherIDs', 'StartDate', 'PrimaryCompletionDate', 'CompletionDate', 'FirstPosted'
            , 'ResultsFirstPosted', 'LastUpdatePosted', 'Locations', 'Rank', 'StudyDocuments'
            , 'StudyResults', 'URL']
       
       # output excel
        print('Loading Clinical Trials Data to Excel file.')
        writer = pd.ExcelWriter('ClinicalTrials_{}.xlsx'.format(DateTimeSTR), engine='xlsxwriter',
            options={'strings_to_urls': False})
        allCTDataDF[allCTDataDF_Columns].to_excel(writer, index=False, encoding='utf-8')
        writer.close()

        # output csv
        print('Loading Clinical Trials Data to CSV file.')
        allCTDataDF[allCTDataDF_Columns].to_csv('ClinicalTrials_{}.csv'.format(DateTimeSTR), index=False, encoding='utf-8')
    except Exception as e:
        print(str(e))
        with open('errorFileLog.log', 'w+') as errorFileLog:
            errorFileLog.write(str(e))
if __name__ == '__main__':
    main()
    print('Downloads Clinical Trials is Done.')
