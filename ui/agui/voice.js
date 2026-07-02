(function() {
  let audioPlayer = null;

  async function speakText(text) {
    const ttsToggle = document.getElementById('tts-toggle');
    if (ttsToggle && !ttsToggle.checked) return;

    window.speechSynthesis.cancel();
    if (audioPlayer) {
      audioPlayer.pause();
      audioPlayer = null;
    }

    const preferredLang = document.getElementById('language-selector')?.value || 'English';
    const cleanText = text.replace(/```[\s\S]*?```/g, '').replace(/[*#_]/g, '');

    const voiceLangMap = {
      'Hindi': 'hi-IN',
      'Marathi': 'mr-IN',
      'Telugu': 'te-IN',
      'Swahili': 'sw-KE',
      'English': 'en-US'
    };
    const targetLangCode = voiceLangMap[preferredLang] || 'en-US';

    const voices = window.speechSynthesis.getVoices();
    const langVoices = voices.filter(v => v.lang.startsWith(targetLangCode));

    const maleKeywords = ['male', 'david', 'mark', 'ravi', 'rishi', 'mohan', 'karan', 'madhur', 'hemant', 'alex', 'fred', 'daniel', 'nathan', 'oliver', 'george', 'microsoft'];
    const femaleKeywords = ['samantha', 'siri', 'veena', 'heera', 'kalpana', 'neerja', 'zira', 'hazel', 'susan', 'linda', 'helen', 'zari', 'female'];

    let preferredVoice = langVoices.find(v => {
      const nameLower = v.name.toLowerCase();
      return maleKeywords.some(kw => nameLower.includes(kw)) && !femaleKeywords.some(fw => nameLower.includes(fw));
    });

    if (preferredVoice) {
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.lang = targetLangCode;
      utterance.voice = preferredVoice;
      window.speechSynthesis.speak(utterance);
    } else {
      try {
        const response = await fetch('/api/tts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ lang: preferredLang, text: cleanText })
        });
        if (response.ok) {
          const blob = await response.blob();
          const audioUrl = URL.createObjectURL(blob);
          audioPlayer = new Audio(audioUrl);
          audioPlayer.play();
        } else {
          console.warn("Backend TTS responded with error status:", response.status);
        }
      } catch (err) {
        console.warn("Backend TTS playback failed:", err);
      }
    }
  }

  function triggerMicrophoneListen() {
    const mainVoiceBtn = document.getElementById('main-voice-btn');
    const micWaveContainer = document.getElementById('mic-wave-container');
    const voiceStatusLabel = document.getElementById('voice-status-label');
    const userInputField = document.getElementById('user-input-field');

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const rec = new SpeechRecognition();
      rec.continuous = false;
      rec.interimResults = false;
      const currentLang = localStorage.getItem('aaa_preferred_language') || 'English';
      
      if (currentLang === 'Hindi') rec.lang = 'hi-IN';
      else if (currentLang === 'Marathi') rec.lang = 'mr-IN';
      else if (currentLang === 'Telugu') rec.lang = 'te-IN';
      else if (currentLang === 'Swahili') rec.lang = 'sw-KE';
      else rec.lang = 'en-US';

      window.recognitionInstance = rec;
      
      rec.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (userInputField) userInputField.value = transcript;
        if (mainVoiceBtn) mainVoiceBtn.classList.remove('listening');
        if (micWaveContainer) micWaveContainer.style.display = 'none';
        if (voiceStatusLabel) voiceStatusLabel.textContent = 'बोलकर पूछें';
        
        if (typeof window.appendMessage === 'function') {
          window.appendMessage('System', `मैंने सुना: "${transcript}"`, 'system-msg');
        }
        if (typeof window.handleSend === 'function') {
          window.handleSend();
        }
      };
      
      rec.onerror = (e) => {
        console.warn("Speech error:", e.error);
        if (mainVoiceBtn) mainVoiceBtn.classList.remove('listening');
        if (micWaveContainer) micWaveContainer.style.display = 'none';
        if (voiceStatusLabel) voiceStatusLabel.textContent = 'बोलकर पूछें';
        if (typeof window.showToast === 'function') {
          window.showToast("Speech Error", `Could not recognize speech: ${e.error}`, "warning");
        }
      };
      
      rec.start();
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    const mainVoiceBtn = document.getElementById('main-voice-btn');
    const micWaveContainer = document.getElementById('mic-wave-container');
    const voiceStatusLabel = document.getElementById('voice-status-label');

    if (mainVoiceBtn) {
      mainVoiceBtn.addEventListener('click', () => {
        if (mainVoiceBtn.classList.contains('listening')) {
          mainVoiceBtn.classList.remove('listening');
          if (micWaveContainer) micWaveContainer.style.display = 'none';
          if (voiceStatusLabel) voiceStatusLabel.textContent = 'बोलकर पूछें';
          if (window.recognitionInstance) {
            window.recognitionInstance.stop();
          }
        } else {
          mainVoiceBtn.classList.add('listening');
          if (micWaveContainer) micWaveContainer.style.display = 'flex';
          if (voiceStatusLabel) voiceStatusLabel.textContent = 'मैं सुन रहा हूँ...';
          triggerMicrophoneListen();
        }
      });
    }
  });

  window.speakText = speakText;
  window.triggerMicrophoneListen = triggerMicrophoneListen;
})();
