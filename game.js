// ============================================================
//  Spilmotor til "vælg-selv-eventyr"
//  Historien ligger i story.js (window.STORY). Denne fil viser
//  afsnit, håndterer valg og holder styr på eventyrarket.
// ============================================================

(function () {
  "use strict";

  const STORY = window.STORY;
  const bog = document.getElementById("bog");
  const ark = document.getElementById("ark");

  // Spillerens tilstand
  let spiller = null;
  let aktueltAfsnit = null;
  let kampVundet = false;

  // ---------- Gem / hent (localStorage) ----------
  //  Gemmer spillerens ark, hvilket afsnit man står i, og om afsnittets
  //  kamp allerede er vundet. Gemmes ved hvert afsnit og hver ændring
  //  af stats, så man ikke kan genindlæse sig ud af et dårligt slag.
  const GEMNOEGLE = "eventyr-gem:" + STORY.titel;

  function gem() {
    if (!spiller || aktueltAfsnit == null) return;
    try {
      localStorage.setItem(GEMNOEGLE, JSON.stringify({ version: 1, afsnit: aktueltAfsnit, kampVundet, spiller, stemning: document.body.dataset.stemning || "" }));
    } catch (e) { /* privat vindue o.l. – spillet virker bare uden gem */ }
  }

  function hentGemt() {
    try {
      const data = JSON.parse(localStorage.getItem(GEMNOEGLE));
      if (data && data.version === 1 && data.spiller && STORY.afsnit[data.afsnit]) {
        // ting, der har skiftet navn siden spillet blev gemt
        const NYE_NAVNE = { "Nissens løfte": "Koboldens løfte" };
        data.spiller.inventar = (data.spiller.inventar || []).map((t) => NYE_NAVNE[t] || t);
        data.spiller.foelge = data.spiller.foelge || [];
        data.spiller.minder = data.spiller.minder || [];
        // gemt før Karisma fandtes: giv en middel-værdi
        if (data.spiller.karisma == null) {
          data.spiller.karisma = 9;
          data.spiller.max.karisma = 9;
        }
        return data;
      }
    } catch (e) { /* ugyldigt eller utilgængeligt */ }
    return null;
  }

  function sletGemt() {
    try { localStorage.removeItem(GEMNOEGLE); } catch (e) { /* ignorer */ }
  }

  // ---------- Opdagelser (huskes på tværs af gennemspilninger) ----------
  //  Hvilke afsnit, slutninger og ting du nogensinde har fundet, hvor mange
  //  gange du er død, og hvilke præstationer du har låst op. Gemmes for sig,
  //  så de overlever "Start forfra" og nye eventyr.
  const OPDNOEGLE = "eventyr-opdagelser:" + STORY.titel;
  const ALLE_AFSNIT = Object.keys(STORY.afsnit).map(Number).sort((x, y) => x - y);
  const SLUTNINGER = [
    ...ALLE_AFSNIT.filter((n) => STORY.afsnit[n].slut).map((n) => ({
      id: String(n), navn: STORY.afsnit[n].slutnavn || `Slutning ${n}`, sejr: STORY.afsnit[n].slut === "sejr",
    })),
    { id: "udmattet", navn: "Kræfterne slap op", sejr: false },
  ];
  const opd = hentOpd();

  function hentOpd() {
    const tom = { afsnit: new Set(), slutninger: new Set(), ting: new Set(), praestationer: new Set(), doede: 0 };
    try {
      const d = JSON.parse(localStorage.getItem(OPDNOEGLE));
      if (d) {
        return {
          afsnit: new Set((d.afsnit || []).map(Number)), slutninger: new Set(d.slutninger || []),
          ting: new Set(d.ting || []), praestationer: new Set(d.praestationer || []), doede: d.doede || 0,
        };
      }
    } catch (e) { /* ugyldigt eller utilgængeligt */ }
    return tom;
  }

  function gemOpd() {
    try {
      localStorage.setItem(OPDNOEGLE, JSON.stringify({
        afsnit: [...opd.afsnit], slutninger: [...opd.slutninger], ting: [...opd.ting],
        praestationer: [...opd.praestationer], doede: opd.doede,
      }));
    } catch (e) { /* ignorer */ }
  }

  function opfyldt(p) {
    if (p.afsnit != null) return opd.afsnit.has(p.afsnit);
    if (p.nogenAfsnit) return p.nogenAfsnit.some((n) => opd.afsnit.has(n));
    if (p.ting) return opd.ting.has(p.ting);
    if (p.procent != null) return (opd.afsnit.size * 100) / ALLE_AFSNIT.length >= p.procent;
    if (p.slutninger != null) return opd.slutninger.size >= p.slutninger;
    if (p.doede != null) return opd.doede >= p.doede;
    return false;
  }

  // Registrér noget nyt og vis en lille besked ved nye slutninger og præstationer
  function noter({ afsnit, slut, ting, doed } = {}) {
    if (afsnit != null) opd.afsnit.add(Number(afsnit));
    if (ting) opd.ting.add(ting);
    if (doed) opd.doede++;
    if (slut != null && !opd.slutninger.has(String(slut))) {
      opd.slutninger.add(String(slut));
      const s = SLUTNINGER.find((x) => x.id === String(slut));
      if (s) toast(s.sejr ? "✦ Ny slutning" : "☠ Ny slutning", s.navn);
    }
    for (const p of STORY.praestationer || []) {
      if (!opd.praestationer.has(p.id) && opfyldt(p)) {
        opd.praestationer.add(p.id);
        toast("🏆 Præstation", p.titel);
        Lyd.spil("held");
      }
    }
    gemOpd();
  }

  function toast(overskrift, tekst) {
    let holder = document.getElementById("toasts");
    if (!holder) {
      holder = el("div", { id: "toasts", "aria-live": "polite" });
      document.body.append(holder);
    }
    const t = el("div", { class: "toast" }, el("strong", {}, overskrift), el("span", {}, tekst));
    holder.append(t);
    setTimeout(() => t.classList.add("vaek"), 4200);
    setTimeout(() => t.remove(), 5000);
  }

  // ---------- Kortet ----------
  //  Tegnes ud fra STORY.kort. Et sted bliver synligt, når man har besøgt et af
  //  dets afsnit (i et hvilket som helst spil). Resten ligger i tåge.
  function stedFor(afsnit) {
    return (STORY.kort?.steder || []).find((x) => x.afsnit.includes(Number(afsnit))) || null;
  }

  function visKort() {
    const K = STORY.kort;
    if (!K) return;
    const B = K.bredde, H = K.hoejde;
    let frø = 11;
    const rnd = () => (frø = (frø * 16807) % 2147483647) / 2147483647;
    const sti = (pts) => "M" + pts.map(([x, y]) => `${x} ${y}`).join(" L") + "Z";
    const glat = (pts) => {
      let d = `M${pts[0][0]} ${pts[0][1]}`;
      for (let i = 1; i < pts.length; i++) {
        const [x0, y0] = pts[i - 1], [x1, y1] = pts[i];
        d += ` Q${x0} ${y0} ${(x0 + x1) / 2} ${(y0 + y1) / 2}`;
      }
      const [xs, ys] = pts[pts.length - 1];
      return d + ` T${xs} ${ys}`;
    };
    const inde = (pts, x, y) => {
      let ind = false;
      for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
        const [xi, yi] = pts[i], [xj, yj] = pts[j];
        if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) ind = !ind;
      }
      return ind;
    };

    // landskab
    let ter = "";
    for (const t of K.terraen) {
      if (t.type === "sne") ter += `<path d="${sti(t.punkter)}" fill="#eef3f6" stroke="#9fb3c2" stroke-width="2"/>`;
      if (t.type === "hav") {
        ter += `<path d="${sti(t.punkter)}" fill="#a9c4d4" stroke="#5f7f94" stroke-width="2.5"/>`;
        let boelger = "";
        for (let i = 0; i < 160 && boelger.length < 2600; i++) {
          const x = rnd() * B, y = rnd() * H;
          if (inde(t.punkter, x, y) && inde(t.punkter, x + 16, y)) boelger += `M${x.toFixed(0)} ${y.toFixed(0)} q4 -4 8 0 t8 0 `;
        }
        ter += `<path d="${boelger}" stroke="#5f7f94" stroke-width="1.4" fill="none" opacity=".7"/>`;
      }
      if (t.type === "oe") ter += `<circle cx="${t.x}" cy="${t.y}" r="${t.r}" fill="#c9c08f" stroke="#6b5536" stroke-width="2"/>`;
      if (t.type === "flod") ter += `<path d="${glat(t.punkter)}" fill="none" stroke="#7fa3bb" stroke-width="7" stroke-linecap="round"/><path d="${glat(t.punkter)}" fill="none" stroke="#5f7f94" stroke-width="1.2" stroke-linecap="round"/>`;
      if (t.type === "sump") ter += `<ellipse cx="${t.x}" cy="${t.y}" rx="${t.r}" ry="${t.r * 0.6}" fill="#7d8f6a" opacity=".6"/>`;
      if (t.type === "bjerge") {
        for (let i = 0; i < t.antal; i++) {
          const x = t.x - t.b / 2 + (t.b * (i + 0.5)) / t.antal + (rnd() - 0.5) * 18;
          const y = t.y + (rnd() - 0.5) * 30;
          const h = 26 + rnd() * 22, w = h * 0.9;
          ter += `<path d="M${x - w / 2} ${y + h / 2} L${x} ${y - h / 2} L${x + w / 2} ${y + h / 2}Z" fill="${t.sne ? "#dfe6ea" : "#a8987e"}" stroke="#4a3a2a" stroke-width="1.8"/>`;
          ter += `<path d="M${x} ${y - h / 2} L${x + w / 2} ${y + h / 2} L${x + w * 0.1} ${y + h / 2}Z" fill="#4a3a2a" opacity=".25"/>`;
          ter += `<path d="M${x - w * 0.18} ${y - h * 0.18} L${x} ${y - h / 2} L${x + w * 0.18} ${y - h * 0.18}" fill="#fff" stroke="none" opacity=".85"/>`;
        }
      }
      if (t.type === "skov") {
        for (let i = 0; i < Math.round(t.r / 2.2); i++) {
          const a = rnd() * Math.PI * 2, d = Math.sqrt(rnd()) * t.r;
          const x = t.x + Math.cos(a) * d, y = t.y + Math.sin(a) * d * 0.6;
          ter += `<path d="M${x - 6} ${y + 6} L${x} ${y - 9} L${x + 6} ${y + 6}Z" fill="#4f7a3c" stroke="#2f4a2c" stroke-width="1"/>`;
        }
      }
      if (t.type === "hede" || t.type === "aske") {
        for (let i = 0; i < 40; i++) {
          const a = rnd() * Math.PI * 2, d = Math.sqrt(rnd()) * t.r;
          ter += `<circle cx="${(t.x + Math.cos(a) * d).toFixed(0)}" cy="${(t.y + Math.sin(a) * d * 0.6).toFixed(0)}" r="${(1.5 + rnd() * 2).toFixed(1)}" fill="${t.type === "hede" ? "#9a5a7a" : "#8a817a"}" opacity=".7"/>`;
        }
      }
    }

    // steder, veje og tåge
    const besoegt = (st) => st.afsnit.some((n) => opd.afsnit.has(n));
    const syn = new Set(K.steder.filter(besoegt).map((x) => x.id));
    const her = aktueltAfsnit != null ? stedFor(aktueltAfsnit) : null;
    const pos = Object.fromEntries(K.steder.map((x) => [x.id, x]));
    let veje = "";
    for (const [a, b] of K.veje) {
      if (!syn.has(a) || !syn.has(b)) continue;
      veje += `<path d="M${pos[a].x} ${pos[a].y} L${pos[b].x} ${pos[b].y}" stroke="#6b5536" stroke-width="2" stroke-dasharray="6 5" fill="none" opacity=".8"/>`;
    }
    let huller = "", markoerer = "";
    for (const st of K.steder) {
      if (!syn.has(st.id)) continue;
      huller += `<circle cx="${st.x}" cy="${st.y}" r="78" fill="black"/>`;
      const erHer = her && her.id === st.id;
      markoerer += `<g class="kortsted${erHer ? " her" : ""}">` +
        (erHer ? `<circle cx="${st.x}" cy="${st.y}" r="22" fill="none" stroke="#8b1e1e" stroke-width="3" class="puls"/>` : "") +
        `<circle cx="${st.x}" cy="${st.y}" r="15" fill="#f3e7c9" stroke="#2b1d0e" stroke-width="2"/>` +
        `<text x="${st.x}" y="${st.y + 5}" text-anchor="middle" font-size="15">${st.ikon}</text>` +
        `<text x="${st.x}" y="${st.y + 32}" text-anchor="middle" class="kortnavn">${st.navn}</text></g>`;
    }
    const svg =
      `<svg viewBox="0 0 ${B} ${H}" class="kortsvg" role="img" aria-label="Kort over eventyrets verden">` +
      `<defs><filter id="kTaage" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="22"/></filter>` +
      `<mask id="kMaske"><rect width="${B}" height="${H}" fill="white"/><g filter="url(#kTaage)">${huller}</g></mask>` +
      `<filter id="kPapir"><feTurbulence type="fractalNoise" baseFrequency=".02" numOctaves="3" seed="4"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .45  0 0 0 0 .3  0 0 0 .35 -.05"/></filter></defs>` +
      `<rect width="${B}" height="${H}" fill="#efe0bd"/>${ter}` +
      `<rect width="${B}" height="${H}" fill="#efe4c8" mask="url(#kMaske)" opacity=".93"/>` +
      `<rect width="${B}" height="${H}" filter="url(#kPapir)" opacity=".6"/>` +
      veje + markoerer +
      `<g transform="translate(${B - 58} ${H - 58})" class="kompas"><circle r="24" fill="#f3e7c9" stroke="#2b1d0e" stroke-width="1.5"/>` +
      `<path d="M0 -20 L5 0 L0 20 L-5 0Z" fill="#2b1d0e"/><path d="M0 -20 L5 0 L-5 0Z" fill="#8b1e1e"/><text y="-28" text-anchor="middle" class="kortnavn">N</text></g>` +
      `<rect x="3" y="3" width="${B - 6}" height="${H - 6}" fill="none" stroke="#2b1d0e" stroke-width="4"/></svg>`;

    const holder = el("div", { class: "kort-holder" });
    holder.innerHTML = svg;
    const dlg = el("dialog", { class: "opdagelser kort-dialog" },
      el("button", { class: "luk", type: "button", "aria-label": "Luk", onclick: () => dlg.close() }, "✕"),
      el("h2", {}, "🗺️ Kortet"),
      el("p", { class: "samlet" }, `Du har udforsket ${syn.size} af ${K.steder.length} steder${her ? ` · Du er i ${her.navn}` : ""}`),
      holder,
      el("p", { class: "regel" }, "Steder dukker op, når du har været der – i dette eller et tidligere eventyr.")
    );
    dlg.addEventListener("close", () => dlg.remove());
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    document.body.append(dlg);
    dlg.showModal();
  }

  function visOpdagelser() {
    const set = opd.afsnit.size;
    const pct = (n, i) => (i ? Math.round((n * 100) / i) : 0);
    const bar = (n, i) => el("div", { class: "bar" }, el("div", { class: "fyld", style: `width:${pct(n, i)}%` }));

    const kapitler = [...(STORY.kapitler || [{ titel: STORY.titel, start: STORY.start }])].sort((a, b) => a.start - b.start);
    const kapRaekker = kapitler.map((k, i) => {
      const slut = kapitler[i + 1] ? kapitler[i + 1].start : Infinity;
      const ids = ALLE_AFSNIT.filter((n) => n >= k.start && n < slut);
      const sete = ids.filter((n) => opd.afsnit.has(n)).length;
      return el("div", { class: "kaprad" },
        el("div", { class: "kaptitel" }, el("span", {}, k.titel), el("span", {}, `${sete} / ${ids.length}`)), bar(sete, ids.length));
    });

    const slutListe = el("ul", { class: "slutliste" }, ...SLUTNINGER.map((s) => {
      const fundet = opd.slutninger.has(s.id);
      return el("li", { class: fundet ? (s.sejr ? "sejr" : "doed") : "skjult" },
        el("span", { class: "ikon" }, fundet ? (s.sejr ? "✦" : "☠") : "?"), fundet ? s.navn : "???");
    }));

    const praest = STORY.praestationer || [];
    const praestListe = el("ul", { class: "praestliste" }, ...praest.map((p) => {
      const har = opd.praestationer.has(p.id);
      return el("li", { class: har ? "har" : "mangler" },
        el("span", { class: "ikon" }, har ? "🏆" : "🔒"),
        el("div", {}, el("strong", {}, p.titel), el("span", {}, p.tekst)));
    }));

    const dlg = el("dialog", { class: "opdagelser" },
      el("button", { class: "luk", type: "button", "aria-label": "Luk", onclick: () => dlg.close() }, "✕"),
      el("h2", {}, "📜 Opdagelser"),
      el("p", { class: "samlet" }, `Du har set ${set} af ${ALLE_AFSNIT.length} afsnit (${pct(set, ALLE_AFSNIT.length)} %)`),
      bar(set, ALLE_AFSNIT.length),
      ...kapRaekker,
      el("h3", {}, `Slutninger · ${opd.slutninger.size} af ${SLUTNINGER.length}`),
      slutListe,
      el("h3", {}, `Præstationer · ${opd.praestationer.size} af ${praest.length}`),
      praestListe,
      el("p", { class: "doede" }, opd.doede ? `Du er død ${opd.doede} ${opd.doede === 1 ? "gang" : "gange"} indtil videre.` : "Du er ikke død endnu. Godt gået!"),
      el("button", {
        class: "lille", type: "button",
        onclick: () => {
          if (!confirm("Vil du nulstille alle opdagelser og præstationer? Det kan ikke fortrydes.")) return;
          for (const k of ["afsnit", "slutninger", "ting", "praestationer"]) opd[k].clear();
          opd.doede = 0;
          gemOpd();
          dlg.close();
        },
      }, "Nulstil opdagelser")
    );
    dlg.addEventListener("close", () => dlg.remove());
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    document.body.append(dlg);
    dlg.showModal();
  }

  // ---------- Hjælpere ----------
  const d6 = () => 1 + Math.floor(Math.random() * 6);

  function el(tag, attrs = {}, ...born) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") e.className = v;
      else if (k === "onclick") e.addEventListener("click", v);
      else if (v === true) e.setAttribute(k, "");
      else if (v !== false && v != null) e.setAttribute(k, v);
    }
    for (const b of born) if (b != null) e.append(b);
    return e;
  }

  // Som append(), men springer null/undefined over (ellers skrives "null" på siden)
  function fyld(maal, ...dele) {
    maal.append(...dele.filter((d) => d != null));
  }

  function illustration(src, tekst) {
    if (!src) return null;
    const img = el("img", { src, alt: tekst || "", loading: "lazy" });
    img.addEventListener("error", () => fig.remove()); // manglende billede → bare ingen billede
    const fig = el("figure", { class: "illustration" }, img, tekst ? el("figcaption", {}, tekst) : null);
    return fig;
  }

  // Stemning: skifter baggrundens farve (skov, flod, tårn …). Se style.css.
  function saetStemning(navn) {
    document.body.dataset.stemning = navn || "";
  }

  // ---------- Lyd (laves med Web Audio – ingen lydfiler) ----------
  const Lyd = (() => {
    let ctx = null;
    let til = false;
    try { til = localStorage.getItem("eventyr-lyd") === "til"; } catch (e) { /* ignorer */ }

    function lydkort() {
      if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
      if (ctx.state === "suspended") ctx.resume();
      return ctx;
    }
    function stoej(varighed, frekvens, styrke = 0.3, filter = "bandpass") {
      const a = lydkort();
      const n = Math.floor(a.sampleRate * varighed);
      const buf = a.createBuffer(1, n, a.sampleRate);
      const d = buf.getChannelData(0);
      for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 2);
      const src = a.createBufferSource();
      src.buffer = buf;
      const f = a.createBiquadFilter();
      f.type = filter;
      f.frequency.value = frekvens;
      const g = a.createGain();
      g.gain.value = styrke;
      src.connect(f).connect(g).connect(a.destination);
      src.start();
    }
    function tone(frekvens, start, varighed, styrke = 0.12, type = "triangle") {
      const a = lydkort();
      const o = a.createOscillator();
      const g = a.createGain();
      const t = a.currentTime + start;
      o.type = type;
      o.frequency.value = frekvens;
      g.gain.setValueAtTime(0, t);
      g.gain.linearRampToValueAtTime(styrke, t + 0.02);
      g.gain.exponentialRampToValueAtTime(0.001, t + varighed);
      o.connect(g).connect(a.destination);
      o.start(t);
      o.stop(t + varighed + 0.05);
    }
    const lyde = {
      side: () => stoej(0.4, 1600, 0.15),
      terning: () => { for (let i = 0; i < 4; i++) setTimeout(() => stoej(0.05, 2800, 0.35, "highpass"), i * 70 + Math.random() * 30); },
      hug: () => { stoej(0.2, 700, 0.6); tone(180, 0, 0.15, 0.1, "sawtooth"); },
      au: () => { stoej(0.25, 300, 0.7, "lowpass"); tone(110, 0, 0.3, 0.15, "sine"); },
      held: () => [880, 1175, 1568].forEach((f, i) => tone(f, i * 0.07, 0.4, 0.07, "sine")),
      sejr: () => [523, 659, 784, 1047].forEach((f, i) => tone(f, i * 0.16, 0.7)),
      doed: () => [220, 196, 165, 110].forEach((f, i) => tone(f, i * 0.32, 0.9, 0.12, "sine")),
    };
    return {
      get til() { return til; },
      skift() {
        til = !til;
        try { localStorage.setItem("eventyr-lyd", til ? "til" : "fra"); } catch (e) { /* ignorer */ }
        if (til) lyde.side();
        return til;
      },
      spil(navn) {
        if (!til) return;
        try { lyde[navn]?.(); } catch (e) { /* lyd er ikke vigtig nok til at stoppe spillet */ }
      },
    };
  })();

  const lydknap = document.getElementById("lyd");
  const tegnLydknap = () => {
    lydknap.textContent = Lyd.til ? "🔊" : "🔇";
    lydknap.setAttribute("aria-label", Lyd.til ? "Slå lyd fra" : "Slå lyd til");
    lydknap.title = Lyd.til ? "Lyd: til" : "Lyd: fra";
  };
  lydknap.addEventListener("click", () => { Lyd.skift(); tegnLydknap(); });
  tegnLydknap();

  function afsnitTekst(tekst) {
    const div = el("div", { class: "tekst" });
    const stykker = Array.isArray(tekst) ? tekst : String(tekst).split(/\n\s*\n/);
    for (const s of stykker) div.append(el("p", {}, s.trim()));
    return div;
  }

  function nySide(klasse = "") {
    bog.replaceChildren();
    bog.className = "bog " + klasse;
    // genstart blad-animationen
    void bog.offsetWidth;
    bog.style.animation = "none";
    void bog.offsetWidth;
    bog.style.animation = "";
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // ---------- Startskærm og terningeslag ----------
  function slaaEvner() {
    const evne = d6() + 6;
    const udh = d6() + d6() + 12;
    const held = d6() + 6;
    const karisma = d6() + 6;
    return {
      evne, udholdenhed: udh, held, karisma, guld: STORY.startGuld ?? 5,
      max: { evne, udholdenhed: udh, held, karisma },
      inventar: [...(STORY.startInventar || [])],
      foelge: [],
      minder: [],
    };
  }

  function visStart() {
    ark.hidden = true;
    nySide();
    let slag = slaaEvner();

    const vaerdier = el("div", { class: "slag" });
    const tegnSlag = () => {
      vaerdier.replaceChildren(
        ...[["Evne", slag.evne], ["Udholdenhed", slag.udholdenhed], ["Held", slag.held], ["Karisma", slag.karisma]]
          .map(([navn, v]) => el("div", {}, el("span", { class: "vaerdi" }, String(v)), el("span", { class: "navn" }, navn)))
      );
    };
    tegnSlag();

    const gemt = hentGemt();
    const fortsaet = gemt
      ? el("div", { class: "gemt" },
          el("p", {}, `Du har et gemt eventyr i afsnit ${gemt.afsnit} med ${gemt.spiller.udholdenhed} Udholdenhed.`),
          el("button", {
            class: "stor", type: "button",
            onclick: () => {
              spiller = gemt.spiller;
              ark.hidden = false;
              saetStemning(gemt.stemning);
              gaaTil(gemt.afsnit, { fraGem: true, vundet: !!gemt.kampVundet });
            },
          }, "Fortsæt eventyret")
        )
      : null;

    saetStemning(STORY.forsidestemning || "");
    fyld(bog,
      el("h1", {}, STORY.titel),
      el("p", { class: "undertitel" }, STORY.undertitel || ""),
      el("p", { class: "opd-link" },
        el("button", { class: "lille", type: "button", onclick: visOpdagelser },
          `📜 Opdagelser · ${opd.praestationer.size} af ${(STORY.praestationer || []).length} præstationer`),
        el("button", { class: "lille", type: "button", onclick: visKort }, "🗺️ Kort")),
      illustration(STORY.forsidebillede),
      fortsaet,
      afsnitTekst(STORY.intro),
      el("h2", {}, "Dine evner"),
      el("p", { class: "regel" },
        "Evne = 1 terning + 6 · Udholdenhed = 2 terninger + 12 · Held = 1 terning + 6 · Karisma = 1 terning + 6. " +
        "Karisma afgør, hvordan folk tager imod dig – men ikke alle kan lide en sølvtunge. " +
        "Falder din Udholdenhed til 0, er dit eventyr forbi."),
      vaerdier,
      el("div", { class: "knapper" },
        el("button", { class: "stor sekundaer", type: "button", onclick: () => { slag = slaaEvner(); tegnSlag(); } }, "🎲 Slå igen"),
        el("button", {
          class: gemt ? "stor sekundaer" : "stor", type: "button",
          onclick: () => begynd(slag, STORY.start, null, gemt),
        }, gemt ? "Begynd et nyt eventyr" : "Begynd eventyret")
      ),
      kapitelvalg(() => slag, gemt)
    );
  }

  // Start et nyt eventyr – evt. i et senere kapitel med standard-udstyr
  function begynd(slag, start, udstyr, gemt) {
    if (gemt && !confirm("Vil du starte et nyt eventyr? Dit gemte eventyr bliver overskrevet.")) return;
    const s = JSON.parse(JSON.stringify(slag));
    if (udstyr) {
      if (udstyr.inventar) s.inventar = [...udstyr.inventar];
      if (typeof udstyr.guld === "number") s.guld = udstyr.guld;
      for (const [stat, n] of Object.entries(udstyr.loeft || {})) {
        s.max[stat] += n;
        s[stat] += n;
      }
    }
    spiller = s;
    ark.hidden = false;
    gaaTil(start);
  }

  function kapitelvalg(hentSlag, gemt) {
    const senere = (STORY.kapitler || []).filter((k) => k.start !== STORY.start);
    if (!senere.length) return null;
    return el("details", { class: "kapitelvalg" },
      el("summary", {}, "Start i et senere kapitel"),
      el("p", { class: "regel" },
        "Du starter med dine slåede evner, lidt ekstra styrke og et standard-udstyr. " +
        "Ting, du ellers ville have fundet i de tidligere kapitler, har du ikke med."),
      el("div", { class: "knapper" },
        ...senere.map((k) => el("button", {
          class: "stor sekundaer", type: "button",
          onclick: () => begynd(hentSlag(), k.start, k.udstyr, gemt),
        }, k.titel))
      )
    );
  }

  // ---------- Effekter ----------
  function anvendEffekter(eff) {
    const log = [];
    if (!eff) return log;

    for (const stat of ["evne", "udholdenhed", "held", "karisma", "guld"]) {
      if (typeof eff[stat] !== "number" || eff[stat] === 0) continue;
      const foer = spiller[stat];
      let efter = foer + eff[stat];
      if (stat !== "guld" && spiller.max[stat] != null) efter = Math.min(efter, spiller.max[stat]);
      efter = Math.max(0, efter);
      spiller[stat] = efter;
      const diff = efter - foer;
      if (diff !== 0) {
        const navn = stat[0].toUpperCase() + stat.slice(1);
        log.push({ klasse: diff < 0 ? "minus" : "plus", tekst: `${diff > 0 ? "+" : "−"}${Math.abs(diff)} ${navn}` });
        blink(stat);
      }
    }
    // "loeft" hæver både startværdien og den nuværende værdi (fx et magisk sværd)
    for (const [stat, n] of Object.entries(eff.loeft || {})) {
      if (spiller.max[stat] == null || !n) continue;
      spiller.max[stat] += n;
      spiller[stat] += n;
      const navn = stat[0].toUpperCase() + stat.slice(1);
      log.push({ klasse: "plus", tekst: `+${n} ${navn} (permanent)` });
      blink(stat);
    }
    for (const ting of [].concat(eff.giv || [])) {
      if (!spiller.inventar.includes(ting)) {
        spiller.inventar.push(ting);
        log.push({ klasse: "ting", tekst: `+ ${ting}` });
        opd.ting.add(ting);
      }
    }
    for (const ting of [].concat(eff.tag || [])) {
      const i = spiller.inventar.indexOf(ting);
      if (i >= 0) {
        spiller.inventar.splice(i, 1);
        log.push({ klasse: "minus", tekst: `− ${ting}` });
      }
    }
    // Minder: vigtige valg, som historien husker på tværs af kapitler
    spiller.minder = spiller.minder || [];
    for (const m of [].concat(eff.husk || [])) {
      if (!spiller.minder.includes(m)) spiller.minder.push(m);
    }
    // Følgesvende kommer og går
    spiller.foelge = spiller.foelge || [];
    if (eff.forladAlle && spiller.foelge.length) {
      for (const navn of spiller.foelge) log.push({ klasse: "minus", tekst: `👋 ${navn} går sin egen vej` });
      spiller.foelge = [];
    }
    for (const navn of [].concat(eff.forlad || [])) {
      const i = spiller.foelge.indexOf(navn);
      if (i >= 0) {
        spiller.foelge.splice(i, 1);
        log.push({ klasse: "minus", tekst: `👋 ${navn} går sin egen vej` });
      }
    }
    for (const navn of [].concat(eff.foelge || [])) {
      if (!spiller.foelge.includes(navn)) {
        spiller.foelge.push(navn);
        log.push({ klasse: "plus", tekst: `🤝 ${navn} følger med dig` });
      }
    }
    return log;
  }

  // ---------- Brug af ting ----------
  function brugTing(navn) {
    const def = (STORY.genstande || {})[navn];
    const i = spiller.inventar.indexOf(navn);
    if (!def || !def.brug || i < 0 || spiller.udholdenhed <= 0) return;
    spiller.inventar.splice(i, 1);
    const log = anvendEffekter(def.brug);
    Lyd.spil("held");
    toast(`${def.ikon || "🎒"} Du bruger ${navn}`, log.map((l) => l.tekst).join(" · ") || "Intet sker.");
    opdaterArk();
    gem();
  }

  function visTing(navn) {
    const def = (STORY.genstande || {})[navn] || {};
    const kanBruges = !!def.brug && spiller.inventar.includes(navn) && spiller.udholdenhed > 0;
    const dlg = el("dialog", { class: "ting-dialog" },
      el("button", { class: "luk", type: "button", "aria-label": "Luk", onclick: () => dlg.close() }, "✕"),
      el("div", { class: "ting-ikon" }, def.ikon || "🎒"),
      el("h2", {}, navn),
      el("p", {}, def.tekst || "En ting, du har med dig."),
      kanBruges
        ? el("button", { class: "stor", type: "button", onclick: () => { dlg.close(); brugTing(navn); } }, `Brug ${navn.toLowerCase()}`)
        : null
    );
    dlg.addEventListener("close", () => dlg.remove());
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    document.body.append(dlg);
    dlg.showModal();
  }

  function visFoelgesvend(navn) {
    const def = (STORY.foelgesvende || {})[navn] || {};
    const evne = def.heling ? `Heler dig ${def.heling} Udholdenhed` : `Gør ${def.skade || 1} skade`;
    const dlg = el("dialog", { class: "ting-dialog" },
      el("button", { class: "luk", type: "button", "aria-label": "Luk", onclick: () => dlg.close() }, "✕"),
      el("div", { class: "ting-ikon" }, def.ikon || "🤝"),
      el("h2", {}, navn),
      el("p", {}, def.tekst || "Din følgesvend."),
      el("p", { class: "regel" }, `I kamp: ${evne} i ${Math.round((def.chance || 0) * 100)} % af runderne.`)
    );
    dlg.addEventListener("close", () => dlg.remove());
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    document.body.append(dlg);
    dlg.showModal();
  }

  function blink(stat) {
    const dd = document.getElementById("stat-" + stat);
    if (!dd) return;
    dd.classList.remove("blink");
    void dd.offsetWidth;
    dd.classList.add("blink");
  }

  // ---------- Valg ----------
  // Tekstvarianter: { kraever?: "ting" | ["ting", ...], mangler?: ..., tekst, billede?, billedtekst? }
  //  Den første variant, hvis betingelser passer med oppakningen, erstatter
  //  afsnittets tekst – fx når en fange allerede er sluppet fri. Varianten kan
  //  også skifte billedet ud (eller skjule det med billede: null).
  function harAlle(liste) {
    return [].concat(liste || []).every((t) => spiller.inventar.includes(t));
  }
  function harIngen(liste) {
    return [].concat(liste || []).every((t) => !spiller.inventar.includes(t));
  }
  // Betingelser på ting (kraever/mangler) og minder (husker/glemt)
  function opfylder(x) {
    const minder = spiller.minder || [];
    return harAlle(x.kraever) && harIngen(x.mangler)
      && [].concat(x.husker || []).every((m) => minder.includes(m))
      && [].concat(x.glemt || []).every((m) => !minder.includes(m));
  }
  function valgtVariant(a) {
    return (a.varianter || []).find(opfylder) || null;
  }
  // Ekstra tekst: afsnit, der føjes til, når betingelserne passer (fx et minde)
  function ekstraTekst(a) {
    return (a.ekstra || []).filter(opfylder).map((x) => x.tekst);
  }

  function kanVaelge(v) {
    if (v.kraever && !spiller.inventar.includes(v.kraever)) return { synlig: false };
    if (v.mangler && spiller.inventar.includes(v.mangler)) return { synlig: false };
    if (v.husker && !(spiller.minder || []).includes(v.husker)) return { synlig: false };
    if (v.glemt && (spiller.minder || []).includes(v.glemt)) return { synlig: false };
    if (v.kraeverGuld && spiller.guld < v.kraeverGuld) return { synlig: true, aktiv: false, grund: `kræver ${v.kraeverGuld} guld` };
    // Karisma: nogle samtaler kræver, at folk kan lide dig – andre, at du er grov og ligefrem
    const kar = spiller.karisma ?? 9;
    if (v.kraeverKarisma && kar < v.kraeverKarisma) return { synlig: true, aktiv: false, grund: `kræver Karisma ${v.kraeverKarisma}` };
    if (v.hoejstKarisma && kar > v.hoejstKarisma) return { synlig: true, aktiv: false, grund: `kun med Karisma højst ${v.hoejstKarisma}` };
    return { synlig: true, aktiv: true };
  }

  // ---------- Vis et afsnit ----------
  function gaaTil(id, { fraGem = false, vundet = false, besked = null } = {}) {
    const a = STORY.afsnit[id];
    if (!a) {
      nySide();
      bog.append(el("h2", {}, "Fejl i historien"), el("p", {}, `Afsnit ${id} findes ikke.`));
      return;
    }

    // Effekter gælder kun, når man går ind i afsnittet – ikke når man henter et gemt spil
    const log = fraGem ? [] : anvendEffekter(a.effekter);
    if (besked) log.unshift(besked);
    aktueltAfsnit = id;
    kampVundet = vundet;
    gem();
    opdaterArk();
    if (!fraGem) noter({ afsnit: id });

    const doed = spiller.udholdenhed <= 0 || a.slut === "død";
    nySide(a.slut === "sejr" ? "slut-sejr" : doed ? "slut-dod" : "");
    if (a.stemning !== undefined) saetStemning(a.stemning);
    if (!fraGem) Lyd.spil("side");

    fyld(bog, a.kapitel ? el("h2", { class: "kapitel" }, a.kapitel) : null, el("span", { class: "nummer" }, String(id)), ...(() => {
      const v = valgtVariant(a);
      const billede = v && "billede" in v ? v.billede : a.billede;
      const billedtekst = v && "billedtekst" in v ? v.billedtekst : a.billedtekst;
      const ekstra = ekstraTekst(a);
      const tekst = [v ? v.tekst : a.tekst, ...ekstra].join("\n\n");
      return [illustration(billede, billedtekst), afsnitTekst(tekst)];
    })());

    if (log.length) {
      bog.append(el("ul", { class: "effekter" }, ...log.map((l) => el("li", { class: l.klasse }, l.tekst))));
    }

    if (doed || a.slut) {
      const sejr = a.slut === "sejr" && !doed;
      const udmattet = doed && a.slut !== "død";
      if (!fraGem) noter({ slut: udmattet ? "udmattet" : id, doed: !sejr });
      visSlut(sejr, udmattet, doed ? null : a.fortsaet);
      return;
    }

    if (a.kamp && !kampVundet) {
      visKamp(a, () => { kampVundet = true; gem(); visValg(a); });
    } else {
      visValg(a);
    }
  }

  // fortsaet: { til, tekst } – en sejr, der fører videre til næste kapitel.
  //  Så beholdes det gemte spil, og spilleren kan fortsætte med samme helt.
  function visSlut(sejr, udmattet, fortsaet = null) {
    if (sejr && fortsaet) {
      saetStemning("sejr");
      Lyd.spil("sejr");
      bog.classList.add("slut-sejr");
      bog.append(
        el("h2", { class: "slutskilt" }, "✦ Kapitlet er slut! ✦"),
        el("div", { class: "knapper" },
          el("button", { class: "stor", type: "button", onclick: () => gaaTil(fortsaet.til) }, fortsaet.tekst || "Fortsæt til næste kapitel"),
          el("button", { class: "stor sekundaer", type: "button", onclick: () => { sletGemt(); aktueltAfsnit = null; visStart(); } }, "Start forfra")
        )
      );
      return;
    }
    sletGemt();
    aktueltAfsnit = null;
    saetStemning(sejr ? "sejr" : "død");
    Lyd.spil(sejr ? "sejr" : "doed");
    bog.classList.toggle("slut-dod", !sejr);
    bog.classList.toggle("slut-sejr", sejr);
    if (udmattet) {
      bog.append(el("p", {}, "Dine kræfter slipper op. Du segner om, og mørket lukker sig om dig."));
    }
    bog.append(
      el("h2", { class: "slutskilt" }, sejr ? "✦ Du har klaret det! ✦" : "Dit eventyr ender her"),
      el("div", { class: "knapper" }, el("button", { class: "stor", type: "button", onclick: visStart }, "Spil igen"))
    );
  }

  // Ændr en stat (holder sig inden for 0 og startværdien) og opdatér arket
  function aendre(stat, n) {
    let v = spiller[stat] + n;
    if (stat !== "guld" && spiller.max[stat] != null) v = Math.min(v, spiller.max[stat]);
    spiller[stat] = Math.max(0, v);
    blink(stat);
    opdaterArk();
    if (spiller.udholdenhed > 0) gem();
  }

  // ---------- Kamp ----------
  //  Hver runde: begge slår 2 terninger + Evne. Den laveste mister 2 Udholdenhed.
  //  Uafgjort: ingen skade. Efter et træf kan man "prøve lykken":
  //  slå 2 terninger ≤ Held = heldig. Held falder med 1 hver gang.
  //    Du ramte:  heldig → +2 ekstra skade, uheldig → 1 skade mindre
  //    Du blev ramt: heldig → 1 skade mindre, uheldig → 1 skade ekstra
  const vis = (ds) => `🎲${ds.join("+")}`;

  function visKamp(a, naarVundet) {
    const fjender = [].concat(a.kamp).map((f) => ({ ...f, liv: f.udholdenhed }));
    let nr = 0;          // hvilken fjende vi kæmper mod
    let runde = 0;
    let sidste = null;   // "ramte" | "ramt" | null – åbner for "Prøv lykken"
    let animation = null; // samme værdier – hvilken rystelse der skal vises ved næste tegning
    let truffet = -1;     // hvilken fjende der lige er blevet ramt
    const log = [];
    const boks = el("section", { class: "kamp", "aria-live": "polite" });
    bog.append(boks);

    function tjekSlut() {
      if (spiller.udholdenhed <= 0) {
        tegn(false);
        noter({ slut: "udmattet", doed: true });
        visSlut(false, true);
        return true;
      }
      const f = fjender[nr];
      if (f.liv <= 0) {
        log.unshift({ k: "vandt", t: `${f.navn} falder til jorden!` });
        nr++;
        sidste = null;
        if (nr >= fjender.length) {
          tegn(false);
          boks.append(el("p", { class: "sejrtekst" }, fjender.length > 1 ? "Du har besejret alle dine fjender." : `Du har besejret ${f.navn}.`));
          naarVundet();
          return true;
        }
      }
      return false;
    }

    function angrib() {
      const f = fjender[nr];
      runde++;
      const mine = [d6(), d6()], dens = [d6(), d6()];
      const dinStyrke = mine[0] + mine[1] + spiller.evne;
      const densStyrke = dens[0] + dens[1] + f.evne;
      const tal = `Du ${vis(mine)} + ${spiller.evne} = ${dinStyrke} · ${f.navn} ${vis(dens)} + ${f.evne} = ${densStyrke}`;
      Lyd.spil("terning");
      if (dinStyrke > densStyrke) {
        f.liv -= 2; sidste = "ramte";
        log.unshift({ k: "ramte", t: `Runde ${runde}: ${tal}. Du rammer! (−2)` });
        setTimeout(() => Lyd.spil("hug"), 300);
      } else if (densStyrke > dinStyrke) {
        aendre("udholdenhed", -2); sidste = "ramt";
        log.unshift({ k: "ramt", t: `Runde ${runde}: ${tal}. Du bliver ramt! (−2)` });
        setTimeout(() => Lyd.spil("au"), 300);
      } else {
        sidste = null;
        log.unshift({ k: "lige", t: `Runde ${runde}: ${tal}. I parerer begge.` });
      }
      animation = sidste;
      truffet = nr;
      foelgesvendeHandler(f);
      if (!tjekSlut()) tegn(true);
    }

    // Hver runde kan dine følgesvende hjælpe til
    function foelgesvendeHandler(f) {
      for (const navn of spiller.foelge || []) {
        const def = (STORY.foelgesvende || {})[navn];
        if (!def || f.liv <= 0 || spiller.udholdenhed <= 0 || Math.random() >= (def.chance || 0)) continue;
        if (def.skade) {
          f.liv -= def.skade;
          if (animation !== "ramt") { animation = "ramte"; truffet = nr; }
          log.unshift({ k: "ramte", t: `${def.ikon || "🤝"} ${def.handling || navn + " hjælper"}: ${f.navn} mister ${def.skade}.` });
        }
        if (def.heling) {
          aendre("udholdenhed", def.heling);
          log.unshift({ k: "ramte", t: `${def.ikon || "🤝"} ${def.handling || navn + " hjælper"} (+${def.heling} Udholdenhed).` });
        }
      }
    }

    function proevLykken() {
      const f = fjender[nr];
      const ds = [d6(), d6()];
      const heldig = ds[0] + ds[1] <= spiller.held;
      aendre("held", -1);
      Lyd.spil("terning");
      if (heldig) setTimeout(() => Lyd.spil("held"), 300);
      animation = sidste === "ramte" ? (heldig ? "ramte" : null) : (heldig ? null : "ramt");
      truffet = nr;
      const intro = `Prøv lykken: ${vis(ds)} = ${ds[0] + ds[1]} mod Held ${spiller.held + 1}. `;
      if (sidste === "ramte") {
        if (heldig) { f.liv -= 2; log.unshift({ k: "ramte", t: intro + "Heldig! Et dybt sår (−2 ekstra)." }); }
        else { f.liv += 1; log.unshift({ k: "ramt", t: intro + "Uheldig, kun en skramme (+1 tilbage)." }); }
      } else {
        if (heldig) { aendre("udholdenhed", 1); log.unshift({ k: "ramte", t: intro + "Heldig! Slaget strejfer dig kun (+1)." }); }
        else { aendre("udholdenhed", -1); log.unshift({ k: "ramt", t: intro + "Uheldig, slaget sidder hårdt (−1 ekstra)." }); }
      }
      sidste = null;
      if (!tjekSlut()) tegn(true);
    }

    function flygt() {
      aendre("udholdenhed", -2);
      if (spiller.udholdenhed <= 0) {
        log.unshift({ k: "ramt", t: "Du får et hug i ryggen, da du vender dig for at flygte." });
        tegn(false);
        noter({ slut: "udmattet", doed: true });
        visSlut(false, true);
        return;
      }
      gaaTil(a.flygt.til);
    }

    function tegn(aktiv) {
      const kort = fjender.map((x, j) =>
        el("div", { class: "fjende" + (aktiv && j === nr ? " aktiv" : "") + (x.liv <= 0 ? " faldet" : "") + (animation === "ramte" && j === truffet ? " truffet" : "") },
          el("span", { class: "fnavn" }, x.navn),
          el("span", {}, `Evne ${x.evne}`),
          el("span", {}, `Udholdenhed ${Math.max(0, x.liv)} / ${x.udholdenhed}`)
        )
      );
      const knapper = aktiv
        ? el("div", { class: "kampknapper" },
            el("button", { class: "stor", type: "button", onclick: angrib }, `⚔ Angrib ${fjender[nr].navn}`),
            el("button", {
              class: "stor sekundaer", type: "button", onclick: proevLykken,
              disabled: !sidste || spiller.held <= 0,
              title: "Slå 2 terninger. Er resultatet højst din Held, er du heldig. Koster 1 Held.",
            }, "🍀 Prøv lykken"),
            a.flygt ? el("button", { class: "stor sekundaer", type: "button", onclick: flygt }, `🏃 ${a.flygt.tekst || "Flygt"} (−2 Udholdenhed)`) : null
          )
        : null;
      boks.replaceChildren();
      fyld(boks,
        el("h2", {}, "⚔ Kamp"),
        el("div", { class: "fjender" }, ...kort),
        knapper,
        log.length ? el("ol", { class: "kamplog" }, ...log.map((l) => el("li", { class: l.k }, l.t))) : null
      );
      // Ryst skærmen når spilleren bliver ramt
      bog.classList.remove("ryst");
      if (animation === "ramt") { void bog.offsetWidth; bog.classList.add("ryst"); }
      animation = null;
    }

    tegn(true);
  }

  // Et valg kan være en lykketest: { test: "held", til: <heldig>, ellers: <uheldig> }
  //  Slå 2 terninger – højst din Held = heldig. Held falder altid med 1.
  function vaelg(v) {
    if (v.test === "karisma") return karismaproeve(v);
    if (v.test !== "held") return gaaTil(v.til);
    const ds = [d6(), d6()];
    const sum = ds[0] + ds[1];
    const heldig = sum <= spiller.held;
    const foer = spiller.held;
    spiller.held = Math.max(0, spiller.held - 1);
    Lyd.spil("terning");
    if (heldig) setTimeout(() => Lyd.spil("held"), 300);
    gaaTil(heldig ? v.til : v.ellers, {
      besked: {
        klasse: heldig ? "plus" : "minus",
        tekst: `🍀 ${ds[0]}+${ds[1]} = ${sum} mod Held ${foer}: ${heldig ? "Heldig!" : "Uheldig!"} (−1 Held)`,
      },
    });
  }

  // Karismaprøve: slå 2 terninger – højst din Karisma = det lykkes.
  //  I modsætning til Held bliver Karisma ikke brugt op af at prøve.
  function karismaproeve(v) {
    const ds = [d6(), d6()];
    const sum = ds[0] + ds[1];
    const kar = spiller.karisma ?? 9;
    const lykkes = sum <= kar;
    Lyd.spil("terning");
    if (lykkes) setTimeout(() => Lyd.spil("held"), 300);
    gaaTil(lykkes ? v.til : v.ellers, {
      besked: {
        klasse: lykkes ? "plus" : "minus",
        tekst: `🗣️ ${ds[0]}+${ds[1]} = ${sum} mod Karisma ${kar}: ${lykkes ? "Det lykkes!" : "Det mislykkes."}`,
      },
    });
  }

  function visValg(a) {
    const liste = el("ul", { class: "valg" });
    for (const v of a.valg || []) {
      const status = kanVaelge(v);
      if (!status.synlig) continue;
      const knap = el("button", { type: "button", disabled: !status.aktiv, onclick: () => vaelg(v) },
        el("span", {}, v.tekst + (status.grund ? ` (${status.grund})` : "")),
        el("span", { class: "til" }, v.test === "held" ? "🍀 Prøv lykken" : v.test === "karisma" ? "🗣️ Karismaprøve" : `Gå til ${v.til}`)
      );
      liste.append(el("li", {}, knap));
    }
    bog.append(liste);
    liste.querySelector("button:not(:disabled)")?.focus({ preventScroll: true });
  }

  // ---------- Eventyrark ----------
  function opdaterArk() {
    document.getElementById("stat-evne").textContent = `${spiller.evne} / ${spiller.max.evne}`;
    document.getElementById("stat-udholdenhed").textContent = `${spiller.udholdenhed} / ${spiller.max.udholdenhed}`;
    document.getElementById("stat-held").textContent = `${spiller.held} / ${spiller.max.held}`;
    document.getElementById("stat-karisma").textContent = `${spiller.karisma ?? 9} / ${spiller.max.karisma ?? 9}`;
    document.getElementById("stat-guld").textContent = spiller.guld;
    const ul = document.getElementById("inventar");
    const genstande = STORY.genstande || {};
    ul.replaceChildren(
      ...(spiller.inventar.length
        ? spiller.inventar.map((t) => {
            const def = genstande[t] || {};
            return el("li", { class: def.brug ? "kan-bruges" : "" },
              el("button", { type: "button", class: "ting-knap", title: def.brug ? "Klik for at læse om tingen eller bruge den" : "Klik for at læse om tingen", onclick: () => visTing(t) },
                def.ikon ? el("span", { class: "ikon" }, def.ikon) : null, t, def.brug ? el("span", { class: "brug-maerke" }, "brug") : null));
          })
        : [el("li", { class: "tom" }, "Tom")])
    );
    const fl = document.getElementById("foelge");
    const foelge = spiller.foelge || [];
    document.getElementById("foelge-titel").hidden = !foelge.length;
    fl.hidden = !foelge.length;
    fl.replaceChildren(...foelge.map((n) => {
      const def = (STORY.foelgesvende || {})[n] || {};
      return el("li", {}, el("button", { type: "button", class: "ting-knap", onclick: () => visFoelgesvend(n) },
        el("span", { class: "ikon" }, def.ikon || "🤝"), n));
    }));
  }

  document.getElementById("opdagelser").addEventListener("click", visOpdagelser);
  document.getElementById("kort").addEventListener("click", visKort);

  document.getElementById("forfra").addEventListener("click", () => {
    if (confirm("Vil du starte forfra? Dit nuværende eventyr går tabt.")) {
      sletGemt();
      aktueltAfsnit = null;
      visStart();
    }
  });

  // ---------- Kom i gang ----------
  document.title = STORY.titel;
  visStart();

  // Til fejlsøgning i konsollen: tjekHistorie()
  window.tjekHistorie = function () {
    const ids = new Set(Object.keys(STORY.afsnit).map(Number));
    const naaet = new Set();
    const fejl = [];
    const koe = [STORY.start];
    while (koe.length) {
      const id = koe.pop();
      if (naaet.has(id)) continue;
      naaet.add(id);
      const a = STORY.afsnit[id];
      if (!a) { fejl.push(`Afsnit ${id} mangler`); continue; }
      if (!a.slut && !(a.valg || []).length) fejl.push(`Afsnit ${id} har ingen valg og er ikke en slutning`);
      for (const v of a.valg || []) {
        koe.push(v.til);
        if (v.test) {
          if (v.ellers == null) fejl.push(`Afsnit ${id}: lykke-valget "${v.tekst}" mangler "ellers"`);
          else koe.push(v.ellers);
        }
      }
      if (a.flygt) koe.push(a.flygt.til);
      if (a.fortsaet) koe.push(a.fortsaet.til);
    }
    for (const id of ids) if (!naaet.has(id)) fejl.push(`Afsnit ${id} kan ikke nås`);
    for (const p of STORY.praestationer || []) {
      for (const n of [].concat(p.afsnit ?? [], p.nogenAfsnit ?? [])) {
        if (!ids.has(n)) fejl.push(`Præstationen "${p.titel}" peger på afsnit ${n}, som ikke findes`);
      }
    }
    return fejl.length ? fejl : "Alt ser fint ud ✔";
  };
})();
