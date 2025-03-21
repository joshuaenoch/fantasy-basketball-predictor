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
  const [injuries, setInjuries] = useState([]);
  const [allPlayers, setAllPlayers] = useState([]);
  const [comparingPlayers, setComparingPlayers] = useState([]);
  const [maxStats, setMaxStats] = useState({});
  const [comparingData, setComparingData] = useState([]);
  const [leagueId, setLeagueId] = useState('');
  const [teamId, setTeamId] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = localStorage.getItem('fantasyData');
        setData(JSON.parse(result));
      } catch (error) {
        console.error('Error fetching data or no data:', error);
      }
    };

    const fetchFullData = async () => {
      try {
        const response = await fetch('/src/scripts/outputs/full_data.csv');
        const result = await response.text();
        toArray(result);
      } catch (error) {
        console.error('Error fetching full data:', error);
      }
    };

    const fetchInjuries = async () => {
      try {
        const response = await fetch('/src/scripts/outputs/injuries.json');
        const result = await response.text();
        setInjuries(result);
      } catch (error) {
        console.error('Error fetching injuries:', error);
      }
    };

    fetchData();
    fetchFullData();
    fetchInjuries();
  }, []);

  useEffect(() => {
    if (data) {
      const freeAgents = data.free_agents;
      setFreeAgents(freeAgents);
    }
  }, [data]);

  useEffect(() => {
    const filterAgents = () => {
      let newList = [...allPlayers];
      if (freeAgentsOnly) {
        const freeAgentNames = freeAgents.map(agent => agent.name);
        newList = allPlayers.filter(player => freeAgentNames.includes(player[0]))
      }
      if (hideInjured) {
        newList = newList.filter(player => !injuries.includes(player[0]))
      }
      if(search != '') {
        newList = newList.filter(player => player[0].toLowerCase().includes(search.toLowerCase()))
      }
      setFilteredAgents(newList);
    };

    filterAgents();
  }, [freeAgents, hideInjured, freeAgentsOnly, search]);

  useEffect(() => {
    if(comparingPlayers.length > 1) {
      let maxStats = {};
      comparingPlayers.forEach(player => {
        maxStats["FPPG"] = Math.max(maxStats["FPPG"] || 0, player[28]);
        maxStats["FPPG7"] = Math.max(maxStats["FPPG7"] || 0, player[33]);
        maxStats["FPPG30"] = Math.max(maxStats["FPPG30"] || 0, player[34]);
        maxStats["GP"] = Math.max(maxStats["GP"] || 0, player[7]);
        maxStats["PPG"] = Math.max(maxStats["PPG"] || 0, player[27]);
        maxStats["AST"] = Math.max(maxStats["AST"] || 0, player[22]);
        maxStats["REB"] = Math.max(maxStats["REB"] || 0, player[21]);
        maxStats["STL"] = Math.max(maxStats["STL"] || 0, player[23]);
        maxStats["BLK"] = Math.max(maxStats["BLK"] || 0, player[24]);
        maxStats["TOV"] = Math.max(maxStats["TOV"] || 0, player[25]);
      });
      setMaxStats(maxStats);
    } else {
      setMaxStats({FPPG: -10, FPPG7: -10, FPPG30: -10, GP: -1,PPG: -1, AST: -1, REB: -1, STL: -1, BLK: -1, TOV: -1});
    }

    let newCompData = [...comparingData]
    comparingPlayers.forEach(playerName => {
      const playerStats = allPlayers.find(player => player[0] === playerName);
      if (playerStats) {
        newCompData.push(playerStats);
      }
    });
    setComparingData(newCompData);
    console.log(comparingData);
  }, [comparingPlayers]);

  const toArray = (csvData) => {
    let newData = csvData.split('\n').slice(1);
    newData = newData.map(row => row.split(','));
    let sortedData = [...newData];
    sortedData = sortedData.sort((a, b) => b[28] - a[28]);
    setAllPlayers(sortedData);
    setFilteredAgents(sortedData);
  }

  const addPlayer = (playerName) => {
    const playerData = allPlayers.find(player => player[0] === playerName);

    if (playerData) {
      const isAlreadyAdded = comparingPlayers.some(p => p[0] === playerData[0]);

      if (!isAlreadyAdded) {
        setComparingPlayers([...comparingPlayers, playerData]);
      }
    }
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

  if (data) {
    console.log(data)
    console.log(data.roster)
  } else {
    console.log("bruh")
  }

  return (
    <div style={{margin: '20px'}}>
      <div style={{display: 'flex', justifyContent: 'space-between', width: "100%"}}>
        <div style={{display: 'flex', flexDirection: 'column', gap: '20px', width: "18%"}}>
          <div className="league-box" style={{height: "54vh", overflow: "scroll"}}>
            {data ?
            (<>
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
                    <div style={{display: 'flex'}} onClick={() => addPlayer(player.name)}>
                      <div style={{color: player.injured ? 'red' : 'inherit'}}>{player.name}</div>
                      {player.injured && <div style={{color: 'red'}}>&nbsp;(OUT)</div>}
                    </div>
                    <div>Season FPPG - {player.avg_points}</div>
                    <div>Last 7 FPPG - <span style={{color: player.avg_points_7 > player.avg_points ? 'green' : 'red'}}>{player.avg_points_7}</span></div>
                  </div>
                ))}
              </div>
            </>) : (
              <>
                <div className="league-header">Your Team</div>
                <div style={{color: 'green'}}>? W - ? L (Rank ?/10)</div>
                <hr />
                <div>Enter your league and team ID to see your team</div>
              </>
          )}
          </div>
          <form className="change-team" onSubmit={handleSubmit}>
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
            <div style={{margin: "5px 0", fontSize: "14px"}}><a style={{color: "grey"}} href="./">How to find league and team ID</a></div>
            <button type="submit">Change Team</button>
          </form>
        </div>
        <div style={{display: 'flex', flexDirection: 'column', width: "50%"}}>
          <div className="comparison-box">
            {comparingPlayers.length > 0 ? (
              comparingPlayers.map((player, index) => (
                <div key={index}>
                  <p>{player[0]}</p>
                  <hr className="hr2" />
                  <p style={{color: parseFloat(player[28]) === maxStats["FPPG"] ? "green" : "inherit"}}>
                    FPPG: {player[28]}
                  </p>
                  <p style={{color: parseFloat(player[33]) === maxStats["FPPG7"] ? "green" : "inherit"}}>
                    7 Day FPPG: {player[33]}
                  </p>
                  <p style={{color: parseFloat(player[34]) === maxStats["FPPG30"] ? "green" : "inherit"}}>
                    30 Day FPPG: {player[34]}
                  </p>
                  <hr className="hr2" />
                  <p style={{color: parseFloat(player[7]) === maxStats["GP"] ? "green" : "inherit"}}>
                    GP: {player[7]}
                  </p>
                  <p style={{color: parseFloat(player[27]) === maxStats["PPG"] ? "green" : "inherit"}}>
                    PPG: {player[27]}
                  </p>
                  <p style={{color: parseFloat(player[22]) === maxStats["AST"] ? "green" : "inherit"}}>
                    AST: {player[22]}
                  </p>
                  <p style={{color: parseFloat(player[21]) === maxStats["REB"] ? "green" : "inherit"}}>
                    REB: {player[21]}
                  </p>
                  <p style={{color: parseFloat(player[23]) === maxStats["STL"] ? "green" : "inherit"}}>
                    STL: {player[23]}
                  </p>
                  <p style={{color: parseFloat(player[24]) === maxStats["BLK"] ? "green" : "inherit"}}>
                    BLK: {player[24]}
                  </p>
                  <p style={{color: parseFloat(player[25]) === maxStats["TOV"] ? "red" : "inherit"}}>
                    TOV: {player[25]}
                  </p>
                  <p style={{color: "grey"}} onClick={() => setComparingPlayers(comparingPlayers.filter((p, i) => i !== index))}>
                    Remove
                  </p>
                </div>
              ))
            ) : (
              <div>Click on player's names to begin comparing them</div>
            )}
          </div>
        </div>
        <div style={{display: 'flex', flexDirection: 'column', gap: '20px', width: "18%"}}>
          <div className='league-box' style={{height: "37vh", overflow: "scroll"}}>
              <div className="league-header">Top 10 Free Agents</div>
              <div>Based on games from the last 7 days</div>
              <hr />
              <div style={{
                display: "flex",
                flexDirection: "column",
                gap: "15px"
              }}>
                {data ? (
                  data.top_agents.map((player, index) => (
                    <div key={index} onClick={() => addPlayer(player.name)}>
                      <div>
                        {index + 1}.
                        <span style={{ color: player.injured ? 'red' : 'inherit' }}>
                          {player.name}
                          {player.injured && <span>&nbsp;(OUT)</span>}
                        </span>
                      </div>
                      <div>7 day total points - {player.score}</div>
                      <div>
                        7 day average -&nbsp;
                        <span style={{ color: player.average >= 30 ? 'green' : 'grey' }}>
                          {player.average}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div>Enter your league and team ID to see top agents</div>
                )}
              </div>
          </div>
          <div className='league-box' style={{height: "37vh", overflow: "scroll"}}>
            <div className="league-header">All Players</div>
            <div style={{display: "flex", flexDirection: "column", gap: "10px", margin:"10px 0"}}>
              <div>
                {data && <><input type="checkbox" id="freeAgents" name="freeAgents" onChange={() => setFreeAgentsOnly(!freeAgentsOnly)}/>
                <label for="freeAgents" style={{marginLeft: "5px"}}>Free Agents Only</label></>}
              </div>
              <div>
                <input type="checkbox" id="injured" name="injured" onChange={() => setHideInjured(!hideInjured)}/>
                <label for="injured" style={{marginLeft: "5px"}}>Hide Injured</label>
              </div>
              <input type="text" id="search" name="search" placeholder="Enter player name" style={{width: "90%"}} value={search} onChange={(e) => setSearch(e.target.value)}/>
            </div>
            <div style={{
              display: "flex",
              flexDirection: "column",
              gap: "20px"
            }}>
              {filteredAgents.map((player, index) => (
                <div key={index} onClick={() => addPlayer(player[0])}>
                  <div style={{color: injuries.includes(player[0]) ? 'red' : 'inherit'}}>{player[0]} {injuries.includes(player[0]) && <span>(OUT)</span>}</div>
                  <p>FPPG: {player[28]}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}