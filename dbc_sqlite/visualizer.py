# import sqlite3
# import pandas as pd

# # Connect to your SQLite DB
# conn = sqlite3.connect('can.db')

# # Load all signal data into a DataFrame
# query = """
# SELECT 
#     s.id,
#     s.name,
#     s.length,
#     s.start_bit,
#     s.factor,
#     s.offset,
#     s.min AS minimum,
#     s.max AS maximum,
#     s.unit,
#     m.message_id AS frame_id,
#     m.name AS message_name,
#     cm.car_model AS model_name,
#     cm.manufacturer AS brand_name,
#     cm.variant
# FROM signals s
# JOIN messages m ON s.message_id = m.id
# JOIN dbc_files d ON s.dbc_id = d.id
# JOIN car_models cm ON d.car_model_id = cm.id
# """

# df = pd.read_sql_query(query, conn)

# # Optional: fill nulls, encode units/categories
# df['factor'].fillna(1.0, inplace=True)
# df['offset'].fillna(0.0, inplace=True)

# # Select features for PCA
# features = ['length', 'start_bit', 'factor', 'offset']
# X = df[features].values

# from sklearn.decomposition import PCA
# import matplotlib.pyplot as plt

# pca = PCA(n_components=2)
# X_pca = pca.fit_transform(X)

# # Add PCA results to df
# df['pca_x'] = X_pca[:, 0]
# df['pca_y'] = X_pca[:, 1]

# import seaborn as sns

# plt.figure(figsize=(10, 6))
# sns.scatterplot(data=df, x='pca_x', y='pca_y', hue='brand_name', style='model_name')
# plt.title('PCA of Signal Layouts Across Car Brands/Models')
# plt.show()

import sqlite3
import pandas as pd

# Connect to your database
conn = sqlite3.connect("can.db")

# Query shared message_ids across models of the same manufacturer
query = """
SELECT 
    manufacturer,
    message_id,
    car_model
FROM messages
WHERE message_id IN (
    SELECT message_id
    FROM messages
    GROUP BY manufacturer, message_id
    HAVING COUNT(DISTINCT car_model) > 1
)
ORDER BY manufacturer, message_id, car_model;
"""

df = pd.read_sql_query(query, conn)
import seaborn as sns
import matplotlib.pyplot as plt

# Pivot the data: rows = message_id, columns = car_model
pivot = df.pivot_table(index='message_id', columns='car_model', 
                       values='manufacturer', aggfunc='first')

# Replace non-null with 1 (present), NaN with 0 (absent)
pivot = pivot.notna().astype(int)

plt.figure(figsize=(12, 8))
sns.heatmap(pivot, cmap="YlGnBu", cbar=True)
plt.title("Shared Message IDs Across Car Models")
plt.ylabel("Message ID")
plt.xlabel("Car Model")
plt.tight_layout()
plt.show()
