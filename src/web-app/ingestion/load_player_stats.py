import json, os
import pandas as pd
from sqlalchemy import create_engine, text

# -------------------------
# CONFIG
# -------------------------
DB_CONNECTION   = "mssql+pyodbc://@TTUK02671286934/baller?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
TABLE_NAME      = "PlayerStats"
# -------------------------
# LOAD JSON
# -------------------------
path = 'teams/players/stats/'
player_files = os.listdir(path)

for file in player_files:
    file_path = path + file
        
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)


    player      = data["player"]
    stats       = data["stats"]

    id          = player['id']
    name        = player['name']
    team        = player["currentTeam"]

    # Extract key fields
    record = {
     "PlayerId"                                         : player.get("id")
    ,"TeamId"                                           : team.get("id") 
    ,"duelsLost"                                        : stats.get("duelsLost")
    ,"penaltiesSaved"                                   : stats.get("penaltiesSaved")
    ,"fiftyFifty"                                       : stats.get("fiftyFifty")
    ,"blockedShots"                                     : stats.get("blockedShots")
    ,"shotsOnTargetIncGoals"                            : stats.get("shotsOnTargetIncGoals")
    ,"expectedGoalsOnTarget"                            : stats.get("expectedGoalsOnTarget")
    ,"totalTackles"                                     : stats.get("totalTackles")
    ,"throughBalls"                                     : stats.get("throughBalls")
    ,"gamesPlayed"                                      : stats.get("gamesPlayed")
    ,"setPiecesGoals"                                   : stats.get("setPiecesGoals")
    ,"successfulFiftyFifty"                             : stats.get("successfulFiftyFifty")
    ,"totalPasses"                                      : stats.get("totalPasses")
    ,"goals"                                            : stats.get("goals")
    ,"offsides"                                         : stats.get("offsides")
    ,"awayGoals"                                        : stats.get("awayGoals")
    ,"oboxBlocked"                                      : stats.get("oboxBlocked")
    ,"substituteOn"                                     : stats.get("substituteOn")
    ,"PlayerIndex"                                      : stats.get("index")
    ,"penaltiesFaced"                                   : stats.get("penaltiesFaced")
    ,"iboxTarget"                                       : stats.get("iboxTarget")
    ,"aerialDuelsLost"                                  : stats.get("aerialDuelsLost")
    ,"goalsConcededOutsideBox"                          : stats.get("goalsConcededOutsideBox")
    ,"groundDuelsWon"                                   : stats.get("groundDuelsWon")
    ,"successfulCornersIntoBox"                         : stats.get("successfulCornersIntoBox")
    ,"penaltyGoalsConceded"                             : stats.get("penaltyGoalsConceded")
    ,"expectedGoalsOnTargetConceded"                    : stats.get("expectedGoalsOnTargetConceded")
    ,"ownGoalScored"                                    : stats.get("ownGoalScored")
    ,"keyPassesAttemptAssists"                          : stats.get("keyPassesAttemptAssists")
    ,"successfulLaunches"                               : stats.get("successfulLaunches")
    ,"totalFoulsWon"                                    : stats.get("totalFoulsWon")
    ,"winningGoal"                                      : stats.get("winningGoal")
    ,"recoveries"                                       : stats.get("recoveries")
    ,"appearances"                                      : stats.get("appearances")
    ,"rightFootGoals"                                   : stats.get("rightFootGoals")
    ,"crossesNotClaimed"                                : stats.get("crossesNotClaimed")
    ,"leftFootGoals"                                    : stats.get("leftFootGoals")
    ,"unsuccessfulDribbles"                             : stats.get("unsuccessfulDribbles")
    ,"redCards2ndYellow"                                : stats.get("redCards2ndYellow")
    ,"unsuccessfulCrossesAndCorners"                    : stats.get("unsuccessfulCrossesAndCorners")
    ,"otherGoals"                                       : stats.get("otherGoals")
    ,"timesTackled"                                     : stats.get("timesTackled")
    ,"freekickTotal"                                    : stats.get("freekickTotal")
    ,"gkSuccessfulDistribution"                         : stats.get("gkSuccessfulDistribution")
    ,"openPlayPasses"                                   : stats.get("openPlayPasses")
    ,"shotsOffTargetIncWoodwork"                        : stats.get("shotsOffTargetIncWoodwork")
    ,"totalLossesOfPossession"                          : stats.get("totalLossesOfPossession")
    ,"tacklesWon"                                       : stats.get("tacklesWon")
    ,"attemptsFromSetPieces"                            : stats.get("attemptsFromSetPieces")
    ,"savesMadeParried"                                 : stats.get("savesMadeParried")
    ,"leftsidePasses"                                   : stats.get("leftsidePasses")
    ,"totalFoulsConceded"                               : stats.get("totalFoulsConceded")
    ,"unsuccessfulCornersIntoBox"                       : stats.get("unsuccessfulCornersIntoBox")
    ,"clearancesOffTheLine"                             : stats.get("clearancesOffTheLine")
    ,"successfulLongPasses"                             : stats.get("successfulLongPasses")
    ,"backwardPasses"                                   : stats.get("backwardPasses")
    ,"touches"                                          : stats.get("touches")
    ,"throwInsToOwnPlayer"                              : stats.get("throwInsToOwnPlayer")
    ,"hitWoodwork"                                      : stats.get("hitWoodwork")
    ,"goalsFromInsideBox"                               : stats.get("goalsFromInsideBox")
    ,"successfulPassesOwnHalf"                          : stats.get("successfulPassesOwnHalf")
    ,"savesMadeFromInsideBox"                           : stats.get("savesMadeFromInsideBox")
    ,"handballsConceded"                                : stats.get("handballsConceded")
    ,"unsuccessfulLongPasses"                           : stats.get("unsuccessfulLongPasses")
    ,"unsuccessfulPassesOwnHalf"                        : stats.get("unsuccessfulPassesOwnHalf")
    ,"secondGoalAssists"                                : stats.get("secondGoalAssists")
    ,"successfulCrossesOpenPlay"                        : stats.get("successfulCrossesOpenPlay")
    ,"expectedAssists"                                  : stats.get("expectedAssists")
    ,"totalRedCards"                                    : stats.get("totalRedCards")
    ,"expectedGoalsFreekick"                            : stats.get("expectedGoalsFreekick")
    ,"catches"                                          : stats.get("catches")
    ,"overruns"                                         : stats.get("overruns")
    ,"savesMadeFromOutsideBox"                          : stats.get("savesMadeFromOutsideBox")
    ,"totalShots"                                       : stats.get("totalShots")
    ,"unsuccessfulShortPasses"                          : stats.get("unsuccessfulShortPasses")
    ,"goalAssists"                                      : stats.get("goalAssists")
    ,"successfulLayoffs"                                : stats.get("successfulLayoffs")
    ,"foulWonPenalty"                                   : stats.get("foulWonPenalty")
    ,"setPieceGoals"                                    : stats.get("setPieceGoals")
    ,"starts"                                           : stats.get("starts")
    ,"totalUnsuccessfulPassesExclCrossesAndCorners"     : stats.get("totalUnsuccessfulPassesExclCrossesAndCorners")
    ,"unsuccessfulCrossesOpenPlay"                      : stats.get("unsuccessfulCrossesOpenPlay")
    ,"goalKicks"                                        : stats.get("goalKicks")
    ,"savesMadeCaught"                                  : stats.get("savesMadeCaught")
    ,"cornersTakenInclShortCorners"                     : stats.get("cornersTakenInclShortCorners")
    ,"aerialDuels"                                      : stats.get("aerialDuels")
    ,"cleanSheets"                                      : stats.get("cleanSheets")
    ,"successfulCrossesAndCorners"                      : stats.get("successfulCrossesAndCorners")
    ,"timePlayed"                                       : stats.get("timePlayed")
    ,"unsuccessfulLayoffs"                              : stats.get("unsuccessfulLayoffs")
    ,"duelsWon"                                         : stats.get("duelsWon")
    ,"penaltiesConceded"                                : stats.get("penaltiesConceded")
    ,"putthroughBlockedDistribution"                    : stats.get("putthroughBlockedDistribution")
    ,"successfulShortPasses"                            : stats.get("successfulShortPasses")
    ,"savesFromPenalty"                                 : stats.get("savesFromPenalty")
    ,"totalTouchesInOppositionBox"                      : stats.get("totalTouchesInOppositionBox")
    ,"throwInsToOppositionPlayer"                       : stats.get("throwInsToOppositionPlayer")
    ,"successfulOpenPlayPasses"                         : stats.get("successfulOpenPlayPasses")
    ,"punches"                                          : stats.get("punches")
    ,"cornersTakenIncShortCorners"                      : stats.get("cornersTakenIncShortCorners")
    ,"totalSuccessfulPassesExclCrossesAndCorners"       : stats.get("totalSuccessfulPassesExclCrossesAndCorners")
    ,"totalClearances"                                  : stats.get("totalClearances")
    ,"goalsConceded"                                    : stats.get("goalsConceded")
    ,"groundDuelsLost"                                  : stats.get("groundDuelsLost")
    ,"rightsidePasses"                                  : stats.get("rightsidePasses")
    ,"savesMade"                                        : stats.get("savesMade")
    ,"duels"                                            : stats.get("duels")
    ,"putthroughBlockedDistributionWon"                 : stats.get("putthroughBlockedDistributionWon")
    ,"homeGoals"                                        : stats.get("homeGoals")
    ,"goalkeeperSmother"                                : stats.get("goalkeeperSmother")
    ,"forwardPasses"                                    : stats.get("forwardPasses")
    ,"penaltiesTaken"                                   : stats.get("penaltiesTaken")
    ,"oboxTarget"                                       : stats.get("oboxTarget")
    ,"drops"                                            : stats.get("drops")
    ,"tacklesLost"                                      : stats.get("tacklesLost")
    ,"lastPlayerTackle"                                 : stats.get("lastPlayerTackle")
    ,"successfulPassesOppositionHalf"                   : stats.get("successfulPassesOppositionHalf")
    ,"goalsConcededInsideBox"                           : stats.get("goalsConcededInsideBox")
    ,"headedGoals"                                      : stats.get("headedGoals")
    ,"iboxBlocked"                                      : stats.get("iboxBlocked")
    ,"groundDuels"                                      : stats.get("groundDuels")
    ,"aerialDuelsWon"                                   : stats.get("aerialDuelsWon")
    ,"straightRedCards"                                 : stats.get("straightRedCards")
    ,"cornersWon"                                       : stats.get("cornersWon")
    ,"successfulDribbles"                               : stats.get("successfulDribbles")
    ,"blocks"                                           : stats.get("blocks")
    ,"gkUnsuccessfulDistribution"                       : stats.get("gkUnsuccessfulDistribution")
    ,"interceptions"                                    : stats.get("interceptions")
    ,"penaltyGoals"                                     : stats.get("penaltyGoals")
    ,"assistsIntentional"                               : stats.get("assistsIntentional")
    ,"substituteOff"                                    : stats.get("substituteOff")
    ,"unsuccessfulLaunches"                             : stats.get("unsuccessfulLaunches")
    ,"foulAttemptedTackle"                              : stats.get("foulAttemptedTackle")
    ,"expectedGoals"                                    : stats.get("expectedGoals")
    ,"goalsFromOutsideBox"                              : stats.get("goalsFromOutsideBox")
    ,"yellowCards"                                      : stats.get("yellowCards")
    }

    # -------------------------
    # LOAD INTO DATABASE
    # -------------------------
    engine = create_engine(DB_CONNECTION)

    # Create table if not exists (for SQLite demo; for SQL Server, precreate via SQL)
    create_table_sql = f"""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{TABLE_NAME}' AND xtype='U')
    CREATE TABLE {TABLE_NAME} (
        PlayerStatsId INT IDENTITY(1,1)
        ,PlayerId INT NOT NULL
        ,TeamId INT NOT NULL
        ,duelsLost DECIMAL(20,4) NOT NULL
        ,penaltiesSaved DECIMAL(20,4) NOT NULL
        ,fiftyFifty DECIMAL(20,4) NOT NULL
        ,blockedShots DECIMAL(20,4) NOT NULL
        ,shotsOnTargetIncGoals DECIMAL(20,4) NOT NULL
        ,expectedGoalsOnTarget DECIMAL(20,4) NOT NULL
        ,totalTackles DECIMAL(20,4) NOT NULL
        ,throughBalls DECIMAL(20,4) NOT NULL
        ,gamesPlayed DECIMAL(20,4) NOT NULL
        ,setPiecesGoals DECIMAL(20,4) NOT NULL
        ,successfulFiftyFifty DECIMAL(20,4) NOT NULL
        ,totalPasses DECIMAL(20,4) NOT NULL
        ,goals DECIMAL(20,4) NOT NULL
        ,offsides DECIMAL(20,4) NOT NULL
        ,awayGoals DECIMAL(20,4) NOT NULL
        ,oboxBlocked DECIMAL(20,4) NOT NULL
        ,substituteOn DECIMAL(20,4) NOT NULL
        ,PlayerIndex DECIMAL(20,4) NOT NULL
        ,penaltiesFaced DECIMAL(20,4) NOT NULL
        ,iboxTarget DECIMAL(20,4) NOT NULL
        ,aerialDuelsLost DECIMAL(20,4) NOT NULL
        ,goalsConcededOutsideBox DECIMAL(20,4) NOT NULL
        ,groundDuelsWon DECIMAL(20,4) NOT NULL
        ,successfulCornersIntoBox DECIMAL(20,4) NOT NULL
        ,penaltyGoalsConceded DECIMAL(20,4) NOT NULL
        ,expectedGoalsOnTargetConceded DECIMAL(20,4) NOT NULL
        ,ownGoalScored DECIMAL(20,4) NOT NULL
        ,keyPassesAttemptAssists DECIMAL(20,4) NOT NULL
        ,successfulLaunches DECIMAL(20,4) NOT NULL
        ,totalFoulsWon DECIMAL(20,4) NOT NULL
        ,winningGoal DECIMAL(20,4) NOT NULL
        ,recoveries DECIMAL(20,4) NOT NULL
        ,appearances DECIMAL(20,4) NOT NULL
        ,rightFootGoals DECIMAL(20,4) NOT NULL
        ,crossesNotClaimed DECIMAL(20,4) NOT NULL
        ,leftFootGoals DECIMAL(20,4) NOT NULL
        ,unsuccessfulDribbles DECIMAL(20,4) NOT NULL
        ,redCards2ndYellow DECIMAL(20,4) NOT NULL
        ,unsuccessfulCrossesAndCorners DECIMAL(20,4) NOT NULL
        ,otherGoals DECIMAL(20,4) NOT NULL
        ,timesTackled DECIMAL(20,4) NOT NULL
        ,freekickTotal DECIMAL(20,4) NOT NULL
        ,gkSuccessfulDistribution DECIMAL(20,4) NOT NULL
        ,openPlayPasses DECIMAL(20,4) NOT NULL
        ,shotsOffTargetIncWoodwork DECIMAL(20,4) NOT NULL
        ,totalLossesOfPossession DECIMAL(20,4) NOT NULL
        ,tacklesWon DECIMAL(20,4) NOT NULL
        ,attemptsFromSetPieces DECIMAL(20,4) NOT NULL
        ,savesMadeParried DECIMAL(20,4) NOT NULL
        ,leftsidePasses DECIMAL(20,4) NOT NULL
        ,totalFoulsConceded DECIMAL(20,4) NOT NULL
        ,unsuccessfulCornersIntoBox DECIMAL(20,4) NOT NULL
        ,clearancesOffTheLine DECIMAL(20,4) NOT NULL
        ,successfulLongPasses DECIMAL(20,4) NOT NULL
        ,backwardPasses DECIMAL(20,4) NOT NULL
        ,touches DECIMAL(20,4) NOT NULL
        ,throwInsToOwnPlayer DECIMAL(20,4) NOT NULL
        ,hitWoodwork DECIMAL(20,4) NOT NULL
        ,goalsFromInsideBox DECIMAL(20,4) NOT NULL
        ,successfulPassesOwnHalf DECIMAL(20,4) NOT NULL
        ,savesMadeFromInsideBox DECIMAL(20,4) NOT NULL
        ,handballsConceded DECIMAL(20,4) NOT NULL
        ,unsuccessfulLongPasses DECIMAL(20,4) NOT NULL
        ,unsuccessfulPassesOwnHalf DECIMAL(20,4) NOT NULL
        ,secondGoalAssists DECIMAL(20,4) NOT NULL
        ,successfulCrossesOpenPlay DECIMAL(20,4) NOT NULL
        ,expectedAssists DECIMAL(20,4) NOT NULL
        ,totalRedCards DECIMAL(20,4) NOT NULL
        ,expectedGoalsFreekick DECIMAL(20,4) NOT NULL
        ,catches DECIMAL(20,4) NOT NULL
        ,overruns DECIMAL(20,4) NOT NULL
        ,savesMadeFromOutsideBox DECIMAL(20,4) NOT NULL
        ,totalShots DECIMAL(20,4) NOT NULL
        ,unsuccessfulShortPasses DECIMAL(20,4) NOT NULL
        ,goalAssists DECIMAL(20,4) NOT NULL
        ,successfulLayoffs DECIMAL(20,4) NOT NULL
        ,foulWonPenalty DECIMAL(20,4) NOT NULL
        ,setPieceGoals DECIMAL(20,4) NOT NULL
        ,starts DECIMAL(20,4) NOT NULL
        ,totalUnsuccessfulPassesExclCrossesAndCorners DECIMAL(20,4) NOT NULL
        ,unsuccessfulCrossesOpenPlay DECIMAL(20,4) NOT NULL
        ,goalKicks DECIMAL(20,4) NOT NULL
        ,savesMadeCaught DECIMAL(20,4) NOT NULL
        ,cornersTakenInclShortCorners DECIMAL(20,4) NOT NULL
        ,aerialDuels DECIMAL(20,4) NOT NULL
        ,cleanSheets DECIMAL(20,4) NOT NULL
        ,successfulCrossesAndCorners DECIMAL(20,4) NOT NULL
        ,timePlayed DECIMAL(20,4) NOT NULL
        ,unsuccessfulLayoffs DECIMAL(20,4) NOT NULL
        ,duelsWon DECIMAL(20,4) NOT NULL
        ,penaltiesConceded DECIMAL(20,4) NOT NULL
        ,putthroughBlockedDistribution DECIMAL(20,4) NOT NULL
        ,successfulShortPasses DECIMAL(20,4) NOT NULL
        ,savesFromPenalty DECIMAL(20,4) NOT NULL
        ,totalTouchesInOppositionBox DECIMAL(20,4) NOT NULL
        ,throwInsToOppositionPlayer DECIMAL(20,4) NOT NULL
        ,successfulOpenPlayPasses DECIMAL(20,4) NOT NULL
        ,punches DECIMAL(20,4) NOT NULL
        ,cornersTakenIncShortCorners DECIMAL(20,4) NOT NULL
        ,totalSuccessfulPassesExclCrossesAndCorners DECIMAL(20,4) NOT NULL
        ,totalClearances DECIMAL(20,4) NOT NULL
        ,goalsConceded DECIMAL(20,4) NOT NULL
        ,groundDuelsLost DECIMAL(20,4) NOT NULL
        ,rightsidePasses DECIMAL(20,4) NOT NULL
        ,savesMade DECIMAL(20,4) NOT NULL
        ,duels DECIMAL(20,4) NOT NULL
        ,putthroughBlockedDistributionWon DECIMAL(20,4) NOT NULL
        ,homeGoals DECIMAL(20,4) NOT NULL
        ,goalkeeperSmother DECIMAL(20,4) NOT NULL
        ,forwardPasses DECIMAL(20,4) NOT NULL
        ,penaltiesTaken DECIMAL(20,4) NOT NULL
        ,oboxTarget DECIMAL(20,4) NOT NULL
        ,drops DECIMAL(20,4) NOT NULL
        ,tacklesLost DECIMAL(20,4) NOT NULL
        ,lastPlayerTackle DECIMAL(20,4) NOT NULL
        ,successfulPassesOppositionHalf DECIMAL(20,4) NOT NULL
        ,goalsConcededInsideBox DECIMAL(20,4) NOT NULL
        ,headedGoals DECIMAL(20,4) NOT NULL
        ,iboxBlocked DECIMAL(20,4) NOT NULL
        ,groundDuels DECIMAL(20,4) NOT NULL
        ,aerialDuelsWon DECIMAL(20,4) NOT NULL
        ,straightRedCards DECIMAL(20,4) NOT NULL
        ,cornersWon DECIMAL(20,4) NOT NULL
        ,successfulDribbles DECIMAL(20,4) NOT NULL
        ,blocks DECIMAL(20,4) NOT NULL
        ,gkUnsuccessfulDistribution DECIMAL(20,4) NOT NULL
        ,interceptions DECIMAL(20,4) NOT NULL
        ,penaltyGoals DECIMAL(20,4) NOT NULL
        ,assistsIntentional DECIMAL(20,4) NOT NULL
        ,substituteOff DECIMAL(20,4) NOT NULL
        ,unsuccessfulLaunches DECIMAL(20,4) NOT NULL
        ,foulAttemptedTackle DECIMAL(20,4) NOT NULL
        ,expectedGoals DECIMAL(20,4) NOT NULL
        ,goalsFromOutsideBox DECIMAL(20,4) NOT NULL
        ,yellowCards DECIMAL(20,4) NOT NULL
    );
    """
    with engine.begin() as conn:
        conn.execute(text(create_table_sql))

    # Insert record
    df = pd.DataFrame([record])
    df.to_sql(TABLE_NAME, con=engine, if_exists="append", index=False)

    print(f"Successfully loaded \t {id},\t{name}.")