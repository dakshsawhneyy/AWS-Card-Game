import axios from "axios";
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom";


const Lobby = () => {
  
  const [players, setPlayers] = useState([]);
  const gameId = localStorage.getItem('gameId')
  const playerId = localStorage.getItem('playerId')
  const navigate = useNavigate()

  // for updating stats every 3 second, fetching latest details of players
  useEffect(() => {
    const fetchLobby = async() => {
      try {
        const response = await axios.get("https://a7suws2gr6.execute-api.ap-south-1.amazonaws.com/dev/gameStats", {
          params: {
            GameID: gameId,
          }
        })
        setPlayers(response.data.Players || []);    // Add players to players list for retrival of their names
        // console.log(response)
      } catch (error) {
        console.error(error)
        alert()
      }
    }
    
    fetchLobby();
    const interval = setInterval(fetchLobby, 3000);
    return() => clearInterval(interval)
  }, [gameId])

  // Function for handling start game
  const handleStartGame = async() => {
    try {
      await axios.post("https://a7suws2gr6.execute-api.ap-south-1.amazonaws.com/dev/startGame",{
        GameID: gameId,
        PlayerID: playerId,
      })
      navigate('/game');
    } catch (error) {
      console.error("Error starting game:", error);
      alert(error.response.data.message || "An unexpected error occurred")
    }
  }

  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gradient-to-br from-pink-500 to-purple-600 text-white">
      <h1 className="text-5xl font-bold mb-6">Lobby</h1>
      <h3 className="text-2xl font-bold mb-6">GameID: {gameId}</h3>
      
      {/* Looping through players array, to list their names */}
      {players.map((item,index) => (
        <li key={index} className="">{item.Name}</li>
      ))}
      <button onClick={handleStartGame} className="bg-black px-6 py-3 rounded-xl hover:scale-105 transition">Start Game</button>
    </div>
  )
}

export default Lobby