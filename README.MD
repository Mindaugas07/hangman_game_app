# Hangman Game in Flask

## Description
Game of Hangman in your browser. The user gets a hidden word and has to guess it letter by letter until either the word is complete or the man in the picture is hanged. The user can add or replace words in 'hangman_game_app/app/game/game_words.py'. User registration is stored using SQL database. All necessary game data is stored using Mongo DB.

## Instalation

1. Download the latest version of python.

2. Navigate to the directory of your choice.

3. Clone the repository:
```
git clone https://github.com/Mindaugas07/hangman_game_app
```
4. Create and run a virtual environment.
```
python -m venv .venv
source .venv/Scripts/activate
```

5. Install dependencies.
```
pip install -r requirements.txt
```

6. Install Docker.

7. Navigate to the directory where the docker file is located and run a command in terminal.
```
docker-compose up --build --force-recreate --no-deps
```

8. Run the program.
```
Flask run
```















