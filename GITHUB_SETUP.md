# How to Host on GitHub

It seems that **Git** is not currently installed or recognized on your computer. To host this project on GitHub, please follow these steps:

## Step 1: Install Git

1. Download Git from [git-scm.com](https://git-scm.com/downloads).
2. Install it (use the default settings).
3. **Restart your terminal/command prompt** (or VS Code) after installation.

## Step 2: Initialize Repository

Open your terminal in this project folder and run:

```bash
# Initialize git
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit of Bollywood Movie Recommender"
```

## Step 3: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new).
2. Repository name: `bollywood-movie-recommender` (or any name you like).
3. Description: "A Flask-based movie recommendation system".
4. Visibility: **Public**.
5. **Do not** check "Add a README file" or .gitignore (we already have them).
6. Click **Create repository**.

## Step 4: Push to GitHub

Copy the commands shown on GitHub under "…or push an existing repository from the command line" and run them. They will look like this:

```bash
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/bollywood-movie-recommender.git

git branch -M main

git push -u origin main
```

## Troubleshooting

- **"git is not recognized..."**: Make sure you installed Git and restarted your terminal.
- **Authentication failed**: You may need to sign in to GitHub in the browser window that pops up, or use a Personal Access Token if prompted for a password.
