#!/usr/bin/env python3
"""Compone la cornice naturale incompleta dell'apertura.

Non e' un motivo ripetuto: e' una composizione unica, fatta di gruppi ancorati
ai bordi. Ogni gruppo e' un SVG con il suo viewBox; le figure che sporgono dal
viewBox vengono tagliate, ed e' cosi' che si ottengono gli elementi
"parzialmente tagliati dal bordo".

Lo script controlla che nessuna coppia di figure si sovrapponga e stampa i
margini piu' stretti, cosi' le distanze restano verificate e non a occhio.
"""
import math

TRATTO = 1.45  # spessore del tratto, uguale per tutte le figure

# ---- figure: path, centro, mezze-estensioni ------------------------------
PIGNA = dict(nome="pigna", c=(16, 21.75), h=(8.5, 16.25), tipo="linea", d=(
    "M16 5.5v3"
    "M16 8.5c6 3.5 8.5 9 8.5 14.5S20.5 33.5 16 38c-4.5-4.5-8.5-9.5-8.5-15S10 12 16 8.5z"
    "M9 15.5q7 5 14 0M8 21.5q8 5.5 16 0M9.5 27.5q6.5 5 13 0M12 33q4 4 8 0"))

FUNGO = dict(nome="fungo", c=(46.5, 23.75), h=(9.5, 9.75), tipo="linea",
             punti="M43.4 19.8h.01M49.8 18.4h.01M46.6 22.4h.01", d=(
    "M37 25q0-11 9.5-11T56 25M37 25h19M43 25v8.5q3.5 2.6 7 0V25"))

# foglia nuova: lamina a mandorla, nervatura centrale, quattro coppie di
# nervature laterali e un gambo. Serve per i "foglie" della cornice.
FOGLIA = dict(nome="foglia", c=(12, 17), h=(9, 15), tipo="linea", d=(
    "M12 2C19.5 9 21.5 19 12 27.5 2.5 19 4.5 9 12 2z"
    "M12 4V32"
    "M12 9.5 7.2 13.4M12 9.5 16.8 13.4"
    "M12 15 6.4 19.2M12 15 17.6 19.2"
    "M12 20.5 8 23.8M12 20.5 16 23.8"))

RAMO = dict(nome="ramo", c=(48, 23), h=(7, 15), tipo="linea", d=(
    "M48 38V8"
    "M48 12l-4-3M48 12l4-3M48 15.6l-4.8-3.4M48 15.6l4.8-3.4"
    "M48 19.2l-5.4-3.8M48 19.2l5.4-3.8M48 22.8l-6-4.2M48 22.8l6-4.2"
    "M48 26.4l-6.4-4.5M48 26.4l6.4-4.5M48 30l-6.8-4.8M48 30l6.8-4.8"
    "M48 33.6l-7-5M48 33.6l7-5"))

SCOIA = dict(nome="scoiattolo", c=(23.2, 24.65), h=(19.5, 19.7), tipo="piena")

SCOIA_BODY = (
    "<path d='M23 42C8 40 4 22 12 13 14.5 10 18 8 19 10.5' fill='none'"
    " stroke='currentColor' stroke-width='8.5' stroke-linecap='round'/>"
    "<ellipse cx='29' cy='31.5' rx='8.5' ry='11'/>"
    "<ellipse cx='34' cy='41.8' rx='5.2' ry='2.5'/>"
    "<circle cx='34' cy='16.5' r='7'/>"
    "<ellipse cx='39.5' cy='19' rx='3.2' ry='2.3'/>"
    "<path d='M30 11.5 29.4 5.4 34.8 8.6z'/>")


def n(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s else "0"


def raggio(g, sc):
    return sc * math.hypot(*g["h"])


def disegna(g, px, py, rot, sc):
    t = (f"translate({n(px)} {n(py)}) rotate({n(rot)}) scale({n(sc)})"
         f" translate({n(-g['c'][0])} {n(-g['c'][1])})")
    if g["tipo"] == "piena":
        return (f"<g class='cornice__piena' transform='{t}'"
                f" fill='currentColor'>{SCOIA_BODY}</g>")
    # tratto diviso per la scala: cosi' lo spessore a schermo resta uguale
    # per tutte le figure, grandi o piccole. E' quello che rende il segno
    # uniforme e "disegnato", invece di ingrassare con l'ingrandimento.
    sw = TRATTO / sc
    inner = f"<path d='{g['d']}'/>"
    if g.get("punti"):
        inner += f"<g stroke-width='{n(sw*2.3)}'><path d='{g['punti']}'/></g>"
    return (f"<g class='cornice__linea' transform='{t}' fill='none'"
            f" stroke='currentColor' stroke-width='{n(sw)}'"
            f" stroke-linecap='round' stroke-linejoin='round'>{inner}</g>")


def gruppo(classe, w, h, elementi, etichetta):
    """Verifica le distanze e restituisce l'SVG del gruppo."""
    peggiore = None
    for i, (g1, x1, y1, _, s1) in enumerate(elementi):
        for g2, x2, y2, _, s2 in elementi[i + 1:]:
            varco = math.hypot(x1 - x2, y1 - y2) - raggio(g1, s1) - raggio(g2, s2)
            if peggiore is None or varco < peggiore[0]:
                peggiore = (varco, g1["nome"], g2["nome"])
    tagliate = [g["nome"] for g, x, y, _, s in elementi
                if x - raggio(g, s) < 0 or x + raggio(g, s) > w
                or y - raggio(g, s) < 0 or y + raggio(g, s) > h]
    stato = "OK " if peggiore is None or peggiore[0] > 0 else "SOVRAPPOSTE"
    varco = "—" if peggiore is None else f"{peggiore[0]:.1f}px fra {peggiore[1]}/{peggiore[2]}"
    print(f"  {etichetta:<14} {len(elementi)} figure  varco minimo {varco:<34} {stato}")
    print(f"                 tagliate dal bordo: {', '.join(tagliate) or 'nessuna'}")

    corpo = "".join(disegna(*e) for e in elementi)
    return (f"    <svg class=\"cornice__gruppo {classe}\" viewBox=\"0 0 {w} {h}\""
            f" aria-hidden=\"true\" focusable=\"false\">{corpo}</svg>")


# ---- la composizione -----------------------------------------------------
# Peso in basso e a sinistra; a destra pochi dettagli; in alto quasi niente.
print("verifica della composizione\n")

gruppi = []

# angolo in basso a sinistra: il gruppo piu' pesante, l'ancora di tutto
gruppi.append(gruppo("cornice__gruppo--bs", 240, 300, [
    (SCOIA,  96, 250,    5, 1.05),
    (PIGNA,  34, 214,  -16, 1.50),
    (FOGLIA, 38, 292,  -34, 1.70),
    (FUNGO, 160, 284,    7, 1.45),
    (FUNGO, 196, 232,  -14, 0.85),
    (RAMO,  128, 186,   16, 1.25),
    (FOGLIA, 10, 132,   38, 1.15),
    (PIGNA, 214, 296,   22, 0.95),
], "basso-sx"))

# angolo in basso a destra: piu' leggero
gruppi.append(gruppo("cornice__gruppo--bd", 210, 150, [
    (FOGLIA,  40, 128, -22, 1.30),
    (PIGNA,  112, 112,  12, 1.15),
    (FUNGO,  176, 136,  -8, 1.10),
    (FOGLIA, 204,  96,  44, 0.80),
], "basso-dx"))

# bordo sinistro a mezza altezza, tagliato dal bordo
gruppi.append(gruppo("cornice__gruppo--sx", 90, 170, [
    (RAMO,  14,  46, -24, 1.10),
    (FUNGO, 44, 118,  10, 0.95),
    (PIGNA,  8, 150,  28, 1.00),
], "sinistra"))

# lo scoiattolo che entra da destra
gruppi.append(gruppo("cornice__gruppo--dx", 80, 90, [
    (SCOIA, 46, 46, -8, 1.25),
], "destra"))

# in alto: due sole figure, appese, tagliate dal bordo superiore
gruppi.append(gruppo("cornice__gruppo--alto", 110, 70, [
    (FOGLIA, 30, 14, 152, 1.05),
    (PIGNA,  84,  8, 196, 0.80),
], "alto"))

blocco = ('  <div class="cornice" aria-hidden="true">\n'
          + "\n".join(gruppi) + "\n  </div>")
open("cornice.html", "w").write(blocco + "\n")
tot = sum(1 for g in gruppi)
print(f"\nscritto cornice.html — {len(blocco)} byte, {tot} gruppi")
