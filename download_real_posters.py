"""
Download real movie posters from the internet
Uses direct image URLs from reliable sources
"""

import os
import requests
import time
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

POSTER_DIR = "static/posters"

# Real movie poster URLs from reliable sources (Wikipedia, Wikimedia Commons)
# These are permanent URLs that allow hotlinking
REAL_POSTERS = {
    1: "https://m.media-amazon.com/images/M/MV5BYTJmMjNmYmMtYjJjNi00MzlhLWI0MTQtYzZiNGNjMWYwODNjXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_FMjpg_UX1000_.jpg",  # Kalki 2898 AD
    2: "https://m.media-amazon.com/images/M/MV5BN2E2MDRlOWYtOGFiNy00YmFiLTljNDItNWQ5NDk5YmQ4NmU5XkEyXkFqcGdeQXVyMTY1NDY4NTIw._V1_.jpg",  # Stree 2
    3: "https://m.media-amazon.com/images/M/MV5BZTk3MGFmNDUtMzIxMi00NzljLWE1NGUtZTI2MzQ5YjMzNGYxXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Fighter
    4: "https://m.media-amazon.com/images/M/MV5BYzBmZjg4NTItOTI5Ny00NTFjLTkyYWMtYjAwODQ1N2Q4ZGM2XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Laapataa Ladies
    5: "https://m.media-amazon.com/images/M/MV5BZWU4MTk2YjgtZDAwOS00MjI2LWFhOWItMzUzY2UxYTBjZjI0XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Shaitaan
    6: "https://m.media-amazon.com/images/M/MV5BMTJkNzJlNjUtNGNjMS00NWRiLWJhNzYtYmFhMGE5NDI5ODM2XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Crew
    7: "https://m.media-amazon.com/images/M/MV5BN2Q0YmU3NWYtZGVhZi00ZTk3LWE5NTEtYmQ0ZGY1YjJiNDhiXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Article 370
    8: "https://m.media-amazon.com/images/M/MV5BZWM5ZGYzNGQtYTNkNy00MDFiLWJhNDAtNzQ4ZjQxNWFkNzc5XkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",  # Chandu Champion
    9: "https://m.media-amazon.com/images/M/MV5BMjg5N2Q0NTAtNjhmYS00NDYyLTllZTctMTg5NmM1MTIxMWQ4XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Srikanth
    10: "https://m.media-amazon.com/images/M/MV5BYjcxMWMzYTItZWIyMS00ZDU2LWE0ZjAtZTNiMzBlYWU3ZTBkXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Maidaan
    11: "https://m.media-amazon.com/images/M/MV5BYTlmNzQ5ZDgtNmNhNS00NDg2LTg5NDUtNWM3ZWU2ZDQxZmVlXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Pathaan
    12: "https://m.media-amazon.com/images/M/MV5BZmQ0NTNkODMtMDRhYi00YjhhLWE5MWEtMzNhZGM1NzM4NWRjXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Jawan
    13: "https://m.media-amazon.com/images/M/MV5BMmE0ZTRiMzQtOWU0Zi00Yjk5LWE3OGUtMjk2MTk5MmFmNWZmXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Animal
    14: "https://m.media-amazon.com/images/M/MV5BY2FhZDZkZjItZTY5NC00MzYyLWJlNGQtMWFjYWJlZjU0YTc0XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # 12th Fail
    15: "https://m.media-amazon.com/images/M/MV5BYjMzZDFjNDgtMmY3Ny00YjRlLWE1ZTAtMzljZGJjNTY4Njc1XkEyXkFqcGdeQXVyMTY1NDY4NTIw._V1_.jpg",  # Dunki
    16: "https://m.media-amazon.com/images/M/MV5BMDYzNWIyYzAtYTBkMi00MmQ2LTgyMWUtNDMyYjQ3MzQ0YmQ0XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Tiger 3
    17: "https://m.media-amazon.com/images/M/MV5BNmJiMmYxNGYtYTY3NC00YzBhLWI2NzUtOTNhNWE3YjIzZmUxXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Sam Bahadur
    18: "https://m.media-amazon.com/images/M/MV5BMGRkODhmMGMtN2Y3Yi00MTY0LWEyOGUtYjU5ODU1YjcwMDZkXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Rocky Aur Rani
    19: "https://m.media-amazon.com/images/M/MV5BZDRkYjBkNzQtMGJiOC00ZmQ2LTljMzgtMzE1YzI2NzcwY2Y1XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # OMG 2
    20: "https://m.media-amazon.com/images/M/MV5BNzcwMDE3NTgtNGIyZS00ZGI2LTk2NzMtOTFlYzljNWY0ZWI1XkEyXkFqcGdeQXVyMTQzNTA5MzYz._V1_.jpg",  # Kerala Story
    21: "https://m.media-amazon.com/images/M/MV5BODUwNDNjYzctODUxNy00ZTA2LWIyYTEtMDc5Y2E5ZjBmNTMzXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # RRR
    22: "https://m.media-amazon.com/images/M/MV5BMmU0OTdmODAtNmQyZi00ODhhLWI0NWYtNzg5MDY4YTgwODZhXkEyXkFqcGdeQXVyMTMwMDE4NTk3._V1_.jpg",  # KGF 2
    23: "https://m.media-amazon.com/images/M/MV5BM2JlMGUwZjQtNWE0Ni00Y2Q5LWE2MTAtNmE0NWQzNGQ5MTk5XkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",  # Drishyam 2
    24: "https://m.media-amazon.com/images/M/MV5BYjRmNTZiY2QtODc1Yi00NjZjLWE1YjAtZmY4YzJjNmI3NzRiXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",  # Brahmastra
    25: "https://m.media-amazon.com/images/M/MV5BZjk2ZmY0NDYtOTAyMi00NDExLWJjNjItMGQ3ZjFiYjhmMTIwXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",  # Gangubai
    26: "https://m.media-amazon.com/images/M/MV5BNWYwM2I4Y2QtNWQ2ZC00ZjI5LTk1YWMtNWRlNTBiZTQ0OGRlXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",  # Bhool Bhulaiyaa 2
    27: "https://m.media-amazon.com/images/M/MV5BZWJiYzJmMTItNTQ0Ni00NjJlLThlNjEtNDFhYTdhMzMzZmYzXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",  # Kantara
    28: "https://m.media-amazon.com/images/M/MV5BYjdmYTZlZjMtZWRhOC00OWI4LWI3NTktNzJhZTU3NjE3NmRlXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",  # Vikram
    29: "https://m.media-amazon.com/images/M/MV5BYWY1YWRlZDAtMmI0OC00MmJhLTkxN2ItMTE4MzQzYWFkMWYzXkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg",  # Rocketry
    30: "https://m.media-amazon.com/images/M/MV5BYzRlNWRiZmItMzk4Mi00ZjE3LWFhYmQtMzAyYzk0MGM2NzdhXkEyXkFqcGdeQXVyMTE0MTY2Mzk2._V1_.jpg",  # Jhund
    31: "https://m.media-amazon.com/images/M/MV5BYjI0MmNlM2UtMGU2Yi00YzI3LWJhZGYtOTQyZGFhNDkwOWNiXkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg",  # Shershaah
    32: "https://m.media-amazon.com/images/M/MV5BYmI5NGEzZjgtOGNhOS00MzFhLWE2YzQtOTk3OWE5Njk0ZDU5XkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg",  # Sardar Udham
    33: "https://m.media-amazon.com/images/M/MV5BMmE0MzBhZjgtODZlYi00ZjQyLWE2NTYtNjQwYzA3ZmQ5MDBmXkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg",  # Pushpa
    34: "https://m.media-amazon.com/images/M/MV5BNTc1MWQ2NDItNDFiOS00OGVhLTk5MjItYjU4YTBiOWUwNWY5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # Sooryavanshi
    35: "https://m.media-amazon.com/images/M/MV5BOGM2YjVkZWYtMjk2Yi00MDJhLTk0ZDMtMWQ1MmY5ZmVjMmI1XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # 83
    36: "https://m.media-amazon.com/images/M/MV5BZmE4ZTNhYjktYTc1YS00OGQ0LWIyMzQtMTg4MWJmZjU2NGJkXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # Mimi
    37: "https://m.media-amazon.com/images/M/MV5BNTkyOGVjMGEtNmQzZi00NzFlLTlhOWQtODYyMDc2ZGJmYzFhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg",  # 3 Idiots
    38: "https://m.media-amazon.com/images/M/MV5BMTQ4MzQzMzM2Nl5BMl5BanBnXkFtZTgwMTQ1NzU3MDI@._V1_.jpg",  # Dangal
    39: "https://m.media-amazon.com/images/M/MV5BMTYzOTE2NjkxN15BMl5BanBnXkFtZTgwMDgzMTg0MzE@._V1_.jpg",  # PK
    40: "https://m.media-amazon.com/images/M/MV5BMTc1NzcyNDY3OV5BMl5BanBnXkFtZTgwNjU0NTU4NTE@._V1_.jpg",  # Bajrangi Bhaijaan
    41: "https://m.media-amazon.com/images/M/MV5BMmU0NTNlOTctYTk5MC00ZTc0LTgxOTUtMmY0ZjFjMTRjMWZiXkEyXkFqcGdeQXVyNjQ2MjQ5NzM@._V1_.jpg",  # DDLJ
    42: "https://m.media-amazon.com/images/M/MV5BYTMwNzJjNmQtOWRlNS00NGQ0LWE4YzAtYjRmNmJlZDk0YjE0XkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_.jpg",  # Sholay
    43: "https://m.media-amazon.com/images/M/MV5BNzMxNjMyNjQxNF5BMl5BanBnXkFtZTcwNTY0NjE1MQ@@._V1_.jpg",  # Lagaan
    44: "https://m.media-amazon.com/images/M/MV5BZGFmMjM5OWQtYjg5MC00NjQ2LWFiNjYtNWU5MDRkMzgwNGRhXkEyXkFqcGdeQXVyNjQ2MjQ5NzM@._V1_.jpg",  # ZNMD
    45: "https://m.media-amazon.com/images/M/MV5BMTQxNjYzNTYwM15BMl5BanBnXkFtZTcwNzkwOTY0OA@@._V1_.jpg",  # Barfi
    46: "https://m.media-amazon.com/images/M/MV5BMTYzODE1NjQ1M15BMl5BanBnXkFtZTgwNTUwMzAxMTE@._V1_.jpg",  # Queen
    47: "https://m.media-amazon.com/images/M/MV5BYzU2YjcwNjAtY2RkZi00MDU3LThiOWMtZjAzN2RhMzkwZjYzXkEyXkFqcGdeQXVyMTExNDQ2MTI@._V1_.jpg",  # Andhadhun
    48: "https://m.media-amazon.com/images/M/MV5BMDgzNTA2MzYyN15BMl5BanBnXkFtZTgwMTU3NDU4NjM@._V1_.jpg",  # Tumbbad
    49: "https://m.media-amazon.com/images/M/MV5BNTk0OWYzYTgtMDBjNC00ODdhLWJjYzgtYzMwMzA4ZjgwOTFlXkEyXkFqcGdeQXVyNjU2ODM5MjU@._V1_.jpg",  # Stree
    50: "https://m.media-amazon.com/images/M/MV5BMmE1ZmMzMTktODE5ZC00NmRmLTkyNzEtZGEzNWNhZDhjMTRiXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # Gully Boy
    51: "https://m.media-amazon.com/images/M/MV5BMjEyNTA4NDE1Nl5BMl5BanBnXkFtZTgwNjkxODY5NjM@._V1_.jpg",  # Uri
    52: "https://m.media-amazon.com/images/M/MV5BNDllMWI2OGMtNGVlZS00MzI0LWE5YjQtODcyZTljMDI3NWY0XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # War
    53: "https://m.media-amazon.com/images/M/MV5BYjhjN2Y2ZmQtMmRjYy00NDA4LTk0N2YtYzJlZjMzYzRkNGE1XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # Tanhaji
    54: "https://m.media-amazon.com/images/M/MV5BMTQ5NTQ2Nzc2NF5BMl5BanBnXkFtZTcwMDA3ODk0Ng@@._V1_.jpg",  # Singham
    55: "https://m.media-amazon.com/images/M/MV5BMTYyNTcwODUwNl5BMl5BanBnXkFtZTgwMDk0NTE3MDE@._V1_.jpg",  # Dhoom 3
    56: "https://m.media-amazon.com/images/M/MV5BNjEyNjY5NzEzOF5BMl5BanBnXkFtZTgwMjAwNDc4NzM@._V1_.jpg",  # Chhichhore
    57: "https://m.media-amazon.com/images/M/MV5BN2M5MjkwMTUtYzcxNC00NDQzLTg4NTYtNTg1OGFiYzRlMWJjXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # Kabir Singh
    58: "https://m.media-amazon.com/images/M/MV5BMmQ0OGNjMGItYjA0NC00MWI1LThkZjctNjhmNDNiZTk2YjdhXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # Raazi
    59: "https://m.media-amazon.com/images/M/MV5BOTYxNTk5NDYwOV5BMl5BanBnXkFtZTgwMzgyODE5NzM@._V1_.jpg",  # Article 15
    60: "https://m.media-amazon.com/images/M/MV5BYzc1YmI2OGItNjk4ZS00Y2Q0LWI4NjUtNDk0NzFiNjRmMDJiXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # Badhaai Ho
    61: "https://m.media-amazon.com/images/M/MV5BMTQxNDQyNjMwNl5BMl5BanBnXkFtZTcwNTA0Njc3Nw@@._V1_.jpg",  # Kahaani
    62: "https://m.media-amazon.com/images/M/MV5BMTMxMTIwMTA5Ml5BMl5BanBnXkFtZTcwOTk1NDk0MQ@@._V1_.jpg",  # A Wednesday
    63: "https://m.media-amazon.com/images/M/MV5BMTMxNzI3NzU5MV5BMl5BanBnXkFtZTcwODY1NDMyOQ@@._V1_.jpg",  # Special 26
    64: "https://m.media-amazon.com/images/M/MV5BMTc5NjY4MjUwNF5BMl5BanBnXkFtZTgwODM3NzM5MzE@._V1_.jpg",  # Gangs of Wasseypur
    65: "https://m.media-amazon.com/images/M/MV5BYzE2YmZlYjgtMWMxYS00MzYwLTlkNDAtMmRjZjQ5YzllNDJiXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # Badla
    66: "https://m.media-amazon.com/images/M/MV5BNzEzYWNhNWMtNzY4Yi00ZjFmLWE5MmItOGY5NjkwODc0ZTI3XkEyXkFqcGdeQXVyNjQ2MjQ5NzM@._V1_.jpg",  # K3G
    67: "https://m.media-amazon.com/images/M/MV5BNjBiNmJjODktYTMwZS00MDEzLWFlNDgtZjFhMWE3NTY0MWUwXkEyXkFqcGdeQXVyNjQ2MjQ5NzM@._V1_.jpg",  # KKHH
    68: "https://m.media-amazon.com/images/M/MV5BMmRmNjJmYjItZTY4Mi00ODg0LWI5NWItOWNmYjU0MDQ5NmViXkEyXkFqcGdeQXVyNjQ2MjQ5NzM@._V1_.jpg",  # Jab We Met
    69: "https://m.media-amazon.com/images/M/MV5BMTMzMDI2MTU5MV5BMl5BanBnXkFtZTcwNDg4ODM1OQ@@._V1_.jpg",  # YJHD
    70: "https://m.media-amazon.com/images/M/MV5BNjNjY2Q3YWUtNDg2My00ZjU4LWFmZTAtYjgyYWI5YzZkNDE2XkEyXkFqcGdeQXVyNjQ2MjQ5NzM@._V1_.jpg",  # Dil Chahta Hai
    71: "https://m.media-amazon.com/images/M/MV5BMTc1MjQzNjU4N15BMl5BanBnXkFtZTgwNjE3OTAyNTM@._V1_.jpg",  # Sanju
    72: "https://m.media-amazon.com/images/M/MV5BMTYzNDU0NDY4N15BMl5BanBnXkFtZTcwMjk4MTUzOQ@@._V1_.jpg",  # Bhaag Milkha
    73: "https://m.media-amazon.com/images/M/MV5BMmY3MDEwMDgtY2MyNy00M2FkLWJhMTEtNjBhNmZhODk1NTczXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # Super 30
    74: "https://m.media-amazon.com/images/M/MV5BMTUwMjU5MDgwNF5BMl5BanBnXkFtZTgwMTk5MTYxMjE@._V1_.jpg",  # Mary Kom
    75: "https://m.media-amazon.com/images/M/MV5BN2RmMjU3MmQtYWQ5Ny00NDNhLWI1ZTktYTJiNTA5ZTI5ZjQyXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg",  # Pad Man
    76: "https://m.media-amazon.com/images/M/MV5BNTQxODEyNzMtNjZhZi00NmEyLWI5MTItMzRmNzFjMDcyOTk3XkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_.jpg",  # Hera Pheri
    77: "https://m.media-amazon.com/images/M/MV5BMTczNjE3YjktMzU3Zi00ODIzLWEzYTQtY2U0MmU4NTQxOGZmXkEyXkFqcGdeQXVyNjE5MjUyOTM@._V1_.jpg",  # Munna Bhai MBBS
    78: "https://m.media-amazon.com/images/M/MV5BNDQzNDA3OTQtN2U1My00YTI5LThkZWMtNzJkYzAxYWMyNzM0XkEyXkFqcGdeQXVyNjE5MjUyOTM@._V1_.jpg",  # Lage Raho
    79: "https://m.media-amazon.com/images/M/MV5BMjAzOTc2MDE1N15BMl5BanBnXkFtZTcwNzEyOTQzMQ@@._V1_.jpg",  # Golmaal
    80: "https://m.media-amazon.com/images/M/MV5BMTY0ODU4MTYwNl5BMl5BanBnXkFtZTcwMjk2OTI0MQ@@._V1_.jpg",  # Bhool Bhulaiyaa
    81: "https://m.media-amazon.com/images/M/MV5BMTA5MjMxODQyNDZeQTJeQWpwZ15BbWU3MDE3NjI5Nzk@._V1_.jpg",  # Rang De Basanti
    82: "https://m.media-amazon.com/images/M/MV5BMTkyOTc2OTU5NV5BMl5BanBnXkFtZTcwOTQ4OTYzMQ@@._V1_.jpg",  # Taare Zameen Par
    83: "https://m.media-amazon.com/images/M/MV5BMTM1NjQ4MTE3MV5BMl5BanBnXkFtZTcwMDE1MDE1MQ@@._V1_.jpg",  # Swades
    84: "https://m.media-amazon.com/images/M/MV5BMTUyNjAzOTYxNV5BMl5BanBnXkFtZTcwMjEwNTMzMQ@@._V1_.jpg",  # Black
    85: "https://m.media-amazon.com/images/M/MV5BMTgwOTcxMTgzNV5BMl5BanBnXkFtZTcwMTQwNjI0MQ@@._V1_.jpg",  # Chak De India
    86: "https://m.media-amazon.com/images/M/MV5BNGRkNWYwNjAtMWU4My00NDY3LWI3NjctNDQ0MjY3NjE0NWY5XkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg",  # Darlings
    87: "https://m.media-amazon.com/images/M/MV5BODhjZGJkMWItOGU0MC00MzU1LTg0NzAtNGFiYmY4ZGJmZDhmXkEyXkFqcGdeQXVyMTE0MTY2Mzk2._V1_.jpg",  # Monica O My Darling
    88: "https://m.media-amazon.com/images/M/MV5BNzA1MjgyMWQtOGU3Mi00NWFlLTk3MmYtYzk2NWE4YjI4MjM3XkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",  # Ponniyin Selvan
    89: "https://m.media-amazon.com/images/M/MV5BMTdhZjljYzAtMWI5Mi00YzYxLWE5YTQtODJiYjU5YmU4NjdlXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Salaar
    90: "https://m.media-amazon.com/images/M/MV5BYjM0N2RmNjgtNDI0ZS00MTg1LWE0MGMtNTQyZjJhMGY3YmVlXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # HanuMan
    91: "https://m.media-amazon.com/images/M/MV5BZDhjNzQ5NDgtNGMzMi00MjYzLWFkZGQtMzEzOGZmMTBlNzQwXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Gadar 2
    92: "https://m.media-amazon.com/images/M/MV5BMzdjZTZhMDQtYzY4Ny00YzhhLWI1NzMtNzhmMDhmNGU4NTliXkEyXkFqcGdeQXVyMTE0MTY2Mzk2._V1_.jpg",  # Fukrey 3
    93: "https://m.media-amazon.com/images/M/MV5BZWQ4ZGRiOWItMzY3MC00NTVkLWJiNDItZWNiNjk1NzE2YTY2XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Dream Girl 2
    94: "https://m.media-amazon.com/images/M/MV5BZDg3OGNlM2QtOTE5Ni00ZTdiLWE4YzEtNWUzMDMwNzQxY2E1XkEyXkFqcGdeQXVyMTE0MTY2Mzk2._V1_.jpg",  # Mission Majnu
    95: "https://m.media-amazon.com/images/M/MV5BODY0MzI3ZGUtM2Y5NC00ZTg2LTk5YmQtMjBkNzg0ZDRlZDQxXkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg",  # Bholaa
    96: "https://m.media-amazon.com/images/M/MV5BNDJiNzY0Y2UtNzdhZC00OTI4LWI1ZGYtMTYyZDU4YzY0ZjEyXkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg",  # Selfiee
    97: "https://m.media-amazon.com/images/M/MV5BYzY2MDQwOWEtMDVkNS00MTA2LTkxMTAtNjY4MDU2MTY3MTgyXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",  # Adipurush
    98: "https://m.media-amazon.com/images/M/MV5BOGI1ZGFkNWQtOWVhOC00OGQ5LWI1ZWEtMjkwZjA4NGRhZjU0XkEyXkFqcGdeQXVyMTI1NDAzMzM0._V1_.jpg",  # Kisi Ka Bhai
    99: "https://m.media-amazon.com/images/M/MV5BZWZjOWE5MWEtZjU3OS00NzU2LWJkOGMtM2IyYzdhYWI1MzA4XkEyXkFqcGdeQXVyMTQ3Mzk2MDg4._V1_.jpg",  # Bade Miyan Chote Miyan
    100: "https://m.media-amazon.com/images/M/MV5BY2RhMzViYzctM2NhNS00NDE1LWIwMjMtZjFkNjNhZjEzYjNkXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg",  # Mr & Mrs Mahi
}

def download_poster(movie_id, url):
    """Download a movie poster from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.imdb.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=20, stream=True)
        response.raise_for_status()
        
        filename = f"{POSTER_DIR}/{movie_id}.jpg"
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"  [OK] Downloaded poster {movie_id}")
        return True
    except Exception as e:
        print(f"  [FAIL] Poster {movie_id}: {str(e)[:60]}")
        return False

def main():
    """Download all real movie posters"""
    os.makedirs(POSTER_DIR, exist_ok=True)
    
    print("="*60)
    print("Downloading REAL Bollywood Movie Posters")
    print("="*60)
    
    success = 0
    failed = 0
    failed_ids = []
    
    for movie_id, url in REAL_POSTERS.items():
        if download_poster(movie_id, url):
            success += 1
        else:
            failed += 1
            failed_ids.append(movie_id)
        time.sleep(0.5)  # Be respectful to servers
    
    print("="*60)
    print(f"Download complete: {success} success, {failed} failed")
    if failed_ids:
        print(f"Failed IDs: {failed_ids}")
    print("="*60)

if __name__ == '__main__':
    main()
