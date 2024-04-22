from random import choice
from typing import Set, Dict
import string
from app.models.user_auth.user_auth import GameUser
from app import game_db
from dataclasses import dataclass
import datetime


list_of_words = [
    "lizards",
    "agreement",
    "insurance",
    "authority",
    "ornament",
    "beetle",
    "grandfather",
    "feeling",
    "bassketball",
    "invention",
    "wine",
    "cabbage",
    "whistle",
]


class HangmanGame:
    MAX_GUESSES = 6
    BAD_GUESSES = 0

    def __init__(self, user: GameUser) -> None:
        self.user = GameUser
        self.used_letters = set()
        self.game_word = choice(list_of_words).strip()

    def player_input(self) -> str:
        while True:
            user_input = input("Guess your letter: ").lower()
            if (
                len(user_input) == 1
                and user_input in string.ascii_lowercase
                and user_input not in self.used_letters
            ):
                return user_input

    def join_guessed_letters(self) -> str:
        return " ".join(sorted(self.used_letters))

    def not_used_letters(self, guessed_letters) -> str:
        full_string = string.ascii_lowercase
        for letter in guessed_letters:
            full_string = full_string.replace(letter, "")
        return full_string

    def guessing_word(self) -> str:
        current_letters = []
        for letter in self.game_word:
            if letter in self.used_letters:
                current_letters.append(letter)
            else:
                current_letters.append("_")
        return " ".join(current_letters)

    def game_over(self):
        if self.BAD_GUESSES == self.MAX_GUESSES:
            return True
        if set(self.game_word) <= self.used_letters:
            return True
        return False


# class GameStats(HangmanGame):
#     def __init__(self, user: GameUser) -> None:
#         super().__init__(GameUser)

#     def get_games_played_by_the_user(self) -> Dict:
#         print(self.user["email"])
#         users_played_games = game_db.find_documents(
#             {
#                 "user email": GameUser.email,
#             },
#             {"_id": 0},
#         )
#         return users_played_games

#     def get_games_played_by_the_user_today(self) -> Dict:
#         todays_games = []
#         current_day_of_the_month = datetime.datetime.now().day
#         for game in self.get_games_played_by_the_user():
#             if game["date"].day == current_day_of_the_month:
#                 todays_games.append(game)

#         return todays_games

#     def get_number_of_games_played_today(self) -> int:
#         return len(self.get_games_played_by_the_user_today())
