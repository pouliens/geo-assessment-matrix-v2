import pandas as pd

def create_comprehensive_csv():
    """Create comprehensive CSV with both geological and engineering constraints"""
    
    # Read existing data
    geo_data = pd.read_csv("geological_data_with_constraints.csv")
    
    # Read engineering constraints
    eng_data = pd.read_csv("reference-engineering-constraints.csv", encoding='latin-1')
    
    # Define engineering constraint columns 
    engineering_columns = [
        'Low thermal conductivity/low water content, overheating',
        'Compressible/ contractive soils',
        'Collapsable soils ',
        'Soil changes character upon crushing ',
        'Potential important resource',
        'Cable/pipeline abrasion or bending ',
        'Freespan development',
        'Cable plough deviation',
        'Trenching technique selection',
        'Reduced shaft friction - soft sediments',
        'Scour - removal of lateral support',
        'Increased lateral load (ice, sediment)',
        'Voids/ punch through/ pile run',
        'Seabed preparation (e.g., flattening)',
        'Reduced skirt burial depth',
        'Uneven load distribution/differential settlement',
        'Lateral/vertical variability in geotechnical values',
        'Reduced overburden (vertical)',
        'Increased overburden (vertical)',
        'May not support hole while drilling',
        'Poor drivability/refusal',
        'Blowout',
        'Damage to tool/foundation during installation',
        'Unknown',
        'Potentially unsuitable ',
        'Requires individual WTG siting investigation'
    ]
    
    # Create enhanced features with engineering constraints
    enhanced_features = []
    
    for _, row in geo_data.iterrows():
        feature_name = row['Geological_Feature']
        
        # Find matching engineering constraints
        eng_constraints = []
        for eng_idx, eng_row in eng_data.iterrows():
            if pd.notna(eng_row['Geological feature inventory']) and feature_name.lower().strip() in eng_row['Geological feature inventory'].lower().strip():
                # Extract active engineering constraints
                for col in engineering_columns:
                    if col in eng_data.columns and pd.notna(eng_row[col]) and str(eng_row[col]).strip() == 'x':
                        eng_constraints.append(col.strip())
                break
        
        # Create new row with engineering constraints
        new_row = row.to_dict()
        new_row['Engineering_Constraints'] = ';'.join(eng_constraints) if eng_constraints else ''
        enhanced_features.append(new_row)
    
    # Convert to DataFrame
    enhanced_df = pd.DataFrame(enhanced_features)
    
    # Save to CSV
    enhanced_df.to_csv('geological_data_comprehensive.csv', index=False)
    
    print(f"Created comprehensive CSV with {len(enhanced_df)} features")
    print("\nSample features with constraints:")
    for _, row in enhanced_df.head(5).iterrows():
        geo_constraints = len(row['Active_Constraints'].split(';')) if pd.notna(row['Active_Constraints']) and row['Active_Constraints'] else 0
        eng_constraints = len(row['Engineering_Constraints'].split(';')) if pd.notna(row['Engineering_Constraints']) and row['Engineering_Constraints'] else 0
        print(f"  {row['Geological_Feature']}: {geo_constraints} geo + {eng_constraints} eng constraints")
    
    return enhanced_df

if __name__ == "__main__":
    create_comprehensive_csv()