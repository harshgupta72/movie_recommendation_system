# 🎬 Bollywood Movie Recommendation System

A comprehensive movie recommendation system for **Bollywood movies** implementing both **Content-Based Filtering** and **Collaborative Filtering** techniques with **IMDb ratings** support.

## ✨ Features

### 🎯 Recommendation Techniques

1. **Content-Based Filtering**
   - Recommends movies based on genre similarity
   - Uses TF-IDF vectorization and cosine similarity
   - Supports filtering by IMDb rating, director, and year

2. **Collaborative Filtering**
   - **User-Based**: Finds users with similar preferences
   - **Item-Based**: Finds similar movies based on rating patterns
   - Predicts ratings for unrated movies

3. **IMDb Rating-Based Recommendations**
   - Get top-rated Bollywood movies
   - Filter by minimum IMDb rating
   - Combine with genre and year filters

4. **Director-Based Recommendations**
   - Find all movies by a specific director
   - Sorted by IMDb rating

### 📊 Dataset

Includes **100 popular Bollywood movies** from 1975-2024 with:
- IMDb ratings
- Genres
- Directors
- Release years
- 200 user ratings from 20 users

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Your First Recommendation

```bash
# Top movies by IMDb rating
python main.py --method imdb --min-imdb 8.0

# Movies similar to "Pathaan"
python main.py --method content --movie "Pathaan"

# Action Thriller movies
python main.py --method content --genres Action Thriller

# Movies by Rajkumar Hirani
python main.py --method director --director "Rajkumar Hirani"

# Collaborative filtering
python main.py --method collaborative --user-id 1
```

### 3. Run Example Script

```bash
python example_usage.py
```

## 📁 Project Structure

```
movie_recommender/
├── data/
│   ├── movies.csv          # 100 Bollywood movies with IMDb ratings
│   └── ratings.csv         # User ratings data
├── recommender/
│   ├── __init__.py
│   ├── data_loader.py      # Data loading with IMDb support
│   ├── content_based.py    # Content-based filtering
│   ├── collaborative.py    # Collaborative filtering
│   └── utils.py            # Utility functions
├── main.py                 # CLI interface
├── example_usage.py        # Usage examples
├── requirements.txt        # Dependencies
└── README.md
```

## 🎮 Usage Examples

### Top IMDb Rated Movies

```bash
# Get top 10 movies with IMDb >= 8.0
python main.py --method imdb --min-imdb 8.0 --n 10
```

**Output:**
```
🎬 Top Bollywood Movies by IMDb Rating
================================================================================
#    Title                                         IMDb   Genres                    Year  
---- --------------------------------------------- ------ ------------------------- ------
1    12th Fail                                     9.0    Biography|Drama           2023  
2    Rocketry The Nambi Effect                     8.8    Biography|Drama           2022  
3    Sardar Udham                                  8.6    Action|Biography|Drama    2021  
4    Laapataa Ladies                               8.5    Comedy|Drama              2024  
5    Shershaah                                     8.4    Action|Biography|Drama    2021  
...
```

### Content-Based Recommendations

```bash
# Find movies similar to "3 Idiots"
python main.py --method content --movie "3 Idiots" --min-imdb 7.0
```

### Genre-Based Recommendations

```bash
# Action Thriller movies with good ratings
python main.py --method content --genres Action Thriller --min-imdb 7.0

# Biography Drama movies
python main.py --method content --genres Biography Drama --min-imdb 8.0

# Comedy movies
python main.py --method content --genres Comedy --min-imdb 7.5
```

### Director-Based Recommendations

```bash
# All Rajkumar Hirani movies
python main.py --method director --director "Rajkumar Hirani"

# Sanjay Leela Bhansali movies
python main.py --method director --director "Sanjay Leela Bhansali"
```

### Collaborative Filtering

```bash
# User-based recommendations
python main.py --method collaborative --user-id 1 --cf-method user

# Item-based recommendations
python main.py --method collaborative --user-id 3 --cf-method item
```

### Recent Movies

```bash
# Top movies from 2023-2024
python main.py --method imdb --year-from 2023 --min-imdb 6.5
```

## 📋 Command-Line Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--method` | Recommendation method | `content`, `collaborative`, `imdb`, `director` |
| `--movie` | Movie title | `"Pathaan"`, `"3 Idiots"` |
| `--genres` | Genre filter | `Action Thriller`, `Comedy Drama` |
| `--director` | Director name | `"Rajkumar Hirani"` |
| `--min-imdb` | Minimum IMDb rating | `7.0`, `8.0` |
| `--year-from` | Minimum year | `2020`, `2023` |
| `--user-id` | User ID for CF | `1`, `5`, `10` |
| `--cf-method` | CF method | `user`, `item` |
| `--n` | Number of results | `5`, `10`, `20` |

## 🎥 Sample Movies in Dataset

| Movie | Year | IMDb | Genres |
|-------|------|------|--------|
| 12th Fail | 2023 | 9.0 | Biography, Drama |
| Rocketry | 2022 | 8.8 | Biography, Drama |
| Shershaah | 2021 | 8.4 | Action, Biography, Drama |
| 3 Idiots | 2009 | 8.4 | Comedy, Drama |
| Kantara | 2022 | 8.4 | Action, Adventure, Drama |
| Dangal | 2016 | 8.3 | Action, Biography, Drama |
| KGF Chapter 2 | 2022 | 8.3 | Action, Crime, Drama |
| Pathaan | 2023 | 5.9 | Action, Thriller, Spy |
| Jawan | 2023 | 6.1 | Action, Thriller, Drama |
| Animal | 2023 | 6.2 | Action, Crime, Drama |

## 🔧 How It Works

### Content-Based Filtering

1. **Feature Extraction**: Genres and directors are converted to TF-IDF vectors
2. **Similarity Matrix**: Cosine similarity computed between all movies
3. **Recommendations**: Movies with highest similarity scores are recommended
4. **IMDb Filter**: Only movies above the threshold are included

### Collaborative Filtering

1. **User-Movie Matrix**: Created from ratings data
2. **Similarity Computation**: 
   - User-based: Similar users identified
   - Item-based: Similar movies identified
3. **Prediction**: Ratings predicted using weighted averages
4. **Recommendations**: Top predicted movies returned

### IMDb Rating-Based

1. **Filtering**: Movies filtered by minimum rating
2. **Sorting**: Sorted by IMDb rating (descending)
3. **Additional Filters**: Genre and year filters applied
4. **Results**: Top N movies returned

## 📊 Evaluation & Limitations

### Strengths
- ✅ Covers latest Bollywood movies (up to 2024)
- ✅ Uses actual IMDb ratings
- ✅ Multiple recommendation approaches
- ✅ Director and genre-based filtering
- ✅ Easy to extend with more movies

### Limitations
- ⚠️ Cold start problem for new users/movies
- ⚠️ Limited to 100 movies in sample dataset
- ⚠️ Simulated user ratings (not real data)

### Future Improvements
- Add more movies to the dataset
- Include actor-based recommendations
- Add plot-based similarity using NLP
- Build web interface with Streamlit
- Implement matrix factorization (SVD)

## 🛠️ Dependencies

```
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
scipy>=1.9.0
```

## 📝 License

This project is provided for educational and portfolio purposes.

## 🙏 Acknowledgments

- IMDb for movie ratings
- Bollywood film industry for amazing content

---

**Made with ❤️ for Bollywood Movie Lovers! 🎬🍿**
