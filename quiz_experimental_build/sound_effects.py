import pygame as pg
import time


pg.mixer.init()

right_answer_sound = pg.mixer.Sound("virgil.mp3")
wrong_answer_sound = pg.mixer.Sound("vrong.mp3")


if __name__ == "__main__":
    right_answer_sound.play()
    time.sleep(2)

    