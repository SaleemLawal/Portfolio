"""
File:         metro_lines.py
Author:       Saleem Lawal
Date:         5/06/2022
E-mail:       slawal1@umbc.edu
Description:  A program that create stations, trains, and connect the stations by lines.
              This code will create a trip planner which will tell a user how to get from one station to another.
"""

EXIT = "exit"
FOUR = 4
TWO = 2
THREE = 3
FIVE = 5


def run_metro_system(system_name):
    """
    :param system_name: Generic name for the city/map
    """
    increment = 0
    print(f"[{system_name}]", end=" ")
    user_input = input(">>> ")
    stations_names = dict()
    id_lst = {}

    while user_input != EXIT:
        if "create station" in user_input:
            create_station(stations_names, user_input)
        elif "connect stations" in user_input:
            connect_station(stations_names, user_input)
        elif "plan trip" in user_input:
            history = []
            user_input = user_input.split()
            if len(user_input) == FOUR:
                start, dest = user_input[TWO], user_input[THREE]
                visited_list_reset(stations_names)
                visited_stations = plan_trip(start, dest, stations_names, id_lst, history)
                # reverse list
                reverse_history = []
                for i in range(len(history), -1, -1):
                    if i < len(history):
                        reverse_history.append(history[i])
                output(reverse_history, visited_stations, dest, increment)
        elif "create train" in user_input:
            create_train(stations_names, user_input, id_lst)
        elif "display stations" in user_input:
            for i in stations_names:
                print(f"       {i}")
        elif "display trains" in user_input:
            display_trains(id_lst)
        elif "get station info" in user_input:
            station_info(stations_names, user_input)
        elif "get train info" in user_input:
            train_info(id_lst, user_input)
        else:
            print(f"Unknown command {user_input}")
        print(f"[{system_name}]", end=" ")
        user_input = input(">>> ")


def create_station(stations_names, user_input):
    """
    :param stations_names: individual stations that user inputted to be created
    :param user_input: User un-split input
    """
    stations = user_input.split()
    # assigns the last index to a key in a dictionary of stations
    if stations[-1] in stations_names.keys():
        print(f"Station with the name {user_input[-1]} already exists.")
    else:
        if len(stations) == THREE:
            stations_names[stations[-1]] = {"connections": [], "visited": False}
        else:
            print(f"invalid format")


def connect_station(stations_names, user_input):
    """
    :param stations_names: dictionary containing station names and their aspects
    :param user_input: User un-split input that will be split to get specific information
    :return:
    """
    # creates a connection between lines
    connect = user_input.split()
    if len(connect) == FIVE:
        first_station, second_station, line_name = connect[TWO], connect[THREE], connect[FOUR]
        if first_station not in stations_names.keys():
            print(f"    {first_station} is not in the list of stations.")
        elif second_station not in stations_names.keys():
            print(f"    {second_station} is not in the list of stations.")
        else:
            stations_names[first_station]["connections"].append([second_station, line_name])
            stations_names[second_station]["connections"].append([first_station, line_name])


def plan_trip(start, dest, stations_names, id_lst, history):
    """
    :param start: start station
    :param dest: destination station
    :param stations_names: dictionary containing stations and their connections
    :param id_lst: train ids and connections
    :param history: visited stations
    :return: recursive function returns stations that were visited
    """
    if start not in stations_names.keys():
        print(f"{start} is not in the list of stations.")
    elif dest not in stations_names.keys():
        print(f"{dest} is not in the list of stations.")

    if start and dest in stations_names.keys():
        if start == dest:
            return [dest]
        stations_names[start]['visited'] = True

        for inner in stations_names[start]["connections"]:
            connections = inner[0]
            if not stations_names[connections]['visited']:
                # calls this function again as long as that station isn't visited
                # which is known through the "visited" boolean
                plan = plan_trip(connections, dest, stations_names, id_lst, history)
                if plan:
                    # append places visited to a list
                    if inner[1] not in history:
                        history.append(inner[1])
                    return [start] + plan

        return []


def visited_list_reset(stations):
    """
    :param stations: dictionary of stations, contains connections and visited boolean
    """
    # resets the boolean in the station list dictionary
    for individual in stations:
        stations[individual]["visited"] = False


def create_train(stations_names, user_input, id_lst):
    """
    :param stations_names: dictionary of stations, contains connections and visited boolean
    :param user_input: user input that will be split to get information
    :param id_lst: dictionary of stations and their train ID
    """
    # create a train with inputs such as train ID, line name, and starting station
    user_input = user_input.split()
    if len(user_input) == FIVE:
        user_input = [user_input[-THREE], user_input[-TWO], user_input[-1]]
        if user_input[TWO] not in stations_names.keys():
            print(f"    {user_input[TWO]} isn't a station")
        elif user_input[0] not in id_lst.keys():
            id_lst[user_input[0]] = [user_input[1], user_input[TWO]]
        elif user_input[0] in id_lst:
            print(f"    Train with the id {user_input[0]} already exists.")


def display_trains(id_lst):
    """
    :param id_lst: dictionary of stations and their train ID
    """
    for i in id_lst:
        print(f"*** Information for Train {i} ***")
        print(f"      line: {id_lst[i][0]}")
        print(f"      Current Position: {id_lst[i][1]}")


def station_info(stations_names, user_input):
    """
    :param stations_names: dictionary of stations, contains connections and visited boolean
    :param user_input: user input that will be split to get information
    """
    # prints out specific station information
    user_input = user_input.split()
    station = user_input[THREE]
    if len(user_input) == FOUR:
        if station in stations_names.keys():
            print(f"*** Information for Station {station} ***")
            for connection_info in stations_names[station]["connections"]:
                print(f"    {connection_info[1]} Line - Next Station: {connection_info[0]}")
        else:
            print(f"Unable to find station: {station}")


def train_info(id_lst, user_input):
    """
    :param id_lst: dictionary of stations and their train ID
    :param user_input: info that will be split to get information required
    """
    # prints out specific trains information
    user_input = user_input.split()
    train = user_input[THREE]
    if len(user_input) == FOUR:
        if train in id_lst.keys():
            print(f"*** Information for Train {train} ***")
            print(f"    Line: {id_lst[train][0]}")
            print(f"    Current Position: {id_lst[train][1]}")
        else:
            print(f"Unable to find train: {train}")


def output(line_history, station_visited, dest, increment):
    """
    :param line_history: history of lines visited
    :param station_visited: history o station visited
    :param dest: Ending stop
    :param increment: used to move along line visited list
    """
    # computes the final output detailing the movements in steps
    if line_history:
        print(f"start on the {line_history[0]}", end=" ")

        if len(line_history) == 1:
            for station in station_visited:
                print(f"--> {station}", end=" ")
            print()
        else:
            prev_line = line_history[0]
            for line in line_history:
                if station_visited[increment] != dest:
                    print(f"--> {station_visited[increment]}", end=" ")
                    increment += 1
                if prev_line != line:
                    print(f"--> transfer from {prev_line} line to {line} line", end=" ")
                    prev_line = line
            print(f"--> {dest}")


if __name__ == '__main__':
    metro_system_name = input('>>> ')
    run_metro_system(metro_system_name)
