import pandas as pd

# Read the Excel file starting from different rows to find the actual data
excel_file = "T5.2a _FINAL_Geo-Assessment_Matrix _D5.4_2025_v2.xlsx"

# Try to find where the actual geological feature data starts
for start_row in range(0, 15):
    try:
        df = pd.read_excel(excel_file, sheet_name=0, skiprows=start_row, nrows=5)
        print(f"\n=== Starting from row {start_row} ===")
        print("Columns:", list(df.columns)[:10])  # First 10 columns
        
        # Look for first column that might contain geological features
        first_col = df.iloc[:, 0] if not df.empty else []
        print("First column values:")
        for i, val in enumerate(first_col):
            if pd.notna(val):
                print(f"  Row {i}: {str(val)[:100]}")
        
        # Check if this looks like geological feature data
        first_col_str = ' '.join(str(val).lower() for val in first_col if pd.notna(val))
        if any(term in first_col_str for term in ['peat', 'mud', 'sand', 'gravel', 'clay', 'rock']):
            print("*** This looks like geological feature data! ***")
            
    except Exception as e:
        print(f"Row {start_row}: Error - {e}")