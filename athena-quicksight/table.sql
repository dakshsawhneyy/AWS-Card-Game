CREATE EXTERNAL TABLE IF NOT EXISTS `aws_cardgame_db`.`cardgame_players` (
-- since our json is nested, we need to use struct and inside map it with keys
  item struct<      -- struct is a box that groups multiple things
    PlayerID: struct<S: string>,    
    PlayerName: struct<S: string>,  -- in JSON, PlayerName looks like "PlayerName": { "S": "Daksh" }
    GameID: struct<S: string>, 
    Health: struct<N: string>,  -- N means number
    Status: struct<S: string>,
    Shield: struct<BOOL: boolean>,
    LastActionAt: struct<S: string>,
    TotalHeals: struct<N: string>,
    TotalSpecial: struct<N: string>,
    TotalAttacks: struct<N: string>,
    TotalDamageDealt: struct<N: string>
  >
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json' = 'FALSE',
  'dots.in.keys' = 'FALSE',
  'case.insensitive' = 'TRUE'
)
LOCATION 's3://aws-cardgame-metrics-bucket/players-data/AWSDynamoDB/-//data/'   -- as per your data
TBLPROPERTIES ('classification' = 'json');