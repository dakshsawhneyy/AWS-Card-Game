import React from 'react'

const PlayerCard = ({playerInfo, currentTurn,myTurn}) => {
  return (
    <div className={`bg-white rounded-xl shadow-md p-4 text-black flex flex-col items-center w-50 transition ${currentTurn ? "border-4 border-red-600" : ""}`}>
      <h3 className="font-bold text-lg">{playerInfo.Name}</h3>
      <p><strong>Health: </strong>{playerInfo.Health}</p>
      <p><strong>Shield: </strong>{playerInfo.Shield ? "🛡️ Active" : "Not Active"}</p>
      <p><strong>Deck Size: </strong>{playerInfo.HandSize}</p>
      {myTurn && <p className="text-green-500 font-semibold">Your Turn!</p>}
    </div>
  )
}

export default PlayerCard