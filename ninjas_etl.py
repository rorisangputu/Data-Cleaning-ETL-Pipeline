import pandas as pd
import numpy as np
import os
import logging
from datetime import datetime

def etl_data_cleaning(data_path, data_name):
    print(f"\n🔍 Loading dataset: {data_path}")

    # Create log file with timestamp in name
    log_filename = f"{data_name}_cleaning_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info(f"Starting ETL cleaning for dataset: {data_path}")

    # Data Loading
    if not os.path.exists(data_path):
        print("❌ Path not found! Please double-check and try again.")
        return None, None

    if data_path.endswith('.csv'): #checks if file is csv
        df = pd.read_csv(data_path, encoding_errors='ignore') #importing file using read csv
    elif data_path.endswith('.xlsx'): #checks if file is excel
        df = pd.read_excel(data_path) #importing file using read excel
    else:
        #Error handling 
        print("❌ Unsupported file type. Please use CSV or Excel.")
        return None, None

    print(f"✅ Dataset loaded. {df.shape[0]} rows × {df.shape[1]} columns")
    logging.info(f"Dataset loaded successfully. {df.shape[0]} rows × {df.shape[1]} columns")

    # Handle duplicates
    total_duplicates = df.duplicated().sum()
    print(f"🔁 Found {total_duplicates} duplicate rows.")

    duplicates = None  # Initialize duplicates
    if total_duplicates > 0:
        duplicates = df[df.duplicated()]
        duplicates.to_csv(f"{data_name}_duplicates.csv", index=False)
        print(f"📝 Duplicates saved as: {data_name}_duplicates.csv")
        df = df.drop_duplicates()
    
    # After Handle duplicates
    print(f"Summary: {total_duplicates} duplicates found. {df.shape[0]} rows remain after deduplication.")
    
    logging.info(f"Duplicates handled: {total_duplicates} found, {df.shape[0]} rows remain after deduplication.")
    if total_duplicates > 0:
        logging.info(f"Duplicates saved to {data_name}_duplicates.csv")

    # Cleaning name column: removing titles, impute missing
    if 'name' in df.columns:
        df['name'] = df['name'].str.replace(r'^(Dr|Mr|Mrs|Ms|MD|DDS|DVM)\.?\s+', '', regex=True).str.strip()
        df['name'] = df['name'].fillna("Unknown")  # New: Impute missing names
    
    # Post cleaning name column
    print(f"Summary: Missing names imputed: {df['name'].eq('Unknown').sum()}. Titles removed from names.")
    logging.info(f"Name cleaning: {df['name'].eq('Unknown').sum()} missing names imputed, titles removed.")
    
    # Cleaning email column: changing to lowercase, strip, impute missing
    if 'email' in df.columns:
        df['email'] = df['email'].str.lower().str.strip()
        df['email'] = df['email'].fillna("no_email@unknown.com")  # New: Impute missing emails
    
    # Post cleaning email column
    print(f"Summary: Missing emails imputed: {df['email'].eq('no_email@unknown.com').sum()}. Emails standardized to lowercase.")
    logging.info(f"Email cleaning: {df['email'].eq('no_email@unknown.com').sum()} missing emails imputed, standardized to lowercase.")
    
    # Converting birthdate to datetime, drop invalid, adding age column
    if 'birthdate' in df.columns:

        df['birthdate'] = pd.to_datetime(df['birthdate'], errors='coerce')
        df = df[df['birthdate'].notna()]
        
        # New column: Ages calculated
        df['age'] = df['birthdate'].apply(lambda x: datetime.now().year - x.year)

        # New column: Flags suspicious ages
        df['age_flag'] = df['age'].apply(lambda x: 'Suspicious' if x < 0 or x > 100 else 'Valid')
        
        # New column: Adds birthdate string format
        df['birthdate_str'] = df['birthdate'].dt.strftime('%d-%m-%Y')

    # Post conversion messaging
    print(f"Summary: Invalid birthdates dropped: {df['birthdate'].isna().sum()}. Suspicious ages flagged: {df['age_flag'].eq('Suspicious').sum()}. Birthdate string format added.")
    logging.info(f"Birthdate processing: {df['birthdate'].isna().sum()} invalid birthdates dropped, {df['age_flag'].eq('Suspicious').sum()} suspicious ages flagged, string format (dd-mm-yyyy) added.")
    
    # Clean and validate signup_date, add days since signup
    if 'signup_date' in df.columns:
        df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
        df = df[df['signup_date'].notna()]  #Drop missing signup_date
        today = pd.Timestamp.today()
        df = df[df['signup_date'] <= today]  #Drop future signup dates
        df['days_since_signup'] = (today - df['signup_date']).dt.days  # Days since signup
        
        # Making signup_date string format in a different column
        df['signup_date_str'] = df['signup_date'].dt.strftime('%d-%m-%Y')
    
    # Post cleaning and validation messaging
    print(f"Summary: Invalid signup dates dropped: {df['signup_date'].isna().sum()}. Future signup dates removed: {df['signup_date'].gt(today).sum()}. Days since signup and string format added.")
    logging.info(f"Signup date processing: {df['signup_date'].isna().sum()} invalid signup dates dropped, {df['signup_date'].gt(today).sum()} future signup dates removed, days_since_signup and string format (dd-mm-yyyy) added.")

    # Cleaning purchase_amount: convert to numeric, fill NAs with mean (instead of 0)
    if 'purchase_amount' in df.columns:
        df['purchase_amount'] = pd.to_numeric(df['purchase_amount'], errors='coerce')
        df['purchase_amount'] = df['purchase_amount'].fillna(df['purchase_amount'].mean())  # New: Use mean
    
    # Post cleaning messaging
    print(f"Summary: Non-numeric purchase_amount values converted to NaN: {df['purchase_amount'].isna().sum()}. Missing values filled with mean: {df['purchase_amount'].isna().sum()}.")
    logging.info(f"Purchase amount cleaning: {df['purchase_amount'].isna().sum()} non-numeric values converted to NaN, missing values filled with mean.")

    # Normalizing category, drop missing
    if 'category' in df.columns:
        df['category'] = df['category'].str.lower().str.strip()
        df = df[df['category'].notna()]  # Drop missing category
        category_map = {
            'electronics': 'Electronics', 'electronic': 'Electronics',
            'clothing': 'Clothing', 'clothes': 'Clothing',
            'furniture': 'Furniture', 'furnitures': 'Furniture',
            'toys': 'Toys', 'toy': 'Toys',
            'books': 'Books', 'book': 'Books',
            'groceries': 'Groceries', 'grocery': 'Groceries',
            'sports': 'Sports', 'sport': 'Sports',
            'beauty': 'Beauty'
        }
        df['category'] = df['category'].map(category_map).fillna(df['category'])
    
    # Post normalisation messaging
    print(f"Summary: Missing categories dropped: {df['category'].isna().sum()}. Categories standardized: {df['category'].value_counts().to_dict()}.")
    logging.info(f"Category normalization: {df['category'].isna().sum()} missing categories dropped, standardized categories: {df['category'].value_counts().to_dict()}.")

    # Trim whitespace from all string columns
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    # After Trim whitespace from all string columns
    print(f"Summary: Whitespace trimmed from string columns: {list(df.select_dtypes(include='object').columns)}.")


    # Checking data consistency: flagging rows where signup_date is before birthdate
    if 'birthdate' in df.columns and 'signup_date' in df.columns:
        df['date_consistency'] = df.apply(
            lambda x: 'Invalid' if pd.notna(x['birthdate']) and pd.notna(x['signup_date']) 
            and x['signup_date'] < x['birthdate'] else 'Valid', axis=1)
    
    # Post check messaging
    print(f"Summary: Inconsistent dates flagged: {df['date_consistency'].eq('Invalid').sum()} invalid signup_date vs. birthdate cases.")
    logging.info(f"Data consistency check: {df['date_consistency'].eq('Invalid').sum()} invalid signup_date vs. birthdate cases flagged.")
    
    # Save cleaned data
    clean_file = f"{data_name}_cleaned.csv"
    df.to_csv(clean_file, index=False)
    print(f"🎉 Dataset cleaned! Saved as: {clean_file}")
    print(f"Final shape: {df.shape[0]} rows × {df.shape[1]} columns")
    logging.info(f"Dataset cleaned and saved as {clean_file}. Final shape: {df.shape[0]} rows × {df.shape[1]} columns")
    return duplicates, df

if __name__ == "__main__":
    print("🚀 Welcome to ETL Data Cleaning!")
    data_path = input("📂 Enter dataset path: ")
    data_name = input("📛 Enter dataset name: ")
    duplicates, clean_data = etl_data_cleaning(data_path, data_name)