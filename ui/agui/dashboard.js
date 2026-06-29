document.addEventListener('DOMContentLoaded', () => {
  const chatMessages = document.getElementById('chat-messages');
  const userInputField = document.getElementById('user-input-field');
  const sendBtn = document.getElementById('send-btn');
  const aguiCanvas = document.getElementById('agui-canvas');

  // Floating Action Buttons (FABs)
  const fabDiagnose = document.getElementById('fab-diagnose');
  const fabRefresh = document.getElementById('fab-refresh');
  const fabRun = document.getElementById('fab-run');

  // Local Simulation State
  let simState = {
    day: 0,
    stage: 'germination',
    soilMoisture: 40.0,
    health: 100.0,
    pestIndex: 5.0
  };

  // Keep track of the active session ID
  let sessionId = localStorage.getItem('aaa_session_id');

  async function getSessionId() {
    if (sessionId) return sessionId;
    try {
      const resp = await fetch('http://127.0.0.1:8080/apps/app/users/user/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      const data = await resp.json();
      sessionId = data.session_id || data.id;
      if (sessionId) {
        localStorage.setItem('aaa_session_id', sessionId);
      }
      return sessionId;
    } catch (e) {
      console.warn("Failed to create session on ADK server, falling back to local uuid.", e);
      sessionId = crypto.randomUUID();
      return sessionId;
    }
  }

  // Toast Notification Engine
  function showToast(title, message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast-alert ${type}`;
    
    let icon = '🔔';
    if (type === 'danger') icon = '🚨';
    if (type === 'warning') icon = '⚠️';
    if (type === 'success') icon = '✅';

    toast.innerHTML = `
      <div class="toast-icon">${icon}</div>
      <div class="toast-content">
        <strong class="toast-title">${title}</strong>
        <p class="toast-message">${message}</p>
      </div>
    `;

    container.appendChild(toast);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
      toast.style.animation = 'fadeOut 0.4s forwards';
      setTimeout(() => toast.remove(), 400);
    }, 4000);
  }

  // Appends a new message bubble to the chat timeline
  function appendMessage(sender, text, type = 'msg') {
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    msg.innerHTML = `<strong>${sender}:</strong> <span class="message-text">${text}</span>`;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return msg;
  }

  function markdownToHtml(text) {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
  }

  // Auto-closes brackets/braces for truncated JSON blocks
  function repairJSON(str) {
    let openBraces = 0;
    let openBrackets = 0;
    let inString = false;
    let escape = false;
    
    for (let i = 0; i < str.length; i++) {
      const char = str[i];
      if (escape) {
        escape = false;
        continue;
      }
      if (char === '\\') {
        escape = true;
        continue;
      }
      if (char === '"') {
        inString = !inString;
        continue;
      }
      if (!inString) {
        if (char === '{') openBraces++;
        if (char === '}') openBraces--;
        if (char === '[') openBrackets++;
        if (char === ']') openBrackets--;
      }
    }
    
    if (inString) str += '"';
    
    while (openBrackets > 0) {
      str += ']';
      openBrackets--;
    }
    while (openBraces > 0) {
      str += '}';
      openBraces--;
    }
    return str;
  }

  // Extracts JSON blocks from agent response text and renders them on the left panel
  function detectAndRenderA2UI(text) {
    if (!text) return false;
    
    // 1. Try matching markdown fenced code block first (most robust)
    const codeBlockRegex = /```json\s*([\s\S]*?)\s*```/;
    const match = text.match(codeBlockRegex);
    if (match) {
      try {
        const rawJson = repairJSON(match[1].trim());
        const data = JSON.parse(rawJson);
        if (data.type === 'card' && Array.isArray(data.components)) {
          if (data.title && data.title.toLowerCase().includes('simulator')) {
            bindSimulationState(data);
          }
          window.renderA2UIPayload(data, aguiCanvas);
          return true;
        }
      } catch (e) {
        // Fall back to outermost search if parsed block is invalid
      }
    }

    // 2. Fallback: Parse using outermost brace boundaries
    const firstBrace = text.indexOf('{');
    const lastBrace = text.lastIndexOf('}');
    if (firstBrace !== -1) {
      try {
        // Extract substring from first brace to the end and try repairing it!
        const candidate = text.substring(firstBrace);
        const repaired = repairJSON(candidate);
        const data = JSON.parse(repaired);
        if (data.type === 'card' && Array.isArray(data.components)) {
          if (data.title && data.title.toLowerCase().includes('simulator')) {
            bindSimulationState(data);
          }
          window.renderA2UIPayload(data, aguiCanvas);
          return true;
        }
      } catch (e) {
        // Ignore
      }
    }
    return false;
  }

  // Binds the active simulation state to the schema structure
  function bindSimulationState(schema) {
    schema.components.forEach(comp => {
      if (comp.type === 'grid') {
        comp.items.forEach(item => {
          const label = item.label.toLowerCase();
          if (label.includes('day')) {
            item.value = `Day ${simState.day}`;
          } else if (label.includes('stage')) {
            item.value = simState.stage;
          } else if (label.includes('moisture')) {
            item.value = `${simState.soilMoisture.toFixed(1)}%`;
          } else if (label.includes('health')) {
            item.value = `${simState.health.toFixed(1)}%`;
          } else if (label.includes('pest')) {
            item.value = `${simState.pestIndex.toFixed(1)}%`;
            item.status = simState.pestIndex > 25.0 ? 'warning' : 'optimal';
          }
        });
      } else if (comp.type === 'button' && comp.label.includes('Step Simulation')) {
        comp.label = `🎮 Step Simulation (Day ${simState.day + 1})`;
      }
    });
  }

  // Load static or stored schema
  async function loadSchema(schemaName) {
    try {
      const response = await fetch(`../schemas/${schemaName}.json`);
      if (!response.ok) {
        throw new Error(`Failed to load schema: ${response.statusText}`);
      }
      const data = await response.json();
      if (schemaName === 'simulation') {
        bindSimulationState(data);
      }
      window.renderA2UIPayload(data, aguiCanvas);
    } catch (err) {
      aguiCanvas.innerHTML = `<div style="color:var(--trend-down);padding:1rem;">Error rendering panel: ${err.message}</div>`;
    }
  }

  // Send message to live ADK Python server
  async function handleSend() {
    const text = userInputField.value.trim();
    if (!text) return;

    appendMessage('User', text, 'user-msg');
    userInputField.value = '';

    const thinkingBubble = appendMessage('Coordinator', 'Thinking...', 'thinking-msg');

    try {
      const activeSessionId = await getSessionId();
      const response = await fetch('http://127.0.0.1:8080/run_sse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          app_name: 'app',
          user_id: 'user',
          session_id: activeSessionId,
          new_message: {
            parts: [{ text: text }]
          },
          streaming: true
        })
      });

      if (!response.ok) {
        throw new Error(`Agent response error: ${response.statusText}`);
      }

      thinkingBubble.remove();
      
      const responseMsg = appendMessage('Coordinator', '', 'agent-msg');
      const textContainer = responseMsg.querySelector('.message-text');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      let fullResponseText = '';

      function getStreamingCleanText(text) {
        if (!text) return "";
        const fenceIndex = text.indexOf('```json');
        if (fenceIndex !== -1) {
          return text.substring(0, fenceIndex).trim();
        }
        const cardIndex = text.indexOf('"type": "card"');
        if (cardIndex !== -1) {
          const sub = text.substring(0, cardIndex);
          const braceIndex = sub.lastIndexOf('{');
          if (braceIndex !== -1) {
            return text.substring(0, braceIndex).trim();
          }
        }
        return text;
      }

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop();

        for (const line of lines) {
          if (line.trim().startsWith('data: ')) {
            try {
              const eventData = JSON.parse(line.trim().substring(6));
              if (eventData.content && eventData.content.parts) {
                for (const part of eventData.content.parts) {
                  if (part.text) {
                    fullResponseText += part.text;
                    textContainer.innerHTML = markdownToHtml(getStreamingCleanText(fullResponseText));
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                  }
                }
              }
            } catch (err) {
              // Ignore partial chunk parse errors
            }
          }
        }
      }

      textContainer.innerHTML = markdownToHtml(getStreamingCleanText(fullResponseText));

      // Check if response contains raw JSON card
      const renderedInline = detectAndRenderA2UI(fullResponseText);
      
      // If no card was returned directly, run intent routing to load relevant left panel!
      if (!renderedInline && window.panelRouter) {
        const targetSchema = window.panelRouter.routeIntent(fullResponseText);
        if (targetSchema) {
          loadSchema(targetSchema);
          showToast("Workspace Synced", `Panel switched to ${targetSchema.replace('_', ' ')} based on advisor reply.`, "success");
        }
      }

      // Handle toast triggers inside response text
      if (fullResponseText.toLowerCase().includes('outbreak') || fullResponseText.toLowerCase().includes('disease')) {
        showToast("Pest Warning", "Regional active disease risk detected on leaf samples.", "danger");
      } else if (fullResponseText.toLowerCase().includes('water') && fullResponseText.toLowerCase().includes('critical')) {
        showToast("Irrigation Alert", "Soil moisture dropping below critical limit. Watering advised.", "warning");
      }

    } catch (err) {
      thinkingBubble.remove();
      appendMessage('System', `Connection failed: ${err.message}. Ensure agents-cli playground is running on port 8080.`, 'error-msg');
    }
  }

  // Load default crop dashboard schema on startup
  loadSchema('crop_dashboard');

  // Hook up FAB actions
  if (fabDiagnose) {
    fabDiagnose.addEventListener('click', () => {
      userInputField.value = "Show active pest alerts. Use get_ui_schema tool to load 'pest_alert' card.";
      handleSend();
    });
  }
  if (fabRefresh) {
    fabRefresh.addEventListener('click', () => {
      userInputField.value = "Refresh live crop data. Use get_ui_schema tool to load 'crop_dashboard' card.";
      handleSend();
    });
  }
  if (fabRun) {
    fabRun.addEventListener('click', () => {
      userInputField.value = "Open simulation sandbox. Use get_ui_schema tool to load 'simulation' card.";
      handleSend();
    });
  }

  // Voice Speech-to-Text Recognition integration
  const micBtn = document.getElementById('mic-btn');
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  
  if (micBtn && SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    
    let isRecording = false;
    
    recognition.onstart = () => {
      isRecording = true;
      micBtn.classList.add('recording');
      micBtn.innerHTML = '🔴';
      userInputField.placeholder = "Listening...";
    };
    
    recognition.onend = () => {
      isRecording = false;
      micBtn.classList.remove('recording');
      micBtn.innerHTML = '🎙️';
      userInputField.placeholder = "Ask the advisor a question or trigger a tool...";
    };
    
    recognition.onerror = (e) => {
      console.warn("Speech recognition error:", e.error);
      isRecording = false;
      micBtn.classList.remove('recording');
      micBtn.innerHTML = '🎙️';
      userInputField.placeholder = "Speech error. Try again.";
    };
    
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      userInputField.value = transcript;
      handleSend();
    };
    
    micBtn.addEventListener('click', () => {
      if (isRecording) {
        recognition.stop();
      } else {
        recognition.start();
      }
    });
  } else if (micBtn) {
    micBtn.addEventListener('click', () => {
      alert("Voice Speech Recognition is not fully supported in this browser. Please try Google Chrome.");
    });
  }

  // Listen to A2UI actions (like stepping the simulation sandbox or submitting templates)
  document.addEventListener('a2ui-action', (e) => {
    const action = e.detail.action;
    if (action === 'run_sim_step') {
      const cropInput = document.querySelector('select[name="crop_type"]') || document.querySelector('input[name="crop_type"]');
      const waterInput = document.querySelector('input[name="water_liters"]');
      const fertilizerInput = document.querySelector('input[name="fertilizer_kg"]');
      
      const cropType = cropInput ? cropInput.value : 'corn';
      const waterLiters = waterInput ? parseFloat(waterInput.value) || 10.0 : 10.0;
      const fertilizerKg = fertilizerInput ? parseFloat(fertilizerInput.value) || 5.0 : 5.0;
      
      // Advance step
      simState.day += 1;
      
      // Calculate moisture updates (evapotranspiration vs irrigation)
      const rain = Math.random() > 0.85 ? 8.0 : 0.0;
      const depletion = 2.5;
      const gain = (rain * 1.5) + (waterLiters * 0.8);
      simState.soilMoisture = Math.max(0.0, Math.min(100.0, simState.soilMoisture - depletion + gain));
      
      // Calculate pest updates
      const treatment = fertilizerKg > 8.0;
      if (treatment) {
        simState.pestIndex = Math.max(1.0, simState.pestIndex - 20.0);
      } else {
        simState.pestIndex = Math.min(100.0, simState.pestIndex + 1.2);
      }
      
      // Calculate health updates
      const temp = 21.0 + Math.random() * 4.0;
      const tempFactor = Math.max(0.1, 1.0 - Math.abs(temp - 23.0) / 15.0);
      const waterFactor = Math.max(0.1, 1.0 - Math.abs(simState.soilMoisture - 50.0) / 40.0);
      const pestFactor = Math.max(0.1, 1.0 - (simState.pestIndex / 100.0));
      const growthRate = 2.5 * tempFactor * waterFactor * pestFactor;
      
      if (simState.soilMoisture < 15.0 || simState.soilMoisture > 85.0) {
        simState.health = Math.max(0.0, simState.health - 2.5);
      } else {
        simState.health = Math.min(100.0, simState.health + 0.5);
      }
      
      const cumulativeGrowth = simState.day * growthRate;
      if (cumulativeGrowth >= 100.0 || simState.day >= 30) {
        simState.stage = 'harvested';
      } else if (cumulativeGrowth >= 75.0 || simState.day >= 20) {
        simState.stage = 'maturity';
      } else if (cumulativeGrowth >= 40.0 || simState.day >= 12) {
        simState.stage = 'flowering';
      } else if (cumulativeGrowth >= 15.0 || simState.day >= 5) {
        simState.stage = 'vegetative';
      }
      
      // Update DOM values of the active left panel simulator card
      const metrics = aguiCanvas.querySelectorAll('.a2ui-metric');
      metrics.forEach(m => {
        const labelText = m.textContent.toLowerCase();
        const valEl = m.querySelector('.metric-val');
        if (!valEl) return;
        
        if (labelText.includes('day')) {
          valEl.textContent = `Day ${simState.day}`;
        } else if (labelText.includes('stage')) {
          valEl.textContent = simState.stage;
        } else if (labelText.includes('moisture')) {
          valEl.textContent = `${simState.soilMoisture.toFixed(1)}%`;
          m.className = `a2ui-metric ${simState.soilMoisture > 30 && simState.soilMoisture < 70 ? 'optimal' : 'warning'}`;
        } else if (labelText.includes('health')) {
          valEl.textContent = `${simState.health.toFixed(1)}%`;
          m.className = `a2ui-metric ${simState.health > 80 ? 'optimal' : 'warning'}`;
        } else if (labelText.includes('pest')) {
          valEl.textContent = `${simState.pestIndex.toFixed(1)}%`;
          m.className = `a2ui-metric ${simState.pestIndex > 25.0 ? 'warning' : 'optimal'}`;
        }
      });
      
      const stepBtn = aguiCanvas.querySelector('.a2ui-btn');
      if (stepBtn && stepBtn.textContent.includes('Step Simulation')) {
        stepBtn.textContent = `🎮 Step Simulation (Day ${simState.day + 1})`;
      }
      
      showToast("Simulation Stepped", `Advanced to Day ${simState.day}. Health is ${simState.health.toFixed(1)}%`, "success");
      
      // Notify agent of the new state in the conversation context
      const statusPrompt = `Simulation Advanced: Day ${simState.day}, Crop: ${cropType}, Stage: ${simState.stage}, Soil Moisture: ${simState.soilMoisture.toFixed(1)}%, Crop Health: ${simState.health.toFixed(1)}%, Pest Level: ${simState.pestIndex.toFixed(1)}%. Advise on irrigation or nutrient needs.`;
      userInputField.value = statusPrompt;
      handleSend();
    } else {
      // General Form Submission to Agent
      const form = aguiCanvas.querySelector('form') || aguiCanvas.querySelector('.a2ui-form');
      const params = {};
      if (form) {
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
          if (input.name) {
            params[input.name] = input.value;
          }
        });
      }
      
      let prompt = `Action triggered: '${action}'`;
      if (Object.keys(params).length > 0) {
        prompt += ` with fields: ` + Object.entries(params).map(([k, v]) => `${k}='${v}'`).join(', ');
      }
      
      userInputField.value = prompt;
      handleSend();
    }
  });

  // Event handlers
  sendBtn.addEventListener('click', handleSend);
  userInputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
  });
});
