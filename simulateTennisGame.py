from selenium import webdriver
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import mysql.connector
from mysql.connector import Error
from random import choices

def serveTable(page_soup):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='test_schema',
                                             user='root',
                                             password='LADY179okra')
        mySql_Create_Table_Query = """CREATE TABLE Serve2 ( 
                                 `Name` varchar(250) NOT NULL,
                                 `Serve_Rating` float NOT NULL,
                                `First_Serve(%)` float NOT NULL, 
                               `First_Serve_Points(%)` float NOT NULL,
                                 `Second_Serve_Points(%)` float NOT NULL,
                                 `Service_Games_Won(%)` float NOT NULL,
                                 `Average_Aces_Per_Match` float NOT NULL,
                                 `Average_Double_Faults_Per_Match` float NOT NULL) """
        cursor = connection.cursor()
        result = cursor.execute(mySql_Create_Table_Query)
        #insert
        tableServe = page_soup.findAll("tr", {"class": "stats-listing-row"})
        for playerRow in tableServe:
            name = playerRow.find("a", "stats-player-name").text
            serveRating = float(playerRow.findAll("td", {"data-type" : "serveRating"})[0].text)
            firstServePct = float(playerRow.findAll("td", {"data-type" : "1stServePct"})[0].text[:-1])
            firstServePointWonPct = float(playerRow.findAll("td", {"data-type" : "1stServePointsWonPct"})[0].text[:-1])
            secondServePointWonPct = float(playerRow.findAll("td", {"data-type" : "2ndServePointsWonPct"})[0].text[:-1])
            serviceGamesWon = float(playerRow.findAll("td", {"data-type" : "serviceGamesWonPct"})[0].text[:-1])
            avgAces = float(playerRow.findAll("td", {"data-type" : "avgAcesPerMatch"})[0].text)
            avgDoubleFaults = float(playerRow.findAll("td", {"data-type" : "avgDblFaultsPerMatch"})[0].text)
            mySql_insert_query = """INSERT INTO Serve2 (`Name`, `Serve_Rating`, `First_Serve(%)`, `First_Serve_Points(%)`, `Second_Serve_Points(%)`, `Service_Games_Won(%)`, `Average_Aces_Per_Match`, `Average_Double_Faults_Per_Match`)
                                VALUES
                                (%s, %s, %s, %s, %s, %s, %s, %s) """
            recordTuple = (name, serveRating, firstServePct, firstServePointWonPct, secondServePointWonPct, serviceGamesWon, avgAces, avgDoubleFaults)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
        print("Serve Table created successfully ")
    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def returnTable(page_soup2):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='test_schema',
                                             user='root',
                                             password='LADY179okra')
        mySql_Create_Table_Query = """CREATE TABLE `Returns` ( 
                                 `Name` varchar(250) NOT NULL,
                                 `Return_Rating` float NOT NULL,
                                 `First_Serve_Return_Points(%)` float NOT NULL,
                                 `Second_Serve_Return_Points(%)` float NOT NULL,
                                 `Return_Games_Won(%)` float NOT NULL,
                                 `Break_Points_Converted(%)` float NOT NULL) """
        cursor = connection.cursor()
        result = cursor.execute(mySql_Create_Table_Query)
        #insert
        tableReturn = page_soup2.findAll("tr", {"class": "stats-listing-row"})
        for playerRow in tableReturn:
            name = playerRow.find("a", "stats-player-name").text
            returnRating = float(playerRow.findAll("td", {"data-type" : "returnRating"})[0].text)
            #firstServePct = float(playerRow.findAll("td", {"data-type" : "1stServePct"})[0].text[:-1])
            firstServeReturnPointWonPct = float(playerRow.findAll("td", {"data-type" : "1stServeReturnPointsWonPct"})[0].text[:-1])
            secondServeReturnPointWonPct = float(playerRow.findAll("td", {"data-type" : "2ndServeReturnPointsWonPct"})[0].text[:-1])
            returnGamesWon = float(playerRow.findAll("td", {"data-type" : "returnGamesWonPct"})[0].text[:-1])
            breakPointsConverted = float(playerRow.findAll("td", {"data-type" : "brkPointsConvertedPct"})[0].text[:-1])

            connection = mysql.connector.connect(host='localhost', database='test_schema', user='root', password='LADY179okra')
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO `Returns` (`Name`, `Return_Rating`, `First_Serve_Return_Points(%)`, `Second_Serve_Return_Points(%)`, `Return_Games_Won(%)`, `Break_Points_Converted(%)`)
                               VALUES
                                (%s, %s, %s, %s, %s, %s) """
            recordTuple = (name, returnRating, firstServeReturnPointWonPct, secondServeReturnPointWonPct, returnGamesWon, breakPointsConverted)
            cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
        print("Return Table created successfully ")
    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def servePointWonTable(page_soup3):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='test_schema',
                                             user='root',
                                             password='LADY179okra')
        mySql_Create_Table_Query = """CREATE TABLE `ServePointsWon` ( 
                                 `Name` varchar(250) NOT NULL,
                                 `Serve_Points_Won(%)` float NOT NULL) """
        cursor = connection.cursor()
        result = cursor.execute(mySql_Create_Table_Query)
        servePointWon = page_soup3.findAll("td", {"class": "text-right"})
        for serve in servePointWon:
            percentage = float(serve.a.text[:-1])
            name = serve.parent.findAll("td", {"style": "width:300px;"})[0].text.strip()
            connection = mysql.connector.connect(host='localhost', database='test_schema', user='root', password='LADY179okra')
            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO `ServePointsWon` (`Name`, `Serve_Points_Won(%)`)
                                VALUES
                                (%s, %s) """
            recordTuple = (name, percentage)
            result = cursor.execute(mySql_insert_query, recordTuple)
            connection.commit()
        print("ServePointsWon created successfully ")
    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def finalPlayersTable():
    try:
        connection = mysql.connector.connect(host='localhost', database='test_schema', user='root', password='LADY179okra')
        cursor = connection.cursor()
        my_sql_insert_query = """CREATE TABLE finalPlayers AS SELECT returns.Name FROM ((returns INNER JOIN servepointswon ON returns.Name = servepointswon.Name))""";
        cursor.execute(my_sql_insert_query)
        connection.commit()
        print("Final Players successfully created")
    except mysql.connector.Error as error:
        print("Failed to create Final Players in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

#def getStats():
    

def simulateGame():
    rowCount = 1
    try:
        connection = mysql.connector.connect(host='localhost', database='test_schema', user='root', password='LADY179okra')
        cursor = connection.cursor()
        #cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM finalPlayers")
        availablePlayers = cursor.fetchall()
        for player in availablePlayers:
            print(player[0])
        print("\n")
        while(rowCount != 0):
            player1 = input("Select Player 1: ")
            cursor.execute(
                "SELECT Name, COUNT(*) FROM finalPlayers WHERE `Name` = %s GROUP BY Name",
                (player1,)
            )
            # gets the number of rows affected by the command executed

            msg = cursor.fetchone()
            if not msg:
                print("Player 1 is not in the above table")
            else:
                rowCount = 0
        rowCount = 1
        while(rowCount != 0):
            player2 = input("Select Player 2: ")
            cursor.execute(
                "SELECT Name, COUNT(*) FROM finalPlayers WHERE `Name` = %s GROUP BY Name",
                (player2,)
            )
            msg = cursor.fetchone()
            if not msg:
                print("Player 2 is not in the above table")
            else:
                rowCount = 0
        cursor.execute("SELECT AVG(`First_Serve(%)`) FROM `serve2`")
        aAV = cursor.fetchall()[0][0]/100

        recordTuple = (player1, )
        mySql_insert_query = """SELECT `First_Serve(%)` FROM `serve2` WHERE `Name` =%s"""
        cursor.execute(mySql_insert_query, recordTuple)
        aI = cursor.fetchall()[0][0]/100
        mySql_insert_query = """SELECT `First_Serve_Points(%)` FROM `serve2` WHERE `Name` =%s"""
        cursor.execute(mySql_insert_query, recordTuple)
        bI = cursor.fetchall()[0][0]/100
        mySql_insert_query = """SELECT `Second_Serve_Points(%)` FROM `serve2` WHERE `Name` =%s"""
        cursor.execute(mySql_insert_query, recordTuple)
        cI = cursor.fetchall()[0][0]/100
        mySql_insert_query = """SELECT `First_Serve_Return_Points(%)` FROM `Returns` WHERE `Name` =%s"""
        cursor.execute(mySql_insert_query, recordTuple)
        dI = cursor.fetchall()[0][0]/100
        mySql_insert_query = """SELECT `Second_Serve_Return_Points(%)` FROM `Returns` WHERE `Name` =%s"""
        cursor.execute(mySql_insert_query, recordTuple)
        eI = cursor.fetchall()[0][0]/100

        recordTuple = (player2, )
        cursor.execute("SELECT `First_Serve(%)` FROM `serve2` WHERE `Name` = %s", recordTuple)
        aJ = cursor.fetchall()[0][0]/100
        cursor.execute("SELECT `First_Serve_Points(%)` FROM `serve2` WHERE `Name` = %s", recordTuple)
        bJ = cursor.fetchall()[0][0]/100
        cursor.execute("SELECT `Second_Serve_Points(%)` FROM `serve2` WHERE `Name` = %s", recordTuple)
        cJ = cursor.fetchall()[0][0]/100
        cursor.execute("SELECT `First_Serve_Return_Points(%)` FROM `Returns` WHERE `Name` = %s", recordTuple)
        dJ = cursor.fetchall()[0][0]/100
        cursor.execute("SELECT `Second_Serve_Return_Points(%)` FROM `Returns` WHERE `Name` = %s", recordTuple)
        eJ = cursor.fetchall()[0][0]/100

        fI = (aI * bI) + ((1 - aI) * (cI))
        gI = (aAV * dI) + ((1 - aAV) * (eI))
        fJ = (aJ * bJ) + ((1 - aJ) * (cJ))
        gJ = (aAV * dJ) + ((1 - aAV) * (eJ))

        cursor.execute("SELECT AVG(`Serve_Points_Won(%)`) FROM `ServePointsWon`")
        serveAvg = cursor.fetchall()[0][0]/100
        returnAvg = 1 - serveAvg

        fIJ = serveAvg + (fI - serveAvg) - (gJ - returnAvg) #chance that player i wins on serve
        gIJ = returnAvg + (gI - returnAvg) - (fJ - serveAvg) #chance that player i wins on return
        fJI = serveAvg + (fJ - serveAvg) - (gI - returnAvg) #chance that player j wins on serve
        gJI = returnAvg + (gJ - returnAvg) - (fI - serveAvg) #chance that player j wins on return
        connection.commit()
    except mysql.connector.Error as error:
        print("Failed to insert values in table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    #simulate game
    pointWon = ['s', 'r']
    #score tracker
    playerOneScore = 0
    playerTwoScore = 0
    #games tracker
    playerOneGames = 0;
    playerTwoGames = 0
    #set tracker
    playerOneSets = 0
    playerTwoSets = 0

    deuce = 0
    differenceGames = 0
    while (playerOneSets != 3 and playerTwoSets != 3):
        print("\n" + "************ " + player1 + " Sets: " + str(playerOneSets) + " | " + player2 + " Sets: " + str(playerTwoSets) + "\n")
        while ((playerOneGames < 6 or  differenceGames < 2) and (playerTwoGames < 6 or differenceGames < 2)):
            print(player1 + " Games: " + str(playerOneGames) + " | " + player2 + " Games: " + str(playerTwoGames))
            print("----------------------------------------------------------------------------------------------------------------")
            if ((playerOneGames + playerTwoGames) % 2 == 0):
                weights = [fIJ, gJI]
                #print(weights)
                server = player1
                reciever = player2
            else:
                weights = [fJI, gIJ]
                #print(weights)
                server = player2
                reciever = player1
            print("\t" + "Server: " + server)
            
            while (playerOneScore < 60 and playerTwoScore < 60):
                point = choices(pointWon, weights)
                #print(point)
                if (point[0] == 's' and server == player1):
                    playerOneScore = playerOneScore + 15
                elif (point[0] == 's' and server == player2):
                    playerTwoScore = playerTwoScore + 15
                elif (point[0] == 'r' and reciever == player1):
                    playerOneScore = playerOneScore + 15
                elif (point[0] == 'r' and reciever == player2):
                    playerTwoScore = playerTwoScore + 15

                if (playerOneScore == 45 and playerTwoScore == 45):
                    while ((playerOneScore - playerTwoScore) != 30 and (playerTwoScore - playerOneScore) != 30):
                        point = choices(pointWon, weights)
                        print("\t" + "\t" + player1 + " Score: " + str(playerOneScore) + " " + player2 + " Score: " + str(playerTwoScore))
                        #print(point)
                        if (point[0] == 's' and server == player1):
                            playerOneScore = playerOneScore + 15
                        elif (point[0] == 's' and server == player2):
                            playerTwoScore = playerTwoScore + 15
                        elif (point[0] == 'r' and reciever == player1):
                            playerOneScore = playerOneScore + 15
                        elif (point[0] == 'r' and reciever == player2):
                            playerTwoScore = playerTwoScore + 15                    
                        deuce = 1
                #if (deuce == 0):
                print("\t" + "\t" + player1 + " Score: " + str(playerOneScore) + " " + player2 + " Score: " + str(playerTwoScore))
            if (playerOneScore > playerTwoScore):
                playerOneGames = playerOneGames + 1
            else:
                playerTwoGames = playerTwoGames + 1
            if (playerOneGames >= 6 or playerTwoGames >= 6):
                differenceGames = abs(playerOneGames - playerTwoGames)
            playerOneScore = 0
            playerTwoScore = 0
            deuce = 0
        if (playerOneGames > playerTwoGames):
            playerOneSets = playerOneSets + 1
        else:
            playerTwoSets = playerTwoSets + 1
        print(player1 + " Games: " + str(playerOneGames) + " | " + player2 + " Games: " + str(playerTwoGames))
        differenceGames = 0
        playerOneScore = 0
        playerTwoScore = 0
        playerOneGames = 0
        playerTwoGames = 0
    print("\n" + player1 + " won " + str(playerOneSets) + " sets" + "\n" + player2 + " won " + str(playerTwoSets) + " sets")


#Service Table
browser = webdriver.Chrome()
url = 'https://www.atptour.com/en/stats/leaderboard?boardType=serve&timeFrame=52Week&surface=all&versusRank=all&formerNo1=false'
browser.get(url)
innerHTML = browser.execute_script("return document.body.innerHTML")
page_soup = soup(innerHTML, "html.parser")
serveTable(page_soup)
#Return Table
url2 = 'https://www.atptour.com/en/stats/leaderboard?boardType=return&timeFrame=52Week&surface=all&versusRank=all&formerNo1=false'
browser.get(url2)
innerHTML2 = browser.execute_script("return document.body.innerHTML")
page_soup2 = soup(innerHTML2, "html.parser")
returnTable(page_soup2)
#ServePointWon Table
url3 = 'https://www.ultimatetennisstatistics.com/statsLeaders'
browser.get(url3)
python_button = browser.find_element_by_xpath("(//button[@class='btn btn-default dropdown-toggle'])[1]")
python_button.click()
python_button = browser.find_element_by_xpath("//a[@data-action='100']")
python_button.click()
python_button = browser.find_element_by_id('category')
python_button.send_keys("Service Points Won %")
innerHTML3 = browser.execute_script("return document.body.innerHTML")
page_soup3 = soup(innerHTML3, "html.parser")
servePointWonTable(page_soup3)
#finalPlayers Table
finalPlayersTable()
#get players and stats
##simulate the game
simulateGame()
#close browser
browser.close()