import json
from textwrap import indent
import time
from turtle import done
from osu_ranking import osu_ranking, get_ranking_with_pages
from osu_create_pm import osu_create_pm


def get_done():
    try:
        with open('done.json') as f:
            return json.loads(f.read())
    except:
        return []


def get_ranking():
    try:
        with open('ranking.json') as f:
            return json.loads(f.read())
    except:
        return get_ranking_with_pages('CN', 1, 9)


def handle_send(msg, ranking):
    user_id = ranking['user']['id']
    username = ranking['user']['username']

    if username in done:
        print('skip', username)
        return True

    pp = ranking['pp']
    rank = ranking['global_rank']
    print(
        f'sending: {username}, id: {user_id}, pp: {pp} rank: {rank}')
    try:
        osu_create_pm(user_id, msg)
        done.append(username)
        with open('done.json', 'w') as f:
            f.write(json.dumps(done, indent=2))
        time.sleep(1)
        return True
    except Exception as err:
        print(err)
        time.sleep(1)
        return False


def start_handle(msg, rankings):
    num = 0
    for ranking in rankings:
        retry = 0
        flag = True
        while flag:
            flag = not handle_send(msg, ranking)
            retry += 1
            print('try', retry)
        num += 1

if __name__ == '__main__':
    rankings = get_ranking()
    print('count', len(rankings))
    
    if len(rankings) == 0:
        raise Exception('No rankings')

    done = get_done()

    msg = '''时隔一年多, OCLB再次开赛
    比赛会申请badge!
    组队机制仍为ocl传统的draft制, 更为具体的其他细则将在不久后于赛群发出
    比赛推荐8000rank及以上, 不足8000rank仍可报名, 但需参加qualifier, 第一轮NM1难度为6.3左右

    赛群: 331774490
    Forum页: https://osu.ppy.sh/community/forums/topics/1620575?n=1

    上届OCLBmainsheet: 
    https://docs.google.com/spreadsheets/d/1jbKCT-BHfJZEvIKXBOUev1YbG7t11cCp8O4Pz8IhDJg/edit#gid=1932996510

    报名链接: https://forms.gle/WBRZHj7tgTLSXxgn9

    本消息实际上为高科技自动发送, 如果有打扰到您, 请回复TD退订
    '''


    start_handle(msg, rankings)
