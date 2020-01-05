#!/usr/bin/python

# -
# Calculates average bike activities across renting stations from passed csv file with predefined structure
# -

import csv
import datetime as dt
import re
import sys

try:
    # Check passed params
    if len(sys.argv) != 2:
        print("Error: Please pass a csv file with the data as a parameter.")
        sys.exit()

    # Digest data
    with open(sys.argv[1]) as csvDataFile:
        csvReader = csv.reader(csvDataFile)

        bikeStats = {}
        stationStats = {}

        entries = []

        for index, row in enumerate(csvReader):
            if len(row) == 4:

                # Perform few data sanity checks

                # Station ID is 1-1000

                if not re.match(r"^[0-9]{1,4}$", row[0]) or int(row[0]) > 1000:
                    # Adjust index+1 to properly reference human readable line number on csv file
                    print("Error: Invalid csv data structure on line: {} (Check station ID) Aborting".format(index+1))
                    sys.exit()

                # Bike ID is 1-10000

                if not re.match(r"^[0-9]{1,5}$", row[1]) or int(row[1]) > 10000:
                    index += 1  # Adjust index to properly reference human readable line number on csv file
                    print("Error: Invalid csv data structure on line: {} (Check bike ID) Aborting".format(index+1))
                    sys.exit()

                # Arrival timestamps is empty or matches YYYYMMDDThh:mm:ss format

                if row[2] != "" and not re.match(r"^20[0-9]{6}T[0-9]{2}:[0-9]{2}:[0-9]{2}$", row[2]):
                    # Adjust index+1 to properly reference human readable line number on csv file
                    print("Error: Invalid csv data structure on line: {} (Check arrival time) Aborting".format(index+1))
                    sys.exit()

                # Departure timestamps is empty or matches YYYYMMDDThh:mm:ss format

                if row[3] != "" and not re.match(r"^20[0-9]{6}T[0-9]{2}:[0-9]{2}:[0-9]{2}$", row[3]):
                    # Adjust index+1 to properly reference human readable line number on csv file
                    print("Error: Invalid csv data structure on line: {} (Check departure time) Aborting".format(index+1))
                    sys.exit()

                # Both arrival and departure timestamps cannot be empty

                if row[2] == row[3] == "":
                    # Adjust index+1 to properly reference human readable line number on csv file
                    print("Error: Invalid csv data structure on line: {} (Check empty timestamps) Aborting".format(index+1))
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
                print("Error: Invalid csv data column count on line: %d - Aborting".format(index + 1))
                sys.exit()

    csvDataFile.close()

except IOError:
    print("Error: Import csv file does not exist")
    sys.exit()


try:
    sortedEntries = sorted(entries)
    # print(sortedEntries)

    for index, entry in enumerate(sortedEntries):
        if index < (len(sortedEntries) - 1) and entry[1] == sortedEntries[index + 1][1]: # Same bike
            depart = dt.datetime.strptime(entry[3], '%Y%m%dT%H:%M:%S')
            arrive = dt.datetime.strptime(sortedEntries[index + 1][2], '%Y%m%dT%H:%M:%S')

            if not str(entry[1]) in bikeStats.keys():
                bikeStats[str(entry[1])] = []

            bikeStats[str(entry[1])].append((arrive - depart).total_seconds())

            if entry[0] == sortedEntries[index + 1][0]: # Same station
                depart = dt.datetime.strptime(entry[3], '%Y%m%dT%H:%M:%S')
                arrive = dt.datetime.strptime(sortedEntries[index + 1][2], '%Y%m%dT%H:%M:%S')

                if not str(entry[0]) in stationStats.keys():
                    stationStats[str(entry[0])] = []

                stationStats[str(entry[0])].append((arrive - depart).total_seconds())

    '''
    print("##### Aggregated bike trips data ######")
    print(bikeStats)
    print("##### Aggregated station trips data ######")
    print(stationStats)
    '''

    for bike, stats in sorted(bikeStats.items()):
        print("##### Bike ID:{} ######".format(bike))
        print("  Total usage: {} seconds in {} trips".format(sum(stats), len(stats)))

        averageBikeSeconds = sum(stats) / len(stats)  # Average time
        averageBikeMinutes = averageBikeSeconds // 60
        averageBikeHours = averageBikeMinutes // 60

        print("  Average trip: %02d:%02d:%02d" % (averageBikeHours, averageBikeMinutes % 60, averageBikeSeconds % 60))

    for station, stats in sorted(stationStats.items()):
        print("##### Station ID:{} ######".format(station))
        print("  Total usage: {} seconds in {} trips".format(sum(stats), len(stats)))

        averageStationSeconds = sum(stats) / len(stats)  # Average time
        averageStationMinutes = averageStationSeconds // 60
        averageStationHours = averageStationMinutes // 60

        print("  Average trip: %02d:%02d:%02d" % (averageStationHours, averageStationMinutes % 60, averageStationSeconds % 60))

except Exception as e:
    print("Error occurred:{}".format(e.message))
    sys.exit()