import os
from bs4.element import *
import requests
import inspect
from tqdm import tqdm


def not_implemented() -> None:
    print("[-] Not implemented.")


def generic_artwork(showcase_element: Tag) -> None:
    upper_function_name = str(inspect.stack()[1].function)
    DEST_DIR = os.path.join(f"{upper_function_name}")
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
    os.chdir(DEST_DIR)
    showcase_element_list = showcase_element.select(".showcase-element")
    showcase_element: Tag
    for showcase_element in showcase_element_list:
        element_link_right_list: list[Tag]
        element_link_right_list = showcase_element.select(
            ".element-link-right")
        if len(element_link_right_list) == 0:
            continue
        element_text: Tag
        element_text = showcase_element.select_one(".element-text")
        img_title = element_text.text
        img_link = element_link_right_list[0]['href']
        print(f"{img_title}: {img_link}")
        filename_from_url = img_link.rsplit('/', 1)[1]
        suffix = filename_from_url.split(".")[1]
        filename = f"{img_title}.{suffix}"
        if os.path.exists(filename):
            print("[+] File exists.")
            continue
        print(f"[*] Downloading image from {img_link}")
        file_request = requests.get(img_link, stream=True)
        total_size_in_bytes = int(
            file_request.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes,
                            unit='iB', unit_scale=True)
        with open(filename, "wb") as f:
            for data in file_request.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        print(f"[+] Image saved.")
    os.chdir("..")


def cards(cards_tag: Tag) -> None:
    generic_artwork(cards_tag)


def foilcards(foilcards_tag: Tag) -> None:
    generic_artwork(foilcards_tag)


def booster(booster_tag: Tag) -> None:
    not_implemented()


def badges(badges_tag: Tag) -> None:
    not_implemented()


def foilbadges(foilbadges_tag: Tag) -> None:
    not_implemented()


def emoticons(emoticons_tag: Tag) -> None:
    not_implemented()


def backgrounds(backgrounds_tag: Tag) -> None:
    generic_artwork(backgrounds_tag)


def avataranimated(avataranimated_tag: Tag) -> None:
    not_implemented()


def animatedstickers(animatedstickers_tag: Tag) -> None:
    not_implemented()
