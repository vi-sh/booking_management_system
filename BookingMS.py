# =============================================================================
#  P R O J E C T   I N F O R M A T I O N
# -----------------------------------------------------------------------------
#  Project : Flight Management System
# =============================================================================
#  F I L E   I N F O R M A T I O N
# -----------------------------------------------------------------------------
# Author         : Vishwanath Purohit
# @brief         : This is a class for handling Booking and itinerary
# =============================================================================


import os
import sys
import csv
import pandas as pd
from tabulate import tabulate
from datetime import datetime
from os.path import join, abspath

THIS_DIR = abspath(os.path.dirname(__file__))
BOOKINGS_FILE = join(THIS_DIR, 'bookings.csv')
FLIGHT_DETAILS = join(THIS_DIR, 'flight_infos.csv')


class Bookings:
    """
    Bookings class that holds the information of Passengers ,Itinerary and flight departure time
    """
    def __init__(self,name=None,departure=None,src_city=None,dest_city=None):
        self.__name = name
        self.__departure = departure
        self.__src_city = src_city
        self.__dest_city = dest_city

    # Get properties
    @property
    def get_name(self):
        return self.__name

    @property
    def get_departure(self):
        return self.__departure

    @property
    def get_src_city(self):
        return self.__src_city

    @property
    def get_dest_city(self):
        return self.__dest_city


    def __repr__(self):
        print(f"New Booking Details")
        return f"Pax name:{self.__name}\ndeparture:{self.__departure}\nItinerary:{self.__src_city}->{self.__dest_city}"


    def add_booking(self):
        """
        Adds new passenger booking 
        Input : Passenger details
        Output : Add new passenger to the Bookings csv file 
        """
        booking_data = []
        name = str(input("Enter your Name: "))
        departure = str(input('Enter date in(MMM-DD HH:MM YYYY)\nExample: may-26 6:45 2020: '))
        src_city = str(input("Enter Origin city with IATA code\nExample: AMS or LHR: ")).upper()
        dest_city = str(input("Enter Destination city with IATA code\nExample: AMS or LHR: ")).upper()
        if src_city == None:
            print("Invalid Origin")
            sys.exit(f"No flights starts from {src_city}")
        elif dest_city == None:
            print("Invalid Destination")
            sys.exit(f"No flights connected from {src_city} to {dest_city}")
        else:
            itinerary = f"{src_city}->{dest_city}"
            booking_data = [name, departure, itinerary]
            print("Do you want to add this Booking ? y/n")
            print(booking_data)
            choice = str(input())
            if choice == 'y':
                with open(BOOKINGS_FILE, 'a', encoding='UTF8', newline='') as booking_file:
                    writer = csv.writer(booking_file)
                    writer.writerow(booking_data)
                return booking_data
            else:
                sys.exit("Cancelled Booking")


    def display_all_bookings_data(self):
        """
        Displays all the Bookings information
        """
        print("|-------------------KLM Booking Details---------------|")
        global BOOKINGS_FILE
        bookings_dataframe = pd.read_csv(BOOKINGS_FILE)
        booking_headers = list(bookings_dataframe.columns.values)
        bookings_dataframe.to_html('output\\bookings.html')
        print(tabulate(bookings_dataframe, headers=booking_headers, tablefmt='fancy_grid', showindex=False))


    def get_booking_before_this_time(self):
        """
        Retrieves all the Bookings that are scheduled after the input time.
        Input : Date and Time 
        Output : Bookings detail that are occuring after given input date and time
        """
        given_time = str(input('Enter date in(MMM-DD HH:MM YYYY)\nExample: may-26 6:45 2020: '))
        print(f"Booking details before the Departure Time - {given_time} - are as follows:")
        given_time = datetime.strptime(given_time, '%b-%d %H:%M %Y')
        bookings_dataframe, booking_headers = get_csv_data_as_dataframe(BOOKINGS_FILE)
        new_df = pd.DataFrame(columns=booking_headers, dtype=object)
        for row_label, row in bookings_dataframe.iterrows():
            dep_time = datetime.strptime(row['departure'], '%b-%d %H:%M %Y')
            if given_time <= dep_time:
                new_df = new_df.append(row, ignore_index=True)
        print(tabulate(new_df, headers=booking_headers, tablefmt='fancy_grid', showindex=False))


    def get_sequential_visits_info(self):
        """
        Displays all the itinerary of given 2 sequential visiting airports.
        Input : airport 1 and airport 2
        Output : Bookings information that has itinerary of given sequentially visiting airports.
        """
        print("\nPlease refer the Flight details list above")
        from_city = str(input('Please enter 1st airport IATA code\nExample: LHR: ').upper())
        to_city = str(input('Please enter 2nd airport city IATA code\nExample: AMS: ').upper())
        print(f"Bookings visiting 2 airprots {from_city}->{to_city} sequentially is as follows:")
        bookings_dataframe, booking_headers = get_csv_data_as_dataframe(BOOKINGS_FILE)
        new_df = pd.DataFrame(columns=booking_headers, dtype=object)
        for row_label, row in bookings_dataframe.iterrows():
            itinerary_list = row['itinerary'].split('->')
            for i in range(len(itinerary_list)-1):
                if itinerary_list[i] == from_city and itinerary_list[i+1] == to_city:
                    new_df = new_df.append(row, ignore_index=True)
        print(tabulate(new_df, headers=booking_headers, tablefmt='fancy_grid', showindex=False))


    def display_flights_airport_information():
        """
        Displays flights and airport details with their IATA codes
        """
        print("|---------------------------------------------------------------------|")
        print("|                            Flight Details                           |")
        flight_details_dataframe = pd.read_csv(FLIGHT_DETAILS)
        flight_headers = list(flight_details_dataframe.columns.values)
        flight_details_dataframe.to_html('output\\flight_details.html')
        print(tabulate(flight_details_dataframe, headers=flight_headers, tablefmt='fancy_grid', showindex=False))


def main():
    """
    Main function interface that carries out interaction with User
    """
    print("|-----------------------------------------------------|")
    print("|       Welcome to KLM Airline Booking system         |")
    print("|-----------------------------------------------------|")
    print("| 1. Display all bookings                             |")
    print("| 2. Add Bookings                                     |")
    print("| 3. Get bookings departing before the given time     |")
    print("| 4. Get bookings that visits 2 airports sequentially |")
    print("| 5. Exit                                             |")
    print("|-----------------------------------------------------|")
    option = input()

    if option == '1':
        Bookings().display_all_bookings_data()
        main()
    elif option == '2':
        Bookings().add_booking()
        main()
    elif option == '3':
        Bookings().get_booking_before_this_time()
        main()
    elif option == '4':
        Bookings.display_flights_airport_information()
        Bookings().get_sequential_visits_info()
    else:
        print("Invalid entry !\nPlease try again")


def get_csv_data_as_dataframe(csv_file):
    """
    """
    l_dataframe = pd.read_csv(csv_file)
    l_headers = list(l_dataframe.columns.values)
    return l_dataframe, l_headers

if __name__ == "__main__":
    main()
