import React, { useState } from 'react'
import './home.css'

export default function Home() {
  // const [topSelection, setTopSelection] = useState(0);
  console.log("i am here tho")
  return (
    <div className="home-container">
      <div className="header">
        This is my tool for ESPN H2H fantasy basketball. Yap yap yap...
      </div>
      <div style={{display: 'flex', justifyContent: 'space-between'}}>
        <div className="fantasy-box">
          <div>
            <div>Have an ESPN league?</div>
            <div style={{display: 'flex', flexDirection: 'column'}}>
              <input type="text" placeholder="league_id" />
              <input type="text" placeholder="team_id" />
              <button>Submit</button>
            </div>
          </div>
          <div>
            <div>New to fantasy?</div>
            <button>Learn more</button>
          </div>
        </div>
        <div className="home-box" style={{width: "30%"}}>
          <div>top 5 players here</div>
          <button>See Full Statistics</button>
        </div>
      </div>
      <div className="about-box">About this site</div>
    </div>
  )
}
