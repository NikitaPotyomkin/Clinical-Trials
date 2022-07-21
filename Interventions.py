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
directory = os.getcwd()
with open("Interventions.txt", 'w') as f:
    f.close()

#очищаем файлы

with open('Interventions.csv', 'w') as f:
    f.write('NCTId')
    f.close()


def getxml(company_name,target_condition):
    c_name = company_name
    #Формируем search expr: фильтр по Компании, Статусу (Active...),и Препарат(Drug)
    exp = f'AREA[LeadSponsorName]{c_name} AND AREA[Condition]"{target_condition}"'
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

target_cond = {}
with open('count_target_conditions.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        target_cond[line.replace('\n', '').split(',')[0]] = int(line.replace('\n', '').split(',')[1])
target_condition = max(target_cond, key=target_cond.get)
print('Наиболее часто встречающееся целевое заболевание: ', target_condition)

for name in Functions.read_companies(): #read_companies - функция читает в массив список компаний

    a = getxml(name,target_condition)
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
        print('ищем препараты для компании: ', name)
        # Functions.count_condition_and_phase_t1(name,df) #=>Functions.py переходим в функцию подсчета исследований
        Functions.count_interventions(name, df,target_condition)
print("Данные по препаратам целевого заболевания размещены в файле 'Interventions.txt'")
import Most_repeated_word




