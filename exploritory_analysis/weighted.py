import pandas as pd

# Define weights for each trait (example values)
trait_weights = {
    "Background": 0.5,
    "Fur": 0.8,
    "Accessory": 0.3,
    # Add more traits and their respective weights
}

# Calculate rarity using weighted sum of trait counts
def calculate_weighted_rarity(asset):
    rarity = 1
    for trait in asset['traits']:
        trait_count = trait['trait_count']
        trait_type = trait['trait_type']
        trait_weight = trait_weights.get(trait_type, 1)  # Default weight of 1 if not specified
        rarity *= trait_count * trait_weight
    return rarity

# Example usage
df = pd.DataFrame(assets)  # DataFrame of assets
df['weighted_rarity'] = df.apply(calculate_weighted_rarity, axis=1)
