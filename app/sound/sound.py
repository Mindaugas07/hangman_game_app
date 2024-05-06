from playsound import playsound


def success_sound() -> None:
    playsound("app/static/sounds/correct.mp3")


def incorect_sound() -> None:
    playsound("app/static/sounds/wrong.mp3")
