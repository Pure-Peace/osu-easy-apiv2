import json
from typing import Literal, Optional

from osu_api import OsuApi

GameMode = Literal['fruits', 'mania', 'osu', 'taiko']
RankingType = Literal['charts', 'country', 'performance', 'score']
RankingFilter = Literal['all', 'friends']


def osu_ranking(
    mode: GameMode,
    ranking_type: RankingType,
    country: Optional[str] = None,
    cursor: Optional[str] = None,
    filter: Optional[RankingFilter] = None,
    spotlight: Optional[str] = None,
    variant: Optional[str] = None
):
    return OsuApi(f'rankings/{mode}/{ranking_type}').add_queries(
        locals(),
        'country', 'cursor', 'filter', 'spotlight', 'variant').send()


def get_ranking_with_pages(country: str, start_page: int, end_page: int, file_save='ranking.json'):
    rankings = []
    for page in range(start_page, end_page + 1):
        print('page', page)
        rankings += osu_ranking('osu', 'performance', country=country,
                                cursor=f'cursor[page]={page}')['ranking']
        print('current', len(rankings))

    with open(file_save, 'w') as f:
        f.write(json.dumps(rankings, indent=2))

    return rankings


if __name__ == '__main__':
    print(osu_ranking('osu', 'performance', country='CN'))
