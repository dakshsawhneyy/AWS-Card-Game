import React from "react"
import attack from "../assets/attack.png"
import heal from "../assets/heal.png"
import defense from "../assets/defense.png"
import special from "../assets/special.png"

const Card = ({card, onThrow, disabled}) => {
  return (
    <div className={`w-32 h-48 shadow-lg cursor-pointer transition transform hover:scale-105 ${disabled ? "opacity-50 cursor-not-allowed" : ""}`} onClick={!disabled ? () => onThrow(card.CardID,card.Type) : undefined} >
      {/* Differentiating Cards as jsx doesnt have if statements */}
      {card.Type == 'attack' && (
        <img src={attack} alt="Attack Card" className="w-full h-full rounded object-cover" />
      )}
      {card.Type == 'defence' && (
        <img src={defense} alt="Defense Card" className="w-full h-full rounded object-cover" />
      )}
      {card.Type == 'heal' && (
        <img src={heal} alt="Heal Card" className="w-full h-full rounded object-cover" />
      )}
      {card.Type == 'special' && (
        <img src={special} alt="Attack Card" className="w-full h-full rounded object-cover" />
      )}
      
    </div>
  )
}

export default Card