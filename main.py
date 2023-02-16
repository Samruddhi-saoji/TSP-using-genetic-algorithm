from Genetic_algo import GeneticAlgorithm
from TSP import TSP
from random import random


#randomly generate the cities
n = 13 #number of cities
cities = []
max_dist = 1000
for i in range(n) :
    tup = (max_dist*random(), max_dist*random(), i+1) #(x, y, name)
    cities.append(tup)

'''n = 16
cities = [(947.3612445509046 , 872.9585107695043, 1), (942.8609024631703 , 151.5408509461057, 2), (944.7317526958012 , 123.33296895218825, 3), (212.57740899784116 , 653.9571002434129, 4), (188.3908379453012 , 349.25288255239786, 5), (209.70695797968696 , 286.9696061099798, 6), (275.8040347314483 , 17.565098727461482, 7), (406.7735035187862 , 20.57622842965612, 8), (853.7323446491461 , 123.48985777584132, 9), (867.7433164109344 , 311.98198704313063, 10), (962.0845394904624 , 447.4731786842732, 11), (593.2445091792242 , 408.3265323472042, 12), (569.3824107564518 , 485.2592895044864, 13), (364.56046603040005 , 732.5706121326565, 14), (118.60599689859053 , 883.4367479820525, 15), (129.40647626991887 , 965.4524857132357, 16)]'''

#the TSP problem
tsp = TSP(n, cities)

#the genetic algorithm
#hyper parameters
epochs = 10000
pop_size = 20
N = 2 #elitism rate
tournament_size = 3
crossover_rate = 0.3
mutation_rate = 0.1

algo = GeneticAlgorithm(tsp, epochs, n, pop_size, N , tournament_size, crossover_rate , mutation_rate )
algo.run()
