# Quick Start Guide

Get up and running with the Movie Recommendation System in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Download Dataset

1. Visit [MovieLens Dataset](https://grouplens.org/datasets/movielens/)
2. Download the **small dataset** (recommended for testing)
3. Extract the ZIP file
4. Copy `movies.csv` and `ratings.csv` to the `data/` folder

**Alternative:** Create minimal test files (see `data/README.md`)

## Step 3: Verify Setup

```bash
python verify_setup.py
```

This will check:
- ✅ Python version
- ✅ Installed packages
- ✅ Project structure
- ✅ Data files

## Step 4: Run Your First Recommendation

### Content-Based (by movie title):
```bash
python main.py --method content --movie "Toy Story"
```

### Content-Based (by genres):
```bash
python main.py --method content --genres Action Adventure
```

### Collaborative Filtering:
```bash
python main.py --method collaborative --user-id 1
```

## Step 5: Explore Examples

```bash
python example_usage.py
```

This demonstrates:
- Content-based recommendations
- User-based collaborative filtering
- Item-based collaborative filtering
- Comparing different methods

## Common Issues

### "File not found" error
- Ensure `movies.csv` and `ratings.csv` are in the `data/` directory
- Check file names are exactly `movies.csv` and `ratings.csv` (case-sensitive)

### "Module not found" error
- Run `pip install -r requirements.txt`
- Ensure you're using Python 3.8+

### "User not found" error
- Try a different user ID (check available IDs in your dataset)
- For MovieLens small dataset, user IDs range from 1 to 610

## Next Steps

- Read `README.md` for detailed documentation
- Modify `main.py` to customize recommendations
- Experiment with different recommendation methods
- Try building a web interface using Streamlit or Flask

## Need Help?

- Check `data/README.md` for dataset information
- Review `README.md` for full documentation
- Run `python main.py --help` for command-line options

---

**Happy Recommending! 🎬**
