import React, { useEffect, useState } from 'react';
import './predictions.css';

export default function Predictions() {
  const [data, setData] = useState([]);
  const [sorted, setSorted] = useState("");

  useEffect(() => {
    fetch('/test_predictions.csv')
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

    if (sorted === "fppg") {
      sortedData = sortedData.sort((a, b) => b[1] - a[1]);
    } else if (sorted === "pfppg") {
      sortedData = sortedData.sort((a, b) => b[2] - a[2]);
    }

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
            <th onClick = {() => setSorted("")}>Name</th>
            <th onClick = {() => setSorted("fppg")}>FPPG</th>
            <th onClick = {() => setSorted("pfppg")}>Projected FPPG</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row[0]}</td>
              <td>{row[1]}</td>
              <td>{row[2]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
