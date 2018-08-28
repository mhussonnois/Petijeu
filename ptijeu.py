import random as rd
from enum import Enum


class ItemType(Enum):
    WEAPON = 1
    ARMOR = 2
    SHIELD = 3
    UNKNOWN = 4
    POTION = 5
    BOMBE = 6

    def __str__(self):
        return self.name


class Item:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return "[name=" + self.name + ", type=" + self.type.name + "]"

    @staticmethod
    def filter_items_for_type(items, type):
        return list(filter(lambda i : i.type == type, items))


class Weapon(Item):
    def __init__(self, name, attack):
        super().__init__(name, ItemType.WEAPON)
        self.attack = attack

    def __repr__(self):
        return "[name=" + self.name + ", attack=" + str(self.attack) + " type=" + self.type.name + "]"

class Armor(Item):
    def __init__(self, name, defense):
        super().__init__(name, ItemType.ARMOR)
        self.defense = defense

    def __repr__(self):
        return "[name=" + self.name + ", defense=" + str(self.defense) + " type=" + self.type.name + "]"

class Shield(Item):
    def __init__(self, name, defense):
        super().__init__(name, ItemType.SHIELD)
        self.defense = defense

    def __repr__(self):
        return "[name=" + self.name + ", defense=" + str(self.defense) + " type=" + self.type.name + "]"

class Potion(Item):
    def __init__(self, name, PointDeVie):
        super().__init__(name, ItemType.POTION)
        self.PointDeVie = PointDeVie

    def __repr__(self):
        return "[name=" + self.name + ", PointDeVie=" + str(self.PointDeVie) + " type=" + self.type.name + "]"

class Bombe(Item):
    def __init__(self, name, PointDeVie):
        super().__init__(name, ItemType.BOMBE)
        self.PointDeVie = PointDeVie

    def __repr__(self):
        return "[name=" + self.name + ", PointDeVie=" + str(self.PointDeVie) + " type=" + self.type.name + "]"


class Personnage:
    def __init__(self,Nom,Pdv,Atq,dfs):
        self.PointDeVie=Pdv
        self.Attaque=Atq
        self.defense=dfs
        self.name=Nom
        self.berserk = False
        self.items=[]

    def is_dead (self):
        return self.PointDeVie <= 0

    def add_item(self, item):
        self.items.append(item)

    def get_armors(self):
        return Item.filter_items_for_type(self.items, ItemType.ARMOR)

    def get_weapons(self):
        return Item.filter_items_for_type(self.items, ItemType.WEAPON)

    def get_shields(self):
        return Item.filter_items_for_type(self.items, ItemType.SHIELD)
    def get_object_utilisable(self):
        return Item.filter_items_for_type(self.items, ItemType.POTION and ItemType.BOMBE)
    def get_potion(self):
        return Item.filter_items_for_type(self.items, ItemType.POTION)
    def get_bombe(self):
        return Item.filter_items_for_type(self.items, ItemType.BOMBE)
    def get_berserk(self):
        self.berserk=True
        print(self.name + " passe en mode berserker")
        return self.berserk

class Action:

    def __init__(self):
        self.board : Board = None

    def execute(self, current_player):
        pass

    def setBoard(self, board):
        self.board = board



class Attack(Action):

    def execute(self, current_player):
        target_player= self.board.select_target_for(current_player)
        dommage = target_player.defense - self.compute_attack(current_player)
        if dommage>0:
            dommage=0
        target_player.PointDeVie = target_player.PointDeVie + dommage
        print("L'attaque de " + current_player.name + " a infligé " + str(dommage) + " de dommage")
        print("il ne reste plus que " + str(target_player.PointDeVie) + " de point de vie à " + target_player.name)
        if target_player.PointDeVie < 20:
            target_player.get_berserk()

    def compute_attack(self, player) -> int:
        pass

class HandAttack(Attack):

    def compute_attack(self, player):
        d = rd.uniform(1, 2)
        if d == 2:
            print("Coup critique!")
        return player.Attaque * d

class CriticalAttack(Attack):
    def __init__(self,attack):
        self.attack=attack

    def compute_attack(self, player):
        factor = 2 if player.berserk else 1
        return self.attack.compute_attack(player) * factor

class WeaponAttack(Attack):
    def __init__(self,attack : Attack):
        self.attack=attack

    def compute_attack(self, player: Personnage):

        weapons = player.get_weapons()

        previous_attack = self.attack.compute_attack(player)

        if len(weapons) == 0:
            return previous_attack
        else:
            weapon_index = -1
            while weapon_index < 0 or weapon_index > len(weapons) :
                print("Which weapon would you like to use ?")
                print(list(enumerate(weapons)))
                weapon_index = int(input())
            return previous_attack + weapons[weapon_index].attack

class Bombeattack(Attack):


    def compute_attack(self, player):

        bombes=player.get_bombe()
        bombe_index = -1
        while bombe_index < 0 or bombe_index > len(bombes):
            print("Which bombe would you like to use ?")
            print(list(enumerate(bombes)))
            bombe_index = int(input())
        Bonus = bombes[bombe_index].defense
        idx = player.items.index(bombes[bombe_index])
        del player.items[idx]
        print(2)
        return Bonus




class Defend(Action):

    def execute(self, current_player):
        current_player.defense=self.compute_defense(current_player)
        print("ma defense est maintenant de " + str(current_player.defense))


    def compute_defense(self, player) -> int:
        pass

class BoostDefense(Defend):
    def compute_defense(self, current_player):
        return current_player.defense + 10


class ArmorDefend(Defend):
    def __init__(self,defense : Defend):
        self.defense=defense

    def compute_defense(self, player: Personnage):

        armor = player.get_armors()
        previous_defense = self.defense.compute_defense(player)

        if len(armor) == 0:
            return previous_defense
        else:
            armor_index = -1
            while armor_index < 0 or armor_index > len(armor) :
                print("Which armor would you like to use ?")
                print(list(enumerate(armor)))
                armor_index = int(input())

            Bonus = armor[armor_index].defense
            idx = player.items.index(armor[armor_index])
            del player.items[idx]
            return previous_defense + Bonus

class ShieldDefend(Defend):
    def __init__(self,defense : Defend):
        self.defense=defense

    def compute_defense(self, player: Personnage):

        shield = player.get_shields()
        previous_defense = self.defense.compute_defense(player)

        if len(shield) == 0:
            return previous_defense
        else:
            shield_index = -1
            while shield_index < 0 or shield_index > len(shield) :
                print("Which armor would you like to use ?")
                print(list(enumerate(shield)))
                shield_index = int(input())
            Bonus=shield[shield_index].defense
            idx=player.items.index(shield[shield_index])
            del player.items[idx]
            return previous_defense + Bonus

class Objet(Action):
    def execute(self, current_player):
        list_object=current_player.get_object_utilisable()
        print(list_object)
        print("Which object would you like to use ?")
        print(list(enumerate(list_object)))
        object_index=int(input())
        print(type(list_object[object_index].type))
        current_player.PointDeVie+=self.compute_pdv(current_player,list_object[object_index])

        def compute_pdv(self, player,object) -> int:
            pass

class Potion(Objet):
    def __init__(self, objet : Objet):
        self.objet=objet
    def compute_pdv(self,player, object):
        Bonus=object.PointDeVie
        del player.items[object]
        return Bonus
class Bombe(Objet):
    def __init__(self, objet : Objet):
        self.objet=objet
    def compute_pdv(self,player, object):
        Bonus=object.PointDeVie
        del player.items[object]
        return Bonus

class Exploration(Action):


    def execute(self,current_player : Personnage):
        list_items_names=self.board.list_items()
        if len(list_items_names)==0:
            print("il n'y a plus d'objet")
        else:
            idx_item=rd.randint(0,len(list_items_names)-1)
            item_name = list_items_names[idx_item]
            item=self.board.get_item_for_name(item_name)

            current_player.add_item(item)
            self.board.remove_item_for_name(item_name)
            print ("Yeah! You have found one : " + str(item))


class Board:

    def __init__(self):
        self.actions = {}
        self.players = []
        self.playersKeyedByName = {}
        self.started = False
        self.__items={}

    def add_player(self, player):
        self.__checkIsNotStarted()
        self.players.append(player)
        self.playersKeyedByName[player.name] = player

    def add_action(self, name, action: Action):
        self.__checkIsNotStarted()
        self.actions[name] = action
        action.setBoard(self)

    def add_item(self, item: Item):
        self.__items[item.name] = item

    def get_item_for_name(self, name):
        return self.__items[name]

    def list_items(self):
        return list(self.__items)

    def remove_item_for_name(self, name):
        del self.__items[name]

    def get_action_for_name(self, name):
        if not name in self.actions:
            raise ValueError("Unknown action for name " + name)
        return self.actions[name]

    def lancer_des(self):
        return rd.randint(1,6)

    def __checkIsNotStarted(self):
        if self.started:
            raise ValueError("IllegalStateError : Game is started!")

    def start(self):
        self.started = True
        self.__nextPlayerIdx = self.__get_idx_first_player()

    def __get_idx_first_player(self):
        lastDes = 0
        idx = 0
        for i in range (0, len(self.players)):
            des = self.lancer_des()
            if  des > lastDes :
                lastDes = des
                idx = i
        return idx

    def get_next_player(self):
        current = self.__nextPlayerIdx
        self.__nextPlayerIdx +=1
        return self.players[current % self.__player_size()]

    def get_list_player_names(self, player_filter_fn):
        players = self.__get_players_filtered_by(player_filter_fn)
        return list(map(lambda p: p.name, players))

    def get_list_action_name(self):
        return list(filter(lambda p: self.actions.keys(),self.actions))

    def select_target_for(self, current_player):

        print("qui veux tu attaquer?")
        print(self.get_list_player_names(lambda player: player.name != current_player.name))

        p2 = input()
        return self.playersKeyedByName[p2]

    def __get_players_filtered_by(self, player_filter_fn):
        return list(filter(player_filter_fn, self.players))

    def __player_size(self):
        return len(self.players)

    def has_winner(self):
        return len(self.__get_players_filtered_by(lambda p: not p.is_dead())) == 1

def main():


    board = Board()

    board.add_player(Personnage("Maxence", 50, 30, 10))
    board.add_player(Personnage("Flo", 100, 20, 10))

    board.add_item(Weapon("Excalibur", 30))
    board.add_item(Shield("Aegis", 30))
    board.add_item(Armor("Cerberus", 30))
    board.add_item(Item("Red Flower", ItemType.UNKNOWN))
    board.add_item(Item("Mushroom", ItemType.UNKNOWN))
    board.add_item(Potion("Potion", 50))
    board.add_item(Potion("Grosse Potion", 100))
    board.add_item(Bombe("Bombe", 40))
    board.add_item(Bombe("GrossenBombe", 80))

    board.add_action("attaquer", CriticalAttack(WeaponAttack(HandAttack())))
    board.add_action("defendre", ShieldDefend(ArmorDefend(BoostDefense())))
    board.add_action("explorer", Exploration())
    board.add_action("Objet",Objet())

    board.start()

    while not (board.has_winner()):

        current_player = board.get_next_player()

        print("A " + current_player.name + " de jouer")
        # print alls player names and select

        # find player for name
        print("que veux tu faire?")
        print(board.get_list_action_name())
        action_name = input()

        action = board.get_action_for_name(action_name)

        action.execute(current_player)



if __name__ == '__main__':
  main()
