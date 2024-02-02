from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
import pandas as pd
import numpy as np
import collections
import distance
import warnings
import umap
from sklearn.manifold import TSNE
from Code.drug_groups_with_comments import *

warnings.filterwarnings("ignore", category=FutureWarning)


def format_med():
    med = pd.read_csv('Data/Concomitant_Medication_Log.csv')
    med = med[['PATNO', 'CMTRT', 'WHODRUG', 'CMINDC_TEXT', 'STARTDT', 'STOPDT', 'ONGOING']]
    med['CMTRT'] = [' '.join(i.split()).lower() for i in med['CMTRT']]
    med['WHODRUG'] = [str(i).lower() for i in med['WHODRUG']]

    # get a column of WHODRUG and if WHODRUG == nan, get CMTRT value
    med['WHO_CMTRT'] = med['WHODRUG']
    med = med.replace('nan', np.nan)
    med.loc[med['WHO_CMTRT'].isna(), 'WHO_CMTRT'] = med['CMTRT']
    # sort values by drug name
    med = med.sort_values(by='WHO_CMTRT')
    return med


def cluster_words(words):
    words = np.asarray(words)
    lev_similarity = -1 * np.array([[distance.levenshtein(w1, w2) for w1 in words] for w2 in words])

    affprop = AffinityPropagation(affinity="precomputed", damping=0.5)
    affprop.fit(lev_similarity)
    di_clustered = {}
    for cluster_id in np.unique(affprop.labels_):
        exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
        cluster = np.unique(words[np.nonzero(affprop.labels_ == cluster_id)])
        di_clustered[exemplar] = list(cluster)

    return di_clustered, lev_similarity


reversed_di = {}
for k, v in drug_groups_di.items():
    for value in v:
        reversed_di[value] = k

df = format_med()
df['drug_group'] = df['WHO_CMTRT'].map(reversed_di)
drug_usage = df['drug_group'].value_counts()

# check how many are properly classified
drugs_grouped = sum(list(drug_groups_di.values()), [])
not_grouped = [i for i in df['WHO_CMTRT'].unique() if i not in drugs_grouped]
# check for duplicates
duplicates = [item for item, count in collections.Counter(drugs_grouped).items() if count > 1]

# check if ICD10 groups match dictionary keys
drug_groups = list(drug_groups_di.keys())
drug_groups_icd10 = list(drug_group_icd10.keys())
print([i for i in drug_groups_icd10 if i not in drug_groups])

# TODO: UMAPS showing Levenstein distance clustering
li = ["Antidiabetic drug", 'Antihistamine drug', 'Supplement iron', 'Hypothyroidism drug', "Testosterone topical",
      'Analgesic nonprescription', 'Cholesterol drug', 'Supplement calcium & vitD', 'Depression drug']
# li = ['Antidiabetic drug']
to_cluster = df[df['drug_group'].isin(li)]
words_to_cluster = list(to_cluster['WHO_CMTRT'].unique())
di, lev_dist = cluster_words(words=words_to_cluster)
print(0)

tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(lev_dist)

u = pd.DataFrame(X_tsne)
u['WHO_CMTRT'] = words_to_cluster
u['drug_group'] = u['WHO_CMTRT'].map(reversed_di)

plt.figure(figsize=(5, 3))
sns.scatterplot(data=u, x=0, y=1, hue='drug_group')
plt.legend(loc=(1.04, 0.4), frameon=False)
plt.tight_layout()
plt.savefig("Graphs/diabetes_clustering_cluster.png", dpi=400, bbox_inches="tight")


reducer = umap.UMAP(min_dist=0.15, n_neighbors=20)
embedding = reducer.fit_transform(lev_dist)
print(embedding.shape)

kmeans = KMeans(n_clusters=5).fit(lev_dist)
labs = kmeans.labels_

u = pd.DataFrame(embedding)
u['WHO_CMTRT'] = words_to_cluster
u['drug_group'] = u['WHO_CMTRT'].map(reversed_di)
u['cluster'] = [f'cluster {i}' for i in labs]
u = u.sort_values(by='cluster')

plt.figure(figsize=(5, 3))
sns.scatterplot(data=u, x=0, y=1, hue='cluster')
plt.legend(loc=(1.04, 0.4), frameon=False)
plt.tight_layout()
plt.savefig("Graphs/diabetes_clustering_cluster.png", dpi=400, bbox_inches="tight")
u.to_csv('umap_diabetic_drug_clustering.csv', index=False)

plt.scatter(u[0], u[1])

sns.scatterplot(data=u, x=0, y=1, hue='cluster')
for i, txt in enumerate(u['WHO_CMTRT']):
    plt.annotate(txt, (u[0][i], u[1][i]), size=7)


plt.figure(figsize=(7, 4))
cmap = ['#006400', '#00008b', "#b03060", "#ff4500", "#ffd700", "#00ffff", "#ff00ff", "#7fff00", "#6495ed", "#ffdab9"]
sns.scatterplot(data=u, x=0, y=1, hue='drug_group')
plt.legend(loc=(1.04, 0.4), frameon=False)
plt.tight_layout()
plt.savefig("Graphs/medication_clustering.png", dpi=400, bbox_inches="tight")

