const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const API_KEY = process.env.API_FOOTBALL_KEY;
const API_BASE = 'https://v3.football.api-sports.io';

// In-memory cache so we don't hammer the rate limit
const cache = {};
const CACHE_TTL = 60 * 1000; // 60 seconds

async function apiFetch(url) {
  const now = Date.now();
  if (cache[url] && now - cache[url].ts < CACHE_TTL) {
    return cache[url].data;
  }
  const res = await fetch(url, { headers: { 'x-apisports-key': API_KEY } });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  const data = await res.json();
  cache[url] = { ts: now, data };
  return data;
}

app.use(express.static(path.join(__dirname, 'frontend')));

app.get('/api/fixtures', async (req, res) => {
  if (!API_KEY) return res.status(503).json({ error: 'API_FOOTBALL_KEY not set' });
  try {
    const data = await apiFetch(`${API_BASE}/fixtures?league=1&season=2026`);
    res.json(data);
  } catch (e) {
    res.status(502).json({ error: e.message });
  }
});

app.get('/api/standings', async (req, res) => {
  if (!API_KEY) return res.status(503).json({ error: 'API_FOOTBALL_KEY not set' });
  try {
    const data = await apiFetch(`${API_BASE}/standings?league=1&season=2026`);
    res.json(data);
  } catch (e) {
    res.status(502).json({ error: e.message });
  }
});

// Live-only fixtures — short TTL so in-progress scores refresh quickly
const LIVE_STATUSES = ['1H','HT','2H','ET','BT','P','INT'];
const LIVE_TTL = 30 * 1000; // 30 seconds

app.get('/api/live', async (req, res) => {
  if (!API_KEY) return res.status(503).json({ error: 'API_FOOTBALL_KEY not set' });
  try {
    const url = `${API_BASE}/fixtures?league=1&season=2026&live=all`;
    const now = Date.now();
    if (cache[url] && now - cache[url].ts < LIVE_TTL) {
      return res.json(cache[url].data);
    }
    const apiRes = await fetch(url, { headers: { 'x-apisports-key': API_KEY } });
    if (!apiRes.ok) throw new Error(`API error ${apiRes.status}`);
    const data = await apiRes.json();
    cache[url] = { ts: now, data };
    res.json(data);
  } catch (e) {
    res.status(502).json({ error: e.message });
  }
});

app.listen(PORT, () => console.log(`Server on port ${PORT}`));
