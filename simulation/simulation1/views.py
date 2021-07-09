from django.shortcuts import render
from .models import *
import random

from django.http import JsonResponse

"""
DA RULES:

# General simulation
- spawn new player every 10 iterations

# Player
- add player
- delete player
- actions:
	° do nothing
	° gamble with other player
	° buy card
	° sell card
	° add cash to account
	° retreive cash from account

# House
- set retreiving fee
- actions:
	° create card
	° transfer card
	° delete card
"""


def create_player(request):
    new_player = Player(experience=0, cash=0.0)
    new_player.save()
    for i in range(5):
        hero = Hero.objects.get(id=i+1)
        new_card = HeroCard(type='hero', hero=hero, level=1,
                            value=0, name='Basic card', owner=new_player)
        new_card.save()
    return JsonResponse(new_player.to_dict())


def stats(request):
    return JsonResponse({})


players = Player.objects.all()


def play_round(request):
    id_player1 = request.GET['id_player']
    player1 = Player.objects.get(pk=id_player1)
    if not list(player1.cards.all()):
        return JsonResponse({'message': 'not valid'})
    p1_card = random.choice(list(player1.cards.all().filter(type='hero')))
    # Plays againts other player
    if random.random() > 0.39:
        player2 = random.choice(players)
        while not list(player2.cards.all().filter(type='hero')):
            player2 = random.choice(players)
        p2_card = random.choice(list(player2.cards.all().filter(type='hero')))
        if p1_card.get_power_points() > p2_card.get_power_points():
            p2_card.owner = player1
            p2_card.save()
        elif p1_card.get_power_points() < p2_card.get_power_points():
            p1_card.owner = player2
            p2_card.save()
        else:
            p1_card.owner = None
            p2_card.owner = None
    # Plays againts the house
    else:
        if random.random() > 0.75:
            p2_card = random.choice(
                list(HeroCard.objects.all().filter(owner=None)))
            p2_card.owner = player1
            p2_card.save()
        else:
            p1_card.owner = None
            p1_card.save()
    player1 = Player.objects.get(pk=id_player1)
    return JsonResponse(player1)


def buy_card(request, price):
    player = Player.objects.get(pk=request.GET['id_player'])
    if player.cash < price:
        return JsonResponse({'message': 'Invalid transaction.'})
    for hero in Hero.objects.all():
        if hero.get_price() == price:
            new_card = HeroCard(type='hero', hero=hero, level=1,
                                value=price, name='Card', owner=player)
            new_card.save()
            return JsonResponse(new_card.to_dict())


def sell_card(request, id_card):
    card = Card.objects.get(pk=id_card)
    card.owner = None
    card.save()
    player = Player.objects.get(pk=request.GET['id_player'])
    player.cash += card.value
    player.save()
    return JsonResponse(player.to_dict())


def add_cash_to_account(request, amount):
    player = Player.objects.get(pk=request.GET['id_player'])
    player.cash += amount
    return JsonResponse(player.to_dict())


def retreive_cash_from_account(request, amount):
    player = Player.objects.get(pk=request.GET['id_player'])
    if player.cash < amount * 1.1:
        return JsonResponse({'message': 'Invalid transaction'})
    player.cash -= amount * 1.1
    return JsonResponse(player.to_dict())


def create_card(request):
    pass


def transfer_card(request):
    pass


def delete_card(request):
    pass
