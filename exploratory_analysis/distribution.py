import pandas as pd
import numpy as np
from scipy.stats import norm

# Extract trait counts as an array
trait_counts = df['trait_count'].values

# Fit a normal distribution to the trait counts
mu, sigma = norm.fit(trait_counts)

# Calculate rarity based on the position within the distribution
def calculate_distribution_rarity(trait_count):
    rarity = 1 - norm.cdf(trait_count, mu, sigma)
    return rarity

# Example usage
df['distribution_rarity'] = df['trait_count'].apply(calculate_distribution_rarity)
