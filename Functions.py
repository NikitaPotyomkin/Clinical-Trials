#код со вспомогательными функциями
import pandas as pd

def read_companies():
    c_names = []
    with open("ListOfCompanies.txt",'r') as f:
        lines = f.readlines()
        for line in lines:
            c_name = line.replace('\n','')
            c_names.append(c_name)
    return c_names

def count_condition_and_phase_t1(name,df):
    pd.set_option('display.max_columns', 10)
    print(f"получаем данные для компании (з.1): {name}") #обозначаем наименование компании
    # print(df)
    df1 = df.loc[:,('Condition', 'Phase')] #берем колонки с целевым заболеванием и фазой
    df1.fillna('No info',inplace=True) #заполняем пробелы в фазах
    for field in ["Condition", "Phase"]:
        cond_list = df1[field].tolist()
        # Use list comprehension to convert a list of lists to a flat list
        target_list = [elem for elem in cond_list if type(elem) != list]
        nested_list = [item for elem in cond_list for item in elem if type(elem)==list]
        target_list = target_list+nested_list
        from collections import Counter
        counts = Counter(target_list)
        count_df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
        count_df.columns=['Name', name]
        count_df = count_df.sort_values(name, ascending = False).reset_index(drop=True)
        m_df = pd.read_csv(field+'s.csv')
        merged_df = pd.merge(m_df, count_df, on='Name', how='outer').reset_index(drop=True)
        merged_df.to_csv(field+'s.csv',header=True, index=False)

def count_drugs_(name,df):
    pd.set_option('display.max_columns', 10)
    df = df.loc[(df['OverallStatus'] == 'Active, not recruiting')]
    df = df[df['Phase'].str.contains("Phase 3",na=False)]
    cols_to_use = df.columns.difference(df.columns)
    print(f"получаем данные для компании (з.2): {name}")  # обозначаем наименование компании
    m_df = pd.read_csv('Drugs' + '.csv')
    merged_df = pd.concat([m_df,df], ignore_index=True)
    merged_df.to_csv('Drugs' + '.csv', header=True, index=False)
    conditions_list = merged_df['Condition'].tolist()
    target_list = [elem for elem in conditions_list if type(elem) != list]
    nested_list = [item for elem in conditions_list for item in elem if type(elem) == list]
    conditions_list = target_list + nested_list
    target_condition = max(set(conditions_list), key=conditions_list.count)
    list_to_write = [target_condition,',',str(conditions_list.count(target_condition))]
    with open('count_target_conditions.txt','a') as f:
        for x in list_to_write:
            f.write(x)
        f.write('\n')
    f.close()

def count_interventions(name,df,target_condition):
    pd.set_option('display.max_columns', 10)
    df = df[df['Condition'].str.contains(target_condition,na=False)]
    # print(df.head())
    phases = ['Phase 3', 'Phase 4']
    df = df[df['Phase'].isin(phases)]
    df = df.loc[(df['OverallStatus'] != 'Suspended')]
    df = df.loc[(df['OverallStatus'] != 'Terminated')]
    df = df.loc[(df['OverallStatus'] != 'Withdrawn')]
    inter_names = df['InterventionName'].tolist()
    inter_names = [x for x in inter_names if x is not None]
    target_list = [elem for elem in inter_names if type(elem) != list]
    nested_list = [item for elem in inter_names for item in elem if type(elem) == list]
    inter_names = target_list + nested_list
    inter_names = list(set(inter_names))
    with open('Interventions.txt','a') as f:
        if len(inter_names)>0:
            f.write(name+ ':'+str(','.join(inter_names))+"\n")
    f.close()

    m_df = pd.read_csv('Interventions' + '.csv')
    merged_df = pd.concat([m_df,df], ignore_index=True)
    merged_df.to_csv('Interventions' + '.csv', header=True, index=False)

