"""
E-Commerce Data Preprocessing Hints
====================================
This file provides guidance for handling data quality issues.
Students should implement these transformations as part of their pipeline.
"""

import pandas as pd
import numpy as np

# HINT 1: Creating User IDs for Customer Reviews
# ===============================================
# The review data lacks user identifiers. You'll need to create them
# to build a recommendation system.

def create_user_ids(reviews_df):
    """
    Create synthetic user IDs for reviews.
    
    Simple approach: Use row index
    Better approach: Group by age + other features to identify likely same users
    """
    # Simple approach (start here):
    reviews_df['user_id'] = 'user_' + reviews_df.index.astype(str)
    
    # Advanced approach (optional challenge):
    # Group reviews by age, division, and writing style to identify same users
    # reviews_df['user_id'] = reviews_df.groupby(['Age', 'Division Name']).ngroup()
    
    return reviews_df


# HINT 2: Linking Products and Reviews
# =====================================
# Reviews use 'Clothing ID' while products use 'p_id'
# You need to verify these match and create a mapping

def link_products_reviews(products_df, reviews_df):
    """
    Create a reliable mapping between products and reviews.
    Handle missing products gracefully.
    """
    # Check which review clothing IDs actually exist in products
    valid_product_ids = set(products_df['p_id'].unique())
    reviews_with_products = reviews_df[reviews_df['Clothing ID'].isin(valid_product_ids)]
    
    print(f"Reviews with valid products: {len(reviews_with_products)}/{len(reviews_df)}")
    
    return reviews_with_products


# HINT 3: Creating User-Item Interaction Matrix
# ==============================================
# For collaborative filtering, you need user-item interactions

def create_interaction_matrix(reviews_df):
    """
    Transform reviews into user-item interaction data.
    This is essential for recommendation systems.
    """
    # Create basic interactions from reviews
    interactions = reviews_df[['user_id', 'Clothing ID', 'Rating']].copy()
    
    # Optional: Add implicit feedback (1 = reviewed, regardless of rating)
    interactions['interacted'] = 1
    
    # Create sparse matrix for collaborative filtering
    from scipy.sparse import csr_matrix
    
    user_item_matrix = pd.pivot_table(
        interactions,
        index='user_id',
        columns='Clothing ID',
        values='Rating',
        fill_value=0
    )
    
    return interactions, user_item_matrix


# HINT 4: Handling Missing Product Images
# ========================================
# Some products might not have corresponding images

def validate_product_images(products_df, image_folder='product_images'):
    """
    Check which products have missing images.
    Create a flag for products with valid images.
    """
    import os
    
    products_df['has_image'] = products_df['p_id'].apply(
        lambda pid: os.path.exists(f'{image_folder}/{pid}.jpg')
    )
    
    print(f"Products with images: {products_df['has_image'].sum()}/{len(products_df)}")
    
    return products_df


# HINT 5: Feature Engineering from Product Attributes
# ====================================================
# The p_attributes column is a string representation of a dictionary
# You'll need to parse it for useful features

def parse_product_attributes(products_df):
    """
    Extract features from the p_attributes JSON-like string.
    """
    import ast
    
    # Parse the string representation of dictionary
    products_df['attributes_dict'] = products_df['p_attributes'].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) else {}
    )
    
    # Extract specific useful features
    products_df['sleeve_length'] = products_df['attributes_dict'].apply(
        lambda x: x.get('Sleeve Length', 'Unknown')
    )
    products_df['fabric'] = products_df['attributes_dict'].apply(
        lambda x: x.get('Top Fabric', 'Unknown')
    )
    
    return products_df


# Example Usage
# =============
if __name__ == "__main__":
    # Load your data
    reviews = pd.read_csv('customer_reviews_export.csv')
    products = pd.read_csv('product_catalog_2025.csv')
    
    # Apply preprocessing
    reviews = create_user_ids(reviews)
    reviews = link_products_reviews(products, reviews)
    interactions, user_item_matrix = create_interaction_matrix(reviews)
    products = validate_product_images(products)
    products = parse_product_attributes(products)
    
    # Save preprocessed data
    reviews.to_csv('reviews_with_users.csv', index=False)
    interactions.to_csv('user_interactions.csv', index=False)
    
    print("Preprocessing complete!")
    print(f"Users: {reviews['user_id'].nunique()}")
    print(f"Items: {reviews['Clothing ID'].nunique()}")
    print(f"Interactions: {len(interactions)}")