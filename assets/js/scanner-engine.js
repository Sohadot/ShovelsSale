(function () {
  'use strict';

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

  function init(model) {
    var signals = model.signals;
    var presets = model.presets;
    var dispatchExamples = model.dispatchExamples;
    var waveDispatchMap = model.waveDispatchMap;
    var scoring = model.scoring;
    var conf = model.confidence;
    var layers = model.layers;
    var narratives = model.narratives;

    var state = {
      actorName: presets[0].name,
      actorType: presets[0].actorType,
      marketWave: presets[0].marketWave,
      values: Object.assign({}, presets[0].values),
      activePreset: presets[0].name,
      classified: false
    };

    /* ── Sync form inputs from state (called on init and preset click) ── */
    function syncInputs() {
      $('actorName').value = state.actorName;
      $('actorType').value = state.actorType;
      $('marketWave').value = state.marketWave;
    }

    /* ── Scoring model — reads weights from JSON ── */
    function computeRawScore(term, v) {
      var total = 0;
      scoring[term].forEach(function (w) {
        total += (w.invert ? (100 - v[w.signal]) : v[w.signal]) * w.weight;
      });
      return clamp(total, 0, 100);
    }

    function computeDerived(name, v, rawScores) {
      var def = model.derivedMetrics[name];
      if (!def) return 0;
      if (def.formula === 'avg') {
        var sum = 0;
        def.components.forEach(function (c) {
          sum += c.invert ? (100 - v[c.signal]) : v[c.signal];
        });
        return Math.round(sum / def.components.length);
      }
      if (def.formula === 'score') {
        return Math.round(rawScores[def.source] || 0);
      }
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

      var rawScores = { miner: minerRaw, shovel: shovelRaw, gatekeeper: gatekeeperRaw };

      var candidates = [
        { key: 'Miner',      val: minerRaw },
        { key: 'Shovel',     val: shovelRaw },
        { key: 'Gatekeeper', val: gatekeeperRaw }
      ].sort(function (a, b) { return b.val - a.val; });

      var spread  = candidates[0].val - candidates[1].val;
      var primary = candidates[0].key;
      var confidence;

      if (candidates[0].val < conf.lowScoreThreshold) {
        primary    = 'Unclear / Early Signal';
        confidence = 'Low';
      } else if (spread <= conf.hybridSpreadThreshold) {
        primary    = 'Hybrid';
        confidence = 'Mixed';
      } else if (spread >= conf.highSpreadThreshold && candidates[0].val >= conf.highMinScore) {
        confidence = 'High';
      } else {
        confidence = 'Moderate';
      }

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
      var block = narratives[type] || {};
      var tmpl  = block[primary] || block['Unclear / Early Signal'] || '';
      return applyTemplate(tmpl, name, wave);
    }

    /* ── Dispatch suggestions ── */
    function buildDispatchSuggestions(primary, marketWave) {
      var suggestions = (dispatchExamples[primary] || dispatchExamples['Shovel']).slice();
      var waveIds     = waveDispatchMap[marketWave] || [];
      var existing    = suggestions.map(function (s) { return s.id; });
      var allExamples = [];
      Object.keys(dispatchExamples).forEach(function (k) {
        allExamples = allExamples.concat(dispatchExamples[k]);
      });
      waveIds.forEach(function (id) {
        if (existing.indexOf(id) === -1) {
          var match = allExamples.filter(function (e) { return e.id === id; })[0];
          if (match) suggestions.push(match);
        }
      });
      return suggestions.slice(0, 3);
    }

    /* ── Shared score-bar builder ── */
    function barRow(label, value) {
      var row = div('score-row');
      row.appendChild(el('span', 'score-row-label', label));
      var track = div('score-track');
      var fill  = div('score-fill');
      fill.style.width = value + '%';
      track.appendChild(fill);
      row.appendChild(track);
      row.appendChild(el('span', 'score-row-value', value + '/100'));
      return row;
    }

    /* ── Badge class helper ── */
    function badgeClass(primary) {
      return 'classification-badge badge-' + primary.toLowerCase().replace(/[\s/]+/g, '-');
    }

    /* ── Read current actor name from DOM ── */
    function currentName() {
      return sanitize($('actorName').value, 120) || 'Unnamed Actor';
    }
    function currentWaveLabel() {
      var sel = $('marketWave');
      return sel.options[sel.selectedIndex].text;
    }

    /* ── Update live metrics panel (top panel, always live) ── */
    function updateLiveMetrics(r) {
      $('metricInfra').textContent      = r.infrastructureDensity + '/100';
      $('metricSpec').textContent       = r.speculationExposure   + '/100';
      $('metricDurability').textContent = r.durabilitySignal      + '/100';
      $('metricControl').textContent    = r.controlLayerStrength  + '/100';
      $('metricConfidence').textContent = r.confidence;
    }

    /* ── Update immediate result preview ── */
    function updateResultPreview(r) {
      var preview = $('resultPreview');
      if (!preview) return;
      preview.removeAttribute('hidden');

      var name = currentName();
      if ($('previewActorName')) $('previewActorName').textContent = name;

      var badge = $('previewBadge');
      if (badge) { badge.textContent = r.primary; badge.className = badgeClass(r.primary); }

      if ($('previewConfidence'))  $('previewConfidence').textContent  = r.confidence + ' Confidence';
      if ($('previewInfra'))       $('previewInfra').textContent       = r.infrastructureDensity + '/100';
      if ($('previewControl'))     $('previewControl').textContent     = r.controlLayerStrength  + '/100';
      if ($('previewSpec'))        $('previewSpec').textContent        = r.speculationExposure   + '/100';
      if ($('previewBody'))        $('previewBody').textContent        = getNarrative('classification', r.primary, name, currentWaveLabel());
    }

    /* ── Update full result dossier ── */
    function updateDossier(r) {
      var dossier = $('dossier');
      if (dossier) dossier.removeAttribute('hidden');

      var name      = currentName();
      var waveLabel = currentWaveLabel();

      if ($('dossierActorName'))    $('dossierActorName').textContent    = name;
      if ($('dossierPrimaryLayer')) $('dossierPrimaryLayer').textContent = r.primaryLayer;
      if ($('dossierSecondaryLayer')) $('dossierSecondaryLayer').textContent = r.secondaryLayer || '—';
      if ($('dossierConfidence'))   $('dossierConfidence').textContent   = r.confidence + ' Confidence';
      if ($('dossierBody'))         $('dossierBody').textContent         = getNarrative('classification', r.primary, name, waveLabel);
      if ($('dossierMatters'))      $('dossierMatters').textContent      = getNarrative('matters',         r.primary, name, waveLabel);
      if ($('dossierLimits'))       $('dossierLimits').textContent       = getNarrative('limits',          r.primary, name, waveLabel);

      var badge = $('dossierBadge');
      if (badge) { badge.textContent = r.primary; badge.className = badgeClass(r.primary); }

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

    /* ── Central update (reads state, updates all outputs) ── */
    function updateAllOutputs() {
      state.actorName  = sanitize($('actorName').value, 120) || 'Unnamed Actor';
      state.actorType  = $('actorType').value  || 'company';
      state.marketWave = $('marketWave').value || 'other';

      var r = scoreModel(state.values);
      updateLiveMetrics(r);

      if (state.classified) {
        updateResultPreview(r);
        updateDossier(r);
      }
    }

    /* ── Classify button: run, show, scroll ── */
    function classifyNow() {
      state.actorName  = sanitize($('actorName').value, 120) || 'Unnamed Actor';
      state.actorType  = $('actorType').value  || 'company';
      state.marketWave = $('marketWave').value || 'other';
      state.classified = true;

      var r = scoreModel(state.values);
      updateLiveMetrics(r);
      updateResultPreview(r);
      updateDossier(r);

      var preview = $('resultPreview');
      if (preview) preview.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /* ── Build signal slider cards ── */
    function buildSignals() {
      var grid = $('signalsGrid');
      if (!grid) return;
      grid.replaceChildren();

      signals.forEach(function (signal) {
        var card   = div('signal-card');
        var header = div('signal-header');
        var info   = div('signal-info');
        info.appendChild(el('div', 'signal-label', signal.label));
        info.appendChild(el('p',   'signal-desc',  signal.description));

        var badge     = el('div', 'signal-badge', state.values[signal.key] + '/100');
        badge.id      = 'badge-' + signal.key;
        header.appendChild(info);
        header.appendChild(badge);
        card.appendChild(header);

        var range = document.createElement('input');
        range.type  = 'range';
        range.min   = '0';
        range.max   = '100';
        range.step  = '1';
        range.value = state.values[signal.key];
        range.setAttribute('aria-label', signal.label);
        range.id    = 'range-' + signal.key;
        range.addEventListener('input', function () {
          state.values[signal.key] = parseInt(this.value, 10);
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

      presets.forEach(function (preset) {
        var btn       = document.createElement('button');
        btn.type      = 'button';
        btn.className = 'pill' + (state.activePreset === preset.name ? ' active' : '');
        btn.textContent = preset.name;
        btn.addEventListener('click', function () {
          state.actorName    = preset.name;
          state.actorType    = preset.actorType;
          state.marketWave   = preset.marketWave;
          state.values       = Object.assign({}, preset.values);
          state.activePreset = preset.name;
          syncInputs();
          buildPresets();
          buildSignals();
          updateAllOutputs();
        });
        row.appendChild(btn);
      });
    }

    /* ── Actor name input: clear active preset if name no longer matches ── */
    $('actorName').addEventListener('input', function () {
      var typed    = sanitize(this.value, 120);
      var matched  = presets.filter(function (p) { return p.name === typed; })[0];
      var newActive = matched ? matched.name : null;
      if (newActive !== state.activePreset) {
        state.activePreset = newActive;
        buildPresets();
      }
      updateAllOutputs();
    });

    $('actorType').addEventListener('change', updateAllOutputs);
    $('marketWave').addEventListener('change', updateAllOutputs);

    var classifyBtn = $('classifyBtn');
    if (classifyBtn) classifyBtn.addEventListener('click', classifyNow);

    /* ── Remove loading indicator ── */
    var loadingEl = $('scannerLoading');
    if (loadingEl) loadingEl.style.display = 'none';

    /* ── Initial render ── */
    syncInputs();
    buildPresets();
    buildSignals();
    updateAllOutputs();
  }

  /* ── Bootstrap: fetch model then initialise ── */
  var loadingEl = $('scannerLoading');

  fetch('/data/scanner-model.json')
    .then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function (model) {
      init(model);
    })
    .catch(function () {
      if (loadingEl) {
        loadingEl.textContent = 'Scanner model could not be loaded. Please reload the page.';
        loadingEl.style.display = '';
      }
    });

})();
