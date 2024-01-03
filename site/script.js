const teams = [
    { name: 'Team A', winPercentage: 0.7 },
    { name: 'Team B', winPercentage: 0.6 },
    { name: 'Team C', winPercentage: 0.5 },
    // Add more teams here
  ];
  
  const teamsContainer = document.getElementById('teams');
  
  teams.forEach(team => {
    const teamElement = document.createElement('div');
    teamElement.className = 'team';
    teamElement.textContent = `${team.name}: ${Math.round(team.winPercentage * 100)}%`;
    teamsContainer.appendChild(teamElement);
  });
  