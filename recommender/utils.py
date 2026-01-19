"""
Utility functions for the Bollywood Movie Recommendation System
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Union


def handle_missing_values(df: pd.DataFrame, column: str, fill_value: str = '') -> pd.DataFrame:
    """
    Handle missing values in a DataFrame column.
    
    Args:
        df: Input DataFrame
        column: Column name to process
        fill_value: Value to fill missing entries with
        
    Returns:
        DataFrame with missing values handled
    """
    df = df.copy()
    df[column] = df[column].fillna(fill_value)
    return df


def calculate_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate Root Mean Squared Error (RMSE).
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        RMSE value
    """
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def calculate_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate Mean Absolute Error (MAE).
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        MAE value
    """
    return np.mean(np.abs(y_true - y_pred))


def print_recommendations(
    recommendations: List[Tuple], 
    title: str = "Recommendations"
) -> None:
    """
    Pretty print recommendations with IMDb ratings.
    
    Args:
        recommendations: List of recommendation tuples
        title: Title for the recommendations section
    """
    print(f"\n{'='*80}")
    print(f"🎬 {title}")
    print(f"{'='*80}")
    
    if len(recommendations) == 0:
        print("No recommendations found.")
        print(f"{'='*80}\n")
        return
    
    # Detect format based on tuple length
    if len(recommendations[0]) == 2:
        # Simple format: (title, score)
        for i, (movie, score) in enumerate(recommendations, 1):
            print(f"{i:2d}. {movie:<50} Score: {score:.4f}")
    elif len(recommendations[0]) == 4:
        # Extended format: (title, score/rating, genres/imdb, year)
        # Check if second element looks like IMDb rating (typically 1-10)
        sample_second = recommendations[0][1]
        if sample_second > 1:  # Likely IMDb rating
            print(f"{'#':<4} {'Title':<45} {'IMDb':<6} {'Genres':<25} {'Year':<6}")
            print(f"{'-'*4} {'-'*45} {'-'*6} {'-'*25} {'-'*6}")
            for i, (movie, imdb, genres, year) in enumerate(recommendations, 1):
                genres_short = genres[:22] + '...' if len(str(genres)) > 25 else genres
                print(f"{i:<4} {movie:<45} {imdb:<6.1f} {genres_short:<25} {year:<6}")
        else:  # Similarity score format
            print(f"{'#':<4} {'Title':<45} {'Score':<8} {'IMDb':<6} {'Year':<6}")
            print(f"{'-'*4} {'-'*45} {'-'*8} {'-'*6} {'-'*6}")
            for i, (movie, score, imdb, year) in enumerate(recommendations, 1):
                print(f"{i:<4} {movie:<45} {score:<8.4f} {imdb:<6.1f} {year:<6}")
    
    print(f"{'='*80}\n")


def print_movie_details(movie_info: dict) -> None:
    """
    Pretty print movie details.
    
    Args:
        movie_info: Dictionary containing movie information
    """
    print(f"\n{'='*60}")
    print(f"🎥 Movie Details")
    print(f"{'='*60}")
    print(f"Title:       {movie_info.get('title', 'N/A')}")
    print(f"Year:        {movie_info.get('year', 'N/A')}")
    print(f"IMDb Rating: {movie_info.get('imdb_rating', 'N/A')}/10 ⭐")
    print(f"Genres:      {movie_info.get('genres', 'N/A')}")
    print(f"Director:    {movie_info.get('director', 'N/A')}")
    print(f"Language:    {movie_info.get('language', 'N/A')}")
    print(f"{'='*60}\n")


def print_statistics(stats: dict) -> None:
    """
    Pretty print dataset statistics.
    
    Args:
        stats: Dictionary containing statistics
    """
    print(f"\n{'='*50}")
    print(f"📊 Dataset Statistics")
    print(f"{'='*50}")
    print(f"Total Movies:        {stats.get('num_movies', 'N/A')}")
    print(f"Total Users:         {stats.get('num_users', 'N/A')}")
    print(f"Total Ratings:       {stats.get('num_ratings', 'N/A')}")
    print(f"Unique Genres:       {stats.get('num_genres', 'N/A')}")
    print(f"Unique Directors:    {stats.get('num_directors', 'N/A')}")
    print(f"Year Range:          {stats.get('year_range', 'N/A')}")
    print(f"Avg IMDb Rating:     {stats.get('avg_imdb_rating', 0):.2f}/10")
    print(f"Avg User Rating:     {stats.get('avg_user_rating', 0):.2f}/5")
    print(f"{'='*50}\n")


def format_genres(genres: str) -> List[str]:
    """
    Convert pipe-separated genre string to list.
    
    Args:
        genres: Pipe-separated genre string (e.g., "Action|Drama|Thriller")
        
    Returns:
        List of genres
    """
    if not genres or pd.isna(genres):
        return []
    return [g.strip() for g in genres.split('|')]


def get_imdb_rating_category(rating: float) -> str:
    """
    Get a category label for IMDb rating.
    
    Args:
        rating: IMDb rating (0-10)
        
    Returns:
        Category string
    """
    if rating >= 8.5:
        return "🏆 Masterpiece"
    elif rating >= 8.0:
        return "⭐ Excellent"
    elif rating >= 7.5:
        return "👍 Very Good"
    elif rating >= 7.0:
        return "✅ Good"
    elif rating >= 6.0:
        return "👌 Above Average"
    elif rating >= 5.0:
        return "😐 Average"
    else:
        return "👎 Below Average"
