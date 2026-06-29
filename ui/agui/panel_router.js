/**
 * panel_router.js - Dynamic Intent-based Workspace Panel Switcher
 * Decouples agent conversation topics from static tabs with word boundary checks.
 */
(function() {
  // Ordered by priority (specific sandbox/simulation keywords checked first)
  const intentMap = [
    {
      schema: 'simulation',
      keywords: ['step', 'sandbox', 'advance', 'sim', 'simulator', 'simulation', 'fertilizer', 'growth', 'harvest']
    },
    {
      schema: 'market_insights',
      keywords: ['price', 'pricing', 'market', 'cbot', 'futures', 'dollar', 'bushel', 'insights']
    },
    {
      schema: 'irrigation_planner',
      keywords: ['irrigate', 'irrigation', 'water', 'sprinkler', 'watering', 'schedule', 'volume', 'gallon', 'planner']
    },
    {
      schema: 'pest_alert',
      keywords: ['pest', 'disease', 'infestation', 'blight', 'aphid', 'protection', 'outbreak', 'spray', 'treatment', 'alert', 'alerts']
    },
    {
      schema: 'crop_dashboard',
      keywords: ['telemetry', 'nitrogen', 'health', 'npk', 'vigor', 'ndvi', 'soil', 'temp', 'nutrient', 'dashboard']
    },
    {
      schema: 'voice_interface',
      keywords: ['voice', 'translate', 'swahili', 'spanish', 'speak', 'mic', 'recording', 'audio', 'readout']
    }
  ];

  window.panelRouter = {
    routeIntent: function(text) {
      if (!text) return null;
      const lowerText = text.toLowerCase();
      
      for (const entry of intentMap) {
        for (const word of entry.keywords) {
          const regex = new RegExp(`\\b${word}\\b`, 'i');
          if (regex.test(lowerText)) {
            return entry.schema;
          }
        }
      }
      return null;
    }
  };
})();
