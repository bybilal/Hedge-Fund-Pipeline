import pandas as pd

# Define weights for each factor (example values)
factor_weights = {
    "Uniqueness": 0.6,
    "Popularity": 0.4,
    # Add more factors and their respective weights
}

# Calculate rarity index using weighted sum of factor scores
def calculate_rarity_index(asset):
    index = 0
    for factor in asset['factors']:
        factor_score = factor['score']
        factor_name = factor['name']
        factor_weight = factor_weights.get(factor_name, 1)  # Default weight of 1 if not specified
        index += factor_score * factor_weight
    return index

# Example usage
df['rarity_index'] = df.apply(calculate_rarity_index, axis=1)
