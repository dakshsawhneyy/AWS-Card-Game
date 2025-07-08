import axios from 'axios';
import { useState } from 'react'
import { useNavigate } from 'react-router-dom';


const CreateGame = () => {
    const [playerName, setPlayerName] = useState(""); 
    const navigate = useNavigate();

    const handleCreateGame = async() => {
        try {
            const response = await axios.post("https://a7suws2gr6.execute-api.ap-south-1.amazonaws.com/dev/createGame", { CreatorName: playerName, }) // Sending PlayerName as body
            console.log(response)
            const gameId = response.data.GameID;
            // const playerId = response.data.PlayerID;

            // Save Info to local storage
            localStorage.setItem('gameId',gameId)
            // localStorage.setItem('playerId',playerId)
            
            // Navigate to Lobby
            navigate('/lobby')
        } catch (error) {
            console.error("Error creating game:", error);
            // Handle error (e.g., show a notification)
            alert("Failed to create game. Please try again.");
        }
        
    }

    return (
        <div className='h-screen flex flex-col items-center justify-center bg-gradient-to-br from-green-500 to-teal-500 text-white'>
            <h1 className='text-4xl font-bold mb-8'>Create Game</h1>
            <input type="text" placeholder='Enter your name' value={playerName} onChange={(e) => setPlayerName(e.target.value)} className='p-3 rounded text-black mb-6' />
            <button onClick={handleCreateGame} className='bg-black px-6 py-3 rounded-xl hover:scale-105 transition'>Create</button>
        </div>
  )
}

export default CreateGame
