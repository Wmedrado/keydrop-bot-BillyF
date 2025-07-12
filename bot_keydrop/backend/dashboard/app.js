const { useState, useEffect, useRef } = React;

function Dashboard() {
  const [tabs, setTabs] = useState([]);
  const [winnings, setWinnings] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [status, setStatus] = useState(null);
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  const fetchData = () => {
    fetch('/bot/tabs').then(r => r.json()).then(setTabs);
    fetch('/winnings?limit=10').then(r => r.json()).then(setWinnings);
    fetch('/stats/system').then(r => r.json()).then(data => {
      setMetrics(data);
    });
    fetch('/bot/status').then(r => r.json()).then(setStatus);
  };

  useEffect(() => {
    fetchData();
    const id = setInterval(fetchData, 5000);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    if (!metrics) return;
    const labels = ['CPU', 'RAM'];
    const data = [parseFloat(metrics.cpu_percent), parseFloat(metrics.memory_percent)];
    if (!chartInstance.current) {
      chartInstance.current = new Chart(chartRef.current, {
        type: 'bar',
        data: { labels, datasets: [{ label: '%', data }] },
        options: { scales: { y: { beginAtZero: true, max: 100 } } }
      });
    } else {
      chartInstance.current.data.datasets[0].data = data;
      chartInstance.current.update();
    }
  }, [metrics]);

  const controlBot = action => {
    fetch('/bot/control', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action })
    }).then(fetchData);
  };

  return React.createElement('div', {},
    React.createElement('h1', {}, 'Keydrop Dashboard'),
    React.createElement('div', { className: 'section' },
      React.createElement('button', { onClick: () => controlBot('pause') }, 'Pause'),
      React.createElement('button', { onClick: () => controlBot('resume') }, 'Resume'),
      React.createElement('button', { onClick: () => controlBot('stop') }, 'Stop'),
      React.createElement('button', { onClick: () => controlBot('start') }, 'Start')
    ),
    React.createElement('div', { className: 'section' },
      React.createElement('h2', {}, 'System Metrics'),
      React.createElement('canvas', { ref: chartRef, width: 400, height: 200 })
    ),
    React.createElement('div', { className: 'section' },
      React.createElement('h2', {}, 'Active Tabs'),
      React.createElement('table', { className: 'tabs' },
        React.createElement('thead', {},
          React.createElement('tr', {},
            React.createElement('th', {}, 'ID'),
            React.createElement('th', {}, 'Status'),
            React.createElement('th', {}, 'URL')
          )
        ),
        React.createElement('tbody', {},
          tabs.map(t => React.createElement('tr', { key: t.tab_id },
            React.createElement('td', {}, t.tab_id),
            React.createElement('td', {}, t.status),
            React.createElement('td', {}, t.url)
          ))
        )
      )
    ),
    React.createElement('div', { className: 'section' },
      React.createElement('h2', {}, 'Recent Winnings'),
      React.createElement('ul', { className: 'winnings' },
        winnings.map((w, i) => React.createElement('li', { key: i }, `${w.amount} - ${w.lottery_type}`))
      )
    )
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(Dashboard));
