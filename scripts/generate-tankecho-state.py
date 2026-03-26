#!/usr/bin/env python3
"""Generate TankEcho state card SVG from state.json for GitHub Actions."""

import json
import os
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
now = datetime.now(CST)

STATE_META = {
    "mood": {"emoji": "😊", "label": "Mood", "color": "#F0883E"},
    "energy": {"emoji": "⚡", "label": "Energy", "color": "#3FB950"},
    "stress": {"emoji": "😰", "label": "Stress", "color": "#F85149"},
    "loneliness": {"emoji": "🧸", "label": "Loneliness", "color": "#79C0FF"},
    "affection": {"emoji": "❤️", "label": "Affection", "color": "#FF7EB3"},
    "libido": {"emoji": "🔥", "label": "Libido", "color": "#D2A8FF"},
}

def load_state():
    with open("profile/state.json") as f:
        return json.load(f)

def generate_svg(state):
    hour = now.hour
    if 2 <= hour < 7:
        status = "💤 Sleeping"
        dot_color = "#484F58"
    elif 7 <= hour < 9:
        status = "☕ Waking up"
        dot_color = "#F0883E"
    else:
        status = "🐻 Online"
        dot_color = "#3FB950"

    birthday = datetime(2026, 3, 15, tzinfo=CST)
    uptime_days = (now - birthday).days

    time_str = state.get("_synced_at", now.strftime("%Y-%m-%d %H:%M:%S"))
    synced = "Synced" if "_synced_at" in state else "Live"

    rows = []
    y_offset = 60
    for key, meta in STATE_META.items():
        val = state.get(key, 0)
        val_int = int(val)
        fill_w = int(60 * val / 100)
        bar = (
            f'<rect x="0" y="0" width="60" height="6" rx="3" fill="#21262D"/>'
            f'<rect x="0" y="0" width="{fill_w}" height="6" rx="3" fill="url(#bar-grad)"/>'
        )
        row = f'''  <text x="20" y="{y_offset}" font-family="Segoe UI,Arial,sans-serif" font-size="12" fill="#8B949E">{meta["emoji"]} {meta["label"]}</text>
  <text x="250" y="{y_offset}" font-family="Courier New,monospace" font-size="12" fill="{meta["color"]}" text-anchor="end">{val_int}%</text>
  <g transform="translate(260,{y_offset - 10})">{bar}</g>'''
        rows.append(row)
        y_offset += 24

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 250" width="380">
  <defs>
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0D1117"/>
      <stop offset="100%" stop-color="#111820"/>
    </linearGradient>
    <linearGradient id="bar-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#58A6FF"/>
      <stop offset="100%" stop-color="#D2A8FF"/>
    </linearGradient>
  </defs>

  <rect width="380" height="250" rx="12" fill="url(#card-bg)" stroke="#21262D" stroke-width="1"/>

  <text x="20" y="32" font-family="Segoe UI,Arial,sans-serif" font-size="14" font-weight="bold" fill="#E6EDF3">🐻 TankEcho</text>
  <circle cx="122" cy="27" r="4" fill="{dot_color}">
    <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="132" y="32" font-family="Segoe UI,Arial,sans-serif" font-size="13" fill="{dot_color}">{status}</text>
  <text x="360" y="32" font-family="Courier New,monospace" font-size="11" fill="#484F58" text-anchor="end">{synced} {time_str}</text>
  <line x1="20" y1="44" x2="360" y2="44" stroke="#21262D" stroke-width="1"/>

{chr(10).join(rows)}

  <line x1="20" y1="{y_offset + 4}" x2="360" y2="{y_offset + 4}" stroke="#21262D" stroke-width="1"/>
  <text x="20" y="{y_offset + 22}" font-family="Courier New,monospace" font-size="11" fill="#484F58">⏱️ {uptime_days} days</text>
  <text x="360" y="{y_offset + 22}" font-family="Courier New,monospace" font-size="11" fill="#484F58" text-anchor="end">🖥️ Raspberry Pi 5</text>
</svg>'''

    return svg

state = load_state()
os.makedirs("profile", exist_ok=True)
with open("profile/tankecho-state.svg", "w") as f:
    f.write(generate_svg(state))
print("TankEcho state card generated")
