# Sito del matrimonio — Ivan & Greta

Sito a pagina singola, senza framework: tre file e una cartella di foto. Si pubblica su GitHub Pages così com'è.

```
index.html    contenuti e testi
style.css     colori, tipografia, impaginazione
script.js     countdown, campi invitati, invio del modulo
img/          le vostre foto (foto-1.jpeg, foto-2.jpeg, foto-3.jpeg)
```

Più due file che il sito non usa: `strumenti-motivi.py` rigenera i motivi
decorativi sparsi e `strumenti-cornice.py` la cornice dell'apertura. Servono
solo se vuoi cambiarne densità o disposizione, e si possono cancellare.

---

## 1. Pubblicare su GitHub Pages

1. Crea un repository nuovo. Due possibilità:
   - **`tuonome.github.io`** → il sito sta su `https://tuonome.github.io` (un solo sito per account);
   - **`matrimonio`** → il sito sta su `https://tuonome.github.io/matrimonio/` (puoi averne quanti vuoi).
2. Carica i file mantenendo la struttura (`index.html` deve stare nella radice del repository).
3. Vai su **Settings → Pages**, alla voce *Source* scegli **Deploy from a branch**, branch `main`, cartella `/ (root)`, salva.
4. Dopo un minuto il sito è online. Ogni `push` successivo lo aggiorna.

Da riga di comando:

```bash
git init
git add .
git commit -m "Sito del matrimonio"
git branch -M main
git remote add origin https://github.com/TUONOME/matrimonio.git
git push -u origin main
```

**Dominio personalizzato** (per esempio `ivanegreta.it`): in *Settings → Pages → Custom domain* inserisci il dominio, poi dal pannello del tuo registrar crea quattro record `A` verso `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`. Lascia attiva l'opzione *Enforce HTTPS*.

---

## 2. Modulo di conferma

GitHub Pages serve solo file statici: non può ricevere dati da sé. Il modulo funziona già, gli serve solo un indirizzo a cui consegnare le risposte. Scegli una delle due strade e incollala in `script.js`, alla voce `endpointModulo`.

### Formspree — la via rapida (10 minuti)

1. Registrati su [formspree.io](https://formspree.io) (il piano gratuito copre 50 invii al mese).
2. Crea un nuovo form e copia l'indirizzo che ti viene mostrato, del tipo `https://formspree.io/f/abcdwxyz`.
3. In `script.js`:

```js
endpointModulo: "https://formspree.io/f/abcdwxyz",
tipoEndpoint: "formspree",
```

Ogni conferma arriva per email con tutti i campi, invitato per invitato.

### Google Sheets — le risposte in tabella

Visto che lavori già con Sheets, questa è probabilmente la strada che preferisci: le conferme finiscono in un foglio pronto da filtrare per allergie.

1. Crea un foglio Google e apri **Estensioni → Apps Script**.
2. Incolla:

```js
function doPost(e) {
  const foglio = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  const dati = e.parameter;
  if (foglio.getLastRow() === 0) {
    foglio.appendRow(["Ricevuto il", ...Object.keys(dati)]);
  }
  foglio.appendRow([new Date(), ...Object.values(dati)]);
  return ContentService.createTextOutput("ok");
}
```

3. **Deploy → New deployment → Web app**, *Execute as* «Me», *Who has access* «Anyone», e copia l'URL `https://script.google.com/macros/s/…/exec`.
4. In `script.js`:

```js
endpointModulo: "https://script.google.com/macros/s/IL_TUO_ID/exec",
tipoEndpoint: "apps-script",
```

Le colonne cambiano a seconda di quanti invitati indica ogni gruppo: normale, il foglio si allarga da solo.

### Come è resa obbligatoria l'allergia

Per ogni invitato indicato nel menu «Quante persone» compare una scheda con nome e allergie, entrambi obbligatori. Chi prova a inviare lasciandoli vuoti riceve un messaggio sotto al campo e la pagina lo porta lì. I pulsanti «Nessuna», «Glutine», «Lattosio»… riempiono il campo con un tocco, così nessuno è tentato di saltarlo — ma una risposta esplicita resta necessaria.

---

## 3. Cosa cambiare nei file

### `script.js` — il blocco `CONFIG` in cima

| Voce | A cosa serve |
|---|---|
| `dataMatrimonio` | Data e ora della cerimonia. **I mesi partono da 0**: luglio è `6`, settembre è `8`. |
| `endpointModulo` | L'indirizzo del punto 2. |
| `tipoEndpoint` | `"formspree"` oppure `"apps-script"`. |
| `maxInvitati` | Massimo di persone per gruppo. Se lo cambi, aggiorna anche le opzioni del menu in `index.html`. |

### `index.html`

Da sostituire, in ordine di comparsa:

- il `<title>` e le due `<meta>` di descrizione e anteprima;
- i nomi nell'apertura, nel monogramma `I&G` della barra e nel fondo pagina;
- la data: sia il testo visibile sia l'attributo `datetime="2027-07-24"`;
- i due blocchi `.luogo` della sezione «I luoghi», uno per sede: titolo, orario, indirizzo, mappa e i tre pulsanti di navigazione. Le mappe e i pulsanti funzionano **per indirizzo**, non per coordinate: dentro gli URL c'è l'indirizzo scritto per esteso, quindi per cambiare sede basta sostituire quello (ricordando di scriverlo in forma URL: spazio `%20` nell'`src` dell'iframe, `+` nei link, `à` `%C3%A0`). Se una sede non venisse trovata da Maps, ripiega sulle coordinate: `?q=46.1234,8.4567`;
- i tre riquadri della sezione «Dove parcheggiare». Questi funzionano **per coordinate**, non per indirizzo, perché un piazzale di montagna spesso non ha un civico: su Google Maps da computer fai click destro sul punto esatto, la prima voce del menu sono le coordinate, e le incolli dopo `destination=`. Per aggiungere o togliere un parcheggio, duplica o cancella un intero blocco `<article class="parcheggio">`: la griglia si riadatta da sola;
- i cinque riquadri «In auto / In treno / Fra i due luoghi / Dove dormire / Cosa portare»;
- gli orari del programma, che vanno tenuti d'accordo con `dataMatrimonio` in `script.js`: il countdown punta all'ora della cerimonia;
- nella sezione regali: intestatari, IBAN (in **due posti**: il testo e l'attributo `data-iban` del pulsante) e causale;
- email e telefono nel fondo pagina, e l'indirizzo email che compare nel messaggio d'errore in `script.js`.

### `style.css` — tema e motivo decorativo

Il tema è **bosco di montagna**. Il motivo decorativo si cambia da `index.html`,
nella classe del `<body>`, e si compone di due parole.

La prima dice **quali figure**:

| Prima parola | Cosa disegna |
|---|---|
| `tema-pigne` | pigne e rami d'abete |
| `tema-creste` | creste di montagna innevate |
| `tema-bosco` | pigne, funghi e scoiattoli |
| `tema-scoiattolo` | scoiattoli, pigne e rami, più la mascotte nel monogramma, in fondo al programma e nel fondo pagina |

La seconda dice **come sono disposte**:

| Seconda parola | Disposizione |
|---|---|
| *niente* | sparse e irregolari, poco dense *(predefinito)* |
| `regolare` | la griglia fitta e ordinata della prima versione |

Una terza parola facoltativa, `filigrana`, rimette la texture di sfondo
nell'apertura al posto della cornice. Vedi «La cornice dell'apertura».

Quindi `class="tema-bosco"` dà il bosco sparso e `class="tema-bosco regolare"`
lo stesso motivo a griglia.

Il motivo compare in due punti: le bande divisorie fra le sezioni e la filigrana
dietro l'apertura. Sono disegni a una tinta usati come maschera CSS, quindi il
colore arriva dalla palette e non va toccato dentro l'SVG.

**Come è fatta la casualità.** Una maschera CSS si ripete per forza, quindi non
esiste il vero caso: è costruito in due modi diversi.

- La **banda** usa una sola tessera larga 1399 px, con le figure distribuite a
  rumore blu — cioè scegliendo ogni posizione fra molte candidate e tenendo la
  più lontana dalle altre. Senza questo passaggio venivano grumi e vuoti. A
  quella larghezza il ciclo non entra in uno schermo.
- Il **fondo** dell'apertura sovrappone tre livelli di maschera con periodi
  primi fra loro (331, 397 e 449 px). Il disegno complessivo si ripete solo al
  loro minimo comune multiplo, cioè oltre 57 milioni di px: in pratica mai.

Le tessere sparse sono generate figura per figura da uno script, non scritte a
mano: se vuoi cambiarne densità o disposizione conviene rigenerarle. Pesano
50 KB in chiaro ma circa 3 KB compresse, che è quello che viaggia in rete.

I colori stanno tutti in `:root`, in cima al file:

| Variabile | Uso |
|---|---|
| `--bosco-scuro` | fondi scuri: apertura e fondo pagina. Se lo cambi, cambia anche il `<meta name="theme-color">` in `index.html` |
| `--bosco` | colore principale: bottoni, link, titoli piccoli |
| `--nebbia` | il fondo carta della pagina |
| `--oro` | oro larice, usato **solo** sui fondi scuri |
| `--pigna` | bruno pigna, usato **solo** sui fondi chiari |
| `--muschio` | verde muschio, per i messaggi di conferma |

`--oro` e `--pigna` sono due accenti separati per una ragione: l'oro su fondo
chiaro non ha contrasto sufficiente e il bruno su fondo scuro nemmeno. Se ne usi
uno al posto dell'altro, il testo diventa poco leggibile.

### `img/` e il carosello

Le foto stanno in un carosello, non in una griglia, e **non vengono ritagliate**:
ognuna entra per intero in un riquadro quadrato, quindi il formato è libero e
si possono mescliare orizzontali e verticali. Le fasce color carta che restano
ai lati (o sopra e sotto, per le orizzontali) sono volute.

Il quadrato è il compromesso con meno spazio buttato: con un riquadro verticale
una foto orizzontale perderebbe il 40% di altezza, e viceversa.

Per cambiare foto, in ogni `<li class="diapositiva">` di `index.html` servono
tre cose:

- **`src`** — attenzione all'estensione: i file attuali sono `.jpeg`, non `.jpg`.
  Se non corrispondono, la foto non compare e non c'è nessun messaggio d'errore;
- **`width` e `height`** — le dimensioni vere in pixel. Non servono a
  dimensionare niente: servono al browser per riservare lo spazio prima che la
  foto arrivi, così la pagina non salta mentre si carica;
- **`alt`** — descrive la foto a chi non la vede.

Per aggiungerne o togliere, duplica o cancella un `<li>`: le frecce e i puntini
si adeguano da soli, li costruisce `script.js` contando le diapositive.

Sul peso: stai sotto i 400 KB per foto. Le foto pesanti sono la prima causa di
siti lenti sul telefono, ed è da telefono che le guarderanno quasi tutti.

### Lo sfondo dell'apertura

L'apertura ha una fotografia di bosco (`img/sfondo.jpg`) più un **velo verde
scuro**. Il velo non è decorativo, è necessario: dentro la zona del titolo la
fotografia va da 0.00 a 0.997 di luminanza, quindi il testo bianco sul sentiero
chiaro arriverebbe a 1.0:1, cioè invisibile.

La forma del velo segue la fotografia. È un'ellisse alta e stretta, quasi opaca
nella colonna centrale — che è insieme la parte più chiara dell'immagine e quella
dove cade il testo — e molto più leggera ai lati, dove stanno funghi, felci e
scoiattoli, che così restano visibili. Il centro della foto è sfocato e vuoto,
quindi coprirlo non toglie niente.

Sotto i 620 px il ritaglio si sposta al 26% invece che al centro: su uno schermo
verticale `cover` mostrerebbe solo la striscia centrale, cioè il sentiero vuoto,
e sotto il velo resterebbe un verde quasi piatto.

Due dettagli che servono a far tornare i contrasti, da non togliere:

- la targa della data ha un suo velo al 55%. Il nome del luogo è in oro e
  piccolo, ed era l'unica scritta che non arrivava a 4.5:1;
- le etichette del countdown sono bianche all'88% e non al 64%. Sul verde pieno
  il 64% bastava, sulla fotografia scendeva a 2.8:1.

**L'apertura è alta quanto lo schermo** (`min-height: 100svh`) e il contenuto sta
al centro, così il pulsante di conferma si vede sempre senza scorrere. È
`min-height` e non `height` perché su uno schermo molto basso l'apertura deve
poter crescere invece di tagliare il pulsante. Per farci stare tutto:

- i nomi si dimensionano su `min(13vw, 13vh)`, quindi rimpiccioliscono anche in
  base all'**altezza**: da soli erano la voce che mangiava lo spazio del pulsante;
- sotto gli 860 px di altezza il ritmo verticale si stringe, e sotto i 600 si
  riducono anche il corpo delle cifre e il pulsante.

Verificato: entra in una schermata da circa 490 px di altezza in su. Più in basso
di così (telefono in orizzontale) scorre, che è il comportamento giusto.

### I tre file dello sfondo

| File | Peso | Chi lo usa |
|---|---|---|
| `sfondo.png` | 9,9 MB | **nessuno.** È il tuo originale, resta lì intatto |
| `sfondo.jpg` | 620 KB | schermi sopra i 620 px (2816 px, qualità 40) |
| `sfondo-telefono.jpg` | 159 KB | schermi fino a 620 px (1200 px, qualità 45) |

La risoluzione conta più della qualità. Su uno schermo retina l'immagine viene
ingrandita per coprire l'apertura: una versione da 1800 px risultava
**visibilmente sfocata**, mentre a 2816 px è nitida. La qualità invece può stare
bassa, perché il velo copre gli artefatti. Il telefono ha un file suo perché non
gli servono 2816 px e sono 460 KB in meno da scaricare.

Per rigenerarli:

```
sips -Z 2816 -s format jpeg -s formatOptions 40 img/sfondo.png --out img/sfondo.jpg
sips -Z 1200 -s format jpeg -s formatOptions 45 img/sfondo.png --out img/sfondo-telefono.jpg
```

### La cornice dell'apertura

Attorno al titolo c'è una cornice incompleta di funghi, foglie, pigne e
scoiattoli, con più peso in basso e a sinistra e un centro lasciato libero.

Non è un motivo ripetuto ma una composizione unica, divisa in cinque gruppi
ancorati ai bordi (`cornice__gruppo--bs`, `--bd`, `--sx`, `--dx`, `--alto`).
Ogni gruppo è un SVG con il suo `viewBox`: le figure che sporgono dal viewBox
vengono tagliate, ed è così che alcune sembrano entrare da fuori. Essendo
gruppi separati e non un'immagine unica, non si stirano a nessuna larghezza:
si allontanano fra loro sugli schermi larghi, che è esattamente ciò che serve
a una cornice che deve sembrare incompleta.

Sotto i 560 px restano solo i due gruppi in basso, altrimenti ruberebbero
spazio al titolo.

`strumenti-cornice.py` rigenera la composizione. Le posizioni sono in fondo al
file, come liste di `(figura, x, y, rotazione, scala)`; lo script verifica che
nessuna coppia si sovrapponga e stampa il varco più stretto, così le distanze
restano controllate e non a occhio.

Di norma l'apertura ha la cornice e nessuna filigrana, perché il centro va
lasciato pulito. Se preferisci la vecchia texture di sfondo, aggiungi la parola
`filigrana` alla classe del `<body>`.

---

## 4. Prima di mandare il link

- Aprilo sul telefono: la maggior parte degli invitati lo vedrà da WhatsApp.
- Prova una conferma vera, con due o tre persone, e controlla che arrivi tutto.
- Prova a inviare lasciando vuote le allergie: deve bloccarti.
- Verifica che i link della mappa aprano il posto giusto.
- Controlla l'IBAN carattere per carattere, e poi fallo ricontrollare da qualcun altro.

Una nota sull'IBAN: pubblicandolo su una pagina aperta lo rendi visibile a chiunque. Non è un rischio per il conto — con l'IBAN si può solo ricevere, non prelevare — ma è un dato che finisce nei motori di ricerca. Se preferisci tenerlo riservato, un'alternativa è togliere il codice dalla pagina e lasciare una riga tipo «scriveteci e ve lo mandiamo».

---

## 5. Note tecniche

- Nessuna dipendenza: solo i font di Google (Fraunces e Manrope).
- Funziona senza JavaScript, tranne countdown e modulo.
- Navigazione da tastiera, contrasti verificati, `prefers-reduced-motion` rispettato.
- La mappa è l'incorporamento pubblico di Google Maps: non serve alcuna chiave API.
