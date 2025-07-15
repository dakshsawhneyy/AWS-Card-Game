CREATE OR REPLACE aws_cardgame_db.cardgame_players AS
SELECT
    item.PlayerID.S              AS player_id,
    item.PlayerName.S            AS player_name,
    item.GameID.S                AS game_id,
    CAST(item.Health.N AS int)   AS health,
    item.Status.S                AS status,
    item.Shield.BOOL             AS shield,
    item.LastActionAt.S          AS last_action,
    CAST(item.TotalHeals.N AS int)        AS total_heals,
    CAST(item.TotalSpecial.N AS int)      AS total_special,
    CAST(item.TotalAttacks.N AS int)      AS total_attacks,
    CAST(item.TotalDamageDealt.N AS int)  AS total_damage
FROM aws_cardgame_db.cardgame_players;

-- ? quicksight doesn't understand nested queries, so we need to flatten it
-- * THis is created as a view table, so quicksight can easily see it