from osu_api import OsuApi


def osu_create_pm(
    target_id: int,
    message: str,
    is_action: bool = False,
):
    return OsuApi(f'chat/new').add_json(locals(), 'target_id', 'message', 'is_action').post()


if __name__ == '__main__':
    print(osu_create_pm(13275309, 'performance'))
