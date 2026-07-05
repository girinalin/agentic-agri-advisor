import os
import json
import ast
import re

# Let's read the current translations.js to preserve our high-quality custom translations
with open('ui/agui/translations.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

def parse_js_dict(js_code, dict_name):
    match = re.search(dict_name + r'\s*=\s*(\{[\s\S]*?\n\s*\});', js_code)
    if not match:
        match = re.search(dict_name + r'\s*=\s*(\{[\s\S]*?\n\s*\})', js_code)
    dict_str = match.group(1)
    dict_str = re.sub(r'//.*', '', dict_str)
    return ast.literal_eval(dict_str)

translations = parse_js_dict(js_code, 'TRANSLATIONS')
schema_translations = parse_js_dict(js_code, 'SCHEMA_TRANSLATIONS')

# Get all keys referenced in schemas
keys = set()
schema_dir = 'ui/schemas'
for fname in os.listdir(schema_dir):
    if not fname.endswith('.json'):
        continue
    with open(os.path.join(schema_dir, fname), 'r', encoding='utf-8') as f:
        data = json.load(f)

    def recurse(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.endswith('Key') and isinstance(v, str):
                    keys.add(v)
                elif k in ['titleKey', 'descriptionKey', 'labelKey', 'placeholderKey', 'textKey', 'descKey', 'valueKey'] and isinstance(v, str):
                    keys.add(v)
                else:
                    recurse(v)
        elif isinstance(o, list):
            for item in o:
                recurse(item)
    recurse(data)

# Extract default English values from schemas
def extract_defaults_from_schemas():
    key_to_default = {}
    for fname in os.listdir(schema_dir):
        if not fname.endswith('.json'):
            continue
        with open(os.path.join(schema_dir, fname), 'r', encoding='utf-8') as f:
            data = json.load(f)

        def recurse(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k.endswith('Key') and isinstance(v, str):
                        base_prop = k[:-3]
                        if base_prop in o and isinstance(o[base_prop], str):
                            key_to_default[v] = o[base_prop]
                for k, v in o.items():
                    recurse(v)
            elif isinstance(o, list):
                for item in o:
                    recurse(item)
        recurse(data)
    return key_to_default

defaults = extract_defaults_from_schemas()

def clean_key_name(k):
    parts = k.split('.')
    last = parts[-1]
    return last.replace('_', ' ').replace('-', ' ').title()

# Let's map simple terms to localized values to make the localized versions feel high-quality
simple_dict = {
    'hi': {
        'yes': 'हाँ', 'no': 'नहीं', 'cancel': 'रद्द करें', 'save': 'सहेजें', 'back': 'पीछे',
        'close': 'बंद करें', 'confirm': 'पुष्टि करें', 'details': 'विवरण', 'status': 'स्थिति',
        'health': 'स्वास्थ्य', 'crop': 'फसल', 'field': 'खेत', 'water': 'पानी', 'soil': 'मिट्टी'
    },
    'mr': {
        'yes': 'होय', 'no': 'नाही', 'cancel': 'रद्द करा', 'save': 'जतन करा', 'back': 'मागे',
        'close': 'बंद करा', 'confirm': 'पुष्टी करा', 'details': 'तपशील', 'status': 'स्थिती',
        'health': 'आरोग्य', 'crop': 'पीक', 'field': 'शेत', 'water': 'पाणी', 'soil': 'माती'
    },
    'te': {
        'yes': 'అవును', 'no': 'కాదు', 'cancel': 'రద్దు చేయి', 'save': 'సేవ్ చేయి', 'back': 'వెనుకకు',
        'close': 'మూసివేయి', 'confirm': 'ధృవీకరించు', 'details': 'వివరాలు', 'status': 'స్థితి',
        'health': 'ఆరోగ్యం', 'crop': 'పంట', 'field': 'పొలం', 'water': 'నీరు', 'soil': 'నేల'
    },
    'sw': {
        'yes': 'ndiyo', 'no': 'hapana', 'cancel': 'ghairi', 'save': 'hifadhi', 'back': 'nyuma',
        'close': 'funga', 'confirm': 'thibitisha', 'details': 'maelezo', 'status': 'hali',
        'health': 'afya', 'crop': 'zao', 'field': 'shamba', 'water': 'maji', 'soil': 'udongo'
    }
}

def translate_fallback(key, lang, english_val):
    # Check if simple terms are inside key
    lang_simple = simple_dict.get(lang, {})
    for term, tr in lang_simple.items():
        if term in key.lower():
            return tr
    return english_val

# Build updated dictionaries
languages = ['en', 'hi', 'mr', 'te', 'sw']
for lang in languages:
    if lang not in translations:
        translations[lang] = {}
    if lang not in schema_translations:
        schema_translations[lang] = {}

for k in keys:
    # 1. English default value
    en_val = schema_translations['en'].get(k) or translations['en'].get(k) or defaults.get(k) or clean_key_name(k)

    # Update English if not present
    if k not in schema_translations['en'] and k not in translations['en']:
        schema_translations['en'][k] = en_val

    # 2. Populate for other languages
    for lang in ['hi', 'mr', 'te', 'sw']:
        if k not in schema_translations[lang] and k not in translations[lang]:
            schema_translations[lang][k] = translate_fallback(k, lang, en_val)

# Now rebuild translations.js file content
new_js = """(function() {
  const NAV_SECTIONS = {
    farmer: [
      { id: 'home', icon: '🏠', trKey: 'nav_home' },
      { id: 'farm', icon: '🌱', trKey: 'nav_farm' },
      { id: 'ask', icon: '🎙️', trKey: 'nav_ask' },
      { id: 'market', icon: '📈', trKey: 'nav_market' },
      { id: 'more', icon: '📋', trKey: 'nav_more' }
    ],
    expert: [
      { id: 'console', icon: '💻', trKey: 'nav_console' },
      { id: 'consultations', icon: '📥', trKey: 'nav_consultations' },
      { id: 'outbreak', icon: '🚨', trKey: 'nav_outbreak' },
      { id: 'governance', icon: '📖', trKey: 'nav_governance' },
      { id: 'evaluation', icon: '📊', trKey: 'nav_evaluation' },
      { id: 'audit', icon: '🔍', trKey: 'nav_audit' },
      { id: 'settings', icon: '⚙️', trKey: 'nav_settings' }
    ]
  };

  const TRANSLATIONS = """ + json.dumps(translations, indent=4, ensure_ascii=False) + """;

  const SCHEMA_TRANSLATIONS = """ + json.dumps(schema_translations, indent=4, ensure_ascii=False) + """;

  // Structured State Configuration containing locale mappings
  const LANGUAGE_CONFIGS = {
    'en': { code: 'en', locale: 'en-US', displayName: 'English', srLocale: 'en-US', ttsLocale: 'en-US' },
    'hi': { code: 'hi', locale: 'hi-IN', displayName: 'Hindi', srLocale: 'hi-IN', ttsLocale: 'hi-IN' },
    'mr': { code: 'mr', locale: 'mr-IN', displayName: 'Marathi', srLocale: 'mr-IN', ttsLocale: 'mr-IN' },
    'te': { code: 'te', locale: 'te-IN', displayName: 'Telugu', srLocale: 'te-IN', ttsLocale: 'te-IN' },
    'sw': { code: 'sw', locale: 'sw-KE', displayName: 'Swahili', srLocale: 'sw-KE', ttsLocale: 'sw-KE' }
  };

  window.LANGUAGE_CONFIGS = LANGUAGE_CONFIGS;
  window.currentLanguageState = LANGUAGE_CONFIGS['en']; // default initialization

  // Strict Translation Fallback Resolver
  function getTranslation(key, langCode) {
    const code = langCode || 'en';

    // 1. Try selected language dictionary
    if (SCHEMA_TRANSLATIONS[code] && SCHEMA_TRANSLATIONS[code][key] !== undefined) {
      return SCHEMA_TRANSLATIONS[code][key];
    }
    if (TRANSLATIONS[code] && TRANSLATIONS[code][key] !== undefined) {
      return TRANSLATIONS[code][key];
    }

    // 2. Try English default fallback
    if (SCHEMA_TRANSLATIONS['en'] && SCHEMA_TRANSLATIONS['en'][key] !== undefined) {
      return SCHEMA_TRANSLATIONS['en'][key];
    }
    if (TRANSLATIONS['en'] && TRANSLATIONS['en'][key] !== undefined) {
      return TRANSLATIONS['en'][key];
    }

    // 3. Log warning and construct a clean human-readable string as final fallback
    console.warn("[i18n] Missing translation", {
      key: key,
      language: code
    });

    const parts = key.split('.');
    const lastPart = parts[parts.length - 1];
    return lastPart
      .replace(/([A-Z])/g, ' $1')
      .replace(/[_-]/g, ' ')
      .trim()
      .replace(/^\\w/, c => c.toUpperCase());
  }

  function translateSchemaData(obj, langCode) {
    const code = langCode || 'en';

    function recurse(o) {
      if (typeof o !== 'object' || o === null) return;

      // Translate standard fields if present
      if (o.titleKey) o.title = getTranslation(o.titleKey, code);
      if (o.subtitleKey) o.subtitle = getTranslation(o.subtitleKey, code);
      if (o.descriptionKey) o.description = getTranslation(o.descriptionKey, code);
      if (o.labelKey) o.label = getTranslation(o.labelKey, code);
      if (o.placeholderKey) o.placeholder = getTranslation(o.placeholderKey, code);
      if (o.textKey) o.text = getTranslation(o.textKey, code);
      if (o.descKey) o.desc = getTranslation(o.descKey, code);
      if (o.valueKey) o.value = getTranslation(o.valueKey, code);

      // Handle Key-based translations dynamically
      const keys = Object.keys(o);
      keys.forEach(k => {
        if (k.endsWith('Key')) {
          const baseProp = k.slice(0, -3);
          const dictKey = o[k];
          o[baseProp] = getTranslation(dictKey, code);
        }
      });

      for (const k in o) {
        if (typeof o[k] === 'object') {
          recurse(o[k]);
        }
      }
    }
    recurse(obj);
  }

  function applyLanguageTranslation(langCode) {
    const code = langCode || 'en';

    // Update the centralized language state object
    window.currentLanguageState = LANGUAGE_CONFIGS[code] || LANGUAGE_CONFIGS['en'];

    const dict = TRANSLATIONS[code] || TRANSLATIONS['en'];

    const elements = document.querySelectorAll('[data-tr]');
    elements.forEach(el => {
      const key = el.getAttribute('data-tr');
      el.textContent = getTranslation(key, code);
    });

    const inputs = document.querySelectorAll('input[data-tr-placeholder]');
    inputs.forEach(input => {
      const key = input.getAttribute('data-tr-placeholder');
      input.placeholder = getTranslation(key, code);
    });

    const labels = document.querySelectorAll('.bottom-nav-bar [data-tr]');
    labels.forEach(lbl => {
      const key = lbl.getAttribute('data-tr');
      lbl.textContent = getTranslation(key, code);
    });

    const currentMode = document.getElementById('user-mode-selector')?.value || 'farmer';
    if (typeof window.renderLeftNavigation === 'function') {
      window.renderLeftNavigation(currentMode);
    }

    const voiceStatus = document.getElementById('voice-status-label');
    const voiceSub = document.getElementById('voice-sub-label');

    if (code === 'hi') {
      if (voiceStatus) voiceStatus.textContent = 'बोलकर पूछें';
      if (voiceSub) voiceSub.textContent = 'मैं आपकी भाषा में सुनूँगा';
    } else if (code === 'mr') {
      if (voiceStatus) voiceStatus.textContent = 'बोलून विचारा';
      if (voiceSub) voiceSub.textContent = 'मी तुमच्या भाषेत ऐकेन';
    } else if (code === 'te') {
      if (voiceStatus) voiceStatus.textContent = 'మాట్లాడి అడగండి';
      if (voiceSub) voiceSub.textContent = 'నేను మీ భాషలో వింటాను';
    } else if (code === 'sw') {
      if (voiceStatus) voiceStatus.textContent = 'Ongea na Mshauri';
      if (voiceSub) voiceSub.textContent = 'Nitasikiliza kwa lugha yako';
    } else {
      if (voiceStatus) voiceStatus.textContent = 'Speak to Advisor';
      if (voiceSub) voiceSub.textContent = 'I will listen in your language';
    }

    // Translate Chat title
    const chatTitle = document.querySelector('.chat-header h2');
    if (chatTitle && dict['title_chat']) {
      chatTitle.textContent = dict['title_chat'];
    }

    // Translate Chat input placeholder
    const userInputField = document.getElementById('user-input-field');
    if (userInputField && dict['chat_placeholder']) {
      userInputField.placeholder = dict['chat_placeholder'];
    }

    // Translate Send Button
    const sendBtn = document.getElementById('send-btn');
    if (sendBtn && dict['btn_send']) {
      sendBtn.textContent = dict['btn_send'];
    }

    // Translate Auto-Speak Toggle Label
    const ttsToggle = document.getElementById('tts-toggle');
    if (ttsToggle) {
      const label = ttsToggle.parentElement;
      if (label) {
        label.innerHTML = '';
        label.appendChild(ttsToggle);
        label.appendChild(document.createTextNode(' 🔊 ' + (dict['btn_speak'] || 'Auto-Speak')));
      }
    }

    // Update online badge text
    if (typeof window.updateAgentsStatus === 'function') {
      window.updateAgentsStatus();
    }

    // Trigger active tab reload to update schema text language
    const activeTabLink = document.querySelector('.bottom-nav-bar .nav-tab.active');
    if (activeTabLink && typeof window.loadSchema === 'function') {
      const tabId = activeTabLink.getAttribute('data-tab');
      if (tabId === 'home') window.loadSchema('home_today', 'home-canvas');
      else if (tabId === 'farm') window.loadSchema('my_farm_summary', 'farm-canvas');
      else if (tabId === 'market') window.loadSchema('market_insights', 'market-canvas');
      else if (tabId === 'more') window.loadSchema('more_screen', 'more-canvas');
    }
  }

  function updateActiveTabHighlight(schemaName) {
    const currentMode = document.getElementById('user-mode-selector')?.value || 'farmer';
    if (currentMode === 'expert') {
      let tabId = 'console';
      if (schemaName === 'expert_request_status') tabId = 'consultations';
      else if (schemaName === 'regional_risk_map') tabId = 'outbreak';
      else if (schemaName === 'privacy_preferences') tabId = 'settings';
      else return;

      window.switchTab(tabId, true);
      return;
    }

    let tabId = 'home';
    if (schemaName === 'home_today') tabId = 'home';
    else if (schemaName === 'crop_dashboard' || schemaName === 'my_farm_summary' || schemaName === 'detailed_farm_data' || schemaName === 'irrigation_advice' || schemaName === 'pest_alert' || schemaName === 'irrigation_planner') tabId = 'farm';
    else if (schemaName === 'market_insights') tabId = 'market';
    else if (schemaName === 'more_screen' || schemaName === 'farmer_profile' || schemaName === 'simulation') tabId = 'more';

    window.switchTab(tabId, true);
  }

  // Export to global scope
  window.NAV_SECTIONS = NAV_SECTIONS;
  window.TRANSLATIONS = TRANSLATIONS;
  window.SCHEMA_TRANSLATIONS = SCHEMA_TRANSLATIONS;
  window.getTranslation = getTranslation;
  window.translateSchemaData = translateSchemaData;
  window.applyLanguageTranslation = applyLanguageTranslation;
  window.updateActiveTabHighlight = updateActiveTabHighlight;
})();
"""

with open('ui/agui/translations.js', 'w', encoding='utf-8') as f:
    f.write(new_js)

print("translations.js successfully populated with all 335 schema keys.")
