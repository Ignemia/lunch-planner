import bs4
import typing

def extract_information_menicka(soup: bs4.BeautifulSoup) -> typing.Tuple[str, typing.Optional[int], bs4.BeautifulSoup]:
    assert isinstance(soup, bs4.BeautifulSoup)
    _name = soup.find("h1").text
    _distance = 0
    _content = soup.find(class_="obsah")
    if _content:
        return _name, _distance, _content.find(class_ = "menicka")
    return _name, _distance, ""
