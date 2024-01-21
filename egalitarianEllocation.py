
#!python3

"""
Author: Sappir Bohbot
Date: 21/01/2024

Task 3 from Economic algorithms course, Based on Erel Segal-Halevi Work, 
link to Course:https://github.com/erelsgl-at-ariel/algorithms-5784
link to code:https://github.com/erelsgl-at-ariel/algorithms-5784/blob/main/02-pareto-efficiency/code/3-leximin-sums.py
"""

import cvxpy
from itertools import combinations

'''
This function is the main function for egaliterian allocation
input:  3x5 matrix of all the valuations of the 3 players to the 5 resources (float)
return: 3x5 matrix describing  the present of resource each player gets (cvxpy.Variable())
'''
def egaliterian_allocation(valuations:list[list[float]])->list[list[cvxpy.Variable()]]:
  print_process = False
  resources_allocation = solve_allocation(valuations,print_process)
  print_players_stat(resources_allocation)
  return resources_allocation

'''Printing the players stats for each resource'''
def print_players_stat(resources_allocation: list[cvxpy.Variable()]):
  for player in range(0,3):
    player_stat = "Player "
    player_stat += f"{player} receive: "
    for resource in range(0,5):
      present = 100.0 * resources_allocation[resource][player].value.round(2)
      if present == 0:
        player_stat += "0"  
        present = 0.0
      if resource < 4:
        player_stat += f"{present}% of Resource {resource}, "
      else:
        player_stat += f"{present}% of Resource {resource}"
    print(player_stat)

def create_utilities(valuations:list[list[float]], resources:list[cvxpy.Variable()], players:list[int]):
  utilities = []             
  for i in range(0,4):
    for j in range(0,2):
      utilities.append(resources[i][players[j]]*valuations[players[j]][i])
  return utilities

'''Print the resources stats'''
def print_resource(resources:list[cvxpy.Variable()]):
    index = 0
    for resource in resources:
        if resource.value is not None:
            print("Resource_", index, ": ", resource.value.round(2))
        else:
            print("Resource_", index, ": Value not available")
        index += 1
  
def get_constraints(resources:list[cvxpy.Variable()]):
  fixed_constraints = \
      [0<=t for t in resources[0]] + [t<=1 for t in resources[0]] + \
      [0<=t for t in resources[1]] + [t<=1 for t in resources[1]] + \
      [0<=t for t in resources[2]] + [t<=1 for t in resources[2]] + \
      [0<=t for t in resources[3]] + [t<=1 for t in resources[3]] + \
      [0<=t for t in resources[4]] + [t<=1 for t in resources[4]] + \
      [sum(resources[0])==1, sum(resources[1])==1, sum(resources[2])==1,
       sum(resources[3])==1,sum(resources[4])==1]
  return fixed_constraints

def create_cvxpy_resources_variable(num_of_players:int)->list[cvxpy.Variable()]:
  resource_0 = cvxpy.Variable(num_of_players)
  resource_1 = cvxpy.Variable(num_of_players)  
  resource_2 = cvxpy.Variable(num_of_players)  
  resource_3 = cvxpy.Variable(num_of_players)  
  resource_4 = cvxpy.Variable(num_of_players)

  resources = [resource_0,resource_1,resource_2,resource_3,resource_4]
  return resources

def create_players():
    player_0 = 0    
    player_1 = 1
    player_2 = 2
    players = [player_0,player_1,player_2]
    return players

'''
Main function for solving the  allocation.
input: 1. valuations - same as egaliterian_allocation.
       2. print_process - (optional) add printing to each step of the algorithm.
return: 3x5 matrix describing  the present of resource each player gets (cvxpy.Variable()) 
'''
def solve_allocation(valuations:list[list[float]], print_process: bool) ->list[list[cvxpy.Variable()]]:
  num_of_players = 3
  resources = create_cvxpy_resources_variable(num_of_players)

  players = create_players()

  utilities = create_utilities(valuations, resources, players)

  fixed_constraints = get_constraints(resources)

  if print_process:
    print("\nITERATION 1: Egalitarian division")
  
  min_utility = cvxpy.Variable()    # smallest utility of a single agent
  prob = cvxpy.Problem(
      cvxpy.Maximize(min_utility),
      constraints = fixed_constraints + [min_utility <= u for u in utilities]
      )
  prob.solve(solver=cvxpy.ECOS)
  if print_process:
    print("optimal value: ", prob.value)
    print("Utilities: ", [u.value for u in utilities])
    print_resource(resources)

  if print_process:
    print("\nITERATION 2: Max the smallest sum of two:")

  min_utility_of_two = cvxpy.Variable()    
  prob = cvxpy.Problem(
      cvxpy.Maximize(min_utility_of_two),
      constraints = fixed_constraints + 
          [min_utility.value <= u for u in utilities] +
          [min_utility_of_two  <= u+v for u,v in combinations(utilities,2)]
      )
  prob.solve(solver=cvxpy.ECOS)
  if print_process:
    print("optimal value: ", prob.value)
    print("Utilities: ", [u.value for u in utilities])
    print_resource(resources)

  if print_process:
    print("\nITERATION 3: Max the smallest sum of three")

  min_utility_of_three = cvxpy.Variable()  
  prob = cvxpy.Problem(
      cvxpy.Maximize(min_utility_of_three),
      constraints = fixed_constraints + 
          [min_utility.value <= u for u in utilities] +
          [min_utility_of_two.value  <= u+v for u,v in combinations(utilities,2)] +
          [min_utility_of_three  <= u+v+w for u,v,w in combinations(utilities,3)] 
      )
  prob.solve(solver=cvxpy.ECOS)
  
  if print_process:
      print("optimal value: ", prob.value)
      print("Utilities: ", [u.value for u in utilities])
      print_resource(resources)
  return resources
