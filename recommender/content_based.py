"""
Content-Based Filtering Recommendation System for Bollywood Movies
Uses genres, IMDb ratings, and metadata to find similar movies
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Optional


class ContentBasedRecommender:
    """
    Content-based recommendation system using movie genres and IMDb ratings.
    """
    
    def __init__(self, movies_df: pd.DataFrame):
        """
        Initialize Content-Based Recommender.
        
        Args:
            movies_df: DataFrame with columns: movieId, title, genres, imdb_rating, year, director
        """
        self.movies_df = movies_df.copy()
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.vectorizer = None
        self._build_model()
    
    def _build_model(self):
        """Build the TF-IDF model and similarity matrix."""
        # Create combined features: genres + director for better recommendations
        self.movies_df['features'] = (
            self.movies_df['genres'].apply(lambda x: x.replace('|', ' ').lower()) + ' ' +
            self.movies_df['director'].str.lower().fillna('')
        )
        
        # Initialize TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)
        )
        
        # Create TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self.movies_df['features'])
        
        # Compute cosine similarity matrix
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
        
        print(f"✅ Built content-based model with {self.similarity_matrix.shape[0]} movies")
    
    def get_movie_index(self, movie_id: int) -> Optional[int]:
        """
        Get the index of a movie in the DataFrame.
        
        Args:
            movie_id: Movie ID to look up
            
        Returns:
            Index in the DataFrame or None if not found
        """
        mask = self.movies_df['movieId'] == movie_id
        if mask.sum() == 0:
            return None
        return self.movies_df[mask].index[0]
    
    def get_movie_id_by_title(self, title: str, exact_match: bool = False) -> Optional[int]:
        """
        Get movie ID by title (partial or exact match).
        
        Args:
            title: Movie title to search for
            exact_match: If True, requires exact match; otherwise partial match
            
        Returns:
            Movie ID or None if not found
        """
        title_lower = title.lower()
        
        if exact_match:
            mask = self.movies_df['title'].str.lower() == title_lower
        else:
            mask = self.movies_df['title'].str.lower().str.contains(title_lower, na=False)
        
        matches = self.movies_df[mask]
        
        if len(matches) == 0:
            return None
        elif len(matches) == 1:
            return int(matches.iloc[0]['movieId'])
        else:
            # Multiple matches - return the one with highest IMDb rating
            best_match = matches.loc[matches['imdb_rating'].idxmax()]
            print(f"📋 Found {len(matches)} movies matching '{title}'. Using: {best_match['title']}")
            return int(best_match['movieId'])
    
    def recommend_by_movie(
        self, 
        movie_id: int, 
        n_recommendations: int = 10,
        exclude_self: bool = True,
        min_imdb_rating: float = 0.0
    ) -> List[Tuple[str, float, float, int]]:
        """
        Recommend movies similar to a given movie.
        
        Args:
            movie_id: Movie ID to base recommendations on
            n_recommendations: Number of recommendations to return
            exclude_self: Whether to exclude the input movie from results
            min_imdb_rating: Minimum IMDb rating filter
            
        Returns:
            List of (movie_title, similarity_score, imdb_rating, year) tuples
        """
        movie_idx = self.get_movie_index(movie_id)
        
        if movie_idx is None:
            return []
        
        # Get similarity scores for this movie
        similarity_scores = list(enumerate(self.similarity_matrix[movie_idx]))
        
        # Sort by similarity score (descending)
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N recommendations
        recommendations = []
        for idx, score in similarity_scores:
            if exclude_self and idx == movie_idx:
                continue
            
            movie = self.movies_df.iloc[idx]
            imdb_rating = float(movie['imdb_rating'])
            
            # Filter by minimum IMDb rating
            if imdb_rating < min_imdb_rating:
                continue
            
            movie_title = movie['title']
            year = int(movie['year'])
            recommendations.append((movie_title, float(score), imdb_rating, year))
            
            if len(recommendations) >= n_recommendations:
                break
        
        return recommendations
    
    def recommend_by_genre(
        self,
        genres: List[str],
        n_recommendations: int = 10,
        min_imdb_rating: float = 0.0
    ) -> List[Tuple[str, float, float, int]]:
        """
        Recommend movies based on genre preferences.
        
        Args:
            genres: List of genre names (e.g., ['Action', 'Drama'])
            n_recommendations: Number of recommendations to return
            min_imdb_rating: Minimum IMDb rating filter
            
        Returns:
            List of (movie_title, relevance_score, imdb_rating, year) tuples
        """
        # Create a query string from genres
        query = ' '.join(genres).lower()
        
        # Transform query using the same vectorizer
        query_vector = self.vectorizer.transform([query])
        
        # Compute similarity with all movies
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Create list of (index, score) and sort
        scored_movies = list(enumerate(similarity_scores))
        scored_movies = sorted(scored_movies, key=lambda x: x[1], reverse=True)
        
        # Get recommendations with IMDb rating filter
        recommendations = []
        for idx, score in scored_movies:
            movie = self.movies_df.iloc[idx]
            imdb_rating = float(movie['imdb_rating'])
            
            if imdb_rating < min_imdb_rating:
                continue
            
            movie_title = movie['title']
            year = int(movie['year'])
            recommendations.append((movie_title, float(score), imdb_rating, year))
            
            if len(recommendations) >= n_recommendations:
                break
        
        return recommendations
    
    def recommend_by_imdb_rating(
        self,
        n_recommendations: int = 10,
        min_rating: float = 7.0,
        genres: Optional[List[str]] = None,
        year_from: Optional[int] = None
    ) -> List[Tuple[str, float, str, int]]:
        """
        Recommend top movies by IMDb rating with optional filters.
        
        Args:
            n_recommendations: Number of recommendations to return
            min_rating: Minimum IMDb rating threshold
            genres: Optional list of genres to filter by
            year_from: Optional minimum year filter
            
        Returns:
            List of (movie_title, imdb_rating, genres, year) tuples
        """
        filtered_df = self.movies_df[self.movies_df['imdb_rating'] >= min_rating].copy()
        
        # Apply genre filter
        if genres:
            genre_pattern = '|'.join(genres)
            filtered_df = filtered_df[
                filtered_df['genres'].str.contains(genre_pattern, case=False, na=False)
            ]
        
        # Apply year filter
        if year_from:
            filtered_df = filtered_df[filtered_df['year'] >= year_from]
        
        # Sort by IMDb rating
        filtered_df = filtered_df.sort_values('imdb_rating', ascending=False)
        
        recommendations = []
        for _, movie in filtered_df.head(n_recommendations).iterrows():
            recommendations.append((
                movie['title'],
                float(movie['imdb_rating']),
                movie['genres'],
                int(movie['year'])
            ))
        
        return recommendations
    
    def recommend_by_director(
        self,
        director: str,
        n_recommendations: int = 10
    ) -> List[Tuple[str, float, str, int]]:
        """
        Recommend movies by a specific director.
        
        Args:
            director: Director name (partial match supported)
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of (movie_title, imdb_rating, genres, year) tuples
        """
        director_movies = self.movies_df[
            self.movies_df['director'].str.contains(director, case=False, na=False)
        ].copy()
        
        # Sort by IMDb rating
        director_movies = director_movies.sort_values('imdb_rating', ascending=False)
        
        recommendations = []
        for _, movie in director_movies.head(n_recommendations).iterrows():
            recommendations.append((
                movie['title'],
                float(movie['imdb_rating']),
                movie['genres'],
                int(movie['year'])
            ))
        
        return recommendations
    
    def get_similarity_score(self, movie_id_1: int, movie_id_2: int) -> Optional[float]:
        """
        Get similarity score between two movies.
        
        Args:
            movie_id_1: First movie ID
            movie_id_2: Second movie ID
            
        Returns:
            Similarity score (0-1) or None if movies not found
        """
        idx1 = self.get_movie_index(movie_id_1)
        idx2 = self.get_movie_index(movie_id_2)
        
        if idx1 is None or idx2 is None:
            return None
        
        return float(self.similarity_matrix[idx1][idx2])
