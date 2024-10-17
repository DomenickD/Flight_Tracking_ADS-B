# """Convert the data into a sqlite database here"""

# import sqlite3
# import pandas as pd

# combined_df = pd.read_csv(r"data_files/combined_df.csv")
# cleaned_df = pd.read_csv(r"data_files/preprocessed_ads_b_data.csv")

# conn = sqlite3.connect("adsb_data.db")

# combined_df.to_sql("combined_data", conn, if_exists="replace", index=False)
# cleaned_df.to_sql("cleaned_data", conn, if_exists="replace", index=False)

# conn.commit()
# conn.close()


"""Create the db file on start to handle potential file size issues when loading."""

import sqlite3
import pandas as pd
import os

# Get the current working directory and define the database path
db_path = os.path.join(os.path.abspath(os.getcwd()), "adsb_data.db")

# Load the CSV data into DataFrames
combined_df = pd.read_csv(r"data_files/combined_df.csv", low_memory=False)
cleaned_df = pd.read_csv(r"data_files/preprocessed_ads_b_data.csv", low_memory=False)

# Create or Connect to the SQLite database
conn = sqlite3.connect(db_path)

# Write the DataFrames to the SQLite database
combined_df.to_sql("combined_data", conn, if_exists="replace", index=False)
cleaned_df.to_sql("cleaned_data", conn, if_exists="replace", index=False)

# Commit and close the database connection
# conn.commit()
conn.close()
