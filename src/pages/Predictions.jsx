import React, { useEffect, useState } from 'react';
import './predictions.css';

export default function Predictions() {
  const [data, setData] = useState([]);
  const [sorted, setSorted] = useState("");

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
    let sortedData = [...data];

    sortedData = sortedData.sort((a, b) => b[sorted] - a[sorted]);

    setData(sortedData);
  }, [sorted]);

  const toArray = (csvData) => {
    let newData = csvData.split('\n').slice(1);
    newData = newData.map(row => row.split(','));
    setData(newData);
  }

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th onClick = {() => setSorted(0)}>Name</th>
            <th onClick = {() => setSorted(5)}>Team</th>
            <th onClick = {() => setSorted(28)}>FPPG</th>
            <th onClick = {() => setSorted(7)}>Games Played</th>
            <th onClick = {() => setSorted(8)}>Games Started</th>
            <th onClick = {() => setSorted(27)}>PPG</th>
            <th onClick = {() => setSorted(9)}>MPG</th>
            <th onClick = {() => setSorted(10)}>FGM</th>
            <th onClick = {() => setSorted(11)}>FGA</th>
            <th onClick = {() => setSorted(13)}>3PM</th>
            <th onClick = {() => setSorted(14)}>3PA</th>
            <th onClick = {() => setSorted(16)}>FTM</th>
            <th onClick = {() => setSorted(17)}>FTA</th>
            <th onClick = {() => setSorted(21)}>REB</th>
            <th onClick = {() => setSorted(22)}>AST</th>
            <th onClick = {() => setSorted(23)}>STL</th>
            <th onClick = {() => setSorted(24)}>BLK</th>
            <th onClick = {() => setSorted(25)}>TOV</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row[0]}</td>
              <td>{row[5]}</td>
              <td>{row[28]}</td>
              <td>{row[7]}</td>
              <td>{row[8]}</td>
              <td>{row[27]}</td>
              <td>{row[9]}</td>
              <td>{row[10]}</td>
              <td>{row[11]}</td>
              <td>{row[13]}</td>
              <td>{row[14]}</td>
              <td>{row[16]}</td>
              <td>{row[17]}</td>
              <td>{row[21]}</td>
              <td>{row[22]}</td>
              <td>{row[23]}</td>
              <td>{row[24]}</td>
              <td>{row[25]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
