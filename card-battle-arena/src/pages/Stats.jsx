import axios from "axios"
import { useEffect, useState } from "react"


const Stats = () => {
  const [gameData, setGameData] = useState({})
  const [playersData, setPlayersData] = useState([])
  
  const gameId = localStorage.getItem('gameId')

  const getStats = async() => {
    try {
      const response = await axios.get("https://a7suws2gr6.execute-api.ap-south-1.amazonaws.com/dev/gameStats", {
        params: {
          GameID: gameId,
        }
      })
      setGameData(response.data)
      console.log(response.data)

      // Get Players Info
      setPlayersData(response.data.Players)
    } catch (error) {
      console.error("Error fetching game stats:", error);
      alert(error.response.data.message || "An unexpected error occurred")
    }
  }

  useEffect(() => {
    getStats();
    const interval = setTimeout(getStats, 3000);
    return () => clearInterval(interval)
  }, [gameId])

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold mb-4">Game Stats</h1>
      <div className="mb-2">Game ID: {gameId}</div>
      <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
        {playersData.map((item) => (
          <div key={item.PlayerID} className="border rounded py-4 px-2 drop-shadow-xl shadow">
            <p><strong>Player Name:</strong> {item.Name}</p>
            <p><strong>Player Health:</strong> {item.Health}</p>
            <p><strong>Player Status:</strong> {item.Status}</p>
            <p><strong>Player Shield:</strong> {item.Shield ? "YES🛡️" : "NO"}</p>
            <p><strong>Cards Left:</strong> {item.Hand.length}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Stats