import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <div className="h-screen bg-gradient-to-br from-purple-800 to-pink-500 flex flex-col items-center justify-center text-white">
      <motion.h1 initial={{ opacity: 0, y: -50 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1 }} className="text-6xl font-bold mb-6" >
        ⚔️ Card Battle Arena
      </motion.h1>
      <motion.div className="flex space-x-6" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1 }} >
        <Link to="/create" className="px-8 py-3 bg-white text-black rounded-xl shadow-xl hover:scale-110 transition">
          Create Game
        </Link>
        <Link to="/join" className="px-8 py-3 bg-black border border-white text-white rounded-xl hover:scale-110 transition">
          Join Game
        </Link>
      </motion.div>
    </div>
  );
}