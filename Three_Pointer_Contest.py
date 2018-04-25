from random import choice, randint
import random
import math
import csv
import matplotlib.pyplot as plt
class player():
    name=''
    _3PG = 0
    stamina = 0
    on_fire_prob = 0
    growing = 1
    def __init__(self,attr_list,bonus=1,strategy=5):
        self.name = attr_list[0]
        self._3PG=eval(attr_list[1])
        self.stamina= eval(attr_list[2])
        self.on_fire_prob = eval(attr_list[3])
        self.growing=eval(attr_list[4])
        self.bonus = bonus
        self.strategy = strategy

    def _3pointer_contest(self):
        """
        simulate the score based on the shooting percetage of the player
        :param _3PG: shooting percentage of a player
        :return: the simulated score of the player
        """
        score=0
        offset = 0
        state=0
        lefttime = 60.0
        for i in range(25):
            shoot = random.randint(1,100)
            runtime = self.runtime(i)
            shootingtime = self.shootingtime(i, lefttime)
            if lefttime<shootingtime:
                shootingtime=lefttime
            if lefttime <= 0:
                break
            elif i in range(self.bonus*5-4 ,self.bonus*5+1):
                if shoot<=(self._3PG*(1-self.stamina/100*(i))*math.log2(min(2.5,(0.5*shootingtime+1))))+state:
                    score+=2
                    offset+=10
                else:
                    offset-=6
            else:
                if shoot<=(self._3PG*(1-self.stamina/100*(i))*math.log2(min(2.5,(0.5*shootingtime+1))))+state:
                    score+=1
                    offset+=10
                else:
                    offset-=6
            state = self.get_on_fire_state(offset)
            lefttime -= shootingtime + runtime
        return score


    def get_on_fire_state(self,offset):
        """
        define the state of a player for every shoot.
        :param offset: the offset adding to the basic probability to turn on-fire state
        :return: state: whether the state is on-fire of not
        """
        prob = random.randint(1,100)
        if prob<(self.on_fire_prob+offset):
            state = self.growing
            #print(self.name+ " is onfire")
        else:
            state= 0
        return state

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
        best_score = 0
        for bonus in range(1,6):
            self.bonus = bonus
            for strategy in range(1,6):
                avg_score = 0
                score_list = []
                self.strategy=strategy
                for round in range(simulation_time):
                    score = self._3pointer_contest()
                    score_list.append(score)
                avg_score = sum(score_list)/len(score_list)
                #print('The average score with bonus {} and strategy {} is: {} '.format(self.bonus,self.strategy,avg_score))
                if avg_score>best_score:
                    best_score = avg_score
                    best_bonus = self.bonus
                    best_strategy=self.strategy
        self.bonus = best_bonus
        self.strategy=best_strategy
        print('The final stratgy {} applied is: bonus {} and strategy {} with the average score of {}'.format(self.name,self.bonus,self.strategy,best_score))


    def shootingtime(self, i, lefttime):
        """
        simulate the time to shoot each ball
        :param i: the number of shoot
        :param lefttime: total time left in the game
        :return: the simulated shooting time for each shoot
        """
        shootingtime = 0
        if self.strategy == 1:
            shootingtime = random.uniform(1, lefttime/(25-i))
        elif self.strategy == 2:
            if i in range(self.bonus * 5 - 4, self.bonus * 5 + 1):
                shootingtime = random.uniform(1, lefttime / (25 - i)) * 1.5
            else:
                shootingtime = random.uniform(1, lefttime/(25-i))
        elif self.strategy == 3:
            if i in range(10):
                shootingtime = random.uniform(1, lefttime / (25 - i)) * 2
            else:
                shootingtime = random.uniform(1, lefttime / (25 - i))
        elif self.strategy == 4:
            if i in range(10):
                shootingtime = random.uniform(1 / 0.8, lefttime / (25 - i)) * 0.8
            else:
                shootingtime = random.uniform(1, lefttime / (25 - i))
        elif self.strategy == 5:
            shootingtime= random.uniform(2,3)

        return shootingtime


def sort_dic(dic):
    """
    get the sorted game result based on the socres
    :param dic: the game result
    :return: the sorted game result
    """
    return sorted(dic.items(),key = lambda item:item[1],reverse=True)


def get_game_result(candidate_number,player_list):
    """
    To get the player list of next round based on the number of required candidate and the player list of current round.
    :param candidate_number: the number of required candidate
    :param player_list: the player list of current round
    :return: the player list of next round
    """
    threshold = 0
    score = 0
    result = {}
    next_round_candidate={}
    next_round_candidate_list = []
    for player in player_list:
        score = player._3pointer_contest()
        result[player.name] = score
    #print(result)
        #print('{} got {} this round!'.format(player.name, score))

    #print(result)
    #print(stat)
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
    :return: the winner of the game
    """

    over_time_flag=True
    candidate_list = get_game_result(3,player_list)
    #print('The players in the final game are:')
    candidate_list = get_game_result(1, candidate_list)
    while over_time_flag:
        if len(candidate_list)==1:
            over_time_flag=False
        else:
            #print('The players in the overtime game are:')
            #for player in candidate_list:
                #print(player[0])
            candidate_list=get_game_result(1,candidate_list)

    winner = candidate_list[0].name
    return winner

if __name__ == '__main__':
    file = csv.reader(open('player_data.csv'))
    headers = next(file)
    player_list=[]
    result = {}
    for row in file:
        num = 0
        attr_list=[]
        for header in headers:
            attr_list.append(row[num])
            num+=1
        player_list.append(player(attr_list))
    for player in player_list:
        player.choose_strategy(6000)
    winner_list = []
    for index in range(6000):
        winner = one_simulation(player_list)
        winner_list.append(winner)
    print('--------------------------------------')
    print('Winning Rate:')
    for player in player_list:
        print('The winning rate of {} is: {}'.format(player.name,
                                                     round(winner_list.count(player.name) / len(winner_list), 3)))

