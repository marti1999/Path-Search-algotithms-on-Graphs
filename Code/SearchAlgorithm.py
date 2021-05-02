# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1563587'
__group__ = 'DM.18'

from operator import itemgetter, attrgetter, methodcaller

# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2016- 2017
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy
from operator import attrgetter

def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """

    path_list = []
    nearbyStations = map.connections[path.route[-1]]  # using path.last won't work

    for s in list(nearbyStations.keys()):
        newPath = copy.deepcopy(path)
        newPath.add_route(s)
        # newPath.route.append(s)
        path_list.append(newPath)

    return path_list

def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """

    noDuplicates = [path for path in path_list if len(path.route) == len(set(path.route))]
    return noDuplicates

def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """

    return expand_paths + list_of_path

def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    stations = [Path([origin_id])]

    while stations[0].route[-1] != destination_id and len(stations) != 0:
        exp = expand(stations[0], map)
        dlt = remove_cycles(exp)
        stations = insert_depth_first_search(dlt, stations[1:])

    if not stations:
        return "No existeix Solucio"
    else:
        return stations[0]

def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """

    return list_of_path + expand_paths

def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    stations = [Path([origin_id])]

    while stations[0].route[-1] != destination_id and len(stations) != 0:
        exp = expand(stations[0], map)
        dlt = remove_cycles(exp)
        stations = insert_breadth_first_search(dlt, stations[1:])

    if not stations:
        return "No existeix Solucio"
    else:
        return stations[0]

def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency (increase by 1)
                                1 - minimum Time (there's a dictionary with time values)
                                2 - minimum Distance (inside map.stations there's the speed)
                                3 - minimum Transfers (Transfers means changing lines, inside map class we well)
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """

    for path in expand_paths:
        if type_preference==0:
            path.update_g(1)
            continue
        if type_preference==1:
            path.update_g(map.connections[path.route[-1]][path.route[-2]])
            continue
        if type_preference==2:
            if map.stations[path.route[-1]]["line"] == map.stations[path.route[-2]]["line"]:
                time = map.connections[path.route[-2]][path.route[-1]]
                speed = map.stations[path.route[-2]]["velocity"]
                distance = time * speed
                path.update_g(distance)
            else:
                path.update_g(0)
            continue

        if type_preference==3:
            if map.stations[path.route[-1]]["line"] != map.stations[path.route[-2]]["line"]:
                path.update_g(1)


    return expand_paths

def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    # return (sorted(expand_paths+list_of_path, key=attrgetter('g')))
    return sorted(expand_paths+list_of_path, key=lambda x: x.g)

def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    stations = [Path([origin_id])]

    while stations[0].route[-1] != destination_id and len(stations) != 0:
        exp = expand(stations[0], map)
        dlt = remove_cycles(exp)
        cost = calculate_cost(dlt, map, type_preference)
        stations = insert_cost(cost, stations[1:])

    if not stations:
        return "No existeix Solucio"
    else:
        return stations[0]

def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """

    for path in expand_paths:
        if type_preference==0:
            if  path.route[-1] != destination_id:
                path.update_h(1)
            else:
                path.update_h(0)
            continue
        if type_preference==1:
            currentCoord = [map.stations[path.route[-1]]['x'], map.stations[path.route[-1]]['y']]
            destCoord = [map.stations[destination_id]['x'], map.stations[destination_id]['y']]

            x = destCoord[0] - currentCoord[0]
            y = destCoord[1] - currentCoord[1]
            dist = math.sqrt(x * x + y * y)
            maxSpeed = max(map.velocity.values())
            path.update_h(dist/maxSpeed)
            continue
        if type_preference==2:
            currentCoord = [map.stations[path.route[-1]]['x'], map.stations[path.route[-1]]['y']]
            destCoord = [map.stations[destination_id]['x'], map.stations[destination_id]['y']]

            x = destCoord[0] - currentCoord[0]
            y = destCoord[1] - currentCoord[1]
            dist = math.sqrt(x*x + y*y)
            path.update_h(dist)

           # if map.stations[path.route[-1]]["line"] != map.stations[path.route[-2]]["line"]:
              #  path.update_g(-1) # TODO ask Ali why I have to do this

            continue

        if type_preference==3:
            if map.stations[path.route[-1]]["line"] != map.stations[path.route[-2]]["line"]:
                path.update_h(1)
            else:
                path.update_h(0)

    return expand_paths

def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """

    for path in expand_paths:
        path.update_f()

    return expand_paths

def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g in this moment, we should remove this path.
      If cost is equal, DO NOT remove
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
    """

    for path in expand_paths:
        if path.route[-1] in visited_stations_cost: # already visited
            if path.g < visited_stations_cost[path.route[-1]]: # new cost is better, removing old path
                list_of_path = remove_path_by_last_station(list_of_path, path.route[-1])
                visited_stations_cost[path.route[-1]] = path.g
            else: # new cost is worse, removing new path
                expand_paths = remove_path_by_last_station(expand_paths, path.route[-1])
        else: # not visited yet
            visited_stations_cost[path.route[-1]] = path.g

    return expand_paths, list_of_path, visited_stations_cost

def remove_path_by_last_station(list_of_path, index):
    return [path for path in list_of_path if path.route[-1] != index ]

def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    # newList = updateLastAttribute(expand_paths + list_of_path)
    # newList2 = (sorted(newList, key=attrgetter('last'), reverse=True))
    # newList3 =  (sorted(newList2, key=attrgetter('f')))
    # return newList3
    return (sorted(expand_paths+list_of_path, key=attrgetter('f')))

def coord2station(coord, map):
    """
        From coordinates, it searches the closest station.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """

    minimum = INF
    nearby = []

    for key, value in map.stations.items():
        dist = math.hypot(value['x'] - coord[0], value['y'] - coord[1])
        if dist <= minimum:
            if dist < minimum:
                nearby.clear()
            nearby.append(key)
            minimum = dist

    return nearby

def Astar(origin_coor, dest_coor, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (list): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    origin_id = coord2station(origin_coor, map)[0]
    destination_id = coord2station(dest_coor, map)[0]

    stations = [Path([origin_id])]
    visitedStationsCost = {}

    while stations[0].route[-1] != destination_id and len(stations) != 0:
        exp = expand(stations[0], map)
        dlt = remove_cycles(exp)
        cost = calculate_cost(dlt, map, type_preference)
        costHeuristic = calculate_heuristics(cost, map, destination_id, type_preference)
        expandWithF = update_f(costHeuristic)
        costNoRedundant, stations, visitedStationsCost = remove_redundant_paths(expandWithF, stations, visitedStationsCost)
        if type_preference == 3:
            #more information on why i'm doing this at the very end of the file
            costNoRedundant.reverse()

        stations = insert_cost_f(costNoRedundant, stations[1:])

    if not stations:
        return "No existeix Solucio"
    else:
        return stations[0]

def updateAttributeLast(paths):
    """
    I would have created a getter, but this is the only file we are to deliver.
    """
    for p in paths:
        p.last = p.route[-1]
    return paths


""""
Astar issue (check the function for reference).
I already sent you an email with the "problem" I came up with.
Long story short, when there are two possible paths, say [3, 2, 10, 11, 12, 13, 14] and [3, 2, 5, 6, 7, 8, 13, 14] (both having equal cost, heuristica and so),
the testCases expect me to return the first one. However, [3,2,5] comes first to the head than [3,2,10], and so the found path is the one starting by [3,2,5,...].
That's the reason why I need to reverse them.
"""
