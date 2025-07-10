import React from 'react'

const PlayerCard = ({playerInfo, currentTurn, playerId}) => {
  const isMyCard = playerInfo.PlayerID === playerId   // kya jo card selected hai woh mera hai
  const isMyTurn = currentTurn && isMyCard  // kya meri turn hai aur woh card mera selected hai, agr han toh uspr Your Turn Likho

  return (
    <div className={`bg-white rounded-xl shadow-md p-4 text-black flex flex-col items-center w-50 transition ${currentTurn ? "border-4 border-red-600" : ""}`}>
      <h3 className="font-bold text-lg">{playerInfo.Name}</h3>
      <p><strong>Health: </strong>{playerInfo.Health}</p>
      <p><strong>Shield: </strong>{playerInfo.Shield ? "🛡️ Active" : "Not Active"}</p>
      <p><strong>Deck Size: </strong>{playerInfo.HandSize}</p>
      {isMyTurn && <p className="text-green-500 font-semibold">Your Turn!</p>}
    </div>
  )
}

export default PlayerCard