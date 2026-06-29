# Agent-to-User Interface (A2UI)

A2UI is a declarative user interface protocol. AI agents send JSON payloads describing interface widgets, which are parsed and rendered locally on the client.

## Folder Structure

* `index.html`: Dev entrypoint/test harness for verifying agent declarative UI payloads.
* `app.js`: Script containing the schema parser that turns declarative JSON payloads into HTML components.
* `styles.css`: Styling for the declarative UI components (cards, forms, gauges).
