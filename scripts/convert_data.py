import pandas as pd
import os

def convert_data():
    input_file = "Online Retail.xlsx"
    output_dir = "public"
    output_file = os.path.join(output_dir, "data.parquet")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Loading {input_file}...")
    try:
        # Load data with openpyxl engine
        df = pd.read_excel(input_file, engine="openpyxl")
        
        # Determine strict types to avoid Arrow conversion errors
        # Convert InvoiceDate to datetime
        if "InvoiceDate" in df.columns:
            df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
            
        if "InvoiceNo" in df.columns:
            df["InvoiceNo"] = df["InvoiceNo"].astype(str)

        if "StockCode" in df.columns:
            df["StockCode"] = df["StockCode"].astype(str)
            
        if "Description" in df.columns:
            df["Description"] = df["Description"].astype(str)
            
        if "Country" in df.columns:
            df["Country"] = df["Country"].astype(str)

        # Ensure numeric types
        if "Quantity" in df.columns:
            df["Quantity"] = pd.to_numeric(df["Quantity"], errors='coerce').fillna(0)
            
        if "UnitPrice" in df.columns:
            df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors='coerce').fillna(0.0)
            
        if "CustomerID" in df.columns:
             # CustomerID is often float in Excel but logically integer/string. Handle NaNs.
            df["CustomerID"] = df["CustomerID"].fillna(-1).astype(int).astype(str)

        print(f"Converting to Parquet...")
        df.to_parquet(output_file, index=False)
        print(f"Success! Saved to {output_file}")
        
    except Exception as e:
        print(f"Error converting data: {e}")

if __name__ == "__main__":
    convert_data()
