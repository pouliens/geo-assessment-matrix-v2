import pandas as pd
import sys

def compare_data_sources():
    """Compare CSV data with Excel file to ensure alignment."""
    
    try:
        # Read CSV file
        print("Reading CSV file...")
        csv_data = pd.read_csv("geological_data.csv")
        print(f"CSV has {len(csv_data)} rows and {len(csv_data.columns)} columns")
        print("CSV columns:", list(csv_data.columns))
        print()
        
        # Read Excel file - try different approaches
        print("Reading Excel file...")
        
        # First, let's see what sheets are available
        try:
            excel_file = pd.ExcelFile("T5.2a _FINAL_Geo-Assessment_Matrix _D5.4_2025_v2.xlsx")
            print("Available sheets:", excel_file.sheet_names)
        except:
            print("Could not read sheet names")
        
        # Try reading with different header rows
        excel_data = None
        for header_row in [0, 1, 2, 3, 4, 5]:
            try:
                test_data = pd.read_excel("T5.2a _FINAL_Geo-Assessment_Matrix _D5.4_2025_v2.xlsx", 
                                         sheet_name=0, header=header_row)
                print(f"\\nTrying header row {header_row}:")
                print(f"Excel has {len(test_data)} rows and {len(test_data.columns)} columns")
                print("First few columns:", list(test_data.columns)[:5])
                
                # Check if this looks like geological data
                cols_str = ' '.join(str(col).lower() for col in test_data.columns)
                if ('geological' in cols_str and 'feature' in cols_str) or 'setting' in cols_str or 'process' in cols_str:
                    print("*** This looks like the correct header row! ***")
                    excel_data = test_data
                    break
                    
            except Exception as e:
                print(f"Header row {header_row} failed: {e}")
                continue
        
        if excel_data is None:
            print("Could not find proper header row, using row 4 as fallback")
            excel_data = pd.read_excel("T5.2a _FINAL_Geo-Assessment_Matrix _D5.4_2025_v2.xlsx", 
                                     sheet_name=0, header=4)
        print()
        
        # Compare column names
        csv_cols = set(csv_data.columns)
        excel_cols = set(excel_data.columns)
        
        print("=== COLUMN COMPARISON ===")
        if csv_cols == excel_cols:
            print("Column names match perfectly!")
        else:
            print("Column names differ:")
            only_in_csv = csv_cols - excel_cols
            only_in_excel = excel_cols - csv_cols
            
            if only_in_csv:
                print(f"Only in CSV: {only_in_csv}")
            if only_in_excel:
                print(f"Only in Excel: {only_in_excel}")
        print()
        
        # Compare number of geological features
        if 'Geological_Feature' in csv_data.columns:
            csv_features = set(csv_data['Geological_Feature'].dropna())
            print(f"CSV has {len(csv_features)} unique geological features")
        
        if 'Geological_Feature' in excel_data.columns:
            excel_features = set(excel_data['Geological_Feature'].dropna())
            print(f"Excel has {len(excel_features)} unique geological features")
        elif 'Geological Feature' in excel_data.columns:
            excel_features = set(excel_data['Geological Feature'].dropna())
            print(f"Excel has {len(excel_features)} unique geological features")
        else:
            # Check for any column that might contain geological features
            for col in excel_data.columns:
                if 'geological' in col.lower() or 'feature' in col.lower():
                    excel_features = set(excel_data[col].dropna())
                    print(f"Excel has {len(excel_features)} unique values in column '{col}'")
                    break
        print()
        
        # Show first few rows of each for manual inspection
        print("=== FIRST 3 ROWS OF CSV ===")
        print(csv_data.head(3).to_string())
        print()
        
        print("=== FIRST 3 ROWS OF EXCEL ===")
        print(excel_data.head(3).to_string())
        print()
        
        # Check for missing data
        print("=== DATA COMPLETENESS ===")
        print("CSV missing values per column:")
        print(csv_data.isnull().sum())
        print()
        
        print("Excel missing values per column:")
        print(excel_data.isnull().sum())
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    compare_data_sources()