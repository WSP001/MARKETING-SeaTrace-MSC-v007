/**
 * WAFC-GGSE REELS — waterline-demo
 * Scenario-safe seafood traceability reel simulator.
 * No backend. All client-side. Synthetic data only.
 *
 * One shared ledger, four nodes on a packet_id spine (SCN-TRIP-0007).
 * Parties: SYN-CO-WAFC (originating), SYN-CO-GGSE (receiving).
 * Public bands disclose net weights; the private rail stays WITHHELD.
 * Incoming emulation runs forward; outgoing simulation runs in reverse;
 * "Play Both" runs them in parallel (forward + asynchronous reverse).
 */

// ── Scenario ledger ──────────────────────────────────────────────
const LEDGER = {
  reelId: 'SCN-TRIP-0007',
  zone: 'Synthetic Zone A · MOCK-COORD',
  originating: 'SYN-CO-WAFC',
  receiving: 'SYN-CO-GGSE',
  summary: {
    received: '2,485 lb',
    delivered: '2,460 lb',
    reconciliation: '-1.0% (within range)',
    packetMatch: 'SCN-TRIP-0007 · MATCHED'
  },
  nodes: [
    {
      seq: 0, pillar: 'SeaSide', tag: '#CATCH', mode: 'HOLD',
      party: 'SYN-CO-WAFC', packetId: 'SCN-PKT-0007-01',
      measureLabel: 'Catch estimate band', measure: '2,400–2,600 lb (est.)',
      publicFields: [
        { label: 'Region', value: 'Synthetic Zone A' },
        { label: 'Gear Category', value: 'Set Gillnet (category)' },
        { label: 'Trip Window', value: 'Scenario Range' },
        { label: 'Disclosure', value: 'Delayed / verified' }
      ],
      privateFields: [
        'Vessel identity (SYN-CO-WAFC unit)',
        'Precise coordinates (MOCK-COORD)',
        'Captain / crew names',
        'Continuous position trail'
      ]
    },
    {
      seq: 1, pillar: 'DeckSide', tag: '#HARVEST', mode: 'RECORD',
      party: 'SYN-CO-WAFC', packetId: 'SCN-PKT-0007-02',
      measureLabel: 'Net landed weight', measure: '2,540 lb',
      publicFields: [
        { label: 'Species', value: 'Sockeye Salmon' },
        { label: 'Landed (net)', value: '2,540 lb' },
        { label: 'Grade Projection', value: 'A / B mix' },
        { label: 'Review Marker', value: 'Set' }
      ],
      privateFields: [
        'Exact deck weight sheet',
        'Hold-by-hold map',
        'Crew exception notes',
        'Raw estimate detail'
      ]
    },
    {
      seq: 2, pillar: 'DockSide', tag: '#RECEIVE', mode: 'STORE',
      party: 'SYN-CO-GGSE', packetId: 'SCN-PKT-0007-03',
      measureLabel: 'Net received weight', measure: '2,485 lb',
      publicFields: [
        { label: 'Net Received', value: '2,485 lb' },
        { label: 'Variance', value: '-2.2% (within range)' },
        { label: 'Case Count', value: '249 x 10 lb' },
        { label: 'Conversion', value: 'Measured' }
      ],
      privateFields: [
        'Scale-ticket detail',
        'Recovery % formula',
        'Job cost / COGS',
        'Plant economics'
      ]
    },
    {
      seq: 3, pillar: 'MarketSide', tag: '#EXCHANGE', mode: 'EXCHANGE',
      party: 'SYN-CO-GGSE', packetId: 'SCN-PKT-0007-04',
      measureLabel: 'Net delivered weight', measure: '2,460 lb',
      publicFields: [
        { label: 'Net Delivered', value: '2,460 lb' },
        { label: 'PO Match State', value: 'Partial (state)' },
        { label: 'Delivery Window', value: 'Scenario Range' },
        { label: 'QR Proof', value: 'READY' }
      ],
      privateFields: [
        'Price / lb',
        'Margin',
        'Invoice lines',
        'Settlement ledger'
      ]
    }
  ]
};

const INCOMING = [0, 1, 2];        // SeaSide -> DeckSide -> DockSide
const OUTGOING = [3, 2, 1, 0];     // MarketSide -> ... -> SeaSide (reverse)
const IDLE_MS = 90000;             // 90-second idle timeout
const FRAME_MS = 950;              // reel frame cadence

// ── State ────────────────────────────────────────────────────────
const state = {
  kickedOff: false,
  gated: false,
  incomingDone: [],
  outgoingUnlocked: false,
  deliveryPtr: 3,
  deliveryVisited: [],
  playingIn: false,
  playingOut: false
};

let idleTimer = null;
const $ = (id) => document.getElementById(id);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ── Idle gate (90s) ──────────────────────────────────────────────
function armIdle() {
  clearTimeout(idleTimer);
  if (!state.kickedOff || state.gated) return;
  idleTimer = setTimeout(gateSession, IDLE_MS);
}
function gateSession() {
  state.gated = true;
  $('idle-gate').hidden = false;
}
function resumeSession() {
  state.gated = false;
  $('idle-gate').hidden = true;
  armIdle();
}
function touch() {
  if (state.gated) return;
  armIdle();
}

// ── Click2Kickoff ────────────────────────────────────────────────
function kickoff() {
  state.kickedOff = !state.kickedOff;
  const btn = $('kickoff-btn');
  if (state.kickedOff) {
    btn.classList.add('live');
    $('kickoff-label').textContent = 'Reel LIVE — click to gate';
    $('kickoff-note').textContent = 'Ledger armed. Play the incoming reel, then the outgoing trace — or run both.';
    $('incoming').setAttribute('aria-disabled', 'false');
    setBanner('Ledger armed — awaiting first atomic write.', 'armed');
    $('in-status').textContent = 'Ready — play or step the incoming emulation.';
    armIdle();
  } else {
    btn.classList.remove('live');
    $('kickoff-label').textContent = 'Click2Kickoff';
    $('kickoff-note').textContent = 'Idle until you start it. Nothing runs until you say go.';
    clearTimeout(idleTimer);
    fullReset();
  }
}

// ── Stage spine ──────────────────────────────────────────────────
function buildSpine() {
  const spine = $('stage-spine');
  spine.innerHTML = '';
  LEDGER.nodes.forEach((node, i) => {
    const el = document.createElement('div');
    el.className = 'spine-node';
    el.dataset.seq = String(node.seq);
    el.innerHTML =
      `<span class="sp-num">0${i + 1}</span>` +
      `<span class="sp-pillar">${node.pillar}</span>` +
      `<span class="sp-tag">${node.tag}</span>`;
    spine.appendChild(el);
    if (i < LEDGER.nodes.length - 1) {
      const a = document.createElement('div');
      a.className = 'spine-arrow';
      a.textContent = '→';
      spine.appendChild(a);
    }
  });
}
function pulseSpine(seq) {
  document.querySelectorAll('#stage-spine .spine-node').forEach((el) => {
    const active = Number(el.dataset.seq) === seq;
    el.classList.toggle('active', active);
    if (active) {
      el.classList.remove('pulse');
      void el.offsetWidth;
      el.classList.add('pulse');
    }
  });
}

// ── Filmstrips ───────────────────────────────────────────────────
function buildStrip(elId, order) {
  const strip = $(elId);
  strip.innerHTML = '';
  order.forEach((seq) => {
    const node = LEDGER.nodes[seq];
    const frame = document.createElement('div');
    frame.className = 'frame';
    frame.dataset.seq = String(seq);
    frame.innerHTML =
      `<div class="frame-sprockets"></div>` +
      `<div class="frame-body">` +
        `<div class="frame-pillar">${node.pillar}</div>` +
        `<div class="frame-tag">${node.tag}</div>` +
        `<div class="frame-measure">${node.measureLabel}</div>` +
        `<div class="frame-value">${node.measure}</div>` +
        `<div class="frame-packet">${node.packetId}</div>` +
      `</div>` +
      `<div class="frame-sprockets"></div>`;
    strip.appendChild(frame);
  });
}
function activateFrame(elId, seq) {
  document.querySelectorAll(`#${elId} .frame`).forEach((f) => {
    const on = Number(f.dataset.seq) === seq;
    f.classList.toggle('rolling', on);
    if (on) f.classList.add('played');
  });
}

// ── Atomic commit ────────────────────────────────────────────────
function commit(seq, banner) {
  const node = LEDGER.nodes[seq];
  renderBoards(node);
  flashCommit(banner || `Atomic write · ${node.pillar} ${node.tag} · ${node.packetId}`);
  pulseSpine(seq);
}
function renderBoards(node) {
  let ph = '<div class="field-group">';
  node.publicFields.forEach((f, i) => {
    const ready = f.value === 'READY' ? ' ready' : '';
    ph += `<div class="field slide-in" style="animation-delay:${i * 0.05}s"><span class="field-label">${f.label}</span><span class="field-value${ready}">${f.value}</span></div>`;
  });
  ph += '</div>';
  ph += `<div class="board-foot"><span class="foot-key">Pillar</span><span class="foot-val">${node.pillar} — ${node.mode} · ${node.party}</span></div>`;
  $('public-fields').innerHTML = ph;

  let vh = '<div class="field-group">';
  node.privateFields.forEach((f, i) => {
    vh += `<div class="blocked-item slide-in" style="animation-delay:${i * 0.05}s">${f}<span class="withheld-tag">WITHHELD</span></div>`;
  });
  vh += '</div>';
  vh += `<div class="board-foot withheld"><span class="foot-key">$CHECK rail</span><span class="foot-val">Category only — values never disclosed.</span></div>`;
  $('private-fields').innerHTML = vh;
}
function flashCommit(text) {
  setBanner(text, 'commit');
  ['public-board', 'private-board'].forEach((id) => {
    const el = $(id);
    el.classList.remove('commit-flash');
    void el.offsetWidth;
    el.classList.add('commit-flash');
  });
}
function setBanner(text, cls) {
  $('commit-banner').className = 'commit-banner' + (cls ? ' ' + cls : '');
  $('commit-banner-text').textContent = text;
}

// ── Incoming receiving reel ──────────────────────────────────────
function runIncomingStep(seq) {
  if (!state.incomingDone.includes(seq)) state.incomingDone.push(seq);
  activateFrame('incoming-strip', seq);
  commit(seq);
  addWaitCard(LEDGER.nodes[seq]);
  const pct = (state.incomingDone.length / INCOMING.length) * 100;
  $('in-progress').style.width = pct + '%';
  if (state.incomingDone.length < INCOMING.length) {
    $('in-status').textContent = `${state.incomingDone.length} of ${INCOMING.length} receiving writes committed.`;
  } else {
    $('in-status').textContent = 'Receiving reel complete — net received weight disclosed. Outgoing reel unlocked.';
    unlockOutgoing();
    $('pub-received').textContent = LEDGER.summary.received;
    $('prv-received').textContent = 'WITHHELD';
  }
}
function incomingStep() {
  if (!guard()) return;
  const next = INCOMING.find((s) => !state.incomingDone.includes(s));
  if (next === undefined) return;
  runIncomingStep(next);
  touch();
}
async function playIncoming() {
  if (!guard() || state.playingIn) return;
  state.playingIn = true;
  $('in-play').disabled = true;
  for (const seq of INCOMING) {
    if (state.gated) break;
    if (!state.incomingDone.includes(seq)) {
      runIncomingStep(seq);
      touch();
      await sleep(FRAME_MS);
    }
  }
  state.playingIn = false;
  $('in-play').disabled = false;
}
function addWaitCard(node) {
  const wrap = $('wait-cards');
  const empty = wrap.querySelector('.empty-state');
  if (empty) empty.remove();
  if (wrap.querySelector(`[data-seq="${node.seq}"]`)) return;
  const card = document.createElement('div');
  card.className = 'wait-card slide-in';
  card.dataset.seq = String(node.seq);
  card.innerHTML =
    `<div class="wc-head"><span class="wc-pillar">${node.pillar}</span><span class="wc-tag">${node.tag}</span></div>` +
    `<div class="wc-measure"><span class="wc-measure-label">${node.measureLabel}</span><span class="wc-measure-value">${node.measure}</span></div>` +
    `<div class="wc-foot"><span class="wc-packet">${node.packetId}</span><span class="wc-status">COMMIT ✓</span></div>`;
  wrap.appendChild(card);
}

// ── Outgoing delivery reel ───────────────────────────────────────
function unlockOutgoing() {
  if (state.outgoingUnlocked) return;
  state.outgoingUnlocked = true;
  const sec = $('outgoing');
  sec.classList.remove('locked');
  sec.setAttribute('aria-disabled', 'false');
  $('out-lock').textContent = '🔓 Unlocked';
  ['out-play', 'out-fwd', 'out-back', 'out-reset'].forEach((id) => ($(id).disabled = false));
}
function renderDeliveryPtr() {
  document.querySelectorAll('#outgoing-strip .frame').forEach((f) => {
    const seq = Number(f.dataset.seq);
    f.classList.toggle('rolling', state.deliveryVisited.length > 0 && seq === state.deliveryPtr);
    if (state.deliveryVisited.includes(seq)) f.classList.add('played');
  });
}
function visitDelivery(seq) {
  state.deliveryPtr = seq;
  if (!state.deliveryVisited.includes(seq)) state.deliveryVisited.push(seq);
  renderDeliveryPtr();
  pulseSpine(seq);
  renderMatch();
  if (seq === 3) {
    $('pub-delivered').textContent = LEDGER.summary.delivered;
    $('prv-delivered').textContent = 'WITHHELD';
  }
  if (seq === 0) {
    // reverse trace reached originating record → reconciliation + match resolve
    $('pub-recon').textContent = LEDGER.summary.reconciliation;
    $('prv-recon').textContent = 'WITHHELD';
    $('pub-match').textContent = LEDGER.summary.packetMatch;
    $('prv-match').textContent = 'WITHHELD';
  }
}
function stepDelivery(dir) {
  if (!guardOutgoing()) return;
  if (state.deliveryVisited.length === 0) {
    visitDelivery(3); // first touch shows the counter node
  } else {
    const nextSeq = Math.max(0, Math.min(3, state.deliveryPtr + dir));
    visitDelivery(nextSeq);
  }
  touch();
}
async function playOutgoing() {
  if (!guardOutgoing() || state.playingOut) return;
  state.playingOut = true;
  $('out-play').disabled = true;
  for (const seq of OUTGOING) {
    if (state.gated) break;
    visitDelivery(seq);
    touch();
    await sleep(FRAME_MS);
  }
  state.playingOut = false;
  if (state.outgoingUnlocked) $('out-play').disabled = false;
}
function renderMatch() {
  const cur = LEDGER.nodes[state.deliveryPtr];
  const origin = LEDGER.nodes[0];
  const atOrigin = state.deliveryPtr === 0;
  $('match-body').innerHTML =
    `<div class="match-row"><span class="mr-key">Current node</span><span class="mr-val">${cur.pillar} ${cur.tag}</span></div>` +
    `<div class="match-row"><span class="mr-key">Current packet</span><span class="mr-val mono">${cur.packetId}</span></div>` +
    `<div class="match-row"><span class="mr-key">Measure</span><span class="mr-val">${cur.measureLabel}: ${cur.measure}</span></div>` +
    `<div class="match-link">${cur.packetId} ↔ ${origin.packetId} <span class="matched">MATCHED</span></div>` +
    `<div class="match-spine">Spine ${LEDGER.reelId} · ${LEDGER.nodes[3].party} → ${origin.party}</div>` +
    `<div class="match-note">${atOrigin ? 'Reverse trace reached the originating record — reconciliation resolved.' : 'Reconciling delivery back toward the originating record.'}</div>`;
}

// ── Parallel mode ────────────────────────────────────────────────
async function playBoth() {
  if (!guard()) return;
  resetReels();
  unlockOutgoing(); // parallel demonstrates both directions at once
  setBanner('Parallel run — forward emulation + asynchronous reverse trace.', 'commit');
  await Promise.all([playIncoming(), playOutgoing()]);
  $('in-status').textContent = 'Parallel run complete — both rails reconciled on the shared packet_id.';
}

// ── Public / private split table ─────────────────────────────────
function buildSplitTable() {
  const tbody = $('split-tbody');
  tbody.innerHTML = '';
  LEDGER.nodes.forEach((node) => {
    const pub = node.publicFields.map((f) => `${f.label}: ${f.value}`).join(' · ');
    const priv = node.privateFields.join(' · ');
    const tr = document.createElement('tr');
    tr.innerHTML =
      `<td><strong>${node.pillar}</strong><br><span class="td-tag">${node.tag}</span></td>` +
      `<td class="mono">${node.packetId}</td>` +
      `<td class="td-public">${pub}</td>` +
      `<td class="td-private">${priv} <span class="withheld-tag">WITHHELD</span></td>`;
    tbody.appendChild(tr);
  });
}

// ── Reset ────────────────────────────────────────────────────────
function resetReels() {
  state.incomingDone = [];
  state.deliveryPtr = 3;
  state.deliveryVisited = [];
  $('in-progress').style.width = '0%';
  $('in-status').textContent = state.kickedOff ? 'Ready — play or step the incoming emulation.' : 'Idle — run the incoming reel to begin the emulation.';
  $('wait-cards').innerHTML = '<div class="empty-state"><div class="empty-icon">📥</div><p>Received-weight cards queue here as each stage commits.</p></div>';
  $('public-fields').innerHTML = '<div class="empty-state"><div class="empty-icon">📋</div><p>Public proof fields appear here on each atomic commit.</p></div>';
  $('private-fields').innerHTML = '<div class="empty-state"><div class="empty-icon">🔒</div><p>Private categories appear here — value withheld, never disclosed.</p></div>';
  $('match-body').innerHTML = '<div class="empty-state"><div class="empty-icon">🔗</div><p>Step the delivery reel to match each node back to the originating record.</p></div>';
  ['pub-received', 'pub-delivered', 'pub-recon', 'pub-match', 'prv-received', 'prv-delivered', 'prv-recon', 'prv-match'].forEach((id) => ($(id).textContent = '—'));
  document.querySelectorAll('.frame').forEach((f) => f.classList.remove('rolling', 'played'));
  document.querySelectorAll('.spine-node').forEach((n) => n.classList.remove('active', 'pulse'));
}
function fullReset() {
  resetReels();
  state.outgoingUnlocked = false;
  const sec = $('outgoing');
  sec.classList.add('locked');
  sec.setAttribute('aria-disabled', 'true');
  $('incoming').setAttribute('aria-disabled', 'true');
  $('out-lock').textContent = '🔒 Locked — finish incoming';
  ['out-play', 'out-fwd', 'out-back', 'out-reset'].forEach((id) => ($(id).disabled = true));
  setBanner('Session gated — no writes.', '');
}

// ── Guards ───────────────────────────────────────────────────────
function guard() {
  if (!state.kickedOff) {
    setBanner('Press Click2Kickoff first — the reel is idle.', '');
    const b = $('kickoff-btn');
    b.classList.add('nudge');
    setTimeout(() => b.classList.remove('nudge'), 600);
    return false;
  }
  return !state.gated;
}
function guardOutgoing() {
  if (!guard()) return false;
  if (!state.outgoingUnlocked) {
    $('in-status').textContent = 'Finish the incoming emulation first — it unlocks the outgoing reel.';
    return false;
  }
  return true;
}

// ── Init ─────────────────────────────────────────────────────────
function init() {
  buildSpine();
  buildStrip('incoming-strip', INCOMING);
  buildStrip('outgoing-strip', OUTGOING);
  buildSplitTable();

  $('kickoff-btn').addEventListener('click', kickoff);
  $('resume-btn').addEventListener('click', resumeSession);
  $('in-play').addEventListener('click', playIncoming);
  $('in-step').addEventListener('click', incomingStep);
  $('in-reset').addEventListener('click', () => { if (guard()) { resetReels(); touch(); } });
  $('out-play').addEventListener('click', playOutgoing);
  $('out-fwd').addEventListener('click', () => stepDelivery(1));
  $('out-back').addEventListener('click', () => stepDelivery(-1));
  $('out-reset').addEventListener('click', () => {
    if (!guardOutgoing()) return;
    state.deliveryPtr = 3;
    state.deliveryVisited = [];
    renderDeliveryPtr();
    $('match-body').innerHTML = '<div class="empty-state"><div class="empty-icon">🔗</div><p>Step the delivery reel to match each node back to the originating record.</p></div>';
    touch();
  });
  $('play-both').addEventListener('click', playBoth);

  ['click', 'keydown', 'pointerdown'].forEach((evt) =>
    document.addEventListener(evt, touch, { passive: true })
  );

  console.log('🌊 waterline-demo · WAFC-GGSE REELS initialized · spine', LEDGER.reelId);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
