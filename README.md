# 🧹 Data Ninjas ETL Pipeline 🧹

Welcome to the **Data Ninjas ETL Pipeline**!  
This Python application cleans and transforms messy datasets, ensuring they’re ready for analysis.  
It handles duplicates, missing values, inconsistent formats, and more — all with detailed logging and summaries for transparency. 🚀

---

## ✨ Features

- 📂 **Loads CSV/Excel Files**: Supports `.csv` and `.xlsx` formats.  
- 🔁 **Removes Duplicates**: Identifies and saves duplicates for review.  
- 🧼 **Cleans Data**:
  - Strips whitespace from strings  
  - Standardizes `name`, `email`, and `category` fields  
  - Converts and normalizes dates (`birthdate`, `signup_date`) to `dd-mm-yyyy`  
  - Imputes missing values for `name`, `email`, and `purchase_amount`  
- ✅ **Validates Data**:
  - Flags suspicious ages and inconsistent dates  
  - Removes future `signup_date` values and invalid dates  
- 📊 **Adds Features**:
  - Computes `age` and `days_since_signup`  
  - Creates normalized date strings  
- 📜 **Logs Actions**: Timestamped log file created for all cleaning steps  
- 💾 **Saves Output**: Cleaned data exported as `{data_name}_cleaned.csv`

---

## 🛠️ Prerequisites

- Python 3.8+
- Required libraries: `pandas`, `numpy`

**Install dependencies:**
```bash
pip install pandas numpy
```

---

## 📋 How to Run

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/data-ninjas-etl.git
   cd data-ninjas-etl
   ```

2. **Prepare Your Dataset:**
   - Place your `.csv` or `.xlsx` file in the project directory or use the full file path.
   - Example dataset: `sample_dirty_dataset.csv`

3. **Run the Script:**
   ```bash
   python ninjas_etl.py
   ```

4. **Provide Inputs When Prompted:**
   ```
   🚀 Welcome to ETL Data Cleaning!
   📂 Enter dataset path: sample_dirty_dataset.csv
   📛 Enter dataset name: sales
   ```

5. **Review Outputs:**
   - Cleaned Data: `sales_cleaned.csv`
   - Duplicates (if any): `sales_duplicates.csv`
   - Log File: `sales_cleaning_log_YYYYMMDD_HHMMSS.log`

   You'll also see summaries and progress in the console after each step.

---

## 📈 Example Output

For `sample_dirty_dataset.csv` (252 rows):

- Cleaned Data: `sales_cleaned.csv` (242 rows after removing 10 invalid `signup_date` entries)
- Log Sample:
  ```
  2025-04-25 12:34:56 - Dataset loaded successfully. 252 rows × 6 columns
  2025-04-25 12:34:56 - Duplicates handled: 0 found, 252 rows remain after deduplication.
  2025-04-25 12:34:56 - Name cleaning: 5 missing names imputed, titles removed.
  ```
- Console Summary:
  - `Summary: 0 duplicates found.`
  - `Summary: Missing names imputed: 5. Titles removed from names.`

---

## 🧪 Dataset Requirements

This script works best with datasets that include the following (optional) columns:

- `name` (string)  
- `email` (string)  
- `birthdate` (date)  
- `signup_date` (date)  
- `category` (e.g., "Toys", "Furniture")  
- `purchase_amount` (numeric or "N/A")  

Other columns can be included, but some operations (e.g., date calculations) may be skipped if columns are missing.

---

## 🛡️ Notes

- **Future Dates**: Any `signup_date` beyond the current date is considered invalid and removed.
- **Missing Values**:
  - `name` → `"Unknown"`
  - `email` → `"no_email@unknown.com"`
  - `purchase_amount` → replaced with column mean
- **Logs**: A full audit trail is saved in a timestamped log file.

---

## 🤝 Contributing

Feel free to fork the repo, submit issues, or open pull requests!  
You’re welcome to add new cleaning steps or improve logging. 🌟

---

## 📧 Contact

Questions? Reach out at [rorisangputu@gmail.com](mailto:rorisangputu@gmail.com)

---

Happy cleaning! 🧼✨
```
