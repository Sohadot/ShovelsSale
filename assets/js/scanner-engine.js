(function () {
  'use strict';

  /* ── Runtime model — source of truth for validation: data/scanner-model.json ── */
  var MODEL = {
    signals: [
      {
        key: 'enablesMany',
        label: 'Enables many participants',
        description: 'Does this actor enable many participants across the market, regardless of who wins the visible competition?',
        leftLabel: 'Serves one participant',
        rightLabel: 'Enables many participants',
        defaultValue: 50
      },
      {
        key: 'chasesVisible',
        label: 'Chases visible demand directly',
        description: 'Does this actor primarily compete for visible, narratively attractive outcomes rather than serving the infrastructure beneath them?',
        leftLabel: 'Infrastructure position',
        rightLabel: 'Chases visible demand',
        defaultValue: 50
      },
      {
        key: 'controlsAccess',
        label: 'Controls access, standards, routing, or bottlenecks',
        description: 'Does this actor define who gets access, set the rules of the market, or control critical distribution rails or permissions?',
        leftLabel: 'No control power',
        rightLabel: 'Defines access and standards',
        defaultValue: 50
      },
      {
        key: 'nearCoreInfra',
        label: 'Sits near compute, money, identity, or distribution',
        description: 'How close is this actor to core infrastructure layers: compute, payments, identity, records, deployment, security, or distribution?',
        leftLabel: 'Application layer',
        rightLabel: 'Core infrastructure',
        defaultValue: 50
      },
      {
        key: 'failureDisrupts',
        label: 'Failure would disrupt many participants',
        description: 'If this actor failed or disappeared, would many participants in the market be operationally disrupted?',
        leftLabel: 'Easily absorbed',
        rightLabel: 'System-critical',
        defaultValue: 50
      },
      {
        key: 'hardToSwitch',
        label: 'Switching away is operationally difficult',
        description: 'How embedded is this actor in workflows, standards, or operations that make switching away genuinely costly?',
        leftLabel: 'Easy to leave',
        rightLabel: 'Deep operational lock-in',
        defaultValue: 50
      },
      {
        key: 'dependencyGrows',
        label: 'Dependency increases over time',
        description: "Does the market's reliance on this actor grow as adoption deepens, integrations accumulate, and switching costs rise?",
        leftLabel: 'Dependency shrinks',
        rightLabel: 'Dependency compounds',
        defaultValue: 50
      },
      {
        key: 'necessityNotSpec',
        label: 'Value tied to operational necessity, not speculation',
        description: 'Is demand driven by genuine operational need, or by speculative interest in a narrative outcome?',
        leftLabel: 'Speculation-driven',
        rightLabel: 'Necessity-driven',
        defaultValue: 50
      },
      {
        key: 'replaceable',
        label: 'Replaceable by many alternatives',
        description: 'Could this actor be replaced by many credible alternatives within a reasonable operational timeframe?',
        leftLabel: 'Hard to replace',
        rightLabel: 'Many alternatives exist',
        defaultValue: 50
      },
      {
        key: 'compoundsIntegrations',
        label: 'Compounds through integrations, workflows, standards, or trust',
        description: "Does this actor's value compound as more systems, workflows, records, and dependencies accumulate around it?",
        leftLabel: 'Static value',
        rightLabel: 'Compounds over time',
        defaultValue: 50
      }
    ],

    scoring: {
      miner: [
        { signal: 'chasesVisible',    weight: 0.30, invert: false },
        { signal: 'replaceable',      weight: 0.20, invert: false },
        { signal: 'enablesMany',      weight: 0.15, invert: true  },
        { signal: 'necessityNotSpec', weight: 0.15, invert: true  },
        { signal: 'failureDisrupts',  weight: 0.10, invert: true  },
        { signal: 'hardToSwitch',     weight: 0.10, invert: true  }
      ],
      shovel: [
        { signal: 'enablesMany',      weight: 0.25, invert: false },
        { signal: 'failureDisrupts',  weight: 0.20, invert: false },
        { signal: 'necessityNotSpec', weight: 0.20, invert: false },
        { signal: 'nearCoreInfra',    weight: 0.13, invert: false },
        { signal: 'hardToSwitch',     weight: 0.12, invert: false },
        { signal: 'dependencyGrows',  weight: 0.10, invert: false }
      ],
      gatekeeper: [
        { signal: 'controlsAccess',        weight: 0.35, invert: false },
        { signal: 'compoundsIntegrations', weight: 0.25, invert: false },
        { signal: 'hardToSwitch',          weight: 0.15, invert: false },
        { signal: 'failureDisrupts',       weight: 0.15, invert: false },
        { signal: 'nearCoreInfra',         weight: 0.10, invert: false }
      ]
    },

    derivedMetrics: {
      infrastructureDensity: {
        formula: 'avg',
        components: [
          { signal: 'enablesMany',     invert: false },
          { signal: 'nearCoreInfra',   invert: false },
          { signal: 'failureDisrupts', invert: false },
          { signal: 'dependencyGrows', invert: false }
        ]
      },
      controlLayerStrength: { formula: 'score',  source: 'gatekeeper' },
      dependencyBreadth: {
        formula: 'avg',
        components: [
          { signal: 'enablesMany',     invert: false },
          { signal: 'failureDisrupts', invert: false }
        ]
      },
      switchingCost:         { formula: 'signal', source: 'hardToSwitch', invert: false },
      replacementDifficulty: { formula: 'signal', source: 'replaceable',  invert: true  },
      speculationExposure: {
        formula: 'avg',
        components: [
          { signal: 'chasesVisible',    invert: false },
          { signal: 'necessityNotSpec', invert: true  }
        ]
      },
      durabilitySignal: {
        formula: 'avg',
        components: [
          { signal: 'hardToSwitch',          invert: false },
          { signal: 'dependencyGrows',       invert: false },
          { signal: 'compoundsIntegrations', invert: false }
        ]
      }
    },

    confidence: {
      lowScoreThreshold:    50,
      hybridSpreadThreshold: 8,
      highSpreadThreshold:  25,
      highMinScore:         65
    },

    layers: {
      'Miner':                 'Extraction Layer',
      'Shovel':                'Infrastructure Layer',
      'Gatekeeper':            'Control Layer',
      'Hybrid':                'Hybrid Layer',
      'Unclear / Early Signal':'Unclassified'
    },

    narratives: {
      classification: {
        'Miner':      '{name} shows strongest structural alignment with the Miner position in the {wave} market. It appears to compete primarily for visible market outcomes rather than enabling the infrastructure beneath the competition. Its value is more dependent on who wins the race than on whether the race continues at all.',
        'Shovel':     '{name} shows strongest structural alignment with the Shovel position in the {wave} market. It captures value by serving many participants, embedding into operations where its utility compounds regardless of which specific players win the visible competition. This is the classic infrastructure-over-extraction dynamic.',
        'Gatekeeper': '{name} shows strongest structural alignment with the Gatekeeper position in the {wave} market. Its dominant economic behavior is controlling access, defining standards, or shaping the permissions and rails through which others must move. Gatekeeper power tends to outlast individual market cycles.',
        'Hybrid':     '{name} shows meaningful signals across more than one structural position in the {wave} market. This is a Hybrid classification — not a failure of the model, but a structural observation. It should be studied as a tension between positions rather than resolved prematurely into one label.',
        'Unclear / Early Signal': '{name} does not yet provide enough consistent structural evidence for a confident classification in the {wave} market. Use this output as a research prompt rather than a conclusion. Revisit when more operational evidence is available.'
      },
      matters: {
        'Miner':      "Miner-classified actors are most exposed to the outcome of specific market races. If the dominant narrative shifts, or if the expected winner changes, extraction-layer exposure becomes fragile quickly. This does not mean the position is wrong — it means the bet is directional.",
        'Shovel':     "Shovel-classified actors capture value regardless of which specific players win the visible competition. This structural breadth makes them more durable across market cycles, though they remain vulnerable to commodity risk if the category matures and alternatives multiply.",
        'Gatekeeper': "Gatekeeper-classified actors derive structural power from defining access rules. This can be the most durable position — standards and permission systems often outlast the markets they govern — but it also attracts regulatory and competitive pressure that infrastructure players rarely face.",
        'Hybrid':     "Hybrid actors carry structural complexity. They may be transitioning between positions, or deliberately maintaining exposure across layers. Understanding which layer drives durable value and which introduces fragility is more useful than resolving the Hybrid label too quickly.",
        'Unclear / Early Signal': "Early-signal actors require continued observation. Premature classification can mislead analysis. The structural signals may clarify as the market matures, as the actor's behavior compounds, or as competitive alternatives emerge and the actor's position becomes legible."
      },
      limits: {
        'Miner':      "This classification reflects current structural signals, not competitive or financial outcomes. A Miner can be a successful business. Classification describes structural position, not performance or valuation. Signals are scored by the analyst and subject to interpretation bias.",
        'Shovel':     "Infrastructure breadth does not protect against commodity risk. If the category becomes commoditised, shovel-layer actors face pricing pressure regardless of structural position. Dependency breadth can erode as markets mature and credible alternatives multiply.",
        'Gatekeeper': "Control-layer strength can erode when regulatory action, open standards movements, or platform competition undermines the gating mechanism. This classification describes current observed behavior, not permanent structural advantage.",
        'Hybrid':     "Hybrid classifications are the least predictive. They indicate structural complexity rather than structural weakness or strength. Deeper case study — using the Dispatch archive as reference — is recommended before drawing strategic conclusions.",
        'Unclear / Early Signal': "Low-confidence classifications should not be used for strategic decisions without further primary research. They indicate insufficient structural evidence, not a negative outcome for the actor being assessed."
      }
    },

    presets: [
      {
        id: 'nvidia', name: 'NVIDIA', actorType: 'company', marketWave: 'AI',
        values: { enablesMany:92, chasesVisible:22, controlsAccess:74, nearCoreInfra:97, failureDisrupts:94, hardToSwitch:86, dependencyGrows:89, necessityNotSpec:84, replaceable:18, compoundsIntegrations:80 }
      },
      {
        id: 'stripe', name: 'Stripe', actorType: 'platform', marketWave: 'payments',
        values: { enablesMany:89, chasesVisible:18, controlsAccess:80, nearCoreInfra:84, failureDisrupts:93, hardToSwitch:82, dependencyGrows:87, necessityNotSpec:91, replaceable:28, compoundsIntegrations:84 }
      },
      {
        id: 'cloudflare', name: 'Cloudflare', actorType: 'infrastructure', marketWave: 'cloud',
        values: { enablesMany:86, chasesVisible:14, controlsAccess:93, nearCoreInfra:91, failureDisrupts:94, hardToSwitch:76, dependencyGrows:81, necessityNotSpec:89, replaceable:21, compoundsIntegrations:86 }
      },
      {
        id: 'vertical-ai-app', name: 'Vertical AI App', actorType: 'product', marketWave: 'AI',
        values: { enablesMany:22, chasesVisible:89, controlsAccess:11, nearCoreInfra:16, failureDisrupts:14, hardToSwitch:28, dependencyGrows:25, necessityNotSpec:20, replaceable:87, compoundsIntegrations:14 }
      },
      {
        id: 'google', name: 'Google', actorType: 'company', marketWave: 'developer infrastructure',
        values: { enablesMany:80, chasesVisible:42, controlsAccess:98, nearCoreInfra:90, failureDisrupts:92, hardToSwitch:86, dependencyGrows:78, necessityNotSpec:78, replaceable:22, compoundsIntegrations:92 }
      },
      {
        id: 'openai', name: 'OpenAI', actorType: 'company', marketWave: 'AI',
        values: { enablesMany:72, chasesVisible:92, controlsAccess:60, nearCoreInfra:50, failureDisrupts:65, hardToSwitch:48, dependencyGrows:55, necessityNotSpec:30, replaceable:74, compoundsIntegrations:52 }
      },
      {
        id: 'microsoft', name: 'Microsoft', actorType: 'company', marketWave: 'cloud',
        values: { enablesMany:88, chasesVisible:42, controlsAccess:60, nearCoreInfra:94, failureDisrupts:93, hardToSwitch:90, dependencyGrows:88, necessityNotSpec:88, replaceable:22, compoundsIntegrations:86 }
      }
    ],

    dispatchExamples: {
      'Shovel': [
        { id: '001', actor: 'NVIDIA',       wave: 'AI',                     note: 'Compute infrastructure enabling the entire AI gold rush regardless of which model wins' },
        { id: '002', actor: 'ASML',         wave: 'Semiconductors',         note: 'Sole supplier of EUV lithography — every chip manufacturer depends on one tool provider' },
        { id: '006', actor: 'Stripe',       wave: 'Payments',               note: 'Payment infrastructure embedded into thousands of builders regardless of commerce outcome' }
      ],
      'Gatekeeper': [
        { id: '004', actor: 'Oracle',       wave: 'Enterprise',             note: 'Database standards and enterprise lock-in define decades of structural control-layer power' },
        { id: '005', actor: 'Cloudflare',   wave: 'Internet Infrastructure', note: 'Security, access routing, and DNS at internet scale — a modern control-layer example' }
      ],
      'Miner': [
        { id: '003', actor: 'Domain Names', wave: 'Digital Assets',         note: 'Infrastructure assets that behave like extraction-layer bets when treated as speculation' }
      ],
      'Hybrid': [
        { id: '007', actor: 'Shopify',      wave: 'Commerce',               note: 'Serves merchant infrastructure while competing for consumer commerce at the extraction layer' },
        { id: '008', actor: 'GitHub',       wave: 'Developer Infrastructure', note: 'Developer infrastructure with growing platform control-layer behavior as adoption compounds' }
      ],
      'Unclear / Early Signal': [
        { id: '003', actor: 'Domain Names', wave: 'Digital Assets',         note: 'Early-stage classification discipline helps avoid premature extraction-layer bets' },
        { id: '007', actor: 'Shopify',      wave: 'Commerce',               note: 'Hybrid and unclear actors often share structural complexity worth studying in case examples' }
      ]
    },

    waveDispatchMap: {
      'AI':                       ['001'],
      'semiconductors':           ['002'],
      'payments':                 ['006'],
      'cloud':                    ['005', '008'],
      'commerce':                 ['007'],
      'developer infrastructure': ['008'],
      'digital assets':           ['003']
    }
  };

  /* ── DOM helpers ── */
  function $(id) { return document.getElementById(id); }
  function clamp(n, lo, hi) { return Math.max(lo, Math.min(hi, n)); }
  function sanitize(str, max) { return String(str || '').trim().slice(0, max); }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function div(cls) { return el('div', cls); }

  function applyTemplate(tmpl, name, wave) {
    return (tmpl || '').replace(/\{name\}/g, name).replace(/\{wave\}/g, wave);
  }

  /* ── Runtime safety: verify required DOM elements exist ── */
  function requireEl(id) {
    var e = $(id);
    if (!e) console.warn('[ShovelsSale Scanner] Missing required element: #' + id);
    return e;
  }

  /* ── Scoring engine ── */
  function computeRawScore(term, v) {
    var total = 0;
    MODEL.scoring[term].forEach(function (w) {
      total += (w.invert ? (100 - v[w.signal]) : v[w.signal]) * w.weight;
    });
    return clamp(total, 0, 100);
  }

  function computeDerived(name, v, rawScores) {
    var def = MODEL.derivedMetrics[name];
    if (!def) return 0;
    if (def.formula === 'avg') {
      var sum = 0;
      def.components.forEach(function (c) {
        sum += c.invert ? (100 - v[c.signal]) : v[c.signal];
      });
      return Math.round(sum / def.components.length);
    }
    if (def.formula === 'score') return Math.round(rawScores[def.source] || 0);
    if (def.formula === 'signal') {
      var val = v[def.source] || 0;
      return Math.round(def.invert ? (100 - val) : val);
    }
    return 0;
  }

  function scoreModel(v) {
    var minerRaw      = computeRawScore('miner', v);
    var shovelRaw     = computeRawScore('shovel', v);
    var gatekeeperRaw = computeRawScore('gatekeeper', v);
    var rawScores     = { miner: minerRaw, shovel: shovelRaw, gatekeeper: gatekeeperRaw };

    var candidates = [
      { key: 'Miner',      val: minerRaw },
      { key: 'Shovel',     val: shovelRaw },
      { key: 'Gatekeeper', val: gatekeeperRaw }
    ].sort(function (a, b) { return b.val - a.val; });

    var spread  = candidates[0].val - candidates[1].val;
    var primary = candidates[0].key;
    var confidence;
    var conf    = MODEL.confidence;

    if (candidates[0].val < conf.lowScoreThreshold) {
      primary = 'Unclear / Early Signal'; confidence = 'Low';
    } else if (spread <= conf.hybridSpreadThreshold) {
      primary = 'Hybrid'; confidence = 'Mixed';
    } else if (spread >= conf.highSpreadThreshold && candidates[0].val >= conf.highMinScore) {
      confidence = 'High';
    } else {
      confidence = 'Moderate';
    }

    var layers         = MODEL.layers;
    var primaryLayer   = layers[primary] || 'Unclassified';
    var secondaryLayer = (primary !== 'Unclear / Early Signal' && primary !== 'Hybrid')
      ? layers[candidates[1].key] : null;

    return {
      minerScore:           Math.round(minerRaw),
      shovelScore:          Math.round(shovelRaw),
      gatekeeperScore:      Math.round(gatekeeperRaw),
      primary:              primary,
      primaryLayer:         primaryLayer,
      secondaryLayer:       secondaryLayer,
      confidence:           confidence,
      spread:               Math.round(spread),
      infrastructureDensity: computeDerived('infrastructureDensity', v, rawScores),
      controlLayerStrength:  computeDerived('controlLayerStrength',  v, rawScores),
      dependencyBreadth:     computeDerived('dependencyBreadth',     v, rawScores),
      switchingCost:         computeDerived('switchingCost',         v, rawScores),
      replacementDifficulty: computeDerived('replacementDifficulty', v, rawScores),
      speculationExposure:   computeDerived('speculationExposure',   v, rawScores),
      durabilitySignal:      computeDerived('durabilitySignal',      v, rawScores)
    };
  }

  /* ── Narrative helpers ── */
  function getNarrative(type, primary, name, wave) {
    var block = MODEL.narratives[type] || {};
    var tmpl  = block[primary] || block['Unclear / Early Signal'] || '';
    return applyTemplate(tmpl, name, wave);
  }

  /* ── Dispatch suggestions ── */
  function buildDispatchSuggestions(primary, marketWave) {
    var ex          = MODEL.dispatchExamples;
    var suggestions = (ex[primary] || ex['Shovel']).slice();
    var waveIds     = MODEL.waveDispatchMap[marketWave] || [];
    var existing    = suggestions.map(function (s) { return s.id; });
    var all         = [];
    Object.keys(ex).forEach(function (k) { all = all.concat(ex[k]); });
    waveIds.forEach(function (id) {
      if (existing.indexOf(id) === -1) {
        var match = all.filter(function (e) { return e.id === id; })[0];
        if (match) suggestions.push(match);
      }
    });
    return suggestions.slice(0, 3);
  }

  /* ── Score-bar builder ── */
  function barRow(label, value) {
    var row   = div('score-row');
    var track = div('score-track');
    var fill  = div('score-fill');
    fill.style.width = value + '%';
    track.appendChild(fill);
    row.appendChild(el('span', 'score-row-label', label));
    row.appendChild(track);
    row.appendChild(el('span', 'score-row-value', value + '/100'));
    return row;
  }

  function badgeClass(primary) {
    return 'classification-badge badge-' + primary.toLowerCase().replace(/[\s/]+/g, '-');
  }

  /* ── Application state ── */
  var state = {
    actorName:       MODEL.presets[0].name,
    actorType:       MODEL.presets[0].actorType,
    marketWave:      MODEL.presets[0].marketWave,
    values:          Object.assign({}, MODEL.presets[0].values),
    activePreset:    MODEL.presets[0].name,
    classified:      false,
    isCustomNeutral: false
  };

  /* ── DOM reads ── */
  function currentName()      { return sanitize($('actorName').value, 120) || 'Unnamed Actor'; }
  function currentWaveLabel() { var s = $('marketWave'); return s.options[s.selectedIndex].text; }

  /* ── Sync form inputs from state ── */
  function syncInputs() {
    $('actorName').value  = state.actorName;
    $('actorType').value  = state.actorType;
    $('marketWave').value = state.marketWave;
  }

  /* ── Update live metrics panel ── */
  function updateLiveMetrics(r) {
    var e;
    if ((e = $('metricInfra')))      e.textContent = r.infrastructureDensity + '/100';
    if ((e = $('metricSpec')))       e.textContent = r.speculationExposure   + '/100';
    if ((e = $('metricDurability'))) e.textContent = r.durabilitySignal      + '/100';
    if ((e = $('metricControl')))    e.textContent = r.controlLayerStrength  + '/100';
    if ((e = $('metricConfidence'))) e.textContent = r.confidence;
  }

  /* ── Update result preview ── */
  function showResultPreview(r) {
    /* Swap placeholder → result */
    var placeholder = $('previewPlaceholder');
    var content     = $('previewContent');
    if (placeholder) placeholder.style.display = 'none';
    if (content) content.removeAttribute('hidden');

    var name      = currentName();
    var waveLabel = currentWaveLabel();

    /* Signal source label */
    var ctxEl = $('previewContext');
    if (ctxEl) {
      ctxEl.textContent = state.activePreset
        ? 'Signal Source: ' + state.activePreset + ' preset'
        : 'Signal Source: Custom signal analysis';
    }

    var e;
    if ((e = $('previewActorName'))) e.textContent = name;
    if ((e = $('previewBadge')))   { e.textContent = r.primary; e.className = badgeClass(r.primary); }
    if ((e = $('previewConfidence'))) e.textContent = r.confidence + ' Confidence';
    if ((e = $('previewInfra')))    e.textContent = r.infrastructureDensity + '/100';
    if ((e = $('previewControl')))  e.textContent = r.controlLayerStrength  + '/100';
    if ((e = $('previewSpec')))     e.textContent = r.speculationExposure   + '/100';
    if ((e = $('previewBody'))) {
      e.textContent = r.isNeutralOverride
        ? 'Adjust the structural signals below before treating this classification as meaningful.'
        : getNarrative('classification', r.primary, name, waveLabel);
    }
  }

  /* ── Update full result dossier ── */
  function showDossier(r) {
    var dossier = $('result-dossier');
    if (dossier) dossier.removeAttribute('hidden');

    var name      = currentName();
    var waveLabel = currentWaveLabel();
    var e;

    if ((e = $('dossierActorName')))     e.textContent = name;
    if ((e = $('dossierPrimaryLayer')))  e.textContent = r.primaryLayer;
    if ((e = $('dossierSecondaryLayer'))) e.textContent = r.secondaryLayer || '—';
    if ((e = $('dossierConfidence')))    e.textContent = r.confidence + ' Confidence';
    if ((e = $('dossierBody'))) {
      e.textContent = r.isNeutralOverride
        ? 'Adjust the structural signals below before treating this classification as meaningful.'
        : getNarrative('classification', r.primary, name, waveLabel);
    }
    if ((e = $('dossierMatters')))       e.textContent = getNarrative('matters',         r.primary, name, waveLabel);
    if ((e = $('dossierLimits')))        e.textContent = getNarrative('limits',          r.primary, name, waveLabel);

    if ((e = $('dossierBadge'))) { e.textContent = r.primary; e.className = badgeClass(r.primary); }

    var scoreGrid = $('dossierScores');
    if (scoreGrid) {
      scoreGrid.replaceChildren();
      scoreGrid.appendChild(barRow('Miner',      r.minerScore));
      scoreGrid.appendChild(barRow('Shovel',     r.shovelScore));
      scoreGrid.appendChild(barRow('Gatekeeper', r.gatekeeperScore));
    }

    var metricsGrid = $('dossierMetrics');
    if (metricsGrid) {
      metricsGrid.replaceChildren();
      [
        { label: 'Infrastructure Density', val: r.infrastructureDensity },
        { label: 'Control-Layer Strength', val: r.controlLayerStrength  },
        { label: 'Dependency Breadth',     val: r.dependencyBreadth     },
        { label: 'Switching Cost',         val: r.switchingCost         },
        { label: 'Replacement Difficulty', val: r.replacementDifficulty },
        { label: 'Speculation Exposure',   val: r.speculationExposure   },
        { label: 'Durability Signal',      val: r.durabilitySignal      }
      ].forEach(function (m) {
        var card  = div('derived-card');
        var track = div('derived-track');
        var fill  = div('derived-fill');
        fill.style.width = m.val + '%';
        track.appendChild(fill);
        card.appendChild(el('div', 'derived-label', m.label));
        card.appendChild(track);
        card.appendChild(el('div', 'derived-value', m.val + '/100'));
        metricsGrid.appendChild(card);
      });
    }

    var dispatchList = $('dossierDispatch');
    if (dispatchList) {
      dispatchList.replaceChildren();
      buildDispatchSuggestions(r.primary, state.marketWave).forEach(function (s) {
        var card = div('dispatch-card');
        var link = document.createElement('a');
        link.href      = '/dispatch/' + s.id + '.html';
        link.className = 'dispatch-card-link';
        link.appendChild(el('div', 'dispatch-card-id',    'Dispatch ' + s.id));
        link.appendChild(el('div', 'dispatch-card-actor', s.actor));
        link.appendChild(el('div', 'dispatch-card-wave',  s.wave));
        card.appendChild(link);
        card.appendChild(el('p', 'dispatch-card-note', s.note));
        dispatchList.appendChild(card);
      });
    }
  }

  /* ── Central update: live metrics + classified outputs ── */
  function updateAllOutputs() {
    state.actorName  = sanitize($('actorName').value, 120) || 'Unnamed Actor';
    state.actorType  = $('actorType').value  || 'company';
    state.marketWave = $('marketWave').value || 'other';

    var r = scoreModel(state.values);
    updateLiveMetrics(r);

    if (state.classified) {
      showResultPreview(r);
      showDossier(r);
    }
  }

  /* ── Classify button action ── */
  function classifyNow() {
    state.actorName  = sanitize($('actorName').value, 120) || 'Unnamed Actor';
    state.actorType  = $('actorType').value  || 'company';
    state.marketWave = $('marketWave').value || 'other';
    state.classified = true;

    var r = (!state.activePreset && state.isCustomNeutral)
      ? { primary: 'Unclear / Early Signal', confidence: 'Low', primaryLayer: 'Unclassified',
          secondaryLayer: null, minerScore: 50, shovelScore: 50, gatekeeperScore: 50, spread: 0,
          infrastructureDensity: 50, controlLayerStrength: 50, dependencyBreadth: 50,
          switchingCost: 50, replacementDifficulty: 50, speculationExposure: 50,
          durabilitySignal: 50, isNeutralOverride: true }
      : scoreModel(state.values);

    updateLiveMetrics(r);
    showResultPreview(r);
    showDossier(r);

    var preview = $('previewContent');
    if (preview) preview.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  /* ── Build signal slider cards ── */
  function buildSignals() {
    var grid = $('signalsGrid');
    if (!grid) return;
    grid.replaceChildren();

    MODEL.signals.forEach(function (signal) {
      var card   = div('signal-card');
      var header = div('signal-header');
      var info   = div('signal-info');
      info.appendChild(el('div', 'signal-label', signal.label));
      info.appendChild(el('p',   'signal-desc',  signal.description));

      var badge = el('div', 'signal-badge', state.values[signal.key] + '/100');
      badge.id  = 'badge-' + signal.key;
      header.appendChild(info);
      header.appendChild(badge);
      card.appendChild(header);

      var range   = document.createElement('input');
      range.type  = 'range';
      range.min   = '0';
      range.max   = '100';
      range.step  = '1';
      range.value = state.values[signal.key];
      range.setAttribute('aria-label', signal.label);
      range.id    = 'range-' + signal.key;
      range.addEventListener('input', function () {
        state.values[signal.key] = parseInt(this.value, 10);
        state.isCustomNeutral = false;
        var b = $('badge-' + signal.key);
        if (b) b.textContent = this.value + '/100';
        updateAllOutputs();
      });

      var scale = div('range-scale');
      scale.appendChild(el('span', null, signal.leftLabel));
      scale.appendChild(el('span', null, signal.rightLabel));

      card.appendChild(range);
      card.appendChild(scale);
      grid.appendChild(card);
    });
  }

  /* ── Build preset pills ── */
  function buildPresets() {
    var row = $('presetRow');
    if (!row) return;
    row.replaceChildren();

    MODEL.presets.forEach(function (preset) {
      var btn       = document.createElement('button');
      btn.type      = 'button';
      btn.className = 'pill' + (state.activePreset === preset.name ? ' active' : '');
      btn.textContent = preset.name;
      btn.addEventListener('click', function () {
        state.actorName       = preset.name;
        state.actorType       = preset.actorType;
        state.marketWave      = preset.marketWave;
        state.values          = Object.assign({}, preset.values);
        state.activePreset    = preset.name;
        state.isCustomNeutral = false;
        var note = $('customSignalNote');
        if (note) note.setAttribute('hidden', '');
        syncInputs();
        buildPresets();
        buildSignals();
        updateAllOutputs();
      });
      row.appendChild(btn);
    });
  }

  /* ── Actor name: enter custom mode or re-activate matching preset ── */
  var nameInput = $('actorName');
  if (nameInput) {
    nameInput.addEventListener('input', function () {
      var typed     = sanitize(this.value, 120);
      var matched   = MODEL.presets.filter(function (p) { return p.name === typed; })[0];
      var newActive = matched ? matched.name : null;
      if (newActive !== state.activePreset) {
        var note = $('customSignalNote');
        state.activePreset = newActive;
        buildPresets();
        if (!newActive) {
          /* Entering custom mode: reset all signals to neutral 50 */
          MODEL.signals.forEach(function (s) { state.values[s.key] = 50; });
          state.isCustomNeutral = true;
          state.classified = false;
          buildSignals();
          var placeholder = $('previewPlaceholder');
          var content     = $('previewContent');
          if (placeholder) placeholder.style.display = '';
          if (content) content.setAttribute('hidden', '');
          if (note) note.removeAttribute('hidden');
        } else {
          /* Name exactly matches a preset — load its values */
          state.actorType       = matched.actorType;
          state.marketWave      = matched.marketWave;
          state.values          = Object.assign({}, matched.values);
          state.isCustomNeutral = false;
          syncInputs();
          buildSignals();
          if (note) note.setAttribute('hidden', '');
        }
      }
      updateAllOutputs();
    });
  }

  var typeSelect = $('actorType');
  if (typeSelect) typeSelect.addEventListener('change', updateAllOutputs);

  var waveSelect = $('marketWave');
  if (waveSelect) waveSelect.addEventListener('change', updateAllOutputs);

  var classifyBtn = $('classifyBtn');
  if (classifyBtn) {
    classifyBtn.addEventListener('click', classifyNow);
  } else {
    console.warn('[ShovelsSale Scanner] #classifyBtn not found — classify action unavailable');
  }

  /* ── Hide loading indicator and initialise ── */
  var loadingEl = $('scannerLoading');
  if (loadingEl) loadingEl.style.display = 'none';

  syncInputs();
  buildPresets();
  buildSignals();
  updateAllOutputs();

})();
