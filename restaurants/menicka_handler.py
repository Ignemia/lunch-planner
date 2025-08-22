import bs4
import typing

def extract_information_menicka(soup: bs4.BeautifulSoup) -> typing.Tuple[str, typing.Optional[int], str]:
    _name = soup.find("h1").text
    _distance = 0
    _menu = soup.find(class_="obsah").find("menicka").text
    return _name, _distance, _menu
