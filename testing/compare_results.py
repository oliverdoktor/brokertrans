from nltk.translate.bleu_score import corpus_bleu
from nltk.translate.meteor_score import meteor_score
import numpy as np
from tqdm import tqdm
import pandas as pd
import translators as ts
import time

def evaluate_translations(reference_translations, candidate_translations):
    """
    Evaluate translations using multiple metrics
    
    Args:
        reference_translations: List of reference (ground truth) translations
        candidate_translations: List of model-generated translations
    """
    # Convert single sentences to list of lists for BLEU
    references = [[ref.split()] for ref in reference_translations]
    candidates = [cand.split() for cand in candidate_translations]
    
    # Calculate BLEU score
    bleu_score = corpus_bleu(references, candidates)
    
    # Calculate METEOR scores
    meteor_scores = []
    for ref, cand in zip(reference_translations, candidate_translations):
        score = meteor_score([ref.split()], cand.split())
        meteor_scores.append(score)
    avg_meteor = np.mean(meteor_scores)
    
    return {
        'BLEU': bleu_score,
        'METEOR': avg_meteor,
    }

def compare_with_google_and_others(source_texts, reference_translations, my_translations, source_lang='auto', target_lang='fr'):
    """
    Compare your translations with Google Translate and other providers using translators package
    
    Args:
        source_texts: List of original texts
        reference_translations: List of reference translations
        source_lang: Source language code (e.g., 'en', 'fr', 'de')
        target_lang: Target language code
        
    Returns:
        DataFrame with comparison metrics for different translation services
    """
    # Initialize dictionaries to store translations
    translations = {
        'google': [],
        'bing': []
    }
    
    # Get translations from different services
    for text in tqdm(source_texts):
        for provider in translations.keys():
            try:
                # Add delay to respect rate limits
                time.sleep(1)
                translation = ts.translate_text(text, translator=provider, from_language=source_lang, to_language=target_lang)              
                translations[provider].append(translation)
                
            except Exception as e:
                print(f"Error with {provider}: {e}")
                translations[provider].append("")
    
    # Evaluate all systems
    metrics = {}
    for provider, provider_translations in translations.items():
        if any(provider_translations):  # Check if we have any successful translations
            metrics[provider] = evaluate_translations(reference_translations, provider_translations)
    
    # Add your system's metrics
    metrics['your_system'] = evaluate_translations(reference_translations, my_translations)
    
    # Create comparison DataFrame
    comparison_data = []
    for metric in next(iter(metrics.values())).keys():  # Get metric names from first provider
        row = {'Metric': metric}
        for provider, provider_metrics in metrics.items():
            row[provider.capitalize()] = provider_metrics[metric]
        comparison_data.append(row)
    
    comparison_df = pd.DataFrame(comparison_data)
    
    return comparison_df

if __name__ == "__main__":

    # Load your translated data
    translated_data = pd.read_csv('/data/oliver_data/repos/trans/testing/translated_results.csv')
    source_texts = translated_data['english'].tolist()
    reference_translations = translated_data['translated_value'].tolist()
    my_translations = translated_data['translation_hu'].tolist()

    # Evaluate your translations
    metrics = evaluate_translations(reference_translations, my_translations)
    print("Your translation metrics:", metrics)

    # Compare with baseline
    comparison = compare_with_google_and_others(
        source_texts,
        reference_translations,
        my_translations=my_translations,
        source_lang='en',
        target_lang='hu',        
    )
    
    print("\nComparison with baseline models:")
    print(comparison)
    comparison.to_csv('comparison.csv', index=False)