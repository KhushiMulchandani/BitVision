import { useState } from "react";
import "./Navbar.css";

import logo from "../../assets/logo.png";

import { FaMoon, FaSun } from "react-icons/fa";
import { Link } from "react-router-dom";

function Navbar() {

  const [darkMode, setDarkMode] = useState(false);

  return (

    <header className="navbar">

      {/* Logo */}

      <div className="logo">

        <img src={logo} alt="BitVision Logo" />

        <span>BitVision</span>

      </div>

      {/* Navigation */}

      <nav>

        <ul className="nav-links">
  <li><Link to="/">Home</Link></li>

  <li><Link to="/prediction">Prediction</Link></li>

  <li><Link to="/analytics">Analytics</Link></li>

  <li><Link to="/models">Models</Link></li>

  <li><Link to="/about">About</Link></li>
</ul>

      </nav>

      {/* Right */}

      <div className="nav-right">

        <button
          className="theme-btn"
          onClick={() => setDarkMode(!darkMode)}
        >

          {darkMode ? <FaSun /> : <FaMoon />}

        </button>

        <button className="login-btn">

          Login

        </button>

      </div>

    </header>

  );

}

export default Navbar;