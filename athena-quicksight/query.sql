SELECT
  item.playername.s AS player_name,
  CAST(item.health.n AS int) AS health,
  item.status.s AS status,
  CAST(item.totalheals.n AS int) AS total_heals,
  CAST(item.totalattacks.n AS int) AS total_attacks,
  CAST(item.totaldamageDealt.n AS int) AS total_damage,
  CAST(item.totalspecial.n AS int) AS total_special,
  item.lastactionat.s AS last_action,
  item.shield.bool AS shield

FROM aws_cardgame_db.cardgame_players
WHERE CAST(item.totalattacks.n AS int) > 0

-- ! total_heals meaning show it as total_heals column in table
-- * CAST convert string to int