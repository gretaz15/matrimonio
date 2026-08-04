# Sito del matrimonio — Ivan & Greta

Sito a pagina singola, senza framework: tre file e una cartella di foto. Si pubblica su GitHub Pages così com'è.

```
index.html    contenuti e testi
style.css     colori, tipografia, impaginazione
script.js     countdown, campi invitati, invio del modulo
img/          le vostre foto (foto-1.jpg, foto-2.jpg, foto-3.jpg)
```

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
| `dataMatrimonio` | Data e ora della cerimonia. **I mesi partono da 0**: giugno è `5`, settembre è `8`. |
| `endpointModulo` | L'indirizzo del punto 2. |
| `tipoEndpoint` | `"formspree"` oppure `"apps-script"`. |
| `maxInvitati` | Massimo di persone per gruppo. Se lo cambi, aggiorna anche le opzioni del menu in `index.html`. |

### `index.html`

Da sostituire, in ordine di comparsa:

- il `<title>` e le due `<meta>` di descrizione e anteprima;
- **Ivan** e **Sofia** nell'apertura, nel monogramma `I&S` della barra e nel fondo pagina;
- la data: sia il testo visibile sia l'attributo `datetime="2027-06-12"`;
- il nome e l'indirizzo della villa;
- l'`src` della mappa: cerca il luogo su Google Maps, prendi le coordinate dall'URL e sostituisci `45.5769,9.5306`. Le stesse coordinate vanno nei tre link sotto la mappa (Google, Apple, Waze) — un cerca-e-sostituisci le prende tutte;
- i quattro riquadri «In auto / In treno / Navetta / Dove dormire»: sono scritti su misura per un posto che non è il vostro, quindi vanno riscritti;
- gli orari del programma;
- nella sezione regali: intestatari, IBAN (in **due posti**: il testo e l'attributo `data-iban` del pulsante) e causale;
- email e telefono nel fondo pagina, e l'indirizzo email che compare nel messaggio d'errore in `script.js`.

### `img/`

Tre foto chiamate `foto-1.jpg`, `foto-2.jpg`, `foto-3.jpg`. Formato verticale, lato lungo intorno a 1600 px, sotto i 400 KB ciascuna: le foto pesanti sono la prima causa di siti lenti sul telefono. Finché non le carichi, al loro posto compare un rettangolo tratteggiato.

Ricordati di aggiornare gli `alt`: descrivono la foto a chi non la vede.

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
