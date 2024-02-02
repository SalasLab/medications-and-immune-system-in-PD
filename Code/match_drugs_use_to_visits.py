from Code.drug_groups_with_comments import *
from datetime import timedelta, datetime
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


def format_main_data():
    ppmi = pd.read_csv('Data/PPMI_Curated_Data_Cut_Public_20230612_rev.csv')
    steve = pd.read_csv('Data/PPMI_pheno_Stevecleaned.csv')
    ppmi = ppmi.sort_values(by='PATNO')
    data = pd.merge(ppmi[['PATNO', 'EVENT_ID', 'visit_date']], steve, on=['PATNO', 'EVENT_ID'])
    data['visit_date'] = pd.to_datetime(data['visit_date'])
    cols = ['PATNO', "EVENT_ID", "visit_date", "Current_age", "Gender_reported", "CONCOHORT_DEFINITION",
            "Bas", "Bmem", "Bnv", "CD4mem", "CD4nv", "CD8mem", "CD8nv", "Eos", "Mono", "Neu", "NK", "Treg", "NLR"]
    data = data[cols]
    return data


def format_medication_data(which_patients):
    drug_df = pd.read_csv('Data/Concomitant_Medication_Log.csv')
    cols = ['PATNO', 'CMTRT', 'WHODRUG', 'CMINDC_TEXT', 'STARTDT', 'STOPDT', 'ONGOING']
    drug_df = drug_df[cols]
    drug_df['CMTRT'] = [' '.join(i.split()).lower() for i in drug_df['CMTRT']]
    drug_df['WHODRUG'] = [str(i).lower() for i in drug_df['WHODRUG']]
    drug_df['WHO_CMTRT'] = drug_df['WHODRUG']
    drug_df = drug_df.replace('nan', np.nan)
    drug_df.loc[drug_df['WHO_CMTRT'].isna(), 'WHO_CMTRT'] = drug_df['CMTRT']

    # Using medication group dictionary, reverse keys and values for easy mapping
    reversed_di = {}
    for k, v in drug_groups_di.items():
        for value in v:
            reversed_di[value] = k
    # add a column with broader medicine groups using the reversed dictionary
    drug_df['drug_group'] = drug_df['WHO_CMTRT'].map(reversed_di)
    drug_df = drug_df[drug_df['PATNO'].isin(which_patients)].reset_index(drop=True)

    # bone marrow suppressants is a good group to have for immune cell comparisons, however it is equally
    # useful to have those same drugs in other groups. Hence, we are duplicating those patients who take BM supp
    # and adding them at the end of the dataframe as extra rows.
    bone_marrow_supp_df = drug_df[drug_df['WHO_CMTRT'].isin(bone_marrow_suppressants)].copy()
    bone_marrow_supp_df['drug_group'] = 'bone marrow suppressants (duplicated)'
    drug_df = pd.concat([drug_df, bone_marrow_supp_df]).reset_index(drop=True)

    # add a column to the medication dataframe (windows)
    # this is a list of months during which the participant took a specific drug
    windows_li = []
    for idx in range(len(drug_df)):
        # idx = 567  # 555, 567
        start_dt = pd.to_datetime(drug_df.loc[idx]['STARTDT'])
        end_dt = pd.to_datetime(drug_df.loc[idx]['STOPDT'])
        # nostopdt = drug_df[drug_df['STOPDT'].isnull()]

        # Some drugs do not have a stop date. Most CVD and anxiety/depression drugs are chronic, so we can assume
        # the patient is still taking them. For acute drugs, we set the stop date as start date = 1 month window
        acute_drugs = ['Malaria drug', 'Decongestant drug', 'Abortion drug', 'Other', 'Antibiotic']
        acute = drug_df.loc[idx]['drug_group'] in acute_drugs
        if pd.isnull(end_dt):
            if not acute:
                end_dt = datetime.today()
            else:
                end_dt = start_dt

        dates = []
        while start_dt <= end_dt:
            dates.append(start_dt)
            start_dt += timedelta(days=31)
            start_dt = start_dt.replace(day=1)

        windows_li.append(dates)
    drug_df['windows'] = windows_li

    return drug_df


# format main data (df) and concomitant medication data (med)
df = format_main_data()
steves_patients = list(df['PATNO'].unique())
med = format_medication_data(steves_patients)

all_drugs = list(drug_groups_di.keys())
all_drugs.append('bone marrow suppressants (duplicated)')
for drug in all_drugs:
    # drug = 'Cancer drug'
    print(drug)
    overlap_di = {}
    for patient in df['PATNO']:
        # patient = 41471
        print(patient)
        overlap_di[patient] = {}

        # check if they have taken this drug at all (whole_window = drug taken (or not) during this time)
        windows_df = med[(med['drug_group'] == drug) & (med['PATNO'] == patient)]['windows']
        windows_df = windows_df.reset_index(drop=True)
        # in case the patient used similar drug multiple times, bind these together in a long list
        # (e.g., different antidepressants which would be saved in separate rows)
        whole_window = []
        for row in range(len(windows_df)):
            whole_window.extend(windows_df[row])
        # remove duplicates (this might be someone taking two drugs of the same class at the same time)
        whole_window = list(set(whole_window))

        if len(whole_window) > 0:
            per = df[df['PATNO'] == patient].reset_index(drop=True)
            for visit in per['visit_date']:
                # check if the drug use window overlaps with any of the visits
                overlap_date = [i for i in whole_window if i == visit]
                event = per[per['visit_date'] == visit]['EVENT_ID'].values[0]
                if len(overlap_date) == 0:
                    overlap_di[patient][event] = np.NaN
                else:
                    overlap_di[patient][event] = 1

    overlap_df = pd.DataFrame.from_dict(overlap_di, orient='index').reset_index().melt(id_vars='index')
    # because of how the dictionary is transformed into a dataframe, some visits that patients did not have get an NaN
    # that's why there's the dropna command on the next line
    overlap_df = overlap_df.dropna()
    overlap_df.columns = ['PATNO', 'EVENT_ID', f'{drug}']
    df = pd.merge(df, overlap_df, on=['PATNO', 'EVENT_ID'], how='outer')

df[all_drugs] = df[all_drugs].fillna(0)
all_drugs.remove('bone marrow suppressants (duplicated)')
df['drug_count'] = df[all_drugs].sum(axis=1)
df = df[df['EVENT_ID'] == 'BL']
df.to_csv('Data/formatted/240127_BL_matched_drugs.csv', index=False)


# TODO: Make dataframe from drug groups and associated ICD10 codes
icd10 = pd.DataFrame.from_dict(drug_group_icd10, orient='index')
icd10.to_csv('Data/formatted/ICD10_key.csv')
