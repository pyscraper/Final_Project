from random import choice, randint
import random
import math
import csv
import matplotlib.pyplot as plt


# Define the class player
class player:
    name=''
    FG_3PCT = 0
    stamina = 0
    onfire = 0
    variance = 0


    def __init__(self,attr_list,bonus=1,strategy=0):
        self.name = attr_list[0]
        self.FG_3PCT=eval(attr_list[1])
        self.stamina= eval(attr_list[2])
        self.onfire = eval(attr_list[3])
        self.variance=eval(attr_list[4])
        self.bonus = bonus
        self.strategy = strategy


    def get_score(self):
        """
        simulate the score based on the shooting percetage of the player
        :param FG_3PCT: shooting percentage of a player
        :return score: the simulated score of the player
        """
        score=0
        onfire = self.onfire
        lefttime = 60.0
        for i in range(25):
            shoot = random.randint(1,100)
            runtime = self.runtime(i)
            shootingtime = self.shootingtime(i, lefttime)
            # run out of time
            if lefttime<shootingtime:
                break
            # making shot
            elif shoot <= self.FG_3PCT * (1-self.stamina/100*(i)) \
                                       * math.log2(min(2.5,(0.5*shootingtime+1))) \
                                       + self.variance * self.get_onfire(onfire):
                # Moneyball spot
                if i in range(self.bonus * 5 - 4, self.bonus * 5 + 1):
                    score += 2
                    onfire += 5
                else:
                    score += 1
                    onfire += 5
            # fail to make the shot
            else:
                onfire -= 3
            # time deduction
            lefttime -= shootingtime + runtime

        return score

    def get_onfire(self, onfire):
        """
        define the if a player is in onfire_mode for each shoot.
        :param onfire: adding to the basic probability to turn on-fire state
        :return: onfire_mode: 1 means player is in onfire_mode can increase their shooting %
        and 0 means player is not in the onfire_mode, and there's no shooing % increase
        """
        prob = random.randint(1,100)
        if prob <= onfire:
            onfire_mode = 1
        else:
            onfire_mode = 0
        return onfire_mode

    def runtime(self, i):
        """
        simulate the time to run between each shooting spot
        :param i: the number of shoot
        :return: the simulated time spent of each run
        """
        if (i + 1) % 5 == 0 and i < 24:
            runtime = random.uniform(2, 4)
        else:
            runtime = 0
        return runtime

    def choose_strategy(self,simulation_time):
        """
        let the player simulate every possible strategy and bonus point to find out the best combination
        :param: simulation_time: The number of times of the simulation
        """
        best_bonus = 0
        best_strategy = 0
        best_score = 0.0
        for bonus in range(1,6):
            self.bonus = bonus
            for strategy in range(0,6):
                score_list = []
                self.strategy=strategy
                for r in range(simulation_time):
                    score = self.get_score()
                    score_list.append(score)
                avg_score = round((sum(score_list)/len(score_list)),2)
                print('{:5} {:12} {:15} '.format(self.bonus,self.strategy,avg_score))
                if avg_score>best_score:
                    best_score = avg_score
                    best_bonus = self.bonus
                    best_strategy=self.strategy
        self.bonus = best_bonus
        self.strategy=best_strategy
        print('\n >>> The best strategy for {} is: bonus {} and strategy {} \n >>> Average score = {} \n'.format(self.name,self.bonus,self.strategy,best_score))

    def shootingtime(self, i, lefttime):
        """
        simulate the time to shoot each ball
        :param i: the number of shoot
        :param lefttime: total time left in the game
        :return: the simulated shooting time for each shoot
        """
        shootingtime = 0
        # quick release
        if self.strategy == 0:
            shootingtime = random.uniform(1, 3)
        # high quality
        elif self.strategy == 1:
            shootingtime = random.uniform(2, 4)
        # high quality & time controlling
        elif self.strategy == 2:
            shootingtime= random.uniform(2, lefttime / (25-i))
        # focus on bonus spot
        elif self.strategy == 3:
            if i in range(self.bonus * 5 - 4, self.bonus * 5 + 1):
                shootingtime = random.uniform(3, 4)
            else:
                shootingtime = random.uniform(1, lefttime/(25-i))
        # focus on first ten shots
        elif self.strategy == 4:
            if i in range(10):
                shootingtime = random.uniform(2, 4)
            else:
                shootingtime = random.uniform(1, lefttime / (25 - i))
        # focus on last ten shots
        elif self.strategy == 5:
            if i in range(16,25):
                shootingtime = random.uniform(2, 4)
            else:
                shootingtime = random.uniform(1, lefttime / (25 - i))

        return shootingtime


def sort_dic(dic):
    """
    get the sorted game result based on the socres
    :param dic: the game result
    :return: the sorted game result
    >>> dic = {'Curry':18, 'George':13, 'Thompson':15, 'Booker':20}
    >>> sort_dic(dic)
    [('Booker', 20), ('Curry', 18), ('Thompson', 15), ('George', 13)]
    """
    return sorted(dic.items(),key = lambda item:item[1],reverse=True)


def get_game_result(player_list):
    """
    To get the result of the game based on the player list of current round.
    :param player_list: the player list of current round
    :return result: the result of the game
    """
    result = {}
    for player in player_list:
        score = player.get_score()
        result[player.name] = score
    return result


def get_next_round(candidate_number, result):
    """
    Based on the game result and the assign candidate_number to choose the candidate for next round
    :param candidate_number: how many candidates can advance to next round
    :param result: the game result with the players' scores
    :return: the candidate list for next round
    """
    next_round_candidate = {}
    next_round_candidate_list = []
    # set the threshold for next round candidate
    threshold = sort_dic(result)[candidate_number-1][1]

    for key, value in result.items():
        if value >= threshold:
            next_round_candidate[key] = value
    for player in player_list:
        if player.name in next_round_candidate.keys():
            next_round_candidate_list.append(player)
    return next_round_candidate_list


def one_simulation(player_list):
    """
    Simulate one game
    :param player_list: player list who attend the competition
    :return: The winner of the game
    """
    over_time_flag=True
    candidate_list = get_next_round(3,get_game_result(player_list))
    candidate_list = get_next_round(1,get_game_result(candidate_list))
    while over_time_flag:
        if len(candidate_list)==1:
            over_time_flag=False
        else:
            candidate_list=get_next_round(1,get_game_result(candidate_list))

    winner = candidate_list[0].name
    return winner


if __name__ == '__main__':

    # read csv file with player data
    file = csv.reader(open('player_data.csv'))
    headers = next(file)
    player_list=[]
    for row in file:
        num = 0
        attr_list=[]
        for header in headers:
            attr_list.append(row[num])
            num+=1
        player_list.append(player(attr_list))
    # simulation one game
    print('\nOne game simulation: \n')
    # first round
    first = get_game_result(player_list)
    print('=========================')
    print("First round")
    print('=========================')
    print('Player              Score')
    print('--------------      -----')
    for key, value in first.items():
        print('{:20} {:<5}'.format(key, value))
    next_round_candidate_list = get_next_round(3, first)

    # Final round
    print('\n=========================')
    print("Final round")
    print('=========================')
    print('Player              Score')
    print('--------------      -----')
    final = get_game_result(next_round_candidate_list)
    for key, value in final.items():
        print('{:20} {:<5}'.format(key, value))

    next_round_candidate_list = get_next_round(1, final)

    # OverTime or Winner
    while len(next_round_candidate_list) != 1:
        print('\n=========================')
        print("Overtime")
        print('=========================')
        print('Player              Score')
        print('--------------      -----')
        ot = get_game_result(next_round_candidate_list)
        for key, value in ot.items():
            print('{:20} {:<5}'.format(key, value))
        next_round_candidate_list = get_next_round(1, ot)

    print('\n>>> The winner is: {}\n'.format(next_round_candidate_list[0].name))


    print('===================================\n')
    print('Strategy Detail: \n')
    for player in player_list:
        print(player.name)
        print('\nBonus     Strategy    Average Score')
        print('-----     --------    -------------')
        player.choose_strategy(1200)
    winner_list = []
    for index in range(1000):
        winner = one_simulation(player_list)
        winner_list.append(winner)
    print('\n===============================================')
    print("Ｗinning rate")
    print('===============================================')
    print('\nPlayer           Bonus   Strategy    Winning %')
    print('-------------    -----   --------    ---------')
    for player in player_list:
        print('{:15} {:6} {:10} {:10}%'.format(player.name, player.bonus, player.strategy, round(winner_list.count(player.name) / len(winner_list)*100, 2)))
        #print('(Bonus:{}, Strategy:{})'.format(player.bonus, player.strategy))

    print('\n================================================================')
    print("Ｗinning rate when Curry & Thompson apply bad bonus and strategy")
    print('================================================================')
    print('\nPlayer           Bonus   Strategy    Winning %')
    print('-------------    -----   --------    ---------')
    player_list[0].bonus = 1
    player_list[0].strategy = 5
    player_list[3].bonus = 5
    player_list[3].strategy = 1
    winner_list = []
    for index in range(1000):
        winner = one_simulation(player_list)
        winner_list.append(winner)
    for player in player_list:
        print('{:15} {:6} {:10} {:10}%'.format(player.name, player.bonus, player.strategy,
                                               round(winner_list.count(player.name) / len(winner_list) * 100, 2)))


