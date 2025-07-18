import React from "react"
import attack from "../assets/attack.png"
import heal from "../assets/heal.png"
import defense from "../assets/defense.png"
import special from "../assets/special.png"
import special2 from "../assets/special2.png"
import Tilt from 'react-parallax-tilt'

const Card = ({card, onThrow, disabled}) => {
  return (
    <Tilt  glareEnable glareMaxOpacity={0.2} scale={1.05} transitionSpeed={400} className="rounded-2xl backdrop-blur-md shadow-xl transition-all" >
      <div className={`w-32 h-48 shadow-lg cursor-pointer transition drop-shadow-3xl transform hover:scale-105 ${disabled ? "opacity-50 cursor-not-allowed" : ""}`} onClick={!disabled ? () => onThrow(card.CardID,card.Type) : undefined} >
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
          <img src={special2} alt="Attack Card" className="w-full h-full rounded object-cover" />
        )}
      </div>
    </Tilt>
  )
}

export default Card