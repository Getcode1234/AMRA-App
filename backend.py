import pandas as pd
import streamlit as st
import os

def get_cheap_medicines(medicine_query):
    query = medicine_query.lower().strip()
    file_path = 'medicines.csv'
    
    # 1. File Check
    if not os.path.exists(file_path):
        st.error("Error: 'medicines.csv' file nahi mili! Pehle file folder mein rakhein.")
        return pd.DataFrame()

    # 2. Read Real Database
    df = pd.read_csv(file_path)
    
    # 3. ADVANCED SEARCH LOGIC (Brand OR Generic)
    # Dono columns mein search karega
    condition_brand = df['Brand Name'].str.lower().str.contains(query, na=False)
    condition_generic = df['Generic'].str.lower().str.contains(query, na=False)
    
    # Agar dono mein se kisi aik mein bhi match ho jaye
    match = df[condition_brand | condition_generic]
    
    if not match.empty:
        results = []
        
        # Agar aik generic ke multiple brands hon, toh sab ko list mein add karega
        for index, row in match.iterrows():
            # Sasta Alternative Add Karein
            results.append({
                "Medicine Name": row['Alternative Brand'],
                "Price (PKR)": float(row['Alt Price (PKR)']),
                "Manufacturer / Type": f"{row['Generic']} (Alternative)"
            })
            # Original Brand Add Karein taake comparison ho sake
            results.append({
                "Medicine Name": row['Brand Name'],
                "Price (PKR)": float(row['Price (PKR)']),
                "Manufacturer / Type": "Original Brand"
            })
            
        # Duplicates remove kar ke sasti price ke hisab se sort karna
        final_df = pd.DataFrame(results).drop_duplicates(subset=['Medicine Name']).sort_values(by="Price (PKR)", ascending=True)
        return final_df.reset_index(drop=True)
        
    else:
        # Agar dawai file mein nahi hai
        st.warning("Note: Yeh medicine verified database mein nahi hai, estimated data show ho raha hai.")
        mock_data = [
            {"Medicine Name": f"Alt-{medicine_query.capitalize()}", "Price (PKR)": 150.0, "Manufacturer / Type": "Local Alternative"},
            {"Medicine Name": medicine_query.capitalize(), "Price (PKR)": 350.0, "Manufacturer / Type": "Original Brand"}
        ]
        return pd.DataFrame(mock_data).sort_values(by="Price (PKR)", ascending=True)