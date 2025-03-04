import React, { useEffect, useState } from 'react';
import './league.css';

export default function FantasyData() {
  const [data, setData] = useState(null);
  const [fullData, setFullData] = useState([]);
  const [freeAgents, setFreeAgents] = useState([]);
  const [filteredAgents, setFilteredAgents] = useState([]);
  const [hideInjured, setHideInjured] = useState(false);
  const [freeAgentsOnly, setFreeAgentsOnly] = useState(false);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/src/scripts/outputs/fantasy_data.json');
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const fetchFullData = async () => {
      try {
        const response = await fetch('/src/scripts/outputs/full_data.csv');
        const result = await response.text();
        setFullData(result);
      } catch (error) {
        console.error('Error fetching full data:', error);
      }
    };

    fetchData();
    fetchFullData();
  }, []);

  useEffect(() => {
    if (data) {
      const freeAgents = data.free_agents;
      setFreeAgents(freeAgents);
    }
  }, [data]);

  useEffect(() => {
    const filterAgents = () => {
      if (hideInjured) {
        setFilteredAgents(freeAgents.filter(player => !player.injured));
      } else {
        setFilteredAgents(freeAgents);
      }
    };

    filterAgents();
  }, [freeAgents, hideInjured]);

  return (
    <div style={{margin: '20px'}}>
      {data ? (
        <div style={{display: 'flex', justifyContent: 'space-between', width: "100%"}}>
          <div style={{display: 'flex', flexDirection: 'column', gap: '20px', width: "18%"}}>
            <div className="league-box">
              <div className="league-header">{data.team_name}</div>
              <div style={{color: data.standing<=4 ? 'green' : 'red'}}>{data.wins} W - {data.losses} L (Rank {data.standing}/10)</div>
              <hr />
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
                gap: '15px'
              }}>
                {data.roster.map((player, index) => (
                  <div key={index}>
                    <div style={{display: 'flex'}}>
                      <div>{player.name}</div>
                      {player.injured && <div style={{color: 'red'}}>&nbsp;(OUT)</div>}
                    </div>
                    <div>Season FPPG - {player.avg_points}</div>
                    <div>Last 7 FPPG - <span style={{color: player.avg_points_7 > player.avg_points ? 'green' : 'red'}}>{player.avg_points_7}</span></div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="comparison-box" style={{display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
                gap: '20px', width: "50%"}}>
            <div>Comparing 1</div>
            <div>Comparing 2</div>
            <div>Comparing 3</div>
            <div>Comparing 4</div>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', gap: '20px', width: "18%"}}>
            <div className='league-box' style={{height: "500px", overflow: "scroll"}}>
                <div className="league-header">Top 10 Free Agents</div>
                <div>Based on games from the last 7 days</div>
                <hr />
                <div style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "15px"
                }}>
                  {data.top_agents.map((player, index) => (
                    <div key={index}>
                      <div>{index+1}. {player.name}</div>
                      <div>7 day total points - {player.score}</div>
                      <div>7 day average - <span style={{color: player.average >= 30 ? 'green' : 'grey'}}>{player.average}</span></div>
                    </div>
                ))}
                </div>
            </div>
            <div className='league-box'>
              <div className="league-header">All Players</div>
              <div style={{display: "flex", flexDirection: "column", gap: "10px", margin:"10px 0"}}>
                <div>
                  <input type="checkbox" id="freeAgents" name="freeAgents" onChange={() => setFreeAgentsOnly(!freeAgentsOnly)}/>
                  <label for="freeAgents" style={{marginLeft: "5px"}}>Free Agents Only</label>
                </div>
                <div>
                  <input type="checkbox" id="injured" name="injured" onChange={() => setHideInjured(!hideInjured)}/>
                  <label for="injured" style={{marginLeft: "5px"}}>Hide Injured</label>
                </div>
                <input type="text" id="search" name="search" placeholder="Enter player name" style={{width: "90%"}} onChange={(e) => setSearchTerm(e.target.value)}/>
              </div>
              <div style={{
                display: "flex",
                flexDirection: "column",
                gap: "20px"
              }}>
                {filteredAgents.map((player, index) => (
                  <div key={index}>
                    <div>{player.name} {player.injured && <span style={{color: 'red'}}>(OUT)</span>}</div>
                    <p>FPPG: {player.avg_points}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
