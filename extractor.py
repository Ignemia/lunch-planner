if __name__ == "__main__":
    response = pullMenicka()
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        menicka = soup.find_all("div", class_="menicka_detail")

        for m in menicka:
            cleaned_text = re.sub(r'^\s*$', '', m.text, flags=re.MULTILINE).strip()  # Remove empty lines and excess whitespace
            is_name = True
            is_phone = False
            is_distance = False
            current_restaurant = None

            for line in cleaned_text.splitlines():
                if len(line.strip()) == 0:
                    continue
                if is_name:
                    current_restaurant = Restaurant(line.strip())
                    is_name = False
                    is_phone = True
                    continue

                if is_phone:
                    is_phone = False
                    is_distance = True
                    continue

                if is_distance:
                    assert current_restaurant is not None
                    d = re.match(r"Vzdálenost\:\ (\d+)\s*(k?m).*", line)
                    if d:
                        distance = d.group(1)
                        current_restaurant.add_distance(float(distance), DISTANCE_UNITS.M)
                    is_distance = False
                    continue
                if
            ALL_RESTAURANTS.add(current_restaurant)
            current_restaurant = None

        for r in ALL_RESTAURANTS:
            print(r)
    else:
        print("ERROR GATHERING DATA")
