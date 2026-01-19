"""
Data loading and preprocessing module for Bollywood Movie Recommendation System
Supports IMDb ratings, genres, directors, and year-based filtering
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional, List
import os


class DataLoader:
    """
    Handles loading and preprocessing of Bollywood movie dataset with IMDb ratings.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize DataLoader.
        
        Args:
            data_dir: Directory containing the dataset files
        """
        self.data_dir = data_dir
        self.movies_df = None
        self.ratings_df = None
        
    def load_movies(self, filename: str = "movies.csv") -> pd.DataFrame:
        """
        Load movies dataset with IMDb ratings.
        
        Expected columns: movieId, title, genres, imdb_rating, year, director, language
        
        Args:
            filename: Name of the movies CSV file
            
        Returns:
            DataFrame containing movie information
        """
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"Movies file not found at {filepath}. "
                "Please ensure movies.csv exists in the data directory."
            )
        
        self.movies_df = pd.read_csv(filepath)
        
        # Handle missing values
        self.movies_df['genres'] = self.movies_df['genres'].fillna('')
        self.movies_df['title'] = self.movies_df['title'].fillna('Unknown')
        self.movies_df['imdb_rating'] = self.movies_df['imdb_rating'].fillna(0.0)
        self.movies_df['year'] = self.movies_df['year'].fillna(0).astype(int)
        self.movies_df['director'] = self.movies_df['director'].fillna('Unknown')
        self.movies_df['language'] = self.movies_df['language'].fillna('Hindi')
        
        # Ensure movieId is integer
        self.movies_df['movieId'] = self.movies_df['movieId'].astype(int)
        
        print(f"✅ Loaded {len(self.movies_df)} Bollywood movies")
        return self.movies_df
    
    def load_ratings(self, filename: str = "ratings.csv") -> pd.DataFrame:
        """
        Load user ratings dataset.
        
        Expected columns: userId, movieId, rating, timestamp (optional)
        
        Args:
            filename: Name of the ratings CSV file
            
        Returns:
            DataFrame containing rating information
        """
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"Ratings file not found at {filepath}. "
                "Please ensure ratings.csv exists in the data directory."
            )
        
        self.ratings_df = pd.read_csv(filepath)
        
        # Handle missing values
        self.ratings_df = self.ratings_df.dropna(subset=['userId', 'movieId', 'rating'])
        
        # Ensure correct data types
        self.ratings_df['userId'] = self.ratings_df['userId'].astype(int)
        self.ratings_df['movieId'] = self.ratings_df['movieId'].astype(int)
        self.ratings_df['rating'] = self.ratings_df['rating'].astype(float)
        
        print(f"✅ Loaded {len(self.ratings_df)} ratings from {self.ratings_df['userId'].nunique()} users")
        return self.ratings_df
    
    def load_all(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load both movies and ratings datasets.
        
        Returns:
            Tuple of (movies_df, ratings_df)
        """
        movies = self.load_movies()
        ratings = self.load_ratings()
        return movies, ratings
    
    def get_movie_info(self, movie_id: int) -> Optional[dict]:
        """
        Get movie information by movie ID.
        
        Args:
            movie_id: Movie ID to look up
            
        Returns:
            Dictionary with movie information or None if not found
        """
        if self.movies_df is None:
            self.load_movies()
        
        movie = self.movies_df[self.movies_df['movieId'] == movie_id]
        if len(movie) == 0:
            return None
        
        return {
            'movieId': int(movie.iloc[0]['movieId']),
            'title': movie.iloc[0]['title'],
            'genres': movie.iloc[0]['genres'],
            'imdb_rating': float(movie.iloc[0]['imdb_rating']),
            'year': int(movie.iloc[0]['year']),
            'director': movie.iloc[0]['director'],
            'language': movie.iloc[0]['language']
        }
    
    def get_user_ratings(self, user_id: int) -> pd.DataFrame:
        """
        Get all ratings for a specific user with movie details.
        
        Args:
            user_id: User ID to look up
            
        Returns:
            DataFrame with user's ratings and movie details
        """
        if self.ratings_df is None:
            self.load_ratings()
        if self.movies_df is None:
            self.load_movies()
        
        user_ratings = self.ratings_df[self.ratings_df['userId'] == user_id].copy()
        
        # Merge with movie details
        user_ratings = user_ratings.merge(
            self.movies_df[['movieId', 'title', 'genres', 'imdb_rating', 'year']],
            on='movieId',
            how='left'
        )
        
        return user_ratings
    
    def get_top_imdb_movies(self, n: int = 10, min_rating: float = 7.0) -> pd.DataFrame:
        """
        Get top N movies by IMDb rating.
        
        Args:
            n: Number of movies to return
            min_rating: Minimum IMDb rating threshold
            
        Returns:
            DataFrame with top rated movies
        """
        if self.movies_df is None:
            self.load_movies()
        
        top_movies = self.movies_df[self.movies_df['imdb_rating'] >= min_rating].copy()
        top_movies = top_movies.sort_values('imdb_rating', ascending=False).head(n)
        
        return top_movies[['movieId', 'title', 'genres', 'imdb_rating', 'year', 'director']]
    
    def get_movies_by_genre(self, genre: str) -> pd.DataFrame:
        """
        Get movies filtered by genre.
        
        Args:
            genre: Genre to filter by (e.g., 'Action', 'Drama')
            
        Returns:
            DataFrame with movies in the specified genre
        """
        if self.movies_df is None:
            self.load_movies()
        
        genre_movies = self.movies_df[
            self.movies_df['genres'].str.contains(genre, case=False, na=False)
        ].copy()
        
        return genre_movies.sort_values('imdb_rating', ascending=False)
    
    def get_movies_by_year(self, year: int) -> pd.DataFrame:
        """
        Get movies from a specific year.
        
        Args:
            year: Release year
            
        Returns:
            DataFrame with movies from the specified year
        """
        if self.movies_df is None:
            self.load_movies()
        
        year_movies = self.movies_df[self.movies_df['year'] == year].copy()
        return year_movies.sort_values('imdb_rating', ascending=False)
    
    def get_movies_by_director(self, director: str) -> pd.DataFrame:
        """
        Get movies by a specific director.
        
        Args:
            director: Director name (partial match supported)
            
        Returns:
            DataFrame with movies by the specified director
        """
        if self.movies_df is None:
            self.load_movies()
        
        director_movies = self.movies_df[
            self.movies_df['director'].str.contains(director, case=False, na=False)
        ].copy()
        
        return director_movies.sort_values('imdb_rating', ascending=False)
    
    def create_user_movie_matrix(self) -> pd.DataFrame:
        """
        Create a user-movie rating matrix (pivot table).
        
        Returns:
            DataFrame with userId as index, movieId as columns, ratings as values
        """
        if self.ratings_df is None:
            self.load_ratings()
        
        matrix = self.ratings_df.pivot_table(
            index='userId',
            columns='movieId',
            values='rating'
        )
        
        print(f"✅ Created user-movie matrix: {matrix.shape[0]} users x {matrix.shape[1]} movies")
        return matrix
    
    def get_statistics(self) -> dict:
        """
        Get dataset statistics.
        
        Returns:
            Dictionary with dataset statistics
        """
        stats = {}
        
        if self.movies_df is not None:
            stats['num_movies'] = len(self.movies_df)
            all_genres = set()
            for genres in self.movies_df['genres']:
                all_genres.update(genres.split('|'))
            stats['num_genres'] = len(all_genres)
            stats['avg_imdb_rating'] = self.movies_df['imdb_rating'].mean()
            stats['year_range'] = f"{self.movies_df['year'].min()} - {self.movies_df['year'].max()}"
            stats['num_directors'] = self.movies_df['director'].nunique()
        
        if self.ratings_df is not None:
            stats['num_ratings'] = len(self.ratings_df)
            stats['num_users'] = self.ratings_df['userId'].nunique()
            stats['num_movies_rated'] = self.ratings_df['movieId'].nunique()
            stats['avg_user_rating'] = self.ratings_df['rating'].mean()
        
        return stats
    
    def search_movies(self, query: str) -> pd.DataFrame:
        """
        Search movies by title (partial match).
        
        Args:
            query: Search query string
            
        Returns:
            DataFrame with matching movies
        """
        if self.movies_df is None:
            self.load_movies()
        
        matches = self.movies_df[
            self.movies_df['title'].str.contains(query, case=False, na=False)
        ].copy()
        
        return matches.sort_values('imdb_rating', ascending=False)
