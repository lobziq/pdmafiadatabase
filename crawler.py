import requests
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from bs4 import BeautifulSoup, Tag
from enum import Enum, auto
from typing import Tuple, List, Optional, Set
from lxml.etree import HTML


class Faction(Enum):
    city = auto()
    mafia = auto()
    neutral = auto()


@dataclass
class Group:
    name: str
    faction: Optional[Faction] = None

    def __post_init__(self):
        if not self.faction:
            if self.name in ["norole", "active"]:
                self.faction = Faction.city

            if "mafia" in self.name:
                self.faction = Faction.mafia

            if "neutral" in self.name:
                self.faction = Faction.neutral


@dataclass
class Role:
    name: str
    group: Group

    def __post_init__(self):
        if self.name != "Мирный житель" and self.group.name == "norole":
            self.group.name = "active"


@dataclass_json
@dataclass
class Setting:
    name: str
    author: str
    role_list: List[Role] = field(default_factory=list)


@dataclass_json
@dataclass
class PlayerStatus:
    exit_day_number: int
    exit_reason: str
    exit_frame: str


@dataclass_json
@dataclass
class Player:
    name: str
    role_name: str
    status: PlayerStatus


@dataclass_json
@dataclass
class Game:
    prodota_id: int
    pdmafia_id: int
    name: str
    setting_name: str
    host: str
    time_str: str
    day_count: int
    tags: List[str] = field(default_factory=list)
    faction_winner_list: Set[str] = field(default_factory=set)
    player_list: List[Player] = field(default_factory=list)


class PDMafiaCrawler:
    def __init__(self) -> None:
        self.base_url = "http://pdmafia.com"
        pass

    def get_url_soup(self, url: str) -> Tuple[BeautifulSoup, HTML]:
        r = requests.get(f"{self.base_url}{url}", timeout=30)
        soup = BeautifulSoup(r.text, 'html.parser')
        html = HTML(str(soup))
        return soup, html

    def get_setting_list(self) -> List[Tuple[int, Setting]]:
        setting_list = list()
        soup, html = self.get_url_soup(f"/settings")
        for element in set([e for e in soup.find_all("a") if e["href"] and "/settings/" in e["href"]]):
            setting_url = str(element["href"])
            setting_id = int(setting_url.split('/')[-1])
            setting_name = element.get_text()
            setting_list.append((setting_id, self.get_setting(setting_id, setting_name)))
        return setting_list

    def get_setting(self, setting_id: int, setting_name: Optional[str] = None) -> Setting:
        soup, html = self.get_url_soup(f"/settings/{setting_id}")
        author = html.xpath("/html/body/div/div/div/div/div/div[2]/div/div/div/table/tbody/tr[1]/td[2]/a")[0].text
        setting = Setting(name=setting_name if setting_name else f"Сеттинг {setting_id}", author=author)

        for element in [e for e in soup.find_all("span", class_=lambda t: t.startswith("faction") if t else None) if e]:
            clean_text = "".join(element.stripped_strings).replace(',', '')
            pdmafia_faction = "".join(element.attrs['class'][0].split('-')[1:])
            setting.role_list.append(Role(name=clean_text, group=Group(name=pdmafia_faction)))

        setting.role_list = [r for r in setting.role_list if r.group.faction]
        return setting

    def get_game_list(self) -> List[Game]:
        soup, html = self.get_url_soup(f"/games")

        game_list = list()

        for element in [e for e in soup.find_all("tr")]:
            contents = [p for p in element.contents if isinstance(p, Tag)]
            pdmafia_game_id = int(contents[1].contents[0]["href"].split('/')[-1])
            tags = [contents[3].get_text(strip=True)]
            game_list.append(self.get_game(pdmafia_game_id=pdmafia_game_id, tags=tags))

        return game_list

    def get_game(self, pdmafia_game_id: int, tags: List[str] = None) -> Game:
        _tags = list() if not tags else [t for t in tags]
        soup, html = self.get_url_soup(f"/games/{pdmafia_game_id}")
        prodota_id = int(html.xpath("/html/body/div/div/div/section/div/div[1]/div/div/table/tbody/tr[1]/td[2]")[0].text)
        name = html.xpath("/html/body/div/div/div/section/div/div[1]/div/div/table/tbody/tr[2]/td[2]")[0].text
        setting_name = html.xpath("/html/body/div/div/div/section/div/div[1]/div/div/table/tbody/tr[3]/td[2]/a")[0].text
        host = html.xpath("/html/body/div/div/div/section/div/div[1]/div/div/table/tbody/tr[4]/td[2]/a")[0].text
        time_str = html.xpath("/html/body/div/div/div/section/div/div[1]/div/div/table/tbody/tr[5]/td[2]")[0].text
        day_count = html.xpath("/html/body/div/div/div/section/div/div[1]/div/div/table/tbody/tr[6]/td[2]")[0].text

        game = Game(prodota_id=prodota_id, pdmafia_id=pdmafia_game_id, name=name, setting_name=setting_name, host=host, time_str=time_str, day_count=day_count, tags=_tags)

        for element in [e for e in soup.find_all("span", class_=lambda t: t.startswith("faction") if t else None) if e]:
            if "Фракция победитель" in [p for p in element.parents][1].get_text():
                game.faction_winner_list.add("".join(element.attrs['class'][0].split('-')[1:]))

        player_table = [e for e in soup.find_all("tbody")][1]

        for player in [p for p in player_table.children if isinstance(p, Tag)]:
            try:
                player_contents = [p for p in player.contents if isinstance(p, Tag)]
                player_name = player_contents[1].get_text(strip=True)
                player_role_name = player_contents[2].get_text(strip=True)
                player_status_list = player_contents[3].get_text().split()
                player_status = PlayerStatus(exit_day_number=player_status_list[-2], exit_reason=' '.join(player_status_list[:-2]), exit_frame=player_status_list[-1])
                game.player_list.append(Player(name=player_name, role_name=player_role_name, status=player_status))
            except IndexError as e:
                pass

        return game


if __name__ == "__main__":
    crawler = PDMafiaCrawler()

    # for setting_id, setting in crawler.get_setting_list():
    #     with open(f"test/static/settings/{setting_id}.json", 'w', encoding='utf-8') as f:
    #         f.write(setting.to_json(ensure_ascii=False))

    for game in crawler.get_game_list():
        with open(f"test/static/games/{game.prodota_id}.json", 'w', encoding='utf-8') as f:
            f.write(game.to_json(ensure_ascii=False))
