import pandas as pd
data = pd.read_csv('../dataset/niubi.csv')
n_user = len(list(set(data["user_id"]))) + 1  # 根据数据集设置
n_item = len(list(set(data["movie_id"]))) + 1
print(n_item,n_user)