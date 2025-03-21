import React, { useState, useEffect } from 'react'
import './home.css'

export default function Home() {
  const [data, setData] = useState([]);
  const [example, setExample] = useState([false, false])
  const [leagueId, setLeagueId] = useState('');
  const [teamId, setTeamId] = useState('');

  useEffect(() => {
    fetch('/src/scripts/outputs/full_data.csv')
      .then(response => response.text())
      .then(result => {
        toArray(result);
      })
      .catch(error => {
        console.error('Error getting data');
      });
  }, []);

  const toArray = (csvData) => {
    let newData = csvData.split('\n').slice(1);
    newData = newData.map(row => row.split(','));
    newData = newData.sort((a, b) => b[28] - a[28])
    setData(newData);
  }

  const getTop5Players = () => {
    return data.slice(0, 5).map(player => ({
      name: player[0],
      fppg: player[28]
    }));
  }

  const changeExample = (index) => {
    let newExample = [...example];
    newExample[index] = !newExample[index];
    setExample(newExample);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('http://localhost:5000/run-script', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ leagueId, teamId }),
    });

    const result = await response.json();
    localStorage.setItem('fantasyData', JSON.stringify(result));
    window.location.href = '/league';
  };

  return (
    <div className="home-container">
      <div className="header">
        This is my tool for ESPN H2H fantasy basketball. To get started, check out below.
      </div>
      <div style={{display: 'flex', justifyContent: 'space-between'}}>
        <div className="home-box" style={{width: "30%"}}>
          <div style={{marginBottom: "10px"}}>Top performers</div>
          {getTop5Players().map((player, index) => (
            <div key={index} className="top-performers">
              {player.name} - {player.fppg}
            </div>
          ))}
          <button style={{marginTop: "10px", width: "150px"}} onClick ={() => window.location.href = '/stats'}>See Full Statistics</button>
        </div>
        <div className="fantasy-box">
          <div className="home-espn-league">
            <div style={{marginBottom: "10px"}}>Have an ESPN team?</div>
            <form className="fantasy-form" onSubmit={handleSubmit}>
              <input
                type="text"
                value={leagueId}
                onChange={(e) => setLeagueId(e.target.value)}
                placeholder="League ID"
              />
              <input
                type="text"
                value={teamId}
                onChange={(e) => setTeamId(e.target.value)}
                placeholder="Team ID"
              />
              <button type="submit">See Team</button>
            </form>
          </div>
        </div>
        <div className="new-box">
          <div>
            <div>New to fantasy?</div>
            <div>Fantasy sports is where players “draft” real sports players to teams to compete against other teams for better statistics. Check out <a href="https://www.rotowire.com/basketball/advice/">this guide</a> and how to play.</div>
          </div>
        </div>
      </div>
      <div className="info-boxes">
        <div className="about-box">
          <h4>How do you find your league and team ID on for ESPN fantasy?</h4>
          <div className="howto">
            <div>
              <div>If you're on desktop, the two ID's should be a paramateres in the link of your fantasy team page. Simply log in, click on the desired team, and look at the link.</div>
              <div className="home-example">
                {example[0] ? (
                  <div style={{width: "200px"}} onClick={() => changeExample(0)}>Hide Example</div>
                ) : (
                  <div style={{width: "200px"}} onClick={() => changeExample(0)}>Show Example</div>
                )}
                {example[0] && (
                  <img src="/src/pages/assets/desktophowto.gif" />
                )}
              </div>
            </div>
            <div>
              <div>In the mobile app, the league ID is located in the league info tab, which can be navigated to through My Team-&gt;League-&gt;League Info.</div>
              <div className="home-example">
                {example[1] ? (
                  <div style={{width: "200px"}} onClick={() => changeExample(1)}>Hide Example</div>
                ) : (
                  <div style={{width: "200px"}} onClick={() => changeExample(1)}>Show Example</div>
                )}
                {example[1] && (
                  <img src="/src/pages/assets/mobilehowto.gif" />
                )}
              </div>
            </div>
          </div>
        </div>
        <div className="about-box">
          <h4>What is this website?</h4>
          <div>I first built this site to host my model predictions. Using the Python scikit learn library, I attempted to predict the fantasy points of players with a couple models. You can find the predictions on the <a href="/stats">Statistics page</a> with model 1 currently having around an 80% accuracy rate and model 2 having around a 60% accuracy rate from testing. I also decided to integrate an ESPN fantasy API so you could have all your fantasy information in one place. Feel free to check out the <a href="/league">Fantasy page</a>!</div>
        </div>
      </div>
    </div>
  )
}
