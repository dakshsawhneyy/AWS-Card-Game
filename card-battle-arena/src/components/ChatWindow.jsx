import axios from 'axios'
import { useEffect, useState } from 'react'

const ChatWindow = ({gameId, playerId, onClose}) => {

    const [messages, setMessages] = useState([])    // updating messages list as messages gets added
    const [msg, setMsg] = useState("")      // send this new state as a response


    // Fetch Chat Messages
    const fetchMessages = async() => {
        try {
            const response = await axios.get("https://a7suws2gr6.execute-api.ap-south-1.amazonaws.com/dev/getChatMessage",{
                params: {
                    GameID: gameId
                }
            })
            //console.log(response)
            setMessages(response.data.messages)
        } catch (error) {
            console.error(error)
            alert(error.response.data.message || "An unexpected error occurred")
        }
    }

    // send messages
    const sendMessages = async() => {
        try {
            const response = await axios.post("https://a7suws2gr6.execute-api.ap-south-1.amazonaws.com/dev/sendChatMessage",{
                GameID: gameId,
                sender: playerId,
                message: msg     // thats why created new state
            })
            setMsg('')  // empty msg after adding to db
            // fetchMessages()     // refresh chat
        } catch (error) {
            console.error(error)
            alert(error.response.data.message || "An unexpected error occurred")
        }
    }

    // constantly use polling to fetch latest details
    useEffect(() => {
      fetchMessages()
      const interval = setInterval(fetchMessages, 3000);
      return () => clearInterval(interval)
    }, [])

  return (
    <div className='absolute right-4 bottom-4 bg-white border border-gray-400 rounded-lg shadow-lg w-80 h-96 p-4 z-50 flex flex-col'>
        <div className='flex justify-between items-center mb-2'>
            <h2 className='text-lg font-semibold'>Game Chat</h2>
            <button className="text-red-600" onClick={onClose}>✖</button>
        </div>

        <div className='flex-1 overflow-y-auto border rounded p-2 bg-gray-50'>
            { messages && (
                messages.map((item, index) => (
                    <div key={index} className='mb-1'>
                        <strong className=''>{item.sender}:</strong>{item.message}
                    </div>
                ))
            )}
        </div>

        <div className='flex mt-2'>
            <input type='text' placeholder='Enter Message' onChange={(e) => setMsg(e.target.value)} value={msg} className='flex-1 border rounded-l px-2 py-1 text-black'/>
            <button onClick={sendMessages} className='bg-blue-600 text-white px-3 py-1 rounded-r'>Send</button>
        </div>
    </div>
  )
}

export default ChatWindow