from Code.drug_groups_with_comments import *
import matplotlib.pyplot as plt
from scipy.stats import zscore
import seaborn as sns
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

df = pd.read_csv('Data/formatted/230117_steve_df_with_drugs.csv')
immune_cells = ['Bas', 'Bmem', 'Bnv', 'CD4mem', 'CD4nv', 'CD8mem', 'CD8nv', 'Eos', 'Mono', 'Neu', 'NK', 'Treg', 'NLR']
for cell in immune_cells:
    df[f'{cell} z-score'] = df.groupby("CONCOHORT_DEFINITION")[cell].transform(lambda x: zscore(x, ddof=1))


for drug in drug_groups_di.keys():
    # drug = 'bone marrow suppressants (duplicated)'
    per_drug = df[df[drug] == 1.0]
    # per_drug = df[df['drug_count'] == 0]
    if len(per_drug) > 0:
        per_drug = per_drug[
            ['CONCOHORT_DEFINITION', 'Bas z-score', 'Bmem z-score', 'Bnv z-score', 'CD4mem z-score', 'CD4nv z-score',
             'CD8mem z-score', 'CD8nv z-score', 'Eos z-score', 'Mono z-score', 'Neu z-score', 'NK z-score',
             'Treg z-score']]

        per_drug = per_drug.groupby('CONCOHORT_DEFINITION').sum()
        plt.figure(figsize=(6, 2.5))
        ax = sns.heatmap(per_drug, cmap='viridis')
        ax.set(xlabel="", ylabel="")
        ax.xaxis.tick_top()
        plt.yticks(rotation=0)
        plt.xticks(rotation=90)
        plt.title(drug)
        # plt.title('True controls')
        plt.tight_layout()
        plt.savefig(f'Graphs/{drug} z-scores.png', dpi=300)
        # plt.savefig(f'Graphs/True controls z-scores.png', dpi=300)
        plt.close()


