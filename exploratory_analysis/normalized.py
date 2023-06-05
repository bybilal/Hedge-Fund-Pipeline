import pandas as pd

# Find maximum trait count for normalization
max_trait_count = df['trait_count'].max()

# Calculate rarity using normalized trait counts
def calculate_normalized_rarity(trait_count):
    normalized_count = trait_count / max_trait_count
    return normalized_count

# Example usage
df['normalized_rarity'] = df['trait_count'].apply(calculate_normalized_rarity)
