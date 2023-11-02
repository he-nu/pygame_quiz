import pygame as pg
import time


pg.mixer.init()

right_answer_sound = pg.mixer.Sound("sounds/virgil.mp3")
wrong_answer_sound = pg.mixer.Sound("sounds/vrong.mp3")
level_up_sound = pg.mixer.Sound("sounds/powerup.mp3")
win_sound = pg.mixer.Sound("sounds/game_win.mp3")
button_sound = pg.mixer.Sound("sounds/button.mp3")


if __name__ == "__main__":
    pg.mixer.music.play()
    time.sleep(8)

    