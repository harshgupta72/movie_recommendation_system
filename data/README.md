# Data Directory

Place your MovieLens dataset files here.

## Required Files

1. **movies.csv** - Movie metadata
   - Required columns: `movieId`, `title`, `genres`
   - Example:
     ```csv
     movieId,title,genres
     1,Toy Story (1995),Animation|Children's|Comedy
     2,Jumanji (1995),Adventure|Children's|Fantasy
     ```

2. **ratings.csv** - User ratings
   - Required columns: `userId`, `movieId`, `rating`
   - Optional: `timestamp`
   - Example:
     ```csv
     userId,movieId,rating,timestamp
     1,1,4.0,964982703
     1,2,3.5,964982703
     ```

## Download Dataset

Visit [MovieLens Dataset](https://grouplens.org/datasets/movielens/) and download:
- **Small dataset** (recommended for testing): ~1MB, 9,000 movies, 100,000 ratings
- **Full dataset** (for production): ~250MB, 27,000 movies, 20 million ratings

After downloading:
1. Extract the ZIP file
2. Copy `movies.csv` and `ratings.csv` to this directory
3. Ensure the column names match exactly (case-sensitive)

## Quick Start with Sample Data

If you want to test the system quickly, you can create minimal sample files:

**movies.csv** (minimal example):
```csv
movieId,title,genres
1,Toy Story,Animation|Children|Comedy
2,Jumanji,Adventure|Children|Fantasy
3,Grumpier Old Men,Comedy|Romance
4,Waiting to Exhale,Comedy|Drama|Romance
5,Father of the Bride Part II,Comedy
```

**ratings.csv** (minimal example):
```csv
userId,movieId,rating
1,1,4.0
1,2,3.5
1,3,5.0
2,1,4.5
2,2,4.0
2,4,3.0
3,1,5.0
3,3,4.0
3,5,3.5
```
