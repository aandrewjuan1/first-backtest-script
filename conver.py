import pandas as pd

# Load the CSV file using a comma as the separator
df = pd.read_csv('EURUSDH1.csv', sep=',')

# Save the DataFrame to a new CSV file using a tab as the separator
df.to_csv('output_file.csv', sep='\t', index=False)
