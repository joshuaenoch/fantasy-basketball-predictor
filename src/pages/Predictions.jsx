import React, { useEffect, useState } from 'react';
import './predictions.css';

export default function Predictions() {
  const [data, setData] = useState([]);
  const [sorted, setSorted] = useState("");
  const standardRuleset = {
    "Points": 1,
    "Assists": 2,
    "Rebounds": 1,
    "Blocks": 4,
    "Steals": 4,
    "Turnovers": -2,
    "FGM": 2,
    "FGA": -1,
    "FTM": 1,
    "FTA": -1,
    "3PM": 1,
  }
  const [isStandard, setIsStandard] = useState(true);
  const [customRuleset, setCustomRuleset] = useState(standardRuleset);
  const [search, setSearch] = useState("");
  const [filteredData, setFilteredData] = useState(data);

  useEffect(() => {
    fetch('/src/scripts/computed_data/new-2024-2025.csv')
      .then(response => response.text())
      .then(result => {
        toArray(result);
      })
      .catch(error => {
        console.error('Error getting data');
      });
  }, []);

  useEffect(() => {
    setFilteredData(data);
  }, [data]);

  useEffect(() => {
    let sortedData = [...filteredData];

    sortedData = sortedData.sort((a, b) => b[sorted] - a[sorted]);

    setFilteredData(sortedData);
  }, [sorted]);

  useEffect(() => {
    let filteredData = [...data];
    if (search) {
      filteredData = filteredData.filter(row => row[0].toLowerCase().includes(search.toLowerCase()));
    }
    setFilteredData(filteredData);
  }, [search]);

  console.log(search)

  const toArray = (csvData) => {
    let newData = csvData.split('\n').slice(1);
    newData = newData.map(row => row.split(','));
    setData(newData);
  }

  return (
    <div style={{display: "flex", padding: "40px"}}>
      <div style={{marginRight: "30px", minWidth: "150px", maxWidth: "250px"}}>
        <div className="checkboxes" style={{display: "flex", flexDirection: "column", marginBottom: "20px", gap: "10px"}}>
          <div>
            <label for="model1" style={{marginRight: "5px"}}>Model 1</label>
            <input type="checkbox" id="model1" name="model1" value="model1" />
          </div>
          <div>
            <label for="model1" style={{marginRight: "5px"}}>Model 2</label>
            <input type="checkbox" id="model2" name="model2" value="model2" />
          </div>
          <div>
            <label for="fullstats" style={{marginRight: "5px"}}>Show Full Stats</label>
            <input type="checkbox" id="fullstats" name="fullstats" value="fullstats" />
          </div>
        </div>
        <div>
          <select name="ruleset" id="ruleset" onChange={(e) => setIsStandard(e.target.value === "standard")}W>
            <option value="standard">Standard Ruleset</option>
            <option value="custom">Custom Ruleset</option>
          </select>
          <div>
            {Object.entries(customRuleset).map(([key, value]) => (
              isStandard ? (<div style={{margin: "10px 0", display: "flex"}}>
                <div style={{marginRight: "5px"}}>{key} = </div>
                <div>{value}</div>
              </div>) : (
              <div style={{margin: "10px 0"}}>
                <label style={{marginRight: "5px"}} for={key}>{key}</label>
                <input type="number" id={key} name={key} min="0" max="99" value={value}/>
              </div>
              )
            ))}
            <button>Apply</button>
          </div>
        </div>
      </div>
      <div>
      </div>
      <div style={{overflowX: "auto", width: "100%"}}>
        <input type="text" placeholder="Search for player" value={search} onChange={(e) => setSearch(e.target.value)}/>
        <table>
          <thead>
            <tr>
              <th onClick = {() => setSorted(0)} className={sorted === 0 ? "sorted" : ""}>Name</th>
              <th onClick = {() => setSorted(5)} className={sorted === 5 ? "sorted" : ""}>Team</th>
              <th onClick = {() => setSorted(28)} className={sorted === 28 ? "sorted" : ""}>FPPG</th>
              <th onClick = {() => setSorted(7)} className={sorted === 7 ? "sorted" : ""}>Games Played</th>
              <th onClick = {() => setSorted(8)} className={sorted === 8 ? "sorted" : ""}>Games Started</th>

              <th onClick = {() => setSorted(27)} className={sorted === 27 ? "sorted" : ""}>PPG</th>
              <th onClick = {() => setSorted(9)} className={sorted === 9 ? "sorted" : ""}>MPG</th>
              <th onClick = {() => setSorted(10)} className={sorted === 10 ? "sorted" : ""}>FGM</th>
              <th onClick = {() => setSorted(11)} className={sorted === 11 ? "sorted" : ""}>FGA</th>
              <th onClick = {() => setSorted(13)} className={sorted === 13 ? "sorted" : ""}>3PM</th>
              <th onClick = {() => setSorted(14)} className={sorted === 14 ? "sorted" : ""}>3PA</th>
              <th onClick = {() => setSorted(16)} className={sorted === 16 ? "sorted" : ""}>FTM</th>
              <th onClick = {() => setSorted(17)} className={sorted === 17 ? "sorted" : ""}>FTA</th>
              <th onClick = {() => setSorted(21)} className={sorted === 21 ? "sorted" : ""}>REB</th>
              <th onClick = {() => setSorted(22)} className={sorted === 22 ? "sorted" : ""}>AST</th>
              <th onClick = {() => setSorted(23)} className={sorted === 23 ? "sorted" : ""}>STL</th>
              <th onClick = {() => setSorted(24)} className={sorted === 24 ? "sorted" : ""}>BLK</th>
              <th onClick = {() => setSorted(25)} className={sorted === 25 ? "sorted" : ""}>TOV</th>
            </tr>
          </thead>
          <tbody>
            {filteredData.map((row, index) => (
              <tr key={index}>
                <td className={sorted === 0 ? "sorted" : ""}>{row[0]}</td>
                <td className={sorted === 5 ? "sorted" : ""}>{row[5]}</td>
                <td className={sorted === 28 ? "sorted" : ""}>{row[28]}</td>
                <td className={sorted === 7 ? "sorted" : ""}>{row[7]}</td>
                <td className={sorted === 8 ? "sorted" : ""}>{row[8]}</td>

                <td className={sorted === 27 ? "sorted" : ""}>{row[27]}</td>
                <td className={sorted === 9 ? "sorted" : ""}>{row[9]}</td>
                <td className={sorted === 10 ? "sorted" : ""}>{row[10]}</td>
                <td className={sorted === 11 ? "sorted" : ""}>{row[11]}</td>
                <td className={sorted === 13 ? "sorted" : ""}>{row[13]}</td>
                <td className={sorted === 14 ? "sorted" : ""}>{row[14]}</td>
                <td className={sorted === 16 ? "sorted" : ""}>{row[16]}</td>
                <td className={sorted === 17 ? "sorted" : ""}>{row[17]}</td>
                <td className={sorted === 21 ? "sorted" : ""}>{row[21]}</td>
                <td className={sorted === 22 ? "sorted" : ""}>{row[22]}</td>
                <td className={sorted === 23 ? "sorted" : ""}>{row[23]}</td>
                <td className={sorted === 24 ? "sorted" : ""}>{row[24]}</td>
                <td className={sorted === 25 ? "sorted" : ""}>{row[25]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
