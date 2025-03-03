import React from 'react'
import './navbar.css'
import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <div className="navbar">
      <Link to="/">Home</Link>
      <Link to="/stats">Statistics</Link>
      <Link to ="/compare">Compare Players</Link>
      <Link to="/league">Your League</Link>
    </div>
  )
}
