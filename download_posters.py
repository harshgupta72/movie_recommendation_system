"""
Download movie posters for the Bollywood Movie Recommendation System
"""

import os
import requests
import time
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Poster directory
POSTER_DIR = "static/posters"

# Movie poster URLs from Wikipedia (reliable source)
MOVIE_POSTERS = {
    1: "https://upload.wikimedia.org/wikipedia/en/4/4f/Kalki_2898_AD.jpg",
    2: "https://upload.wikimedia.org/wikipedia/en/1/15/Stree_2_poster.jpg",
    3: "https://upload.wikimedia.org/wikipedia/en/4/41/Fighter_2024_poster.jpg",
    4: "https://upload.wikimedia.org/wikipedia/en/a/a5/Laapataa_Ladies.jpg",
    5: "https://upload.wikimedia.org/wikipedia/en/8/8b/Shaitaan_film_poster.jpg",
    6: "https://upload.wikimedia.org/wikipedia/en/3/30/Crew_2024_poster.jpg",
    7: "https://upload.wikimedia.org/wikipedia/en/3/31/Article_370_film_poster.jpg",
    8: "https://upload.wikimedia.org/wikipedia/en/4/45/Chandu_Champion.jpg",
    9: "https://upload.wikimedia.org/wikipedia/en/9/9f/Srikanth_%282024_film%29.jpg",
    10: "https://upload.wikimedia.org/wikipedia/en/1/1e/Maidaan_poster.jpg",
    11: "https://upload.wikimedia.org/wikipedia/en/1/1e/Pathaan_film_poster.jpg",
    12: "https://upload.wikimedia.org/wikipedia/en/2/21/Jawan_film_poster.jpg",
    13: "https://upload.wikimedia.org/wikipedia/en/9/93/Animal_%282023_film%29.jpg",
    14: "https://upload.wikimedia.org/wikipedia/en/6/68/12th_Fail_film_poster.jpg",
    15: "https://upload.wikimedia.org/wikipedia/en/d/d0/Dunki_poster.jpg",
    16: "https://upload.wikimedia.org/wikipedia/en/3/31/Tiger_3_poster.jpg",
    17: "https://upload.wikimedia.org/wikipedia/en/4/47/Sam_Bahadur.jpg",
    18: "https://upload.wikimedia.org/wikipedia/en/2/27/Rocky_Aur_Rani_Kii_Prem_Kahaani.jpg",
    19: "https://upload.wikimedia.org/wikipedia/en/7/78/OMG_2_poster.jpg",
    20: "https://upload.wikimedia.org/wikipedia/en/3/31/The_Kerala_Story.jpg",
    21: "https://upload.wikimedia.org/wikipedia/en/d/d7/RRR_Poster.jpg",
    22: "https://upload.wikimedia.org/wikipedia/en/1/15/KGF_Chapter_2.jpg",
    23: "https://upload.wikimedia.org/wikipedia/en/8/80/Drishyam_2.jpg",
    24: "https://upload.wikimedia.org/wikipedia/en/5/5e/Brahmastra_The_Beginning.jpg",
    25: "https://upload.wikimedia.org/wikipedia/en/8/80/Gangubai_Kathiawadi.jpg",
    26: "https://upload.wikimedia.org/wikipedia/en/d/de/Bhool_Bhulaiyaa_2.jpg",
    27: "https://upload.wikimedia.org/wikipedia/en/f/f4/Kantara_film_poster.jpg",
    28: "https://upload.wikimedia.org/wikipedia/en/4/43/Vikram_2022_poster.jpg",
    29: "https://upload.wikimedia.org/wikipedia/en/1/12/Rocketry_The_Nambi_Effect.jpg",
    30: "https://upload.wikimedia.org/wikipedia/en/4/43/Jhund_poster.jpg",
    31: "https://upload.wikimedia.org/wikipedia/en/3/3b/Shershaah_film_poster.jpg",
    32: "https://upload.wikimedia.org/wikipedia/en/8/86/Sardar_Udham_poster.jpg",
    33: "https://upload.wikimedia.org/wikipedia/en/6/61/Pushpa_The_Rise.jpg",
    34: "https://upload.wikimedia.org/wikipedia/en/4/45/Sooryavanshi_film_poster.jpg",
    35: "https://upload.wikimedia.org/wikipedia/en/4/44/83_film_poster.jpg",
    36: "https://upload.wikimedia.org/wikipedia/en/1/15/Mimi_2021_poster.jpg",
    37: "https://upload.wikimedia.org/wikipedia/en/d/df/3_idiots_poster.jpg",
    38: "https://upload.wikimedia.org/wikipedia/en/9/99/Dangal_Poster.jpg",
    39: "https://upload.wikimedia.org/wikipedia/en/1/1b/PK_%28film%29_poster.jpg",
    40: "https://upload.wikimedia.org/wikipedia/en/2/2e/Bajrangi_Bhaijaan_poster.jpg",
    41: "https://upload.wikimedia.org/wikipedia/en/8/80/Dilwale_Dulhania_Le_Jayenge_poster.jpg",
    42: "https://upload.wikimedia.org/wikipedia/en/4/45/Sholay_poster.jpg",
    43: "https://upload.wikimedia.org/wikipedia/en/8/8e/Lagaan_poster.jpg",
    44: "https://upload.wikimedia.org/wikipedia/en/5/59/Zindagi_Na_Milegi_Dobara_poster.jpg",
    45: "https://upload.wikimedia.org/wikipedia/en/b/ba/Barfi%21_poster.jpg",
    46: "https://upload.wikimedia.org/wikipedia/en/b/bc/Queen_Poster.jpg",
    47: "https://upload.wikimedia.org/wikipedia/en/6/63/Andhadhun_poster.jpg",
    48: "https://upload.wikimedia.org/wikipedia/en/9/95/Tumbbad_poster.jpg",
    49: "https://upload.wikimedia.org/wikipedia/en/b/b0/Stree_poster.jpg",
    50: "https://upload.wikimedia.org/wikipedia/en/2/2c/Gully_Boy_poster.jpg",
    51: "https://upload.wikimedia.org/wikipedia/en/7/7a/Uri_-_The_Surgical_Strike_poster.jpg",
    52: "https://upload.wikimedia.org/wikipedia/en/8/8d/War_film_poster.jpg",
    53: "https://upload.wikimedia.org/wikipedia/en/2/29/Tanhaji.jpg",
    54: "https://upload.wikimedia.org/wikipedia/en/e/e4/Singham_poster.jpg",
    55: "https://upload.wikimedia.org/wikipedia/en/f/fb/Dhoom_3_Film_Poster.jpg",
    56: "https://upload.wikimedia.org/wikipedia/en/3/3f/Chhichhore_Poster.jpg",
    57: "https://upload.wikimedia.org/wikipedia/en/d/d5/Kabir_Singh_poster.jpg",
    58: "https://upload.wikimedia.org/wikipedia/en/5/51/Raazi_poster.jpg",
    59: "https://upload.wikimedia.org/wikipedia/en/0/0b/Article_15_poster.jpg",
    60: "https://upload.wikimedia.org/wikipedia/en/9/96/Badhaai_Ho.jpg",
    61: "https://upload.wikimedia.org/wikipedia/en/b/be/Kahaani_poster.jpg",
    62: "https://upload.wikimedia.org/wikipedia/en/e/e8/A_Wednesday.jpg",
    63: "https://upload.wikimedia.org/wikipedia/en/b/bf/Special_26_poster.jpg",
    64: "https://upload.wikimedia.org/wikipedia/en/2/2a/Gangs_of_wasseypur.jpg",
    65: "https://upload.wikimedia.org/wikipedia/en/d/d5/Badla_poster.jpg",
    66: "https://upload.wikimedia.org/wikipedia/en/7/7d/Kabhi_Khushi_Kabhie_Gham_poster.jpg",
    67: "https://upload.wikimedia.org/wikipedia/en/c/c5/Kuch_Kuch_Hota_Hai_poster.jpg",
    68: "https://upload.wikimedia.org/wikipedia/en/a/ac/Jab_We_Met_poster.jpg",
    69: "https://upload.wikimedia.org/wikipedia/en/c/c8/Yeh_Jawaani_Hai_Deewani_Poster.jpg",
    70: "https://upload.wikimedia.org/wikipedia/en/2/24/Dil_Chahta_Hai_poster.jpg",
    71: "https://upload.wikimedia.org/wikipedia/en/1/17/Sanju_film_poster.jpg",
    72: "https://upload.wikimedia.org/wikipedia/en/0/08/Bhaag_Milkha_Bhaag_poster.jpg",
    73: "https://upload.wikimedia.org/wikipedia/en/8/82/Super_30_film_poster.jpg",
    74: "https://upload.wikimedia.org/wikipedia/en/b/b2/Mary_Kom_poster.jpg",
    75: "https://upload.wikimedia.org/wikipedia/en/f/f3/Pad_Man_film_poster.jpg",
    76: "https://upload.wikimedia.org/wikipedia/en/1/10/Hera_Pheri.jpg",
    77: "https://upload.wikimedia.org/wikipedia/en/1/1d/Munna_Bhai_M.B.B.S._poster.jpg",
    78: "https://upload.wikimedia.org/wikipedia/en/b/b7/Lage_Raho_Munna_Bhai.jpg",
    79: "https://upload.wikimedia.org/wikipedia/en/4/4d/Golmaal_Fun_Unlimited.jpg",
    80: "https://upload.wikimedia.org/wikipedia/en/b/be/Bhool_Bhulaiyaa_poster.jpg",
    81: "https://upload.wikimedia.org/wikipedia/en/0/09/Rang_De_Basanti_poster.jpg",
    82: "https://upload.wikimedia.org/wikipedia/en/b/be/Taare_Zameen_Par_Like_Stars_on_Earth_poster.png",
    83: "https://upload.wikimedia.org/wikipedia/en/1/19/Swades_poster.jpg",
    84: "https://upload.wikimedia.org/wikipedia/en/e/e7/Black_2005_film_poster.jpg",
    85: "https://upload.wikimedia.org/wikipedia/en/4/42/Chak_De%21_India_poster.jpg",
    86: "https://upload.wikimedia.org/wikipedia/en/d/d9/Darlings_film_poster.jpg",
    87: "https://upload.wikimedia.org/wikipedia/en/4/4b/Monica%2C_O_My_Darling.jpg",
    88: "https://upload.wikimedia.org/wikipedia/en/2/22/Ponniyin_Selvan_I.jpg",
    89: "https://upload.wikimedia.org/wikipedia/en/4/46/Salaar_Part_1_-_Ceasefire.jpg",
    90: "https://upload.wikimedia.org/wikipedia/en/b/b5/HanuMan_poster.jpg",
    91: "https://upload.wikimedia.org/wikipedia/en/8/81/Gadar_2.jpg",
    92: "https://upload.wikimedia.org/wikipedia/en/f/fb/Fukrey_3_poster.jpg",
    93: "https://upload.wikimedia.org/wikipedia/en/4/46/Dream_Girl_2.jpg",
    94: "https://upload.wikimedia.org/wikipedia/en/2/21/Mission_Majnu_poster.jpg",
    95: "https://upload.wikimedia.org/wikipedia/en/a/a9/Bholaa_poster.jpg",
    96: "https://upload.wikimedia.org/wikipedia/en/c/c5/Selfiee_poster.jpg",
    97: "https://upload.wikimedia.org/wikipedia/en/5/57/Adipurush_film_poster.jpg",
    98: "https://upload.wikimedia.org/wikipedia/en/e/e7/Kisi_Ka_Bhai_Kisi_Ki_Jaan.jpg",
    99: "https://upload.wikimedia.org/wikipedia/en/9/90/Bade_Miyan_Chote_Miyan_2024.jpg",
    100: "https://upload.wikimedia.org/wikipedia/en/d/d5/Mr._%26_Mrs._Mahi.jpg",
}

def download_poster(movie_id, url):
    """Download a movie poster"""
    # Determine file extension
    ext = ".jpg" if ".jpg" in url.lower() else ".png"
    filename = f"{POSTER_DIR}/{movie_id}{ext}"
    
    if os.path.exists(filename) or os.path.exists(f"{POSTER_DIR}/{movie_id}.jpg") or os.path.exists(f"{POSTER_DIR}/{movie_id}.png"):
        print(f"  [OK] Poster {movie_id} already exists")
        return True
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"  [OK] Downloaded poster {movie_id}")
        return True
    except Exception as e:
        print(f"  [FAIL] Poster {movie_id}: {str(e)[:50]}")
        return False

def main():
    """Download all movie posters"""
    os.makedirs(POSTER_DIR, exist_ok=True)
    
    print("="*50)
    print("Downloading Bollywood Movie Posters")
    print("="*50)
    
    success = 0
    failed = 0
    failed_ids = []
    
    for movie_id, url in MOVIE_POSTERS.items():
        result = download_poster(movie_id, url)
        if result:
            success += 1
        else:
            failed += 1
            failed_ids.append(movie_id)
        time.sleep(0.2)
    
    print("="*50)
    print(f"Download complete: {success} success, {failed} failed")
    if failed_ids:
        print(f"Failed IDs: {failed_ids}")
    print("="*50)

if __name__ == '__main__':
    main()
