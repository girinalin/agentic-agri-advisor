import os
import re

with open('ui/agui/dashboard.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# 1. Replace default language fallback 'English' with 'en'
js_content = js_content.replace(
    "const savedLang = localStorage.getItem('aaa_preferred_language') || 'English';",
    "const savedLang = localStorage.getItem('aaa_preferred_language') || 'en';"
)

# 2. Add renderAssistantInfoPane call when language changes
old_lang_change = """    languageSelector.addEventListener('change', () => {
      const selectedLang = languageSelector.value;
      localStorage.setItem('aaa_preferred_language', selectedLang);
      applyLanguageTranslation(selectedLang);"""

new_lang_change = """    languageSelector.addEventListener('change', () => {
      const selectedLang = languageSelector.value;
      localStorage.setItem('aaa_preferred_language', selectedLang);
      applyLanguageTranslation(selectedLang);
      const currentMode = document.getElementById('user-mode-selector')?.value || 'farmer';
      renderAssistantInfoPane(currentMode);"""

js_content = js_content.replace(old_lang_change, new_lang_change)

# 3. Replace handleSend completely. We locate from the start of async function handleSend() until before async function handleOfflineSend
# We will use regex to do a clean swap
handle_send_pattern = r"async function handleSend\(\) \{[\s\S]*?\}\s*async function handleOfflineSend"
new_handle_send = """async function handleSend() {
    const text = userInputField.value.trim();
    if (!text) return;

    appendMessage('User', text, 'user-msg');
    userInputField.value = '';

    const langCode = window.currentLanguageState?.code || 'en';
    const preferredLang = window.currentLanguageState?.displayName || 'English';

    // Smart Triage Router: Route simple/local questions to local Gemma edge skills, complex to cloud agents
    const lowercaseText = text.toLowerCase();
    const complexKeywords = [
      'weather', 'forecast', 'price', 'trend', 'predict', 'mandi', 'market', 'sensor', 'planning', 'cost',
      'मौसम', 'दाम', 'भाव', 'मूल्य', 'मंडी', 'पूर्वानुमान',
      'हवामान', 'किंमत', 'बाजार', 'अंदाज',
      'వాతావరణం', 'ధర', 'మార్కెట్', 'అంచనా',
      'hewa', 'mvua', 'bei', 'soko', 'utabiri'
    ];
    const isComplex = complexKeywords.some(kw => lowercaseText.includes(kw));

    if (!navigator.onLine || !isComplex) {
      console.log(`[Triage] Routing "${text}" to client-side multi-agent edge skills.`);
      const thinkingBubble = appendMessage('Coordinator', 'Thinking...', 'thinking-msg');
      handleOfflineSend(text, langCode, thinkingBubble);
      return;
    }

    const thinkingBubble = appendMessage('Coordinator', 'Thinking...', 'thinking-msg');

    // Context Enrichment: Grab the saved profile and prepend it to the text payload!
    const savedProfile = localStorage.getItem('aaa_farmer_profile');
    let textToSend = text;
    if (savedProfile) {
      try {
        const profile = JSON.parse(savedProfile);
        textToSend = `[Context: Farmer Name: ${profile.farmer_name || 'unnamed'}, Language: ${langCode}, Location: ${profile.region}, Acres: ${profile.acres}, Soil: ${profile.soil_type}, Crop: ${profile.primary_crop}, Drip Irrigation: ${profile.has_drip}]\n\n${text}`;
      } catch (e) {
        textToSend = `[Context: Language: ${langCode}]\n\n${text}`;
      }
    } else {
      textToSend = `[Context: Language: ${langCode}]\n\n${text}`;
    }

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
            parts: [{ text: textToSend }]
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
        const lines = buffer.split('\\n\\n');
        buffer = lines.pop();

        for (const line of lines) {
          if (line.trim().startsWith('data: ')) {
            try {
              const eventData = JSON.parse(line.trim().substring(6));
              if (eventData.content && eventData.content.parts) {
                if (eventData.partial === false) {
                  let consolidatedText = "";
                  for (const part of eventData.content.parts) {
                    if (part.text) {
                      consolidatedText += part.text;
                    }
                  }
                  if (consolidatedText) {
                    fullResponseText = consolidatedText;
                  }
                } else {
                  for (const part of eventData.content.parts) {
                    if (part.text) {
                      fullResponseText += part.text;
                    }
                  }
                }
                const cleaned = getStreamingCleanText(fullResponseText);
                if (cleaned.trim().startsWith('{') || cleaned.includes('"recommendation"')) {
                  textContainer.innerHTML = getPreparingAdvisoryMsg(langCode);
                } else {
                  textContainer.innerHTML = markdownToHtml(cleaned);
                }
                chatMessages.scrollTop = chatMessages.scrollHeight;
              }
            } catch (err) {
              // Ignore
            }
          }
        }
      }

      const cleanResponse = getStreamingCleanText(fullResponseText).trim();
      let isStructured = false;
      try {
        const extracted = extractJsonContent(cleanResponse);
        const parsed = JSON.parse(extracted);
        if (parsed && typeof parsed === 'object' && parsed.recommendation !== undefined) {
          isStructured = true;
          renderStructuredResponse(parsed, textContainer, responseMsg);
          const ttsToggle = document.getElementById('tts-toggle');
          if (ttsToggle && ttsToggle.checked) {
            speakText(parsed.recommendation + (parsed.question ? " " + parsed.question : ""));
          }
        }
      } catch (err) {
        // Fall back to standard rendering
      }

      if (!isStructured) {
        textContainer.innerHTML = markdownToHtml(cleanResponse);
        const ttsToggle = document.getElementById('tts-toggle');
        if (ttsToggle && ttsToggle.checked) {
          speakText(cleanResponse);
        }
      }

      const renderedInline = detectAndRenderA2UI(fullResponseText);
      
      if (!renderedInline && window.panelRouter) {
        const targetSchema = window.panelRouter.routeIntent(fullResponseText);
        if (targetSchema) {
          loadSchema(targetSchema);
          showToast("Workspace Synced", `Panel switched to ${targetSchema.replace('_', ' ')} based on advisor reply.`, "success");
        }
      }

      if (fullResponseText.toLowerCase().includes('outbreak') || fullResponseText.toLowerCase().includes('disease')) {
        showToast("Pest Warning", "Regional active disease risk detected on leaf samples.", "danger");
      } else if (fullResponseText.toLowerCase().includes('water') && fullResponseText.toLowerCase().includes('critical')) {
        showToast("Irrigation Alert", "Soil moisture dropping below critical limit. Watering advised.", "warning");
      }

    } catch (err) {
      console.warn("ADK server fetch failed. Falling back to offline AI mode.", err);
      handleOfflineSend(text, langCode, thinkingBubble);
    }
  }

  async function handleOfflineSend"""

js_content = re.sub(handle_send_pattern, new_handle_send, js_content)

# 4. Replace renderLeftNavigation completely
left_nav_pattern = r"function renderLeftNavigation\(mode = 'farmer'\) \{[\s\S]*?\}\s*// Collapsible toggle buttons"
new_left_nav = """function renderLeftNavigation(mode = 'farmer') {
    const list = document.getElementById('left-nav-links-list');
    if (!list) return;
    list.innerHTML = '';

    const lang = window.currentLanguageState?.code || 'en';
    const dict = TRANSLATIONS[lang] || TRANSLATIONS['en'];
    const items = NAV_SECTIONS[mode] || NAV_SECTIONS['farmer'];

    items.forEach(item => {
      const label = dict[item.trKey] || item.trKey;
      const link = document.createElement('a');
      link.href = '#';
      link.className = 'left-nav-item';
      link.setAttribute('data-tab', item.id);
      link.setAttribute('title', label); // tooltip for collapsed mode
      link.setAttribute('aria-label', label);
      
      const currentActive = localStorage.getItem('nav_route_user') || (mode === 'expert' ? 'console' : 'home');
      if (item.id === currentActive) {
        link.classList.add('active');
      }

      link.innerHTML = `
        <span class="nav-icon">${item.icon}</span>
        <span class="nav-label">${label}</span>
      `;

      link.addEventListener('click', (e) => {
        e.preventDefault();
        window.switchTab(item.id);
      });

      list.appendChild(link);
    });

    // Translate profile labels in footer
    const profileName = document.getElementById('left-nav-profile-name');
    if (profileName) {
      profileName.textContent = mode === 'expert' ? 'Dr. Agronomist' : 'माधव जी';
    }
    
    // Render the new assistant info pane dynamically
    renderAssistantInfoPane(mode);
  }

  // Collapsible toggle buttons"""

js_content = re.sub(left_nav_pattern, new_left_nav, js_content)

# 5. Insert new helper functions before export block
export_block = "// Export functions to global window for modular submodules"

helpers = """  // Extracts JSON blocks from agent response text
  function extractJsonContent(text) {
    const trimmed = text.trim();
    const jsonMatch = trimmed.match(/^```json\\s*([\\s\\S]*?)\\s*```$/) || trimmed.match(/^```\\s*([\\s\\S]*?)\\s*```$/);
    return jsonMatch ? jsonMatch[1].trim() : trimmed;
  }

  // Localized preparing message
  function getPreparingAdvisoryMsg(langCode) {
    if (langCode === 'hi') return '⏳ <em>कृषि शास्त्री सलाह तैयार कर रहे हैं...</em>';
    if (langCode === 'mr') return '⏳ <em>कृषि शास्त्री सल्ला तयार करत आहेत...</em>';
    if (langCode === 'te') return '⏳ <em>కృషి శాస్త్రి సలహాను సిద్ధం చేస్తున్నారు...</em>';
    if (langCode === 'sw') return '⏳ <em>Krishi Sastri anaandaa ushauri...</em>';
    return '⏳ <em>Krishi Sastri is preparing advisory...</em>';
  }

  // Render structured JSON response card inside chat bubble
  function renderStructuredResponse(data, container, messageEl) {
    container.innerHTML = '';
    
    if (data.title) {
      const titleDiv = document.createElement('div');
      titleDiv.style.fontWeight = 'bold';
      titleDiv.style.fontSize = '1.1rem';
      titleDiv.style.marginBottom = '0.5rem';
      titleDiv.textContent = data.title;
      container.appendChild(titleDiv);
    }
    
    if (data.summary) {
      const summaryDiv = document.createElement('div');
      summaryDiv.style.marginBottom = '0.5rem';
      summaryDiv.textContent = data.summary;
      container.appendChild(summaryDiv);
    }
    
    if (data.recommendation) {
      const recDiv = document.createElement('div');
      recDiv.style.marginBottom = '0.5rem';
      recDiv.style.fontWeight = '600';
      recDiv.style.color = 'var(--accent)';
      recDiv.textContent = data.recommendation;
      container.appendChild(recDiv);
    }
    
    if (data.reasons && Array.isArray(data.reasons) && data.reasons.length > 0) {
      const ul = document.createElement('ul');
      ul.style.margin = '5px 0 10px 20px';
      ul.style.padding = '0';
      ul.style.listStyleType = 'disc';
      data.reasons.slice(0, 4).forEach(r => {
        const li = document.createElement('li');
        li.style.marginBottom = '2px';
        li.textContent = r;
        ul.appendChild(li);
      });
      container.appendChild(ul);
    }
    
    if (data.question) {
      const qDiv = document.createElement('div');
      qDiv.style.fontStyle = 'italic';
      qDiv.style.marginBottom = '0.75rem';
      qDiv.textContent = data.question;
      container.appendChild(qDiv);
    }
    
    if (data.actions && Array.isArray(data.actions) && data.actions.length > 0) {
      const actionsDiv = document.createElement('div');
      actionsDiv.style.display = 'flex';
      actionsDiv.style.flexWrap = 'wrap';
      actionsDiv.style.gap = '8px';
      actionsDiv.style.marginTop = '10px';
      
      data.actions.forEach(act => {
        const btn = document.createElement('button');
        btn.className = 'a2ui-btn';
        btn.style.padding = '6px 12px';
        btn.style.fontSize = '0.9rem';
        btn.style.borderRadius = '16px';
        btn.style.backgroundColor = 'var(--accent)';
        btn.style.color = '#fff';
        btn.style.border = 'none';
        btn.style.cursor = 'pointer';
        btn.style.fontWeight = 'bold';
        btn.textContent = act.label;
        
        btn.addEventListener('click', () => {
          const userInputField = document.getElementById('user-input-field');
          if (userInputField) {
            userInputField.value = act.prompt || act.label;
            handleSend();
          }
        });
        actionsDiv.appendChild(btn);
      });
      container.appendChild(actionsDiv);
    }
  }

  // Render assistant info pane containing Crop, Field, Advisory, Freshness
  function renderAssistantInfoPane(mode = 'farmer') {
    const pane = document.getElementById('assistant-info-pane');
    if (!pane) return;

    const preferredLang = window.currentLanguageState?.code || 'en';
    const activeField = activeFields.find(f => f.field_id === activeFieldId);
    
    if (mode === 'expert') {
      pane.innerHTML = `
        <div style="font-weight: bold; margin-bottom: 5px; color: var(--accent);">🔬 Specialist Agents Connectivity</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px; font-size: 0.8rem; color: var(--text-sub);">
          <div>🤖 Coordinator: <span style="color: var(--trend-up);">Active</span></div>
          <div>🌾 Crop Analyst: <span style="color: var(--trend-up);">Active</span></div>
          <div>💧 Irrigation Planner: <span style="color: var(--trend-up);">Active</span></div>
          <div>🐛 Pest Detector: <span style="color: var(--trend-up);">Active</span></div>
        </div>
      `;
    } else {
      const crop = activeField && activeField.planting ? activeField.planting.crop_type : 'Wheat';
      const fieldName = activeField ? activeField.name : 'Nagpur Field';
      
      let cropTr = window.getTranslation('profile.crop.wheat', preferredLang) || 'Wheat';
      if (crop.toLowerCase() === 'corn') {
        cropTr = window.getTranslation('profile.crop.corn', preferredLang) || 'Corn';
      } else if (crop.toLowerCase() === 'soybeans') {
        cropTr = window.getTranslation('profile.crop.soybeans', preferredLang) || 'Soybeans';
      }
      
      const advisory = window.getTranslation('farm.recommendation.desc', preferredLang) || 'Irrigate tomorrow morning.';
      const freshness = window.getTranslation('irrigation.weatherStatus.cached', preferredLang) || 'Cached 3h ago';
      
      pane.innerHTML = `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; color: var(--text-main);">
          <div><strong>🌾 ${window.getTranslation('profile.crop.label', preferredLang) || 'Crop'}:</strong> ${cropTr}</div>
          <div><strong>📍 ${window.getTranslation('profile.region.label', preferredLang) || 'Field'}:</strong> ${fieldName}</div>
          <div style="grid-column: span 2;"><strong>💡 ${window.getTranslation('farm.recommendation.title', preferredLang) || 'Advisory'}:</strong> ${advisory}</div>
          <div style="grid-column: span 2; font-size: 0.8rem; color: var(--text-sub);">🕒 ${freshness}</div>
        </div>
      `;
    }
  }

  // Update renderAssistantInfoPane when field changes
  const oldFieldSelector = document.getElementById('field-selector');
  if (oldFieldSelector) {
    oldFieldSelector.addEventListener('change', () => {
      setTimeout(() => {
        const currentMode = document.getElementById('user-mode-selector')?.value || 'farmer';
        renderAssistantInfoPane(currentMode);
      }, 200);
    });
  }

  // Trigger initial render of assistant pane
  setTimeout(() => {
    const currentMode = document.getElementById('user-mode-selector')?.value || 'farmer';
    renderAssistantInfoPane(currentMode);
  }, 500);

  """

js_content = js_content.replace(export_block, helpers + export_block)

with open('ui/agui/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
print("dashboard.js patched successfully.")
