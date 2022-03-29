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
    return OsuApi(f'rankings/{mode}/{ranking_type}', locals()).add_queries(
        'country', 'cursor', 'filter', 'spotlight', 'variant').send()


if __name__ == '__main__':
    print(osu_ranking('osu', 'performance', country='CN'))
