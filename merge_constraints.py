import pandas as pd

def merge_constraint_data():
    """Merge constraint data from reference.csv with geological_data_updated.csv"""
    
    # Read the reference CSV with constraint data
    print("Reading reference.csv...")
    try:
        ref_data = pd.read_csv("reference.csv", encoding='utf-8')
    except UnicodeDecodeError:
        print("UTF-8 failed, trying latin-1 encoding...")
        ref_data = pd.read_csv("reference.csv", encoding='latin-1')
    except:
        print("Latin-1 failed, trying cp1252 encoding...")
        ref_data = pd.read_csv("reference.csv", encoding='cp1252')
    print(f"Reference data shape: {ref_data.shape}")
    
    # Read the existing geological data
    print("Reading geological_data_updated.csv...")
    geo_data = pd.read_csv("geological_data_updated.csv")
    print(f"Geological data shape: {geo_data.shape}")
    
    # Extract constraint columns from reference data
    constraint_columns = [
        'Spatial soil variability (lateral/vertical)',
        'Rafts or boulders', 
        'Coarse soil units (including gravel)',
        'Soft  soil units - low shear strength ',
        'Overconsolidation (clays / extremely dense sands)',
        'Strong bedrock at/near seabed',
        'Uneven ground (relief)',
        'Steep slopes/margins (>5 degree angle)',
        'Active sedimentary system (inc. mobile sediments)',
        'Shallow water (<15-20 m)',
        'Deep water (<200 m)',
        'Potential fault reactivation/seismic activity',
        'Potential  slope failure',
        'Potential volcanic activity',
        'Potential conduit for fluids',
        'Active fluid flow',
        'Organic soils/gassy sediments',
        'Unknown'
    ]
    
    # Create a mapping of geological features from reference to our data
    ref_features = ref_data['Geological feature inventory'].dropna().tolist()
    geo_features = geo_data['Geological_Feature'].tolist()
    
    print("\nMatching features between datasets...")
    
    # Create merged dataset starting with geological data
    merged_data = geo_data.copy()
    
    # Add constraint columns to merged data (initialize as empty)
    for col in constraint_columns:
        merged_data[col] = ''
    
    # Match and merge constraint data
    matched_count = 0
    for idx, geo_feature in enumerate(geo_features):
        # Find matching feature in reference data
        ref_match = None
        for ref_idx, ref_feature in enumerate(ref_features):
            if pd.notna(ref_feature) and geo_feature.lower().strip() in ref_feature.lower().strip():
                ref_match = ref_idx + 1  # +1 because header is at row 0
                break
            elif pd.notna(ref_feature) and ref_feature.lower().strip() in geo_feature.lower().strip():
                ref_match = ref_idx + 1
                break
        
        if ref_match is not None and ref_match < len(ref_data):
            matched_count += 1
            print(f"Matched: {geo_feature} -> {ref_data.iloc[ref_match]['Geological feature inventory']}")
            
            # Copy constraint data
            for col in constraint_columns:
                if col in ref_data.columns:
                    constraint_value = ref_data.iloc[ref_match][col]
                    if pd.notna(constraint_value) and str(constraint_value).strip() == 'x':
                        merged_data.at[idx, col] = 'x'
        else:
            print(f"No match found for: {geo_feature}")
    
    print(f"\nMatched {matched_count} out of {len(geo_features)} features")
    
    # Save the merged data
    merged_data.to_csv('geological_data_with_constraints.csv', index=False)
    print("Saved merged data to geological_data_with_constraints.csv")
    
    # Show sample of constraint data
    print("\nSample constraint data:")
    sample_features = merged_data.head(3)
    for idx, row in sample_features.iterrows():
        print(f"\n{row['Geological_Feature']}:")
        active_constraints = []
        for col in constraint_columns:
            if row[col] == 'x':
                active_constraints.append(col)
        if active_constraints:
            print(f"  Active constraints: {active_constraints}")
        else:
            print("  No active constraints found")
    
    return merged_data

if __name__ == "__main__":
    merged_data = merge_constraint_data()