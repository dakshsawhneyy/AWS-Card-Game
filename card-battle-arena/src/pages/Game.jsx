import axios from "axios";
import { useEffect, useState } from "react"
import Card from "../components/Card";
import PlayerCard from "../components/PlayerCard";
import { Link, useNavigate } from "react-router-dom";
import { toast } from 'react-toastify';
import ChatWindow from "../components/ChatWindow";

const Game = () => {

  const [gameInfo, setGameInfo] = useState({}); 
  const [playerInfo, setPlayerInfo] = useState({});
  const [hand, setHand] = useState([]); 
  const [message, setMessage] = useState("");   // to show messages like Card Drawn, Card Thrown 
  const [currentTurnPlayer, setCurrentTurnPlayer] = useState("")  // store the name of player whose current turn is going on

  const [showChat, setShowChat] = useState(false)

  const navigate = useNavigate()

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
      // console.log(response.data)

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
      
      // if Game Status is ended, navigate directly to stats
      if(response.data.Status == 'ended'){
        navigate('/stats')
      }

    } catch (error) {
      console.error(error)
      alert(error.response.data.message || "An unexpected error occurred")
    }
  }

  // use effect to change values as game stats changes
  useEffect(() => {
    fetchGame();
    const interval = setInterval(fetchGame, 2500);
    return () => clearInterval(interval)
  }, [])
  
  // useEffect(() => {
  //   const ws = new WebSocket("wss://evpfijv179.execute-api.ap-south-1.amazonaws.com/dev-ws/")

  //   ws.onopen = () => {
  //     console.log("WebSocket connection established");
  //   }

  //   ws.onmessage = (message => {
  //     const data = JSON.parse(message.data)
  //     console.log("WebSocket message received:", data)

  //     // update states
  //     setGameInfo(data)

  //     const pInfo = data.Players.find(p => p.PlayerID === playerId)
  //     setPlayerInfo(pInfo)
  //     setHand(pInfo.Hand)

  //     const cpname = data.Players.find(p => p.PlayerID === data.CurrentTurn)?.Name
  //     setCurrentTurnPlayer(cpname)

  //     // if Game Status is ended, navigate directly to stats
  //     if(data.Status == 'ended'){
  //       navigate('/stats')
  //     }

  //     // Send Message (optional)
  //     setMessage("Game state updated via WebSocket")
  //   })

  //   ws.onerror = (error) => {
  //     console.error("WebSocket error:", error)
  //   }

  //   ws.onclose = () => {
  //     console.log("Disconnected from WebSocket")
  //   }

  //   return () => ws.close();
  // }, [])


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
      alert(error.response.data.message || "An unexpected error occurred")
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
      alert(error.response.data.message || "An unexpected error occurred")
    }
  }

  // End Game logic
  const endGame = async() => {
    try {
      const response = await axios.post("https://a7suws2gr6.execute-api.ap-south-1.amazonaws.com/dev/endGame",{
        GameID: gameId,
        PlayerID: playerId,
      })
      toast.success("Game ended successfully!")
      navigate('/stats')
    } catch (error) {
      console.error(error)
      alert(error.response.data.message || "An unexpected error occurred")
    }
  }

  const isMyTurn = gameInfo.CurrentTurn === playerId;   // return true or false and be used for playing turn of player

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-400 to-pink-500 flex flex-col items-center py-8 text-white">
      <h1 className="text-4xl font-bold mb-4">Game Arena</h1>

      <h1 className="text-3xl font-bold">Players:</h1>
      
      {/* Show All Players Cards, by mapping app items in gameInfo.Players -> load all data and show as card */}
      <div className="flex flex-wrap justify-center gap-4 my-3">
        {gameInfo.Players?.map((item) => (
          <PlayerCard key={item.Name} playerInfo={item} currentTurn={gameInfo.CurrentTurn === item.PlayerID} playerId={playerId}/>
        ))}
      </div>

      { /* Show Current Player All Cards */ }
      <div className="flex flex-wrap justify-center gap-2 mb-6">
        {hand.map((item) => (
          <Card key={item.CardID} card={item} onThrow={throwCard} disabled={!isMyTurn} />
        ))}
      </div>

      <button onClick={drawCard} className={`px-6 py-3 rounded-xl transition ${isMyTurn ? "bg-black hover:scale-105" : "bg-gray-600 cursor-not-allowed"}`}>Draw a Card</button>

      {message && <p className="mt-4">{message}</p>}

      <button className={`absolute top-4 right-4 bg-gray-800 text-white px-4 py-2 rounded-lg shadow ${!showChat ? "text-black" : "disabled opacity-0 pointer-events-none"}`} onClick={() => setShowChat(true)}>Show Chat</button>

      {/* Showing Show Chat Box */}
      {showChat && (
        <ChatWindow gameId={gameId} playerId={playerId} onClose={() => setShowChat(false)} />
      )}

      { /* End Game Button, Calling of End Game API */}
      <button className="mt-4 bg-red-600 hover:bg-red-800 px-6 py-3 rounded-xl transition" onClick={endGame}>END GAME</button>
    </div>
  )
}

export default Game