import time
#import pandas as pd
#import numpy as np
import csv
import datetime as dt
import operator
import sys
'''
Definition of a user input possibilities
'''
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = {'january':1,
          'february':2,
          'march':3,
          'april':4,
          'may':5,
          'june':6,
          'july':7,
          'august':8,
          'september':9,
          'october':10,
          'november':11,
          'december':12,
          'all':0,
          'no data':-1}
DAYS = {'monday':1,
        'tuesday':2,
        'wednesday':3,
        'thursday':4,
        'friday':5,
        'saturday':6,
        'sunday':7,
        'all':0,
        'no data':-1}
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def welcome():
    """
    Welcome the user and ask whether he wants to proceed or not.

    Returns:
        (bool) True - Proceed
        (bool) False - Quit
    """
    clear_screen()
    print("Welcome to US bikeshare data, are you ready to go?")
    exit_counter = 0
    while(True):
        response = input("Type yes or no: ")
        response = response.lower() # make response lower case for processing
        if (response == "yes" or response == "y"):
            print("Okay, let's go!")
            clear_screen()
            return True
            break
        elif(response == "no" or response == "n"):
            print("Okay, then it's time for me to go I guess.")
            return False
            break
        else:
            exit_counter += 1
            if exit_counter > 4:
                print("Okay, I don't have all day. Other customers are waiting for me. See you :)")
                break
            print("Sorry I couldn't understand you. Type 'yes' or 'y' to continue, 'no' or 'n' to quit.")
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze. (Must be specified)
        (str) month - name of the month to filter by, or "all" to proceed without filter
        (str) day - name of the day of week to filter by, or "all" to proceed without filter
    """
    #initialize variables
    city = "none"
    month = "none"
    day = "none"
    print('Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while(city == "none"):
        print('First, tell me which city you\'d like to explorer. You can choose between Chicago, New York City and Washington')
        city = input("City selection: ")
        city = check_filter('city', city, CITY_DATA)


    # get user input for month (all, january, february, ... , june)
    while(month == "none"):
        print('What about the month? You can eighter type it\'s name or the corresponding number. For the whole year, type \'all\' or 0.')
        month = input('Month selection: ')
        month = check_filter('month', month, MONTHS)


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while(day == "none"):
        print('We\'re almost done. Just give me the weekday you would like to see. You can eighter type the name or it\'s number, starting with 1 on monday.')
        print('To explorer all days just type \'all\' or 0.')
        day = input("Day selection: ")
        day = check_filter('day', day, DAYS)

    # reverse lookup integer values
    if month.isnumeric():
        month = dict_reverse(month, MONTHS)

    if day.isnumeric():
        day = dict_reverse(day, DAYS)


    print('-'*40)
    summary = "Your city is {}, your month is {}, and your weekday is {}. We are almost ready to go.".format(city.title(), month, day)
    print(summary)
    return city, month, day

def check_filter(title, input_data, dictionary):
    """
    Check if the user's input matches the possibilities given by a dictionary

    Args:
        (str) title - name of the input value, used for response print()
        (str) input_data - user's input, checked against the given dictionary
        (dict) dictionary - possible input values
    Returns:
        (str) intut_data - will be just returned as it is if allowed, or modified and returned if not inside the dictionary
    """
    input_data = input_data.lower()
    if not input_data in dictionary.keys():
        if input_data.isnumeric():
            dictlen = len(dictionary.keys()) -1
            if int(input_data) > dictlen or int(input_data) < 0 or title == "city":
                print("Sorry, I can\'t determine which " + title + " corresponds to the number you gave me. Let's retry...")
                input_data = "none"
        elif not input_data.isnumeric():
            print("Sorry, I have no data about the given " + title + ". Did you type it's whole name correctly? Let's retry...")
            input_data = "none"


    return input_data

def dict_reverse(value, dictionary):
    """
    Dictionary reverse lookup, finds the key for a given value inside a given dictionary

    Args:
        (str) value - value to find inside the dictionary
        (dict) dictionary - dict to lookup for the given value
    Returns:
        (str) d_key - key for the given value
    """
    for d_key, d_val in dictionary.items():
        if d_val == int(value):
            return d_key

def clear_screen():
    '''
    Clear the console screen to have a clean window if requiered (bug fixed for windows)
    Note: found on Stackoverflow - https://stackoverflow.com/questions/4810537/how-to-clear-the-screen-in-python
    '''
    print(chr(27)+"[2J")

class progressbar:
    """
    Shows the progress of a given function while data is being computed.

    Must be initialized and "goal" must be set before starting.
    """
    def __init__(self):
        self.__percAct = 0
        self.__percLast = 0
        self.__percGoal = 100
        self.__pgAct = 0
        self.__pgGoal = 100


    def setGoal(self, goal):
        ''' Set the maximum value the raw progress can reach '''
        self.__pgGoal = goal

    def start(self):
        ''' Print 0% before start of processing '''
        print('{}%'.format(self.__percAct),end='')

    def progress(self, actProgress):
        ''' Called while processing to indicate the progress '''
        self.__pgAct = actProgress
        self.__calc_and_print()

    def __calc_and_print(self):
        ''' Inner function to calculate the progress and print it to the user's screen '''
        self.__percAct = int(self.__pgAct * self.__percGoal / self.__pgGoal)
        if self.__percAct > self.__percLast:
            if self.__percAct % 2 == 0:
                if self.__percAct % 10 == 0:
                    print('{}%'.format(self.__percAct),end='')
                else:
                    print('=',end='')
            self.__percLast = self.__percAct

    def end(self):
        ''' Print 100% when finished processing '''
        print('{}%'.format(self.__percGoal))

    def reset(self):
        ''' reinitialize, usualy not needed '''
        self.__init__()


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
    clear_screen()
    print('Please wait while I apply your filters to the bikeshare data...')
    starttime = dt.datetime.now()
    filename = CITY_DATA.get(city)
    rentals = []
    with open(filename,'r') as datafile:
        raw_rentals = list(csv.reader(datafile,delimiter=','))
    datafile.close()
    header = raw_rentals[:1]
    header[0][0] = 'RentalId'
    act = 1
    last = len(raw_rentals) -1
    month_num = MONTHS.get(month)
    day_num = DAYS.get(day)
    #pg = progressbar()
    #pg.setGoal(last)
    #pg.start()
    print_progress(0, last, 'Progress: ', 'Complete', 1, 50)
    rentals.append(header)
    while act < last:
        #pg.progress(act)
        print_progress(act+1, last, 'Progress: ', 'Complete', 1, 50)
        actDate = dt.datetime.strptime(raw_rentals[act][1], DATE_FORMAT)
        actMonth = actDate.month
        actDay = actDate.isoweekday()
        if not month_num == 0:
            if not day_num == 0:
                if actDay == day_num and actMonth == month_num:
                    rentals.append(raw_rentals[act])
            else:
                if actMonth == month_num:
                    rentals.append(raw_rentals[act])
        else:
            if not day_num == 0:
                if actDay == day_num:
                    rentals.append(raw_rentals[act])
            else:
                rentals.append(raw_rentals[act])
        act += 1
    duration = dt.datetime.now() - starttime
    #pg.end()
    print('\nYour filtered data is now ready to analyze. This took {:.1f} seconds.\n\n'.format(duration.total_seconds()))
    print('-'*40)
    return rentals

def maxDictVal(dt):
    '''
        Finds the key with the max integer value inside a dictionary and returns it
        Note: found on Stackoverflow - https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    '''
    try:
        topKey = max(dt.items(),key=operator.itemgetter(1))[0]
    except:
        topKey = -1
    return topKey

def findColumn(value, row):
    '''
        Used to find a coulumn inside the header row, just in case it could be reordered
    '''
    i = 0
    for r in row:
        for col in r:
            if col.lower() == value.lower():
                return i
            i += 1

def time_stats(df):
    """
        Displays statistics on the most frequent times of travel.
        Note: time conversion found on Tutorialspoint - https://www.tutorialspoint.com/python/time_strptime.htm
    """
    clear_screen()
    start_time = time.time()
    #pg = progressbar()
    act = 1
    last = len(df) -1
    #pg.setGoal(last)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    #pg.start()
    print_progress(0, last, 'Progress: ', 'Complete', 1, 50)
    months = {}
    weekdays = {}
    hours = {}
    timeCol = findColumn('start time', df[0])
    # get the top times
    while act < last:
        #pg.progress(act)
        print_progress(act + 1, last, 'Progress: ', 'Complete', 1, 50)
        actDT  = dt.datetime.strptime(df[act][timeCol],DATE_FORMAT)
        actMonth = actDT.month
        actWeekday = actDT.isoweekday()
        actHour = actDT.hour
        if actMonth in months:
            months[actMonth] += 1
        else:
            months[actMonth] = 1
        if actWeekday in weekdays:
            weekdays[actWeekday] += 1
        else:
            weekdays[actWeekday] = 1
        if actHour in hours:
            hours[actHour] += 1
        else:
            hours[actHour] = 1
        act += 1
    topMonth = maxDictVal(months)
    strTopMonth = dict_reverse(topMonth, MONTHS)
    topWeekday = maxDictVal(weekdays)
    strTopWeekday = dict_reverse(topWeekday, DAYS)
    topHour = maxDictVal(hours)
    pg.end()
    print('Ready. Here are the Most Frequent Times:')
    # display the most common month
    print('Most common month: {}'.format(strTopMonth.title()))
    # display the most common day of weekday
    print('Most common weekday: {}'.format(strTopWeekday.title()))
    # display the most common start hour
    print('Most common hour: {:2d}:00'.format(topHour))

    print("\nThis took {:.2f} seconds.".format((time.time() - start_time)))
    print('-'*40)

def combine_stations(startStation, endStation):
    '''
        Combines the given start and end station to one single string
    '''
    tempList = []
    tempList.append(startStation)
    tempList.append(endStation)
    tempString = ''
    for Station in sorted(tempList):
        tempString = tempString + Station + ' / '
    tempLen = len(tempString) - 3
    tempString = tempString[:tempLen]
    return tempString

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
   # clear_screen()

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    #pg = progressbar()
    act = 1
    last = len(df) -1
    #pg.setGoal(last)
    #pg.start()
    print_progress(0, last, 'Progress: ', 'Complete', 1, 50)
    startStations = {}
    endStations = {}
    combined = {}
    iStartStation = findColumn('Start Station',df[0])
    iEndStation = findColumn('End Station', df[0])
    while act < last:
        #pg.progress(act)
        print_progress(act+1, last, 'Progress: ', 'Complete', 1, 50)
        actStart = df[act][iStartStation]
        actEnd = df[act][iEndStation]
        if actStart in startStations:
            startStations[actStart] += 1
        else:
            startStations[actStart] = 1
        if actEnd in endStations:
            endStations[actEnd] += 1
        else:
            endStations[actEnd] = 1
        combStation = combine_stations(actStart, actEnd)
        if combStation in combined:
            combined[combStation] += 1
        else:
            combined[combStation] = 1

        act += 1
    topStart = maxDictVal(startStations)
    topEnd = maxDictVal(endStations)
    topCombined= maxDictVal(combined)
    #pg.end()
    print('The station statistics are ready now. Here are the most commonly used stations:')
    # display most commonly used start station
    print('Start Station: {}'.format(topStart))
    # display most commonly used end station
    print('End Station: {}'.format(topEnd))
    # display most frequent combination of start station and end station trip
    print('Station Combination: {}'.format(topCombined))


    print("\nThis took {:.2f} seconds.".format((time.time() - start_time)))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    #clear_screen()
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    pg = progressbar()
    act = 1
    last = len(df) -1
    pg.setGoal(last)
    pg.start()
    totalSecs = 0
    iDuration = findColumn('Trip Duration', df[0])
    while act < last:
        pg.progress(act)
        actSecs = df[act][iDuration]
        totalSecs += float(actSecs)
        act += 1
    meanSecs = 0
    if last > 0:
        meanSecs = totalSecs / last
    tSec = dt.timedelta(seconds=totalSecs)
    mSec = dt.timedelta(seconds=meanSecs)
    pg.end()
    print('Time statistics are ready now. Here are some travel times:')
    # display total travel time
    print('Total travel time: {}'.format(tSec))
    # display mean travel time
    print('Mean travel time: {}'.format(mSec))

    print("\nThis took {:.2f} seconds.".format((time.time() - start_time)))
    print('-'*40)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    REFERENCE : https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def user_stats(df):
    """
    Displays statistics on bikeshare users.
    Note: Nonetype check found on Stackoverflow - https://stackoverflow.com/questions/23086383/how-to-test-nonetype-in-python
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    pg = progressbar()
    act = 1
    last = len(df) -1
    pg.setGoal(last)
    pg.start()
    Users = {}
    Genders = {}
    BirthYears = {}
    iUser = findColumn('User Type', df[0])
    iGender = findColumn('Gender', df[0])
    iBirth = findColumn('Birth Year', df[0])
    #Check for Nonetype added to avoid errors in washington where some data is missing
    CalcUser = True
    CalcGender = True
    CalcBirth = True
    if iUser is None:
        CalcUser = False
    if iGender is None:
        CalcGender = False
    if iBirth is None:
        CalcBirth = False
    while act < last:
        pg.progress(act)
        #Calc Userstats
        if CalcUser:
            actUserType = df[act][iUser]
            if actUserType in Users:
                Users[actUserType] += 1
            else:
                Users[actUserType] = 1
        #Calc Genderstats
        if CalcGender:
            actGender = df[act][iGender]
            if actGender in Genders:
                Genders[actGender] += 1
            else:
                Genders[actGender] = 1
        #Calc Year of Birth stats
        if CalcBirth:
            actBirth = df[act][iBirth]
            if actBirth in BirthYears:
                BirthYears[actBirth] += 1
            else:
                BirthYears[actBirth] = 1
        #count up for next line
        act += 1
    if CalcBirth:
        topBirth = maxDictVal(BirthYears)
        if topBirth == '':
            topBirth = 'Unknown'
        else:
            topBirth = int(topBirth)
        mostRecent = 0.0
        earliest = 999999.0
        try:
            for Year in BirthYears:
                if not Year == '':
                    if float(Year) < earliest:
                        earliest = float(Year)
                    if float(Year) > mostRecent:
                        mostRecent = float(Year)
        except:
            print('What happened? Year: {}'.format(Year))
    pg.end()
    print('User statistics are ready now. Here some user related information:')
    # Display counts of user types
    if CalcUser:
        print('Count of different user types: {}'.format(len(Users)))
        for User in Users:
            print('Type {} has {} rental entrys.'.format(User, Users[User]))
    # Display counts of gender
    if CalcGender:
        print('Count of genders: {}'.format(len(Genders)))
        for Gender in Genders:
            print('There were {} rentals from {} users.'.format(Genders[Gender], Gender))
    # Display earliest, most recent, and most common year of birth
    if CalcBirth:
        print('And a few age statistics...')
        print('Earliest year of birth: {}'.format(int(earliest)))
        print('Most recent year of birth: {}'.format(int(mostRecent)))
        print('Most common year of birth: {}'.format(topBirth))
    print("\nThis took {:.2f} seconds.".format((time.time() - start_time)))
    print('-'*40)

def printRaw(df):
    '''
        Print five raw data lines as long as the user retypes 'yes'
    '''
    showraw = input('\nWould you like to see some raw data? Enter yes or no.\n')
    actRaw = 1
    noStop = False
    if showraw.lower() == 'yes':
        noStop = True
    while noStop:
        stopRaw = actRaw + 5
        if stopRaw > len(df) -1:
            stopRaw = len(df) -1
        while actRaw < stopRaw:
            print(df[actRaw])
            actRaw += 1
        showraw = input('\nDo you want more? Enter yes or no.\n')
        noStop = False
        if showraw.lower() == 'yes':
            noStop = True

def main():
    '''
        Main function, calls all othe functions and loops until the user decides to quit
    '''
    while True:
        #Check if the user wants to continue before jumping in
        if not welcome():
            break
        #Let's go, first set filters by user inputs
        city, month, day = get_filters()
        #Now let's load the data filtered by the userinputs before
        df = load_data(city, month, day)
        #Calculate some statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #Print raw data
        printRaw(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main() # call main, start loop
