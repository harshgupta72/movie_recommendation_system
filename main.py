"""
Main script for Bollywood Movie Recommendation System
Provides a command-line interface for getting movie recommendations
"""

import argparse
import sys
import os

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


def main():
    """Main function to run the recommendation system."""
    parser = argparse.ArgumentParser(
        description='🎬 Bollywood Movie Recommendation System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Content-based recommendation by movie title
  python main.py --method content --movie "Pathaan"
  
  # Content-based recommendation with IMDb filter
  python main.py --method content --movie "3 Idiots" --min-imdb 7.0
  
  # Top movies by IMDb rating
  python main.py --method imdb --min-imdb 8.0
  
  # Top movies by IMDb rating with genre filter
  python main.py --method imdb --genres Action Drama --min-imdb 7.5
  
  # Content-based recommendation by genre
  python main.py --method content --genres Action Thriller
  
  # Movies by director
  python main.py --method director --director "Rajkumar Hirani"
  
  # Collaborative filtering (user-based)
  python main.py --method collaborative --user-id 1
  
  # Collaborative filtering (item-based)
  python main.py --method collaborative --user-id 1 --cf-method item
        """
    )
    
    parser.add_argument(
        '--method',
        type=str,
        choices=['content', 'collaborative', 'imdb', 'director'],
        required=True,
        help='Recommendation method: content, collaborative, imdb, or director'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='data',
        help='Directory containing dataset files (default: data)'
    )
    
    # Content-based arguments
    parser.add_argument(
        '--movie',
        type=str,
        help='Movie title for content-based recommendations'
    )
    
    parser.add_argument(
        '--movie-id',
        type=int,
        help='Movie ID for content-based recommendations'
    )
    
    parser.add_argument(
        '--genres',
        nargs='+',
        help='List of genres (e.g., Action Thriller Drama)'
    )
    
    # Director argument
    parser.add_argument(
        '--director',
        type=str,
        help='Director name for recommendations'
    )
    
    # IMDb rating arguments
    parser.add_argument(
        '--min-imdb',
        type=float,
        default=0.0,
        help='Minimum IMDb rating filter (default: 0.0)'
    )
    
    parser.add_argument(
        '--year-from',
        type=int,
        help='Minimum year filter for movies'
    )
    
    # Collaborative filtering arguments
    parser.add_argument(
        '--user-id',
        type=int,
        help='User ID for collaborative filtering recommendations'
    )
    
    parser.add_argument(
        '--cf-method',
        type=str,
        choices=['user', 'item'],
        default='user',
        help='Collaborative filtering method: user or item (default: user)'
    )
    
    # Common arguments
    parser.add_argument(
        '--n',
        type=int,
        default=10,
        help='Number of recommendations to return (default: 10)'
    )
    
    parser.add_argument(
        '--min-rating',
        type=float,
        default=3.0,
        help='Minimum predicted rating for collaborative filtering (default: 3.0)'
    )
    
    args = parser.parse_args()
    
    # Load data
    print("\n🎬 Bollywood Movie Recommendation System")
    print("="*50)
    print("\n📂 Loading dataset...")
    
    try:
        loader = DataLoader(data_dir=args.data_dir)
        movies_df, ratings_df = loader.load_all()
        
        # Print statistics
        stats = loader.get_statistics()
        print_statistics(stats)
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\nPlease ensure the dataset files (movies.csv and ratings.csv) are in the data/ directory.")
        sys.exit(1)
    
    # Run recommendation based on method
    if args.method == 'content':
        print("🔧 Building content-based recommendation model...")
        content_recommender = ContentBasedRecommender(movies_df)
        
        recommendations = []
        
        if args.movie:
            # Find movie by title
            movie_id = content_recommender.get_movie_id_by_title(args.movie)
            if movie_id is None:
                print(f"❌ Error: Movie '{args.movie}' not found in dataset.")
                sys.exit(1)
            
            # Print movie details
            movie_info = loader.get_movie_info(movie_id)
            print_movie_details(movie_info)
            
            print(f"🔍 Finding movies similar to: {args.movie}")
            recommendations = content_recommender.recommend_by_movie(
                movie_id, 
                n_recommendations=args.n,
                min_imdb_rating=args.min_imdb
            )
            
        elif args.movie_id:
            # Use movie ID directly
            movie_info = loader.get_movie_info(args.movie_id)
            if movie_info is None:
                print(f"❌ Error: Movie ID {args.movie_id} not found in dataset.")
                sys.exit(1)
            
            print_movie_details(movie_info)
            print(f"🔍 Finding movies similar to: {movie_info['title']}")
            recommendations = content_recommender.recommend_by_movie(
                args.movie_id,
                n_recommendations=args.n,
                min_imdb_rating=args.min_imdb
            )
            
        elif args.genres:
            # Recommend by genres
            print(f"🔍 Finding movies with genres: {', '.join(args.genres)}")
            recommendations = content_recommender.recommend_by_genre(
                args.genres,
                n_recommendations=args.n,
                min_imdb_rating=args.min_imdb
            )
            
        else:
            print("❌ Error: For content-based recommendations, specify --movie, --movie-id, or --genres")
            sys.exit(1)
        
        if recommendations:
            print_recommendations(recommendations, "Content-Based Recommendations")
        else:
            print("No recommendations found. Try lowering --min-imdb filter.")
    
    elif args.method == 'imdb':
        print("🔧 Building IMDb-based recommendation model...")
        content_recommender = ContentBasedRecommender(movies_df)
        
        print(f"🔍 Finding top movies by IMDb rating (min: {args.min_imdb})")
        recommendations = content_recommender.recommend_by_imdb_rating(
            n_recommendations=args.n,
            min_rating=args.min_imdb if args.min_imdb > 0 else 7.0,
            genres=args.genres,
            year_from=args.year_from
        )
        
        if recommendations:
            print_recommendations(recommendations, "Top Bollywood Movies by IMDb Rating")
        else:
            print("No movies found. Try lowering --min-imdb filter.")
    
    elif args.method == 'director':
        if not args.director:
            print("❌ Error: --director is required for director-based recommendations")
            sys.exit(1)
        
        print("🔧 Building director-based recommendation model...")
        content_recommender = ContentBasedRecommender(movies_df)
        
        print(f"🔍 Finding movies by director: {args.director}")
        recommendations = content_recommender.recommend_by_director(
            args.director,
            n_recommendations=args.n
        )
        
        if recommendations:
            print_recommendations(recommendations, f"Movies by {args.director}")
        else:
            print(f"No movies found for director: {args.director}")
    
    elif args.method == 'collaborative':
        if args.user_id is None:
            print("❌ Error: --user-id is required for collaborative filtering")
            sys.exit(1)
        
        print(f"🔧 Building {args.cf_method}-based collaborative filtering model...")
        cf_recommender = CollaborativeFilteringRecommender(
            ratings_df,
            movies_df,
            method=args.cf_method
        )
        
        # Check if user exists and show their history
        user_ratings = loader.get_user_ratings(args.user_id)
        if len(user_ratings) == 0:
            print(f"❌ Error: User ID {args.user_id} not found in dataset.")
            print(f"Available user IDs: 1-{ratings_df['userId'].max()}")
            sys.exit(1)
        
        print(f"\n👤 User {args.user_id} has rated {len(user_ratings)} movies")
        print("\n🎬 Top rated movies by this user:")
        top_user_ratings = user_ratings.nlargest(5, 'rating')
        for _, row in top_user_ratings.iterrows():
            rating_cat = get_imdb_rating_category(row['imdb_rating'])
            print(f"   ⭐ {row['rating']:.1f}/5  |  {row['title']} ({row['year']}) - IMDb: {row['imdb_rating']}")
        
        print(f"\n🔍 Generating recommendations for user {args.user_id}...")
        recommendations = cf_recommender.recommend_for_user(
            args.user_id,
            n_recommendations=args.n,
            min_rating=args.min_rating
        )
        
        if recommendations:
            print_recommendations(
                recommendations, 
                f"{args.cf_method.capitalize()}-Based Collaborative Filtering Recommendations"
            )
        else:
            print("No recommendations found. Try lowering --min-rating or using a different user.")


if __name__ == '__main__':
    main()
