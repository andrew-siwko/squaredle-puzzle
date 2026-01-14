import json
import requests
r=requests.get('https://squaredle.app/api/today-puzzle-config.js')
data=r.text[r.text.find('gPuzzleConfig =')+16:r.text.find('const gYesterdayWords')-2]
d=json.loads(data)
puzzle_dict=d['puzzles']
puzzle_dict={x:puzzle_dict[x] for x in puzzle_dict if '-xp' not in x}
today_key=list(puzzle_dict.keys())[0]
today_puzzle=puzzle_dict[today_key]
today_puzzle_board=[x.upper() for x in today_puzzle['board']]
puzzle_json={"puzzle_length": 12, "puzzle_text": today_puzzle_board}
with open('puzzle.json','wt') as f:
    f.write(json.dumps(puzzle_json))
