from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass



class AbstractObject(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def draw(self, display):
        pass


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        if hero.hp + 10 > hero.max_hp:
            hero.hp = hero.max_hp
        else:
            hero.hp += 10
            engine.score += 0.5
        self.action(engine, hero)

    def draw(self, display):
        pass


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.max_hp = self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        return 5 + self.stats["endurance"] * 2

    def draw(self, display):
        pass



class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp,  position):
        super().__init__(icon, stats, position)
        self.xp = xp


    def interact(self, engine, hero):
        if hero.stats["endurance"] > hero.stats["strength"]:
            hero_damage = hero.stats["endurance"]
        else:
            hero_damage = hero.stats["strength"]
        if self.stats["endurance"] > self.stats["strength"]:
            damage = self.stats["endurance"]
        else:
            damage = self.stats["strength"]
        print('До' + str(hero.hp))
        hero.hp -= damage
        print('После' + str(hero.hp))
        self.hp - hero_damage
        engine.notify("Hero got " + str(damage))
        engine.notify("Enemy got " + str(hero_damage))
        if hero.hp <= 0:
            engine.game_process = False
            engine.game_over = True
            engine.notify("You are dead")
            engine.notify("Game is ended")
            return False
        else:
            hero.exp += self.xp / 4
            engine.score += 1
            for it in hero.level_up():
                engine.notify(it)
            hero.stats["endurance"] += 1
            hero.stats["strength"] += 1
            hero.max_hp += 5
            return True

class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp



class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


# FIXME
# add classes

class Berserk(Effect):
    def apply_effect(self):
        self.stats['endurance'] += 7
        self.stats['strength'] += 7
        self.stats['luck'] += 7
        self.stats['intelligence'] -= 3


class Blessing(Effect):
    def apply_effect(self):
        self.stats['endurance'] += 2
        self.stats['strength'] += 2
        self.stats['luck'] += 2
        self.stats['intelligence'] += 2


class Weakness(Effect):
    def apply_effect(self):
        self.stats['endurance'] -= 4
        self.stats['strength'] -= 4
