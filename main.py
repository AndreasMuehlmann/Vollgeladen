import random
import copy
TRIES = 10000
HIGHEST_VALUATION = 10
HOTEL_COUNT = 20
END = 20
OVERNIGHT_STAYS = 4
TRAVEL_LENGTH_DAILY = 6
multiple_tries = False


class Hotel:
    def __init__(self):
        self.time_needed = random.randint(1,END - 1)
        self.valuation = random.randint(1,HIGHEST_VALUATION)


def make_random_hotels():
    hotels = []
    for hotel in range(HOTEL_COUNT):
        hotels.append(Hotel())
    return hotels

def give_reachable(current_time, hotels):
    if current_time + TRAVEL_LENGTH_DAILY >= END:
        return True
    reachable = []
    for hotel in hotels:
        if current_time <hotel.time_needed <= current_time + 6:
            reachable.append(hotel)
    return reachable #returns reachable hotels if END is reachable returns True

def path_finder(current_hotel=None, stays=0, path=[], current_path=[], best_lowest_valuation=0, current_best_lowest_valuation=HIGHEST_VALUATION + 1):
    if current_hotel is  None:
        reachable = give_reachable(0, hotels)
    else:
        current_path = copy.deepcopy(current_path)
        current_path.append(current_hotel)
        stays += 1
        if current_best_lowest_valuation > current_hotel.valuation:
            current_best_lowest_valuation = current_hotel.valuation
        reachable = give_reachable(current_hotel.time_needed, hotels)
    if best_lowest_valuation >= current_best_lowest_valuation:
        return best_lowest_valuation, path
    if reachable == True:
        return current_best_lowest_valuation, current_path
    if not reachable or stays >= OVERNIGHT_STAYS:
        return best_lowest_valuation, path
    for hotel in reachable:
        best_lowest_valuation, path = path_finder(hotel, stays, path, current_path, best_lowest_valuation, current_best_lowest_valuation)
    return best_lowest_valuation, path

def main():
    global hotels
    if multiple_tries:
        all_tries_best_lowest_valuation = 0
        for i in range(TRIES):
            hotels = make_random_hotels()
            best_lowest_valuation, path = path_finder()
            all_tries_best_lowest_valuation += best_lowest_valuation
        print(f'{all_tries_best_lowest_valuation / TRIES}')
    else:
        hotels = make_random_hotels()
        best_lowest_valuation, path = path_finder()
        print('These were the hotels:')
        for hotel in hotels:
            print(f'{hotel.time_needed}h {hotel.valuation}')
        print(f'This was your daily travel length: {TRAVEL_LENGTH_DAILY}h.')
        print(f'This was the amount of stays you wanted to make: {OVERNIGHT_STAYS}.')
        print(f'The whole route took {END}h.')
        if path:
            print('This is your path: ')
            for hotel in path:
                print(f'{hotel.time_needed}h {hotel.valuation}')
            print(f'It has the best lowest valuation of {best_lowest_valuation}.')
        else:
            print('there is no path')

if __name__=='__main__':
    main()
