# import necessary modules

import time
import pandas as pd
import numpy as np

# define global variables

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

monthslist = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

daylist = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

citylist = ['new york city', 'washington', 'chicago']

# define functions

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('For which city do you want to calculate statistics? Chicago, New York City or Washington? \n ').lower()

    while city not in citylist:
        print('Seems your input is incorrect. Seems there is a misspelling. Please try again! \n ')
        city = input('For which city do you want to calculate statistics? Chicago, New York City or Washington? \n ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)

    month = input('For which month do you want to calculate statistics? Please enter a month between January an June! \n If you want statistics for all  months, enter "all"! \n ').lower()

    while month not in monthslist:
        print('Seems your input is incorrect. Seems there is a misspelling. Or you did not enter a month from January to June. \n  Please try again!')
        month = input('For which month do you want to calculate statistics? Please enter a month between January and June! \n  If you want statistics for all  months, enter "all" \n ').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('For which weekday do you want to calculate statistics? Please enter a single weekday!If you want statistics for all                          weekdays, enter "all" \n ').lower()

    while day not in daylist:
        print('Seems your input is incorrect. Seems there is a misspelling. Please try again!  \n ')
        day = input('For which weekday do you want to calculate statistics? Please enter a single weekday!If you want statistics for all                       weekdays, enter "All"  \n ').lower()


    print('-'*40)
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
    df['hour'] = df['Start Time'].dt.hour



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

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df.mode()['month'][0]

    # display the most common day of week
    popular_day = df.mode()['day_of_week'][0]

    # display the most common start hour
    popular_hour = df.mode()['hour'][0]

    print('Most common month:', popular_month)
    print('Most common day:', popular_day)
    print('Most common hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df.mode()['Start Station'][0]

    # display most commonly used end station
    popular_end = df.mode()['End Station'][0]

    # display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + ' - ' + df['End Station']
    popular_comb = df.mode()['Combination'][0]


    print('Most common Start Station:', popular_start)
    print('Most common End Station:', popular_end)
    print('Most common Combination:', popular_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    totaltime = df['Trip Duration'].sum()

    # display mean travel time
    meantime = df['Trip Duration'].mean()

    print('Total Travel Time:', str(totaltime) + ' min')
    print('Average Travel Time:', str(meantime) + ' min')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_statistics(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of user types: \n', user_types)
    
    if set(['Gender','Birth Year']).issubset(df.columns):
        # Display counts of gender
        gender = df['Gender'].value_counts()

        # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        most = df['Birth Year'].mode()

        print('Count of Gender: \n', gender)
        print('Earliest Birth Year:', earliest)
        print('Most recent Birth Year:', recent)
        print('Most common Birth Year:', most)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays 5 lines of raw data if users wants to see it."""
    answer = input('Would you like to see the first 5 lines of raw data? Enter "yes" or "no" \n ').lower()
    i = 0
    j = 5
    while answer == 'yes':
        print(df[i:j])
        i = i + 5
        j = j + 5
        answer = input('Would you like to see 5 more lines of raw data? Enter "yes" or "no" \n ').lower()
        if answer == 'no':
            break
        elif answer == 'yes':
            continue
        else:
            print('Seems your input is wrong. Please try again!')
            answer = input('Would you like to see 5 more lines of raw data? Enter "yes" or "no" \n ').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_statistics(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
