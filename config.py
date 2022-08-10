
FIL_BLANC = 8
FIL_GRIS = 7
FIL_VIOLET = 1
FIL_BLEU = 0
FIL_VERT = 5
FIL_JAUNE = 6
FIL_MARRON = 12


BUZZER = FIL_MARRON

CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
PRINT_RATIO = 3.5/5

LED_ROUGE = FIL_GRIS
LED_VERTE = FIL_BLANC

BTN_TRIG = FIL_VIOLET
BTN_1 = FIL_JAUNE
BTN_2 = FIL_VERT
BTN_3 = FIL_BLEU

COUNTDOWN_PIC = 5
COUNTDOWN_BTWN = 1

WINDOW_NAME = "tomaton"

PATH_TMP_NUM = "/tmp/pic{}.jpg"
PATH_TMP = PATH_TMP_NUM.format("")

PATH_PIC = "/home/pi/Pictures/pic_{}.jpg"

#PRINT_COMMAND = "lp -o PageSize=3.5x5.Borderless MediaType=PhotographicGlossy cupsPrintQuality=High print-content-optimize=photo"
PRINT_COMMAND = "lp -o PageSize=3.5x5.Borderless MediaType=Stationery cupsPrintQuality=High print-content-optimize=photo {}"
# -o PageSize=3.5x5 -o MediaType=Stationery -o cupsPrintQuality=High -o print-content-optimize=photo -d HP_ENVY_4500_series_438CF8_ 
# lp -o PageSize=3.5x5.Borderless MediaType=Stationery cupsPrintQuality=High print-content-optimize=photo