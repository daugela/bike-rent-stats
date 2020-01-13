#!/usr/bin/python

# -
# Calculates average bike activities across renting stations from passed csv file with predefined structure
# -

import csv
import datetime as dt
import re
import sys


def main():
    try:
        # Check passed params
        if len(sys.argv) != 2:
            print("Error: Please pass a csv file with the data as a parameter.")
            sys.exit()

        # Digest data
        with open(sys.argv[1]) as csvDataFile:
            csv_reader = csv.reader(csvDataFile)

            bike_stats = {}
            station_stats = {}

            entries = []

            for index, row in enumerate(csv_reader):
                if len(row) == 4:

                    # Perform few data sanity checks

                    # Station ID is 1-1000

                    if not re.match(r"^[0-9]{1,4}$", row[0]) or int(row[0]) > 1000:
                        # Adjust index+1 to properly reference human readable line number on csv file
                        print("Error: Invalid csv data structure on line: {} (Check station ID) Abort".format(index+1))
                        sys.exit()

                    # Bike ID is 1-10000

                    if not re.match(r"^[0-9]{1,5}$", row[1]) or int(row[1]) > 10000:
                        index += 1  # Adjust index to properly reference human readable line number on csv file
                        print("Error: Invalid csv data structure on line: {} (Check bike ID) Abort".format(index+1))
                        sys.exit()

                    # Arrival timestamps is empty or matches YYYYMMDDThh:mm:ss format

                    if row[2] != "" and not re.match(r"^20[0-9]{6}T[0-9]{2}:[0-9]{2}:[0-9]{2}$", row[2]):
                        # Adjust index+1 to properly reference human readable line number on csv file
                        print("Error: Invalid csv data structure on line: {} (Check arrival time) Abort".format(index+1))
                        sys.exit()

                    # Departure timestamps is empty or matches YYYYMMDDThh:mm:ss format

                    if row[3] != "" and not re.match(r"^20[0-9]{6}T[0-9]{2}:[0-9]{2}:[0-9]{2}$", row[3]):
                        # Adjust index+1 to properly reference human readable line number on csv file
                        print("Error: Invalid csv data structure on line: {} (Check departure time) Abort".format(index+1))
                        sys.exit()

                    # Both arrival and departure timestamps cannot be empty

                    if row[2] == row[3] == "":
                        # Adjust index+1 to properly reference human readable line number on csv file
                        print("Error: Invalid csv data structure on line: {} (Check empty timestamps) Abort".format(index+1))
                        sys.exit()

                    '''
                    ################################
                    # Assumptions:
                    # - Bikes cannot be left at different stations after departure
                    # - CSV data entries represents properly fluent history (in order of events)
                    # - Only full journey cycles of departure-arrival on the same station can be evaluated
                    ################################
                    '''

                    # Append entries of csv as tuples into list for processing
                    entries.append((row[0], row[1], row[2], row[3]))

                else:
                    # Adjust index to properly reference human readable line number on csv file
                    print("Error: Invalid csv data column count on line: %d - Abort".format(index + 1))
                    sys.exit()

        csvDataFile.close()

    except IOError:
        print("Error: Import csv file does not exist")
        sys.exit()

    try:
        sorted_entries = sorted(entries)
        # print(sorted_entries)

        for index, entry in enumerate(sorted_entries):
            if index < (len(sorted_entries) - 1) and entry[1] == sorted_entries[index + 1][1]: # Same bike
                depart = dt.datetime.strptime(entry[3], '%Y%m%dT%H:%M:%S')
                arrive = dt.datetime.strptime(sorted_entries[index + 1][2], '%Y%m%dT%H:%M:%S')

                if not str(entry[1]) in bike_stats.keys():
                    bike_stats[str(entry[1])] = []

                bike_stats[str(entry[1])].append((arrive - depart).total_seconds())

                if entry[0] == sorted_entries[index + 1][0]: # Same station
                    depart = dt.datetime.strptime(entry[3], '%Y%m%dT%H:%M:%S')
                    arrive = dt.datetime.strptime(sorted_entries[index + 1][2], '%Y%m%dT%H:%M:%S')

                    if not str(entry[0]) in station_stats.keys():
                        station_stats[str(entry[0])] = []

                    station_stats[str(entry[0])].append((arrive - depart).total_seconds())

        '''
        print("##### Aggregated bike trips data ######")
        print(bike_stats)
        print("##### Aggregated station trips data ######")
        print(station_stats)
        '''

        for bike, stats in sorted(bike_stats.items()):
            print("##### Bike ID:{} ######".format(bike))
            print("  Total usage: {} seconds in {} trips".format(sum(stats), len(stats)))

            average_bike_seconds = sum(stats) / len(stats)  # Average time
            average_bike_minutes = average_bike_seconds // 60
            average_bike_hours = average_bike_minutes // 60

            print("  Average trip: %02d:%02d:%02d" % 
                  (average_bike_hours, average_bike_minutes % 60, average_bike_seconds % 60))

        for station, stats in sorted(station_stats.items()):
            print("##### Station ID:{} ######".format(station))
            print("  Total usage: {} seconds in {} trips".format(sum(stats), len(stats)))

            average_station_seconds = sum(stats) / len(stats)  # Average time
            average_station_minutes = average_station_seconds // 60
            average_station_hours = average_station_minutes // 60

            print("  Average trip: %02d:%02d:%02d" % 
                  (average_station_hours, average_station_minutes % 60, average_station_seconds % 60))

    except Exception as e:
        print("Error occurred:{}".format(e.message))
        sys.exit()


if __name__ == "__main__":
    main()
