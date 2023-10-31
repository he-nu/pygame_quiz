import pygame as pg
import time


pg.mixer.init()

right_answer_sound = pg.mixer.Sound("virgil.mp3")
wrong_answer_sound = pg.mixer.Sound("vrong.mp3")
level_up_sound = pg.mixer.Sound("powerup.mp3")


if __name__ == "__main__":
    level_up_sound.play()
    time.sleep(2)

    