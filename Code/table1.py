from Code.drug_groups_with_comments import *
from statsmodels.stats.multitest import multipletests
from scipy.stats import chi2_contingency
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

df = pd.read_csv('Data/formatted/230113_steve_df_with_drugs.csv')
# n participants in cohorts
n_in_cohorts = df['CONCOHORT_DEFINITION'].value_counts()
n_in_cohorts = n_in_cohorts.reset_index()
n_in_cohorts.columns = ['CONCOHORT_DEFINITION', 'n_pat_in_cohort']

# get a table1 like counts for participants (across Healthy, PD, Prod) taking different drugs
drug_counts = pd.DataFrame()
for drug in drug_groups_di.keys():
    # drug = 'Immunosuppressant drug'
    per = pd.DataFrame(df.groupby('CONCOHORT_DEFINITION')[drug].value_counts())
    per = per.rename(columns={drug: 'count'}).reset_index()

    per = per.pivot(index='CONCOHORT_DEFINITION', columns=drug, values='count')
    per = per.fillna(0)
    per = per.reset_index().melt(id_vars='CONCOHORT_DEFINITION')
    per = per[per[drug] == 1.0].drop(columns=drug)
    per['drug'] = drug
    new_order = ['CONCOHORT_DEFINITION', 'drug', 'value']
    per = per[new_order].rename(columns={'value': 'count'})

    drug_counts = pd.concat([drug_counts, per])


drug_counts = pd.merge(n_in_cohorts, drug_counts, on='CONCOHORT_DEFINITION')
drug_counts['norm count'] = (drug_counts['count'] / drug_counts['n_pat_in_cohort'])*100

# TODO: Variance in use of different drugs
# get a df with drugs in index and cohorts in columns
cont_table = pd.pivot_table(
    drug_counts,
    values='norm count',
    columns='CONCOHORT_DEFINITION',
    index='drug',
    aggfunc='sum',
    fill_value=0)

cohort_pairs = [(c1, c2) for c1 in cont_table.columns for c2 in cont_table.columns if c1 < c2]

sum_of_sqrs = []
for pair in cohort_pairs:
    diff = np.square(cont_table[pair[0]] - cont_table[pair[1]])
    sum_of_sqrs.append(list(diff))

zipped_list = zip(sum_of_sqrs[0], sum_of_sqrs[1], sum_of_sqrs[2])
sum_of_sqrs = [sum(item) for item in zipped_list]
cont_table['sum_of_sqrs'] = np.sqrt(sum_of_sqrs)
cont_table = cont_table.sort_values(by='sum_of_sqrs', ascending=False)


# TODO: CHI2
# in order to do chi2 test, one assumption is that observed cell frequency is >5
drugs_with_few_observations = list(drug_counts[drug_counts['count'] < 5]['drug'].unique())
test = drug_counts[~drug_counts['drug'].isin(drugs_with_few_observations)]
test = test.sort_values(by='drug')

# Create a contingency table from your dataframe
contingency_table = pd.pivot_table(
    test,
    values='norm count',
    index='CONCOHORT_DEFINITION',
    columns='drug',
    aggfunc='sum',
    fill_value=0)

# Perform chi-square test
chi2, p, _, _ = chi2_contingency(contingency_table)
print(f"Chi-square value: {chi2}\nP-value: {p}")

# Get unique pairs of cohorts for comparison
cohort_pairs = [(c1, c2) for c1 in contingency_table.index for c2 in contingency_table.index if c1 < c2]

# Perform pairwise chi-square tests and store p-values
p_values = []
for cohort1, cohort2 in cohort_pairs:
    contingency_subset = contingency_table.loc[[cohort1, cohort2]]
    _, p_value, _, _ = chi2_contingency(contingency_subset)
    p_values.append(p_value)

# Apply Bonferroni correction
alpha = 0.05
reject, corrected_p_values, _, _ = multipletests(p_values, alpha=alpha, method='bonferroni')

# Print the results
for (cohort1, cohort2), p_val, rej in zip(cohort_pairs, corrected_p_values, reject):
    print(f"Comparison: {cohort1} vs {cohort2} - Adjusted p-value: {p_val} - Significant: {rej}")


# TODO: Which combinations of drugs are used most frequently together?
di = {}
cols = ['EVENT_ID', 'visit_date', 'Current_age', 'Gender_reported', 'CONCOHORT_DEFINITION', 'drug_count',
        'Bas', 'Bmem', 'Bnv', 'CD4mem', 'CD4nv', 'CD8mem', 'CD8nv', 'Eos', 'Mono', 'Neu', 'NK', 'Treg', 'NLR',
        'Supplement or multivitamin',
        'Supplement cannabis', 'Other',
        'Supplement fiber', 'Supplement mineral', 'Supplement omega'
        ]
for patient in df['PATNO']:
    per = df[df['PATNO'] == patient].drop(columns=cols)
    per = per[per == 1].dropna(axis=1)
    drug_set = set(per.columns)
    di[patient] = drug_set


df['drug_sets'] = df['PATNO'].map(di)
a = df['drug_sets'].value_counts()
