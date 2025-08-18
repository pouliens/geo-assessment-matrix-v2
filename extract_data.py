import pandas as pd

def extract_geological_data():
    """Extract geological data from Excel and create simplified CSV."""
    
    # Read Excel file with proper header row (row 7)
    excel_data = pd.read_excel("T5.2a _FINAL_Geo-Assessment_Matrix _D5.4_2025_v2.xlsx", 
                              sheet_name=0, header=7)
    
    print(f"Excel data shape: {excel_data.shape}")
    print("Columns:", excel_data.columns.tolist()[:10])
    
    # Create simplified DataFrame with essential columns
    simplified_data = pd.DataFrame()
    
    # Extract geological features (first column)
    simplified_data['Geological_Feature'] = excel_data.iloc[:, 0]
    
    # Extract setting and process (columns 1 and 2)
    if len(excel_data.columns) > 1:
        simplified_data['Setting'] = excel_data.iloc[:, 1]
    if len(excel_data.columns) > 2:
        simplified_data['Process'] = excel_data.iloc[:, 2]
    
    # Extract definition (column 3)
    if len(excel_data.columns) > 3:
        simplified_data['Definition'] = excel_data.iloc[:, 3]
    
    # Find assessment columns by looking for foundation types
    # Look for columns containing constraint assessments
    assessment_columns = {}
    for i, col in enumerate(excel_data.columns):
        col_str = str(col).lower()
        if 'piles' in col_str and 'assessment' not in col_str:
            # Look for data in this column that contains constraint info
            col_data = excel_data.iloc[:, i].dropna()
            if any('constraint' in str(val).lower() for val in col_data):
                assessment_columns['Piles_Assessment'] = i
                break
    
    # Look through the data to find assessment patterns
    print("\nLooking for assessment data...")
    for i, col in enumerate(excel_data.columns):
        if i < 50:  # Check first 50 columns
            sample_data = excel_data.iloc[:, i].dropna().astype(str)
            constraint_count = sum(1 for val in sample_data if 'constraint' in val.lower())
            if constraint_count > 10:  # If many cells contain "constraint"
                print(f"Column {i} ({col}): {constraint_count} constraint values")
    
    # For now, let's create the basic structure and fill in manually
    # Based on the Excel structure, assessments appear to be in later columns
    
    # Try to extract assessment data from the rightmost columns where data exists
    # Look for columns with "Higher Constraint", "Moderate constraint", "Lower Constraint" patterns
    
    # Initialize assessment columns
    simplified_data['Piles_Assessment'] = ''
    simplified_data['Suction_Caisson_Assessment'] = ''  
    simplified_data['GBS_Assessment'] = ''
    simplified_data['Cables_Assessment'] = ''
    
    # Look for assessment data in columns around 50-53 based on the sample we saw
    for row_idx in range(len(excel_data)):
        geological_feature = excel_data.iloc[row_idx, 0]
        if pd.notna(geological_feature) and geological_feature != 'Geological feature inventory':
            # Try to find assessment data for this row
            row_data = excel_data.iloc[row_idx, :]
            
            # Look for constraint patterns in the row
            for col_idx in range(48, min(56, len(row_data))):  # Check columns 48-55
                cell_value = row_data.iloc[col_idx] if col_idx < len(row_data) else None
                if pd.notna(cell_value) and 'constraint' in str(cell_value).lower():
                    # This is likely assessment data
                    if col_idx == 49:  # Assuming this is Piles
                        simplified_data.loc[row_idx, 'Piles_Assessment'] = cell_value
                    elif col_idx == 50:  # Assuming this is Suction Caisson  
                        simplified_data.loc[row_idx, 'Suction_Caisson_Assessment'] = cell_value
                    elif col_idx == 51:  # Assuming this is GBS
                        simplified_data.loc[row_idx, 'GBS_Assessment'] = cell_value
                    elif col_idx == 52:  # Assuming this is Cables
                        simplified_data.loc[row_idx, 'Cables_Assessment'] = cell_value
    
    # Remove rows where geological feature is empty or header-like
    simplified_data = simplified_data[simplified_data['Geological_Feature'].notna()]
    simplified_data = simplified_data[~simplified_data['Geological_Feature'].str.contains('inventory|feature', case=False, na=False)]
    
    # Add dominant constraint and comments columns (empty for now)
    simplified_data['Dominant_Constraint'] = ''
    simplified_data['Comments'] = ''
    
    print(f"\nSimplified data shape: {simplified_data.shape}")
    print("Sample features:")
    print(simplified_data['Geological_Feature'].head(10).tolist())
    
    # Save to CSV
    simplified_data.to_csv('geological_data_simplified.csv', index=False)
    print("\nSaved to geological_data_simplified.csv")
    
    return simplified_data

if __name__ == "__main__":
    data = extract_geological_data()