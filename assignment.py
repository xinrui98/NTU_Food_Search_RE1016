import pygame
from PIL import Image
import time
import pandas as pd
import xlrd
import user_experience as ux
import collections
import numpy as np


# Images are in assets directory
# DataSets are in data_set directory


# load dataset for keyword dictionary - provided
def load_stall_keywords(data_location="data_set/canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location, trim_ws=True)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    keywords = {}
    for canteen in canteens:
        keywords[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_keywords_intermediate = copy.set_index('Stall')['Keywords'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_keywords = stall_keywords_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        keywords[stall_canteen][stall] = stall_keywords

    return keywords


# load dataset for price dictionary - provided
def load_stall_prices(data_location="data_set/canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location, trim_ws=True)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    prices = {}
    for canteen in canteens:
        prices[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_prices_intermediate = copy.set_index('Stall')['Price'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_price = stall_prices_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        prices[stall_canteen][stall] = stall_price

    return prices


# load dataset for location dictionary - provided
def load_canteen_location(data_location="data_set/canteens.xlsx"):
    # get list of canteens
    canteen_data = pd.read_excel(data_location, trim_ws=True)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    # get dictionary of {canteen:[x,y],}
    canteen_locations = {}
    for canteen in canteens:
        copy = canteen_data.copy()
        copy.drop_duplicates(subset="Canteen", inplace=True)
        canteen_locations_intermediate = copy.set_index('Canteen')['Location'].to_dict()
    for canteen in canteens:
        canteen_locations[canteen] = [int(canteen_locations_intermediate[canteen].split(',')[0]),
                                      int(canteen_locations_intermediate[canteen].split(',')[1])]

    return canteen_locations


# get user's location with the use of PyGame - provided
def get_user_location_interface():
    # get image dimensions
    image_location = 'assets/NTUcampus.jpg'
    pin_location = 'assets/pin.png'
    screen_title = "NTU Map"
    image = Image.open(image_location)
    image_width_original, image_height_original = image.size
    scaled_width = image_width_original
    scaled_height = image_height_original
    pinIm = pygame.image.load(pin_location)
    pinIm_scaled = pygame.transform.scale(pinIm, (60, 60))
    # initialize pygame
    pygame.init()
    # set screen height and width to that of the image
    screen = pygame.display.set_mode([image_width_original, image_height_original])
    # set title of screen
    pygame.display.set_caption(screen_title)
    # read image file and rescale it to the window size
    screenIm = pygame.image.load(image_location)

    # add the image over the screen object
    screen.blit(screenIm, (0, 0))
    # will update the contents of the entire display window
    pygame.display.flip()

    # loop for the whole interface remain active
    while True:
        # checking if input detected
        pygame.event.pump()
        event = pygame.event.wait()
        # closing the window
        if event.type == pygame.QUIT:
            pygame.display.quit()
            mouseX_scaled = None
            mouseY_scaled = None
            break
        # resizing the window
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(screenIm, event.dict['size']), (0, 0))
            scaled_height = event.dict['h']
            scaled_width = event.dict['w']
            pygame.display.flip()
        # getting coordinate
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get outputs of Mouseclick event handler
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # paste pin on correct position
            screen.blit(pinIm_scaled, (mouseX - 25, mouseY - 45))
            pygame.display.flip()
            # return coordinates to original scale
            mouseX_scaled = int(mouseX * 1000 / scaled_width)
            mouseY_scaled = int(mouseY * 800 / scaled_height)
            # delay to prevent message box from dropping down
            time.sleep(0.2)
            break

    pygame.quit()
    pygame.init()
    return mouseX_scaled, mouseY_scaled


# Keyword-based Search Function - to be implemented
def search_by_keyword(user_input_keywords):
    # that returns all food stall listed in the database

    # split the keywords into individual words using an array
    individual_keywords_array = user_input_keywords.split()

    # shows how many relevant searches appear
    total_keywords_appearances = 0

    foodcourt_foodstall_dict = {}
    food_court_name_list = []
    food_stall_name_list = []
    food_stall_info_list = []

    for canteen, info in canteen_stall_keywords.items():
        # print("\nCANTEEN:", canteen)
        for key in info:

            for individual_word in individual_keywords_array:

                # check if each individual keyword is in foodstall's name
                if individual_word in key:
                    total_keywords_appearances += 1
                    # updating foodcourt_foodstall_dict
                    # foodcourt_foodstall_dict.update({key: canteen})

                    # updating the arrays for foodcourt name and foodstall name
                    food_court_name_list.append(canteen)
                    food_stall_name_list.append(key)
                    food_stall_info_list.append(info[key])

                    print("CANTEEN: " + canteen + " || ", end="")
                    print("FOOD STALL: " + key)

                # check if keyword is in foodstall's description
                elif individual_word in info[key]:
                    total_keywords_appearances += 1
                    # updating foodcourt_foodstall_dict
                    # foodcourt_foodstall_dict.update({key: canteen})

                    # updating the arrays for foodcourt name and foodstall name
                    food_court_name_list.append(canteen)
                    food_stall_name_list.append(key)
                    food_stall_info_list.append(info[key])

                    print("CANTEEN: " + canteen + "|| ", end="")
                    print("FOOD STALL: " + key)

    print("Food Stalls found: " + str(total_keywords_appearances))

    # print(foodcourt_foodstall_dict)

    # print(food_court_name_list)
    # print(food_stall_name_list)

    no_repeats_food_court_name_list = food_court_name_list.copy()
    no_repeats_food_stall_name_list = food_stall_name_list.copy()
    no_repeats_food_stall_info_list = food_stall_info_list.copy()

    # check for repeats in food stall names and remove them from original list of food stalls and food canteens
    repeated_food_stall_name_dict = check_for_repeats(food_stall_name_list, 2)

    for key_repeated_food_stall in repeated_food_stall_name_dict:
        for j in range(len(no_repeats_food_stall_name_list)):
            if food_stall_name_list[j] == key_repeated_food_stall:
                no_repeats_food_court_name_list[j] = None
                no_repeats_food_stall_name_list[j] = None
                no_repeats_food_stall_info_list[j] = None

    # for repeated_food_stall_name_key in repeated_food_stall_name_dict:
    #     if repeated_food_stall_name_key in food_stall_name_list:
    #         no_repeats_food_stall_name_list.remove(repeated_food_stall_name_key)
    #         # get the index repeated food stall in order to remove the corresponding element in food court list
    #         # to do this, use list.index(element)
    #         repeated_index = food_stall_name_list.index(repeated_food_stall_name_key)
    #         no_repeats_food_court_name_list.pop(repeated_index)

    print("og list")
    print(food_stall_name_list)
    print("########################################################################################################")
    print("Food that only fufils one of the keywords")
    print(no_repeats_food_court_name_list)
    print(no_repeats_food_stall_name_list)
    print(no_repeats_food_stall_info_list)
    print(get_count_by_not_counting_none(no_repeats_food_court_name_list))
    print("########################################################################################################")
    print(repeated_food_stall_name_dict)


def check_for_repeats(food_list, number_of_repeats):
    repeated_food_dict = {}

    while number_of_repeats > 1:
        # repeats = [
        #     item
        for item, count in collections.Counter(food_list).items():
            if count == number_of_repeats:
                repeated_food_dict.update({item: count})
        number_of_repeats -= 1

    return repeated_food_dict


def get_count_by_not_counting_none(food_list):
    total_count = 0
    for i in range(len(food_list)):
        if food_list[i] == None:
            pass
        else:
            total_count += 1
    return total_count


# Price-based Search Function - to be implemented
def search_by_price(keywords):
    pass


# Location-based Search Function - to be implemented
def search_nearest_canteens(user_locations, k):
    pass


# Any additional function to assist search criteria

# Main Python Program Template
# dictionary data structures
canteen_stall_keywords = load_stall_keywords("data_set/canteens.xlsx")
canteen_stall_prices = load_stall_prices("data_set/canteens.xlsx")
canteen_locations = load_canteen_location("data_set/canteens.xlsx")


# main program template - provided
def main():
    loop = True

    while loop:
        print("=======================")
        print("F&B Recommendation Menu")
        print("1 -- Display Data")
        print("2 -- Keyword-based Search")
        print("3 -- Price-based Search")
        print("4 -- Location-based Search")
        print("5 -- Exit Program")
        print("=======================")
        option = int(input("Enter option [1-5]: "))

        if option == 1:
            # print provided dictionary data structures

            # testing ux function
            ux.error_handler()

            print("1 -- Display Data")
            print("Keyword Dictionary: ", canteen_stall_keywords)
            print("Price Dictionary: ", canteen_stall_prices)
            print("Location Dictionary: ", canteen_locations)
        elif option == 2:
            # keyword-based search
            print("Keyword-based Search")
            user_input_keywords = input("Hello, please input intended keywords, e.g. Western Chicken")
            search_by_keyword(user_input_keywords)
            # call keyword-based search function
            # search_by_keyword(keywords)

        elif option == 3:
            # price-based search
            print("Price-based Search")

            # call price-based search function
            # search_by_price(keywords)
        elif option == 4:
            # location-based search
            print("Location-based Search")

            # call PyGame function to get two users' locations
            userA_location = get_user_location_interface()
            print("User A's location (x, y): ", userA_location)
            userB_location = get_user_location_interface()
            print("User B's location (x, y): ", userB_location)

            # call location-based search function
            # search_nearest_canteens(user_locations, k)
        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False


main()
