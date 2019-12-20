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

        for index, row in enumerate(csvReader):
            if len(row) == 4:

                # Perform few data sanity checks

                # Station ID is 1-1000
                if not re.match(r"^[0-9]{1,4}$", row[0]) or int(row[0]) > 1000:
                    index += 1  # Adjust index to properly reference human readable line number on csv file
                    print("Error: Invalid csv data structure on line: %d (Check station ID) Aborting" % index)
                    sys.exit()

                # Bike ID is 1-10000
                if not re.match(r"^[0-9]{1,5}$", row[1]) or int(row[1]) > 10000:
                    index += 1  # Adjust index to properly reference human readable line number on csv file
                    print("Error: Invalid csv data structure on line: %d (Check bike ID) Aborting" % index)
                    sys.exit()

                # Arrival timestamps is empty or matches YYYYMMDDThh:mm:ss format
                if row[2] != "" and not re.match(r"^20[0-9]{6}T[0-9]{2}:[0-9]{2}:[0-9]{2}$", row[2]):
                    index += 1  # Adjust index to properly reference human readable line number on csv file
                    print("Error: Invalid csv data structure on line: %d (Check arrival timestamp) Aborting" % index)
                    sys.exit()

                # Departure timestamps is empty or matches YYYYMMDDThh:mm:ss format
                if row[3] != "" and not re.match(r"^20[0-9]{6}T[0-9]{2}:[0-9]{2}:[0-9]{2}$", row[3]):
                    index += 1  # Adjust index to properly reference human readable line number on csv file
                    print("Error: Invalid csv data structure on line: %d (Check departure timestamp) Aborting" % index)
                    sys.exit()

                # Both arrival and departure timestamps cannot be empty
                if row[2] == row[3] == "":
                    index += 1  # Adjust index to properly reference human readable line number on csv file
                    print("Error: Invalid csv data structure on line: %d (Check empty timestamps) Aborting" % index)
                    sys.exit()

                '''
                # Assumptions:
                # - Bikes cannot be left at different stations after departure
                # - CSV data entries represents properly fluent history (in order of events)
                # - Only full journey cycles of departure-arrival on the same station can be evaluated
                '''

                # Create stats for station if not yet exists
                if not str(row[0]) in stationStats.keys():
                    stationStats[str(row[0])] = []

                # Create stats for bike if not yet exists
                if not str(row[1]) in bikeStats.keys():
                    bikeStats[str(row[1])] = []

                # Append data to station stats
                stationStats[str(row[0])].append(row[2])  # (arrival)
                stationStats[str(row[0])].append(row[3])  # (departure)

                # Append data to bike stats
                bikeStats[str(row[1])].append(row[2])  # (arrival)
                bikeStats[str(row[1])].append(row[3])  # (departure)

            else:
                index += 1  # Adjust index to properly reference human readable line number on csv file
                print("Error: Invalid csv data column count on line: %d - Aborting" % index)
                sys.exit()


        #print(bikeStats)
        # {
        # "bike~1":[{arrive, depart},{arrive, depart},{arrive, depart},{arrive, depart}...],
        # "bike~2":[{arrive, depart},{arrive, depart},{arrive, depart}...]
        # ...
        # }

        totalBikeSeconds = 0

        for bike, stats in bikeStats.items():
            #print("Bike id: %s" % bike)

            #  Loop dict by 2 items starting with 1 (passing first arrival timestamp)
            for i in range(1, len(stats), 2):
                if i+1 < len(stats):
                    depart = dt.datetime.strptime(stats[i], '%Y%m%dT%H:%M:%S')
                    arrive = dt.datetime.strptime(stats[i + 1], '%Y%m%dT%H:%M:%S')

                    totalBikeSeconds += (arrive - depart).total_seconds()
                else:
                    break

        print("Average bike trip: %d minutes" % (totalBikeSeconds/len(bikeStats)/60))

        totalStationSeconds = 0

        for station, stats in stationStats.items():
            #print("Station id: %s" % station)

            for i in range(1, len(stats), 2):
                if i+1 < len(stats):
                    depart = dt.datetime.strptime(stats[i], '%Y%m%dT%H:%M:%S')
                    arrive = dt.datetime.strptime(stats[i + 1], '%Y%m%dT%H:%M:%S')

                    totalStationSeconds += (arrive - depart).total_seconds()
                else:
                    break

        print("Average station trip: %d minutes" % (totalStationSeconds/len(stationStats)/60))


    csvDataFile.close()

except IOError:
    print("Error: Import csv file does not exist.")
    sys.exit()
