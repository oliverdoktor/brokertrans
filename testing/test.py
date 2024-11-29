import pandas as pd
import requests
import time
from typing import List, Optional
import json
from tqdm import tqdm

def translate_column(
    df: pd.DataFrame,
    source_column: str,
    target_language: str,
    base_url: str = 'http://0.0.0.0:6660',
) -> pd.DataFrame:
    """
    Translates text in a DataFrame column using a translation API and adds results as a new column.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        source_column (str): Name of the column containing text to translate
        target_language (str): Target language code (e.g., 'de', 'en', 'hu')
        base_url (str): Base URL of the translation API
        batch_size (int): Number of rows to process before saving temporary results
        sleep_time (float): Time to wait between API calls to prevent overloading
    
    Returns:
        pd.DataFrame: DataFrame with added translation column
    """
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    
    # Initialize the translations column
    target_column = f'translation_{target_language}'
    df_copy[target_column] = None
    
    # Prepare the API endpoint
    translate_url = f"{base_url}/translate/"
    
    # Initialize a list to store failed indices for retry
    failed_indices = []
    
    # Iterate through the DataFrame
    for idx, row in tqdm(df_copy.iterrows(), desc="Translating rows", total=len(df_copy)):
        # Prepare the request payload
        payload = {
            "text":  str(row[source_column]),
            "target_language": target_language
        }

        # Make the API request
        response = requests.post(
            translate_url,
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json',                    
                },
            json=payload
        )
        
        # Check if request was successful
        if response.status_code == 200:
            translation = response.json()['translated_text']
            df_copy.at[idx, target_column] = translation
        else:
            print(f"Failed to translate row {idx}: Status code {response.status_code}")
            failed_indices.append(idx)
                        
    
    # Print summary of failed translations
    if failed_indices:
        print(f"Failed to translate {len(failed_indices)} rows: {failed_indices}")
    
    return df_copy

# Example usage:
if __name__ == "__main__":
    # Load your DataFrame
    df = pd.read_csv('/data/oliver_data/repos/trans/testing/translated_output.csv')
    
    # Translate the 'source_text' column to Hungarian
    translated_df = translate_column(
        df=df,
        source_column='english',
        target_language='hu'
    )
    
    # Save the results
    translated_df.to_csv('translated_results.csv', index=False)