"""
Bollywood Movie Recommendation System - Flask Web Application
A dynamic and attractive movie recommendation website
"""

from flask import Flask, render_template, jsonify, request
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

app = Flask(__name__)

# ============== MOVIE DATABASE ==============
# All posters are stored locally in static/posters/
MOVIES = [
    # 2024 Movies
    {"id": 1, "title": "Kalki 2898 AD", "year": 2024, "genres": ["Action", "Sci-Fi", "Adventure"], "imdb": 6.8, "director": "Nag Ashwin", "cast": ["Prabhas", "Deepika Padukone", "Amitabh Bachchan"], "poster": "/static/posters/1.jpg", "description": "A modern-day avatar of Vishnu, a half-man, half-machine, descends to Earth to protect the world from destruction."},
    {"id": 2, "title": "Stree 2", "year": 2024, "genres": ["Comedy", "Horror"], "imdb": 7.7, "director": "Amar Kaushik", "cast": ["Rajkummar Rao", "Shraddha Kapoor", "Pankaj Tripathi"], "poster": "/static/posters/2.jpg", "description": "The sequel to the 2018 hit horror comedy, where the town faces a new supernatural threat."},
    {"id": 3, "title": "Fighter", "year": 2024, "genres": ["Action", "Drama", "Thriller"], "imdb": 5.5, "director": "Siddharth Anand", "cast": ["Hrithik Roshan", "Deepika Padukone", "Anil Kapoor"], "poster": "/static/posters/3.jpg", "description": "A story of Indian Air Force pilots who risk their lives to protect the nation."},
    {"id": 4, "title": "Laapataa Ladies", "year": 2024, "genres": ["Comedy", "Drama"], "imdb": 8.5, "director": "Kiran Rao", "cast": ["Nitanshi Goel", "Pratibha Ranta", "Sparsh Shrivastava"], "poster": "/static/posters/4.jpg", "description": "Two brides get exchanged on a train, leading to a comedy of errors in rural India."},
    {"id": 5, "title": "Shaitaan", "year": 2024, "genres": ["Horror", "Thriller"], "imdb": 7.1, "director": "Vikas Bahl", "cast": ["Ajay Devgn", "R. Madhavan", "Jyotika"], "poster": "/static/posters/5.jpg", "description": "A family's vacation turns into a nightmare when a mysterious stranger takes control of their daughter."},
    {"id": 6, "title": "Crew", "year": 2024, "genres": ["Comedy", "Crime"], "imdb": 6.2, "director": "Rajesh Krishnan", "cast": ["Tabu", "Kareena Kapoor", "Kriti Sanon"], "poster": "/static/posters/6.jpg", "description": "Three air hostesses plan a heist to solve their financial problems."},
    {"id": 7, "title": "Article 370", "year": 2024, "genres": ["Drama", "Thriller", "Political"], "imdb": 7.7, "director": "Amar Kaushik", "cast": ["Yami Gautam", "Priya Mani"], "poster": "/static/posters/7.jpg", "description": "The story behind the abrogation of Article 370 in Jammu and Kashmir."},
    {"id": 8, "title": "Chandu Champion", "year": 2024, "genres": ["Biography", "Drama", "Sport"], "imdb": 8.2, "director": "Kabir Khan", "cast": ["Kartik Aaryan", "Vijay Raaz"], "poster": "/static/posters/8.jpg", "description": "Based on the true story of India's first Paralympic gold medalist."},
    {"id": 9, "title": "Srikanth", "year": 2024, "genres": ["Biography", "Drama"], "imdb": 8.3, "director": "Tushar Hiranandani", "cast": ["Rajkummar Rao", "Jyotika", "Alaya F"], "poster": "/static/posters/9.jpg", "description": "The inspiring story of Srikanth Bolla, a visually impaired industrialist."},
    {"id": 10, "title": "Maidaan", "year": 2024, "genres": ["Biography", "Drama", "Sport"], "imdb": 7.9, "director": "Amit Sharma", "cast": ["Ajay Devgn", "Priyamani"], "poster": "/static/posters/10.jpg", "description": "The story of Syed Abdul Rahim, the legendary football coach of India."},
    
    # 2023 Movies
    {"id": 11, "title": "Pathaan", "year": 2023, "genres": ["Action", "Thriller", "Spy"], "imdb": 5.9, "director": "Siddharth Anand", "cast": ["Shah Rukh Khan", "Deepika Padukone", "John Abraham"], "poster": "/static/posters/11.jpg", "description": "An Indian spy takes on the leader of a terrorist outfit."},
    {"id": 12, "title": "Jawan", "year": 2023, "genres": ["Action", "Thriller", "Drama"], "imdb": 6.1, "director": "Atlee", "cast": ["Shah Rukh Khan", "Nayanthara", "Vijay Sethupathi"], "poster": "/static/posters/12.jpg", "description": "A prison warden recruits inmates to commit crimes for social causes."},
    {"id": 13, "title": "Animal", "year": 2023, "genres": ["Action", "Crime", "Drama"], "imdb": 6.2, "director": "Sandeep Vanga", "cast": ["Ranbir Kapoor", "Anil Kapoor", "Bobby Deol"], "poster": "/static/posters/13.jpg", "description": "A son goes to extreme lengths to protect his family's legacy."},
    {"id": 14, "title": "12th Fail", "year": 2023, "genres": ["Biography", "Drama"], "imdb": 9.0, "director": "Vidhu Vinod Chopra", "cast": ["Vikrant Massey", "Medha Shankar"], "poster": "/static/posters/14.jpg", "description": "The inspiring story of IPS officer Manoj Kumar Sharma who overcame poverty to succeed."},
    {"id": 15, "title": "Dunki", "year": 2023, "genres": ["Comedy", "Drama"], "imdb": 6.0, "director": "Rajkumar Hirani", "cast": ["Shah Rukh Khan", "Taapsee Pannu", "Vicky Kaushal"], "poster": "/static/posters/15.jpg", "description": "A group of friends take the dangerous 'donkey flight' route to immigrate to a foreign country."},
    {"id": 16, "title": "Tiger 3", "year": 2023, "genres": ["Action", "Thriller", "Spy"], "imdb": 5.2, "director": "Maneesh Sharma", "cast": ["Salman Khan", "Katrina Kaif", "Emraan Hashmi"], "poster": "/static/posters/16.jpg", "description": "Tiger and Zoya battle a Pakistani terrorist organization."},
    {"id": 17, "title": "Sam Bahadur", "year": 2023, "genres": ["Biography", "Drama", "War"], "imdb": 7.7, "director": "Meghna Gulzar", "cast": ["Vicky Kaushal", "Sanya Malhotra", "Fatima Sana Shaikh"], "poster": "/static/posters/17.jpg", "description": "The life story of Sam Manekshaw, India's greatest military commander."},
    {"id": 18, "title": "Rocky Aur Rani Kii Prem Kahaani", "year": 2023, "genres": ["Comedy", "Drama", "Romance"], "imdb": 6.5, "director": "Karan Johar", "cast": ["Ranveer Singh", "Alia Bhatt", "Dharmendra"], "poster": "/static/posters/18.jpg", "description": "Two families from different backgrounds clash when their children fall in love."},
    {"id": 19, "title": "OMG 2", "year": 2023, "genres": ["Comedy", "Drama"], "imdb": 7.9, "director": "Amit Rai", "cast": ["Akshay Kumar", "Pankaj Tripathi", "Yami Gautam"], "poster": "/static/posters/19.jpg", "description": "A man fights the education system to include sex education in schools."},
    {"id": 20, "title": "The Kerala Story", "year": 2023, "genres": ["Drama", "Thriller"], "imdb": 7.1, "director": "Sudipto Sen", "cast": ["Adah Sharma", "Yogita Bihani"], "poster": "/static/posters/20.jpg", "description": "Based on true events about women being forced into terrorism."},
    
    # 2022 Movies
    {"id": 21, "title": "RRR", "year": 2022, "genres": ["Action", "Drama", "Epic"], "imdb": 7.8, "director": "S.S. Rajamouli", "cast": ["N.T. Rama Rao Jr.", "Ram Charan", "Alia Bhatt"], "poster": "/static/posters/21.jpg", "description": "Two legendary revolutionaries embark on a journey far away from home."},
    {"id": 22, "title": "KGF Chapter 2", "year": 2022, "genres": ["Action", "Crime", "Drama"], "imdb": 8.3, "director": "Prashanth Neel", "cast": ["Yash", "Sanjay Dutt", "Raveena Tandon"], "poster": "/static/posters/22.jpg", "description": "Rocky takes control of the Kolar Gold Fields while facing new enemies."},
    {"id": 23, "title": "Drishyam 2", "year": 2022, "genres": ["Crime", "Drama", "Mystery"], "imdb": 8.3, "director": "Abhishek Pathak", "cast": ["Ajay Devgn", "Tabu", "Shriya Saran"], "poster": "/static/posters/23.jpg", "description": "Vijay Salgaonkar's family faces new threats seven years after the incident."},
    {"id": 24, "title": "Brahmastra", "year": 2022, "genres": ["Action", "Adventure", "Fantasy"], "imdb": 5.6, "director": "Ayan Mukerji", "cast": ["Ranbir Kapoor", "Alia Bhatt", "Amitabh Bachchan"], "poster": "/static/posters/24.jpg", "description": "A young man discovers his connection to ancient weapons and supernatural powers."},
    {"id": 25, "title": "Gangubai Kathiawadi", "year": 2022, "genres": ["Biography", "Crime", "Drama"], "imdb": 7.0, "director": "Sanjay Leela Bhansali", "cast": ["Alia Bhatt", "Ajay Devgn", "Shantanu Maheshwari"], "poster": "/static/posters/25.jpg", "description": "The story of a young girl who became the madam of a brothel in Mumbai."},
    {"id": 26, "title": "Bhool Bhulaiyaa 2", "year": 2022, "genres": ["Comedy", "Horror"], "imdb": 5.7, "director": "Anees Bazmee", "cast": ["Kartik Aaryan", "Kiara Advani", "Tabu"], "poster": "/static/posters/26.jpg", "description": "A con man's lies about being a ghostbuster come back to haunt him."},
    {"id": 27, "title": "Kantara", "year": 2022, "genres": ["Action", "Adventure", "Drama"], "imdb": 8.4, "director": "Rishab Shetty", "cast": ["Rishab Shetty", "Sapthami Gowda"], "poster": "/static/posters/27.jpg", "description": "A village rebel clashes with a forest officer over sacred land."},
    {"id": 28, "title": "Vikram", "year": 2022, "genres": ["Action", "Crime", "Thriller"], "imdb": 8.3, "director": "Lokesh Kanagaraj", "cast": ["Kamal Haasan", "Vijay Sethupathi", "Fahadh Faasil"], "poster": "/static/posters/28.jpg", "description": "A special agent investigates a case that connects three notorious criminals."},
    {"id": 29, "title": "Rocketry", "year": 2022, "genres": ["Biography", "Drama"], "imdb": 8.8, "director": "R. Madhavan", "cast": ["R. Madhavan", "Simran", "Shah Rukh Khan"], "poster": "/static/posters/29.jpg", "description": "The life of Nambi Narayanan, a scientist wrongly accused of espionage."},
    {"id": 30, "title": "Jhund", "year": 2022, "genres": ["Drama", "Sport"], "imdb": 8.2, "director": "Nagraj Manjule", "cast": ["Amitabh Bachchan", "Akash Thosar"], "poster": "/static/posters/30.jpg", "description": "A professor transforms street kids into a football team."},
    
    # 2021 Movies
    {"id": 31, "title": "Shershaah", "year": 2021, "genres": ["Action", "Biography", "Drama"], "imdb": 8.4, "director": "Vishnuvardhan", "cast": ["Sidharth Malhotra", "Kiara Advani"], "poster": "/static/posters/31.jpg", "description": "The life of Captain Vikram Batra, a Kargil War hero."},
    {"id": 32, "title": "Sardar Udham", "year": 2021, "genres": ["Action", "Biography", "Drama"], "imdb": 8.6, "director": "Shoojit Sircar", "cast": ["Vicky Kaushal", "Amol Parashar"], "poster": "/static/posters/32.jpg", "description": "The story of Udham Singh who assassinated Michael O'Dwyer."},
    {"id": 33, "title": "Pushpa: The Rise", "year": 2021, "genres": ["Action", "Crime", "Drama"], "imdb": 7.6, "director": "Sukumar", "cast": ["Allu Arjun", "Rashmika Mandanna", "Fahadh Faasil"], "poster": "/static/posters/33.jpg", "description": "A laborer rises in the world of red sandalwood smuggling."},
    {"id": 34, "title": "Sooryavanshi", "year": 2021, "genres": ["Action", "Thriller"], "imdb": 5.6, "director": "Rohit Shetty", "cast": ["Akshay Kumar", "Katrina Kaif", "Ajay Devgn"], "poster": "/static/posters/34.jpg", "description": "ATS chief Veer Sooryavanshi battles against terrorism."},
    {"id": 35, "title": "83", "year": 2021, "genres": ["Biography", "Drama", "Sport"], "imdb": 8.1, "director": "Kabir Khan", "cast": ["Ranveer Singh", "Deepika Padukone"], "poster": "/static/posters/35.jpg", "description": "India's historic 1983 Cricket World Cup victory story."},
    {"id": 36, "title": "Mimi", "year": 2021, "genres": ["Comedy", "Drama"], "imdb": 7.7, "director": "Laxman Utekar", "cast": ["Kriti Sanon", "Pankaj Tripathi"], "poster": "/static/posters/36.jpg", "description": "A surrogate mother's life changes when the couple abandons the baby."},
    
    # Classic & Older Movies
    {"id": 37, "title": "3 Idiots", "year": 2009, "genres": ["Comedy", "Drama"], "imdb": 8.4, "director": "Rajkumar Hirani", "cast": ["Aamir Khan", "R. Madhavan", "Sharman Joshi"], "poster": "/static/posters/37.jpg", "description": "Two friends search for their long-lost college buddy."},
    {"id": 38, "title": "Dangal", "year": 2016, "genres": ["Action", "Biography", "Drama"], "imdb": 8.3, "director": "Nitesh Tiwari", "cast": ["Aamir Khan", "Fatima Sana Shaikh", "Sanya Malhotra"], "poster": "/static/posters/38.jpg", "description": "A former wrestler trains his daughters to become world champions."},
    {"id": 39, "title": "PK", "year": 2014, "genres": ["Comedy", "Drama", "Sci-Fi"], "imdb": 8.1, "director": "Rajkumar Hirani", "cast": ["Aamir Khan", "Anushka Sharma", "Sanjay Dutt"], "poster": "/static/posters/39.jpg", "description": "An alien stranded on Earth questions religious practices."},
    {"id": 40, "title": "Bajrangi Bhaijaan", "year": 2015, "genres": ["Action", "Comedy", "Drama"], "imdb": 8.0, "director": "Kabir Khan", "cast": ["Salman Khan", "Kareena Kapoor", "Nawazuddin Siddiqui"], "poster": "/static/posters/40.jpg", "description": "A man takes a mute Pakistani girl back to her homeland."},
    {"id": 41, "title": "Dilwale Dulhania Le Jayenge", "year": 1995, "genres": ["Comedy", "Drama", "Romance"], "imdb": 8.0, "director": "Aditya Chopra", "cast": ["Shah Rukh Khan", "Kajol", "Amrish Puri"], "poster": "/static/posters/41.jpg", "description": "Two NRI lovers try to win over their families."},
    {"id": 42, "title": "Sholay", "year": 1975, "genres": ["Action", "Adventure", "Comedy"], "imdb": 8.1, "director": "Ramesh Sippy", "cast": ["Amitabh Bachchan", "Dharmendra", "Hema Malini"], "poster": "/static/posters/42.jpg", "description": "Two criminals are hired to capture a ruthless dacoit."},
    {"id": 43, "title": "Lagaan", "year": 2001, "genres": ["Drama", "Musical", "Sport"], "imdb": 8.1, "director": "Ashutosh Gowariker", "cast": ["Aamir Khan", "Gracy Singh", "Rachel Shelley"], "poster": "/static/posters/43.jpg", "description": "Villagers play a cricket match against British rulers to avoid taxes."},
    {"id": 44, "title": "Zindagi Na Milegi Dobara", "year": 2011, "genres": ["Adventure", "Comedy", "Drama"], "imdb": 8.1, "director": "Zoya Akhtar", "cast": ["Hrithik Roshan", "Farhan Akhtar", "Abhay Deol"], "poster": "/static/posters/44.jpg", "description": "Three friends go on a bachelor trip to Spain."},
    {"id": 45, "title": "Barfi!", "year": 2012, "genres": ["Comedy", "Drama", "Romance"], "imdb": 8.1, "director": "Anurag Basu", "cast": ["Ranbir Kapoor", "Priyanka Chopra", "Ileana D'Cruz"], "poster": "/static/posters/45.jpg", "description": "A deaf-mute man's adventures with two women."},
    {"id": 46, "title": "Queen", "year": 2013, "genres": ["Comedy", "Drama"], "imdb": 8.1, "director": "Vikas Bahl", "cast": ["Kangana Ranaut", "Rajkummar Rao", "Lisa Haydon"], "poster": "/static/posters/46.jpg", "description": "A jilted bride goes on her honeymoon alone and discovers herself."},
    {"id": 47, "title": "Andhadhun", "year": 2018, "genres": ["Crime", "Mystery", "Thriller"], "imdb": 8.2, "director": "Sriram Raghavan", "cast": ["Ayushmann Khurrana", "Tabu", "Radhika Apte"], "poster": "/static/posters/47.jpg", "description": "A blind pianist becomes entangled in the murder of his neighbor."},
    {"id": 48, "title": "Tumbbad", "year": 2018, "genres": ["Drama", "Fantasy", "Horror"], "imdb": 8.2, "director": "Rahi Anil Barve", "cast": ["Sohum Shah", "Jyoti Malshe"], "poster": "/static/posters/48.jpg", "description": "A man's obsession with treasure leads him to a cursed village."},
    {"id": 49, "title": "Stree", "year": 2018, "genres": ["Comedy", "Horror"], "imdb": 7.5, "director": "Amar Kaushik", "cast": ["Rajkummar Rao", "Shraddha Kapoor", "Pankaj Tripathi"], "poster": "/static/posters/49.jpg", "description": "A town is terrorized by a ghost who abducts men."},
    {"id": 50, "title": "Gully Boy", "year": 2019, "genres": ["Drama", "Music"], "imdb": 7.9, "director": "Zoya Akhtar", "cast": ["Ranveer Singh", "Alia Bhatt", "Siddhant Chaturvedi"], "poster": "/static/posters/50.jpg", "description": "A street rapper from Mumbai slums rises to fame."},
    
    # More Action Movies
    {"id": 51, "title": "Uri: The Surgical Strike", "year": 2019, "genres": ["Action", "Drama", "War"], "imdb": 8.3, "director": "Aditya Dhar", "cast": ["Vicky Kaushal", "Yami Gautam", "Paresh Rawal"], "poster": "/static/posters/51.jpg", "description": "The story of the Indian Army's surgical strike against militant camps."},
    {"id": 52, "title": "War", "year": 2019, "genres": ["Action", "Thriller"], "imdb": 6.0, "director": "Siddharth Anand", "cast": ["Hrithik Roshan", "Tiger Shroff", "Vaani Kapoor"], "poster": "/static/posters/52.jpg", "description": "A soldier is assigned to eliminate his mentor gone rogue."},
    {"id": 53, "title": "Tanhaji", "year": 2020, "genres": ["Action", "Biography", "Drama"], "imdb": 7.4, "director": "Om Raut", "cast": ["Ajay Devgn", "Saif Ali Khan", "Kajol"], "poster": "/static/posters/53.jpg", "description": "The story of Tanhaji Malusare's attempt to recapture a strategic fort."},
    {"id": 54, "title": "Singham", "year": 2011, "genres": ["Action", "Drama"], "imdb": 6.9, "director": "Rohit Shetty", "cast": ["Ajay Devgn", "Kajal Aggarwal", "Prakash Raj"], "poster": "/static/posters/54.jpg", "description": "A police officer takes on a powerful politician."},
    {"id": 55, "title": "Dhoom 3", "year": 2013, "genres": ["Action", "Crime", "Thriller"], "imdb": 5.5, "director": "Vijay Krishna Acharya", "cast": ["Aamir Khan", "Abhishek Bachchan", "Katrina Kaif"], "poster": "/static/posters/55.jpg", "description": "Jai and Ali chase a master thief in Chicago."},
    
    # More Drama Movies
    {"id": 56, "title": "Chhichhore", "year": 2019, "genres": ["Comedy", "Drama"], "imdb": 8.2, "director": "Nitesh Tiwari", "cast": ["Sushant Singh Rajput", "Shraddha Kapoor", "Varun Sharma"], "poster": "/static/posters/56.jpg", "description": "Friends reunite to help a student who failed his entrance exam."},
    {"id": 57, "title": "Kabir Singh", "year": 2019, "genres": ["Drama", "Romance"], "imdb": 7.1, "director": "Sandeep Vanga", "cast": ["Shahid Kapoor", "Kiara Advani"], "poster": "/static/posters/57.jpg", "description": "A surgeon spirals into self-destruction after a breakup."},
    {"id": 58, "title": "Raazi", "year": 2018, "genres": ["Action", "Drama", "Thriller"], "imdb": 7.8, "director": "Meghna Gulzar", "cast": ["Alia Bhatt", "Vicky Kaushal"], "poster": "/static/posters/58.jpg", "description": "A Kashmiri woman becomes a spy after marrying into a Pakistani family."},
    {"id": 59, "title": "Article 15", "year": 2019, "genres": ["Crime", "Drama"], "imdb": 8.1, "director": "Anubhav Sinha", "cast": ["Ayushmann Khurrana", "Nassar", "Manoj Pahwa"], "poster": "/static/posters/59.jpg", "description": "A police officer investigates the rape and murder of two Dalit girls."},
    {"id": 60, "title": "Badhaai Ho", "year": 2018, "genres": ["Comedy", "Drama"], "imdb": 7.8, "director": "Amit Sharma", "cast": ["Ayushmann Khurrana", "Sanya Malhotra", "Neena Gupta"], "poster": "/static/posters/60.jpg", "description": "A man is embarrassed when his middle-aged mother gets pregnant."},
    
    # More Thriller Movies
    {"id": 61, "title": "Kahaani", "year": 2012, "genres": ["Mystery", "Thriller"], "imdb": 8.1, "director": "Sujoy Ghosh", "cast": ["Vidya Balan", "Parambrata Chatterjee", "Nawazuddin Siddiqui"], "poster": "/static/posters/61.jpg", "description": "A pregnant woman searches for her missing husband in Kolkata."},
    {"id": 62, "title": "A Wednesday", "year": 2008, "genres": ["Crime", "Drama", "Mystery"], "imdb": 8.1, "director": "Neeraj Pandey", "cast": ["Naseeruddin Shah", "Anupam Kher", "Jimmy Shergill"], "poster": "/static/posters/62.jpg", "description": "A common man threatens to blow up Mumbai unless his demands are met."},
    {"id": 63, "title": "Special 26", "year": 2013, "genres": ["Crime", "Drama", "Thriller"], "imdb": 8.0, "director": "Neeraj Pandey", "cast": ["Akshay Kumar", "Manoj Bajpayee", "Anupam Kher"], "poster": "/static/posters/63.jpg", "description": "A group of con artists pose as CBI officers to commit heists."},
    {"id": 64, "title": "Gangs of Wasseypur", "year": 2012, "genres": ["Action", "Crime", "Drama"], "imdb": 8.2, "director": "Anurag Kashyap", "cast": ["Manoj Bajpayee", "Nawazuddin Siddiqui", "Richa Chadha"], "poster": "/static/posters/64.jpg", "description": "A coal mafia family's multi-generational saga of revenge."},
    {"id": 65, "title": "Badla", "year": 2019, "genres": ["Crime", "Drama", "Mystery"], "imdb": 7.8, "director": "Sujoy Ghosh", "cast": ["Amitabh Bachchan", "Taapsee Pannu", "Amrita Singh"], "poster": "/static/posters/65.jpg", "description": "A lawyer defends a businesswoman accused of murder."},
    
    # More Romance Movies
    {"id": 66, "title": "Kabhi Khushi Kabhie Gham", "year": 2001, "genres": ["Drama", "Musical", "Romance"], "imdb": 7.4, "director": "Karan Johar", "cast": ["Shah Rukh Khan", "Kajol", "Amitabh Bachchan"], "poster": "/static/posters/66.jpg", "description": "A family drama about tradition, love, and reconciliation."},
    {"id": 67, "title": "Kuch Kuch Hota Hai", "year": 1998, "genres": ["Comedy", "Drama", "Romance"], "imdb": 7.5, "director": "Karan Johar", "cast": ["Shah Rukh Khan", "Kajol", "Rani Mukerji"], "poster": "/static/posters/67.jpg", "description": "A widower's daughter tries to reunite him with his college love."},
    {"id": 68, "title": "Jab We Met", "year": 2007, "genres": ["Comedy", "Drama", "Romance"], "imdb": 7.9, "director": "Imtiaz Ali", "cast": ["Shahid Kapoor", "Kareena Kapoor"], "poster": "/static/posters/68.jpg", "description": "A depressed businessman meets a bubbly girl on a train."},
    {"id": 69, "title": "Yeh Jawaani Hai Deewani", "year": 2013, "genres": ["Comedy", "Drama", "Romance"], "imdb": 7.1, "director": "Ayan Mukerji", "cast": ["Ranbir Kapoor", "Deepika Padukone", "Aditya Roy Kapur"], "poster": "/static/posters/69.jpg", "description": "A free-spirited traveler reunites with a childhood friend."},
    {"id": 70, "title": "Dil Chahta Hai", "year": 2001, "genres": ["Comedy", "Drama", "Romance"], "imdb": 8.1, "director": "Farhan Akhtar", "cast": ["Aamir Khan", "Saif Ali Khan", "Akshaye Khanna"], "poster": "/static/posters/70.jpg", "description": "Three friends navigate life and love after college."},
    
    # More Biography Movies
    {"id": 71, "title": "Sanju", "year": 2018, "genres": ["Biography", "Drama"], "imdb": 7.5, "director": "Rajkumar Hirani", "cast": ["Ranbir Kapoor", "Paresh Rawal", "Vicky Kaushal"], "poster": "/static/posters/71.jpg", "description": "The turbulent life of actor Sanjay Dutt."},
    {"id": 72, "title": "Bhaag Milkha Bhaag", "year": 2013, "genres": ["Biography", "Drama", "Sport"], "imdb": 8.1, "director": "Rakeysh Mehra", "cast": ["Farhan Akhtar", "Sonam Kapoor", "Pavan Malhotra"], "poster": "/static/posters/72.jpg", "description": "The story of legendary Indian athlete Milkha Singh."},
    {"id": 73, "title": "Super 30", "year": 2019, "genres": ["Biography", "Drama"], "imdb": 7.9, "director": "Vikas Bahl", "cast": ["Hrithik Roshan", "Mrunal Thakur", "Pankaj Tripathi"], "poster": "/static/posters/73.jpg", "description": "A mathematician teaches underprivileged students for IIT."},
    {"id": 74, "title": "Mary Kom", "year": 2014, "genres": ["Biography", "Drama", "Sport"], "imdb": 6.8, "director": "Omung Kumar", "cast": ["Priyanka Chopra", "Darshan Kumar"], "poster": "/static/posters/74.jpg", "description": "The life of boxing champion Mary Kom."},
    {"id": 75, "title": "Pad Man", "year": 2018, "genres": ["Biography", "Comedy", "Drama"], "imdb": 7.9, "director": "R. Balki", "cast": ["Akshay Kumar", "Sonam Kapoor", "Radhika Apte"], "poster": "/static/posters/75.jpg", "description": "A man creates affordable sanitary pads for rural women."},
    
    # More Comedy Movies
    {"id": 76, "title": "Hera Pheri", "year": 2000, "genres": ["Comedy", "Crime"], "imdb": 8.1, "director": "Priyadarshan", "cast": ["Akshay Kumar", "Paresh Rawal", "Suniel Shetty"], "poster": "/static/posters/76.jpg", "description": "Three unemployed men get involved in a kidnapping scheme."},
    {"id": 77, "title": "Munna Bhai M.B.B.S.", "year": 2003, "genres": ["Comedy", "Drama"], "imdb": 8.1, "director": "Rajkumar Hirani", "cast": ["Sanjay Dutt", "Arshad Warsi", "Gracy Singh"], "poster": "/static/posters/77.jpg", "description": "A gangster enrolls in medical college to please his father."},
    {"id": 78, "title": "Lage Raho Munna Bhai", "year": 2006, "genres": ["Comedy", "Drama", "Romance"], "imdb": 8.1, "director": "Rajkumar Hirani", "cast": ["Sanjay Dutt", "Arshad Warsi", "Vidya Balan"], "poster": "/static/posters/78.jpg", "description": "Munna Bhai starts seeing Mahatma Gandhi's ghost."},
    {"id": 79, "title": "Golmaal", "year": 2006, "genres": ["Comedy"], "imdb": 7.1, "director": "Rohit Shetty", "cast": ["Ajay Devgn", "Arshad Warsi", "Tushar Kapoor"], "poster": "/static/posters/79.jpg", "description": "Four runaway crooks take shelter with a blind couple."},
    {"id": 80, "title": "Bhool Bhulaiyaa", "year": 2007, "genres": ["Comedy", "Horror", "Mystery"], "imdb": 7.4, "director": "Priyadarshan", "cast": ["Akshay Kumar", "Vidya Balan", "Shiney Ahuja"], "poster": "/static/posters/80.jpg", "description": "A psychiatrist investigates supernatural events in a haveli."},
    
    # More Movies
    {"id": 81, "title": "Rang De Basanti", "year": 2006, "genres": ["Drama"], "imdb": 8.1, "director": "Rakeysh Mehra", "cast": ["Aamir Khan", "Siddharth", "Sharman Joshi"], "poster": "/static/posters/81.jpg", "description": "College students get inspired by freedom fighters."},
    {"id": 82, "title": "Taare Zameen Par", "year": 2007, "genres": ["Drama", "Family"], "imdb": 8.3, "director": "Aamir Khan", "cast": ["Darsheel Safary", "Aamir Khan", "Tisca Chopra"], "poster": "/static/posters/82.jpg", "description": "A teacher helps a dyslexic student discover his talent."},
    {"id": 83, "title": "Swades", "year": 2004, "genres": ["Drama"], "imdb": 8.2, "director": "Ashutosh Gowariker", "cast": ["Shah Rukh Khan", "Gayatri Joshi"], "poster": "/static/posters/83.jpg", "description": "An NRI returns to India and decides to transform a village."},
    {"id": 84, "title": "Black", "year": 2005, "genres": ["Drama"], "imdb": 8.2, "director": "Sanjay Leela Bhansali", "cast": ["Amitabh Bachchan", "Rani Mukerji"], "poster": "/static/posters/84.jpg", "description": "A teacher helps a deaf-blind girl communicate."},
    {"id": 85, "title": "Chak De! India", "year": 2007, "genres": ["Drama", "Sport"], "imdb": 8.2, "director": "Shimit Amin", "cast": ["Shah Rukh Khan", "Vidya Malvade", "Shilpa Shukla"], "poster": "/static/posters/85.jpg", "description": "A disgraced hockey player coaches the women's team."},
    
    # More Recent Movies
    {"id": 86, "title": "Darlings", "year": 2022, "genres": ["Comedy", "Drama", "Thriller"], "imdb": 6.8, "director": "Jasmeet Reen", "cast": ["Alia Bhatt", "Shefali Shah", "Vijay Varma"], "poster": "/static/posters/86.jpg", "description": "A woman and her mother plot against her abusive husband."},
    {"id": 87, "title": "Monica, O My Darling", "year": 2022, "genres": ["Comedy", "Crime", "Mystery"], "imdb": 7.1, "director": "Vasan Bala", "cast": ["Rajkummar Rao", "Huma Qureshi", "Radhika Apte"], "poster": "/static/posters/87.jpg", "description": "A robotics expert gets involved in a murder plot."},
    {"id": 88, "title": "Ponniyin Selvan", "year": 2022, "genres": ["Action", "Drama", "History"], "imdb": 7.6, "director": "Mani Ratnam", "cast": ["Vikram", "Aishwarya Rai", "Jayam Ravi"], "poster": "/static/posters/88.jpg", "description": "The story of the Chola dynasty's succession."},
    {"id": 89, "title": "Salaar", "year": 2023, "genres": ["Action", "Drama", "Thriller"], "imdb": 6.4, "director": "Prashanth Neel", "cast": ["Prabhas", "Prithviraj Sukumaran", "Shruti Haasan"], "poster": "/static/posters/89.jpg", "description": "A gang leader's violent past catches up with him."},
    {"id": 90, "title": "HanuMan", "year": 2024, "genres": ["Action", "Adventure", "Fantasy"], "imdb": 8.0, "director": "Prasanth Varma", "cast": ["Teja Sajja", "Amritha Aiyer", "Varalaxmi Sarathkumar"], "poster": "/static/posters/90.jpg", "description": "A young man gains superpowers from Lord Hanuman."},
    
    # Fill remaining
    {"id": 91, "title": "Gadar 2", "year": 2023, "genres": ["Action", "Drama", "Romance"], "imdb": 5.5, "director": "Anil Sharma", "cast": ["Sunny Deol", "Ameesha Patel", "Utkarsh Sharma"], "poster": "/static/posters/91.jpg", "description": "Tara Singh returns to Pakistan to rescue his son."},
    {"id": 92, "title": "Fukrey 3", "year": 2023, "genres": ["Comedy"], "imdb": 5.8, "director": "Mrigdeep Lamba", "cast": ["Pulkit Samrat", "Varun Sharma", "Richa Chadha"], "poster": "/static/posters/92.jpg", "description": "The jugaadu boys return with another adventure."},
    {"id": 93, "title": "Dream Girl 2", "year": 2023, "genres": ["Comedy", "Drama"], "imdb": 5.3, "director": "Raaj Shaandilyaa", "cast": ["Ayushmann Khurrana", "Ananya Panday"], "poster": "/static/posters/93.jpg", "description": "Pooja returns with her voice acting skills."},
    {"id": 94, "title": "Mission Majnu", "year": 2023, "genres": ["Action", "Drama", "Thriller"], "imdb": 6.4, "director": "Shantanu Bagchi", "cast": ["Sidharth Malhotra", "Rashmika Mandanna"], "poster": "/static/posters/94.jpg", "description": "RAW's most ambitious covert operation on Pakistani soil."},
    {"id": 95, "title": "Bholaa", "year": 2023, "genres": ["Action", "Crime", "Drama"], "imdb": 6.0, "director": "Ajay Devgn", "cast": ["Ajay Devgn", "Tabu", "Deepak Dobriyal"], "poster": "/static/posters/95.jpg", "description": "A mysterious prisoner fights to reunite with his daughter."},
    {"id": 96, "title": "Selfiee", "year": 2023, "genres": ["Action", "Comedy"], "imdb": 4.6, "director": "Raj Mehta", "cast": ["Akshay Kumar", "Emraan Hashmi", "Nushrratt Bharuccha"], "poster": "/static/posters/96.jpg", "description": "A superstar's life is disrupted by a driving instructor."},
    {"id": 97, "title": "Adipurush", "year": 2023, "genres": ["Action", "Adventure", "Drama"], "imdb": 2.7, "director": "Om Raut", "cast": ["Prabhas", "Kriti Sanon", "Saif Ali Khan"], "poster": "/static/posters/97.jpg", "description": "A visual adaptation of the epic Ramayana."},
    {"id": 98, "title": "Kisi Ka Bhai Kisi Ki Jaan", "year": 2023, "genres": ["Action", "Comedy", "Drama"], "imdb": 3.7, "director": "Farhad Samji", "cast": ["Salman Khan", "Pooja Hegde", "Venkatesh"], "poster": "/static/posters/98.jpg", "description": "An elder brother who is overprotective of his siblings."},
    {"id": 99, "title": "Bade Miyan Chote Miyan", "year": 2024, "genres": ["Action", "Comedy", "Thriller"], "imdb": 4.2, "director": "Ali Abbas Zafar", "cast": ["Akshay Kumar", "Tiger Shroff", "Prithviraj Sukumaran"], "poster": "/static/posters/99.jpg", "description": "Two rival soldiers team up for a mission."},
    {"id": 100, "title": "Mr. & Mrs. Mahi", "year": 2024, "genres": ["Drama", "Romance", "Sport"], "imdb": 6.6, "director": "Sharan Sharma", "cast": ["Rajkummar Rao", "Janhvi Kapoor"], "poster": "/static/posters/100.jpg", "description": "A couple's journey in cricket where dreams collide."},
]

# Genre colors for UI
GENRE_COLORS = {
    "Action": "#e74c3c",
    "Comedy": "#f39c12",
    "Drama": "#9b59b6",
    "Thriller": "#2c3e50",
    "Horror": "#1a1a2e",
    "Romance": "#e91e63",
    "Sci-Fi": "#00bcd4",
    "Biography": "#795548",
    "Crime": "#607d8b",
    "Adventure": "#4caf50",
    "Fantasy": "#673ab7",
    "Mystery": "#3f51b5",
    "Sport": "#ff5722",
    "War": "#8b0000",
    "Musical": "#ff69b4",
    "Family": "#8bc34a",
    "History": "#d4a574",
    "Political": "#455a64",
    "Spy": "#263238",
    "Epic": "#b8860b"
}

# Get all unique genres
def get_all_genres():
    genres = set()
    for movie in MOVIES:
        genres.update(movie["genres"])
    return sorted(list(genres))

# Build recommendation engine
class RecommendationEngine:
    def __init__(self):
        self.movies = MOVIES
        self.build_content_model()
    
    def build_content_model(self):
        """Build TF-IDF model for content-based filtering"""
        features = []
        for movie in self.movies:
            feature = ' '.join(movie['genres']) + ' ' + movie['director'] + ' ' + ' '.join(movie['cast'])
            features.append(feature.lower())
        
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(features)
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
    
    def get_similar_movies(self, movie_id, n=10):
        """Get similar movies using content-based filtering"""
        idx = next((i for i, m in enumerate(self.movies) if m['id'] == movie_id), None)
        if idx is None:
            return []
        
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]
        
        return [{"movie": self.movies[i], "score": round(score * 100, 1)} for i, score in sim_scores]
    
    def get_movies_by_genre(self, genre, n=20):
        """Get movies by genre sorted by IMDb rating"""
        filtered = [m for m in self.movies if genre in m['genres']]
        return sorted(filtered, key=lambda x: x['imdb'], reverse=True)[:n]
    
    def get_top_rated(self, n=20):
        """Get top rated movies"""
        return sorted(self.movies, key=lambda x: x['imdb'], reverse=True)[:n]
    
    def get_latest(self, n=20):
        """Get latest movies"""
        return sorted(self.movies, key=lambda x: x['year'], reverse=True)[:n]
    
    def search_movies(self, query):
        """Search movies by title, cast, or director"""
        query = query.lower()
        results = []
        for movie in self.movies:
            if query in movie['title'].lower():
                results.append(movie)
            elif any(query in cast.lower() for cast in movie['cast']):
                results.append(movie)
            elif query in movie['director'].lower():
                results.append(movie)
        return results
    
    def get_random_recommendations(self, n=10):
        """Get random movie recommendations"""
        return random.sample(self.movies, min(n, len(self.movies)))

# Initialize recommendation engine
engine = RecommendationEngine()

# ============== ROUTES ==============

@app.route('/')
def home():
    """Home page with featured movies"""
    return render_template('index.html', 
                         genres=get_all_genres(),
                         genre_colors=GENRE_COLORS)

@app.route('/api/movies')
def get_movies():
    """Get all movies or filtered by category"""
    category = request.args.get('category', 'all')
    genre = request.args.get('genre', None)
    limit = int(request.args.get('limit', 20))
    
    if category == 'top_rated':
        movies = engine.get_top_rated(limit)
    elif category == 'latest':
        movies = engine.get_latest(limit)
    elif category == 'random':
        movies = engine.get_random_recommendations(limit)
    elif genre:
        movies = engine.get_movies_by_genre(genre, limit)
    else:
        movies = MOVIES[:limit]
    
    return jsonify(movies)

@app.route('/api/movie/<int:movie_id>')
def get_movie(movie_id):
    """Get single movie details"""
    movie = next((m for m in MOVIES if m['id'] == movie_id), None)
    if movie:
        return jsonify(movie)
    return jsonify({"error": "Movie not found"}), 404

@app.route('/api/recommendations/<int:movie_id>')
def get_recommendations(movie_id):
    """Get recommendations for a movie"""
    limit = int(request.args.get('limit', 10))
    recommendations = engine.get_similar_movies(movie_id, limit)
    return jsonify(recommendations)

@app.route('/api/search')
def search():
    """Search movies"""
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    results = engine.search_movies(query)
    return jsonify(results)

@app.route('/api/genres')
def get_genres():
    """Get all genres with colors"""
    genres = get_all_genres()
    return jsonify([{"name": g, "color": GENRE_COLORS.get(g, "#666")} for g in genres])

@app.route('/api/stats')
def get_stats():
    """Get database statistics"""
    genres = get_all_genres()
    years = sorted(set(m['year'] for m in MOVIES), reverse=True)
    avg_rating = sum(m['imdb'] for m in MOVIES) / len(MOVIES)
    
    return jsonify({
        "total_movies": len(MOVIES),
        "genres": len(genres),
        "years": years,
        "avg_rating": round(avg_rating, 1),
        "latest_year": max(years),
        "oldest_year": min(years)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
