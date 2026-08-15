import { NavLink } from "react-router-dom";
import "./Sidebar.css";

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <NavLink to="/">Dashboard</NavLink>
      <NavLink to="/prediction">Prediction</NavLink>
      <NavLink to="/analytics">Analytics</NavLink>
      <NavLink to="/portfolio">Portfolio</NavLink>
      <NavLink to="/models">AI Models</NavLink>
      <NavLink to="/news">News</NavLink>
      <NavLink to="/settings">Settings</NavLink>
      <NavLink to="/about">About</NavLink>
    </aside>
  );
};

export default Sidebar;