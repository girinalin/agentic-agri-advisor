import os

# Define the language mapping
lang_map = {
    'English': 'en',
    'Hindi': 'hi',
    'Marathi': 'mr',
    'Telugu': 'te',
    'Swahili': 'sw'
}

# Read current translations.js
with open('ui/agui/translations.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's write a clean script that creates translations.js from scratch using consolidated and corrected data.
# This ensures perfect syntax, correct 2-letter mapping, and complete home screen keys coverage.
new_content = """(function() {
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

  const TRANSLATIONS = {
    'en': {
      'nav_console': '💻 Console',
      'nav_consultations': '📥 Consultations',
      'nav_outbreak': '🚨 Regional Intel',
      'nav_governance': '📖 Governance',
      'nav_evaluation': '📊 Evaluation',
      'nav_audit': '🔍 Audit Logs',
      'nav_settings': '⚙️ Settings',
      'nav_crop_dashboard': '🌾 Health',
      'nav_irrigation_planner': '💧 Irrigation',
      'nav_pest_alert': '🐛 Pests',
      'nav_market_insights': '📈 Markets',
      'nav_simulation': '🎮 Simulator',
      'nav_farmer_profile': '🧬 Profile',
      'status_online': 'Connected',
      'status_connected': 'Connected',
      'status_offline': 'Offline AI Ready',
      'chat_placeholder': 'Ask Krishi Sastri a question...',
      'btn_send': 'Send',
      'btn_speak': 'Auto-Speak',
      'title_chat': 'Krishi Sastri Chat Portal',
      'nav_home': 'Home',
      'nav_farm': 'My Farm',
      'nav_ask': 'Ask',
      'nav_market': 'Market',
      'nav_more': 'More'
    },
    'hi': {
      'nav_console': '💻 कंसोल',
      'nav_consultations': '📥 परामर्श',
      'nav_outbreak': '🚨 क्षेत्रीय खुफिया',
      'nav_governance': '📖 ज्ञान शासन',
      'nav_evaluation': '📊 मूल्यांकन',
      'nav_audit': '🔍 ऑडिट लॉग',
      'nav_settings': '⚙️ सेटिंग्स',
      'nav_crop_dashboard': '🌾 स्वास्थ्य',
      'nav_irrigation_planner': '💧 सिंचाई',
      'nav_pest_alert': '🐛 कीट',
      'nav_market_insights': '📈 मंडी भाव',
      'nav_simulation': '🎮 सिमुलेटर',
      'nav_farmer_profile': '🧬 प्रोफाइल',
      'status_online': 'संबद्ध',
      'status_connected': 'संबद्ध',
      'status_offline': 'ऑफ़लाइन एआई तैयार',
      'chat_placeholder': 'कृषि शास्त्री से पूछें...',
      'btn_send': 'भेजें',
      'btn_speak': 'ऑटो-बोलें',
      'title_chat': 'कृषि शास्त्री चैट पोर्टल',
      'nav_home': 'होम',
      'nav_farm': 'मेरा खेत',
      'nav_ask': 'पूछें',
      'nav_market': 'मंडी',
      'nav_more': 'अन्य'
    },
    'mr': {
      'nav_console': '💻 कन्सोल',
      'nav_consultations': '📥 सल्लामसलत',
      'nav_outbreak': '🚨 प्रादेशिक माहिती',
      'nav_governance': '📖 ज्ञान नियंत्रण',
      'nav_evaluation': '📊 मूल्यांकन',
      'nav_audit': '🔍 ऑडिट लॉग',
      'nav_settings': '⚙️ सेटिंग्ज',
      'nav_crop_dashboard': '🌾 पिकाची तब्येत',
      'nav_irrigation_planner': '💧 पाणी नियोजन',
      'nav_pest_alert': '🐛 कीड नियंत्रण',
      'nav_market_insights': '📈 बाजार भाव',
      'nav_simulation': '🎮 सिम्युलेटर',
      'nav_farmer_profile': '🧬 प्रोफाइल',
      'status_online': 'कनेक्टेड',
      'status_connected': 'कनेक्टेड',
      'status_offline': 'ऑफलाईन एआय तयार',
      'chat_placeholder': 'कृषि शास्त्रींना विचारा...',
      'btn_send': 'पाठवा',
      'btn_speak': 'ऑटो-बोला',
      'title_chat': 'कृषि शास्त्री चॅट पोर्टल',
      'nav_home': 'होम',
      'nav_farm': 'माझा शेत',
      'nav_ask': 'विचारा',
      'nav_market': 'बाजार',
      'nav_more': 'इतर'
    },
    'sw': {
      'nav_console': '💻 Dashibodi',
      'nav_consultations': '📥 Mashauriano',
      'nav_outbreak': '🚨 Ujasusi wa Kikanda',
      'nav_governance': '📖 Utawala wa Maarifa',
      'nav_evaluation': '📊 Tathmini',
      'nav_audit': '🔍 Ukaguzi',
      'nav_settings': '⚙️ Mipangilio',
      'nav_crop_dashboard': '🌾 Afya ya Mazao',
      'nav_irrigation_planner': '💧 Umwagiliaji',
      'nav_pest_alert': '🐛 Wadudu',
      'nav_market_insights': '📈 Soko',
      'nav_simulation': '🎮 Kifanisi',
      'nav_farmer_profile': '🧬 Wasifu',
      'status_online': 'Imeunganishwa',
      'status_connected': 'Imeunganishwa',
      'status_offline': 'AI Nje ya Mtandao Iko Tayari',
      'chat_placeholder': 'Uliza Krishi Sastri...',
      'btn_send': 'Tuma',
      'btn_speak': 'Soma Kiotomatiki',
      'title_chat': 'Krishi Sastri Portal ya Mazungumzo',
      'nav_home': 'Nyumbani',
      'nav_farm': 'Shamba Langu',
      'nav_ask': 'Uliza',
      'nav_market': 'Soko',
      'nav_more': 'Zaidi'
    },
    'te': {
      'nav_console': '💻 కన్సోల్',
      'nav_consultations': '📥 సంప్రదింపులు',
      'nav_outbreak': '🚨 ప్రాంతీయ నిఘా',
      'nav_governance': '📖 విజ్ఞాన పరిపాలన',
      'nav_evaluation': '📊 మూల్యాంకనం',
      'nav_audit': '🔍 ఆడిట్ లాగ్స్',
      'nav_settings': '⚙️ సెట్టింగులు',
      'nav_crop_dashboard': '🌾 ఆరోగ్యం',
      'nav_irrigation_planner': '💧 నీటి నిర్వహణ',
      'nav_pest_alert': '🐛 పురుగుల నివారణ',
      'nav_market_insights': '📈 మార్కెట్ ధరలు',
      'nav_simulation': '🎮 సిమ్యులేటర్',
      'nav_farmer_profile': '🧬 ప్రొఫైల్',
      'status_online': 'కనెక్ట్ చేయబడింది',
      'status_connected': 'కనెక్ట్ చేయబడింది',
      'status_offline': 'ఆఫ్‌లైన్ AI సిద్ధంగా ఉంది',
      'chat_placeholder': 'వ్యవసాయ సలహాదారుడిని అడగండి...',
      'btn_send': 'పంపించు',
      'btn_speak': 'ఆటో-స్పీక్',
      'title_chat': 'సలహాదారు చాట్ పోర్టల్',
      'nav_home': 'హోమ్',
      'nav_farm': 'నా పొలం',
      'nav_ask': 'అడగండి',
      'nav_market': 'మార్కెట్',
      'nav_more': 'మరింత'
    }
  };

  const SCHEMA_TRANSLATIONS = {
    'en': {
      'console.title': 'Agronomist Operations Console',
      'console.subtitle': 'Triage consultation queues and dispatch expert advice.',
      'console.case1.label': 'Case ID: esc_1 (Maize Leaf Blight)',
      'console.case1.desc': 'Yellowing leaf margins reported in Nagpur region.',
      'console.case2.label': 'Case ID: esc_2 (Tomato Rust)',
      'console.case2.desc': 'Rust pustules spotted on lower tomato foliage.',
      'console.action.assign': 'Assign Me',
      'console.action.resolve': 'Resolve Case',
      'console.action.close': 'Close Ticket',
      'outbreak.map.title': 'Regional Outbreak Risk Map',
      'outbreak.map.subtitle': 'Anonymized aggregation of verified pest symptoms.',
      'outbreak.map.nagpur.label': 'Nagpur Region Cluster',
      'outbreak.map.nagpur.desc': '6 confirmed cases of wheat leaf rust detected.',
      'outbreak.action.details': 'View Correlation Details',
      'outbreak.review.title': 'Outbreak Intelligence Alerts',
      'outbreak.review.subtitle': 'Review outbreak alerts against confidence thresholds.',
      'outbreak.review.item1.label': 'Nagpur Corn Yellow Margins Alert',
      'outbreak.review.item1.desc': 'Signal strength: 4 report counts in 7 days.',
      'outbreak.action.verify': 'Verify Alert',
      'outbreak.action.dismiss': 'Dismiss Alert',
      'outbreak.details.title': 'Outbreak Intel Correlation',
      'outbreak.details.subtitle': 'Correlation analysis of symptoms and weather context.',
      'outbreak.details.symptoms.label': 'Observed Symptoms',
      'outbreak.details.symptoms.val': 'Leaf margin yellowing / spots',
      'outbreak.details.weather.label': 'Weather Correlation',
      'outbreak.details.weather.val': 'Temp rise 32C, Humidity 85%',
      'outbreak.action.back': 'Back to Map',
      'privacy.title': 'Farmer Privacy & Consents',
      'privacy.subtitle': 'Manage locations, camera retention, and audit options.',
      'privacy.location.label': 'Approximate Location Sharing',
      'privacy.image.label': 'Retain Uploaded Crop Images',
      'privacy.voice.label': 'Retain Voice Log Recording Samples',
      'privacy.outbreak.label': 'Participate in Anonymized Outbreak Analytics',
      'privacy.consent.enable': 'Enable / Opt-In',
      'privacy.consent.disable': 'Disable / Opt-Out',
      'privacy.action.save': 'Save Preferences',
      'privacy.action.export': 'Export History',
      'privacy.action.delete': 'Delete My Data',
      'privacy.action.cancel': 'Cancel',
      'privacy.export.title': 'Export My Farm History',
      'privacy.export.subtitle': 'Download a complete JSON database dump of your farm digital twin.',
      'privacy.export.action.trigger': 'Generate & Download Backup',
      'privacy.delete.title': 'Delete My Farm Data',
      'privacy.delete.subtitle': 'Permanently purge your digital twin and history from the advisor database.',
      'privacy.delete.action.trigger': 'Yes, Purge Everything',
      'privacy.consent.title': 'Outbreak Telemetry Participation',
      'privacy.consent.action.grant': 'I Agree to Participate',
      'escalate.status.title': 'Expert Escalation Status',
      'escalate.status.subtitle': 'Your consultation has been escalated to an expert agronomist.',
      'escalate.status.ticket.label': 'Ticket ID',
      'escalate.status.ticket.val': 'TKT-4927',
      'escalate.status.state.label': 'Status',
      'escalate.status.state.val': 'Assigned',
      'escalate.status.expert.label': 'Assigned Expert',
      'escalate.status.expert.val': 'Dr. Ramesh (Chief Agronomist)',
      'escalate.action.back': 'Back to Chat',
      'home.title': 'Home',
      'home.greeting.title': 'Namaste Madhav Ji',
      'home.greeting.subtitle': 'Wheat Field · 10 Acres',
      'home.weather.title': "Today's Weather",
      'home.weather.desc': 'Clear sky · 0% chance of rain',
      'home.alert.title': 'Moisture Alert',
      'home.alert.desc': 'Soil moisture is very dry (35%). Crop impact possible.',
      'home.action.title': 'Water tomorrow morning and apply 15 kg Urea',
      'home.action.label': 'Remind Me',
      'home.quickActions.title': 'Quick Actions',
      'home.quickActions.photo.label': 'Take Crop Photo',
      'home.quickActions.photo.desc': 'Identify issues',
      'home.quickActions.voice.label': 'Ask by Voice',
      'home.quickActions.voice.desc': 'Speak to advisor',
      'home.quickActions.market.label': "Today's Mandi Rates",
      'home.quickActions.market.desc': 'Check latest market rates',
      'home.quickActions.log.label': 'Log Farm Work',
      'home.quickActions.log.desc': 'Record farm activities',
      'more.title': 'More',
      'more.subtitle': 'Krishi Sampark - v2.0.0',
      'more.settings.title': 'Settings & Options',
      'more.items.profile.label': 'Profile',
      'more.items.profile.desc': 'View farmer details',
      'more.items.history.label': 'Farm History',
      'more.items.history.desc': 'Record of past harvests',
      'more.items.support.label': 'Expert Support',
      'more.items.support.desc': 'Consult agronomists',
      'more.items.offline.label': 'Offline Download',
      'more.items.offline.desc': 'Keep models & data offline',
      'more.items.sync.label': 'Sync Status',
      'more.items.sync.desc': 'All data is secure',
      'more.items.voice.label': 'Language & Voice',
      'more.items.voice.desc': 'Change voice preferences',
      'more.items.whatif.label': 'What-If Planner',
      'more.items.whatif.desc': 'Simulate crop scenarios',
      'more.items.help.label': 'About App',
      'more.items.help.desc': 'Version 2.0.0',
      'more.expert.title': 'Expert Mode',
      'more.expert.desc': 'Activate expert metrics and simulators.',
      'more.expert.action.enable': 'Enable',
      'more.expert.action.disable': 'Disable',
      'farm.title': 'My Farm Details',
      'farm.cropHealth.title': 'Crop Health',
      'farm.cropHealth.good': 'Optimal',
      'farm.soilMoisture.title': 'Soil Moisture',
      'farm.soilMoisture.waterSoon': 'Dry - Water Soon',
      'farm.recommendation.title': "Today's Advisory",
      'farm.recommendation.desc': 'Irrigate tomorrow: 15,000 litres needed.'
    },
    'hi': {
      'console.title': 'कृषि विशेषज्ञ संचालन कंसोल',
      'console.subtitle': 'परामर्श कतारों को हल करें और विशेषज्ञ सलाह भेजें।',
      'console.case1.label': 'केस आईडी: esc_1 (मक्का लीफ ब्लाइट)',
      'console.case1.desc': 'नागपुर क्षेत्र में पत्तियों के पीले किनारों की रिपोर्ट।',
      'console.case2.label': 'केस आईडी: esc_2 (टमाटर रस्ट)',
      'console.case2.desc': 'निचली पत्तियों पर जंग के धब्बे देखे गए।',
      'console.action.assign': 'मुझे सौंपें',
      'console.action.resolve': 'केस हल करें',
      'console.action.close': 'टिकट बंद करें',
      'outbreak.map.title': 'क्षेत्रीय प्रकोप जोखिम मानचित्र',
      'outbreak.map.subtitle': 'सत्यापित कीट लक्षणों का अज्ञात एकत्रीकरण।',
      'outbreak.map.nagpur.label': 'नागपुर क्षेत्रीय क्लस्टर',
      'outbreak.map.nagpur.desc': 'गेहूं के पत्तों की जंग के 6 पुष्ट मामले मिले।',
      'outbreak.action.details': 'सहसंबंध विवरण देखें',
      'outbreak.review.title': 'प्रकोप खुफिया अलर्ट',
      'outbreak.review.subtitle': 'विश्वास सीमाओं के खिलाफ प्रकोप अलर्ट की समीक्षा करें।',
      'outbreak.review.item1.label': 'नागपुर मक्का पीली पत्ती अलर्ट',
      'outbreak.review.item1.desc': 'सिग्नल ताकत: 7 दिनों में 4 रिपोर्ट संख्या।',
      'outbreak.action.verify': 'अलर्ट सत्यापित करें',
      'outbreak.action.dismiss': 'अलर्ट खारिज करें',
      'outbreak.details.title': 'प्रकोप खुफिया सहसंबंध',
      'outbreak.details.subtitle': 'लक्षणों और मौसम के संदर्भ का सहसंबंध विश्लेषण।',
      'outbreak.details.symptoms.label': 'देखे गए लक्षण',
      'outbreak.details.symptoms.val': 'पत्तियों के किनारों का पीला होना / धब्बे',
      'outbreak.details.weather.label': 'मौसम सहसंबंध',
      'outbreak.details.weather.val': 'तापमान वृद्धि 32C, आर्द्रता 85%',
      'outbreak.action.back': 'नक्शे पर वापस जाएं',
      'privacy.title': 'किसान गोपनीयता और सहमति',
      'privacy.subtitle': 'स्थान, कैमरा छवियों और ऑडिट विकल्पों का प्रबंधन करें।',
      'privacy.location.label': 'अनुमानित स्थान साझाकरण',
      'privacy.image.label': 'अपलोड की गई फसल छवियों को रखें',
      'privacy.voice.label': 'वॉयस लॉग रिकॉर्डिंग नमूने रखें',
      'privacy.outbreak.label': 'अज्ञान प्रकोप विश्लेषण में भाग लें',
      'privacy.consent.enable': 'सक्षम करें / अनुमति दें',
      'privacy.consent.disable': 'अक्षम करें / मना करें',
      'privacy.action.save': 'प्राथमिकताएं सहेजें',
      'privacy.action.export': 'इतिहास निर्यात करें',
      'privacy.action.delete': 'मेरा डेटा हटाएं',
      'privacy.action.cancel': 'रद्द करें',
      'privacy.export.title': 'मेरा कृषि इतिहास निर्यात करें',
      'privacy.export.subtitle': 'अपने कृषि डिजिटल ट्विन का एक पूरा बैकअप डाउनलोड करें।',
      'privacy.export.action.trigger': 'बैकअप बनाएं और डाउनलोड करें',
      'privacy.delete.title': 'मेरा कृषि डेटा हटाएं',
      'privacy.delete.subtitle': 'डेटाबेस से अपनी पूरी जानकारी स्थायी रूप से मिटा दें।',
      'privacy.delete.action.trigger': 'हाँ, सब कुछ मिटा दें',
      'privacy.consent.title': 'प्रकोप टेलीमेट्री भागीदारी',
      'privacy.consent.action.grant': 'मैं भाग लेने के लिए सहमत हूँ',
      'escalate.status.title': 'विशेषज्ञ एस्केलेशन स्थिति',
      'escalate.status.subtitle': 'आपका परामर्श एक विशेषज्ञ कृषि वैज्ञानिक को भेजा गया है।',
      'escalate.status.ticket.label': 'टिकट आईडी',
      'escalate.status.ticket.val': 'TKT-4927',
      'escalate.status.state.label': 'स्थिति',
      'escalate.status.state.val': 'सौंपा गया',
      'escalate.status.expert.label': 'सौंपे गए विशेषज्ञ',
      'escalate.status.expert.val': 'डॉ. रमेश (मुख्य कृषि वैज्ञानिक)',
      'escalate.action.back': 'चैट पर वापस जाएं',
      'home.title': 'मुख्य पृष्ठ (Home)',
      'home.greeting.title': 'नमस्ते माधव जी',
      'home.greeting.subtitle': 'गेहूँ का खेत · 10 एकड़',
      'home.weather.title': 'आज का मौसम',
      'home.weather.desc': 'साफ आसमान · बारिश की संभावना 0%',
      'home.alert.title': 'नमी चेतावनी',
      'home.alert.desc': 'मिट्टी की नमी बहुत सूखी है (35%)। फसल पर असर हो सकता है।',
      'home.action.title': 'कल सुबह सिंचाई करें और 15 kg यूरिया डालें',
      'home.action.label': 'याद दिलाएँ',
      'home.quickActions.title': 'त्वरित कार्य (Quick Actions)',
      'home.quickActions.photo.label': 'फसल की फोटो लें',
      'home.quickActions.photo.desc': 'समस्या पहचानें',
      'home.quickActions.voice.label': 'आवाज से पूछें',
      'home.quickActions.voice.desc': 'बोलकर सलाह लें',
      'home.quickActions.market.label': 'आज का मंडी भाव',
      'home.quickActions.market.desc': 'ताजा मंडी रेट देखें',
      'home.quickActions.log.label': 'खेती का काम दर्ज करें',
      'home.quickActions.log.desc': 'खेती कार्य दर्ज करें',
      'more.title': 'अन्य (More)',
      'more.subtitle': 'Krishi Sampark - v2.0.0',
      'more.settings.title': 'सेटिंग्स और विकल्प',
      'more.items.profile.label': 'प्रोफ़ाइल',
      'more.items.profile.desc': 'किसान विवरण देखें',
      'more.items.history.label': 'खेत का इतिहास',
      'more.items.history.desc': 'पिछली फसलों का रिकॉर्ड',
      'more.items.support.label': 'विशेषज्ञ सहायता',
      'more.items.support.desc': 'कृषि वैज्ञानिकों से संपर्क करें',
      'more.items.offline.label': 'ऑफ़लाइन डाउनलोड',
      'more.items.offline.desc': 'मॉडल और डेटा ऑफ़लाइन रखें',
      'more.items.sync.label': 'सिंक स्थिति',
      'more.items.sync.desc': 'सभी जानकारी सुरक्षित है',
      'more.items.voice.label': 'भाषा और आवाज',
      'more.items.voice.desc': 'बोली सेटिंग्स बदलें',
      'more.items.whatif.label': 'क्या होगा अगर (What-If Planner)',
      'more.items.whatif.desc': 'अगर ऐसा हो तो? (सिमुलेटर)',
      'more.items.help.label': 'ऐप के बारे में',
      'more.items.help.desc': 'संस्करण 2.0.0',
      'more.expert.title': 'विशेषज्ञ मोड (Expert Mode)',
      'more.expert.desc': 'विस्तृत ग्राफ़, सटीक डेटा और सिमुलेटर नियंत्रण सक्रिय करें।',
      'more.expert.action.enable': 'चालू करें',
      'more.expert.action.disable': 'बंद करें',
      'farm.title': 'मेरे खेत का विवरण',
      'farm.cropHealth.title': 'फसल स्वास्थ्य',
      'farm.cropHealth.good': 'इष्टतम',
      'farm.soilMoisture.title': 'मिट्टी की नमी',
      'farm.soilMoisture.waterSoon': 'सूखा - जल्द पानी दें',
      'farm.recommendation.title': 'आज की सलाह',
      'farm.recommendation.desc': 'कल सुबह सिंचाई करें: 15,000 लीटर पानी की आवश्यकता है।'
    },
    'mr': {
      'escalate.status.title': 'तज्ञ एस्केलेशन स्थिती',
      'escalate.status.subtitle': 'तुमची सल्लामसलत तज्ञ कृषी शास्त्रज्ञाकडे पाठवण्यात आली आहे.',
      'escalate.status.ticket.label': 'तिकीट आयडी',
      'escalate.status.ticket.val': 'TKT-4927',
      'escalate.status.state.label': 'स्थिती',
      'escalate.status.state.val': 'नियुक्त केले',
      'escalate.status.expert.label': 'नियुक्त तज्ञ',
      'escalate.status.expert.val': 'डॉ. रमेश (मुख्य कृषी शास्त्रज्ञ)',
      'escalate.action.back': 'चॅटवर परत जा',
      'home.title': 'मुख्य पृष्ठ (Home)',
      'home.greeting.title': 'नमस्कार माधव जी',
      'home.greeting.subtitle': 'गहू शेत · १० एकर',
      'home.weather.title': 'आजचे हवामान',
      'home.weather.desc': 'स्वच्छ आकाश · पावसाची शक्यता ०%',
      'home.alert.title': 'ओलावा चेतावणी',
      'home.alert.desc': 'जमिनीतील ओलावा खूप कमी आहे (३५%). पिकावर परिणाम होऊ शकतो.',
      'home.action.title': 'उद्या सकाळी पाणी द्या आणि १५ किलो युरिया टाका',
      'home.action.label': 'आठवण ठेवा',
      'home.quickActions.title': 'त्वरित कृती',
      'home.quickActions.photo.label': 'पिकाचा फोटो घ्या',
      'home.quickActions.photo.desc': 'समस्या ओळखा',
      'home.quickActions.voice.label': 'आवाज देऊन विचारा',
      'home.quickActions.voice.desc': 'बोलून सल्ला घ्या',
      'home.quickActions.market.label': 'आजचे बाजार भाव',
      'home.quickActions.market.desc': 'ताजे बाजार भाव पहा',
      'home.quickActions.log.label': 'शेतातील काम नोंदवा',
      'home.quickActions.log.desc': 'काम नोंदवून ठेवा',
      'more.title': 'इतर (More)',
      'more.subtitle': 'Krishi Sampark - v2.0.0',
      'more.settings.title': 'पर्याय आणि सेटिंग्ज',
      'more.items.profile.label': 'प्रोफाइल',
      'more.items.profile.desc': 'शेतकऱ्याची माहिती पहा',
      'more.items.history.label': 'शेताचा इतिहास',
      'more.items.history.desc': 'मागील पिकांची नोंद',
      'more.items.support.label': 'तज्ज्ञांची मदत',
      'more.items.support.desc': 'कृषी शास्त्रज्ञांशी संपर्क साधा',
      'more.items.offline.label': 'ऑफलाईन डाउनलोड',
      'more.items.offline.desc': 'मॉडेल आणि डेटा ऑफलाईन ठेवा',
      'more.items.sync.label': 'सिंक स्थिती',
      'more.items.sync.desc': 'सर्व माहिती सुरक्षित आहे',
      'more.items.voice.label': 'भाषा आणि आवाज',
      'more.items.voice.desc': 'उच्चार सेटिंग्ज बदला',
      'more.items.whatif.label': 'जर असे झाले तर? (What-If)',
      'more.items.whatif.desc': 'असे झाले तर काय? (सिम्युलेटर)',
      'more.items.help.label': 'अ‍ॅप बद्दल माहिती',
      'more.items.help.desc': 'आवृत्ती २.०.०',
      'more.expert.title': 'तज्ज्ञ मोड (Expert Mode)',
      'more.expert.desc': 'तपशीलवार आलेख आणि सिम्युलेटर नियंत्रणे सक्रिय करा.',
      'more.expert.action.enable': 'सुरू करा',
      'more.expert.action.disable': 'बंद करा',
      'farm.title': 'माझा शेत',
      'farm.cropHealth.title': 'पिकाचे आरोग्य',
      'farm.cropHealth.good': 'उत्तम',
      'farm.soilMoisture.title': 'मातीतील ओलावा',
      'farm.soilMoisture.waterSoon': 'कोरडे - लवकर पाणी द्या',
      'farm.recommendation.title': 'आजचा सल्ला',
      'farm.recommendation.desc': 'उद्या सकाळी पाणी द्या: १५,००० लीटर पाण्याची गरज आहे.'
    },
    'sw': {
      'escalate.status.title': 'Hali ya Rufaa ya Wataalamu',
      'escalate.status.subtitle': 'Ushauri wako umetumwa kwa mtaalamu wa kilimo.',
      'escalate.status.ticket.label': 'Nambari ya Tiketi',
      'escalate.status.ticket.val': 'TKT-4927',
      'escalate.status.state.label': 'Hali',
      'escalate.status.state.val': 'Imekabidhiwa',
      'escalate.status.expert.label': 'Mtaalamu Aliyekabidhiwa',
      'escalate.status.expert.val': 'Dkt. Ramesh (Mkuu wa Wataalamu wa Kilimo)',
      'escalate.action.back': 'Rudi kwenye Mazungumzo',
      'home.title': 'Nyumbani',
      'home.greeting.title': 'Jambo Madhav Ji',
      'home.greeting.subtitle': 'Shamba la Ngano · Ekari 10',
      'home.weather.title': 'Hali ya Hewa ya Leo',
      'home.weather.desc': 'Anga wazi · 0% uwezekano wa mvua',
      'home.alert.title': 'Tahadhari ya Unyevu',
      'home.alert.desc': 'Unyevu wa udongo ni mkavu sana (35%). Athari kwa mazao inawezekana.',
      'home.action.title': 'Maji kesho asubuhi na uweke kilo 15 za Urea',
      'home.action.label': 'Nikumbushe',
      'home.quickActions.title': 'Hatua za Haraka',
      'home.quickActions.photo.label': 'Piga Picha ya Mazao',
      'home.quickActions.photo.desc': 'Tambua matatizo',
      'home.quickActions.voice.label': 'Uliza kwa Sauti',
      'home.quickActions.voice.desc': 'Ongea na mshauri',
      'home.quickActions.market.label': 'Bei za Soko Leo',
      'home.quickActions.market.desc': 'Angalia bei za hivi karibuni',
      'home.quickActions.log.label': 'Nakili Kazi ya Shamba',
      'home.quickActions.log.desc': 'Rekodi shughuli za shamba',
      'more.title': 'Zaidi',
      'more.subtitle': 'Krishi Sampark - v2.0.0',
      'more.settings.title': 'Chaguzi na Mipangilio',
      'more.items.profile.label': 'Wasifu',
      'more.items.profile.desc': 'Angalia maelezo ya mkulima',
      'more.items.history.label': 'Historia ya Shamba',
      'more.items.history.desc': 'Rekodi ya mavuno yaliyopita',
      'more.items.support.label': 'Msaada wa Wataalamu',
      'more.items.support.desc': 'Wasiliana na wataalamu wa kilimo',
      'more.items.offline.label': 'Pakua Nje ya Mtandao',
      'more.items.offline.desc': 'Weka mifano na data nje ya mtandao',
      'more.items.sync.label': 'Hali ya Usawazishaji',
      'more.items.sync.desc': 'Data zote ziko salama',
      'more.items.voice.label': 'Lugha na Sauti',
      'more.items.voice.desc': 'Badilisha mipangilio ya sauti',
      'more.items.whatif.label': 'Kipanga Njia cha What-If',
      'more.items.whatif.desc': 'Ikiwa hii itatokea? (Kifanisi)',
      'more.items.help.label': 'Kuhusu Programu',
      'more.items.help.desc': 'Toleo la 2.0.0',
      'more.expert.title': 'Njia ya Wataalamu',
      'more.expert.desc': 'Amilisha vipimo vya kina vya grafu na vidhibiti vya kifanisi.',
      'more.expert.action.enable': 'Washa',
      'more.expert.action.disable': 'Zima',
      'farm.title': 'Shamba Langu',
      'farm.cropHealth.title': 'Afya ya Mazao',
      'farm.cropHealth.good': 'Nzuri sana',
      'farm.soilMoisture.title': 'Unyevu wa Udongo',
      'farm.soilMoisture.waterSoon': 'Kavu - Wagilia Hivi Karibuni',
      'farm.recommendation.title': 'Ushauri wa Leo',
      'farm.recommendation.desc': 'Wagilia kesho asubuhi: Lita 15,000 zinahitajika.'
    },
    'te': {
      'escalate.status.title': 'నిపుణుల ఎస్కలేషన్ స్థితి',
      'escalate.status.subtitle': 'మీ సంప్రదింపులు నిపుణులైన వ్యవసాయ శాస్త్రవేత్తకు పంపబడ్డాయి.',
      'escalate.status.ticket.label': 'టికెట్ ఐడి',
      'escalate.status.ticket.val': 'TKT-4927',
      'escalate.status.state.label': 'స్థితి',
      'escalate.status.state.val': 'కేటాయించబడింది',
      'escalate.status.expert.label': 'కేటాయించిన నిపుణుడు',
      'escalate.status.expert.val': 'డాక్టర్ రమేష్ (చీఫ్ అగ్రోనమిస్ట్)',
      'escalate.action.back': 'చాట్‌కి తిరిగి వెళ్ళు',
      'home.title': 'హోమ్ (Home)',
      'home.greeting.title': 'నమస్తే మాధవ్ జీ',
      'home.greeting.subtitle': 'గోధుమ పొలం · 10 ఎకరాలు',
      'home.weather.title': 'నేటి వాతావరణం',
      'home.weather.desc': 'నిర్మలమైన ఆకాశం · వర్ష సూచన 0%',
      'home.alert.title': 'తేమ హెచ్చరిక',
      'home.alert.desc': 'నేల తేమ చాలా తక్కువగా ఉంది (35%). పంటపై ప్రభావం ఉండవచ్చు.',
      'home.action.title': 'రేపు ఉదయం నీరు పెట్టండి మరియు 15 కిలోల యూరియా వేయండి',
      'home.action.label': 'గుర్తు చేయి',
      'home.quickActions.title': 'త్వరిత చర్యలు',
      'home.quickActions.photo.label': 'పంట ఫోటో తీయండి',
      'home.quickActions.photo.desc': 'సమస్యలను గుర్తించండి',
      'home.quickActions.voice.label': 'ఆవాజ్ ద్వారా అడగండి',
      'home.quickActions.voice.desc': 'మాట్లాడి సలహా తీసుకోండి',
      'home.quickActions.market.label': 'నేటి మార్కెట్ ధరలు',
      'home.quickActions.market.desc': 'తాజా మార్కెట్ ధరలను చూడండి',
      'home.quickActions.log.label': 'పొలం పనిని నమోదు చేయండి',
      'home.quickActions.log.desc': 'వ్యవసాయ కార్యకలాపాలను రికార్డ్ చేయండి',
      'more.title': 'మరింత (More)',
      'more.subtitle': 'Krishi Sampark - v2.0.0',
      'more.settings.title': 'ఎంపికలు మరియు సెట్టింగులు',
      'more.items.profile.label': 'ప్రొఫైల్',
      'more.items.profile.desc': 'రైతు వివరాలను చూడండి',
      'more.items.history.label': 'పొలం చరిత్ర',
      'more.items.history.desc': 'గత పంటల రికార్డు',
      'more.items.support.label': 'నిపుణుల సహాయం',
      'more.items.support.desc': 'వ్యవసాయ శాస్త్రవేత్తలను సంప్రదించండి',
      'more.items.offline.label': 'ఆఫ్‌లైన్ డౌన్‌లోడ్',
      'more.items.offline.desc': 'నమూనాలు & డేటాను ఆఫ్‌లైన్‌లో ఉంచండి',
      'more.items.sync.label': 'సమకాలీకరణ స్థితి',
      'more.items.sync.desc': 'అన్ని డేటా సురక్షితంగా ఉంది',
      'more.items.voice.label': 'భాష & వాయిస్',
      'more.items.voice.desc': 'వాయిస్ సెట్టింగులను మార్చండి',
      'more.items.whatif.label': 'వాట్-ఇఫ్ ప్లానర్',
      'more.items.whatif.desc': 'ఒకవేళ ఇలా జరిగితే? (సిమ్యులేటర్)',
      'more.items.help.label': 'యాప్ గురించి',
      'more.items.help.desc': 'వెర్షన్ 2.0.0',
      'more.expert.title': 'నిపుణుల మోడ్ (Expert Mode)',
      'more.expert.desc': 'వివరణాత్మక గ్రాఫ్‌లు మరియు సిమ్యులేటర్ నియంత్రణలను సక్రియం చేయండి.',
      'more.expert.action.enable': 'సక్రియం చేయి',
      'more.expert.action.disable': 'నిష్క్రియం చేయి',
      'farm.title': 'నా పొలం',
      'farm.cropHealth.title': 'పంట ఆరోగ్యం',
      'farm.cropHealth.good': 'చాలా బాగుంది',
      'farm.soilMoisture.title': 'నేల తేమ',
      'farm.soilMoisture.waterSoon': 'పొడి నేల - వెంటనే నీరు పెట్టండి',
      'farm.recommendation.title': 'ఈరోజు సలహా',
      'farm.recommendation.desc': 'రేపు ఉదయం నీరు పెట్టండి: 15,000 లీటర్ల నీరు అవసరం.'
    }
  };

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
      .replace(/^\w/, c => c.toUpperCase());
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
    f.write(new_content)
print("translations.js patched successfully.")
