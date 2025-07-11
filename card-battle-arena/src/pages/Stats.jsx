import axios from "axios"
import { useEffect, useState } from "react"
import { Link } from "react-router-dom"


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
    const interval = setInterval(getStats, 3000);
    return () => clearInterval(interval)
  }, [gameId])

  return (
    <div className="p-4 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-4 text-center text-blue-700">Game Stats</h1>
      <div className="mb-2 text-lg text-gray-700 font-semibold">Game ID: <span className="text-blue-500">{gameId}</span></div>

      {/* show winner name on the top */}
      {gameData.WinnerID && (
        <div className="text-2xl font-bold text-green-600 mb-6 text-center bg-green-100 rounded py-2 shadow">
          🎉 Winner: {playersData.find(p => p.PlayerID === gameData.WinnerID)?.Name || gameData.WinnerID}
        </div>
      )}

      <h1 className="text-2xl my-5 font-bold text-gray-800">Players:</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
        {playersData.map((item) => (
          <div key={item.PlayerID} className="border rounded-lg py-4 px-3 bg-white drop-shadow-xl shadow hover:scale-105 transition-transform duration-200">
            <p className="font-semibold text-gray-700 mb-1"><strong>Player Name:</strong> <span className="text-blue-600">{item.Name}</span></p>
            <p className="mb-1"><strong>Player Health:</strong> <span className="text-red-500">{item.Health}</span></p>
            <p className="mb-1"><strong>Player Status:</strong> <span className="text-gray-600">{item.Status}</span></p>
            <p className="mb-1"><strong>Player Shield:</strong> <span className={item.Shield ? "text-green-600" : "text-gray-400"}>{item.Shield ? "YES🛡️" : "NO"}</span></p>
            <p><strong>Cards Left:</strong> <span className="text-purple-600">{item.Hand.length}</span></p>
          </div>
        ))}
      </div>
      <h2 className="mt-8 text-xl font-bold text-center text-red-700">Game Ended</h2>
      <div className="flex justify-center">
        <Link to="/">
          <button className="py-3 px-6 rounded-lg my-6 border border-black drop-shadow-2xl bg-black text-white font-semibold hover:bg-gray-800 transition-colors duration-200">
            Proceed to Home
          </button>
        </Link>
      </div>
    </div>
  )
}

export default Stats