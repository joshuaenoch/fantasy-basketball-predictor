import React, { useEffect, useState } from 'react'

export default function Compare() {

  const [data, setData] = useState([]);
  const [comparingPlayers, setComparingPlayers] = useState([]);
  const [maxStats, setMaxStats] = useState({});

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

  useEffect(() => {
    if(comparingPlayers.length > 1) {
      let maxStats = {};
      comparingPlayers.forEach(player => {
        maxStats["FPPG"] = Math.max(maxStats["FPPG"] || 0, player[28]);
        maxStats["PPG"] = Math.max(maxStats["PPG"] || 0, player[27]);
        maxStats["AST"] = Math.max(maxStats["AST"] || 0, player[22]);
        maxStats["REB"] = Math.max(maxStats["REB"] || 0, player[21]);
      });
      setMaxStats(maxStats);
      console.log(maxStats);
    } else {
      setMaxStats({FPPG: -10, PPG: -1, AST: -1, REB: -1});
    }
  }, [comparingPlayers]);

  const toArray = (csvData) => {
    let newData = csvData.split('\n').slice(1);
    newData = newData.map(row => row.split(','));
    let sortedData = [...newData];
    sortedData = sortedData.sort((a, b) => b[28] - a[28]);
    setData(sortedData);
  }

  const addPlayer = (player) => {
    if(!comparingPlayers.find(p => p[0] === player[0])) {
      setComparingPlayers([...comparingPlayers, player]);
    }
  }

  return (
    <div style={{display: "flex", gap: "20px", margin: "20px"}}>
      <div className="player_list" style={{display: "flex", flexDirection: "column", gap: "10px"}}>
        {data.map((player, index) => (
          <div key={index} onClick={() => addPlayer(player)}>
            <p>{player[0]}</p>
            <p>{player[28]}</p>
          </div>
        ))}
      </div>
      <div className="comparing_place" style={{display: "flex", gap: "10px"}}>
        {comparingPlayers.map((player, index) => (
          <div key={index}>
            <p>{player[0]}</p>
            <p style={{backgroundColor: parseFloat(player[28]) === maxStats["FPPG"] ? "green" : "white"}}>FPPG: {player[28]}</p>
            <p style={{ backgroundColor: parseFloat(player[27]) === maxStats.PPG ? "green" : "white" }}>
              PPG: {player[27]}
            </p>
            <p style={{backgroundColor: parseFloat(player[22]) === maxStats["AST"] ? "green" : "white"}}>AST: {player[22]}</p>
            <p style={{backgroundColor: parseFloat(player[21]) === maxStats["REB"] ? "green" : "white"}}>REB: {player[21]}</p>
            <p onClick={() => setComparingPlayers(comparingPlayers.filter((p, i) => i !== index))}>Remove</p>
          </div>
        ))}
      </div>
    </div>
  )
}
