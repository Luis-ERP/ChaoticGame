import requests
import cv2
import random
import asyncio
import json

r = requests.get('url.com')
r.text


class NewPlayer(Thread):
	def __init__(self, *args, **kwargs):
		stats = json.dumps(self.create_player())
		self.cash = stats['cash']
		self.id = stats['id']

	def create_player(self):
		r = requests.get('http://127.0.0.0:8000/game/player/new')
		return r.text

	def update(self, new_player_data):
		if 'message' in new_player_data:
			return
		self.cash = new_player_data['cash']


async def add_cash(player):
	amount = random.randint(
		int(player[0].cash*.1+5), int(player[0].cash*5+5))
	response = get_request(f'game/player/{player[0].id}/addcash?amount={amount}')

async def buy_card(player):
	response = get_request(f'game/player/{player[0].id_player}/buycard?price={int(player[0].cash*.3)}')
	player[0].update(response)

async def retreive_cash(player):
	response = get_request(
		f'game/player/{player[0].id_player}/retreivecash')
	player[0].update(response)

async def play_round(player):
	response = get_request(
		f'game/player/{player[0].id_player}/play')
	player[0].update(response)

async def player_game():
	player = [NewPlayer()]
	while True:
		decision = random.choice(list(range(0, 101)))

		# Add cash to account
		if player.cash == 0 or decision == 0:
			task = asyncio.create_task(add_cash(player))

		# Buy card with cash
		if decision in range(1, 8):
			task = asyncio.create_task(buy_card(player))
		
		# Retreive cash from game
		if decision in range(8, 20):
			task = asyncio.create_task(retreive_cash(player))
			
		# Play round
		if decision in range(20, 101):
			task = asyncio.create_task(retreive_cash(player))
			


def get_request(path):
	r = requests.get(f'http://127.0.0.0:8000/{path}')
	return json.dumps(r.text)


if __name__ == '__main__':
	while True:
		asyncio.run(player_game())
