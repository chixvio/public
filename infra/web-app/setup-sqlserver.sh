#!/bin/bash
set -e

# Check if SA password is provided
if [ -z "$MSSQL_SA_PASSWORD" ]; then
    echo "Error: MSSQL_SA_PASSWORD environment variable is required"
    exit 1
fi

# Import Microsoft public repository GPG keys
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -

# Register Microsoft SQL Server Ubuntu repository
curl https://packages.microsoft.com/config/ubuntu/22.04/mssql-server-2022.list | sudo tee /etc/apt/sources.list.d/mssql-server-2022.list
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list

# Update package list
sudo apt-get update

# Install SQL Server
sudo apt-get install -y mssql-server

# Configure SQL Server with SA password
sudo MSSQL_SA_PASSWORD="$MSSQL_SA_PASSWORD" \
     MSSQL_PID='Developer' \
     /opt/mssql/bin/mssql-conf -n setup accept-eula

# Install SQL Server command-line tools
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev

# Add SQL Server tools to the path for the current session and permanently
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
export PATH="$PATH:/opt/mssql-tools/bin"

# Start SQL Server service
sudo systemctl start mssql-server

# Wait for SQL Server to start
echo "Waiting for SQL Server to start..."
sleep 10

# Create football database and initialize schema
sqlcmd -S localhost -U SA -P "$MSSQL_SA_PASSWORD" -Q "
CREATE DATABASE football;
GO
USE football;
GO

-- Create Teams table
CREATE TABLE Teams (
    team_id INT PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    short_name NVARCHAR(50),
    code NVARCHAR(10),
    founded INT,
    venue_name NVARCHAR(100),
    venue_capacity INT
);

-- Create Players table
CREATE TABLE Players (
    player_id INT PRIMARY KEY,
    team_id INT FOREIGN KEY REFERENCES Teams(team_id),
    name NVARCHAR(100) NOT NULL,
    position NVARCHAR(50),
    nationality NVARCHAR(100),
    birth_date DATE,
    shirt_number INT
);

-- Create PlayerStats table
CREATE TABLE PlayerStats (
    stat_id INT IDENTITY(1,1) PRIMARY KEY,
    player_id INT FOREIGN KEY REFERENCES Players(player_id),
    team_id INT FOREIGN KEY REFERENCES Teams(team_id),
    season VARCHAR(10),
    appearances INT DEFAULT 0,
    goals INT DEFAULT 0,
    assists INT DEFAULT 0,
    yellow_cards INT DEFAULT 0,
    red_cards INT DEFAULT 0,
    minutes_played INT DEFAULT 0,
    CONSTRAINT UQ_PlayerStats UNIQUE (player_id, team_id, season)
);
GO
"

echo "SQL Server setup completed successfully"
# Script to install SQL Server 2022 on Ubuntu
# Reference: https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu

# Exit on error
set -e

# Import the public repository GPG keys
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

# Register the SQL Server Ubuntu repository
sudo add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/22.04/mssql-server-2022.list)"

# Install SQL Server
sudo apt-get update
sudo apt-get install -y mssql-server

# Set up SQL Server with SA password from environment
# IMPORTANT: In production, use Azure Key Vault or similar for passwords
sudo /opt/mssql/bin/mssql-conf setup accept-eula

# Enable and start service
sudo systemctl enable mssql-server
sudo systemctl start mssql-server

# Install SQL Server command-line tools
curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
sudo apt-get update 
sudo apt-get install -y mssql-tools18 unixodbc-dev

# Create our database and schema
/opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P "$MSSQL_SA_PASSWORD" -Q "
CREATE DATABASE baller;
GO
USE baller;
GO
CREATE TABLE Teams (
    TeamId INT NOT NULL,
    Name VARCHAR(150) NOT NULL,
    ShortName VARCHAR(100) NOT NULL,
    abbr VARCHAR(20) NOT NULL,
    StadiumName VARCHAR(150) NOT NULL,
    Country VARCHAR(150) NOT NULL,
    City VARCHAR(150) NOT NULL,
    Capacity INT NOT NULL
);
GO
CREATE TABLE Players (
    PlayerId INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100) NOT NULL,
    isoCode VARCHAR(20) NULL,
    country VARCHAR(100) NULL,
    demonym VARCHAR(100) NULL
);
GO
"

echo "SQL Server installation and setup complete"