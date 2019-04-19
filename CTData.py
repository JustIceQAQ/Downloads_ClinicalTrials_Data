import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime
import os
import io
import sys
import tkinter as tk

x = datetime.now()
DateTimeSTR = '{}{}{}'.format(
    x.year,
    str(x.month).zfill(2) if len(str(x.month)) < 2 else str(x.month),
    str(x.day).zfill(2) if len(str(x.day)) < 2 else str(x.day))


def filetypesSelect(filedf, fileName, filetypesStr, check):
    if 'csv' in filetypesStr:
        filedf.to_csv('{}_{}.csv'.format(check, fileName), index=False, encoding='utf-8')
    elif 'json' in filetypesStr:
        filedf.to_json('{}_{}.json'.format(check, fileName), orient="records")
    elif 'xlsx' in filetypesStr:
        writer = pd.ExcelWriter('{}_{}.xlsx'.format(check, fileName), engine='xlsxwriter',
                                options={'strings_to_urls': False})
        filedf.to_excel(writer, index=False, encoding='utf-8')
        writer.close()
    elif 'msgpack' in filetypesStr:
        filedf.to_msgpack("{}_{}.msg".format(check, fileName), encoding='utf-8')
    elif 'feather' in filetypesStr:
        filedf.to_feather('{}_{}.feather'.format(check, fileName))
    elif 'parquet' in filetypesStr:
        filedf.to_parquet('{}_{}.parquet'.format(check, fileName), engine='pyarrow', encoding='utf-8')
    elif 'pickle' in filetypesStr:
        filedf.to_pickle('{}_{}.pkl'.format(check, fileName))


def change_label_number():
    strLabel = tk.Label(window, text='處理中...')
    strLabel.pack(anchor='center')
    window.update()
    global url
    global zipfileName
    global comboExample
    comboExampleget = fileTypeListbox.get(fileTypeListbox.curselection())
    req = requests.get('https://clinicaltrials.gov/ct2/results?cond=&term=&cntry=&state=&city=&dist=')
    soup = BeautifulSoup(req.text, 'html5lib')
    CTDataCounts = int(''.join(list(filter(str.isdigit, soup.findAll('div', {'class': 'sr-search-terms'})[1].text))))
    strLabel2 = tk.Label(window, text='Downloads Clinical Trials Data.')
    strLabel2.pack(anchor='center')
    window.update()
    for n in tqdm(range(1, CTDataCounts // 10000 + 2 - 29), ascii=True, desc='Downloads Data -> ', ncols=69):
        url = "https://clinicaltrials.gov/ct2/results/download_fields?down_count=10000&down_flds=all&down_fmt=csv&down_chunk={}".format(
            n)
        s = requests.get(url).content
        allCTData.extend(pd.read_csv(io.StringIO(s.decode('utf-8')), encoding='utf-8').to_dict('records'))
    allCTDataDF = pd.DataFrame(allCTData)
    strLabel3 = tk.Label(window, text='Downloads Clinical Trials Data Done.')
    strLabel3.pack(anchor='center')
    window.update()
    allCTDataDF = allCTDataDF.rename(
        dict(zip(allCTDataDF.columns, [i.replace(' ', '') for i in allCTDataDF.columns])),
        axis=1)
    allCTDataDF_Columns = ['NCTNumber', 'Title', 'Acronym', 'Status', 'Conditions'
        , 'Interventions', 'OutcomeMeasures', 'Sponsor/Collaborators', 'Gender', 'Age'
        , 'Phases', 'Enrollment', 'FundedBys', 'StudyType', 'StudyDesigns'
        , 'OtherIDs', 'StartDate', 'PrimaryCompletionDate', 'CompletionDate', 'FirstPosted'
        , 'ResultsFirstPosted', 'LastUpdatePosted', 'Locations', 'Rank', 'StudyDocuments'
        , 'StudyResults', 'URL']
    # 計算三份檔案資料筆數
    allCTDataCounts = 'Clinical Trials Count: {}'.format(len(allCTDataDF))
    with open('ClinicalTrials_DataCounts.txt', 'w', encoding='utf-8') as txt:
        txt.write(allCTDataCounts)
    print('Loading Clinical Trials Data to {}'.format(comboExampleget))
    strLabel4 = tk.Label(window, text='Loading Clinical Trials Data to {}'.format(comboExampleget))
    strLabel4.pack(anchor='center')
    window.update()
    try:
        filetypesSelect(allCTDataDF[allCTDataDF_Columns], 'ClinicalTrials', comboExampleget, DateTimeSTR)
        window.quit()
    except Exception:
        window2 = tk.Tk()
        window2.title('錯誤提示')
        window2.geometry('400x300')
        error_Text = ''
        e_type, e_value, e_traceback = sys.exc_info()
        error_Text += f'''錯誤訊息如下：
                        Errortype ==> {e_type.__name__}
                        ErrorInfo ==> {e_value}
                        ErrorFileName ==> {e_traceback.tb_frame.f_code.co_filename}
                        ErrorLineOn ==> {e_traceback.tb_lineno}
                        ErrorFunctionName ==> {e_traceback.tb_frame.f_code.co_name}'''
        with open('errorFileLog.log', 'w+') as errorFileLog:
            errorFileLog.write(error_Text)
        strLabel2 = tk.Label(window2, text='{}\n{}\n{}'.format(e_type, e_value, e_traceback))
        strLabel2.pack(anchor='center')
        window2.mainloop()

    finally:
        pass


window = tk.Tk()
window.title('請選擇 Clinical Trials 輸出檔案格式(Select File Type)')
window.geometry('400x300')
try:
    allCTData = []
    allCTDataDF = pd.DataFrame()
    path = './{}_ClinicalTrialsData'.format(DateTimeSTR)
    if not os.path.isdir(path):
        os.mkdir(path)
        os.chdir(path)
    else:
        os.chdir(path)
    fileTypeVar = tk.StringVar()
    fileTypeVar.set(('csv', 'json', 'xlsx', 'msgpack', 'feather', 'parquet', 'pickle'))
    fileTypeListbox = tk.Listbox(window, listvariable=fileTypeVar)
    fileTypeListbox.pack(anchor='center')
    saveButton = tk.Button(window, text='儲存(Save)', command=change_label_number)
    saveButton.pack(anchor='center')
    window.mainloop()
except Exception as e:
    window2 = tk.Tk()
    window2.title('錯誤提示')
    window2.geometry('400x300')
    error_Text = ''
    e_type, e_value, e_traceback = sys.exc_info()
    error_Text += f'''錯誤訊息如下：
                Errortype ==> {e_type.__name__}
                ErrorInfo ==> {e_value}
                ErrorFileName ==> {e_traceback.tb_frame.f_code.co_filename}
                ErrorLineOn ==> {e_traceback.tb_lineno}
                ErrorFunctionName ==> {e_traceback.tb_frame.f_code.co_name}'''
    with open('errorFileLog.log', 'w+') as errorFileLog:
        errorFileLog.write(error_Text)
    strLabel2 = tk.Label(window2, text='{}\n{}\n{}'.format(e_type, e_value, e_traceback))
    strLabel2.pack(anchor='center')
    window2.mainloop()
finally:
    pass
