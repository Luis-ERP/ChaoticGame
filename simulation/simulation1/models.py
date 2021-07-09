from django.db import models

# Create your models here.


class Player(models.Model):
    experience = models.IntegerField()
    cash = models.FloatField()

    def to_dict(self):
        return {
            'id': self.id,
            'experience': self.experience,
            'cash': self.cash,
            'cards': [card.to_dict() for card in self.cards.all()]
        }


class Card(models.Model):
    value = models.FloatField()
    name = models.CharField(max_length=140)
    owner = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='cards', null=True, default=None)
    type = models.CharField(max_length=140)

    def to_dict(self):
        return {
            'value': self.value,
            'name': self.name,
            'id': self.id
        }


class CashCard(Card):
    TYPES = (
        ('0', 'blue'),
        ('1', 'green'),
        ('10', 'yellow'),
        ('100', 'orange'),
        ('500', 'purple'),
        ('1000', 'red'),
        ('10000', 'black'),
    )
    type = models.CharField(max_length=120, choices=TYPES)


class Hero(models.Model):
    TYPES = (
            ('0', 'light'),
            ('1', 'dark'),
            ('2', 'fire'),
            ('3', 'water'),
            ('4', 'earth'),
            ('5', 'air'),
    )
    type = models.CharField(max_length=120, choices=TYPES)
    attack1 = models.IntegerField(default=5)
    defense1 = models.IntegerField(default=5)
    speed = models.IntegerField(default=5)

    def get_price(self):
        return self.attack1 + self.defense1 + self.speed

    def to_dict(self):
        return {
            'type': self.type,
            'attack1': self.attack1,
            'defense1': self.defense1,
            'speed': self.speed
        }


class HeroCard(Card):
    hero = models.ForeignKey(
        Hero, on_delete=models.CASCADE, related_name='cards')
    level = models.IntegerField()

    def get_power_points(self):
        return self.attack1*self.level + self.defense1*self.level + self.speed

    def to_dict(self):
        return {
            'value': self.value,
            'name': self.name,
            'id': self.id,
            'hero': self.hero.to_dict(),
            'level': self.level
        }


class Dungeon(models.Model):
    pass


class DungeonCard(Card):
    dungeon = models.ForeignKey(
        Dungeon, on_delete=models.CASCADE, related_name='cards')


class MagicCard:
    pass
