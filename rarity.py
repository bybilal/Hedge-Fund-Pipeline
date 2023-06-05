def calculate_normalized_rarity(asset):
    max_trait_count = max([trait['trait_count'] for trait in asset['traits']])
    rarity = 1
    for trait in asset['traits']:
        trait_count = trait['trait_count']
        normalized_count = trait_count / max_trait_count
        rarity *= normalized_count
    return rarity
