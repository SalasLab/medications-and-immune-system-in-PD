import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

df = pd.read_csv('Data/formatted/230113_steve_df_with_drugs.csv')
cells = ['Bas', 'Bmem', 'Bnv', 'CD4mem', 'CD4nv', 'CD8mem', 'CD8nv', 'Eos', 'Mono', 'Neu', 'NK', 'Treg', 'NLR']

test = df[cells]


X = np.array([[1, 2], [1, 4], [1, 0],
              [10, 2], [10, 4], [10, 0]])
kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(X)
# kmeans.labels_
# kmeans.predict([[0, 0], [12, 3]])
# kmeans.cluster_centers_
