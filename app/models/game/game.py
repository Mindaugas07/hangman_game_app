from random import choice
from typing import Set
import string

# from hangman_draw import draw_hangman

# from hangman_game_app.app.models.user_auth.user_auth import GameUser

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

    def __init__(self, used_letters: Set[str]) -> None:
        self.used_letters = used_letters
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


# if __name__ == "__main__":
#     # user = GameUser()
#     new_game = HangmanGame(used_letters=set())
#     bad_guesses = 0

#     while not new_game.game_over(bad_guesses):
#         draw_hangman(bad_guesses)
#         print(f"Game word is: {new_game.guessing_word()}")
#         print("Your guessed letters: " f"{new_game.join_guessed_letters()}\n")

#         player_guess = new_game.player_input()
#         if player_guess in new_game.game_word:
#             print("Great guess!")
#         else:
#             print("Nope, it's not there.")
#             bad_guesses += 1

#         new_game.used_letters.add(player_guess)
#         selected_word = new_game.guessing_word()

#     draw_hangman(bad_guesses)
#     if bad_guesses == HangmanGame.MAX_GUESSES:
#         print("Sorry, you lost!")
#     else:
#         print("Congratulation! You won the game!")
#     print(f"Your word was: {new_game.game_word}")
