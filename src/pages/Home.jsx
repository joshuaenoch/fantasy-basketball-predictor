import React, { useState, useEffect } from 'react'
import './home.css'

export default function Home() {
  const [data, setData] = useState([]);
  const [example, setExample] = useState([false, false])

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

  console.log("i am here tho")
  return (
    <div className="home-container">
      <div className="header">
        This is my tool for ESPN H2H fantasy basketball. To get started, check out below.
      </div>
      <div style={{display: 'flex', justifyContent: 'space-between'}}>
        <div className="fantasy-box">
          <div className="home-espn-league">
            <div style={{marginBottom: "10px"}}>Have an ESPN league?</div>
            <div className="fantasy-form">
              <input type="text" placeholder="League ID" />
              <input type="text" placeholder="Team ID" />
              <button>Submit</button>
            </div>
          </div>
          <div className="top-questions">
            <div>
              <div>New to fantasy?</div>
              <button onClick={() => window.location.href = 'https://www.rotowire.com/basketball/advice/'}>Learn more</button>
            </div>
            <div>
              <div>How to find team and league ID:</div>
              <button onClick={() => document.querySelector('.howto').scrollIntoView({ behavior: 'smooth' })}>Read below</button>
            </div>
          </div>
        </div>
        <div className="home-box" style={{width: "30%"}}>
          <div style={{marginBottom: "10px"}}>Top performers</div>
          {getTop5Players().map((player, index) => (
            <div key={index} className="top-performers">
              {player.name} - {player.fppg}
            </div>
          ))}
          <button style={{marginTop: "10px", width: "150px"}}>See Full Statistics</button>
        </div>
      </div>
      <div className="about-box">
        <h4>How do you find your league and team ID on for ESPN fantasy?</h4>
        <div className="howto">
          <div>
            <div>If you're on desktop, the two ID's should be a paramateres in the link of your fantasy team page. Simply log in, click on the desired team, and look at the link.</div>
            <div className="home-example">
              {example[0] ? (
                <div onClick={() => changeExample(0)}>Hide Example</div>
              ) : (
                <div onClick={() => changeExample(0)}>Show Example</div>
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
                <div onClick={() => changeExample(1)}>Hide Example</div>
              ) : (
                <div onClick={() => changeExample(1)}>Show Example</div>
              )}
              {example[1] && (
                <img src="/src/pages/assets/mobilehowto.gif" />
              )}
            </div>
          </div>
        </div>
      </div>
      <div className="info-boxes">
        <div className="about-box">
          <h4>How does fantasy even work?</h4>
          <div>If you're new to fantasy sports, here is a quick breakdown of how a H2H fantasy league works. Just like a real sports league, a fantasy league consists of players who act as managers over their own team. After players "draft" or select their own team based on real players of that sport, teams will face off against one another in week long matchups to see which team wins based on real statistics. For a further explanaition of how fantasy works, check out <a href="https://www.rotowire.com/basketball/advice/">this website</a>.</div>
        </div>
        <div className="about-box">
          <h4>What is this website?</h4>
          <div>I first built this site to host my model predictions. Using the Python scikit learn library, I attempted to predict the fantasy points of players with a couple models. You can find the predictions on the <a href="/stats">Statistics page</a> with model 1 currently having around an 80% accuracy rate and model 2 having around a 60% accuracy rate from testing. I also decided to integrate an ESPN fantasy API so you could have all your fantasy information in one place. Feel free to check out the <a href="/league">Fantasy page</a>!</div>
        </div>
      </div>
    </div>
  )
}
