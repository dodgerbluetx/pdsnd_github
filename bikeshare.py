#!/opt/local/anaconda3/bin/python3

# added project into git repo for tracking

import time
import pandas as pd
import numpy as np
import datetime
from colorama import Fore, Back, Style

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str)  city - name of the city to analyze
        (str)  month - name of the month to filter by, or "all" to apply no month filter
        (str)  day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    city_good = 'n'
    while city_good == 'n':
        city = input("Enter the name of the city to analyze (Chicago, New York City, Washington): ").lower()
        if city in cities:
            print(Fore.GREEN + '{} it is!'.format(city.capitalize()) + Style.RESET_ALL)
            print()
            city_good = 'y'
        else:
            print(Fore.RED + 'Error! "{}" is not a valid entry, please try again!'.format(city) + Style.RESET_ALL)
            print()
            city_good = 'n'

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month_good = 'n'
    while month_good == 'n':
        month = input("Enter the month to analyze (All, January, February, March, April, May, June): ").lower()
        if month in months:
            print(Fore.GREEN + '{} it is!'.format(month.capitalize()) + Style.RESET_ALL)
            print()
            month_good = 'y'
        else:
            print(Fore.RED + 'Error! "{}" is not a valid entry, please try again!'.format(month) + Style.RESET_ALL)
            print()
            month_good = 'n'

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    day_good = 'n'
    while day_good == 'n':
        day = input("Enter the day of the week to analyze (All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday): ").lower()
        if day in days:
            print(Fore.GREEN + '{} it is!'.format(day.capitalize()) + Style.RESET_ALL)
            print()
            day_good = 'y'
        else:
            print(Fore.RED + 'Error! "{}" is not a valid entry, please try again!'.format(day) + Style.RESET_ALL)
            print()
            day_good = 'n'

    print('='*70)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday']

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("The most frequent month is {}."
        .format(months[popular_month].capitalize()))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most frequent day of the week for is {}."
        .format(popular_day.capitalize()))

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most frequent start hour is {}:00.".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*70)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular start station is {}.".format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most popular end station is {}.".format(popular_end_station))

    # TO DO: display most frequent combination of start station and end
    # station trip
    # create a concatenated column first
    df['station_combo'] = df['Start Station'] + ',' + df['End Station']
    popular_station_combo = df['station_combo'].mode()[0]
    combo_start, combo_end = popular_station_combo.split(',')
    print("The most popular start/end station combination is {}/{}."
        .format(combo_start, combo_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*70)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    duration_string = str(datetime.timedelta(seconds=int(total_duration)))
    duration_string = duration_string.replace(' ', '').replace('days', '')
    duration_days, duration_time = duration_string.split(',')
    duration_hours, duration_minutes, duration_seconds = duration_time.split(':')

    print('The total trip duration is {} days, {} hours, {} minutes, {} seconds.'
        .format(format(int(duration_days), ","), duration_hours, duration_minutes,
        duration_seconds))

    # TO DO: display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print("The mean trip duration is {} seconds.".format(mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*70)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts().to_string(header=None)
    print('User Types:\n{}\n'.format(user_types))

    # TO DO: Display counts of gender
    # first see if the gender column is in the dataframe, we know that it will
    # not be for washington city
    if 'Gender' in df.columns:
        user_genders = df['Gender'].value_counts().to_string(header=None)
    else:
        user_genders = "User gender data is not available for this city!"

    print('User Genders:\n{}\n'.format(user_genders))

    # TO DO: Display earliest, most recent, and most common year of birth
    # also check for birth year column as again we know it does not exist in
    # washington data set.
    if 'Birth Year' in df.columns:
        print("Earliest Birth Year: {}".format(int(df['Birth Year'].min())))
        print("Most Recent Birth Year: {}".format(int(df['Birth Year'].max())))
        print("Most Common Birth Year: {}".format(int(df['Birth Year'].mode())))
    else:
        print("Birth year data is not available for this city!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*70)


def raw_data(df):
    """
        Dump 5 lines of raw data per user request.
        Continue in a loop displaying more data until the user responds
        with "no"
    """

    print()
    first_ask = ''
    while first_ask != 'yes' and first_ask != 'no':
        first_ask = input("Would you like to view the raw bikeshare data? [yes/no]: \n").lower()

    if first_ask == 'yes':
        first_row = 1
        last_row = 6
        print(df[first_row:last_row])
        print()

        second_ask = ''
        while second_ask != 'no':
            second_ask = input("Would you like to view 5 more rows of raw data? [yes/no]: \n").lower()

            if second_ask == 'yes':
                first_row += 5
                last_row += 5
                print(df[first_row:last_row])
                print()
            elif second_ask == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

        #break

if __name__ == "__main__":
	main()
