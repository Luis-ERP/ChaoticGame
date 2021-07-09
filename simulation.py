import time, math, random, csv
from statistics import mean



def create_id():
	return int(round(time.time() * 1000)) * random.randint(1,10)


class Card:
	def __init__(self, cost, type):
		self.id = create_id()
		self.type = type
		self.cost = cost
		self.destroyed = False

	def __str__(self):
		return self.type

	def destroy(self):
		self.cost = 0
		self.destroyed = True

	def split(self):
		cost = self.cost
		if cost >= 2:
			cost = company.transaction_fee(cost)
		self.cost = cost / 2
		new_card = Card(cost / 2, self.type)
		return new_card

	def merge(self, card):
		if card.type == self.type:
			self.cost += card.cost
			card.destroy()



class PlayerAccount:
	def __init__(self, company):
		self.id = create_id()
		self.cards = []
		self.cash = 0

	def __str__(self):
		return f'{self.id} (${int(self.get_player_worth())}, #Cards:{len(self.cards)})'

	def add_cards(self, cards_list):
		for card in cards_list:
			self.cards.append(card)

	def remove_card(self, card_id):
		for i, card in enumerate(self.cards):
			if card_id == card.id:
				ans = card 
				del self.cards[i]
				return ans

	def sell_card(self, card_id):
		card = None
		index = None
		for i, c in enumerate(self.cards):
			if c.id == card_id:
				card = c 
				index = i
		if not card:
			return False
		new_cost = company.transaction_fee(card.cost)
		self.cash += new_cost
		card.destroy()
		del self.cards[i]

	def add_cash(self):
		amount = random.randint(int(self.cash*.1+5), int(self.cash*5+5))
		new_amount = company.transaction_fee(amount)
		self.cash += new_amount

	def split_card(self):
		cards = self.get_cards_by_worth()
		if len(cards) > 0:
			card = cards[-1].split()
			self.cards.append(card)

	def get_player_worth(self):
		return self.cash + sum([card.cost for card in self.cards])

	def get_cards_by_worth(self):
		return self.cards

	def get_cards_str(self):
		return list(str(card) for card in self.cards)

	def find_card_index(self, card_id):
		for i, card in enumerate(self.cards):
			if card.id == card_id:
				return i



class Company:
	def __init__(self, cash, cards):
		self.total_cash = cash
		self.players = []
		self.cards = cards

	def create_card(self, cost, type):
		if self.total_cash < cost:
			return False
		card = Card(cost, type)
		self.total_cash -= cost
		return card

	def transaction_fee(self, amount):
		self.total_cash += amount * .2
		return amount * .9

	def new_player(self):
		if self.total_cash < 50:
			return False
		new_player = PlayerAccount(self)
		cards = [self.create_card(self.cards[0][1], self.cards[0][0]) for i in range(1)]
		new_player.add_cards(cards)
		self.players.append(new_player)
		return True

	def transfer_card(self, from_player1, to_player2, card_id):
		card = from_player1.remove_card(card_id)
		to_player2.add_cards([card])

	def get_total_cards(self):
		cards = []
		for p in self.players:
			for c in p.cards:
				cards.append(c)

	def buy_card(self, player, cost, type):
		if player.cash < cost:
			return False
		new_cash = self.transaction_fee(cost)
		self.total_cash += new_cash
		card = self.create_card(new_cash, type)
		player.add_cards([card])
		player.cash -= cost





# ----------------------- GAME -----------------------
def print_table_row(operation, involved_p1, involved_p2):
	total_cards = []
	company_cash = round(company.total_cash)
	players_cash = []
	players_cards = []
	for p in company.players:
		for card in p.cards:
			players_cash.append(card.cost)
		players_cards.append(len(p.cards))
	total = company_cash + sum(players_cash)


	string = f'\t{round(total)}\t \
					{round(company_cash)}\t \
					{round(sum(players_cash))}\t \
					{len(company.players)}\t \
					{len(players_cash)}\t \
					{operation}'
	list_ = (total,					# SystemCash
			company_cash,			# CompanyCash
			sum(players_cash),		# PlayersCash
			len(company.players),	# Nu.Players
			len(players_cash),		# Nu.Cards
			operation,				# Operation
			str(involved_p1),		# InvolvedP1
			str(involved_p2),		# InvolvedP2
			mean(players_cash),		# Avg.PlayersCash
			mean(players_cards),	# Avg.PlayersCards
			)

	return string, list_


def gamble(p1, p2, gambed_p1, gambed_p2):
	players = list(zip([p1, p2], [gambed_p1, gambed_p2]))
	random.shuffle(players)
	company.transfer_card(players[0][0], players[1][0], players[0][1].id)


def get_card_type():
	probabilities = []
	for card_type in card_types:
		if not card_type[1]: continue
		for c in range(int(1 / card_type[1] * 1000)):
			probabilities.append(card_type)
	return random.choice(probabilities)





card_types = [
	("type1", 0),
	("type2", 10),
	("type3", 50),
	("type4", 1050),
]





if __name__ == '__main__':

	company = Company(10000, card_types)

	for i in range(100):
		company.new_player()

	movements = []

	# Movements symulation
	for i in range(20000):
		operation = ""
		# player 1
		player = random.choice(company.players)
		p1_cards = player.get_cards_by_worth()
		decision = random.randint(1,20)
		# player 2
		player2 = ""

		if player.cash <= 0:
			player.add_cash()
			operation = "cash added to account"

		elif decision in [1,2,3]:
			type_buy, cost_buy = get_card_type()
			if len(p1_cards) > 0 and cost_buy > player.cash:
				operation = f"sell card (${p1_cards[0].cost}) & "
				player.sell_card(p1_cards[0].id)
			company.buy_card(player, cost_buy, type_buy)
			operation += "buy card"

		elif decision in [4]:
			player.add_cash()
			operation = "cash added to account"

		elif decision in [5]:
			company.new_player()
			operation = "added new player"

		elif decision in [6,7]:
			player.split_card()
			operation = "split card"

		else:
			player2 = random.choice(company.players)
			p2_cards = player2.get_cards_by_worth()
			if len(p1_cards) > 0 and len(p2_cards) > 0:
				gamble(player, player2, p1_cards[0], p2_cards[0])
			operation = "played round"

		# show results
		string, list_ =  print_table_row(operation, player, player2)
		# print(string)
		movements.append(list_)



	print(company.total_cash)



	with open('results.csv', 'w', newline='') as f:
		wr = csv.writer(f)
		wr.writerow(['SystemCash', 'CompanyCash', 'PlayersCash', 
					'Nu.Players', 'Nu.Cards', 'Operation' , 
					'InvolvedP1', 'InvolvedP2', 'Avg.PlayersCash', 'Avg.PlayersCards'])	
		for row in movements:
			wr.writerow(row)

