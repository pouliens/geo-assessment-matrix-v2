import pandas as pd

def final_comparison():
    """Final comparison between CSV and Excel data."""
    
    # Read CSV file
    print("=== CSV DATA ===")
    csv_data = pd.read_csv("geological_data.csv")
    print(f"CSV has {len(csv_data)} rows and {len(csv_data.columns)} columns")
    print("CSV columns:", list(csv_data.columns))
    print(f"CSV geological features: {len(csv_data['Geological_Feature'].unique())}")
    print()
    
    # Read Excel file with proper header row (row 7)
    print("=== EXCEL DATA ===")
    excel_data = pd.read_excel("T5.2a _FINAL_Geo-Assessment_Matrix _D5.4_2025_v2.xlsx", 
                              sheet_name=0, header=7)
    print(f"Excel has {len(excel_data)} rows and {len(excel_data.columns)} columns")
    print("Excel columns:", list(excel_data.columns)[:15])  # First 15 columns
    print()
    
    # Get geological features from both
    csv_features = set(csv_data['Geological_Feature'].str.strip().str.lower())
    excel_features = set(excel_data.iloc[:, 0].dropna().str.strip().str.lower())
    
    print("=== GEOLOGICAL FEATURES COMPARISON ===")
    print(f"CSV features: {len(csv_features)}")
    print(f"Excel features: {len(excel_features)}")
    
    # Find differences
    only_in_csv = csv_features - excel_features
    only_in_excel = excel_features - csv_features
    
    if only_in_csv:
        print(f"\\nFeatures only in CSV ({len(only_in_csv)}):")
        for feature in sorted(only_in_csv):
            print(f"  - {feature}")
    
    if only_in_excel:
        print(f"\\nFeatures only in Excel ({len(only_in_excel)}):")
        for feature in sorted(only_in_excel):
            print(f"  - {feature}")
    
    # Check matching features
    matching = csv_features.intersection(excel_features)
    print(f"\\nMatching features: {len(matching)}/{len(csv_features)} ({len(matching)/len(csv_features)*100:.1f}%)")
    
    # Sample comparison of a few matching features
    print("\\n=== SAMPLE DATA COMPARISON ===")
    sample_features = list(matching)[:3]  # First 3 matching features
    
    for feature in sample_features:
        print(f"\\n--- {feature.title()} ---")
        
        # Find in CSV
        csv_row = csv_data[csv_data['Geological_Feature'].str.lower() == feature].iloc[0]
        print(f"CSV - Setting: {csv_row['Setting']}, Process: {csv_row['Process']}")
        print(f"CSV - Piles: {csv_row['Piles_Assessment']}")
        
        # Find in Excel
        excel_row = excel_data[excel_data.iloc[:, 0].str.lower() == feature].iloc[0]
        excel_setting = excel_row.iloc[1] if len(excel_row) > 1 else "N/A"
        excel_process = excel_row.iloc[2] if len(excel_row) > 2 else "N/A"
        print(f"Excel - Setting: {excel_setting}, Process: {excel_process}")
        
        # Look for assessment data in Excel (might be in different columns)
        for i, col_val in enumerate(excel_row):
            if pd.notna(col_val) and 'constraint' in str(col_val).lower():
                print(f"Excel - Column {i}: {col_val}")
                break
    
    print("\\n=== RECOMMENDATIONS ===")
    if len(only_in_csv) > 5:
        print("⚠ CSV has significantly more features than Excel")
    elif len(only_in_excel) > 5:
        print("⚠ Excel has significantly more features than CSV")
    else:
        print("✓ Feature counts are reasonably aligned")
    
    if len(matching) / len(csv_features) > 0.8:
        print("✓ Good alignment between datasets")
    else:
        print("⚠ Significant differences between datasets - review needed")

if __name__ == "__main__":
    final_comparison()