# Public MSC-v007.5

## SeaTrace Supply Evidence Chain Demonstration

A live traceability workflow showing how origin, receiving, routing, and delivery states can be verified without exposing private operational records.
Primary CTA: View Workflow
Secondary CTA: Review Public Proof
Proof chips:
- Origin Verified
- Receiving Recorded
- Route Matched
- Delivery Confirmed

> ⚠️ **SCENARIO-SAFE DEMO ONLY** — No real purchase order, no live partnership authorization, no actual customer records disclosed.

---

## Overview

MSC-v007 is a standalone public demonstration of the SeaTrace four-pillar proof flow:

| Pillar | Stage | Public View | Private Withheld |
|--------|-------|-------------|------------------|
| **SeaSide** | HOLD | Origin region, vessel class | Exact GPS, vessel identity |
| **DeckSide** | RECORD | #CATCH estimate, species | Raw yield %, crew notes |
| **DockSide** | STORE | #HARVEST actual, conversion measured | Invoice lines, margin |
| **MarketSide** | EXCHANGE | QR proof status, route summary | Price, settlement, PO terms |

---

## Quick Start

### Local Development

```bash
cd seatrace-msc-v007
python -m http.server 8080
```

Then open: http://localhost:8080

### Deploy to Netlify

```bash
# After git init and push
netlify deploy --prod --dir "."
```

---

## File Structure

```
seatrace-msc-v007/
├── index.html                 # Main demo page (complete, no placeholders)
├── netlify.toml               # Deploy config
├── README.md                  # This file
└── assets/
    ├── css/
    │   └── msc-v007-demo.css  # Complete styles (no missing files)
    ├── js/
    │   └── msc-v007-demo.js   # Demo logic & scenario data
    └── data/
        └── publix-sockeye.json # Public fixture data
```

## Engineering Harness

This repo also includes a separate SeaTrace 4P3L engineering harness under
`src/seatrace_4p3l/`. The harness is not the campaign repo; it uses campaign
spec docs as read-only contract references and provides schemas, fixtures,
deterministic flows, offline-safe agent contract wrappers, safety gates, tests,
and `just` recipes.

```bash
just install
just verify
```

See `docs/4P3L_ENGINEERING_HARNESS.md`.

---

## Features

### 1. Sidebar Navigation
- 7-section smooth scroll navigation
- Active section highlighting
- Mobile-responsive (converts to horizontal on small screens)

### 2. 9-Button Taskbar
- Step-by-step proof flow
- Manual or Auto-Run modes
- Visual progress indicator
- Keyboard navigation (← → arrows)

### 3. Dual Board Display
- **Public Proof Board**: #CATCH rail fields
- **Private Blocked Board**: $CHECK rail categories (values withheld)
- Real-time field updates per step

### 4. Four Pillar Cards
- SeaSide HOLD
- DeckSide RECORD  
- DockSide STORE
- MarketSide EXCHANGE

### 5. QR Reverse Trace
- Forward trace: Origin → Counter
- Reverse trace: Consumer scan → Origin
- Animated step visualization

### 6. Public/Private Split Ribbon
- Visual separation of #CATCH vs $CHECK rails
- Clear category labeling

---

## Design System

### Colors (SeaTrace Palette)
- `--black: #01122E` — Deep background
- `--panel: #005696` — UI panels
- `--teal: #00E5FF` — Primary accent
- `--amber: #FFB800` — Secondary/ready state
- `--red: #FF6B6B` — Private/withheld

### Typography
- **Display**: Orbitron (headings, tech feel)
- **Body**: Share Tech Mono (data, proof fields)

### Effects
- CRT scanlines overlay
- Animated scanbar
- Glow effects on active elements

---

## Scenario Data

The demo uses synthetic scenario data:

- **Demo Lot**: `DEMO-PP-PUBLIX-SOCKEYE-001`
- **Species**: Alaska Sockeye Salmon
- **Format**: 10 lb Boxed Fillets
- **Scenario Ref**: `SCN-LOT-2026-PUB-01`

All fields use "scenario-safe" labels:
- ❌ Never: exact weights, prices, margins, GPS
- ✅ Always: bands, ranges, measured labels

---

## Governance

### MSC Blue-Label Status
**WITHHELD** — No MSC certification claim appears in this demo.

### Regulatory Alignment
- **SIMP**: "Supports SIMP-aligned record organization" (not certification)
- **FSMA 204**: "Designed to help prepare records" (not verification)

### Licensing
- **#CATCH (Public)**: Unlimited — displayed on this page
- **$CHECK (Private)**: Limited — categories shown, values withheld

---

## Keyboard Controls

| Key | Action |
|-----|--------|
| `←` / `↑` | Previous step |
| `→` / `↓` | Next step |
| `Space` | Toggle Auto-Run mode |
| `Escape` | Reset demo |

---

## Browser Support

- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers (responsive layout)

---

## No External Dependencies

- ✅ No backend required
- ✅ No API calls
- ✅ No tracking scripts
- ✅ No cookies
- ✅ All assets self-contained

---

## Credits

**Design patterns derived from:**
- `seatrace-campaign` — SeaTrace scanlines, color palette, globe animation
- Interface prototype — Sidebar navigation, card layout, trace visualization

**Owner**: Roberto Scott Echols (WSP001)  
**Built**: 2026-06-05  
**License**: CC BY-SA 4.0 — For the Commons Good

---

## Deployment Checklist

- [ ] No local paths in HTML (`C:\`, `My Drive`, etc.)
- [ ] `noindex` meta tag present
- [ ] MSC gate: WITHHELD
- [ ] No raw yield percentages
- [ ] No price or margin values
- [ ] No exact GPS coordinates
- [ ] Disclaimer visible
- [ ] All 9 taskbar buttons functional
- [ ] Dual boards update correctly
- [ ] Keyboard navigation works
- [ ] Mobile responsive

---

*For the Commons Good — WSP est. 1988*
