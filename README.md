## Bike hire statistics

A bike hire scheme consists of a number of bike hire stations from which bikes can be rented.  
A CSV report (no headers, no specified sort order) can be produced containing the history of bike
movements over a specified period.  

FILEPATH = "data.csv"  


##### CSV File Format
| Field  | Description |
| ------------- | ------------- |
| Station ID  | Integer, representing the bike hire station. Valid values: 1-1,000. |
| Bike ID  | Integer, representing the bike itself. Valid values: 1-10,000.  |
| Arrival Datetime  | Datetime in format YYYYMMDDThh:mm:ss. Representing the date/time the bike arrived at the station. It is empty if the bike was at this station at the start of the reporting period.  |
| Departure Datetime  | Datetime in format YYYYMMDDThh:mm:ss. Representing the date/time the bike departed from the station. It is empty if the bike was at this station at the end of the reporting period.  |

##### Example Line 1:
Bike 102 was docked (arrived) at station 22 at 2015-03-04 13:04 and was rented out again (departed) at 2015-03-04 13:25:32:  
```
22,102,20150304T13:04:00,20150304T13:25:32
```

##### Example Line 2:
Bike 34 was already at station 4 at the start of the reporting period, and was first rented out at 2015- 03-01 05:15:08  
```
4,34,,20150301T05:15:08
```

### Taks
Write Python program that would read the CSV report from the current working directory, and print the average (mean) journey duration, across all bikes and all stations, for the reporting period, in format hh:mm:ss.


### Run

```bash
./bikes.py data.csv
```