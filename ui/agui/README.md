# Antigravity Dashboard UI (AGUI)

AGUI is the main visual dashboard interface for the Agentic Agriculture Advisor (AAA). It establishes the event loop connection to stream agent thoughts, execution steps, and final recommendations.

## Folder Structure

* `index.html`: Web-based dashboard application UI showing maps, telemetry stats, and the agent chat panel.
* `dashboard.js`: Coordinates the event-driven communication (using SSE or websockets simulation) to stream and render agent outputs and accept manual user inputs or confirmations.
* `styles.css`: Styles for the dashboard layout and visual elements.
