import axios from "axios"
import { useState } from "react"
import { useNavigate } from "react-router-dom"


const JoinGame = () => {
  const [playerName, setPlayerName] = useState("");
  const [gameId, setGameId] = useState("");
  const navigate = useNavigate();

  const handleJoinGame = async() => {
    try {
      const response = await axios.post("https://a7suws2gr6.execute-api.ap-south-1.amazonaws.com/dev/joinGame",{
        GameID: gameId, PlayerName: playerName,
      })
      const playerId = await response.data.PlayerID;
      console.log(response)

      localStorage.setItem("gameId", gameId)
      localStorage.setItem('playerId', playerId)
      localStorage.setItem('playerName',playerName)
      
      navigate('/lobby');
    } catch (error) {
      console.error("Error joining game:", error)
      alert(error.response.data.message || "Cannot join game. Please try again.")
    }
  }

  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-500 to-indigo-500 text-white">
      <h1 className="text-4xl font-bold mb-8">Join Game</h1>
      <input type="text" placeholder="Enter your name" value={playerName} onChange={(e) => setPlayerName(e.target.value)} className="p-3 rounded text-black mb-4" />
      <input type="text" placeholder="Enter Game ID" value={gameId} onChange={(e) => setGameId(e.target.value)} className="p-3 rounded text-black mb-6" />
      <button onClick={handleJoinGame} className="bg-black px-6 py-3 rounded-xl hover:scale-105 transition">Join</button>
    </div>
  )
}

export default JoinGame
