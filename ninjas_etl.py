import pandas as pd
import numpy as np
import time
import os
from datetime import datetime

def etl_data_cleaning(data_path, data_name):
    print(f"\n🔍 Loading dataset: {data_path}")

    # Load data
    if not os.path.exists(data_path):
        print("❌ Path not found! Please double-check and try again.")
        return None, None

    if data_path.endswith('.csv'):
        df = pd.read_csv(data_path, encoding_errors='ignore')
    elif data_path.endswith('.xlsx'):
        df = pd.read_excel(data_path)
    else:
        print("❌ Unsupported file type. Please use CSV or Excel.")
        return None, None

    print(f"✅ Dataset loaded. {df.shape[0]} rows × {df.shape[1]} columns")

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


    # Clean 'name' column: remove titles, impute missing
    if 'name' in df.columns:
        df['name'] = df['name'].str.replace(r'^(Dr|Mr|Mrs|Ms|MD|DDS|DVM)\.?\s+', '', regex=True).str.strip()
        df['name'] = df['name'].fillna("Unknown")  # New: Impute missing names
    # After Clean 'name' column
    print(f"Summary: Missing names imputed: {df['name'].eq('Unknown').sum()}. Titles removed from names.")

    # Clean 'email' column: lowercase, strip, impute missing
    if 'email' in df.columns:
        df['email'] = df['email'].str.lower().str.strip()
        df['email'] = df['email'].fillna("no_email@unknown.com")  # New: Impute missing emails
    # After Clean 'email' column
    print(f"Summary: Missing emails imputed: {df['email'].eq('no_email@unknown.com').sum()}. Emails standardized to lowercase.")

    # Convert 'birthdate' to datetime, drop invalid, add age
    if 'birthdate' in df.columns:
        df['birthdate'] = pd.to_datetime(df['birthdate'], errors='coerce')
        df = df[df['birthdate'].notna()]
        df['age'] = df['birthdate'].apply(lambda x: datetime.now().year - x.year)
        # New: Flag suspicious ages
        df['age_flag'] = df['age'].apply(lambda x: 'Suspicious' if x < 0 or x > 100 else 'Valid')
        # New: Add birthdate string format
        df['birthdate_str'] = df['birthdate'].dt.strftime('%d-%m-%Y')
    # After Convert 'birthdate' to datetime, drop invalid, add age
    print(f"Summary: Invalid birthdates dropped: {df['birthdate'].isna().sum()}. Suspicious ages flagged: {df['age_flag'].eq('Suspicious').sum()}. Birthdate string format added.")

    # Clean and validate 'signup_date', add days since signup
    if 'signup_date' in df.columns:
        df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
        df = df[df['signup_date'].notna()]  # Drop missing signup_date
        today = pd.Timestamp.today()
        df = df[df['signup_date'] <= today]  # New: Drop future signup dates
        df['days_since_signup'] = (today - df['signup_date']).dt.days  # New: Days since signup
        # New: Add signup_date string format
        df['signup_date_str'] = df['signup_date'].dt.strftime('%d-%m-%Y')
    # After Clean and validate 'signup_date'
    print(f"Summary: Invalid signup dates dropped: {df['signup_date'].isna().sum()}. Future signup dates removed: {df['signup_date'].gt(today).sum()}. Days since signup and string format added.")

    # Clean 'purchase_amount': convert to numeric, fill NAs with mean (instead of 0)
    if 'purchase_amount' in df.columns:
        df['purchase_amount'] = pd.to_numeric(df['purchase_amount'], errors='coerce')
        df['purchase_amount'] = df['purchase_amount'].fillna(df['purchase_amount'].mean())  # New: Use mean

    # Normalize 'category', drop missing
    if 'category' in df.columns:
        df['category'] = df['category'].str.lower().str.strip()
        df = df[df['category'].notna()]  # New: Drop missing category
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

    # Trim whitespace from all string columns
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()

    # Checking data consistency: flagging rows where signup_date is before birthdate
    if 'birthdate' in df.columns and 'signup_date' in df.columns:
        df['date_consistency'] = df.apply(
            lambda x: 'Invalid' if pd.notna(x['birthdate']) and pd.notna(x['signup_date']) 
            and x['signup_date'] < x['birthdate'] else 'Valid', axis=1)

    # Save cleaned data
    clean_file = f"{data_name}_cleaned.csv"
    df.to_csv(clean_file, index=False)
    print(f"🎉 Dataset cleaned! Saved as: {clean_file}")
    print(f"Final shape: {df.shape[0]} rows × {df.shape[1]} columns")

    return duplicates, df

if __name__ == "__main__":
    print("🚀 Welcome to ETL Data Cleaning!")
    data_path = input("📂 Enter dataset path: ")
    data_name = input("📛 Enter dataset name: ")
    duplicates, clean_data = etl_data_cleaning(data_path, data_name)