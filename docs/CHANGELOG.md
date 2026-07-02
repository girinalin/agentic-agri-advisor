# 📜 Project History of Changes & Transformations

This document maintains a running history of all architectural upgrades, bug fixes, PWA conversions, and edge intelligence integrations in the **Agentic Agriculture Advisor (AAA)** codebase.

---

## 📅 July 01, 2026

### 1. 🧠 Progressive Web App (PWA) & Offline Capability
*   **Installable Application Manifest ([ui/manifest.webmanifest](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/ui/manifest.webmanifest)):**
    *   Added support for home screen installation, configured brand green themes (`#2C6B37`), standalone viewports, and launch short-cuts for diagnostics and irrigation planners.
*   **Asset Pre-caching Service Worker ([ui/sw.js](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/ui/sw.js)):**
    *   Caches crucial HTML templates, stylesheets, JS files, and Outfit google web fonts.
    *   Employs a **cache-first** caching policy for static assets and a **network-first** policy for profiles.
    *   Exposes custom fallback JSON mock payloads when offline to ensure uvicorn API routes don't crash.
*   **Startup Register:** Updated the main landing page ([ui/agui/index.html](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/ui/agui/index.html)) to register the service worker thread and link the manifest headers.

### 2. 📷 Client-Side Camera Capture Viewfinder
*   **Rear Camera prioritize stream ([ui/agui/camera.js](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/ui/agui/camera.js)):**
    *   Accesses system media streams utilizing `navigator.mediaDevices.getUserMedia()`, prioritizes the rear lens (`facingMode: "environment"`), and captures frames on a canvas block.
*   **Upload File Fallback:** Integrates standard local upload buttons (`<input type="file">`) when camera access is blocked or unsupported.
*   **Modal Viewer Panels:** Created visual modal viewfinder overlay frames, capture snapshots, and analyze indicators directly within the chat portals.

### 3. 🔬 Edge AI & Visual Pathology Models
*   **Browser GenAI Inference Manager ([ui/agui/local_models.js](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/ui/agui/local_models.js)):**
    *   Integrated MediaPipe Web LLM Inference API (`@mediapipe/tasks-genai`) loading in WebGPU caches (`Gemma 2B` / `Phi-2`).
    *   Implemented Cache API checking and unmetered storage for the Gemma model weights inside `gemma-model-cache` to avoid duplicate downloads.
    *   Added network-aware download streams tracking real fetch progress percentages via response readers, with automated local dialogue simulator fallback on hardware/network issues.
    *   Pre-caches a lightweight Plant Disease Classifier model TFLite file (`~15MB`) under `ui/models/` for offline leaf pathology checks.
    *   Added a local agronomic rule-based response generator formatting outputs offline in Hindi, Marathi, Telugu, Swahili, and English.
*   **Model Downloader Interface:** Placed a "Load Offline AI" button next to selectors in `index.html` to download and cache the Gemma model dynamically.

### 4. 💾 IndexedDB Caching & Hybrid Routing
*   **IndexedDB Store ([ui/agui/local_db.js](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/ui/agui/local_db.js)):**
    *   Stores farmer profiles, offline chat records, and pending telemetry queues.
*   **Hybrid Connectivity Router ([ui/agui/dashboard.js](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/ui/agui/dashboard.js)):**
    *   Listens to connection events. Updates the header banner (`Offline Edge AI` vs `Agents Online`).
    *   Triage text queries directly to client WebGPU Gemma loops if offline or uvicorn requests time out.
    *   Queues offline telemetry updates and automatically pushes them to the FastAPI backend when connection resumes.

### 5. 🛠️ Critical Bug Fixes
*   **Agent module load:** Fixed a missing `root_agent` export in [app/agent.py](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/app/agent.py) preventing pytest integration tests from loading.
*   **Feedback 500 error:** Appended a proper dict return value and wrapped the cloud logging call in a `try-except` block within `/feedback` inside [app/fast_api_app.py](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/app/fast_api_app.py) to resolve FastAPI validation errors.
*   **Port Binding conflicts:** Migrated both the integration test suite and the main application server [app/fast_api_app.py](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/app/fast_api_app.py) default binding ports from `8000` to `8009` (configurable via `PORT` env var) to completely bypass conflicts with local services like `omlx-server` active on port 8000.

### 6. 📚 Project Documentation Guides
*   **[TECHNICAL_ARCHITECTURE.md](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/docs/TECHNICAL_ARCHITECTURE.md):** Architectural manuals detailing agents, databases, simulator sandbox variables, and layout frameworks.
*   **[PWA_LLM_IMPLEMENTATION_PLAN.md](file:///Users/nalin.giri/workspaces/agentic-agri-advisor/docs/PWA_LLM_IMPLEMENTATION_PLAN.md):** Actionable implementation roadmap for client edge models, IndexedDB layers, and offline classifiers.
