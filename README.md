🧹 Data Ninjas ETL Pipeline 🧹
Welcome to the Data Ninjas ETL Pipeline! This Python application cleans and transforms messy datasets, ensuring they are ready for analysis. It handles duplicates, missing values, inconsistent formats, and more, with detailed logging and summaries for transparency. 🚀
✨ Features
📂 Loads CSV/Excel files: Supports .csv and .xlsx datasets.
🔁 Removes duplicates: Identifies and saves duplicates for review.
🧼 Cleans data:
Strips whitespace from strings.
Standardizes name, email, and category.
Converts and normalizes dates (birthdate, signup_date) to dd-mm-yyyy.
Imputes missing values (name, email, purchase_amount).
✅ Validates data:
Flags suspicious ages and inconsistent dates.
Removes future signup_date and invalid dates.
📊 Adds features: Computes age, days_since_signup, and normalized date strings.
📜 Logs actions: Creates a timestamped log file for all cleaning steps.
💾 Saves output: Exports cleaned data as {data_name}_cleaned.csv.
🛠️ Prerequisites
Python 3.8+
Required libraries: pandas, numpy
Install dependencies:
bash
pip install pandas numpy
📋 How to Run
Follow these steps to clean your dataset:
Clone the Repository:
bash
git clone https://github.com/your-username/data-ninjas-etl.git
cd data-ninjas-etl
Prepare Your Dataset:
Place your dataset (.csv or .xlsx) in the project directory or note its full path.
Example dataset: sample_dirty_dataset.csv (contains name, email, birthdate, signup_date, category, purchase_amount).
Run the Script:
bash
python ninjas_etl.py
Provide Inputs:
Dataset Path: Enter the path to your dataset (e.g., sample_dirty_dataset.csv or /path/to/your/data.csv).
Dataset Name: Enter a name for output files (e.g., sales).
Example:
🚀 Welcome to ETL Data Cleaning!
📂 Enter dataset path: sample_dirty_dataset.csv
📛 Enter dataset name: sales
Review Outputs:
Cleaned Data: Saved as {data_name}_cleaned.csv (e.g., sales_cleaned.csv).
Duplicates (if any): Saved as {data_name}_duplicates.csv.
Log File: Timestamped log (e.g., sales_cleaning_log_20250425_123456.log) with all actions and summaries.
Check the console for progress and summaries after each cleaning step.
📈 Example Output
For sample_dirty_dataset.csv (252 rows):
Cleaned Data: sales_cleaned.csv (242 rows after removing 10 future signup_date rows).
Log File: Records actions like:
2025-04-25 12:34:56 - Dataset loaded successfully. 252 rows × 6 columns
2025-04-25 12:34:56 - Duplicates handled: 0 found, 252 rows remain after deduplication.
2025-04-25 12:34:56 - Name cleaning: 5 missing names imputed, titles removed.
Summaries (console):
Summary: 0 duplicates found. 252 rows remain after deduplication.
Summary: Missing names imputed: 5. Titles removed from names.
🧪 Dataset Requirements
The script is tailored for datasets with these columns (optional):
name (string)
email (string)
birthdate (date)
signup_date (date)
category (string, e.g., "Toys", "Furniture")
purchase_amount (numeric or "N/A")
Other datasets can be cleaned, but some operations (e.g., date conversions) may skip if columns are missing.
🛡️ Notes
Future Dates: signup_date values after the current date (e.g., 2025-04-14) are removed as errors.
Missing Values: Imputed for name ("Unknown"), email ("no_email@unknown.com (mailto:_email@unknown.com)"), and purchase_amount (mean).
Logs: Check the log file for a detailed audit trail of all cleaning steps.
🤝 Contributing
Feel free to fork, submit issues, or create pull requests! 🌟 Add new cleaning operations or enhance logging as needed.
📧 Contact
For questions, reach rorisangputu@gmail.com
Happy cleaning! 🧼✨
