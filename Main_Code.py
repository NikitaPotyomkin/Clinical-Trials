from bs4 import BeautifulSoup
import requests
import Functions
import pandas as pd
# request = requests.get("https://clinicaltrials.gov/api/info/data_vrs")
import traceback
import urllib3
import xmltodict
import os

#очищаем файлы
files = ['Conditions.csv', 'Phases.csv', 'Drugs.csv']
directory = os.getcwd()
for file in files:
    with open(directory+'\\'+file, 'w') as f:
        if 'Drugs' in file or 't3' in file:
            f.write('NCTId')
        else:
            f.write('Name')

with open(directory+'\\'+'count_target_conditions.txt', 'w') as f:
    f.close()





def getxml(company_name):
    c_name = company_name
    #Формируем search expr: фильтр по Компании, Статусу (Active...),и Препарат(Drug)
    exp = f'AREA[LeadSponsorName]{c_name} AND AREA[OverallStatus]"Active, not recruiting" AND AREA[InterventionType]Drug'
    url = f"https://clinicaltrials.gov/api/query/study_fields?expr={exp}&fields=NCTId%2CBriefTitle" \
          f"%2CCondition%2CLeadSponsorName%2COverallStatus%2CPhase%2CInterventionType" \
          f"%2CCompletionDate%2CInterventionName&min_rnk=1&max_rnk=1000&fmt=xml"

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    #парсим xml, полученный по ссылке
    try:
        data = xmltodict.parse(response.data)
    except:
        print("Failed to parse xml from response (%s)" % traceback.format_exc())
    return data

x = 0
for name in Functions.read_companies(): #read_companies - функция читает в массив список компаний
    x+=1 #временный счетчик для ускорения выполнения кода
    # if x>10:
    #     print('breaking')
    #     break
    # if name =='Pfizer':
    a = getxml(name)
    table_values = [] #массив для парсинга словарей
    data_arrays = [] #массив для парсинга словарей
    new_header = []
    # print(a)
    i = 0

    #парсим каскадно словари
    for d in a.values():
        for value in d.values():
            if type(value) is dict:
                for next_value in value.values():
                        for next_value in next_value:
                            if type(next_value) is dict:
                                for c in next_value.keys():
                                    if c== 'FieldValues':
                                        data = next_value[c]
                                        if len(new_header)==0:
                                            df = pd.DataFrame(next_value[c]).transpose()
                                            new_header = df.iloc[0].tolist()
                                        table_values.append(data)

    df = pd.DataFrame(table_values) #массив с выгруженными данными конвертируем в dataframe
    length = len(df.columns)
    for i in range(0,length):
            feature3 = [d.get('FieldValue') for d in df.iloc[:, i]] #из каждого словаря берем значение по ключу Field Value
            data_arrays.append(feature3) #добавляем лист со значениями в общий лист
    df = pd.DataFrame(data_arrays).transpose() #лист добавляем в df и транспонируем
    df.columns = new_header #присваиваем колонкам имена
    if df.shape[0] >0:
        Functions.count_condition_and_phase_t1(name,df) #=>Functions.py переходим в функцию подсчета исследований
        Functions.count_drugs_(name, df)
print("Данные по исследования в разрезе компаний и фаз размещены в файлах 'Conditions.csv' и "
      "'Phases.csv'")

#добавляем total row
df = pd.read_csv("Conditions.csv")
df.loc['Total']= df.sum(numeric_only=True, axis=0)
sum_up = df.iloc[-1].to_csv('Conditions_sum_up.csv')
print('Сумма всех исследований по компаниям сохранена в файл Conditions_sum_up.csv')





