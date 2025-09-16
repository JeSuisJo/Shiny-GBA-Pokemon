import pyautogui
from PIL import Image
import pytesseract
import json
import time
import pydirectinput
from pywinauto import Application

def choisir_langue():
    langues = {
        '1': 'jp', '2': 'en', '3': 'fr', '4': 'de',
        '5': 'es', '6': 'it', '7': 'ko', '8': 'zh-Hans', '9': 'zh-Hant'
    }
    print("Choisissez votre langue préférée:")
    print("1: 日本語 (Japanese)")
    print("2: English")
    print("3: Français")
    print("4: Deutsch")
    print("5: Español")
    print("6: Italiano")
    print("7: 한국어 (Korean)")
    print("8: 简体中文 (Simplified Chinese)")
    print("9: 繁體中文 (Traditional Chinese)")

    choix = input("Entrez le numéro de votre choix: ")
    while choix not in langues:
        print("Choix invalide. Veuillez essayer à nouveau.")
        choix = input("Entrez le numéro de votre choix: ")

    return langues[choix]

def zone(area):
    left, top, width, height = area
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    text = pytesseract.image_to_string(screenshot)
    return text

def shiny_check(x, y):
    screenshot = pyautogui.screenshot()
    pixel_color = screenshot.getpixel((x, y))
    return pixel_color

def detecter_mot(mot, area):
    text = zone(area)
    return mot.lower() in text.lower()

def couleur_proche(couleur1, couleur2, tolérance=5):
    return all(abs(c1 - c2) <= tolérance for c1, c2 in zip(couleur1, couleur2))

with open('shiny.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def combat():
    pas_reset = False
    x, y = 960, 500

    while not pas_reset:
        if not detecter_mot('JOUEUR', reset_text):
            pydirectinput.press('enter')
            time.sleep(0.5)
        else:
            joueur_trouve = False
            while not joueur_trouve:
                pixel_color = shiny_check(x, y)
                femme = (190, 73, 78)
                homme = (192, 56, 56)

                if couleur_proche(pixel_color, femme) or couleur_proche(pixel_color, homme):
                    joueur_trouve = True
                    pydirectinput.press('q')
                    time.sleep(1)
                        
                else:
                    pydirectinput.press('q')
                    time.sleep(0.7)
            pas_reset = True

            
reset_text = (328, 54, 1254, 562)
text_combat = (272, 782, 1373, 200)
pokemon_trouve = data['pokemon_trouve']
nombre_rencontre = 0

langue_preferee = choisir_langue()

try:
    app = Application().connect(title='Pokemon - Version Rouge Feu (France) - VisualBoyAdvance-M 2.1.9')
    app_window = app.window(title='Pokemon - Version Rouge Feu (France) - VisualBoyAdvance-M 2.1.9')
    app_window.set_focus()
except Exception as e:
    print(f"Erreur: {e}")

time.sleep(1)
pydirectinput.keyDown('ctrl')
pydirectinput.press('r')
pydirectinput.keyUp('ctrl')
time.sleep(1)
combat()

while True:
    found_word = False

    for pokemon in pokemon_trouve:
        nom = pokemon['nom'][langue_preferee]

        couleur = pokemon['couleur']

        if detecter_mot(nom, text_combat):
            found_word = True
            for check_couleur, info in couleur.items():
                rgb_value = info['rgb']
                coordinates = info['coordinates']

                pixel_color = shiny_check(coordinates[0], coordinates[1])

                if couleur_proche (pixel_color, tuple(rgb_value)):
                    if check_couleur == 'normal':
                        nombre_rencontre += 1
                        print(f"Nombre de rencontre = {nombre_rencontre}")
                        pydirectinput.keyDown('ctrl')
                        pydirectinput.press('r')
                        pydirectinput.keyUp('ctrl')
                        combat()

                    elif check_couleur == 'shiny':
                        print(f"Le pokémon est shiny. Nombre de rencontre = {nombre_rencontre}")
                        found_word = True
                        exit()
