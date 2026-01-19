"""
Collaborative Filtering Recommendation System
Implements both User-Based and Item-Based Collaborative Filtering
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from typing import List, Tuple, Optional


class CollaborativeFilteringRecommender:
    """
    Collaborative Filtering Recommendation System.
    Supports both User-Based and Item-Based approaches.
    """
    
    def __init__(
        self, 
        ratings_df: pd.DataFrame,
        movies_df: pd.DataFrame,
        method: str = 'user'
    ):
        """
        Initialize Collaborative Filtering Recommender.
        
        Args:
            ratings_df: DataFrame with columns: userId, movieId, rating
            movies_df: DataFrame with columns: movieId, title
            method: 'user' for user-based or 'item' for item-based filtering
        """
        self.ratings_df = ratings_df.copy()
        self.movies_df = movies_df.copy()
        self.method = method.lower()
        
        if self.method not in ['user', 'item']:
            raise ValueError("Method must be 'user' or 'item'")
        
        # Create user-movie matrix
        self.user_movie_matrix = self.ratings_df.pivot_table(
            index='userId',
            columns='movieId',
            values='rating'
        ).fillna(0)
        
        # Create sparse matrix for efficient computation
        self.sparse_matrix = csr_matrix(self.user_movie_matrix.values)
        
        # Build similarity matrix
        self.similarity_matrix = None
        self._build_similarity_matrix()
        
        print(f"Built {self.method}-based collaborative filtering model")
        print(f"Matrix shape: {self.user_movie_matrix.shape}")
    
    def _build_similarity_matrix(self):
        """Build similarity matrix based on the chosen method."""
        if self.method == 'user':
            # User-based: compute similarity between users
            self.similarity_matrix = cosine_similarity(self.sparse_matrix)
        else:
            # Item-based: compute similarity between movies
            self.similarity_matrix = cosine_similarity(self.sparse_matrix.T)
    
    def _get_user_index(self, user_id: int) -> Optional[int]:
        """Get index of user in the matrix."""
        if user_id not in self.user_movie_matrix.index:
            return None
        return self.user_movie_matrix.index.get_loc(user_id)
    
    def _get_movie_index(self, movie_id: int) -> Optional[int]:
        """Get index of movie in the matrix."""
        if movie_id not in self.user_movie_matrix.columns:
            return None
        return self.user_movie_matrix.columns.get_loc(movie_id)
    
    def _get_movie_id_by_index(self, index: int) -> int:
        """Get movie ID by its index in the matrix."""
        return self.user_movie_matrix.columns[index]
    
    def _get_user_id_by_index(self, index: int) -> int:
        """Get user ID by its index in the matrix."""
        return self.user_movie_matrix.index[index]
    
    def predict_rating(
        self, 
        user_id: int, 
        movie_id: int,
        k: int = 50
    ) -> Optional[float]:
        """
        Predict rating for a user-movie pair.
        
        Args:
            user_id: User ID
            movie_id: Movie ID
            k: Number of similar users/items to consider
            
        Returns:
            Predicted rating or None if prediction cannot be made
        """
        if self.method == 'user':
            return self._predict_user_based(user_id, movie_id, k)
        else:
            return self._predict_item_based(user_id, movie_id, k)
    
    def _predict_user_based(
        self, 
        user_id: int, 
        movie_id: int,
        k: int = 50
    ) -> Optional[float]:
        """
        Predict rating using user-based collaborative filtering.
        
        Args:
            user_id: User ID
            movie_id: Movie ID
            k: Number of similar users to consider
            
        Returns:
            Predicted rating or None
        """
        user_idx = self._get_user_index(user_id)
        movie_idx = self._get_movie_index(movie_id)
        
        if user_idx is None or movie_idx is None:
            return None
        
        # Get user's average rating
        user_ratings = self.user_movie_matrix.iloc[user_idx]
        user_mean = user_ratings[user_ratings > 0].mean()
        
        if pd.isna(user_mean):
            return None
        
        # Get similarity scores for this user
        user_similarities = self.similarity_matrix[user_idx]
        
        # Get users who rated this movie
        movie_ratings = self.user_movie_matrix.iloc[:, movie_idx]
        rated_users = movie_ratings[movie_ratings > 0].index
        
        if len(rated_users) == 0:
            return None
        
        # Get indices of users who rated the movie
        rated_user_indices = [self._get_user_index(uid) for uid in rated_users]
        
        # Get similarities and ratings for these users
        similarities = []
        ratings = []
        
        for rated_user_idx in rated_user_indices:
            if rated_user_idx == user_idx:
                continue
            
            similarity = user_similarities[rated_user_idx]
            if similarity > 0:  # Only consider positive similarities
                rating = movie_ratings.iloc[rated_user_idx]
                similarities.append(similarity)
                ratings.append(rating)
        
        if len(similarities) == 0:
            return None
        
        # Get top k similar users
        if len(similarities) > k:
            top_k_indices = np.argsort(similarities)[-k:][::-1]
            similarities = [similarities[i] for i in top_k_indices]
            ratings = [ratings[i] for i in top_k_indices]
        
        # Calculate weighted average
        similarities = np.array(similarities)
        ratings = np.array(ratings)
        
        # Get mean ratings for similar users
        similar_user_means = []
        for rated_user_idx in rated_user_indices[:len(ratings)]:
            similar_user_ratings = self.user_movie_matrix.iloc[rated_user_idx]
            similar_user_mean = similar_user_ratings[similar_user_ratings > 0].mean()
            similar_user_means.append(similar_user_mean)
        
        similar_user_means = np.array(similar_user_means)
        
        # Weighted average prediction
        numerator = np.sum(similarities * (ratings - similar_user_means))
        denominator = np.sum(np.abs(similarities))
        
        if denominator == 0:
            return None
        
        prediction = user_mean + (numerator / denominator)
        
        # Clamp prediction to rating scale (typically 0.5 to 5.0)
        prediction = max(0.5, min(5.0, prediction))
        
        return float(prediction)
    
    def _predict_item_based(
        self, 
        user_id: int, 
        movie_id: int,
        k: int = 50
    ) -> Optional[float]:
        """
        Predict rating using item-based collaborative filtering.
        
        Args:
            user_id: User ID
            movie_id: Movie ID
            k: Number of similar items to consider
            
        Returns:
            Predicted rating or None
        """
        user_idx = self._get_user_index(user_id)
        movie_idx = self._get_movie_index(movie_id)
        
        if user_idx is None or movie_idx is None:
            return None
        
        # Get movies rated by this user
        user_ratings = self.user_movie_matrix.iloc[user_idx]
        rated_movies = user_ratings[user_ratings > 0]
        
        if len(rated_movies) == 0:
            return None
        
        # Get similarity scores for this movie
        movie_similarities = self.similarity_matrix[movie_idx]
        
        # Get similarities and ratings for movies the user has rated
        similarities = []
        ratings = []
        
        for rated_movie_id, rating in rated_movies.items():
            rated_movie_idx = self._get_movie_index(rated_movie_id)
            if rated_movie_idx is None or rated_movie_idx == movie_idx:
                continue
            
            similarity = movie_similarities[rated_movie_idx]
            if similarity > 0:  # Only consider positive similarities
                similarities.append(similarity)
                ratings.append(rating)
        
        if len(similarities) == 0:
            return None
        
        # Get top k similar items
        if len(similarities) > k:
            top_k_indices = np.argsort(similarities)[-k:][::-1]
            similarities = [similarities[i] for i in top_k_indices]
            ratings = [ratings[i] for i in top_k_indices]
        
        # Calculate weighted average
        similarities = np.array(similarities)
        ratings = np.array(ratings)
        
        numerator = np.sum(similarities * ratings)
        denominator = np.sum(np.abs(similarities))
        
        if denominator == 0:
            return None
        
        prediction = numerator / denominator
        
        # Clamp prediction to rating scale
        prediction = max(0.5, min(5.0, prediction))
        
        return float(prediction)
    
    def recommend_for_user(
        self,
        user_id: int,
        n_recommendations: int = 10,
        k: int = 50,
        min_rating: float = 3.0
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations for a user.
        
        Args:
            user_id: User ID
            n_recommendations: Number of recommendations to return
            k: Number of similar users/items to consider
            min_rating: Minimum predicted rating to include
            
        Returns:
            List of (movie_title, predicted_rating) tuples
        """
        user_idx = self._get_user_index(user_id)
        
        if user_idx is None:
            return []
        
        # Get movies already rated by user
        user_ratings = self.user_movie_matrix.iloc[user_idx]
        rated_movie_ids = set(user_ratings[user_ratings > 0].index)
        
        # Predict ratings for all unrated movies
        recommendations = []
        
        for movie_id in self.user_movie_matrix.columns:
            if movie_id in rated_movie_ids:
                continue
            
            predicted_rating = self.predict_rating(user_id, movie_id, k)
            
            if predicted_rating is not None and predicted_rating >= min_rating:
                # Get movie title
                movie_info = self.movies_df[self.movies_df['movieId'] == movie_id]
                if len(movie_info) > 0:
                    movie_title = movie_info.iloc[0]['title']
                    recommendations.append((movie_title, predicted_rating))
        
        # Sort by predicted rating (descending) and return top N
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:n_recommendations]
    
    def get_similar_users(self, user_id: int, n: int = 10) -> List[Tuple[int, float]]:
        """
        Get users similar to a given user (only for user-based method).
        
        Args:
            user_id: User ID
            n: Number of similar users to return
            
        Returns:
            List of (user_id, similarity_score) tuples
        """
        if self.method != 'user':
            raise ValueError("get_similar_users only works with user-based method")
        
        user_idx = self._get_user_index(user_id)
        if user_idx is None:
            return []
        
        similarities = list(enumerate(self.similarity_matrix[user_idx]))
        similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
        
        similar_users = []
        for idx, score in similarities[1:n+1]:  # Skip self (index 0)
            similar_user_id = self._get_user_id_by_index(idx)
            similar_users.append((similar_user_id, float(score)))
        
        return similar_users
    
    def get_similar_movies(self, movie_id: int, n: int = 10) -> List[Tuple[str, float]]:
        """
        Get movies similar to a given movie (only for item-based method).
        
        Args:
            movie_id: Movie ID
            n: Number of similar movies to return
            
        Returns:
            List of (movie_title, similarity_score) tuples
        """
        if self.method != 'item':
            raise ValueError("get_similar_movies only works with item-based method")
        
        movie_idx = self._get_movie_index(movie_id)
        if movie_idx is None:
            return []
        
        similarities = list(enumerate(self.similarity_matrix[movie_idx]))
        similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
        
        similar_movies = []
        for idx, score in similarities[1:n+1]:  # Skip self
            similar_movie_id = self._get_movie_id_by_index(idx)
            movie_info = self.movies_df[self.movies_df['movieId'] == similar_movie_id]
            if len(movie_info) > 0:
                movie_title = movie_info.iloc[0]['title']
                similar_movies.append((movie_title, float(score)))
        
        return similar_movies
