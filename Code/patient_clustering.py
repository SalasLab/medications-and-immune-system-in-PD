from scipy.cluster.hierarchy import dendrogram, linkage, ward, cut_tree
from Code.drug_groups_with_comments import drug_groups_di
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

df = pd.read_csv('Data/formatted/230122_MASTER.csv')
# separate out those taking medications
df_with_meds = df[df['drug_count'] > 0].copy()
# df with medication columns only
drop = ["Antiflatulent drug", "Vaccine other", "Supplement or multivitamin", "Supplement cannabis",
        "Supplement calcium", "Supplement probiotic", "Supplement fiber", "Supplement mineral", "Supplement omega",
        'Vaccine COVID', 'Vaccine influenza', 'Vaccine shingles', "Parkinson\'s drug"]
medications = [drug for drug in drug_groups_di.keys() if drug not in drop]

linkage_data = linkage(df_with_meds[medications], method='ward', metric='euclidean')
dendrogram(linkage_data)
plt.axhline(5, c='red')

Z = ward(df_with_meds[medications])
cutree = cut_tree(Z, height=5)

df_with_meds['cluster'] = cutree

for cluster in range(0, cutree.max() + 1):
    test = df_with_meds[df_with_meds['cluster'] == cluster][medications]
    used_meds = test.sum()[test.sum() > 0].index
    sns.clustermap(test[used_meds], cmap='rocket_r', xticklabels=True)
    plt.savefig(f'Graphs/hier_clust_cl{cluster}.png', dpi=300)
    plt.close()

cols2=[
    'PATNO', 'EVENT_ID', 'visit_date', 'Current_age', 'Gender_reported', 'AA_CCI_bins',
    'Bas_zscore', 'Bmem_zscore', 'Bnv_zscore', 'CD4mem_zscore', 'CD4nv_zscore', 'CD8mem_zscore', 'CD8nv_zscore',
    'Eos_zscore', 'Mono_zscore', 'Neu_zscore', 'NK_zscore', 'Treg_zscore', 'CONCOHORT_DEFINITION', 'drug_count', 'AA_CCI',
    'cluster', 'bone marrow suppressants (duplicated)', 'Other']

