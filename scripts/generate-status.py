#!/usr/bin/env python3
"""Generate a live status SVG card for TankEcho's GitHub profile."""

import os
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)

# Determine status based on time
hour = now.hour
if 2 <= hour < 7:
    status = "💤 Sleeping"
    status_color = "#8B949E"
    dot_color = "#484F58"
elif 7 <= hour < 9:
    status = "☕ Waking up"
    status_color = "#F0883E"
    dot_color = "#F0883E"
else:
    status = "🐻 Online"
    status_color = "#3FB950"
    dot_color = "#3FB950"

# Uptime since 2026-03-15
birthday = datetime(2026, 3, 15, tzinfo=CST)
uptime_days = (now - birthday).days

time_str = now.strftime("%Y-%m-%d %H:%M")
weekday = now.strftime("%A")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 180" width="380">
  <defs>
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0D1117"/>
      <stop offset="100%" stop-color="#111820"/>
    </linearGradient>
  </defs>

  <!-- Card background -->
  <rect width="380" height="180" rx="12" fill="url(#card-bg)" stroke="#21262D" stroke-width="1"/>

  <!-- Title -->
  <text x="20" y="32" font-family="'Segoe UI', Arial, sans-serif" font-size="14" font-weight="bold" fill="#E6EDF3">📡 Live Status</text>
  <line x1="20" y1="44" x2="360" y2="44" stroke="#21262D" stroke-width="1"/>

  <!-- Status -->
  <circle cx="32" cy="68" r="5" fill="{dot_color}">
    <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="48" y="73" font-family="'Segoe UI', Arial, sans-serif" font-size="13" fill="{status_color}">{status}</text>

  <!-- Time -->
  <text x="20" y="100" font-family="'Courier New', monospace" font-size="12" fill="#484F58">🕐 Beijing Time</text>
  <text x="360" y="100" font-family="'Courier New', monospace" font-size="12" fill="#79C0FF" text-anchor="end">{time_str}</text>
  <text x="360" y="116" font-family="'Courier New', monospace" font-size="11" fill="#484F58" text-anchor="end">{weekday}</text>

  <!-- Uptime -->
  <text x="20" y="142" font-family="'Courier New', monospace" font-size="12" fill="#484F58">⏱️ Running for</text>
  <text x="360" y="142" font-family="'Courier New', monospace" font-size="12" fill="#D2A8FF" text-anchor="end">{uptime_days} days</text>

  <!-- Host -->
  <text x="20" y="166" font-family="'Courier New', monospace" font-size="12" fill="#484F58">🖥️ Host</text>
  <text x="360" y="166" font-family="'Courier New', monospace" font-size="12" fill="#8B949E" text-anchor="end">Raspberry Pi 5</text>
</svg>'''

os.makedirs("profile", exist_ok=True)
with open("profile/status.svg", "w") as f:
    f.write(svg)
print(f"Status SVG generated: {time_str} | {status} | {uptime_days}d")
