"""
Generate stylish movie poster placeholders for Bollywood movies
Creates professional-looking gradient posters with movie titles
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

POSTER_DIR = "static/posters"

# Movie data with colors based on genre
MOVIES = [
    (1, "Kalki 2898 AD", ["Action", "Sci-Fi"], 2024),
    (2, "Stree 2", ["Comedy", "Horror"], 2024),
    (3, "Fighter", ["Action", "Drama"], 2024),
    (4, "Laapataa Ladies", ["Comedy", "Drama"], 2024),
    (5, "Shaitaan", ["Horror", "Thriller"], 2024),
    (6, "Crew", ["Comedy", "Crime"], 2024),
    (7, "Article 370", ["Drama", "Thriller"], 2024),
    (8, "Chandu Champion", ["Biography", "Sport"], 2024),
    (9, "Srikanth", ["Biography", "Drama"], 2024),
    (10, "Maidaan", ["Biography", "Sport"], 2024),
    (11, "Pathaan", ["Action", "Spy"], 2023),
    (12, "Jawan", ["Action", "Thriller"], 2023),
    (13, "Animal", ["Action", "Crime"], 2023),
    (14, "12th Fail", ["Biography", "Drama"], 2023),
    (15, "Dunki", ["Comedy", "Drama"], 2023),
    (16, "Tiger 3", ["Action", "Spy"], 2023),
    (17, "Sam Bahadur", ["Biography", "War"], 2023),
    (18, "Rocky Aur Rani", ["Romance", "Drama"], 2023),
    (19, "OMG 2", ["Comedy", "Drama"], 2023),
    (20, "Kerala Story", ["Drama", "Thriller"], 2023),
    (21, "RRR", ["Action", "Epic"], 2022),
    (22, "KGF Chapter 2", ["Action", "Crime"], 2022),
    (23, "Drishyam 2", ["Crime", "Mystery"], 2022),
    (24, "Brahmastra", ["Fantasy", "Action"], 2022),
    (25, "Gangubai", ["Biography", "Crime"], 2022),
    (26, "Bhool Bhulaiyaa 2", ["Comedy", "Horror"], 2022),
    (27, "Kantara", ["Action", "Drama"], 2022),
    (28, "Vikram", ["Action", "Thriller"], 2022),
    (29, "Rocketry", ["Biography", "Drama"], 2022),
    (30, "Jhund", ["Drama", "Sport"], 2022),
    (31, "Shershaah", ["Biography", "War"], 2021),
    (32, "Sardar Udham", ["Biography", "Drama"], 2021),
    (33, "Pushpa", ["Action", "Crime"], 2021),
    (34, "Sooryavanshi", ["Action", "Thriller"], 2021),
    (35, "83", ["Biography", "Sport"], 2021),
    (36, "Mimi", ["Comedy", "Drama"], 2021),
    (37, "3 Idiots", ["Comedy", "Drama"], 2009),
    (38, "Dangal", ["Biography", "Sport"], 2016),
    (39, "PK", ["Comedy", "Sci-Fi"], 2014),
    (40, "Bajrangi Bhaijaan", ["Drama", "Comedy"], 2015),
    (41, "DDLJ", ["Romance", "Drama"], 1995),
    (42, "Sholay", ["Action", "Adventure"], 1975),
    (43, "Lagaan", ["Drama", "Sport"], 2001),
    (44, "ZNMD", ["Adventure", "Comedy"], 2011),
    (45, "Barfi!", ["Romance", "Drama"], 2012),
    (46, "Queen", ["Comedy", "Drama"], 2013),
    (47, "Andhadhun", ["Thriller", "Mystery"], 2018),
    (48, "Tumbbad", ["Horror", "Fantasy"], 2018),
    (49, "Stree", ["Comedy", "Horror"], 2018),
    (50, "Gully Boy", ["Drama", "Music"], 2019),
    (51, "Uri", ["Action", "War"], 2019),
    (52, "War", ["Action", "Thriller"], 2019),
    (53, "Tanhaji", ["Action", "Biography"], 2020),
    (54, "Singham", ["Action", "Drama"], 2011),
    (55, "Dhoom 3", ["Action", "Crime"], 2013),
    (56, "Chhichhore", ["Comedy", "Drama"], 2019),
    (57, "Kabir Singh", ["Romance", "Drama"], 2019),
    (58, "Raazi", ["Thriller", "Drama"], 2018),
    (59, "Article 15", ["Crime", "Drama"], 2019),
    (60, "Badhaai Ho", ["Comedy", "Drama"], 2018),
    (61, "Kahaani", ["Mystery", "Thriller"], 2012),
    (62, "A Wednesday", ["Thriller", "Crime"], 2008),
    (63, "Special 26", ["Crime", "Thriller"], 2013),
    (64, "Gangs of Wasseypur", ["Crime", "Action"], 2012),
    (65, "Badla", ["Mystery", "Thriller"], 2019),
    (66, "K3G", ["Romance", "Drama"], 2001),
    (67, "KKHH", ["Romance", "Comedy"], 1998),
    (68, "Jab We Met", ["Romance", "Comedy"], 2007),
    (69, "YJHD", ["Romance", "Drama"], 2013),
    (70, "Dil Chahta Hai", ["Romance", "Drama"], 2001),
    (71, "Sanju", ["Biography", "Drama"], 2018),
    (72, "Bhaag Milkha", ["Biography", "Sport"], 2013),
    (73, "Super 30", ["Biography", "Drama"], 2019),
    (74, "Mary Kom", ["Biography", "Sport"], 2014),
    (75, "Pad Man", ["Biography", "Drama"], 2018),
    (76, "Hera Pheri", ["Comedy", "Crime"], 2000),
    (77, "Munna Bhai", ["Comedy", "Drama"], 2003),
    (78, "Lage Raho", ["Comedy", "Drama"], 2006),
    (79, "Golmaal", ["Comedy"], 2006),
    (80, "Bhool Bhulaiyaa", ["Horror", "Comedy"], 2007),
    (81, "Rang De Basanti", ["Drama"], 2006),
    (82, "Taare Zameen Par", ["Drama", "Family"], 2007),
    (83, "Swades", ["Drama"], 2004),
    (84, "Black", ["Drama"], 2005),
    (85, "Chak De India", ["Drama", "Sport"], 2007),
    (86, "Darlings", ["Thriller", "Drama"], 2022),
    (87, "Monica O My Darling", ["Mystery", "Crime"], 2022),
    (88, "Ponniyin Selvan", ["Epic", "Drama"], 2022),
    (89, "Salaar", ["Action", "Drama"], 2023),
    (90, "HanuMan", ["Action", "Fantasy"], 2024),
    (91, "Gadar 2", ["Action", "Drama"], 2023),
    (92, "Fukrey 3", ["Comedy"], 2023),
    (93, "Dream Girl 2", ["Comedy", "Drama"], 2023),
    (94, "Mission Majnu", ["Action", "Thriller"], 2023),
    (95, "Bholaa", ["Action", "Crime"], 2023),
    (96, "Selfiee", ["Comedy", "Action"], 2023),
    (97, "Adipurush", ["Epic", "Action"], 2023),
    (98, "Kisi Ka Bhai", ["Action", "Comedy"], 2023),
    (99, "BMCM", ["Action", "Comedy"], 2024),
    (100, "Mr & Mrs Mahi", ["Romance", "Sport"], 2024),
]

# Genre to color mapping (gradient colors)
GENRE_COLORS = {
    "Action": [(139, 0, 0), (220, 20, 60)],  # Dark red to crimson
    "Comedy": [(255, 140, 0), (255, 215, 0)],  # Orange to gold
    "Drama": [(75, 0, 130), (138, 43, 226)],  # Indigo to violet
    "Thriller": [(25, 25, 112), (70, 130, 180)],  # Midnight blue to steel blue
    "Horror": [(0, 0, 0), (75, 0, 75)],  # Black to dark purple
    "Romance": [(199, 21, 133), (255, 105, 180)],  # Deep pink to hot pink
    "Biography": [(101, 67, 33), (160, 82, 45)],  # Brown tones
    "Crime": [(47, 79, 79), (112, 128, 144)],  # Dark slate to slate gray
    "Sci-Fi": [(0, 139, 139), (0, 255, 255)],  # Teal to cyan
    "Fantasy": [(148, 0, 211), (186, 85, 211)],  # Violet to orchid
    "Mystery": [(0, 0, 128), (65, 105, 225)],  # Navy to royal blue
    "Sport": [(34, 139, 34), (50, 205, 50)],  # Forest green to lime
    "War": [(85, 85, 85), (139, 69, 19)],  # Gray to brown
    "Adventure": [(0, 100, 0), (46, 139, 87)],  # Dark green to sea green
    "Music": [(255, 20, 147), (255, 182, 193)],  # Deep pink to light pink
    "Family": [(70, 130, 180), (135, 206, 235)],  # Steel blue to sky blue
    "Spy": [(0, 0, 0), (64, 64, 64)],  # Black to dark gray
    "Epic": [(184, 134, 11), (218, 165, 32)],  # Dark golden to golden
}

def get_colors_for_genre(genres):
    """Get gradient colors based on primary genre"""
    primary_genre = genres[0] if genres else "Drama"
    return GENRE_COLORS.get(primary_genre, [(75, 0, 130), (138, 43, 226)])

def create_gradient(width, height, color1, color2):
    """Create a gradient image"""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        for x in range(width):
            pixels[x, y] = (r, g, b)
    
    return img

def wrap_text(text, max_chars=15):
    """Wrap text to fit in poster"""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line = (current_line + " " + word).strip()
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines

def create_poster(movie_id, title, genres, year):
    """Create a movie poster"""
    width, height = 300, 450
    
    # Get colors based on genre
    color1, color2 = get_colors_for_genre(genres)
    
    # Create gradient background
    img = create_gradient(width, height, color1, color2)
    draw = ImageDraw.Draw(img)
    
    # Add some visual elements
    # Film strip effect at top
    for i in range(0, width, 30):
        draw.rectangle([i, 0, i+20, 20], fill=(0, 0, 0))
        draw.rectangle([i+5, 5, i+15, 15], fill=(255, 255, 255, 100))
    
    # Film strip at bottom
    for i in range(0, width, 30):
        draw.rectangle([i, height-20, i+20, height], fill=(0, 0, 0))
        draw.rectangle([i+5, height-15, i+15, height-5], fill=(255, 255, 255, 100))
    
    # Try to use a nice font, fall back to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        year_font = ImageFont.truetype("arial.ttf", 24)
        genre_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        year_font = ImageFont.load_default()
        genre_font = ImageFont.load_default()
    
    # Draw title
    title_lines = wrap_text(title, 12)
    y_offset = height // 3
    
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        
        # Shadow effect
        draw.text((x+2, y_offset+2), line, fill=(0, 0, 0), font=title_font)
        draw.text((x, y_offset), line, fill=(255, 255, 255), font=title_font)
        y_offset += 40
    
    # Draw year
    year_text = str(year)
    bbox = draw.textbbox((0, 0), year_text, font=year_font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = height - 80
    
    # Year circle
    draw.ellipse([x-20, y-10, x+text_width+20, y+35], fill=(255, 255, 255))
    draw.text((x, y), year_text, fill=(0, 0, 0), font=year_font)
    
    # Draw genre tag
    genre_text = genres[0] if genres else "Movie"
    bbox = draw.textbbox((0, 0), genre_text, font=genre_font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    
    draw.rectangle([x-10, 50, x+text_width+10, 75], fill=(255, 255, 255))
    draw.text((x, 52), genre_text, fill=color1, font=genre_font)
    
    # Add decorative border
    draw.rectangle([5, 25, width-5, height-25], outline=(255, 255, 255), width=2)
    
    # Save
    filename = f"{POSTER_DIR}/{movie_id}.jpg"
    img.save(filename, quality=95)
    return True

def main():
    """Generate all movie posters"""
    os.makedirs(POSTER_DIR, exist_ok=True)
    
    print("="*50)
    print("Generating Bollywood Movie Posters")
    print("="*50)
    
    for movie_id, title, genres, year in MOVIES:
        try:
            create_poster(movie_id, title, genres, year)
            print(f"  [OK] Created poster {movie_id}: {title}")
        except Exception as e:
            print(f"  [FAIL] Poster {movie_id}: {e}")
    
    print("="*50)
    print(f"Generated {len(MOVIES)} posters!")
    print("="*50)

if __name__ == '__main__':
    main()
