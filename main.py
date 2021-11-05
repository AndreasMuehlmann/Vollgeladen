import copy
from dataclasses import dataclass
import requests

TRIES = 20
HIGHEST_VALUATION = 10
HOTEL_COUNT = 12
END = 1680
OVERNIGHT_STAYS = 4
TRAVEL_LENGTH_DAILY = 360

multiple_tries = False
random_hotels = False
should_print_all_hotels = False

@dataclass()
class Hotel:
    time_needed : int
    valuation : float


def get_hotels_from_website(url):
    result = requests.get(url)
    doc = result.content.decode("utf-8").split()
    doc = doc[2:]
    hotels = []
    for line in range(0, len(doc), 2):
        hotels.append(Hotel(int(doc[line]), float(doc[line + 1])))
    return hotels

def give_reachable(current_time, hotels):
    if current_time + TRAVEL_LENGTH_DAILY >= END:
        return True
    reachable = []
    for hotel in hotels:
        if current_time < hotel.time_needed <= current_time + TRAVEL_LENGTH_DAILY:
            reachable.append(hotel)
    reachable.sort(reverse = True, key = lambda hotel : hotel.valuation)
    return reachable #returns reachable hotels/empty list, if END is reachable returns True

def path_finder(current_hotel=None, stays=0, path=[], # finds path through hotels with the best lowest valuation
current_path=[], best_lowest_valuation=0, current_best_lowest_valuation=HIGHEST_VALUATION + 1):
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

def write_path_to_file(path, file):
    file.write('The path with the best lowest valuation:\n\n')
    for hotel in path:
        file.write(f'Hotel at time  {hotel.time_needed}min, valuation  {hotel.valuation}\n')
    file.write('\n')

def main():
    global hotels
    for task in range(1, 6):
        with open(f'vollgeladen_results.txt{task}', 'w') as file:
            file.write('Vollgeladen\n\n')
            file.write(f'Test {task}\n\n')
            hotels = get_hotels_from_website(f'https://bwinf.de/fileadmin/user_upload/hotels{task}.txt')
            best_lowest_valuation, path = path_finder()
            if path:
                write_path_to_file(path, file)
                file.write(f'It has the best lowest valuation of {best_lowest_valuation}.\n')
            else:
                file.write('there is no path\n')

if __name__=='__main__':
    main()