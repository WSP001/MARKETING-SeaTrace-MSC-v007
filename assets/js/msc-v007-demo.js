/**
 * SeaTrace MSC-v007 Demo Logic
 * Scenario-safe proof flow simulator
 * No backend - all client-side
 */

// ═══════════════════════════════════════════════════════════════
// Scenario Data
// ═══════════════════════════════════════════════════════════════

const scenarioData = {
  scenario: {
    id: "CID-H7-PUBLIX-4P3L",
    mode: "public_scenario",
    title: "Peter Pan × Publix Sockeye Demo",
    lotId: "DEMO-PP-PUBLIX-SOCKEYE-001",
    sku: "SOCKEYE-FILLET-10LB-BOX-DEMO",
    species: "Alaska Sockeye Salmon",
    format: "10 lb Boxed Fillets",
    scenarioRef: "SCN-LOT-2026-PUB-01"
  },
  
  steps: [
    {
      id: 0,
      label: "Root Source",
      pillar: "SeaSide",
      mode: "HOLD",
      publicFields: [
        { label: "Origin Region", value: "Pacific Northwest · AK" },
        { label: "Vessel Class", value: "Small Commercial Salmon" },
        { label: "Trip Window", value: "2026-06-10 to 2026-06-13" },
        { label: "Signal Type", value: "Scenario AIS/Permit" }
      ],
      privateFields: [
        "Vessel identity and MMSI",
        "Captain and crew names",
        "Exact GPS coordinates",
        "Precise location trail"
      ],
      description: "Origin context held. Vessel class visible. Exact identity withheld."
    },
    {
      id: 1,
      label: "Receiving Lot",
      pillar: "DeckSide",
      mode: "RECORD",
      publicFields: [
        { label: "Catch Estimate ID", value: "SCN-CATCH-PUB-01" },
        { label: "Species", value: "Sockeye Salmon" },
        { label: "Weight Band", value: "Scenario Estimate" },
        { label: "Grade Projection", value: "A/B Mix" }
      ],
      privateFields: [
        "Crew notes and exceptions",
        "Hold map detail",
        "Protected estimate sheet",
        "Exact weight (pre-reconciliation)"
      ],
      description: "#CATCH estimate recorded. Mutable draft status."
    },
    {
      id: 2,
      label: "Weight Band",
      pillar: "DeckSide",
      mode: "RECORD",
      publicFields: [
        { label: "Weight Band", value: "Scenario Range" },
        { label: "Status", value: "Draft Estimate" },
        { label: "Projected Cases", value: "Estimated Range" }
      ],
      privateFields: [
        "Exact deck weight",
        "Hold-by-hold breakdown",
        "Raw recovery percentage"
      ],
      description: "Pre-landing estimate. Subject to reconciliation at dock."
    },
    {
      id: 3,
      label: "Processing",
      pillar: "DockSide",
      mode: "STORE",
      publicFields: [
        { label: "Processing Stage", value: "Freshpack Fillet" },
        { label: "Custody Review", value: "Scenario: PASS" },
        { label: "Receiving Label", value: "Cold Chain Receipt" }
      ],
      privateFields: [
        "Processing plant details",
        "Production line records",
        "Quality control sheets"
      ],
      description: "Dockside processing. Conversion from round to fillet."
    },
    {
      id: 4,
      label: "Case Count",
      pillar: "DockSide",
      mode: "STORE",
      publicFields: [
        { label: "Finished Case Count", value: "Scenario Count" },
        { label: "Case Format", value: "10 lb IQF Boxes" },
        { label: "Conversion Label", value: "Measured" },
        { label: "Variance Label", value: "Within Range" }
      ],
      privateFields: [
        "Actual recovery percentage",
        "Raw to finished weight ratio",
        "Plant economics",
        "Labor and overhead costs"
      ],
      description: "#HARVEST actual confirmed. Conversion measured (not raw yield %)."
    },
    {
      id: 5,
      label: "PO Match State",
      pillar: "MarketSide",
      mode: "EXCHANGE",
      publicFields: [
        { label: "PO Reference", value: "SCN-PO-PUB-SOCKEYE-01" },
        { label: "PO Balance State", value: "Scenario Partial" },
        { label: "Match Status", value: "Pending" }
      ],
      privateFields: [
        "Actual PO number",
        "Contract terms",
        "Price per pound",
        "Volume commitments"
      ],
      description: "Purchase order reconciliation. Public state label only."
    },
    {
      id: 6,
      label: "Warehouse Route",
      pillar: "MarketSide",
      mode: "EXCHANGE",
      publicFields: [
        { label: "Warehouse Ref", value: "SCN-WH-PUB-ATL-01" },
        { label: "Route Summary", value: "AK → SE Distribution" },
        { label: "Custody Status", value: "In Transit" }
      ],
      privateFields: [
        "Exact warehouse location",
        "Carrier details",
        "Delivery schedules",
        "Temperature logs"
      ],
      description: "Distribution logistics. Route summary visible, specifics withheld."
    },
    {
      id: 7,
      label: "Store Program",
      pillar: "MarketSide",
      mode: "EXCHANGE",
      publicFields: [
        { label: "Buyer Program", value: "Publix Program Label" },
        { label: "Store Region", value: "Southeast" },
        { label: "Program Status", value: "Active" }
      ],
      privateFields: [
        "Store-level pricing",
        "Promotional calendar",
        "Inventory targets",
        "Margin requirements"
      ],
      description: "Retail program assignment. Public label, private terms withheld."
    },
    {
      id: 8,
      label: "QR Proof",
      pillar: "MarketSide",
      mode: "EXCHANGE",
      publicFields: [
        { label: "Proof ID", value: "SCN-PROOF-PUB-01" },
        { label: "QR Status", value: "READY" },
        { label: "Trace Depth", value: "Full Chain" },
        { label: "Public Access", value: "Enabled" }
      ],
      privateFields: [
        "Authentication tokens",
        "Database connection strings",
        "Private ledger keys",
        "Settlement records"
      ],
      description: "Consumer-facing QR proof. Reverse trace from counter to origin."
    }
  ]
};

// ═══════════════════════════════════════════════════════════════
// State Management
// ═══════════════════════════════════════════════════════════════

let currentMode = 'manual';
let currentStep = -1;
let isRunning = false;
let autoRunInterval = null;

// ═══════════════════════════════════════════════════════════════
// DOM References (lazy loaded)
// ═══════════════════════════════════════════════════════════════

function getElements() {
  return {
    progressFill: document.getElementById('progress-fill'),
    progressLabel: document.getElementById('progress-label'),
    publicFields: document.getElementById('public-fields'),
    privateFields: document.getElementById('private-fields'),
    taskBtns: document.querySelectorAll('.task-btn'),
    modeManual: document.getElementById('mode-manual'),
    modeAuto: document.getElementById('mode-auto'),
    navItems: document.querySelectorAll('.nav-item'),
    traceSteps: document.querySelectorAll('.trace-step')
  };
}

// ═══════════════════════════════════════════════════════════════
// Mode Toggle
// ═══════════════════════════════════════════════════════════════

function setMode(mode) {
  currentMode = mode;
  const { modeManual, modeAuto } = getElements();
  
  if (mode === 'manual') {
    modeManual.classList.add('active');
    modeAuto.classList.remove('active');
    stopAutoRun();
  } else {
    modeAuto.classList.add('active');
    modeManual.classList.remove('active');
    startAutoRun();
  }
  
  updateProgressLabel();
}

function startAutoRun() {
  if (autoRunInterval) clearInterval(autoRunInterval);
  isRunning = true;
  
  let step = currentStep < 0 ? 0 : currentStep;
  
  autoRunInterval = setInterval(() => {
    if (step >= scenarioData.steps.length) {
      step = 0; // Loop back to start
    }
    runStep(step);
    step++;
  }, 2000);
}

function stopAutoRun() {
  if (autoRunInterval) {
    clearInterval(autoRunInterval);
    autoRunInterval = null;
  }
  isRunning = false;
}

// ═══════════════════════════════════════════════════════════════
// Step Execution
// ═══════════════════════════════════════════════════════════════

function runStep(stepIndex) {
  if (stepIndex < 0 || stepIndex >= scenarioData.steps.length) return;
  
  currentStep = stepIndex;
  const step = scenarioData.steps[stepIndex];
  
  // Update progress
  updateProgress(stepIndex);
  
  // Update boards
  renderPublicFields(step);
  renderPrivateFields(step);
  
  // Update taskbar buttons
  updateTaskbar(stepIndex);
  
  // Update sidebar nav
  updateSidebarNav(stepIndex);
  
  // Update trace visualization
  updateTraceSteps(stepIndex);
  
  // Scroll to boards if needed
  if (window.innerWidth < 900) {
    document.getElementById('boards-container')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

function updateProgress(stepIndex) {
  const { progressFill, progressLabel } = getElements();
  const percentage = ((stepIndex + 1) / scenarioData.steps.length) * 100;
  
  if (progressFill) {
    progressFill.style.width = `${percentage}%`;
  }
  
  updateProgressLabel();
}

function updateProgressLabel() {
  const { progressLabel } = getElements();
  if (!progressLabel) return;
  
  if (currentStep < 0) {
    progressLabel.textContent = 'Select a step above to begin — or choose Auto-Run';
  } else {
    const step = scenarioData.steps[currentStep];
    progressLabel.textContent = `Step ${currentStep + 1} of ${scenarioData.steps.length}: ${step.label} — ${step.description}`;
  }
}

// ═══════════════════════════════════════════════════════════════
// Board Rendering
// ═══════════════════════════════════════════════════════════════

function renderPublicFields(step) {
  const { publicFields } = getElements();
  if (!publicFields) return;
  
  let html = '<div class="field-group">';
  
  step.publicFields.forEach((field, index) => {
    html += `
      <div class="field slide-in" style="animation-delay:${index * 0.1}s">
        <span class="field-label">${field.label}</span>
        <span class="field-value ${field.value === 'READY' ? 'ready' : ''}">${field.value}</span>
      </div>
    `;
  });
  
  html += '</div>';
  
  // Add pillar reference
  html += `
    <div style="margin-top:16px;padding-top:16px;border-top:1px solid rgba(0,229,255,0.1)">
      <div style="font-size:9px;color:var(--muted);letter-spacing:0.05em;text-transform:uppercase;margin-bottom:4px">Pillar</div>
      <div style="font-size:11px;color:var(--teal)">${step.pillar} — ${step.mode}</div>
    </div>
  `;
  
  publicFields.innerHTML = html;
}

function renderPrivateFields(step) {
  const { privateFields } = getElements();
  if (!privateFields) return;
  
  let html = '<div class="field-group">';
  
  step.privateFields.forEach((field, index) => {
    html += `
      <div class="blocked-item slide-in" style="animation-delay:${index * 0.1}s">
        ${field}
      </div>
    `;
  });
  
  html += '</div>';
  
  // Add withheld notice
  html += `
    <div style="margin-top:16px;padding:12px;background:rgba(255,107,107,0.1);border-radius:4px;border:1px solid rgba(255,107,107,0.2)">
      <div style="font-size:9px;color:var(--red);letter-spacing:0.05em;text-transform:uppercase;margin-bottom:4px">Private $CHECK Rail</div>
      <div style="font-size:10px;color:var(--muted)">These fields remain in the private ledger. Public demo shows category only.</div>
    </div>
  `;
  
  privateFields.innerHTML = html;
}

// ═══════════════════════════════════════════════════════════════
// UI Updates
// ═══════════════════════════════════════════════════════════════

function updateTaskbar(activeIndex) {
  const { taskBtns } = getElements();
  
  taskBtns.forEach((btn, index) => {
    btn.classList.remove('active', 'completed');
    
    if (index === activeIndex) {
      btn.classList.add('active');
    } else if (index < activeIndex) {
      btn.classList.add('completed');
    }
  });
}

function updateSidebarNav(activeIndex) {
  const { navItems } = getElements();
  
  navItems.forEach((item) => {
    const itemStep = parseInt(item.dataset.step);
    item.classList.remove('active');
    
    // Map step ranges to nav items
    if (activeIndex >= 0 && activeIndex <= 1 && itemStep === 0) {
      item.classList.add('active');
    } else if (activeIndex >= 2 && activeIndex <= 3 && itemStep === 1) {
      item.classList.add('active');
    } else if (activeIndex >= 4 && activeIndex <= 5 && itemStep === 2) {
      item.classList.add('active');
    } else if (activeIndex >= 6 && activeIndex <= 8 && itemStep === 3) {
      item.classList.add('active');
    } else if (activeIndex === 8 && itemStep === 8) {
      item.classList.add('active');
    }
  });
}

function updateTraceSteps(activeIndex) {
  const { traceSteps } = getElements();
  
  traceSteps.forEach((step) => {
    const stepNum = parseInt(step.dataset.step);
    step.classList.remove('active');
    
    if (!isNaN(stepNum) && stepNum <= activeIndex) {
      step.classList.add('active');
    }
  });
}

// ═══════════════════════════════════════════════════════════════
// Full Scenario Runner
// ═══════════════════════════════════════════════════════════════

function runFullScenario() {
  stopAutoRun();
  resetDemo();
  
  let step = 0;
  const runNext = () => {
    if (step >= scenarioData.steps.length) {
      // Done - highlight all
      updateTaskbar(scenarioData.steps.length - 1);
      return;
    }
    
    runStep(step);
    step++;
    setTimeout(runNext, 1200);
  };
  
  runNext();
}

// ═══════════════════════════════════════════════════════════════
// Reset
// ═══════════════════════════════════════════════════════════════

function resetDemo() {
  stopAutoRun();
  currentStep = -1;
  
  const { progressFill, progressLabel, publicFields, privateFields, taskBtns, navItems, traceSteps } = getElements();
  
  if (progressFill) progressFill.style.width = '0%';
  if (progressLabel) progressLabel.textContent = 'Select a step above to begin — or choose Auto-Run';
  
  if (publicFields) {
    publicFields.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">📋</div>
        <p>Select a step above to see public proof fields.</p>
      </div>
    `;
  }
  
  if (privateFields) {
    privateFields.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔒</div>
        <p>Blocked fields will appear here.</p>
      </div>
    `;
  }
  
  taskBtns.forEach(btn => btn.classList.remove('active', 'completed'));
  navItems.forEach(item => item.classList.remove('active'));
  navItems[0]?.classList.add('active'); // Set to overview
  
  traceSteps.forEach(step => step.classList.remove('active'));
}

// ═══════════════════════════════════════════════════════════════
// Sidebar Navigation Smooth Scroll
// ═══════════════════════════════════════════════════════════════

function initSidebarNav() {
  const navItems = document.querySelectorAll('.nav-item');
  
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const href = item.getAttribute('href');
      const target = document.querySelector(href);
      
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
      
      // Handle step navigation
      const step = parseInt(item.dataset.step);
      if (!isNaN(step) && step >= 0) {
        runStep(step);
      }
    });
  });
}

// ═══════════════════════════════════════════════════════════════
// Keyboard Navigation
// ═══════════════════════════════════════════════════════════════

function initKeyboardNav() {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault();
      if (currentStep < scenarioData.steps.length - 1) {
        runStep(currentStep + 1);
      }
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      if (currentStep > 0) {
        runStep(currentStep - 1);
      }
    } else if (e.key === ' ') {
      e.preventDefault();
      if (currentMode === 'manual') {
        setMode('auto');
      } else {
        setMode('manual');
      }
    } else if (e.key === 'Escape') {
      resetDemo();
    }
  });
}

// ═══════════════════════════════════════════════════════════════
// Intersection Observer for Scroll Spy
// ═══════════════════════════════════════════════════════════════

function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  const navItems = document.querySelectorAll('.nav-item');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navItems.forEach(item => {
          item.classList.remove('active');
          if (item.getAttribute('href') === `#${id}`) {
            item.classList.add('active');
          }
        });
      }
    });
  }, { threshold: 0.3 });
  
  sections.forEach(section => observer.observe(section));
}

// ═══════════════════════════════════════════════════════════════
// Initialize
// ═══════════════════════════════════════════════════════════════

function init() {
  initSidebarNav();
  initKeyboardNav();
  initScrollSpy();
  
  console.log('🌊 SeaTrace MSC-v007 Demo initialized');
  console.log('📋 Scenario:', scenarioData.scenario.title);
  console.log('⌨️ Keyboard: ← → arrows for steps, SPACE for mode toggle, ESC to reset');
}

// Run initialization when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
