import sqlite3
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt
import folium

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    connection.commit()
    return


def Task1function():
    global connection, cursor

    return

def Task2function():
    global connection, cursor

    return

def Task3function():
    global connection, cursor

    return

def Task4function():
    global connection, cursor

    m = folium.Map(location=[53.5444, -113.323], zoom_start=11) #Instantiates the map 
    start_year = int(input('Enter the starting year (YYYY): '))
    end_year = int(input('Enter the end year (YYYY): '))
    N = int(input('Enter the number of neighborhoods: '))

    cursor.execute('''SELECT Column1.Neighbourhood_Name, Column2.pop, Column1.inc_count, (Column1.inc_count/ CAST(Column2.pop AS FLOAT)) AS Ratio, Column3.Latitude, Column3.Longitude
FROM (
SELECT ci.Neighbourhood_Name, SUM(Incidents_Count) as inc_count
FROM crime_incidents ci
WHERE ci.YEAR >= :sy
AND ci.YEAR <= :ey
GROUP BY ci.Neighbourhood_Name
ORDER BY inc_count DESC) as Column1,

(SELECT Neighbourhood_Name, SUM(CANADIAN_CITIZEN + NON_CANADIAN_CITIZEN + NO_RESPONSE) as pop
FROM population
GROUP BY Neighbourhood_Name) as Column2,

(SELECT Neighbourhood_Name,Latitude, Longitude
FROM coordinates c
WHERE Latitude > 0
OR Longitude > 0
GROUP BY Neighbourhood_Name) as Column3
where Column1.Neighbourhood_Name = Column2.Neighbourhood_Name
AND Column1.Neighbourhood_Name = Column3.Neighbourhood_Name
and Column2.pop > 0
ORDER BY Ratio desc;''', {"sy":start_year, "ey":end_year})
    rows = cursor.fetchall()
    neighbourhoods = rows[0:N]
    for x in neighbourhoods:
        print(x)
        folium.Marker(location=[x[4], x[5]], popup=x[0]).add_to(m)
        m.save(x[0] + "_marker.html")
    m
    
    

    '''
    SQL QUERY:
   SELECT Column1.Neighbourhood_Name, Column2.pop, Column1.inc_count, (Column1.inc_count/ CAST(Column2.pop AS FLOAT)) AS Ratio, Column3.Latitude, Column3.Longitude
FROM (
SELECT ci.Neighbourhood_Name, SUM(Incidents_Count) as inc_count
FROM crime_incidents ci
WHERE ci.YEAR >= 2009
AND ci.YEAR <= 2009
GROUP BY ci.Neighbourhood_Name
ORDER BY inc_count DESC) as Column1,

(SELECT Neighbourhood_Name, SUM(CANADIAN_CITIZEN + NON_CANADIAN_CITIZEN + NO_RESPONSE) as pop
FROM population
GROUP BY Neighbourhood_Name) as Column2,

(SELECT Neighbourhood_Name,Latitude, Longitude
FROM coordinates c
WHERE Latitude > 0
OR Longitude > 0
GROUP BY Neighbourhood_Name) as Column3
where Column1.Neighbourhood_Name = Column2.Neighbourhood_Name
AND Column1.Neighbourhood_Name = Column3.Neighbourhood_Name
and Column2.pop > 0
ORDER BY Ratio desc;

'''

    

    

    return

def SelectFunction():
    global connection, cursor
    
    print("Please choose a task to preform type e/exit to exit: \n 1. Task 1 \n 2. Task 2 \n 3. Task 3 \n 4. Task 4 \n")

    return input()

def ExecuteFunction(choice):

    if choice == 1:
        Task1function()
    elif choice == 2:
        Task2function()
    elif choice == 3:
        Task3function()
    elif choice == 4:
        Task4function()

    return
    

def main():
    global connection, cursor

    path = input("Enter database name: ")
    connect(path)
    
    while True:
        choice = SelectFunction()
        if choice == 'e' or choice == 'exit':
            break
        ExecuteFunction(int(choice))
    

    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()

    
    
