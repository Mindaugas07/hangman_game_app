from random import choice
from typing import Set, Dict
import string, json
from app.models.user_auth.user_auth import GameUser
from app import game_db
from datetime import datetime
from flask_login import login_required, current_user

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
    MAX_GUESSES = 10

    def __init__(
        self,
        user,
        game_status=None,
        used_letters=set(),
        game_word=choice(list_of_words),
        bad_guesses=0,
    ) -> None:
        self.user = user
        self.game_status = None
        self.used_letters = used_letters
        self.game_word = game_word
        self.bad_guesses = bad_guesses

    def guessed_letters(self) -> str:
        return self.join_guessed_letters()

    def set_new_game_word(self) -> None:
        self.game_word = choice(list_of_words).strip()

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

    def set_game_status(self, status) -> None:
        if status == "won":
            self.game_status = f"""Congratulations, you won!!!"""
        elif status == "lost":
            self.game_status = f"""Sorry you lost!
                The word was: '{self.game_word}'.
                Do you want to play again?"""

    def game_over(self):
        if self.bad_guesses == self.MAX_GUESSES:
            return True
        if set(self.game_word) <= self.used_letters:
            return True
        return False

    def insert_game_stats_to_mongo(self, game_outcome: str) -> list:
        self.set_game_status(game_outcome)
        print(f"You made {self.bad_guesses} bad quesses")
        document = self.serialized_game_stats(game_outcome, self.bad_guesses)
        result = game_db.collection.insert_one(document)
        print(f"Inserted document with ID: {result.inserted_id}")
        self.set_game_status(game_outcome)

    def serialized_game_stats(self, status: str, guesses_made: int) -> Dict:
        """Status must be 'won' or 'lost'"""
        game_status_db = status
        current_username = self.user.name
        current_username_email = self.user.email
        current_date = datetime.now()
        current_time = datetime.now().strftime("%H:%M:%S")
        game_word = self.game_word
        return {
            "username": current_username,
            "user email": current_username_email,
            "date": current_date,
            "time": current_time,
            "game result": game_status_db,
            "game word": game_word,
            "guesses made": guesses_made,
        }

    def obj_to_json(self):
        return {
            "username": self.user.name,
            "used letters": list(self.used_letters),
            "game word": self.game_word,
            "bad guesses": self.bad_guesses,
        }

    @classmethod
    def obj_from_json(cls, json_obj: Dict):
        cls.user = current_user
        cls.used_letters = set(json_obj["used letters"])
        cls.game_word = json_obj["game word"]
        cls.bad_guesses = json_obj["bad guesses"]

        return HangmanGame(
            user=cls.user,
            used_letters=cls.used_letters,
            game_word=cls.game_word,
            bad_guesses=cls.bad_guesses,
        )
