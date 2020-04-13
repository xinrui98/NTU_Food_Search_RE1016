import pygame
import math
from PIL import Image
import time
import pandas as pd
import xlrd
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
            # NOTE: replaced original scale with custom scale to improve accuracies
            # mouseX_scaled = int(mouseX * 1000 / scaled_width)
            # mouseY_scaled = int(mouseY * 800 / scaled_height)
            mouseY_scaled = int(mouseX * 1281 / scaled_width)
            mouseX_scaled = int(mouseY * 1550 / scaled_height)
            # delay to prevent message box from dropping down
            time.sleep(0.2)
            break

    pygame.quit()
    pygame.init()
    return mouseX_scaled, mouseY_scaled


# Keyword-based Search Function
def search_by_keyword(user_input_keywords, print_info_true_or_false):
    # that returns all food stall listed in the database

    # split the keywords into individual words using an array
    individual_keywords_array = user_input_keywords.split()
    number_of_keywords = len(individual_keywords_array)

    # shows how many relevant searches appear
    total_keywords_appearances = 0

    # looks something like this, [[foodcourt1, foodcourt2 etc],[foodstall1, foodstall2 etc],[info1, info2 etc]]
    list_matrix_original_food = [[], [], []]

    for canteen, info in canteen_stall_keywords.items():
        for key in info:

            for individual_word in individual_keywords_array:

                # check if keyword is in foodstall's description
                # change all to lower case for easy comparison
                if individual_word.lower() in info[key].lower():
                    total_keywords_appearances += 1

                    # updating the lists for foodcourt name and foodstall name and foodstall info
                    list_matrix_original_food[0].append(canteen)
                    list_matrix_original_food[1].append(key)
                    list_matrix_original_food[2].append(info[key])

                # # bonus function
                # # check if each individual keyword is in foodstall's name
                # # change all to lower case for easy comparison
                # elif individual_word.lower() in key.lower():
                #     total_keywords_appearances += 1
                #
                #     # updating the lists for foodcourt name and foodstall name and foodstall info
                #     list_matrix_original_food[0].append(canteen)
                #     list_matrix_original_food[1].append(key)
                #     list_matrix_original_food[2].append(info[key])

    # handling error of 0 relevant searches found, asking user to try again
    if total_keywords_appearances == 0:
        print("No food stalls found with input keyword(s), please try again")
        return False

    # trying a repeated food matrix to simplify processes
    # it looks something like this [[foodcourt1, foodcourt2 etc],[foodstall1, foodstall2 etc],[info1, info2 etc],[count1, count2 etc]]
    list_matrix_repeated_food = check_for_repeats(list_matrix_original_food[0], list_matrix_original_food[1],
                                                  list_matrix_original_food[2],
                                                  number_of_keywords)

    # updating repeated elements to NONE
    for key_repeated_food_stall in list_matrix_repeated_food[1]:
        for j in range(len(list_matrix_original_food[1])):
            if list_matrix_original_food[1][j] == key_repeated_food_stall:
                list_matrix_original_food[0][j] = None
                list_matrix_original_food[1][j] = None
                list_matrix_original_food[2][j] = None

    # trying a NO repeats food matrix to simplify processes
    # it looks something like this [[foodcourt1, foodcourt2 etc],[foodstall1, foodstall2 etc],[info1, info2 etc],[number of repeats: all values = 1]]
    list_matrix_NO_repeated_food = [remove_NONE_from_list(list_matrix_original_food[0]),
                                    remove_NONE_from_list(list_matrix_original_food[1]),
                                    remove_NONE_from_list(list_matrix_original_food[2]), []]
    list_matrix_NO_repeated_food[3] = [1 for i in range(len(list_matrix_NO_repeated_food[1]))]

    # decide whether to print info or not. I do not want to print this part when executing search_by_price function
    if print_info_true_or_false == True:
        # user output
        # Total number of relevant food stalls
        total_number_of_relevant_food_stalls = len((list_matrix_NO_repeated_food[1])) + len(
            list_matrix_repeated_food[0])
        print("\n")
        print("Total number of relevant food stalls found: " + str(total_number_of_relevant_food_stalls))
        print("\n")

        # only print output for multiple keywords if relevant
        if len(list_matrix_repeated_food[0]) > 0:

            highest_num_of_keywords = list_matrix_repeated_food[3][0]
            print("Relevant food stalls that matches " + str(highest_num_of_keywords) + " keywords: ")
            for i in range(len(list_matrix_repeated_food[0])):
                if list_matrix_repeated_food[3][i] == highest_num_of_keywords:
                    print(list_matrix_repeated_food[0][i] +
                          " - " + list_matrix_repeated_food[1][i] + " " + "| Description: " +
                          list_matrix_repeated_food[2][
                              i])

                else:
                    print("\n")
                    highest_num_of_keywords-=1
                    print("Relevant food stalls that matches " + str(highest_num_of_keywords) + " keywords: ")
            print("\n")

            # print("\n")
            # # Food stalls that matches MULTIPLE keywords
            # print("Total number of relevant food stalls that matches multiple keywords: " + str(
            #     len(list_matrix_repeated_food[0])))
            # for i in range(len((list_matrix_repeated_food)[0])):
            #     print("Number of keywords matched : " + str(list_matrix_repeated_food[3][i]) + " | " +
            #           list_matrix_repeated_food[0][i] +
            #           " - " + list_matrix_repeated_food[1][i] + " " + "| Description: " + list_matrix_repeated_food[2][
            #               i])
            # print("\n")

        # Food stalls that matches ONLY 1 keyword
        print("Relevant food stalls that matches 1 keyword: ")

        # replaced repeats with NONE, so gotta use the remove_NONE_from_list to find actual length of list and print the non-NONE elements
        for i in range(len(list_matrix_NO_repeated_food[1])):
            print(list_matrix_NO_repeated_food[0][i] + " - " +
                  list_matrix_NO_repeated_food[1][i] + " " + "| Description: " +
                  list_matrix_NO_repeated_food[2][i])

    # return all relevant searches in 1 big matrix, combining repeated and non-repeated food
    # looks something like this [[foodcourt1, foodcourt2 etc],[foodstall1, foodstall2 etc],[info1, info2 etc],[no_of_repeats1, no_of_repeats2 etc]]
    list_combined_food_details = [[], [], [], []]
    list_combined_food_details[0] = list_matrix_NO_repeated_food[0].copy()
    list_combined_food_details[1] = list_matrix_NO_repeated_food[1].copy()
    list_combined_food_details[2] = list_matrix_NO_repeated_food[2].copy()
    list_combined_food_details[3] = list_matrix_NO_repeated_food[3].copy()

    for k in range(len(list_matrix_repeated_food[0])):
        list_combined_food_details[0].append(list_matrix_repeated_food[0][k])
        list_combined_food_details[1].append(list_matrix_repeated_food[1][k])
        list_combined_food_details[2].append(list_matrix_repeated_food[2][k])
        list_combined_food_details[3].append(list_matrix_repeated_food[3][k])

    return list_combined_food_details


# Price-based Search Function - to be implemented
# add on to keywords based search

def search_by_price(user_input_keywords):
    list_matrix_search_by_keywords = search_by_keyword(user_input_keywords, False)

    # creating a matrix to store all information and price
    # it looks something like this [[foodcourt1, foodcourt2 etc],[foodstall1, foodstall2 etc],[price1, price2 etc]]
    list_matrix_all_food_prices = [[], [], []]
    for canteen, info in canteen_stall_prices.items():
        for key in info:
            list_matrix_all_food_prices[0].append(canteen)
            list_matrix_all_food_prices[1].append(key)
            list_matrix_all_food_prices[2].append(info[key])

    # creating a matrix with relevant foodstalls and their prices
    # it looks something like this [[foodcourt1, foodcourt2 etc],[foodstall1, foodstall2 etc],[info1, info2 etc],[repeats1, repeats2 etc],[price1, price2 etc]]
    list_matrix_relevant_food_prices = [[], [], [], [], []]
    # filtering the relevant food stalls by keywords and show price
    for relevant_food_stall in list_matrix_search_by_keywords[1]:
        for i in range(len(list_matrix_all_food_prices[1])):
            if relevant_food_stall == list_matrix_all_food_prices[1][i]:
                # getting the relevant food stall prices
                list_matrix_relevant_food_prices[4].append(list_matrix_all_food_prices[2][i])

    # rest of the relevant information(canteen name, food stall, number of repeats) are already known from search_by_keywords function
    list_matrix_relevant_food_prices[0] = list_matrix_search_by_keywords[0].copy()
    list_matrix_relevant_food_prices[1] = list_matrix_search_by_keywords[1].copy()
    list_matrix_relevant_food_prices[2] = list_matrix_search_by_keywords[2].copy()
    list_matrix_relevant_food_prices[3] = list_matrix_search_by_keywords[3].copy()

    # Performing bubbleSort
    # Traverse through all list elements
    list_len = len(list_matrix_relevant_food_prices[4])
    for i in range(list_len):
        # Last i elements are already in place
        for j in range(0, list_len - i - 1):

            # traverse the array from 0 to list_len-i-1
            # Swap if the element found is greater
            # than the next element
            if list_matrix_relevant_food_prices[4][j] > list_matrix_relevant_food_prices[4][j + 1]:
                list_matrix_relevant_food_prices[4][j], list_matrix_relevant_food_prices[4][j + 1] = \
                    list_matrix_relevant_food_prices[4][j + 1], list_matrix_relevant_food_prices[4][j]

                # perform corresponding rearrangement for food canteens
                list_matrix_relevant_food_prices[0][j], list_matrix_relevant_food_prices[0][j + 1] = \
                    list_matrix_relevant_food_prices[0][j + 1], list_matrix_relevant_food_prices[0][j]

                # perform corresponding rearrangement for food stalls
                list_matrix_relevant_food_prices[1][j], list_matrix_relevant_food_prices[1][j + 1] = \
                    list_matrix_relevant_food_prices[1][j + 1], list_matrix_relevant_food_prices[1][j]

                # perform corresponding rearrangement for food info
                list_matrix_relevant_food_prices[2][j], list_matrix_relevant_food_prices[2][j + 1] = \
                    list_matrix_relevant_food_prices[2][j + 1], list_matrix_relevant_food_prices[2][j]

                # perform corresponding rearrangement for number of repeats
                list_matrix_relevant_food_prices[3][j], list_matrix_relevant_food_prices[3][j + 1] = \
                    list_matrix_relevant_food_prices[3][j + 1], list_matrix_relevant_food_prices[3][j]

    # user output
    # Total number of relevant food stalls
    print("\n")
    total_number_of_relevant_food_stalls = len(list_matrix_relevant_food_prices[0])
    print("Total number of relevant food stalls found: " + str(total_number_of_relevant_food_stalls))
    print("\n")

    # printing info with lowest price to highest price
    print("Relevant searches in ascending order PRICE")
    for i in range(total_number_of_relevant_food_stalls):
        print(list_matrix_relevant_food_prices[0][i] + " - " +
              list_matrix_relevant_food_prices[1][i] + " " + "| Description: " + str(
            list_matrix_relevant_food_prices[2][i]) + " " + "| Number of relevant keywords: " + str(
            list_matrix_relevant_food_prices[3][i]) + " " + "| Price: " + str(list_matrix_relevant_food_prices[4][i]))


# Location-based Search Function - to be implemented
def search_nearest_canteens(user_locations):
    # convert canteen locations dict into a 2 row matrix
    # it looks something like this [[canteen1, canteen2 etc],[[cant1 x, cant1 y],[cant2 x, cant2 y etc]]]
    list_matrix_canteen_locations = [[], []]
    for canteen, location_info in canteen_locations.items():
        list_matrix_canteen_locations[0].append(canteen)
        list_matrix_canteen_locations[1].append(location_info)

    # handling user error
    while True:
        try:
            print("\n")
            num_of_nearest_canteens = int(input("Input the number of canteens you want to search: "))
        except ValueError:
            print("Invalid type, please try again")
            # better try again... Return to the start of the loop
            continue
        if (num_of_nearest_canteens > len(list_matrix_canteen_locations[0])):
            print("We only have " + str(len(list_matrix_canteen_locations[0])) + " canteens, please try again.")
            continue
        else:
            # success
            # we're ready to exit the loop.
            break

    # compiling the distances between user(s) location and target location into a single list
    list_of_distances_from_targets = []
    # if only 1 user location is selected
    if len(user_locations) == 1:
        # calc distance between every canteen and the 2 locations chosen by user
        # first location
        userX = user_locations[0][0]
        # print("user1x : " + str(user1X))
        userY = user_locations[0][1]
        # print("user1y : " + str(user1Y))

        for i in range(len(list_matrix_canteen_locations[0])):
            targetX = list_matrix_canteen_locations[1][i][0]
            targetY = list_matrix_canteen_locations[1][i][1]
            # print("targetX: " + str(targetX))
            # print("targetY: " + str(targetY))
            sum_of_2_distances = calc_distance(userX, userY, targetX, targetY)
            list_of_distances_from_targets.append(sum_of_2_distances)

    # if 2 user locations were selected
    elif len(user_locations) == 2:
        # calc distance between every canteen and the 2 locations chosen by user
        # first location
        user1X = user_locations[0][0]
        # print("user1x : " + str(user1X))
        user1Y = user_locations[0][1]
        # print("user1y : " + str(user1Y))

        # second location
        user2X = user_locations[1][0]
        # print("user2X : " + str(user2X))
        user2Y = user_locations[1][1]
        # print("user2Y : " + str(user2Y))

        for i in range(len(list_matrix_canteen_locations[0])):
            targetX = list_matrix_canteen_locations[1][i][0]
            targetY = list_matrix_canteen_locations[1][i][1]
            # print("targetX: " + str(targetX))
            # print("targetY: " + str(targetY))
            sum_of_2_distances = calc_distance(user1X, user1Y, targetX, targetY) + calc_distance(user2X, user2Y,
                                                                                                 targetX,
                                                                                                 targetY)
            list_of_distances_from_targets.append(sum_of_2_distances)

    # perform bubble sort for distances in ascending order
    # Traverse through all array elements
    len_list = len(list_of_distances_from_targets)
    for i in range(len_list):

        # Last i elements are already in place
        for j in range(0, len_list - i - 1):

            # traverse the array from 0 to len_list-i-1
            # Swap if the element found is greater
            # than the next element
            if list_of_distances_from_targets[j] > list_of_distances_from_targets[j + 1]:
                # sorting distances in ascending order
                list_of_distances_from_targets[j], list_of_distances_from_targets[j + 1] = \
                    list_of_distances_from_targets[j + 1], list_of_distances_from_targets[j]

                # matching the corresponding canteen names
                list_matrix_canteen_locations[0][j], list_matrix_canteen_locations[0][j + 1] = \
                    list_matrix_canteen_locations[0][j + 1], list_matrix_canteen_locations[0][j]

    print("\n")
    # printing out user input based on the number of canteens user wants
    print("Showing the nearest " + str(num_of_nearest_canteens) + " canteens to you...")
    for i in range(num_of_nearest_canteens):
        print(list_matrix_canteen_locations[0][i] + " - distance: " + str(list_of_distances_from_targets[i]))


def calc_distance(userX, userY, targetX, targetY):
    distance = math.sqrt(((userX - targetX) ** 2) + ((userY - targetY) ** 2))
    return distance


# Any additional function to assist search criteria

# returns a 4 row matrix that stores all information of repeated food stalls
def check_for_repeats(food_court_list, food_stall_list, food_stall_info_list, number_of_repeats):
    # looks something like this [[foodcourt1, foodcourt2 etc],[foodstall1, foodstall2 etc],[info1, info2 etc],[no_of_repeats1, no_of_repeats2]]
    repeated_food_4_row_matrix = [[], [], [], []]

    while number_of_repeats > 1:
        for item, count in collections.Counter(food_stall_list).items():
            if count == number_of_repeats:
                # get index of element that fufils the criteria to update canteen and food info too
                selected_index = food_stall_list.index(item)

                repeated_food_4_row_matrix[0].append(food_court_list[selected_index])
                repeated_food_4_row_matrix[1].append(food_stall_list[selected_index])
                repeated_food_4_row_matrix[2].append(food_stall_info_list[selected_index])
                repeated_food_4_row_matrix[3].append(count)

        number_of_repeats -= 1

    return repeated_food_4_row_matrix


# remove NONE values from food list to simplify it
def remove_NONE_from_list(food_list):
    return [value for value in food_list if value != None]


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

        # handling user error
        option_list = [1, 2, 3, 4, 5]
        while True:
            try:
                option = int(input("Enter option [1-5]: "))
            except ValueError:
                print("Invalid type, please try again")
                # better try again... Return to the start of the loop
                continue
            if option not in option_list:
                print("invalid input number, please try again")
                continue
            else:
                # we're ready to exit the loop.
                break

        if option == 1:
            # print provided dictionary data structures

            # testing ux function
            print("1 -- Display Data")
            print("Keyword Dictionary: ", canteen_stall_keywords)
            print("Price Dictionary: ", canteen_stall_prices)
            print("Location Dictionary: ", canteen_locations)



        elif option == 2:
            # keyword-based search
            print("Keyword-based Search")

            while True:
                try:
                    # ask for user input keywords
                    user_input_keywords = input(
                        "Please input intended keywords with appropriate spaces, e.g. Western Chicken: ")
                except ValueError:
                    print("Invalid type, please try again")
                    # better try again... Return to the start of the loop
                    continue
                if search_by_keyword(user_input_keywords, True) == False:
                    continue
                else:
                    # we're ready to exit the loop.
                    break




        elif option == 3:
            # price-based search
            print("Price-based Search")
            while True:
                try:
                    # ask for user input keywords
                    user_input_keywords = input(
                        "Please input intended keywords with appropriate spaces, e.g. Western Chicken: ")
                except ValueError:
                    print("Invalid type, please try again")
                    # better try again... Return to the start of the loop
                    continue
                else:
                    # we're ready to exit the loop.
                    break
            search_by_price(user_input_keywords)

        elif option == 4:
            # location-based search
            print("Location-based Search")

            while True:
                try:
                    num_of_locations_to_select = int(input("Do you wish to select 1 or 2 locations on the NTU map?: "))
                except ValueError:
                    print("Invalid type, please try again")
                    # better try again... Return to the start of the loop
                    continue

                if num_of_locations_to_select not in range(1, 3):
                    print("invalid input number, please try again")
                    continue

                elif num_of_locations_to_select == 1:
                    print("num of locations to select = 1")
                    # call PyGame function to get two users' locations
                    user_location = get_user_location_interface()
                    print("User's location (x, y): ", user_location)
                    user_location_list = [user_location]
                    # call location-based search function
                    search_nearest_canteens(user_location_list)
                    break

                elif num_of_locations_to_select == 2:
                    print("num of locations to select = 2")
                    # call PyGame function to get two users' locations
                    userA_location = get_user_location_interface()
                    print("User A's location (x, y): ", userA_location)
                    userB_location = get_user_location_interface()
                    print("User B's location (x, y): ", userB_location)

                    user_locations_list = [userA_location, userB_location]
                    # call location-based search function
                    search_nearest_canteens(user_locations_list)
                    break

                else:
                    # we're ready to exit the loop.
                    break



        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False


main()
