"""
Download Real Movie Posters from TMDb API
Official, Legal, High-Quality Posters
"""

import os
import requests
import time
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from tmdbv3api import TMDb, Movie, Search

POSTER_DIR = "static/posters"

# ========================================
# PASTE YOUR TMDB API KEY HERE
# ========================================
TMDB_API_KEY = "1d8ce45fc8730a6cced3084da3852e8f"  # Your TMDb API key
# ========================================

# Movie list with their exact titles and years for better search accuracy
MOVIES = [
    (1, "Kalki 2898 AD", 2024),
    (2, "Stree 2", 2024),
    (3, "Fighter", 2024),
    (4, "Laapataa Ladies", 2024),
    (5, "Shaitaan", 2024),
    (6, "Crew", 2024),
    (7, "Article 370", 2024),
    (8, "Chandu Champion", 2024),
    (9, "Srikanth", 2024),
    (10, "Maidaan", 2024),
    (11, "Pathaan", 2023),
    (12, "Jawan", 2023),
    (13, "Animal", 2023),
    (14, "12th Fail", 2023),
    (15, "Dunki", 2023),
    (16, "Tiger 3", 2023),
    (17, "Sam Bahadur", 2023),
    (18, "Rocky Aur Rani Kii Prem Kahaani", 2023),
    (19, "OMG 2", 2023),
    (20, "The Kerala Story", 2023),
    (21, "RRR", 2022),
    (22, "KGF: Chapter 2", 2022),
    (23, "Drishyam 2", 2022),
    (24, "Brahmāstra: Part One – Shiva", 2022),
    (25, "Gangubai Kathiawadi", 2022),
    (26, "Bhool Bhulaiyaa 2", 2022),
    (27, "Kantara", 2022),
    (28, "Vikram", 2022),
    (29, "Rocketry: The Nambi Effect", 2022),
    (30, "Jhund", 2022),
    (31, "Shershaah", 2021),
    (32, "Sardar Udham", 2021),
    (33, "Pushpa: The Rise", 2021),
    (34, "Sooryavanshi", 2021),
    (35, "83", 2021),
    (36, "Mimi", 2021),
    (37, "3 Idiots", 2009),
    (38, "Dangal", 2016),
    (39, "PK", 2014),
    (40, "Bajrangi Bhaijaan", 2015),
    (41, "Dilwale Dulhania Le Jayenge", 1995),
    (42, "Sholay", 1975),
    (43, "Lagaan", 2001),
    (44, "Zindagi Na Milegi Dobara", 2011),
    (45, "Barfi!", 2012),
    (46, "Queen", 2013),
    (47, "Andhadhun", 2018),
    (48, "Tumbbad", 2018),
    (49, "Stree", 2018),
    (50, "Gully Boy", 2019),
    (51, "Uri: The Surgical Strike", 2019),
    (52, "War", 2019),
    (53, "Tanhaji", 2020),
    (54, "Singham", 2011),
    (55, "Dhoom 3", 2013),
    (56, "Chhichhore", 2019),
    (57, "Kabir Singh", 2019),
    (58, "Raazi", 2018),
    (59, "Article 15", 2019),
    (60, "Badhaai Ho", 2018),
    (61, "Kahaani", 2012),
    (62, "A Wednesday", 2008),
    (63, "Special 26", 2013),
    (64, "Gangs of Wasseypur", 2012),
    (65, "Badla", 2019),
    (66, "Kabhi Khushi Kabhie Gham", 2001),
    (67, "Kuch Kuch Hota Hai", 1998),
    (68, "Jab We Met", 2007),
    (69, "Yeh Jawaani Hai Deewani", 2013),
    (70, "Dil Chahta Hai", 2001),
    (71, "Sanju", 2018),
    (72, "Bhaag Milkha Bhaag", 2013),
    (73, "Super 30", 2019),
    (74, "Mary Kom", 2014),
    (75, "Padman", 2018),
    (76, "Hera Pheri", 2000),
    (77, "Munna Bhai M.B.B.S.", 2003),
    (78, "Lage Raho Munna Bhai", 2006),
    (79, "Golmaal: Fun Unlimited", 2006),
    (80, "Bhool Bhulaiyaa", 2007),
    (81, "Rang De Basanti", 2006),
    (82, "Taare Zameen Par", 2007),
    (83, "Swades", 2004),
    (84, "Black", 2005),
    (85, "Chak De! India", 2007),
    (86, "Darlings", 2022),
    (87, "Monica, O My Darling", 2022),
    (88, "Ponniyin Selvan: I", 2022),
    (89, "Salaar: Part 1 – Ceasefire", 2023),
    (90, "HanuMan", 2024),
    (91, "Gadar 2", 2023),
    (92, "Fukrey 3", 2023),
    (93, "Dream Girl 2", 2023),
    (94, "Mission Majnu", 2023),
    (95, "Bholaa", 2023),
    (96, "Selfiee", 2023),
    (97, "Adipurush", 2023),
    (98, "Kisi Ka Bhai Kisi Ki Jaan", 2023),
    (99, "Bade Miyan Chote Miyan", 2024),
    (100, "Mr. & Mrs. Mahi", 2024),
]

def setup_tmdb():
    """Initialize TMDb API"""
    if TMDB_API_KEY == "YOUR_API_KEY_HERE":
        print("\n" + "="*60)
        print("ERROR: Please add your TMDb API key!")
        print("="*60)
        print("\nSteps:")
        print("1. Go to: https://www.themoviedb.org/settings/api")
        print("2. Request an API key (choose Developer)")
        print("3. Copy your API Key (v3 auth)")
        print("4. Open fetch_tmdb_posters.py")
        print("5. Replace 'YOUR_API_KEY_HERE' with your actual key")
        print("6. Run this script again")
        print("="*60 + "\n")
        sys.exit(1)
    
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
            print(f"  [SKIP] Movie {movie_id}: {title} - Not found on TMDb")
            return False
        
        if not hasattr(movie_data, 'poster_path') or not movie_data.poster_path:
            print(f"  [SKIP] Movie {movie_id}: {title} - No poster available")
            return False
        
        # Download poster
        poster_url = f"https://image.tmdb.org/t/p/w500{movie_data.poster_path}"
        response = requests.get(poster_url, timeout=15)
        response.raise_for_status()
        
        # Save poster
        filename = f"{POSTER_DIR}/{movie_id}.jpg"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"  [OK] Movie {movie_id}: {title} ({year})")
        return True
        
    except Exception as e:
        print(f"  [FAIL] Movie {movie_id}: {title} - {str(e)[:50]}")
        return False

def main():
    """Download all movie posters from TMDb"""
    print("\n" + "="*60)
    print("TMDb Movie Poster Downloader")
    print("Downloading Real, Official Movie Posters")
    print("="*60 + "\n")
    
    # Setup TMDb
    setup_tmdb()
    
    # Create directory
    os.makedirs(POSTER_DIR, exist_ok=True)
    
    success = 0
    failed = 0
    skipped = 0
    
    print("Starting download...\n")
    
    for movie_id, title, year in MOVIES:
        result = download_poster(movie_id, title, year)
        if result:
            success += 1
        elif result is False:
            failed += 1
        else:
            skipped += 1
        time.sleep(0.3)  # Respect API rate limits
    
    print("\n" + "="*60)
    print(f"Download Complete!")
    print(f"  Success: {success}/100")
    print(f"  Failed:  {failed}/100")
    print(f"  Skipped: {skipped}/100")
    print("="*60)
    
    if success > 80:
        print("\n✅ Great! Most posters downloaded successfully!")
        print("Refresh your browser to see real movie posters!\n")
    elif success > 50:
        print("\n⚠️  Some posters couldn't be downloaded.")
        print("The missing ones will show generated posters as fallback.\n")
    else:
        print("\n❌ Many downloads failed. Check your API key and internet.\n")

if __name__ == '__main__':
    main()
