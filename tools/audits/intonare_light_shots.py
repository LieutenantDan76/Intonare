#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Capture light-mode module screenshots for visual triage.

Usage (repo root):
  npx --yes serve . -p 8899
  python tools/audits/intonare_light_shots.py
  python tools/audits/intonare_light_shots.py --family train
  python tools/audits/intonare_light_shots.py --family tools   # locked Tools regression
  python tools/audits/intonare_light_shots.py --family all

Writes PNGs + manifest to tools/prototypes/light-mode/shots/
Open review.html in the light-mode lab to vote Fine / Looks off.
Default family is train (+ Tuner/Metro chrome) for regression captures.
Tools + Train + Tuner/Metro + Secondary are locked in review.html; use Include locked
to re-vote. Depth/glass lab: tools/prototypes/light-mode/depth.html before shipping.
Prefer --family all only for full regression packs.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "tools" / "prototypes" / "light-mode" / "shots"
DEFAULT_URL = "http://127.0.0.1:8899/Intonare.html"

# (id, label, family, how to open)
TOOLS_SCREENS = [
    ("tools-hub", "Tools hub", "Tools", "hub"),
    ("piano", "Piano", "Tools", "piano"),
    ("piano-expand", "Piano EXPAND", "Tools", "piano:expand"),
    ("tonal", "Tonal Center", "Tools", "tonal"),
    ("theremin", "Theremin", "Tools", "theremin"),
    ("theremin-expand", "Theremin EXPAND", "Tools", "theremin:expand"),
    ("guitarchords", "Guitar Charts", "Tools", "guitarchords"),
    ("chords", "Chords", "Tools", "chords"),
    ("progression", "Progression", "Tools", "progression"),
    ("drumkit", "Drumkit", "Tools", "drumkit"),
    ("rhythmcards", "Rhythm Cards", "Tools", "rhythmcards"),
    ("cof", "Circle of Fifths", "Tools", "cof"),
    ("intervalref", "Interval Ref", "Tools", "intervalref"),
    ("vocalrange", "Vocal Range · Assess", "Tools", "vocalrange"),
    ("vocalrange-history", "Vocal Range · History", "Tools", "vocalrange:history"),
    ("vocalrange-reference", "Vocal Range · Reference", "Tools", "vocalrange:reference"),
    ("scales", "Scales", "Tools", "scales"),
    ("scales-drone", "Scales · Drone", "Tools", "scales:drone"),
    ("scales-compare", "Scales · Compare", "Tools", "scales:compare"),
    ("survivalguide", "Survival Guide", "Tools", "survivalguide"),
    ("volume", "Volume", "Tools", "volume"),
    ("transpose", "Transposer", "Tools", "transpose"),
]

CHROME_SCREENS = [
    ("tuner", "Tuner tab", "Tuner", "mode:tuner"),
    ("metro", "Metro tab", "Metro", "mode:metro"),
]

TRAIN_SCREENS = [
    # hubs / folders
    ("train", "Train hub", "Train", "mode:train"),
    ("train-ear", "Train · Ear folder", "Train", "trainfolder:ear"),
    ("train-rhythm", "Train · Rhythm folder", "Train", "trainfolder:rhythm"),
    ("train-games", "Train · Games folder", "Train", "trainfolder:games"),
    ("train-reading", "Train · Reading folder", "Train", "trainfolder:reading"),
    # ear — interval
    ("ex-interval", "Interval · Tap", "Train", "exercise:interval"),
    ("ex-interval-sing", "Interval · Sing", "Train", "exercise:interval:sing"),
    ("ex-interval-test", "Interval · Test", "Train", "exercise:interval:test"),
    # ear — chords / pitch match / relative
    ("ex-chords", "Chord ID", "Train", "exercise:chords"),
    ("ex-chords-round", "Chord ID · Round", "Train", "exercise:chords:round"),
    ("ex-singsing", "Pitch Match · Single", "Train", "exercise:singsing"),
    ("ex-singsing-melody", "Pitch Match · Melody", "Train", "exercise:singsing:melody"),
    ("ex-singsing-arp", "Pitch Match · Arpeggio", "Train", "exercise:singsing:arpeggio"),
    ("ex-relpitch", "Relative Pitch", "Train", "exercise:relpitch"),
    # rhythm
    ("ex-tempo", "Tempo Lock", "Train", "exercise:tempo"),
    ("ex-tempoguess", "Tempo Guess", "Train", "exercise:tempoguess"),
    ("ex-tempoguess-listen", "Tempo Guess · Listening", "Train", "exercise:tempoguess:listening"),
    ("ex-poly", "Polyrhythm · Listen", "Train", "exercise:poly"),
    ("ex-poly-practice", "Polyrhythm · Practice", "Train", "exercise:poly:practice"),
    ("ex-poly-challenge", "Polyrhythm · Challenge", "Train", "exercise:poly:challenge"),
    ("ex-rhythmread", "Rhythm Reading · Diff picker", "Train", "exercise:rhythmread"),
    ("ex-rhythmread-play", "Rhythm Reading · Play", "Train", "exercise:rhythmread:play"),
    ("ex-rhythmread-sight", "Rhythm Reading · Sight", "Train", "exercise:rhythmread:sight"),
    # games — pickers + in-round
    ("ex-chordle", "Chordle · Diff picker", "Train", "exercise:chordle"),
    ("ex-chordle-play", "Chordle · Playing", "Train", "exercise:chordle:play"),
    ("ex-diadle", "Diadle · Diff picker", "Train", "exercise:diadle"),
    ("ex-diadle-play", "Diadle · Playing", "Train", "exercise:diadle:play"),
    ("ex-tonale", "Tonale · Mode picker", "Train", "exercise:tonale"),
    ("ex-tonale-play", "Tonale · Playing", "Train", "exercise:tonale:play"),
    ("ex-roadtrip", "Road Trip", "Train", "exercise:roadtrip"),
    # reading
    ("ex-staffread", "Staff Notes", "Train", "exercise:staffread"),
    ("ex-staffread-settings", "Staff Notes · Settings", "Train", "exercise:staffread:settings"),
    ("ex-notationcards", "Notation Cards · Browse", "Train", "exercise:notationcards"),
    ("ex-notationcards-test", "Notation Cards · Test", "Train", "exercise:notationcards:test"),
    # quiz
    ("musicquiz", "Music Quiz hub", "Train", "mq"),
    ("musicquiz-daily", "Music Quiz · Daily popup", "Train", "mq:daily"),
]

# Secondary states — locked Fine (v0.210.94). Regression via --family secondary.
SECONDARY_SCREENS = [
    ("sec-settings", "Settings tab", "Secondary", "mode:settings"),
    ("sec-favorites", "Favorites sheet", "Secondary", "fav"),
    ("sec-tuner-simple", "Tuner · Simple face", "Secondary", "tuner:simple"),
    ("sec-tuner-strobe", "Tuner · Strobe", "Secondary", "tuner:strobe"),
    ("sec-metro-analyze", "Metro · Analyze", "Secondary", "metro:analyze"),
    ("sec-metro-ramp", "Metro · Ramp", "Secondary", "metro:ramp"),
    ("sec-metro-groove", "Metro · Groove", "Secondary", "metro:groove"),
    ("sec-mq-quick", "Quiz · Quick sheet", "Secondary", "mq:quick"),
    ("sec-mq-custom", "Quiz · Custom setup", "Secondary", "mq:custom"),
    ("sec-mq-survival", "Quiz · Survival sheet", "Secondary", "mq:survival"),
    ("sec-mq-play", "Quiz · In-round", "Secondary", "mq:play"),
    ("sec-iv-settings", "Interval · Settings modal", "Secondary", "exercise:interval:settings"),
    ("sec-tempo-play", "Tempo Lock · Playing", "Secondary", "exercise:tempo:play"),
    ("sec-poly-play", "Polyrhythm · Playing", "Secondary", "exercise:poly:play"),
    ("sec-singsing-round", "Pitch Match · Round", "Secondary", "exercise:singsing:round"),
]

FAMILIES = {
    "train": CHROME_SCREENS + TRAIN_SCREENS,
    "tools": TOOLS_SCREENS,
    "chrome": CHROME_SCREENS,
    "secondary": SECONDARY_SCREENS,
    "all": TOOLS_SCREENS + CHROME_SCREENS + TRAIN_SCREENS + SECONDARY_SCREENS,
}


INIT_STORAGE = """() => {
  try {
    localStorage.setItem('intonare_appearance', 'light');
    localStorage.setItem('intonare_skip_splash', '1');
    localStorage.setItem('intonare_autotours_off', '1');
    localStorage.setItem('intonare_first_autotour_done', '1');
    localStorage.setItem('intonare_autotour_prompted', '1');
    localStorage.setItem('tune_tour_done', '1');
    localStorage.setItem('intonare_tours_seen', JSON.stringify([
      'overview','launcher','tuner','metronome','tools','practice',
      'piano','tonal','theremin','guitarchords','chords','progression',
      'drumkit','rhythmcards','cof','intervalref','vocalrange','scales',
      'survivalguide','volume','transpose',
      'interval','chords','singsing','relpitch','tempo','tempoguess','poly',
      'rhythmread','chordle','diadle','tonale','roadtrip','staffread',
      'notationcards','musicquiz'
    ]));
  } catch (e) {}
}"""

SETUP_JS = """() => {
  document.documentElement.classList.add('light-root', 'boot-ready');
  document.body.classList.add('light', 'theme-tools', 'is-pro', 'lnch-settled');
  document.body.classList.remove('lnch-open', 'dark', 'lnch-morphing', 'lnch-reveal', 'scroll-locked');
  try { progState.hasPro = true; } catch (e) {}
  try { refreshProUI(); } catch (e) {}
  try { if (typeof tryUnlockCode === 'function') tryUnlockCode('INTONARE_AMICI'); } catch (e) {}
  try { if (typeof autoTourChoice === 'function') autoTourChoice(false); } catch (e) {}
  try {
    if (typeof showAutoTourPrompt === 'function') window.showAutoTourPrompt = function(){};
    if (typeof maybeWelcomeTour === 'function') window.maybeWelcomeTour = function(){};
    if (typeof maybeAutoTour === 'function') window.maybeAutoTour = function(){};
    if (typeof maybeSectionTour === 'function') window.maybeSectionTour = function(){};
  } catch (e) {}
  try { if (typeof endTour === 'function') endTour(); } catch (e) {}
  // Kill achievement toast pollution in shot lab (Everything Everywhere etc.).
  try {
    if (typeof _achToastQueue !== 'undefined') _achToastQueue = [];
    _achToastActive = false;
    window._achShowNextToast = function(){
      try { _achToastQueue = []; } catch (e) {}
      _achToastActive = false;
    };
    window.checkAchievements = function(){ return []; };
    const toast = document.getElementById('achToast');
    if (toast) { toast.classList.remove('show'); toast.style.display = 'none'; }
    const snd = document.getElementById('sndUnlockToast');
    if (snd) { snd.classList.remove('show'); snd.style.display = 'none'; }
    const stack = document.getElementById('achToastStack');
    if (stack) stack.style.display = 'none';
  } catch (e) {}
  const splash = document.getElementById('intonare-splash');
  if (splash) { splash.style.display = 'none'; splash.style.opacity = '0'; splash.remove(); }
  document.querySelectorAll('.tour-overlay, #tourOverlay, #autoTourPrompt').forEach(el => {
    el.classList.remove('active');
    el.style.display = 'none';
    el.style.visibility = 'hidden';
    el.style.pointerEvents = 'none';
  });
  const lnch = document.getElementById('lnch');
  if (lnch) { lnch.style.display = 'none'; lnch.classList.add('lnch-gone'); }
  const veil = document.getElementById('lnchVeil');
  if (veil) { veil.style.display = 'none'; veil.classList.add('lnch-veil-gone'); }
  ['lnchMorph', 'lnchMorphLoading'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
  });
  try { if (typeof closeAllOverlays === 'function') closeAllOverlays(); } catch (e) {}
}"""

OPEN_JS = """(spec) => {
  try { if (typeof autoTourChoice === 'function') autoTourChoice(false); } catch (e) {}
  try { if (typeof endTour === 'function') endTour(); } catch (e) {}
  try { if (typeof closeThereminOverlay === 'function') closeThereminOverlay(); } catch (e) {}
  try { if (typeof closePianoOverlay === 'function') closePianoOverlay(); } catch (e) {}
  try { if (typeof mqClose === 'function') mqClose(); } catch (e) {}
  try { if (typeof exitExercise === 'function') exitExercise(); } catch (e) {}
  try { if (typeof exitTool === 'function') exitTool(); } catch (e) {}
  document.querySelectorAll('.tour-overlay, #tourOverlay, #autoTourPrompt').forEach(el => {
    el.classList.remove('active');
    el.style.display = 'none';
    el.style.visibility = 'hidden';
    el.style.pointerEvents = 'none';
  });
  try {
    if (typeof _achToastQueue !== 'undefined') _achToastQueue = [];
    const toast = document.getElementById('achToast');
    if (toast) { toast.classList.remove('show'); toast.style.display = 'none'; }
    const stack = document.getElementById('achToastStack');
    if (stack) stack.style.display = 'none';
  } catch (e) {}
  const splash = document.getElementById('intonare-splash');
  if (splash) splash.remove();
  const goMode = (m) => {
    if (typeof setMode === 'function') setMode(m);
    document.body.classList.remove('theme-tuner','theme-metro','theme-tools','theme-train');
    const theme = ({ tuner:'tuner', metronome:'metro', tools:'tools', practice:'train', settings:'train' })[m] || m;
    document.body.classList.add('light', 'theme-' + theme, 'lnch-settled', 'is-pro');
    document.body.classList.remove('lnch-open');
  };
  const killTour = () => {
    try { if (typeof endTour === 'function') endTour(); } catch (e) {}
    document.querySelectorAll('.tour-overlay, #tourOverlay, #autoTourPrompt').forEach(el => {
      el.classList.remove('active');
      el.style.display = 'none';
      el.style.visibility = 'hidden';
      el.style.pointerEvents = 'none';
    });
  };

  if (spec === 'hub' || spec.startsWith('mode:')) {
    const want = spec === 'hub' ? 'tools' : spec.slice(5);
    if (want === 'settings') {
      goMode('practice');
      try { if (typeof openSettings === 'function') openSettings(); } catch (e) {}
      killTour();
      return 'settings';
    }
    const mode = ({ tuner:'tuner', metro:'metronome', tools:'tools', train:'practice' })[want] || want;
    document.body.classList.remove('in-module');
    if (typeof moduleExit === 'function') { try { moduleExit(); } catch (e) {} }
    if (typeof exitTool === 'function') { try { exitTool(); } catch (e) {} }
    if (typeof exitExercise === 'function') { try { exitExercise(); } catch (e) {} }
    goMode(mode);
    // Force section titles — exitExercise/exitTool can race setHeaderSection and
    // leave the app-name wordmark on Tuner/Metro shots.
    try {
      if (mode === 'tuner' && typeof setHeaderSection === 'function') {
        setHeaderSection((typeof t === 'function' && t('mode_tuner')) || 'TUNER', null, 'tuner_sub');
      } else if (mode === 'metronome' && typeof setHeaderSection === 'function') {
        setHeaderSection((typeof t === 'function' && t('mode_metro')) || 'METRO', null, 'metro_sub');
      }
    } catch (e) {}
    killTour();
    return mode;
  }

  if (spec === 'fav') {
    goMode('practice');
    try { if (typeof openFavSheet === 'function') openFavSheet(); } catch (e) {}
    killTour();
    return spec;
  }

  if (spec.startsWith('tuner:')) {
    goMode('tuner');
    try {
      if (typeof setHeaderSection === 'function') {
        setHeaderSection((typeof t === 'function' && t('mode_tuner')) || 'TUNER', null, 'tuner_sub');
      }
      const v = spec.slice(6);
      if (v === 'simple' && typeof setTunerFace === 'function') setTunerFace('simple');
      if (v === 'strobe') {
        if (typeof setTunerFace === 'function') setTunerFace('full');
        if (typeof toggleStrobe === 'function' && !document.body.classList.contains('strobe-active')) toggleStrobe();
        else document.body.classList.add('strobe-active');
      }
    } catch (e) {}
    killTour();
    return spec;
  }

  if (spec.startsWith('metro:')) {
    goMode('metronome');
    try {
      if (typeof setHeaderSection === 'function') {
        setHeaderSection((typeof t === 'function' && t('mode_metro')) || 'METRO', null, 'metro_sub');
      }
      const v = spec.slice(6);
      if (v === 'analyze' && typeof setMetroTab === 'function') setMetroTab('analyze');
      if (v === 'ramp' && typeof setMetroTab === 'function') setMetroTab('ramp');
      if (v === 'groove' && typeof setMetroClickMode === 'function') setMetroClickMode('groove');
    } catch (e) {}
    killTour();
    return spec;
  }

  if (spec === 'mq' || spec.startsWith('mq:')) {
    goMode('practice');
    if (typeof mqOpen === 'function') mqOpen();
    if (spec === 'mq:daily') {
      try { if (typeof mqOpenDailyPopup === 'function') mqOpenDailyPopup(); } catch (e) {}
    }
    if (spec === 'mq:quick') {
      try { if (typeof mqShowQuickSheet === 'function') mqShowQuickSheet(); } catch (e) {}
    }
    if (spec === 'mq:custom') {
      try { if (typeof mqGoCustom === 'function') mqGoCustom(); } catch (e) {}
    }
    if (spec === 'mq:survival') {
      try { if (typeof mqSurvivalPlay === 'function') mqSurvivalPlay(); } catch (e) {}
    }
    if (spec === 'mq:play') {
      try {
        if (typeof mqGoCustom === 'function') mqGoCustom();
        if (typeof mqStartCustom === 'function') mqStartCustom();
      } catch (e) {}
    }
    killTour();
    return spec;
  }

  if (spec.startsWith('trainfolder:')) {
    goMode('practice');
    const which = spec.slice('trainfolder:'.length);
    try {
      if (which === 'ear' && typeof enterEarTraining === 'function') enterEarTraining();
      else if (which === 'rhythm' && typeof enterRhythm === 'function') enterRhythm();
      else if (which === 'games' && typeof enterGames === 'function') enterGames();
      else if (which === 'reading' && typeof enterReading === 'function') enterReading();
    } catch (e) {}
    killTour();
    return spec;
  }

  if (spec.startsWith('exercise:')) {
    goMode('practice');
    const rest = spec.slice('exercise:'.length);
    const parts = rest.split(':');
    const name = parts[0];
    const variant = parts[1] || '';
    if (typeof enterExercise === 'function') enterExercise(name);
    try {
      if (name === 'singsing' && variant) {
        const map = { single: 'single', melody: 'string', string: 'string', arpeggio: 'arpeggio', arp: 'arpeggio' };
        ssPlayMode = map[variant] || variant;
        if (typeof ssBuildModeTabs === 'function') ssBuildModeTabs();
        if (typeof ssEnterNeutral === 'function') ssEnterNeutral();
      }
      if (name === 'interval' && variant === 'sing' && typeof ivSetMode === 'function') {
        ivSetMode('sing');
        try { if (typeof ivNext === 'function') ivNext(); } catch (e) {}
      }
      if (name === 'interval' && variant === 'test' && typeof ivStartTestMode === 'function') ivStartTestMode();
      if (name === 'interval' && variant === 'settings' && typeof ivOpenSettings === 'function') ivOpenSettings();
      if (name === 'chords' && variant === 'round' && typeof ceStartRound === 'function') ceStartRound();
      if (name === 'tempo' && variant === 'play') {
        try { if (typeof tlStart === 'function') tlStart(); else if (typeof tlToggle === 'function') tlToggle(); } catch (e) {}
      }
      if (name === 'poly' && variant === 'play') {
        try { if (typeof prStart === 'function') prStart(); } catch (e) {}
      }
      if (name === 'poly' && variant && variant !== 'play' && typeof prSetTab === 'function') prSetTab(variant);
      if (name === 'singsing' && variant === 'round') {
        try { if (typeof ssNext === 'function') ssNext(); } catch (e) {}
      }
      if (name === 'rhythmread' && (variant === 'play' || variant === 'sight')) {
        // Headless: stub preview/count-in so we get the play UI without scheduling audio.
        var _bp = (typeof rrBeginPreview === 'function') ? rrBeginPreview : null;
        var _bc = (typeof rrBeginCountIn === 'function') ? rrBeginCountIn : null;
        try {
          if (_bp) rrBeginPreview = function(){};
          if (_bc) rrBeginCountIn = function(){};
          if (typeof rrPickDiff === 'function') rrPickDiff('easy');
          if (variant === 'sight' && typeof rrSetMode === 'function') rrSetMode('sight');
        } finally {
          if (_bp) rrBeginPreview = _bp;
          if (_bc) rrBeginCountIn = _bc;
        }
      }
      if (name === 'chordle' && variant === 'play' && typeof chordlePickDiff === 'function') chordlePickDiff('easy');
      if (name === 'diadle' && variant === 'play' && typeof diadlePickDiff === 'function') diadlePickDiff('easy');
      if (name === 'tonale' && variant === 'play' && typeof tonaleStartMode === 'function') tonaleStartMode('easy', false);
      if (name === 'tempoguess' && variant === 'listening') {
        try {
          if (typeof tgStartClicks === 'function') tgStartClicks();
          else if (typeof tgGoOrLock === 'function') tgGoOrLock();
        } catch (e) {}
      }
      if (name === 'staffread' && variant === 'settings') {
        try { if (typeof srOpenSettings === 'function') srOpenSettings(); } catch (e) {}
      }
      if (name === 'notationcards' && variant === 'test' && typeof nctStart === 'function') nctStart();
    } catch (e) {}
    killTour();
    return spec;
  }

  // Tools path (tool or tool:variant)
  goMode('tools');
  const parts = String(spec).split(':');
  const tool = parts[0];
  const variant = parts[1] || '';
  if (typeof enterTool === 'function') enterTool(tool);

  try {
    if (tool === 'scales') {
      if (typeof scaleSetDroneMode === 'function') scaleSetDroneMode(false);
      if (typeof scaleGhostOn !== 'undefined' && scaleGhostOn && typeof scaleToggleGhost === 'function') scaleToggleGhost();
    }
  } catch (e) {}

  try {
    if (variant === 'expand' && tool === 'theremin' && typeof openThereminOverlay === 'function') {
      const ov = document.getElementById('thereminOverlay');
      if (ov) { ov.style.display = ''; ov.style.visibility = ''; ov.style.pointerEvents = ''; }
      openThereminOverlay();
    }
    if (variant === 'expand' && tool === 'piano' && typeof openPianoOverlay === 'function') {
      const ov = document.getElementById('pianoOverlay');
      if (ov) { ov.style.display = ''; ov.style.visibility = ''; ov.style.pointerEvents = ''; }
      openPianoOverlay();
    }
    if (variant === 'drone' && typeof scaleSetDroneMode === 'function') scaleSetDroneMode(true);
    if (variant === 'compare') {
      try {
        scaleType = 'dorian';
        if (typeof updateScale === 'function') updateScale();
        else if (typeof scaleRenderTape === 'function') scaleRenderTape(false);
      } catch (e) {}
      if (typeof scaleGhostOn !== 'undefined' && !scaleGhostOn && typeof scaleToggleGhost === 'function') scaleToggleGhost();
      else if (typeof scaleGhostOn !== 'undefined' && scaleGhostOn && typeof scaleRenderGhost === 'function') scaleRenderGhost();
    }
    if (variant === 'history' || variant === 'reference' || variant === 'assess') {
      const want = variant;
      ['assess','history','reference'].forEach(function(t) {
        const btn = document.getElementById('vrTab-' + t);
        const panel = document.getElementById('vrPanel-' + t);
        if (btn) btn.classList.toggle('active', t === want);
        if (panel) {
          panel.classList.toggle('active', t === want);
          panel.style.opacity = '';
          panel.style.transform = '';
        }
      });
      try {
        if (want === 'history' && typeof vrRenderHistory === 'function') vrRenderHistory();
        if (want === 'reference' && typeof vrRenderReference === 'function') vrRenderReference();
      } catch (e) {}
    }
  } catch (e) {}

  killTour();
  return spec;
}"""

# Applied right before screenshot so dbTick cannot wipe the demo readout.
VOLUME_DEMO_JS = """() => {
  try {
    if (typeof dbAnimFrame !== 'undefined' && dbAnimFrame) {
      clearTimeout(dbAnimFrame);
      dbAnimFrame = null;
    }
  } catch (e) {}
  const el = document.getElementById('dbReadout');
  const lbl = document.getElementById('dbZoneLabel');
  const pk = document.getElementById('dbPeakVal');
  if (el) { el.textContent = '62'; el.className = 'db-number'; el.style.color = '#145a28'; }
  if (lbl) {
    lbl.textContent = 'SAFE';
    lbl.className = 'db-zone-badge';
    lbl.style.color = '#145a28';
    lbl.style.background = 'rgba(20,90,40,0.12)';
    lbl.style.borderColor = 'rgba(20,90,40,0.30)';
    lbl.style.boxShadow = 'none';
  }
  if (pk) pk.textContent = '68';
}"""

KILL_TOAST_JS = """() => {
  try {
    if (typeof _achToastQueue !== 'undefined') _achToastQueue = [];
    _achToastActive = false;
  } catch (e) {}
  document.querySelectorAll('#achToast, #sndUnlockToast, #achToastStack').forEach(el => {
    el.classList.remove('show');
    el.style.display = 'none';
  });
  document.querySelectorAll('.tour-overlay, #tourOverlay, #autoTourPrompt').forEach(el => {
    el.classList.remove('active');
    el.style.display = 'none';
    el.style.visibility = 'hidden';
    el.style.pointerEvents = 'none';
  });
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument(
        "--family",
        default="train",
        choices=sorted(FAMILIES.keys()),
        help="train (default), secondary (leftover states), tools, chrome, all",
    )
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    screens = FAMILIES[args.family]

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Need Playwright: pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    manifest = {
        "savedAt": datetime.now(timezone.utc).isoformat(),
        "url": args.url,
        "family": args.family,
        "screens": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 390, "height": 844},
            device_scale_factor=2,
        )
        context.add_init_script(INIT_STORAGE)
        page = context.new_page()
        print(f"Opening {args.url} … family={args.family} ({len(screens)} shots)")
        page.goto(args.url, wait_until="domcontentloaded", timeout=180000)
        page.wait_for_timeout(1200)
        page.evaluate(SETUP_JS)
        page.wait_for_timeout(400)

        for sid, label, family, spec in screens:
            print(f"  shot {sid} …")
            try:
                page.evaluate(SETUP_JS)
                page.evaluate(OPEN_JS, spec)
                page.wait_for_timeout(900)
                page.evaluate(KILL_TOAST_JS)
                if sid == "volume":
                    page.evaluate(VOLUME_DEMO_JS)
                path = out / f"{sid}.png"
                page.screenshot(path=str(path), full_page=False)
                manifest["screens"].append({
                    "id": sid,
                    "label": label,
                    "family": family,
                    "file": f"{sid}.png",
                    "ok": True,
                })
            except Exception as e:
                print(f"    FAIL {sid}: {e}", file=sys.stderr)
                manifest["screens"].append({
                    "id": sid,
                    "label": label,
                    "family": family,
                    "file": None,
                    "ok": False,
                    "error": str(e),
                })

        browser.close()

    man_path = out / "manifest.json"
    man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {len(manifest['screens'])} entries → {man_path}")
    print("Open tools/prototypes/light-mode/review.html (via the same app server):")
    print("  …/tools/prototypes/light-mode/review.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
