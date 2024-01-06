import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()

# database creation and use made possible by mpope9's nba-sql database (available on GitHub)


# gets the answers for squares that are an intersection between two teams
def getTeamByTeamAnswers(team1, team2):
    try:
        connection = psycopg2.connect(
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host="localhost",
            port="5432",
            database="postgres"
        )
        cursor = connection.cursor()
        command = f'''SELECT p.player_name 
                       FROM player as p
                       JOIN player_season as s ON p.player_id = s.player_id
                       JOIN team as t ON s.team_id = t.team_id
                      WHERE t.team_id = {team1.id} OR t.team_id = {team2.id}
                      GROUP BY p.player_name
                     HAVING COUNT(DISTINCT t.team_id) = 2;'''
        cursor.execute(command)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()

# gets the answers for squares that are an intersection between teammates of a player and a team
def getTeamByPlayerAnswers(team, player):
    try:
        connection = psycopg2.connect(
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host="localhost",
            port="5432",
            database="postgres"
        )
        cursor = connection.cursor()
        command = f'''WITH PlayerSeasons as (SELECT season_id, team_id
                                               FROM player_season
                                              WHERE player_id = {player.id})
        
                     SELECT p.player_name
                       FROM player as p
                       JOIN player_season as s ON p.player_id = s.player_id
                      WHERE (s.season_id, s.team_id) IN (SELECT season_id, team_id FROM PlayerSeasons) AND
                            {team.id} IN (SELECT DISTINCT t.team_id
                                            FROM player_season as t
                                           WHERE t.player_id = p.player_id)
                      GROUP BY p.player_name;'''
        cursor.execute(command)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()