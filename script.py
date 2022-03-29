import json
from textwrap import indent
import time
from osu_ranking import osu_ranking
from osu_create_pm import osu_create_pm


""" rankings = []
for page in range(1, 7):
    print('page', page)
    rankings += osu_ranking('osu', 'performance', country='CN',
                            cursor=f'cursor[page]={page}')['ranking']
    print('current', len(rankings))

with open('ranking.json', 'w') as f:
    f.write(json.dumps(rankings, indent=2))
 """

with open('ranking.json') as f:
    rankings = json.loads(f.read())

print('count', len(rankings))


msg = '❥你好，欢迎报名ocl马比赛，比赛规则请看https://docs.qq.com/doc/DTktOR2FmRHdGRGtQ，赛群群号：283956146；staff群群号894875547，如果有任何问题和建议，也可以在游戏内联系prophet或者发pm'

num = 0
for ranking in rankings:
    user_id = ranking['user']['id']
    username = ranking['user']['username']
    pp = ranking['pp']
    rank = ranking['global_rank']
    num += 1
    print(num, username, user_id, pp, rank)
    try:
        print(osu_create_pm(user_id, msg))
        time.sleep(1.5)
    except Exception as err:
        print(err)
