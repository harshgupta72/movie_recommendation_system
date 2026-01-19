"""
Download specific movie posters from TMDb API
"""

import os
import requests
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from tmdbv3api import TMDb, Search

POSTER_DIR = "static/posters"
TMDB_API_KEY = "1d8ce45fc8730a6cced3084da3852e8f"

# Specific movies to download
MOVIES_TO_DOWNLOAD = [
    (9, "Srikanth", 2024),
]

def setup_tmdb():
    """Initialize TMDb API"""
    tmdb = TMDb()
    tmdb.api_key = TMDB_API_KEY
    tmdb.language = 'en'
    return tmdb

def search_movie(title, year):
    """Search for a movie on TMDb"""
    try:
        search = Search()
        results = search.movies(title)
        
        if not results:
            return None
        
        # Try to find exact year match first
        for movie in results:
            if hasattr(movie, 'release_date') and movie.release_date:
                movie_year = int(movie.release_date.split('-')[0])
                if movie_year == year:
                    return movie
        
        # If no exact year match, return first result
        return results[0]
    except Exception as e:
        print(f"    Search error: {str(e)[:50]}")
        return None

def download_poster(movie_id, title, year):
    """Download movie poster from TMDb"""
    try:
        movie_data = search_movie(title, year)
        
        if not movie_data:
            print(f"  [FAIL] Movie {movie_id}: {title} - Not found on TMDb")
            return False
        
        if not hasattr(movie_data, 'poster_path') or not movie_data.poster_path:
            print(f"  [FAIL] Movie {movie_id}: {title} - No poster available")
            return False
        
        # Download poster
        poster_url = f"https://image.tmdb.org/t/p/w500{movie_data.poster_path}"
        response = requests.get(poster_url, timeout=15)
        response.raise_for_status()
        
        # Save poster
        filename = f"{POSTER_DIR}/{movie_id}.jpg"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"  [OK] Downloaded: {title} ({year})")
        print(f"      Saved as: {movie_id}.jpg")
        return True
        
    except Exception as e:
        print(f"  [FAIL] Movie {movie_id}: {title} - {str(e)[:50]}")
        return False

def main():
    """Download specific movie posters"""
    print("\n" + "="*60)
    print("Downloading Specific Movie Posters from TMDb")
    print("="*60 + "\n")
    
    # Setup TMDb
    setup_tmdb()
    
    # Create directory
    os.makedirs(POSTER_DIR, exist_ok=True)
    
    success = 0
    failed = 0
    
    for movie_id, title, year in MOVIES_TO_DOWNLOAD:
        result = download_poster(movie_id, title, year)
        if result:
            success += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"Download Complete!")
    print(f"  Success: {success}/{len(MOVIES_TO_DOWNLOAD)}")
    print(f"  Failed:  {failed}/{len(MOVIES_TO_DOWNLOAD)}")
    print("="*60)
    
    if success == len(MOVIES_TO_DOWNLOAD):
        print("\n✅ All posters downloaded successfully!")
        print("Refresh your browser to see the posters!\n")

if __name__ == '__main__':
    main()
