# Personas & User Journeys

> **Status:** Active
> **Last Updated:** 2026-07-04
> **Owner:** Product / UX

---

## Primary Persona: माधव (Madhav) — The Smallholder Farmer

| Attribute | Detail |
|-----------|--------|
| **Name** | माधव जी (Madhav ji) |
| **Age** | 48 |
| **Location** | Nagpur district, Maharashtra, India |
| **Land** | 5 acres, black clay soil |
| **Crops** | Corn (kharif), Wheat (rabi) |
| **Irrigation** | Drip system (installed 2 years ago) |
| **Phone** | Android smartphone, 2GB RAM, 3G connectivity (intermittent) |
| **Languages** | Hindi (primary), Marathi (regional), limited English |
| **Tech literacy** | Can use WhatsApp, voice calls; struggles with text input |
| **Goals** | Maximize yield, reduce input costs, avoid crop loss from disease/weather |

### Madhav's Day

```
5:00 AM  → Wake up, check weather (clear sky)
6:00 AM  → Walk to field, inspect corn crop (germination stage)
7:00 AM  → Notices leaf discoloration on some plants
8:00 AM  → Opens Krishi Sampark, taps 🎙️ "आवाज से पूछें"
           Says: "मेरे भुट्टे की पत्तियों पर धब्बे हैं"
           → App routes to Pest Detector Agent
           → App suggests taking a photo
8:05 AM  → Takes photo of affected leaf
           → TFLite classifier: "Gray Leaf Spot (77% confidence)"
           → Krishi Sastri: "यह ग्रे लीफ स्पॉट है। 5 दिन में बेहतर होगा।
              अगर बढ़े तो कृषि विशेषज्ञ से सलाह लें।"
           → App offers to log this as a farm activity
12:00 PM → Checks mandi prices: Cotton ₹6,200/quintal (up 3%)
           → Decides to wait for better price
6:00 PM  → Logs irrigation: "15 लीटर पानी दिया"
           → Telemetry syncs to SQLite farm twin
```

## Secondary Persona: राधा (Radha) — The Progressive Farmer

| Attribute | Detail |
|-----------|--------|
| **Name** | राधा देवी (Radha Devi) |
| **Age** | 35 |
| **Location** | Telangana, India |
| **Land** | 8 acres, red sandy loam |
| **Crops** | Cotton, soybeans |
| **Irrigation** | Sprinkler |
| **Phone** | Android, 4GB RAM, 4G |
| **Languages** | Telugu (primary), Hindi (secondary) |
| **Tech literacy** | Comfortable with apps, uses YouTube for farming tips |
| **Goals** | Adopt precision farming, access real-time market data |

### Radha's Journey: Soil Test Workflow

```
Day 1: Visits soil testing lab, gets report
Day 2: Opens Krishi Sampark → 🧪 मिट्टी जांच
       → Selects "रिपोर्ट अपलोड करें" (Upload Report)
       → Uploads PDF soil test report
       → System extracts: pH 7.2, N: 280, P: 22, K: 140
       → Summary: "🟢 pH संतुलित, 🟡 पोटाश कम है"
       → Clicks "खाद सलाह देखें"
       → Krishi Sastri recommends potash application rate for cotton
       → Safety kernel verifies dosage is within limits
       → Activity logged to farm twin
```

## Tertiary Persona: Kamau — The Cooperative Manager

| Attribute | Detail |
|-----------|--------|
| **Name** | Kamau Mwangi |
| **Age** | 52 |
| **Location** | Nakuru County, Kenya |
| **Role** | Manages a 50-farmer cooperative |
| **Crops** | Maize, beans, potatoes |
| **Phone** | Android, 3GB RAM, 3G |
| **Languages** | Swahili (primary), English (secondary) |
| **Goals** | Get aggregate weather alerts, market prices for bulk selling |

## User Journey: Expert Escalation

When the Krishi Sastri (local advisor) encounters a low-confidence diagnosis or complex issue:

```
Farmer asks: "मेरे भुट्टे की पत्तियाँ पीली हो रही हैं"
     │
     ▼
Krishi Sastri (local): "मुझे इसकी पक्की जानकारी नहीं है।
     यह कई कारणों से हो सकता है।"
     │
     ▼
Shows escalation prompt: "कृषि विशेषज्ञ से सलाह लें?"
     │
     ├── Farmer clicks "हाँ" →
     │     Expert form opens (crop, symptom, photo, urgency)
     │     → Routes to full cloud multi-agent system
     │     → Weather + Crop + Pest agents collaborate
     │     → Detailed diagnosis + treatment plan
     │     → Safety kernel verifies all chemical recommendations
     │
     └── Farmer clicks "नहीं" →
           Rule-based offline advice from OKF cache
```

## User Journey: Offline Advisory

```
Farmer's phone has NO connectivity
     │
     ▼
Opens Krishi Sampark → loads from IndexedDB cache
     │
     ▼
Taps "पूछें" → Selects "कृषि शास्त्री" (local advisor)
     │
     ▼
Asks: "गेहूँ के लिए कितना पानी चाहिए?"
     │
     ▼
OKF knowledge cache (IndexedDB) returns:
"Gehu ke liye pratham 30 din mein 2-3 baar sinchai karein."
     │
     ▼
Response displayed in Hindi, TTS reads it aloud
     │
     ▼
Activity queued in IndexedDB sync queue
     │
     ▼
When connectivity returns → sync to SQLite farm twin
```

## Related Documents

- [Product Vision](product-vision.md)
- [Functional Requirements](functional-requirements.md)
- [Farmer UX Guidelines](../03-design/farmer-ux-guidelines.md)