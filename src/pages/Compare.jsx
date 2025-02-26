import React, { useEffect, useState } from 'react'

export default function Compare() {

  const [data, setData] = useState([]);

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
    let sortedData = [...newData];
    sortedData = sortedData.sort((a, b) => b[28] - a[28]);
    setData(sortedData);
  }

  return (
    <div>
      <div className="player_list">
        {data.map((player, index) => (
          <div key={index}>
            <p>{player[0]}</p>
            <p>{player[28]}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
