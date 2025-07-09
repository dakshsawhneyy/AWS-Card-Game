import React from "react"

const Card = ({card, onThrow, disabled}) => {
  return (
    <div className={`w-32 h-48 bg-white text-black rounded-xl shadow-lg flex flex-col justify-center items-center cursor-pointer transition transform hover:scale-105 ${disabled ? "opacity-50 cursor-not-allowed" : ""}`} onClick={!disabled ? () => onThrow(card.CardID,card.Type) : undefined} >
      <p className="font-bold">{card.Type.toUpperCase()}</p>
      <p className="text-xs">{card.CardID}</p>
    </div>
  )
}

export default Card