import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.
    Returns:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for the city with input validation.
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input("\nWhich city would you like to explore? (Chicago, New York City, Washington)?\n").lower()
        if city in cities:
            break
        else:
            print("\nInvalid city. Please try again.")

    # Get user input for the month with input validation.
    while True:
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
        month = input("\nWhich month would you like to filter by? (January, February, March, April, May, June). Type 'all' for no month filter.\n").title()
        if month in months:
            break
        else:
            print("\nInvalid month. Please try again.")

    # Get user input for the day of the week with input validation.
    while True:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
        day = input("\nWhich day would you like to filter by? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday). Type 'all' for no day filter.\n").title()
        if day in days:
            break
        else:
            print("\nInvalid day. Please try again.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    Returns:
    df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # Convert the start time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of the week, and hour from start time to create new columns.
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

    if month != 'All':
        # Filter by month to create the new dataframe.
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'All':
        # Filter by day of the week to create the new dataframe.
        df = df[df['Day of Week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nMost Common Times of Travel...\n')
    start_time = time.time()

    # Display the most common month.
    common_month = df['Month'].mode()[0]
    print('Most Common Month:', common_month)

    # Display the most common day of the week.
    common_day = df['Day of Week'].mode()[0]
    print('Most Common Day of the Week:', common_day)

    # Display the most common start hour.
    common_hour = df['Hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nMost Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', common_start_station)

    # Display most commonly used end station.
    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', common_end_station)

    # Display most frequent combination of start station and end station trip.
    df['Station Combination'] = df['Start Station'] + ', ' + df['End Station']
    common_start_end_station = df['Station Combination'].mode()[0]
    print('Most Frequent Combination of Start Station and End Station Trips:', common_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0

    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
        if view_data != 'yes':
            break

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nTrip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    # Display mean travel time.
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nUser Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:', user_types)

    # Display counts of gender.
    if 'Gender' not in df:
        print('Sorry! Gender data unavailable for Washington')
    else:
        print('The genders are \n{}'.format(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth.
    if 'Birth Year' not in df:
        print('Sorry! Birth year data unavailable for Washington')
    else:
        earliest_year = df['Birth Year'].min()
        print('Earliest Year of Birth:', int(earliest_year))

        most_recent_year = df['Birth Year'].max()
        print('Most Recent Year of Birth:', int(most_recent_year))

        common_year = df['Birth Year'].mode()[0]
        print('Most Common Year of Birth:', int(common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter y for yes or any key for no.\n')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()
