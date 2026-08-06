#!/usr/bin/env python3
"""Genera le tessere-maschera sparse dei motivi decorativi (pigne, funghi,
scoiattoli, creste).

NON serve per far funzionare il sito: le tessere che usa sono gia' dentro
style.css. Serve solo se vuoi cambiare densita' o disposizione delle figure.

    python3 strumenti-motivi.py

Scrive motivi.css, che contiene le variabili --m-<motivo>-sb (banda) e
--m-<motivo>-sf (fondo dell'apertura). Poi ricopia quelle righe dentro il
blocco :root di style.css, al posto di quelle che ci sono.

Le manopole utili sono in fondo al file: FIGURE_BANDA e FIGURE_FONDO per la
densita', LARGH_BANDA e TESS_FONDO per i periodi di ripetizione.
"""
import math, random, urllib.parse

# ---- figure: path, centro, mezze-estensioni ------------------------------
PIGNA = dict(
    d=("M16 5.5v3"
       "M16 8.5c6 3.5 8.5 9 8.5 14.5S20.5 33.5 16 38c-4.5-4.5-8.5-9.5-8.5-15S10 12 16 8.5z"
       "M9 15.5q7 5 14 0M8 21.5q8 5.5 16 0M9.5 27.5q6.5 5 13 0M12 33q4 4 8 0"),
    c=(16, 21.75), h=(8.5, 16.25), kind="stroke", sw=1.15)

RAMO = dict(
    d=("M48 38V8"
       "M48 12l-4-3M48 12l4-3M48 15.6l-4.8-3.4M48 15.6l4.8-3.4"
       "M48 19.2l-5.4-3.8M48 19.2l5.4-3.8M48 22.8l-6-4.2M48 22.8l6-4.2"
       "M48 26.4l-6.4-4.5M48 26.4l6.4-4.5M48 30l-6.8-4.8M48 30l6.8-4.8"
       "M48 33.6l-7-5M48 33.6l7-5"),
    c=(48, 23), h=(7, 15), kind="stroke", sw=1.15)

FUNGO = dict(
    d=("M37 25q0-11 9.5-11T56 25M37 25h19M43 25v8.5q3.5 2.6 7 0V25"),
    dots=("M43.4 19.8h.01M49.8 18.4h.01M46.6 22.4h.01"),
    c=(46.5, 23.75), h=(9.5, 9.75), kind="stroke", sw=1.15)

MONTE = dict(
    d=("M0 20 8 6 13 12 20 2 28 14 34 20"
       "M17.2 6l1.4 1.3 1.4-1.3 1.3 1.3 1.4-1.3"),
    c=(17, 11), h=(17, 10), kind="stroke", sw=1.3)

# scoiattolo: sagoma piena, senza occhio (a questa scala sarebbe invisibile
# e in una maschera un foro non si puo' fare con un riempimento opaco)
SCOIA = dict(
    d=None, c=(23.2, 24.65), h=(19.5, 19.7), kind="scoia")

SCOIA_BODY = (
    "<path d='M23 42C8 40 4 22 12 13 14.5 10 18 8 19 10.5' fill='none'"
    " stroke='#000' stroke-width='8.5' stroke-linecap='round'/>"
    "<ellipse cx='29' cy='31.5' rx='8.5' ry='11'/>"
    "<ellipse cx='34' cy='41.8' rx='5.2' ry='2.5'/>"
    "<circle cx='34' cy='16.5' r='7'/>"
    "<ellipse cx='39.5' cy='19' rx='3.2' ry='2.3'/>"
    "<path d='M30 11.5 29.4 5.4 34.8 8.6z'/>")


def n(v):
    """numero compatto: 1.0 -> 1, 1.50 -> 1.5"""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s else "0"


def place(g, px, py, rot, sc):
    t = f"translate({n(px)} {n(py)})"
    if rot:
        t += f" rotate({n(rot)})"
    if sc != 1:
        t += f" scale({n(sc)})"
    t += f" translate({n(-g['c'][0])} {n(-g['c'][1])})"

    if g["kind"] == "scoia":
        return f"<g transform='{t}' fill='#000'>{SCOIA_BODY}</g>"
    inner = f"<path d='{g['d']}'/>"
    if g.get("dots"):
        inner += f"<g stroke-width='{n(g['sw']*2.4)}'><path d='{g['dots']}'/></g>"
    return (f"<g transform='{t}' fill='none' stroke='#000'"
            f" stroke-width='{n(g['sw'])}' stroke-linecap='round'"
            f" stroke-linejoin='round'>{inner}</g>")


def radius(g, sc):
    return sc * math.hypot(*g["h"])


def tile(w, h, items, wrap_y=True):
    """items: lista di (figura, px, py, rot, scala).
    Duplica ai bordi solo le figure che li attraversano, così la tessera
    combacia con le sue copie senza tagliare nulla."""
    out = []
    for g, px, py, rot, sc in items:
        r = radius(g, sc)
        dxs = [0]
        if px - r < 0:   dxs.append(w)
        if px + r > w:   dxs.append(-w)
        dys = [0]
        if wrap_y:
            if py - r < 0: dys.append(h)
            if py + r > h: dys.append(-h)
        for dx in dxs:
            for dy in dys:
                out.append(place(g, px + dx, py + dy, rot, sc))
    body = "".join(out)
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}'>"
            f"{body}</svg>")


def uri(svg):
    """Codifica minima: dentro url("...") vanno protetti solo % e #, e le
    virgolette doppie (che nell'SVG non usiamo). Tutto il resto puo' restare
    letterale, e questo dimezza il peso rispetto alla codifica integrale."""
    s = svg.replace("%", "%25").replace("#", "%23")
    assert '"' not in s and "\n" not in s
    return 'url("data:image/svg+xml,' + s + '")'


def scatter(rng, w, h, glyphs, count, band):
    """Distribuzione a rumore blu (best-candidate di Mitchell): per ogni figura
    provo 40 posizioni e tengo quella piu' lontana da tutte le precedenti.
    Il semplice rifiuto casuale lasciava grumi e buchi; questo no.
    Le distanze girano ai bordi, così la tessera combacia con le sue copie."""
    items = []
    for k in range(count):
        g = glyphs[k % len(glyphs)]
        base = 0.72 if g["kind"] == "scoia" else (1.24 if g is MONTE else 1.0)
        best = None
        for _ in range(90):
            sc = base * rng.uniform(.86, 1.12)
            px = rng.uniform(0, w)
            py = h / 2 + rng.uniform(-3, 3) if band else rng.uniform(0, h)
            rot = rng.uniform(-26, 26)
            if not items:
                best = (1e9, (g, px, py, rot, sc))
                break
            gaps = []
            for og, ox, oy, _, osc in items:
                d = math.hypot(min(abs(px - ox), w - abs(px - ox)),
                               abs(py - oy) if band
                               else min(abs(py - oy), h - abs(py - oy)))
                gap = d - radius(g, sc) - radius(og, osc)
                # due figure dello stesso tipo vicine si notano come una
                # ripetizione: le allontano contando il divario come minore
                if og is g:
                    gap -= 34
                gaps.append(gap)
            vicino = min(gaps)
            if best is None or vicino > best[0]:
                best = (vicino, (g, px, py, rot, sc))
        items.append(best[1])
    return items


# ---- composizione dei motivi --------------------------------------------
MOTIVI = {
    "pigne":      [PIGNA, RAMO],
    "creste":     [MONTE],
    "bosco":      [PIGNA, FUNGO, SCOIA],
    "scoiattolo": [SCOIA, PIGNA, RAMO],
}
# Banda: una tessera sola e larga. Serve per controllare la spaziatura, che con
# piu' livelli indipendenti non si puo' fare: si formavano grumi e vuoti. A 1399
# px il ciclo non si vede su nessuno schermo normale, e la striscia e' alta 44 px.
LARGH_BANDA, FIGURE_BANDA = 1399, 21
# Fondo: tre livelli con periodi primi fra loro. Qui i livelli servono, perche'
# una tessera unica abbastanza grande da coprire l'apertura pesarebbe troppo.
TESS_FONDO, FIGURE_FONDO = [(331, 293), (397, 341), (449, 389)], 4

righe = []
for nome, glyphs in MOTIVI.items():
    rng = random.Random(f"{nome}-banda")
    items = scatter(rng, LARGH_BANDA, 44, glyphs, FIGURE_BANDA, True)
    righe.append(f"  --m-{nome}-sb:\n    "
                 + uri(tile(LARGH_BANDA, 44, items, wrap_y=False)) + ";")

    livelli = []
    for i, (w, h) in enumerate(TESS_FONDO):
        rng = random.Random(f"{nome}-fondo-{i}")
        ruotati = glyphs[i % len(glyphs):] + glyphs[:i % len(glyphs)]
        items = scatter(rng, w, h, ruotati, FIGURE_FONDO, False)
        livelli.append(uri(tile(w, h, items, wrap_y=True)))
    righe.append(f"  --m-{nome}-sf:\n    " + ",\n    ".join(livelli) + ";")

blocco = "\n".join(righe)
open("motivi.css", "w").write(blocco + "\n")

peso = len(blocco)
print(f"scritto motivi.css — {peso} byte ({peso/1024:.1f} KB)")
for r in righe:
    nome = r.strip().split(":")[0]
    print(f"  {nome}: {len(r)} byte")
