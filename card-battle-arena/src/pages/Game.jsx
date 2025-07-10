import axios from "axios";
import { useEffect, useState } from "react"
import Card from "../components/Card";
import PlayerCard from "../components/PlayerCard";

const Game = () => {

  const [gameInfo, setGameInfo] = useState({}); 
  const [playerInfo, setPlayerInfo] = useState({});
  const [hand, setHand] = useState([]); 
  const [message, setMessage] = useState("");   // to show messages like Card Drawn, Card Thrown 
  const [currentTurnPlayer, setCurrentTurnPlayer] = useState("")  // store the name of player whose current turn is going on

  // fetch gameId and playerId from local storage
  const gameId = localStorage.getItem('gameId')
  const playerId = localStorage.getItem('playerId')

  // fetch gameInfo and playerInfo from gameStats API
  const fetchGame = async() => {
    try {
      const response = await axios.get("https://a7suws2gr6.execute-api.ap-south-1.amazonaws.com/dev/gameStats",{
        params: {
          GameID: gameId
        }
      })
      setGameInfo(response.data)
      console.log(response.data)

      // Find current player stats with its id -- traverse in data and compare matching id and fetch its data
      const pInfo = response.data.Players.find(p => p.PlayerID === playerId)
      setPlayerInfo(pInfo)
      setHand(pInfo.Hand)

      // console.log(pInfo.Hand)
      // console.log(pInfo)

      // Fetch current turn player name
      const cturn = response.data.CurrentTurn   // fetch player id whose current turn is going
      const cpname = response.data.Players.find(p => p.PlayerID === cturn) // Compare this id with All Players ID, and then fetch its name
      setCurrentTurnPlayer(cpname.Name)
      
    } catch (error) {
      console.error(error)
      alert(error.response.data.message || "An unexpected error occurred")
    }
  }

  // use effect to change values as game stats changes
  useEffect(() => {
    fetchGame();
    const interval = setInterval(fetchGame, 3000);
    return () => clearInterval(interval)
  }, [])

  // draw card function
  const drawCard = async() => {
    try {
      const response = await axios.post("https://a7suws2gr6.execute-api.ap-south-1.amazonaws.com/dev/drawCard",{
        GameID: gameId,
        PlayerID: playerId,
      })
      setMessage("Card drawn!") 
      fetchGame()
    } catch (error) {
      console.error(error)
      alert(error.response.message || "An unexpected error occurred")
    }
  }
  
  // Throw card function
  const throwCard = async(cardId,cardName) => {
    try {
      const response = await axios.post("https://a7suws2gr6.execute-api.ap-south-1.amazonaws.com/dev/throwCard",{
        GameID: gameId,
        PlayerID: playerId,
        CardID: cardId,
      })
      setMessage("Card thrown: " + cardName);
      fetchGame();
    } catch (error) {
      console.error(error)
      alert(error.response.message || "An unexpected error occurred")
    }
  }

  const isMyTurn = gameInfo.CurrentTurn === playerId;   // return true or false and be used for playing turn of player

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-400 to-pink-500 flex flex-col items-center p-8 text-white">
      <h1 className="text-4xl font-bold mb-4">Game Arena</h1>

      <h1 className="text-3xl font-bold">Players:</h1>
      
      {/* Show All Players Cards, by mapping app items in gameInfo.Players -> load all data and show as card */}
      <div className="flex flex-wrap justify-center gap-4 my-3">
        {gameInfo.Players?.map((item) => (
          <PlayerCard key={item.Name} playerInfo={item} currentTurn={gameInfo.CurrentTurn === item.PlayerID} playerId={playerId}/>
        ))}
      </div>

      { /* Show Current Player All Cards */ }
      <div className="flex flex-wrap justify-center gap-4 mb-6">
        {hand.map((item) => (
          <Card key={item.CardID} card={item} onThrow={throwCard} disabled={!isMyTurn} />
        ))}
      </div>

      <button onClick={drawCard} className={`px-6 py-3 rounded-xl transition ${isMyTurn ? "bg-black hover:scale-105" : "bg-gray-600 cursor-not-allowed"}`}>Draw a Card</button>

      {message && <p className="mt-4">{message}</p>}
    </div>
  )
}

export default Game