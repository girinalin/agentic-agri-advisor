> **⚠️ SUPERSEDED** — This document is kept for historical reference.
> The authoritative version is now [docs/02-architecture/hybrid-intelligence-strategy.md](02-architecture/hybrid-intelligence-strategy.md).

---

# 🌾 Hybrid Intelligence Strategy: Optimizing Local, Offline, and Agent Networks

This document details the strategy for combining local edge models (Gemma-2B, in-browser classifiers) and the cloud-based multi-agent network (Krishi Sastri coordinator and specialists) to best serve smallholder farmer communities.

---

## 🏗️ The Hybrid Intelligence Paradigm

To deliver maximum value under network and cost constraints, the platform divides intelligence between the **Edge** (Farmer's Mobile Device) and the **Cloud** (FastAPI backend server):

```
                                  [ Farmer's Query / Photo ]
                                              │
                                              ▼
                                   { Local Query Triage }
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
         [ Simple / Local Intents ]                      [ Complex / Dynamic Intents ]
                      │                                               │
             (Check Connection)                                (Check Connection)
            ┌─────────┴─────────┐                            ┌─────────┴─────────┐
            ▼                   ▼                            ▼                   ▼
        [ Online ]         [ Offline ]                  [ Online ]          [ Offline ]
            │                   │                            │                   │
     (Local Gemma)        (Local Gemma)              (Backend Agents)      (Local Gemma
  Low Latency, $0 Cost     Zero-Data, $0 Cost         RAG, Mandi APIs,     Fallback + Queue)
                                                      Weather Models
```

### 1. The Edge Layer (Local & Offline)
*   **Engine:** MediaPipe WebGenAI (Gemma-2B) + Tasks-Vision (TFLite models) + IndexedDB.
*   **Scope:** Common conversation, instant crop disease classification, traditional remedy lookup, and local state management.
*   **Advantage:** Zero ongoing API query cost, sub-100ms response time, and 100% operational availability during network blackouts.

### 2. The Cloud Layer (Agent Networks & APIs)
*   **Engine:** FastAPI + Google ADK + Specialist Agents (Weather, Market, Crop Analyst) + RAG (Vector indices) + OKF (Ontology database).
*   **Scope:** 7-day microclimate risk modeling, commodity price predictions, vector retrieval over thousands of pages of agronomy manuals, and cross-regional outbreak correlation.
*   **Advantage:** Uncapped compute, access to live third-party APIs, and regional data aggregation.

---

## 🚦 Smart Routing Strategy: Simple vs. Complex

We classify user intents to route queries dynamically:

| Query Type | Classification Criteria | Engine Used (Online) | Engine Used (Offline) |
| :--- | :--- | :--- | :--- |
| **Simple / Chit-Chat** | Greetings ("Hello", "Pranam"), general questions ("Who are you?"). | **Local Gemma** (Saves token cost) | **Local Gemma** |
| **Local Diagnostics** | Photo analysis of leaves, insects, or soil profile questions. | **Local Gemma** + TFLite | **Local Gemma** + TFLite |
| **Traditional Remedy** | Basic organic farming queries ("neem spray mix", "cow manure usage"). | **Local Gemma** | **Local Gemma** |
| **Historical Data** | Profile info, current crop stage, or water logs. | **Local Gemma** (Reads IndexedDB) | **Local Gemma** (Reads IndexedDB) |
| **Live Mandi Prices** | Price comparison ("Wheat price in Nagpur", "soybean trends"). | **Backend Market Agent** (API fetch) | **Local Gemma** (Reads cached data) |
| **Weather Risk Forecasting** | Future hazards ("Will it rain next week?", "frost alerts"). | **Backend Weather Agent** (API fetch) | **Local Gemma** (Reads cached data) |
| **Deep Agronomy Retrieval** | Specialized questions ("chemical composition of fertilizer X"). | **Backend Retriever Agent** (RAG) | **Local Gemma** (General knowledge) |

---

## 💡 New Agricultural Edge Use Cases

### Use Case 1: In-Browser Crop Stage Identification
*   **Action:** The farmer takes a photo of the emerging crop sprout.
*   **Local Processing:** A client-side TFLite model identifies the crop's development phase (e.g., *Vegetative - V3 Stage*).
*   **Gemma Explanation:** The local Gemma model is prompted with: *"The farmer's corn crop has reached the V3 vegetative stage in sandy loam. Explain what nutrients (NPK targets) and watering volume are required this week."*
*   **Digital Twin Sync:** Updates the IndexedDB state, automatically adjusting the local dashboard's irrigation thresholds.

### Use Case 2: Voice-First Field Action Logger
*   **Action:** The farmer taps the microphone and speaks: *"I added wood ash to the hillside field and applied 15 liters of water."*
*   **Local Processing:** Browser Speech Recognition transcribes the voice. Gemma parses the text into a structured action: `{ "treatment": "wood_ash", "irrigation_liters": 15.0 }`.
*   **IndexedDB Cache:** Saves the action directly to the local IndexedDB queue. Once a network connection is found, it automatically synchronizes with the backend SQLite database to update the digital twin.

### Use Case 3: Offline Quarantine & Alert System
*   **Action:** Farmer takes a photo of a highly infectious disease (e.g., *Tomato Late Blight*).
*   **Local Processing:** The TFLite model detects a 90%+ match.
*   **Gemma Action:** Gemma instructs the farmer: *"This disease spreads fast. Isolate the infected plants, prune them, and dispose of them far from the field. I have flagged this to report to neighboring farms as soon as you are back online."*
*   **Online Alert Queue:** Queues a report to the backend `/feedback` telemetry service. Once online, the system logs the pest warning coordinates to help the backend warn nearby farmers.

---

## 🛠️ Implementing Simple/Complex Routing in `dashboard.js`

To implement this smart routing in the client script, we update the triage function to check for keywords representing **Dynamic/Complex** intents (e.g., "price", "mandi", "weather", "rain", "forecast", "predict").

If none of these keywords are present, the query bypasses the backend network entirely and runs locally, reducing server load and API expenses.

```javascript
// Example implementation in ui/agui/dashboard.js
async function handleSend() {
  const text = userInputField.value.trim();
  if (!text) return;

  appendMessage('User', text, 'user-msg');
  userInputField.value = '';

  const preferredLang = document.getElementById('language-selector')?.value || 'English';
  const lowercaseText = text.toLowerCase();

  // Keywords requiring live APIs, RAG, or heavy backend computations
  const complexKeywords = ['price', 'mandi', 'weather', 'rain', 'forecast', 'predict', 'trend', 'market', 'manual', 'sensor'];
  const isComplex = complexKeywords.some(kw => lowercaseText.includes(kw));

  // Auto-route to local Gemma if offline OR if the query is simple/local
  if (!navigator.onLine || !isComplex) {
    const thinkingBubble = appendMessage('Coordinator', 'Thinking...', 'thinking-msg');
    handleOfflineSend(text, preferredLang, thinkingBubble);
    return;
  }

  // Otherwise, route to backend agents...
  const thinkingBubble = appendMessage('Coordinator', 'Thinking...', 'thinking-msg');
  // ... standard online fetch('/run_sse')
}
```

---

## 🎙️ Unified Media & Language Triage (STT, TTS, Translation)

To make voice interactions and translations truly robust, cost-effective, and offline-resilient, the media and translation channels also employ a hybrid Edge-Cloud triage model.

### 1. 🎙️ Speech-to-Text (STT) - Voice Input
*   **Edge Processing (Default):** Uses the browser-native **Web Speech API (`webkitSpeechRecognition`)**.
    *   *Mechanism:* Captures farmer speech in local dialects (Hindi, Marathi, Swahili) and processes it directly on the mobile OS.
    *   *Advantage:* Instant, $0 API costs, works offline if the user has downloaded their local language pack on the phone.
*   **Cloud Processing (Online Fallback):** If browser-native recognition fails or is unsupported for a dialect (e.g. Swahili on legacy web viewports), the raw audio stream is sent to the backend `stt` MCP server for processing.

### 2. 🔊 Text-to-Speech (TTS) - Voice Output
*   **Edge Processing (Default/Offline):** Uses the browser-native **SpeechSynthesis API (`window.speechSynthesis`)**.
    *   *Mechanism:* Scans available system voice files (`speechSynthesis.getVoices()`), matches the dialect code (e.g., `hi-IN`), prioritizes high-quality local male voices, and plays back locally.
    *   *Advantage:* 100% free, zero lag, and runs completely offline.
*   **Cloud Processing (Online Fallback):** If the browser lacks local voice files for Marathi or Swahili, it fetches high-fidelity, natural neural voice streams from the FastAPI `/api/tts` endpoint using the `edge-tts` python module.

### 3. 🌐 Language Translation
*   **Edge Processing (Default/Offline):**
    *   *UI Localization:* UI text, charts, and metrics labels are translated instantly client-side using static translation lists (`TRANSLATIONS` map in `dashboard.js`) without reloading pages.
    *   *General Prompts:* Gemma-2B translates user prompts or responses client-side.
*   **Cloud Processing (Online Fallback):** For highly technical or complex sentences, the backend coordinates with the `translation` MCP server (using Gemini cloud translation models) to ensure accurate translation before routing to specialized agents.

---

## ⚙️ Gemma as the Client-Side Intelligent Orchestrator

Instead of static thresholds, the local **Gemma model acts as an Intelligent Client-Side Orchestrator**. Upon startup or connectivity changes, Gemma inspects the system state to negotiate the **optimal configuration** of local vs. cloud media and reasoning resources.

### Dynamic Resource Negotiation Scenarios:

1.  **🔋 Power-Saving & Thermal Moderation:**
    *   *Inputs:* Battery Level (low, <15%), thermal throttling flags, WebGPU processing times.
    *   *Gemma Logic:* If battery is critical, Gemma recommends shutting down client-side GPU model rendering and automatically shifts reasoning to the Cloud Agent network (if online) or falls back to the lightweight local lexicon (if offline) to preserve the farmer's battery.
2.  **📶 Network Cost & Speed Auto-balancing:**
    *   *Inputs:* Network connection type (3G, 4G, 5G, Wi-Fi), latency measurements, telemetry queue size.
    *   *Gemma Logic:* If on a high-cost/slow 3G network, Gemma limits cloud synchronization frequency and routes standard queries locally. If on free Wi-Fi, it triggers full IndexedDB database synchronization and initiates premium cloud neural TTS voice streams.
3.  **🗣️ Multilingual Voice Package Diagnostics:**
    *   *Inputs:* `speechSynthesis.getVoices()` inventory list, user's language selection, native browser translation APIs.
    *   *Gemma Logic:* Gemma queries system capabilities. If Marathi is selected and a local high-quality neural voice is found, Gemma configures native browser playback. If missing, it instructs the UI to request the `/api/tts` backend stream.
4.  **🧠 Semantic Triage Router:**
    *   *Inputs:* Farmer's natural language question.
    *   *Gemma Logic:* Gemma parses the query type locally (e.g., classifying if the intent is a simple instruction, a diagnostic explanation, or a dynamic pricing query). It sets routing flags directly in the browser runtime:
        *   `Route: Local` ➔ Fast local response, bypasses network.
        *   `Route: Backend` ➔ Transmits payload to cloud agent pipelines.
