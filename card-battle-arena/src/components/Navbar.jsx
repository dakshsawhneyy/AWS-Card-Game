import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <div className="bg-black text-white flex gap-6 px-6 py-4 shadow-lg">
      <Link to="/" className="hover:text-yellow-400">Home</Link>
      <Link to="/create" className="hover:text-yellow-400">Create Game</Link>
      <Link to="/join" className="hover:text-yellow-400">Join Game</Link>
      <Link to="/stats" className="hover:text-yellow-400">Stats</Link>
    </div>
  );
};

export default Navbar;
