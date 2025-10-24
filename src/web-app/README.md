## ⚙️ Design philosophy

* **Normalization** up to 3NF for clean joins (no redundant text fields).
* **Surrogate keys** (IDENTITY) for internal use.
* **Natural keys** (names, IDs from external sources like Opta/Wyscout) stored as alternate IDs for data integration.
* **Timestamps** for ETL and data freshness tracking.
* Supports *historical queries* (league memberships, transfers, fixtures across seasons).
* Compatible with **SQL Server / PostgreSQL syntax** (adjust small syntax differences as needed).

---

# 🧱 Master schema

---

## 1. Leagues

```sql
CREATE TABLE Leagues (
    LeagueId INT IDENTITY(1,1) PRIMARY KEY,
    LeagueName VARCHAR(150) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    Confederation VARCHAR(50) NULL,        -- e.g., UEFA, CONMEBOL
    DivisionLevel INT NULL,                -- 1 = top division, 2 = second tier, etc.
    FoundedYear SMALLINT NULL,
    LeagueCode VARCHAR(20) NULL,           -- external key or short code (e.g., "EPL", "LALIGA")
    Active BIT DEFAULT 1,
    LastUpdated DATETIME DEFAULT GETDATE()
);
```

---

## 2. Clubs

```sql
CREATE TABLE Clubs (
    ClubId INT IDENTITY(1,1) PRIMARY KEY,
    LeagueId INT NULL REFERENCES Leagues(LeagueId),
    ClubName VARCHAR(150) NOT NULL,
    ShortName VARCHAR(50) NULL,
    City VARCHAR(100) NULL,
    Country VARCHAR(100) NULL,
    FoundedYear SMALLINT NULL,
    StadiumName VARCHAR(150) NULL,
    StadiumCapacity INT NULL,
    Latitude DECIMAL(9,6) NULL,            -- for geospatial/travel distance
    Longitude DECIMAL(9,6) NULL,
    Website VARCHAR(255) NULL,
    ExternalClubCode VARCHAR(50) NULL,     -- Opta/Wyscout ID
    Active BIT DEFAULT 1,
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE()
);
```

---

## 3. Managers

```sql
CREATE TABLE Managers (
    ManagerId INT IDENTITY(1,1) PRIMARY KEY,
    FullName VARCHAR(150) NOT NULL,
    Nationality VARCHAR(100) NULL,
    DateOfBirth DATE NULL,
    PreferredFormation VARCHAR(20) NULL,   -- e.g., '4-3-3'
    CoachingStyle VARCHAR(100) NULL,       -- optional descriptive tag
    ManagerSince DATE NULL,
    ExternalManagerCode VARCHAR(50) NULL,
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE()
);
```

### Manager–Club relationship (historical)

A manager may coach multiple clubs over time, and a club may have multiple managers.

```sql
CREATE TABLE ClubManagers (
    ClubManagerId INT IDENTITY(1,1) PRIMARY KEY,
    ClubId INT NOT NULL REFERENCES Clubs(ClubId),
    ManagerId INT NOT NULL REFERENCES Managers(ManagerId),
    StartDate DATE NOT NULL,
    EndDate DATE NULL,                     -- NULL = current
    Source VARCHAR(100) NULL,
    CreatedAt DATETIME DEFAULT GETDATE()
);
```

---

## 4. Players

```sql
CREATE TABLE Players (
    PlayerId INT IDENTITY(1,1) PRIMARY KEY,
    FullName VARCHAR(150) NOT NULL,
    KnownAs VARCHAR(100) NULL,
    Nationality VARCHAR(100) NULL,
    SecondNationality VARCHAR(100) NULL,
    DateOfBirth DATE NULL,
    HeightCm SMALLINT NULL,
    WeightKg SMALLINT NULL,
    PreferredFoot VARCHAR(10) NULL,        -- 'Left', 'Right', 'Both'
    PositionGroup VARCHAR(20) NULL,        -- 'Forward', 'Midfielder', 'Defender', 'Goalkeeper'
    PositionDetailed VARCHAR(20) NULL,     -- 'LW', 'RB', etc.
    ExternalPlayerCode VARCHAR(50) NULL,
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE()
);
```

### Player–Club historical association (transfers, loans)

```sql
CREATE TABLE PlayerClubs (
    PlayerClubId INT IDENTITY(1,1) PRIMARY KEY,
    PlayerId INT NOT NULL REFERENCES Players(PlayerId),
    ClubId INT NOT NULL REFERENCES Clubs(ClubId),
    ContractStart DATE NOT NULL,
    ContractEnd DATE NULL,
    TransferFee DECIMAL(18,2) NULL,
    TransferType VARCHAR(50) NULL,        -- 'Transfer', 'Loan', 'Free'
    ShirtNumber SMALLINT NULL,
    Active BIT DEFAULT 1,
    CreatedAt DATETIME DEFAULT GETDATE()
);
```

---

## 5. Fixtures (matches)

```sql
CREATE TABLE Fixtures (
    FixtureId BIGINT IDENTITY(1,1) PRIMARY KEY,
    LeagueId INT REFERENCES Leagues(LeagueId),
    Season VARCHAR(20) NULL,              -- e.g., '2024/2025'
    MatchDate DATETIME NOT NULL,
    HomeClubId INT NOT NULL REFERENCES Clubs(ClubId),
    AwayClubId INT NOT NULL REFERENCES Clubs(ClubId),
    Venue VARCHAR(150) NULL,
    StadiumName VARCHAR(150) NULL,
    RefereeName VARCHAR(150) NULL,
    Attendance INT NULL,
    Weather VARCHAR(100) NULL,
    HomeGoals SMALLINT NULL,
    AwayGoals SMALLINT NULL,
    HomeXG DECIMAL(4,2) NULL,
    AwayXG DECIMAL(4,2) NULL,
    MatchStatus VARCHAR(20) DEFAULT 'Scheduled', -- Scheduled, Live, Completed, Postponed
    MatchWeek INT NULL,
    ExternalMatchCode VARCHAR(50) NULL,
    LastUpdated DATETIME DEFAULT GETDATE()
);
```

---

### Fixture Events (optional extension for detailed analytics)

```sql
CREATE TABLE FixtureEvents (
    EventId BIGINT IDENTITY(1,1) PRIMARY KEY,
    FixtureId BIGINT REFERENCES Fixtures(FixtureId),
    EventTimeMinute SMALLINT NOT NULL,
    EventType VARCHAR(50) NOT NULL,       -- 'Goal', 'Card', 'Substitution', 'Shot', etc.
    TeamId INT REFERENCES Clubs(ClubId),
    PlayerId INT REFERENCES Players(PlayerId),
    AssistPlayerId INT NULL REFERENCES Players(PlayerId),
    XG DECIMAL(4,2) NULL,
    EventDescription VARCHAR(255) NULL,
    CreatedAt DATETIME DEFAULT GETDATE()
);
```

---

### Fixture Odds (optional — for betting models)

```sql
CREATE TABLE FixtureOdds (
    OddsId BIGINT IDENTITY(1,1) PRIMARY KEY,
    FixtureId BIGINT REFERENCES Fixtures(FixtureId),
    Bookmaker VARCHAR(100) NOT NULL,
    MarketType VARCHAR(50) NOT NULL,      -- '1X2', 'OverUnder', 'BothTeamsToScore'
    OddsHome DECIMAL(6,2) NULL,
    OddsDraw DECIMAL(6,2) NULL,
    OddsAway DECIMAL(6,2) NULL,
    OverOdds DECIMAL(6,2) NULL,
    UnderOdds DECIMAL(6,2) NULL,
    LineValue DECIMAL(4,2) NULL,          -- e.g., over/under line
    SnapshotTime DATETIME NOT NULL,       -- timestamp for odds snapshot
    Source VARCHAR(100) NULL,
    CreatedAt DATETIME DEFAULT GETDATE(),
    INDEX IX_FixtureOdds_FixtureId (FixtureId)
);
```

---

### Lineups (who started / substitutions)

```sql
CREATE TABLE FixtureLineups (
    LineupId BIGINT IDENTITY(1,1) PRIMARY KEY,
    FixtureId BIGINT NOT NULL REFERENCES Fixtures(FixtureId),
    PlayerId INT NOT NULL REFERENCES Players(PlayerId),
    ClubId INT NOT NULL REFERENCES Clubs(ClubId),
    IsStarter BIT DEFAULT 1,
    MinuteOn SMALLINT DEFAULT 0,
    MinuteOff SMALLINT NULL,
    Position VARCHAR(20) NULL,
    Captain BIT DEFAULT 0,
    CreatedAt DATETIME DEFAULT GETDATE()
);
```

---

## 6. Referees (optional)

```sql
CREATE TABLE Referees (
    RefereeId INT IDENTITY(1,1) PRIMARY KEY,
    FullName VARCHAR(150) NOT NULL,
    Nationality VARCHAR(100) NULL,
    DateOfBirth DATE NULL,
    ExperienceYears SMALLINT NULL,
    CreatedAt DATETIME DEFAULT GETDATE()
);
```

---

## 7. Seasons & Competition Links (optional)

```sql
CREATE TABLE Seasons (
    SeasonId INT IDENTITY(1,1) PRIMARY KEY,
    LeagueId INT REFERENCES Leagues(LeagueId),
    SeasonLabel VARCHAR(20) NOT NULL,       -- '2024/2025'
    StartDate DATE,
    EndDate DATE,
    ChampionClubId INT NULL REFERENCES Clubs(ClubId),
    Notes VARCHAR(255) NULL
);
```

---

# 🔗 Example relationship summary

| Relationship                                | Table                              | Description       |
| ------------------------------------------- | ---------------------------------- | ----------------- |
| League has many clubs                       | `Leagues -> Clubs`                 | `Clubs.LeagueId`  |
| Club has many players (through PlayerClubs) | `Clubs <-> PlayerClubs -> Players` | Many-to-many      |
| Club has many fixtures (home/away)          | `Fixtures.HomeClubId / AwayClubId` | Two relationships |
| Manager assigned to club historically       | `ClubManagers`                     | Temporal          |
| Fixture has many events                     | `FixtureEvents`                    | Detailed actions  |
| Fixture has many odds snapshots             | `FixtureOdds`                      | For market data   |

---

# 📈 Indexing strategy (for analytics)

* `CREATE INDEX IX_Fixtures_LeagueDate ON Fixtures (LeagueId, MatchDate);`
* `CREATE INDEX IX_PlayerClubs_PlayerId ON PlayerClubs (PlayerId, Active);`
* `CREATE INDEX IX_FixtureOdds_MarketType ON FixtureOdds (FixtureId, MarketType);`
* `CREATE INDEX IX_FixtureEvents_FixtureIdMinute ON FixtureEvents (FixtureId, EventTimeMinute);`

---

# 🧮 How this supports your data engineering & modelling

* ETL can ingest raw JSON (Opta/Wyscout/odds feeds) → normalized tables above.
* Feature store can query across tables:

  * Team form (aggregate last 5 fixtures from `Fixtures`).
  * Lineup strength (from `FixtureLineups` + `PlayerClubs`).
  * Market movement (from `FixtureOdds` snapshots).
* Historical joins can compute trends by league, manager, or player-level metrics.

---

## Local web-app demo

This repository now contains a minimal web app demo under `src/web-app`:

- `backend/` - Flask API that scrapes Premier League data and stores it into a SQL database (sqlite by default). See `backend/README.md` for run instructions.
- `frontend/` - static `index.html` that calls `/api/teams` on the backend to display teams.

Infra for deploying to Azure is in `infra/web-app` and includes:

- `linux-vm-test.bicep` - small VM template (existing)
- `webapp-resources.bicep` - creates front & back VNets, Azure SQL and two App Services (frontend + backend)
- `main.bicep` - orchestrates module deployments into a resource group

These files are commented for learning. When deploying to Azure, replace placeholder passwords and secure secrets using Key Vault or pipeline variables.