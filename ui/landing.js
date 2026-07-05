(() => {
  const modal = document.getElementById('guest-modal');
  const guestEmail = document.getElementById('guest-email');
  const guestError = document.getElementById('guest-error');
  const languageSelector = document.getElementById('language-selector');
  const headerGoogleFallback = document.getElementById('header-google-fallback');
  const heroGoogleFallback = document.getElementById('hero-google-fallback');
  const authStatus = document.getElementById('auth-status');

  const EN = {
    'landing.header.brandTitle': 'Krishi Sampark',
    'landing.header.brandSubtitle': 'Smart farming help in your language',
    'landing.header.navAbout': 'About',
    'landing.header.navFeatures': 'Features',
    'landing.header.navHowItWorks': 'How It Works',
    'landing.header.navSafetyTrust': 'Safety & Trust',
    'landing.header.navContact': 'Contact',

    'landing.hero.title': 'Your farming companion for better decisions',
    'landing.hero.description': 'Ask questions, check crop problems, understand soil reports, plan irrigation, and view mandi prices in your own language.',
    'landing.hero.continueAsGuest': 'Continue as Guest',
    'landing.hero.signInWithGoogle': 'Sign in with Google',
    'landing.hero.voiceAssistTitle': 'Voice Assist',
    'landing.hero.voiceAssistText': 'Tap mic and ask your farming question in your language',
    'landing.hero.trustNote': 'No technical knowledge required. Built for farmers, students, and agriculture advisors.',
    'landing.hero.chipVoice': 'Voice questions',
    'landing.hero.chipPhoto': 'Photo crop check',
    'landing.hero.chipMarket': 'Live mandi trends',
    'landing.hero.trustPanelTitle': 'Works even with limited internet',
    'landing.hero.trust1': 'Local language support (5+ languages)',
    'landing.hero.trust2': 'Offline-first - your data stays safe',
    'landing.hero.trust3': 'Safety-checked advice for fertilizers & pesticides',
    'landing.hero.trust4': 'Expert help for complex issues',
    'landing.hero.trust5': 'Privacy aware - your data is protected',

    'landing.auth.guestTitle': 'Start in Guest Mode',
    'landing.auth.guestMessage': 'Guest mode lets you try the app immediately. Your data stays on this device. Sign in with Google to save your farm profile and access it later.',
    'landing.auth.emailOptional': 'Email (optional)',
    'landing.auth.continue': 'Continue',
    'landing.auth.skip': 'Skip',
    'landing.auth.close': 'Close',
    'landing.auth.invalidEmail': 'Please enter a valid email or leave it blank.',
    'landing.auth.guestError': 'Unable to continue as guest. Please try again.',
    'landing.auth.signingInSecurely': 'Signing you in securely...',

    'landing.features.askTitle': 'Ask or Speak to Krishi Sastri',
    'landing.features.askDescription': 'Ask by text or voice and get simple answers for crop, water, fertilizer, and pest questions.',
    'landing.features.photoTitle': 'Crop Photo Check',
    'landing.features.photoDescription': 'Take a photo and get guided help for crop health problems.',
    'landing.features.soilTitle': 'Soil Report',
    'landing.features.soilDescription': 'Upload a soil test report and understand what it means in simple words.',
    'landing.features.marketTitle': 'Mandi Prices',
    'landing.features.marketDescription': 'Check daily market prices and trends in your local market.',
    'landing.features.planTitle': "Today's Farm Plan",
    'landing.features.planDescription': "See simple recommended actions for today's farm activities.",
    'landing.features.expertTitle': 'Expert Help',
    'landing.features.expertDescription': 'Escalate complex issues to agriculture experts for support.',

    'landing.howItWorks.title': 'How it works',
    'landing.howItWorks.summary': 'Three quick steps to get simple farm guidance from a photo, voice, or text question.',
    'landing.howItWorks.step1Title': 'Tell us about your farm',
    'landing.howItWorks.step1Description': 'Add your crop, location, soil type, and farm details.',
    'landing.howItWorks.step2Title': 'Ask, upload, or take a photo',
    'landing.howItWorks.step2Description': 'Ask questions, upload soil report, or take a photo of your crop.',
    'landing.howItWorks.step3Title': 'Get simple guidance and next actions',
    'landing.howItWorks.step3Description': 'Receive easy advice, safety-checked recommendations, and follow next steps.',

    'landing.trust.title': 'Made for real farming conditions',
    'landing.trust.offlineTitle': 'Offline-first',
    'landing.trust.offlineDescription': 'Works with limited internet',
    'landing.trust.languageTitle': 'Local languages',
    'landing.trust.languageDescription': 'Speak your own language',
    'landing.trust.farmerFriendlyTitle': 'Farmer friendly',
    'landing.trust.farmerFriendlyDescription': 'Easy words, simple recommendations',
    'landing.trust.safetyTitle': 'Safety first',
    'landing.trust.safetyDescription': 'Checked advice for fertilizers and pesticides',
    'landing.trust.expertTitle': 'Expert network',
    'landing.trust.expertDescription': 'Human experts for complex cases',
    'landing.trust.privacyTitle': 'Privacy protected',
    'landing.trust.privacyDescription': 'Your data is safe and secure',

    'landing.capstone.title': 'Krishi Sampark Platform',
    'landing.capstone.description': 'Capstone demo platform for offline-first agriculture intelligence with multilingual guidance, safety-checked recommendations, and expert escalation support.',

    'landing.footer.brandTitle': 'Krishi Sampark',
    'landing.footer.brandSubtitle': 'Smart farming help in your language',
    'landing.footer.about': 'About Us',
    'landing.footer.privacy': 'Privacy Policy',
    'landing.footer.terms': 'Terms of Use',
    'landing.footer.help': 'Help',
    'landing.footer.contact': 'Contact Us',
    'landing.footer.copyright': '© 2025 Krishi Sampark. All rights reserved.'
  };

  function placeholderMap(prefix) {
    const out = {};
    Object.keys(EN).forEach((key) => {
      out[key] = `${prefix} ${EN[key]}`;
    });
    return out;
  }

  const TRANSLATIONS = {
    en: EN,
    hi: placeholderMap('[HI]'),
    mr: placeholderMap('[MR]'),
    te: placeholderMap('[TE]'),
    sw: placeholderMap('[SW]')
  };

  let currentLang = 'en';

  function getText(key) {
    const pack = TRANSLATIONS[currentLang] || TRANSLATIONS.en;
    return pack[key] || TRANSLATIONS.en[key] || key;
  }

  function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach((node) => {
      const key = node.getAttribute('data-i18n');
      if (!key) return;
      node.textContent = getText(key);
    });
  }

  function initHowItWorksVisual() {
    const section = document.getElementById('how-it-works');
    const image = document.getElementById('how-it-works-image');
    if (!section || !image) return;

    const showFallback = () => section.classList.add('how-show-fallback');
    const showImage = () => section.classList.remove('how-show-fallback');

    image.addEventListener('load', showImage);
    image.addEventListener('error', showFallback);

    if (image.complete) {
      if (image.naturalWidth > 0) {
        showImage();
      } else {
        showFallback();
      }
    }
  }

  function setLanguage(lang) {
    currentLang = TRANSLATIONS[lang] ? lang : 'en';
    document.documentElement.lang = currentLang;
    if (languageSelector) languageSelector.value = currentLang;
    localStorage.setItem('aaa_preferred_language', currentLang);
    applyTranslations();
  }

  function openGuestModal() {
    modal.classList.remove('hidden');
    guestError.textContent = '';
    guestEmail.value = '';
    guestEmail.focus();
  }

  function closeGuestModal() {
    modal.classList.add('hidden');
  }

  function hasProfile(profile) {
    return Boolean(profile && Array.isArray(profile.fields) && profile.fields.length > 0);
  }

  async function routeAfterSession() {
    const profileRes = await fetch('/api/profile/user', { credentials: 'include' });
    if (!profileRes.ok) {
      window.location.href = '/onboarding';
      return;
    }
    const profile = await profileRes.json();
    if (hasProfile(profile)) {
      window.location.href = '/app/home';
      return;
    }
    window.location.href = '/onboarding';
  }

  async function startGuest(optionalEmail) {
    const email = (optionalEmail || '').trim().toLowerCase();
    if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      guestError.textContent = getText('landing.auth.invalidEmail');
      return;
    }

    const response = await fetch('/api/auth/guest', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, name: 'Guest' })
    });

    if (!response.ok) {
      guestError.textContent = getText('landing.auth.guestError');
      return;
    }

    await routeAfterSession();
  }

  async function googleLogin(credential) {
    if (authStatus) authStatus.textContent = getText('landing.auth.signingInSecurely');

    const response = await fetch('/api/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ credential })
    });

    if (!response.ok) {
      if (authStatus) authStatus.textContent = '';
      alert('Google sign-in failed. Please try again.');
      return;
    }

    await routeAfterSession();
  }

  function promptGoogle() {
    if (authStatus) authStatus.textContent = getText('landing.auth.signingInSecurely');
    window.google?.accounts?.id?.prompt();
  }

  function renderGoogleButtons(clientId) {
    if (!window.google?.accounts?.id || !clientId) return;

    google.accounts.id.initialize({
      client_id: clientId,
      callback: async (resp) => {
        if (!resp || !resp.credential) {
          if (authStatus) authStatus.textContent = '';
          return;
        }
        await googleLogin(resp.credential);
      }
    });

    const buttonTargets = [
      document.getElementById('hero-google-btn'),
      document.getElementById('header-google-btn')
    ];

    buttonTargets.forEach((node) => {
      if (!node) return;
      node.innerHTML = '';
      node.classList.add('ready');
      google.accounts.id.renderButton(node, {
        theme: 'filled_blue',
        size: 'large',
        shape: 'pill',
        text: 'signin_with',
        width: 220
      });
    });

    headerGoogleFallback?.classList.add('is-hidden');
    heroGoogleFallback?.classList.add('is-hidden');
  }

  async function loadAuth() {
    const configRes = await fetch('/api/auth/config', { credentials: 'include' });
    if (!configRes.ok) return;
    const config = await configRes.json();
    if (config?.enabled && config?.client_id) {
      renderGoogleButtons(config.client_id);
    }
  }

  document.getElementById('hero-guest-btn')?.addEventListener('click', openGuestModal);
  document.getElementById('header-guest-btn')?.addEventListener('click', openGuestModal);
  document.getElementById('guest-close')?.addEventListener('click', closeGuestModal);
  document.getElementById('guest-continue')?.addEventListener('click', () => startGuest(guestEmail.value));
  document.getElementById('guest-skip')?.addEventListener('click', () => startGuest(''));
  headerGoogleFallback?.addEventListener('click', promptGoogle);
  heroGoogleFallback?.addEventListener('click', promptGoogle);

  languageSelector?.addEventListener('change', (e) => setLanguage(e.target.value));

  // English-first for reviewers.
  setLanguage('en');
  initHowItWorksVisual();
  loadAuth();
})();
