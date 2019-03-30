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


def Task1function(array):
    global connection, cursor
    
    start_year = input("Enter start year (YYYY): ")
    end_year = input("Enter end year (YYYY): ")
    crime = input("Enter crime type: ")
    df = pd.read_sql_query('''
                          SELECT M.MONTH, total_sum
                          FROM ( SELECT 1 AS MONTH UNION
                          SELECT 2 AS MONTH UNION
                          SELECT 3 AS MONTH UNION
                          SELECT 4 AS MONTH UNION
                          SELECT 5 AS MONTH UNION
                          SELECT 6 AS MONTH UNION
                          SELECT 7 AS MONTH UNION
                          SELECT 8 AS MONTH UNION
                          SELECT 9 AS MONTH UNION
                          SELECT 10 AS MONTH UNION
                          SELECT 11 AS MONTH UNION
                          SELECT 12 AS MONTH) M
                          LEFT JOIN 
                          (SELECT crime_incidents.MONTH, SUM(Incidents_Count) AS total_sum
                          FROM crime_incidents 
                          WHERE crime_type = ? AND year >= ? AND year <= ?
                          GROUP BY MONTH) C 
                          USING (MONTH) ''', connection, params = (crime, start_year, end_year,))
    # plot the graph
    if not df.empty:
        plot = df.plot.bar(x= 'MONTH')
        plt.savefig('Q1-' + str(array[0]) +'.png')
    return

def Task2function(array):
    global connection, cursor
    N = input("Enter number of locations:")
    df = pd.read_sql_query('''
                              SELECT Neighbourhood_Name, Latitude, Longitude, CANADIAN_CITIZEN + NON_CANADIAN_CITIZEN + NO_RESPONSE AS total_population
                              FROM population LEFT JOIN coordinates USING (neighbourhood_name)
                              WHERE total_population <> 0 AND latitude <> 0 AND longitude <> 0
                              ORDER BY total_population DESC;
                              ''', connection)
    m = folium.Map(location = [53.5444, -113.323], zoom_start = 11)
    
    i = 0
    while i < len(df) and (i < int(N) or df.iloc[i]["total_population"] == df.iloc[i-1]["total_population"]):
        folium.Circle(
            location = [df.iloc[i]['Latitude'], df.iloc[i]['Longitude']],
            popup = df.iloc[i]['Neighbourhood_Name'] + '\n' + str(df.iloc[i]['total_population']),
            radius = df.iloc[i]['total_population'] * 0.2,
            color = 'crimson',
            fill = True,
            fill_color = 'crimson').add_to(m)
        i+=1
        
    df = df.sort_values(by = ['total_population'])
    
    i = 0
    while i < len(df) and (i < int(N) or df.iloc[i]["total_population"] == df.iloc[i-1]["total_population"]):
        folium.Circle(
            location = [df.iloc[i]['Latitude'], df.iloc[i]['Longitude']],
            popup = df.iloc[i]['Neighbourhood_Name'] + '\n' + str(df.iloc[i]['total_population']),
            radius = df.iloc[i]['total_population'] * 1.0,
            color = 'blue',
            fill = True,
            fill_color = 'blue').add_to(m)
        i+=1    
    m.save("Q2-" + str(array[1]) + ".html")
    return

def Task3function(array):
    global connection, cursor
    m = folium.Map(location=[53.5444,-113.323], zoom_start=11)
    start = input('Enter start year (YYYY):')
    end = input('Enter end year (YYYY):')
    crime = input('Enter crime type:')
    num = input('Enter number of neighbourhoods:')

    cursor.execute('''
                   SELECT Neighbourhood_Name, SUM(Incidents_Count), Latitude, Longitude
                   FROM coordinates LEFT JOIN crime_incidents USING(Neighbourhood_Name)
                   WHERE Year >= :start AND Year <= :end AND Crime_Type == :crime AND Longitude != 0 AND Latitude != 0 
                   GROUP BY Neighbourhood_Name, Latitude, Longitude
                   HAVING SUM(Incidents_Count) >= (
                       SELECT MIN(sm) 
                       FROM (
                           SELECT SUM(Incidents_Count) AS sm
                           FROM coordinates LEFT JOIN crime_incidents USING(Neighbourhood_Name)
                           WHERE Year >= :start AND Year <= :end AND Crime_Type == :crime AND Longitude != 0 AND Latitude != 0
                           GROUP BY Neighbourhood_Name
                           ORDER BY SUM(Incidents_Count) DESC
                           LIMIT :num));
                           ''',
                           {'start': start, 'end': end, 'crime': crime, 'num': num})
                   
    rows = cursor.fetchall()
    for row in rows:
        folium.Circle(location=[float(row[2]), float(row[3])], 
                  popup= '%s <br> %d' % (row[0], int(row[1])),
                  radius= int(row[1]),
                  color= 'crimson',
                  fill= True,
                  fill_color= 'crimson'
                  ).add_to(m)
    m.save('Q3-%d.html' % array[2])
    
    return

def Task4function(array):
    global connection, cursor

    m = folium.Map(location=[53.5444, -113.323], zoom_start=11) #Instantiates the map
    # Asks the user for the year range and the number of N neighbourhoods
    start_year = int(input('Enter the starting year (YYYY): '))
    end_year = int(input('Enter the end year (YYYY): '))
    N = int(input('Enter the number of neighborhoods: '))
    # Executes the SQL query
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
WHERE Latitude <> 0
OR Longitude <> 0
GROUP BY Neighbourhood_Name) as Column3
where Column1.Neighbourhood_Name = Column2.Neighbourhood_Name
AND Column1.Neighbourhood_Name = Column3.Neighbourhood_Name
and Column2.pop > 0
ORDER BY Ratio desc;''', {"sy":start_year, "ey":end_year})
    rows = cursor.fetchall()
    i = 0
    while i < len(rows) and (i < N or rows[i][3] == rows[i-1][3]):
    # This while loop will add a circle to the map for top N in neighbourhood

        # Executes the SQL Query to get the most frequent crime type
        cursor.execute('''SELECT col1.Crime_type, MAX(col1.ic)
                        FROM (
                        SELECT Neighbourhood_Name, Crime_type, SUM(Incidents_Count) AS ic
                        FROM crime_incidents
                        WHERE Neighbourhood_Name = :nn
                        AND YEAR >= :sy
                        AND YEAR <= :ey
                        GROUP BY Crime_type
                        ORDER BY ic DESC ) AS col1''', {"nn":rows[i][0], "sy":start_year, "ey":end_year})
        crime_type = cursor.fetchone()
        #Adds the circle to the map
        folium.Circle(
            location = [rows[i][4], rows[i][5]],
            popup = rows[i][0] + '\n' + crime_type[0] + '\n' + str(rows[i][3]),
            radius = rows[i][3] * 5000.0,
            color = 'crimson',
            fill = True,
            fill_color = 'crimson').add_to(m)
        i+=1
    #Saves the map     
    m.save("Q4-" + str(array[3]) + ".html")    

    return

def SelectFunction():
    global connection, cursor
    
    print("Please choose a task to preform type e/exit to exit: \n 1. Task 1 \n 2. Task 2 \n 3. Task 3 \n 4. Task 4 \n")

    return input()

def ExecuteFunction(choice, array):

    # Updates the function count each time the corresponding function is executed
    if choice == 1:
        Task1function(array)
        array[0]+= 1
    elif choice == 2:
        Task2function(array)
        array[1] += 1
    elif choice == 3:
        Task3function(q3c)
        array[2] += 1
    elif choice == 4:
        Task4function(array)
        array[3] += 1
    return

def main():
    global connection, cursor

    path = input("Enter database name: ")
    connect(path)
    # Initializes the count arrray
    count_array = [1,1,1,1]
    while True:
        choice = SelectFunction()
        if choice == 'e' or choice == 'exit':
            break
        ExecuteFunction(int(choice), count_array)
    

    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()

    
    
