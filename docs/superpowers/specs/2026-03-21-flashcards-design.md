# FlashCards — Design Specification
**Datum:** 2026-03-21
**Stav:** Draft

---

## 1. Přehled

Webová aplikace pro učení pomocí flashcards s algoritmem spaced repetition (SM-2). Běží v Dockeru, přístupná přes prohlížeč na desktopu i mobilu. Primární use-case: učení cizích jazyků.

---

## 2. Tech Stack

| Vrstva | Technologie |
|--------|-------------|
| Frontend | Vue.js 3 (SPA) + Vite |
| Backend | FastAPI (Python) |
| Databáze | PostgreSQL |
| Webserver | Nginx (reverse proxy + statické soubory) |
| Autentizace | Authelia (SSO + 2FA proxy) |
| Překlad | LibreTranslate (self-hosted) |
| Deployment | Docker Compose |

---

## 3. Architektura

```
Uživatel (prohlížeč)
    ↓ HTTPS
Authelia (SSO + 2FA)
    ↓ ověřený request
Nginx
    ├── /          → Vue.js SPA (statické soubory)
    └── /api/*     → FastAPI backend
                        ├── PostgreSQL
                        ├── LibreTranslate
                        └── Media volume (obrázky, audio)
```

### Docker Compose služby
- `authelia` — autentizační proxy (konfigurována zvlášť mimo `.env`, má vlastní config soubory)
- `nginx` — webserver + frontend
- `backend` — FastAPI aplikace
- `db` — PostgreSQL
- `libretranslate` — překladač

Konfigurace přes `.env` soubor. Media soubory v pojmenovaném Docker volume.

---

## 4. Datový model

### User
```
id              UUID PK
username        TEXT (z Authelia hlavičky)
email           TEXT
created_at      TIMESTAMP
```

### Language
```
id              UUID PK
user_id         UUID FK → User
name            TEXT (např. "Angličtina")
emoji           TEXT (např. "🇬🇧")
direction_mode  ENUM: front_to_back | back_to_front | random  ← výchozí pro lekce
target_lang     TEXT (ISO 639-1, např. "cs") ← pro LibreTranslate
order           INTEGER
created_at      TIMESTAMP
```

### Lesson
```
id              UUID PK
language_id     UUID FK → Language
name            TEXT (např. "Lekce 1")
direction_mode  ENUM: front_to_back | back_to_front | random | inherit  ← inherit = použij Language.direction_mode
order           INTEGER
created_at      TIMESTAMP
```

### Card
```
id              UUID PK
lesson_id       UUID FK → Lesson
created_at      TIMESTAMP
```

*Poznámka: Card nemá vlastní direction_mode — směr určuje Lesson (nebo Language přes inherit). V1 předpokládá právě dva CardField záznamy (front + back), vynuceno backendovou validací při vytvoření i úpravě karty.*

### CardField
```
id              UUID PK
card_id         UUID FK → Card
label           TEXT — "front" nebo "back" (v1)
content         TEXT
order           INTEGER
is_tested       BOOLEAN DEFAULT true   ← připraveno pro v2 dimenze
image_path      TEXT nullable          ← relativní cesta: {card_id}/{label}.{ext}
audio_path      TEXT nullable          ← relativní cesta: {card_id}/{label}.{ext}
```

*Struktura je připravena pro vícerozměrné karty v v2 bez migrace dat.*

### CardProgress
```
id              UUID PK
card_id         UUID FK → Card
user_id         UUID FK → User
direction       ENUM: front_to_back | back_to_front
interval        INTEGER (dny)
ease_factor     FLOAT (SM-2, výchozí 2.5)
repetitions     INTEGER
due_date        DATE
last_reviewed   TIMESTAMP
is_learned      BOOLEAN DEFAULT false
```

*SM-2 progress se sleduje zvlášť pro každý směr. Karta je zobrazena jako "naučená" (zelené číslo) až když jsou naučeny oba aktivní směry.*

*Reset progressu: smazání CardProgress záznamů pro danou lekci nebo jazyk — karty samotné zůstanou. Reset je nevratný, uživatel je před ním varován potvrzovacím dialogem.*

---

## 5. SM-2 Algoritmus

Standardní implementace SM-2:

- **Hodnocení po odhalení:** 0 (Nevím) / 3 (Těžké) / 4 (Umím) / 5 (Lehké)
- **První review:** interval = 1 den, repetitions = 1
- **Hodnocení < 3:** interval reset na 1 den, repetitions = 0, ease_factor se nemění
- **Hodnocení ≥ 3:** `new_interval = max(1, round(interval × ease_factor))`, ease_factor se upravuje standardním SM-2 vzorcem, minimum ease_factor = 1.3
- **is_learned = true** pokud interval ≥ 21 dní (konfigurovatelné přes `SM2_LEARNED_THRESHOLD_DAYS`)

*"Naučená" karta (zelené číslo v UI): závisí na direction_mode lekce — front_to_back: pouze front→back musí mít is_learned=true; back_to_front: pouze back→front; random: oba směry.*

---

## 6. Směr zkoušení

Hierarchie: **Lesson.direction_mode** přebíjí Language. Pokud je Lesson nastaven na `inherit`, použije se Language.direction_mode.

- `front_to_back` — přední → zadní (default)
- `back_to_front` — zadní → přední
- `random` — náhodně při každém zobrazení karty (vytvoří CardProgress pro oba směry)

CardProgress záznamy jsou oddělené pro každý směr. Při `random` se pro danou session náhodně vybere jeden směr a vytvoří/aktualizuje příslušný CardProgress záznam.

---

## 7. UI Layout

### Desktop (šířkový viewport)
- **Persistentní sidebar** vlevo (180px)
  - Logo + ikona uživatele vpravo nahoře
  - Hierarchický strom: Jazyk → Lekce
  - U každého jazyka/lekce: `zelené/celkové` číslo karet
  - Zaškrtávátka u lekcí pro výběr kombinace k procvičování — resetují se při každém načtení stránky
  - Tlačítko "Začít vybrané (N lekcí)"
  - Kontextové menu (⋯) u jazyka/lekce: přejmenovat, reset progressu, smazat
  - Navigace dole: Statistiky, Nastavení
- **Hlavní oblast** — karta + hodnoticí tlačítka

### Mobil (výškový viewport)
- **Top bar:** hamburger `☰` vlevo, název aplikace uprostřed, ikona uživatele vpravo
- **Hamburger menu** — vysouvací panel s hierarchií lekcí (stejná funkce jako desktop sidebar)
- **Fullscreen karta** — tap = odhalení zadní strany
- **4 tlačítka hodnocení** — zobrazí se až PO odhalení zadní strany (před odhalením jsou skryta)

### Karta při učení
1. Zobrazí se přední strana (+ audio tlačítko pokud existuje)
2. Uživatel klikne/tapne → odhalí se zadní strana (+ obrázek, audio)
3. Teprve po odhalení se zobrazí hodnoticí tlačítka: Nevím / Těžké / Umím / Lehké
4. Po hodnocení: karta se odsune animací (doleva = Nevím/Těžké, doprava = Umím/Lehké), zobrazí se další
5. **Tlačítko Zpět** — pravý horní roh učební plochy, vrátí až 5 kroků zpět v historii session; vrací i SM-2 hodnocení (CardProgress se revertuje na předchozí stav)

### Session persistence
- Průběžně se ukládá do localStorage: seznam lesson_id + aktuální pozice v session + pořadí karet
- Po reloadu stránky uprostřed testu se zobrazí dialog: "Pokračovat v session?" / "Začít znovu"
- "Začít znovu" smaže uložený stav a vrátí na Dashboard
- Pokud karty nebo lekce byly mezitím smazány, přeskočí se — session pokračuje se zbývajícími kartami
- Výběr lekcí (checkboxy) se při reloadu resetuje — uživatel vybírá vždy znovu

---

## 8. Obrazovky

| # | Název | Popis |
|---|-------|-------|
| 1 | Dashboard | Přehled jazyků a lekcí, počty karet, výběr co procvičovat |
| 2 | Učení | SM-2 session — zobrazení a hodnocení karet |
| 3 | Seznam karet | Tabulkový pohled na karty lekce, kliknutím otevřeš editor |
| 4 | Editor karty | Detail jedné karty — přední/zadní, obrázek, audio, překlad |
| 5 | Import | Drag & drop CSV nebo JSON |
| 6 | Statistiky | Streak, přesnost, grafy per jazyk/lekce |

---

## 9. Import/Export

### CSV formát
```
front,back
Hello,Ahoj
Cat,Kočka
```

### JSON formát
```json
[
  {"front": "Hello", "back": "Ahoj"},
  {"front": "Cat", "back": "Kočka"}
]
```

Import cílí do konkrétní lekce. Duplicity se detekují podle `front` pole (case-sensitive, trim whitespace):
- Pokud duplicita nalezena: záznam se **přeskočí** (existující karta zůstane beze změny)
- Po importu se zobrazí shrnutí: N importováno, M přeskočeno (duplicity)

---

## 10. Media (obrázky + audio)

- Upload přes editor karty (nebo drag & drop)
- Uloženo v Docker volume, přístupné přes Nginx `/media/*`
- Podporované formáty: PNG, JPG, WebP (obrázky); MP3, OGG (audio)
- Max velikost: 5 MB per soubor (konfigurovatelné)
- **Pojmenování souborů:** `{card_id}/{label}.{ext}` — např. `a1b2c3.../front.jpg`. Při nahrání nového souboru se starý přepíše. Kolize mezi uživateli nehrozí díky UUID card_id.
- **Smazání karty:** media soubory se smažou okamžitě spolu s kartou.

---

## 11. Překlad (LibreTranslate)

- **Auto-překlad:** pole zadní strany se vyplní automaticky ~1s po přestání psát do přední strany (debounce)
- Uživatel může překlad upravit před uložením
- Zdrojový jazyk: automatická detekce (`source: "auto"`)
- Cílový jazyk: `Language.target_lang` (ISO 639-1, např. `"cs"` pro češtinu), konfigurovatelné per jazyk
- **Chyba LibreTranslate:** pole zadní strany zobrazí šedý placeholder "Překlad není dostupný" — mizí při kliknutí, pole je editovatelné

---

## 12. Autentizace (Authelia)

- Authelia stojí před celou aplikací jako reverse proxy, konfigurována zvlášť (vlastní config soubory, mimo scope tohoto projektu)
- Po úspěšném přihlášení předává Authelia hlavičku `Remote-User` (username) a `Remote-Email`
- Backend vytvoří uživatele při **každém requestu** pokud neexistuje (upsert podle username). Pokud `Remote-User` hlavička chybí, backend vrátí 401. `Remote-Email` je volitelný (email v DB nullable).
- Aplikace sama neřeší hesla ani session — vše zajišťuje Authelia

---

## 13. Co je odloženo do v2

- **Vícerozměrné karty** — více než front/back polí (výslovnost, kanji, psaní...), přepínání dimenzí per lekce. Datový model (`CardField.is_tested`) je připraven.
- **Archivace karet** — dočasné skrytí karty bez smazání (šedá, zatržítko "použít kartu")
- **Mobilní PWA / offline režim**
- **Sdílení decků mezi uživateli**
- **Text-to-speech** (automatické generování audia)

---

## 14. Konfigurace (.env)

```env
POSTGRES_DB=flashcards
POSTGRES_USER=flashcards
POSTGRES_PASSWORD=...
LIBRETRANSLATE_URL=http://libretranslate:5000
MEDIA_MAX_SIZE_MB=5
SM2_LEARNED_THRESHOLD_DAYS=21
```

*Poznámka: Authelia má vlastní konfigurační soubory (configuration.yml, users_database.yml) mimo tento .env.*
