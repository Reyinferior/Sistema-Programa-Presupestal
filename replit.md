# Sistema Programa Presupuestal

A budget program monitoring dashboard for **Hospital San José**.

## Overview

This is a Google Apps Script (GAS) project that, when deployed in Google Workspace, connects to a Google Sheet and displays budget execution data for "Programas Presupuestales" (sheets prefixed with "PP ").

In Replit, the app is served as a static HTML page with a mock `google.script.run` shim that provides sample data so the UI can be viewed and developed without a live Google Sheets connection.

## Project Structure

- `sistema_ppr.html` — Main frontend: dashboard UI with sidebar, KPI cards, Chart.js bar chart, and detail table
- `codigogs.txt` — Google Apps Script backend code (to be deployed in Google Apps Script editor alongside the HTML)
- `server.py` — Lightweight Python HTTP server that serves the HTML with an injected mock `google.script` object for Replit preview

## Tech Stack

- **Frontend:** Vanilla HTML/CSS/JavaScript, Chart.js v4.4.3 (via CDN)
- **Backend (production):** Google Apps Script
- **Dev server (Replit):** Python 3 `http.server`

## Running

The `Start application` workflow runs `python3 server.py` on port 5000.

## Deploying to Google Apps Script

1. Open your Google Sheet
2. Go to Extensions → Apps Script
3. Paste the contents of `codigogs.txt` as `Code.gs`
4. Create a new HTML file named `index` and paste the contents of `sistema_ppr.html`
5. Deploy → New deployment → Web app
   - Execute as: Me
   - Access: Anyone
