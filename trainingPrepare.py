import pandas as pd
from sklearn.model_selection import train_test_split

# Load the datasets
training_df = pd.read_csv('cleaning/training.csv')
eval_df = pd.read_csv('cleaning/eval.csv')

# Split the eval dataset into testing and evaluation sets
eval_df, test_df = train_test_split(eval_df, test_size=0.5, random_state=42)

# Remove the rows in eval_df from training_df
training_df = training_df[~training_df.index.isin(eval_df.index)]

# Save the new datasets
training_df.to_csv('testset/training.csv', index=False)
# eval_df.to_csv('testset/eval_updated.csv', index=False)
test_df.to_csv('testset/test.csv', index=False)