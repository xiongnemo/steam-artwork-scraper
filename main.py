import os
import sys
import getopt
from bs4.element import *
import requests
from bs4 import BeautifulSoup
import marshmallow.steamcardexahangescraper as steamcardexahangescraper

STEAM_CARD_EXCHANGE_BASE_URL = "https://www.steamcardexchange.net/index.php?gamepage-appid-"


def show_help():
    print("Usage: -i <Steam Appid>")
    print("   or: --STEAM_APP_ID=<Steam Appid>")
    print("If you do not supply command line argument, the script will ask for the <Steam Appid> at startup.")


def scrape(steam_appid: str) -> None:
    print(f"Appid = {steam_appid}")
    if os.path.exists(f"{steam_appid}_reply.html"):
        print("[+] Cached file found")
        with open(f"{steam_appid}_reply.html", 'r', encoding='utf8') as f:
            response = f.read()
    else:
        print("[-] No cached file found.")
        print("[+] Pulling from server...")
        r_orig = requests.get(f"{STEAM_CARD_EXCHANGE_BASE_URL}{steam_appid}")
        response = r_orig.content
        print("[+] Writing cache...")
        with open(f'{steam_appid}_reply.html', 'wb') as f:
            f.write(response)
    soup = BeautifulSoup(response, "html.parser")
    # game title
    game_title: Tag
    game_title_list: list[Tag]
    game_title_list = soup.select(".game-title")
    if len(game_title_list) == 1:
        game_title = game_title_list[0]
        game_name = game_title.text.strip()
        print(f"Name: {game_name}")
    else:
        print("[-] No game title found.")
        exit(1)
    
    RESULT_DIR = os.path.join("downloaded")
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)
    os.chdir(RESULT_DIR)

    DEST_DIR = os.path.join(f"{steam_appid} - {game_name}")
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
    os.chdir(DEST_DIR)
    # 620: Portal 2
    # 0: advertisement
    # 1: content-box including all
    # 2: series-1
    # 3: cards
    # 4: foilcards
    # 5: booster
    # 6: badges
    # 7: foilbadges
    # 8: emoticons
    # 9: backgrounds
    # 10: avataranimated
    # 11: ADVERTISEMENT
    content_box_list = soup.select(".content-box")
    # drop first two
    content_box_list = content_box_list[2:]
    # drop last
    content_box_list = content_box_list[:-1]
    item: Tag
    for item in content_box_list:
        span_id: str
        span_id = item.span["id"]
        span_id_splited = span_id.split("-")
        if len(span_id_splited) == 2:
            print(f"Series {span_id_splited[1]}")
        elif len(span_id_splited) == 3:
            print(f"Series {span_id_splited[1]}: {span_id_splited[2]}")
            try:
                tag_processing_function = getattr(
                    steamcardexahangescraper, span_id_splited[2])
                tag_processing_function(item)
            except AttributeError:
                print("[-] No corresponding method in module found. PLEASE OPEN AN ISSUE.")


def main(argv: list):
    steam_appid = ""

    try:
        opts, args = getopt.getopt(
            argv, "hi:", ["help", "STEAM_APPID="])
    except getopt.GetoptError:
        show_help()
        exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit(1)
        elif opt in ("-i", "--STEAM_APPID"):
            try:
                steam_appid = str(int(arg))
            except ValueError:
                print("Supplied steam appid argument is not an int")
    if steam_appid == "":
        print("No vaild steam appid supplied.")
        while True:
            steam_appid_input = input("Steam appid?\n> ")
            try:
                steam_appid = str(int(steam_appid_input))
                break
            except ValueError:
                pass

    scrape(steam_appid)


if __name__ == '__main__':
    main(sys.argv[1:])
