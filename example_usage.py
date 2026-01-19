"""
Example usage script for Bollywood Movie Recommendation System
Demonstrates all recommendation features with IMDb ratings
"""

import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from recommender.data_loader import DataLoader
from recommender.content_based import ContentBasedRecommender
from recommender.collaborative import CollaborativeFilteringRecommender
from recommender.utils import (
    print_recommendations, 
    print_movie_details, 
    print_statistics,
    get_imdb_rating_category
)


def example_top_imdb_movies():
    """Example: Get top Bollywood movies by IMDb rating."""
    print("\n" + "="*70)
    print("🏆 EXAMPLE 1: Top Bollywood Movies by IMDb Rating")
    print("="*70)
    
    loader = DataLoader(data_dir="data")
    movies_df, _ = loader.load_all()
    
    content_recommender = ContentBasedRecommender(movies_df)
    
    # Get top movies with IMDb rating >= 8.0
    print("\n📊 Top 10 Bollywood Movies (IMDb >= 8.0):")
    recommendations = content_recommender.recommend_by_imdb_rating(
        n_recommendations=10,
        min_rating=8.0
    )
    print_recommendations(recommendations, "Top IMDb Rated Bollywood Movies")


def example_content_based():
    """Example: Content-based recommendations."""
    print("\n" + "="*70)
    print("🎯 EXAMPLE 2: Content-Based Filtering")
    print("="*70)
    
    loader = DataLoader(data_dir="data")
    movies_df, _ = loader.load_all()
    
    content_recommender = ContentBasedRecommender(movies_df)
    
    # Example 1: Movies similar to "Pathaan"
    print("\n🔍 Finding movies similar to 'Pathaan'...")
    movie_id = content_recommender.get_movie_id_by_title("Pathaan")
    if movie_id:
        movie_info = loader.get_movie_info(movie_id)
        print_movie_details(movie_info)
        
        recommendations = content_recommender.recommend_by_movie(
            movie_id, 
            n_recommendations=5,
            min_imdb_rating=5.0
        )
        print_recommendations(recommendations, "Movies Similar to 'Pathaan'")
    
    # Example 2: Movies similar to "3 Idiots"
    print("\n🔍 Finding movies similar to '3 Idiots'...")
    movie_id = content_recommender.get_movie_id_by_title("3 Idiots")
    if movie_id:
        movie_info = loader.get_movie_info(movie_id)
        print_movie_details(movie_info)
        
        recommendations = content_recommender.recommend_by_movie(
            movie_id, 
            n_recommendations=5,
            min_imdb_rating=7.0
        )
        print_recommendations(recommendations, "Movies Similar to '3 Idiots' (IMDb >= 7.0)")


def example_genre_based():
    """Example: Genre-based recommendations."""
    print("\n" + "="*70)
    print("🎭 EXAMPLE 3: Genre-Based Recommendations")
    print("="*70)
    
    loader = DataLoader(data_dir="data")
    movies_df, _ = loader.load_all()
    
    content_recommender = ContentBasedRecommender(movies_df)
    
    # Action Thriller movies
    print("\n🔍 Finding Action Thriller movies...")
    recommendations = content_recommender.recommend_by_genre(
        ['Action', 'Thriller'],
        n_recommendations=5,
        min_imdb_rating=6.0
    )
    print_recommendations(recommendations, "Action Thriller Movies (IMDb >= 6.0)")
    
    # Biography Drama movies
    print("\n🔍 Finding Biography Drama movies...")
    recommendations = content_recommender.recommend_by_genre(
        ['Biography', 'Drama'],
        n_recommendations=5,
        min_imdb_rating=7.5
    )
    print_recommendations(recommendations, "Biography Drama Movies (IMDb >= 7.5)")
    
    # Comedy movies
    print("\n🔍 Finding Comedy movies...")
    recommendations = content_recommender.recommend_by_genre(
        ['Comedy'],
        n_recommendations=5,
        min_imdb_rating=7.0
    )
    print_recommendations(recommendations, "Comedy Movies (IMDb >= 7.0)")


def example_director_based():
    """Example: Director-based recommendations."""
    print("\n" + "="*70)
    print("🎬 EXAMPLE 4: Director-Based Recommendations")
    print("="*70)
    
    loader = DataLoader(data_dir="data")
    movies_df, _ = loader.load_all()
    
    content_recommender = ContentBasedRecommender(movies_df)
    
    # Rajkumar Hirani movies
    print("\n🔍 Finding movies by Rajkumar Hirani...")
    recommendations = content_recommender.recommend_by_director(
        "Rajkumar Hirani",
        n_recommendations=10
    )
    print_recommendations(recommendations, "Movies by Rajkumar Hirani")
    
    # Sanjay Leela Bhansali movies
    print("\n🔍 Finding movies by Sanjay Leela Bhansali...")
    recommendations = content_recommender.recommend_by_director(
        "Sanjay Leela Bhansali",
        n_recommendations=5
    )
    print_recommendations(recommendations, "Movies by Sanjay Leela Bhansali")


def example_collaborative():
    """Example: Collaborative filtering recommendations."""
    print("\n" + "="*70)
    print("👥 EXAMPLE 5: Collaborative Filtering")
    print("="*70)
    
    loader = DataLoader(data_dir="data")
    movies_df, ratings_df = loader.load_all()
    
    # User-based collaborative filtering for User 1
    print("\n🔍 User-Based Collaborative Filtering for User 1...")
    cf_recommender = CollaborativeFilteringRecommender(
        ratings_df, 
        movies_df, 
        method='user'
    )
    
    # Show user's rating history
    user_ratings = loader.get_user_ratings(1)
    print(f"\n👤 User 1 has rated {len(user_ratings)} movies:")
    for _, row in user_ratings.nlargest(5, 'rating').iterrows():
        print(f"   ⭐ {row['rating']:.1f}/5  |  {row['title']} - IMDb: {row['imdb_rating']}")
    
    recommendations = cf_recommender.recommend_for_user(
        user_id=1,
        n_recommendations=5,
        min_rating=3.5
    )
    print_recommendations(recommendations, "User-Based Recommendations for User 1")
    
    # Item-based collaborative filtering
    print("\n🔍 Item-Based Collaborative Filtering for User 3...")
    cf_recommender_item = CollaborativeFilteringRecommender(
        ratings_df, 
        movies_df, 
        method='item'
    )
    
    user_ratings = loader.get_user_ratings(3)
    print(f"\n👤 User 3 has rated {len(user_ratings)} movies:")
    for _, row in user_ratings.nlargest(5, 'rating').iterrows():
        print(f"   ⭐ {row['rating']:.1f}/5  |  {row['title']} - IMDb: {row['imdb_rating']}")
    
    recommendations = cf_recommender_item.recommend_for_user(
        user_id=3,
        n_recommendations=5,
        min_rating=3.5
    )
    print_recommendations(recommendations, "Item-Based Recommendations for User 3")


def example_recent_movies():
    """Example: Recent Bollywood movies (2023-2024)."""
    print("\n" + "="*70)
    print("🆕 EXAMPLE 6: Recent Bollywood Movies (2023-2024)")
    print("="*70)
    
    loader = DataLoader(data_dir="data")
    movies_df, _ = loader.load_all()
    
    content_recommender = ContentBasedRecommender(movies_df)
    
    # Top movies from 2023-2024
    print("\n🔍 Finding top movies from 2023-2024...")
    recommendations = content_recommender.recommend_by_imdb_rating(
        n_recommendations=10,
        min_rating=6.0,
        year_from=2023
    )
    print_recommendations(recommendations, "Top Bollywood Movies (2023-2024)")


if __name__ == '__main__':
    try:
        print("\n" + "🎬"*30)
        print("\n   BOLLYWOOD MOVIE RECOMMENDATION SYSTEM - EXAMPLES")
        print("\n" + "🎬"*30)
        
        # Run all examples
        example_top_imdb_movies()
        example_content_based()
        example_genre_based()
        example_director_based()
        example_collaborative()
        example_recent_movies()
        
        print("\n" + "="*70)
        print("✅ All examples completed successfully!")
        print("="*70)
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure the dataset files (movies.csv and ratings.csv) are in the data/ directory.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
