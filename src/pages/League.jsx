import React, { useEffect, useState } from 'react';

export default function FantasyData() {
  const [data, setData] = useState(null);

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

    fetchData();
  }, []);

  return (
    <div style={{margin: '20px'}}>
      {data ? (
        <div>
          <h2>Team</h2>
          <p>{data.team_name}</p>
          <p>Wins: {data.wins}</p>
          <p>Losses: {data.losses}</p>
          <p>Standing: {data.standing}</p>
          <h2 style={{ marginTop: '20px' }}>Roster</h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
            gap: '20px'
          }}>
            {data.roster.map((player, index) => (
              <div key={index}>
                <p>Name: {player.name}</p>
                <p>Position: {player.position}</p>
                <p>FPPG: {player.avg_points}</p>
                <p>Injured: {player.injured ? 'Yes' : 'No'}</p>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
