import random
import copy
from collections import deque
import requests
import time


TRIES = 20
HIGHEST_VALUATION = 10
HOTEL_COUNT = 12
END = 1680
OVERNIGHT_STAYS = 4
TRAVEL_LENGTH_DAILY = 360

multiple_tries = False
random_hotels = False
print_all_hotels = False


class Hotel:

    def __init__(self, time_needed, valuation):
        self.time_needed = time_needed
        self.valuation = valuation


def get_hotels_from_website():
    url = 'https://bwinf.de/fileadmin/user_upload/hotels1.txt'
    result = requests.get(url)
    doc = result.content.decode("utf-8").split()
    HOTEL_COUNT = int(doc[0])
    END = int(doc[1])
    doc = doc[2:]
    hotels = []
    for line in range(0, len(doc), 2):
        hotels.append(Hotel(int(doc[line]), float(doc[line + 1])))
    return hotels

def make_random_hotels():
    hotels = []
    for hotel in range(HOTEL_COUNT):
            hotels.append(Hotel(random.randint(1,END), random.randint(1,HIGHEST_VALUATION)))
    return hotels

def give_reachable(current_time, hotels):
    if current_time + TRAVEL_LENGTH_DAILY >= END:
        return True
    reachable = []
    for hotel in hotels:
        if current_time <hotel.time_needed <= current_time + TRAVEL_LENGTH_DAILY:
            reachable.append(hotel)
    reachable.sort(reverse = True, key = lambda hotel : hotel.valuation)
    return reachable #returns reachable hotels if END is reachable returns True

def path_finder(current_hotel=None, stays=0, path=[], current_path=deque([]), best_lowest_valuation=0, current_best_lowest_valuation=HIGHEST_VALUATION + 1):
    if current_hotel is  None:
        reachable = give_reachable(0, hotels)
    else:
        current_path = copy.deepcopy(current_path)
        current_path.append(current_hotel)
        stays += 1
        if current_best_lowest_valuation > current_hotel.valuation:
            current_best_lowest_valuation = current_hotel.valuation
        reachable = give_reachable(current_hotel.time_needed, hotels)
    if reachable == True:
        return current_best_lowest_valuation, current_path
    if not reachable or stays >= OVERNIGHT_STAYS:
        return best_lowest_valuation, path
    for hotel in reachable:
        END_unreachable = hotel.time_needed + TRAVEL_LENGTH_DAILY * (OVERNIGHT_STAYS + 1 - stays) < END
        if best_lowest_valuation >= hotel.valuation or END_unreachable:
           continue 
        best_lowest_valuation, path = path_finder(hotel, stays, path, current_path, best_lowest_valuation, current_best_lowest_valuation)
    return best_lowest_valuation, path

def main():
    global hotels
    if multiple_tries:
        all_tries_best_lowest_valuation = 0
        total_time = 0
        for i in range(TRIES):
            if random_hotels:
                hotels = make_random_hotels()
            else:
                hotels = get_hotels_from_website()
            start = time.time()
            best_lowest_valuation, path = path_finder()
            end = time.time()
            total_time += end - start
            all_tries_best_lowest_valuation += best_lowest_valuation
        print(f'average best lowest valuation: {all_tries_best_lowest_valuation / TRIES}')
        print(f'average time: {total_time / TRIES}')
    else:
        if random_hotels:
            hotels = make_random_hotels()
        else:
            hotels = get_hotels_from_website()
        start = time.time()
        best_lowest_valuation, path = path_finder()
        end = time.time()
        if print_all_hotels:
            print('These were the hotels:')
            for hotel in hotels:
                print(f'{hotel.time_needed}min {hotel.valuation}')
        print(f'This was your daily travel length: {TRAVEL_LENGTH_DAILY}min.')
        print(f'This was the amount of stays you wanted to make: {OVERNIGHT_STAYS}.')
        print(f'The whole route took {END}min.')
        if path:
            print('This is your path: ')
            for hotel in path:
                print(f'{hotel.time_needed}min {hotel.valuation}')
            print(f'It has the best lowest valuation of {best_lowest_valuation}.')
        else:
            print('there is no path')
        print(f'The programm took {end - start}')

if __name__=='__main__':
    main()
