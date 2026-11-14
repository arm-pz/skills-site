# Tannery Row Cycles (Leeds independent bike workshop) — one-shot build prompt

This is a single, self-contained prompt. Build the whole site from it. Do not ask questions, do not substitute assets, do not add files or dependencies, and do not stop until the three files below exist and the page opens with no console errors.

## What this project is

A one-page website for an independent bike repair workshop in Leeds, England. "Tannery Row Cycles" is a concept shop: its name, address, phone number, email, opening hours and prices are all illustrative and are labelled that way on the page. The audience is Leeds commuters, students and weekend riders who need a bike fixed and want to know three things fast: are you open, what will it cost, how do I book. The page has one job: get the visitor to build a job tag (choose a service and any extra repairs), see the price, and send a booking request for a drop-off day.

## How the page works

1. **Open-now status.** A line in the hero says whether the shop is open right now, computed in the Europe/London time zone (not the visitor's), and if closed, when it next opens. The opening-hours table in the HTML is the single source of truth: each `<tr>` carries `data-day` (0 = Sunday … 6 = Saturday) and, when open, `data-open` and `data-close` as `HH:MM`. The script reads those attributes. Today's row is highlighted.
2. **The job tag (signature mechanic).** Bike workshops write a paper job tag for every bike that comes in. The services section is a tag-builder: one service package (radio buttons) plus extra single jobs (number inputs, 0–4). A kraft-card "job tag" beside the form lists the chosen lines and a running total in pounds, with the words "plus parts, agreed with you before fitting". The tag updates on every input change. The same tag text is what goes into the booking email.
3. **Booking.** The booking form collects name, email, bike type, drop-off date and notes. The date must be today or later and must fall on an open day (Tuesday to Saturday); otherwise the field shows "We're closed that day. Pick Tuesday to Saturday." and the form does not send. At least one package or extra must be chosen. On a valid submit the page opens the visitor's email app with a pre-filled `mailto:` containing the job tag, and shows a status line with the phone number as a fallback. There is no backend.
4. **Show, don't claim.** No ratings, reviews, "years of experience", customer logos or awards. The only facts are the hours, the prices, the vocabulary of the trade and the booking steps.

## Build this exactly

- Reproduce the three files below character for character. Do not "improve", refactor, rename classes or reformat.
- No frameworks, no libraries, no build step, no extra files (no favicon file, no images, no `package.json`).
- Do not replace the copy. Do not add testimonials, a blog, a pricing-tier card grid, stock photography or an icon set.
- Do not change the illustrative prices, hours, phone number or email.
- Do not add fonts beyond the two Google Fonts named below.

## Tech stack

Plain HTML, CSS and JavaScript. No dependencies. Files: `index.html`, `styles.css`, `main.js`. Open `index.html` directly, or serve the folder with `python3 -m http.server 8080` and visit `http://localhost:8080`. The only external request is one Google Fonts stylesheet (Barlow Condensed 700 and Barlow 400/600); if offline, the system fallbacks in the CSS apply.

## Assets

Everything is code-native. The bicycle in the hero is inline SVG drawn in `index.html`. The kraft-paper texture is a CSS gradient. There are no image files to supply.

## Steps to build

1. Create an empty folder and the three files from the File sections below, exactly as written.
2. Open `index.html` in a browser, or run the `python3 -m http.server 8080` command above.
3. Done when: the page loads with no console errors; the hero shows an open or closed line; the tag total changes when you change a package or an extra; submitting the empty-date form shows an error and focuses the date field; submitting a valid form opens an email draft.

## File: `index.html`

```html
<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tannery Row Cycles · Bike repair in Leeds · Hours, prices, booking</title>
  <meta name="description" content="Independent bike repair workshop in Leeds (concept). Opening hours, service prices and how to book a drop-off.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700&family=Barlow:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <a class="skip" href="#services">Skip to services and prices</a>

  <header class="top">
    <a class="brand" href="#top">Tannery Row Cycles</a>
    <nav aria-label="Main">
      <a href="#hours">Hours</a>
      <a href="#services">Services &amp; prices</a>
      <a href="#book">Book</a>
    </nav>
  </header>

  <main id="top">
    <section class="hero">
      <div class="hero-copy">
        <p class="stamp">Independent bike workshop · Leeds</p>
        <h1>Bikes mended properly. Quoted before we pick up a spanner.</h1>
        <p class="lede">Punctures to full overhauls, for commuters, students and weekend riders. Drop off Tuesday to Saturday; we ring you with the price before any work beyond your tag.</p>
        <p class="status" id="open-status" role="status">Checking opening hours…</p>
        <p><a class="btn" href="#services">Build your job tag</a></p>
      </div>
      <svg class="bike" viewBox="0 0 320 160" aria-hidden="true" focusable="false">
        <g fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="70" cy="100" r="42"/>
          <circle cx="250" cy="100" r="42"/>
          <path d="M70 100 L135 100 L120 48 Z"/>
          <path d="M135 100 L215 56 L120 48"/>
          <path d="M215 56 L250 100"/>
          <path d="M120 48 L116 36 M106 36 L128 36"/>
          <path d="M215 56 L210 40 L232 40"/>
          <path d="M135 100 L128 114 M135 100 L142 86" stroke-width="4"/>
        </g>
        <g fill="currentColor">
          <circle cx="70" cy="100" r="5"/>
          <circle cx="250" cy="100" r="5"/>
          <circle cx="135" cy="100" r="7"/>
        </g>
        <g fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 5" opacity=".55">
          <circle cx="70" cy="100" r="33"/>
          <circle cx="250" cy="100" r="33"/>
        </g>
      </svg>
    </section>

    <section class="panel" id="hours" aria-labelledby="hours-h">
      <h2 id="hours-h">Opening hours</h2>
      <div class="hours-wrap">
        <table class="hours">
          <caption class="sr">Opening hours by day (UK time)</caption>
          <tbody>
            <tr data-day="1"><th scope="row">Monday</th><td>Closed</td></tr>
            <tr data-day="2" data-open="08:00" data-close="18:00"><th scope="row">Tuesday</th><td>08:00 – 18:00</td></tr>
            <tr data-day="3" data-open="08:00" data-close="18:00"><th scope="row">Wednesday</th><td>08:00 – 18:00</td></tr>
            <tr data-day="4" data-open="08:00" data-close="18:00"><th scope="row">Thursday</th><td>08:00 – 18:00</td></tr>
            <tr data-day="5" data-open="08:00" data-close="18:00"><th scope="row">Friday</th><td>08:00 – 18:00</td></tr>
            <tr data-day="6" data-open="09:00" data-close="16:00"><th scope="row">Saturday</th><td>09:00 – 16:00</td></tr>
            <tr data-day="0"><th scope="row">Sunday</th><td>Closed</td></tr>
          </tbody>
        </table>
        <div class="where">
          <h3>Find the workshop</h3>
          <p>Unit 4, Tannery Row Yard<br>Kirkstall, Leeds</p>
          <p>Phone <a href="tel:+441134960142">0113 496 0142</a></p>
          <p class="fine">Early drop-off from 08:00 for commuters. Concept shop: name, address, hours and prices are illustrative.</p>
        </div>
      </div>
    </section>

    <section class="panel" id="services" aria-labelledby="services-h">
      <h2 id="services-h">Services &amp; prices</h2>
      <p class="intro">Pick a service, add any single jobs, and the tag on the right adds it up. Labour prices are illustrative and include VAT; parts are extra and agreed with you before fitting.</p>

      <div class="builder">
        <form id="book" class="card" novalidate>
          <fieldset>
            <legend>1 · Service package</legend>
            <label class="opt"><input type="radio" name="pkg" value="none" data-name="Repairs only" data-price="0"><span class="opt-t">Repairs only<small>No package, just the jobs below</small></span><span class="price">£0</span></label>
            <label class="opt"><input type="radio" name="pkg" value="safety" data-name="Safety check" data-price="25"><span class="opt-t">Safety check<small>Brakes, headset, wheels, bolts torqued, tyres and cables looked over. About 30 minutes.</small></span><span class="price">£25</span></label>
            <label class="opt"><input type="radio" name="pkg" value="basic" data-name="Basic service" data-price="60" checked><span class="opt-t">Basic service<small>Safety check plus gears indexed, brakes adjusted, chain wear measured, drivetrain cleaned and lubed.</small></span><span class="price">£60</span></label>
            <label class="opt"><input type="radio" name="pkg" value="full" data-name="Full service" data-price="120"><span class="opt-t">Full service<small>Basic service plus hubs, headset and bottom bracket checked and regreased, wheels trued, cables and outer casing refreshed.</small></span><span class="price">£120</span></label>
            <label class="opt"><input type="radio" name="pkg" value="overhaul" data-name="Overhaul" data-price="220"><span class="opt-t">Overhaul<small>Bike stripped to the frame, every bearing serviced, drivetrain degreased in the parts washer, rebuilt and test-ridden.</small></span><span class="price">£220</span></label>
          </fieldset>

          <fieldset>
            <legend>2 · Single jobs <span class="legend-note">(quantity)</span></legend>
            <label class="opt"><span class="opt-t">Puncture repair<small>Per wheel, inner tube patched or replaced</small></span><span class="price">£10</span><input type="number" min="0" max="4" value="0" inputmode="numeric" data-name="Puncture repair" data-price="10" aria-label="Quantity: puncture repair"></label>
            <label class="opt"><span class="opt-t">Tyre fitted<small>Per wheel, labour only</small></span><span class="price">£8</span><input type="number" min="0" max="4" value="0" inputmode="numeric" data-name="Tyre fitted" data-price="8" aria-label="Quantity: tyre fitted"></label>
            <label class="opt"><span class="opt-t">Tubeless set-up<small>Per wheel, tape, valve and sealant labour</small></span><span class="price">£20</span><input type="number" min="0" max="4" value="0" inputmode="numeric" data-name="Tubeless set-up" data-price="20" aria-label="Quantity: tubeless set-up"></label>
            <label class="opt"><span class="opt-t">Brake adjust<small>Per brake, rim or cable disc</small></span><span class="price">£10</span><input type="number" min="0" max="4" value="0" inputmode="numeric" data-name="Brake adjust" data-price="10" aria-label="Quantity: brake adjust"></label>
            <label class="opt"><span class="opt-t">Hydraulic brake bleed<small>Per brake, fresh fluid, lever feel restored</small></span><span class="price">£25</span><input type="number" min="0" max="4" value="0" inputmode="numeric" data-name="Hydraulic brake bleed" data-price="25" aria-label="Quantity: hydraulic brake bleed"></label>
            <label class="opt"><span class="opt-t">Gear index<small>Derailleur limit screws, cable tension, hanger alignment check</small></span><span class="price">£15</span><input type="number" min="0" max="4" value="0" inputmode="numeric" data-name="Gear index" data-price="15" aria-label="Quantity: gear index"></label>
            <label class="opt"><span class="opt-t">True a wheel<small>Per wheel, spoke tension balanced</small></span><span class="price">£18</span><input type="number" min="0" max="4" value="0" inputmode="numeric" data-name="True a wheel" data-price="18" aria-label="Quantity: true a wheel"></label>
            <label class="opt"><span class="opt-t">Chain and cassette fitted<small>Labour only, per drivetrain</small></span><span class="price">£15</span><input type="number" min="0" max="4" value="0" inputmode="numeric" data-name="Chain and cassette fitted" data-price="15" aria-label="Quantity: chain and cassette fitted"></label>
            <label class="opt"><span class="opt-t">Bottom bracket replaced<small>Labour only, threads faced and greased</small></span><span class="price">£25</span><input type="number" min="0" max="4" value="0" inputmode="numeric" data-name="Bottom bracket replaced" data-price="25" aria-label="Quantity: bottom bracket replaced"></label>
          </fieldset>
          <p class="fine">We work on road, hybrid, gravel, mountain and kids' bikes. We don't service motors or batteries on e-bikes.</p>

          <fieldset id="book-details">
            <legend>3 · Book your drop-off</legend>
            <div class="field">
              <label for="f-name">Your name</label>
              <input id="f-name" name="name" type="text" autocomplete="name" required>
              <p class="err" data-for="f-name"></p>
            </div>
            <div class="field">
              <label for="f-email">Email</label>
              <input id="f-email" name="email" type="email" autocomplete="email" required>
              <p class="err" data-for="f-email"></p>
            </div>
            <div class="field">
              <label for="f-bike">Bike type</label>
              <select id="f-bike" name="bike" required>
                <option value="">Choose…</option>
                <option>Road</option>
                <option>Hybrid / commuter</option>
                <option>Gravel</option>
                <option>Mountain</option>
                <option>Kids' bike</option>
                <option>Folding</option>
              </select>
              <p class="err" data-for="f-bike"></p>
            </div>
            <div class="field">
              <label for="f-date">Drop-off day <span class="legend-note">(Tuesday to Saturday)</span></label>
              <input id="f-date" name="date" type="date" required>
              <p class="err" data-for="f-date"></p>
            </div>
            <div class="field">
              <label for="f-notes">Anything we should know? <span class="legend-note">(optional)</span></label>
              <textarea id="f-notes" name="notes" rows="3" placeholder="Clicking under power, rear brake rubs, tyre keeps going down…"></textarea>
            </div>
            <p class="err" id="form-err" role="alert"></p>
            <button class="btn" type="submit">Email my booking request</button>
            <p class="status" id="send-status" role="status"></p>
          </fieldset>
        </form>

        <aside class="tag" aria-label="Your job tag">
          <div class="tag-hole" aria-hidden="true"></div>
          <p class="tag-h">Job tag</p>
          <p class="tag-meta">Tannery Row Cycles · Leeds</p>
          <ol id="tag-lines" class="tag-lines"></ol>
          <p class="tag-total"><span>Labour from</span> <strong id="tag-total">£0</strong></p>
          <p class="fine">Plus parts, agreed with you before fitting. You pay on collection.</p>
        </aside>
      </div>
    </section>

    <section class="panel" id="steps" aria-labelledby="steps-h">
      <h2 id="steps-h">How booking works</h2>
      <ol class="steps">
        <li><strong>Build your tag.</strong> Choose a package and any single jobs above.</li>
        <li><strong>Pick a drop-off day.</strong> Tuesday to Saturday. Walk-ins are welcome for punctures and quick fixes if the stand is free.</li>
        <li><strong>We confirm by email or phone.</strong> If we find anything beyond your tag (a worn chain, a cracked rim, a bent hanger) we ring you with the price first.</li>
        <li><strong>Collect and pay.</strong> We text when the bike is ready. Most services are done in two working days; a safety check can often be same day if the bike is in before 10:00.</li>
      </ol>
      <p class="fine">Turnaround and prices are illustrative for this concept shop.</p>
    </section>
  </main>

  <footer class="foot">
    <p><strong>Tannery Row Cycles</strong> · Unit 4, Tannery Row Yard, Kirkstall, Leeds · <a href="tel:+441134960142">0113 496 0142</a> · <a href="mailto:workshop@example.com">workshop@example.com</a></p>
    <p class="fine">Concept shop. The name, address, phone number, email, hours and prices on this page are illustrative placeholders to be replaced by the real shop's details.</p>
  </footer>

  <script type="module" src="main.js"></script>
</body>
</html>
```

## File: `styles.css`

```css
:root {
  --kraft: #e8dcc4;
  --paper: #f7f1e3;
  --ink: #1d1b18;
  --oxide: #a82d17; /* darkened from a brighter red so it clears 4.5:1 on kraft and paper */
  --green: #2e4a3c;
  --rule: #1d1b18;
  --display: "Barlow Condensed", "Arial Narrow", Impact, sans-serif;
  --text: "Barlow", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: var(--text);
  font-size: 1.0625rem;
  line-height: 1.5;
  color: var(--ink);
  background-color: var(--kraft);
  background-image: repeating-linear-gradient(0deg, rgba(29, 27, 24, .035) 0 1px, transparent 1px 4px);
}
a { color: var(--oxide); }
h1, h2, h3 { font-family: var(--display); text-transform: uppercase; letter-spacing: .02em; line-height: 1.02; margin: 0 0 .5em; }
h1 { font-size: clamp(2.4rem, 7vw, 4.6rem); max-width: 16ch; }
h2 { font-size: clamp(2rem, 5vw, 3rem); border-bottom: 4px solid var(--rule); padding-bottom: .2em; }
h3 { font-size: 1.4rem; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.skip { position: absolute; left: -999px; top: 0; background: var(--ink); color: var(--paper); padding: .6rem 1rem; z-index: 10; }
.skip:focus { left: 0; }
:focus-visible { outline: 3px solid var(--oxide); outline-offset: 2px; }

.top { display: flex; flex-wrap: wrap; gap: .5rem 1.5rem; align-items: center; justify-content: space-between; padding: .9rem clamp(1rem, 4vw, 3rem); background: var(--ink); color: var(--paper); }
.brand { font-family: var(--display); font-size: 1.5rem; text-transform: uppercase; letter-spacing: .04em; color: var(--paper); text-decoration: none; }
.top nav { display: flex; flex-wrap: wrap; gap: 1.2rem; }
.top nav a { color: var(--paper); text-decoration: none; font-weight: 600; }
.top nav a:hover { text-decoration: underline; text-underline-offset: 4px; }

.hero { display: grid; gap: 1.5rem; align-items: center; padding: clamp(2rem, 6vw, 5rem) clamp(1rem, 4vw, 3rem); max-width: 72rem; margin: 0 auto; }
.stamp { display: inline-block; font-family: var(--mono); font-size: .85rem; text-transform: uppercase; letter-spacing: .08em; border: 2px solid var(--oxide); color: var(--oxide); padding: .15rem .6rem; transform: rotate(-1.5deg); }
.lede { max-width: 38rem; font-size: 1.2rem; }
.bike { width: 100%; max-width: 30rem; color: var(--green); justify-self: center; }
.status { font-family: var(--mono); font-size: .95rem; margin: 1rem 0; }
.status.is-open { color: var(--green); font-weight: 600; }
.status.is-closed { color: var(--oxide); font-weight: 600; }

.btn { display: inline-block; font-family: var(--display); font-size: 1.3rem; text-transform: uppercase; letter-spacing: .05em; background: var(--ink); color: var(--paper); border: 0; padding: .7rem 1.4rem; cursor: pointer; text-decoration: none; }
.btn:hover { background: var(--green); }

.panel { max-width: 72rem; margin: 0 auto; padding: 2.5rem clamp(1rem, 4vw, 3rem); }
.intro { max-width: 42rem; }
.fine { font-size: .9rem; color: #4a463f; }

.hours-wrap { display: grid; gap: 1.5rem; }
.hours { border-collapse: collapse; width: 100%; max-width: 30rem; background: var(--paper); font-family: var(--mono); }
.hours th, .hours td { text-align: left; padding: .55rem .9rem; border-bottom: 1px dashed rgba(29, 27, 24, .4); }
.hours td { text-align: right; }
.hours tr.is-today { background: var(--ink); color: var(--paper); }
.hours tr.is-today th::after { content: " · today"; color: #f0b7a8; }

.builder { display: grid; gap: 2rem; align-items: start; }
.card { background: var(--paper); border: 2px solid var(--ink); padding: 1.2rem; }
fieldset { border: 0; margin: 0 0 1.5rem; padding: 0; min-width: 0; }
legend { font-family: var(--display); font-size: 1.5rem; text-transform: uppercase; letter-spacing: .03em; padding: 0; margin-bottom: .6rem; }
.legend-note { font-family: var(--text); font-size: .9rem; text-transform: none; letter-spacing: 0; font-weight: 400; color: #4a463f; }
.opt { display: grid; grid-template-columns: auto 1fr auto; gap: .2rem .8rem; align-items: start; padding: .7rem 0; border-top: 1px dashed rgba(29, 27, 24, .4); cursor: pointer; }
.opt input[type="radio"] { margin-top: .35rem; accent-color: var(--oxide); width: 1.1rem; height: 1.1rem; }
.opt input[type="number"] { width: 4rem; font: inherit; padding: .3rem; border: 2px solid var(--ink); background: #fff; order: 3; }
.opt:has(input[type="number"]) { grid-template-columns: 1fr auto auto; }
.opt-t { font-weight: 600; }
.opt-t small { display: block; font-weight: 400; font-size: .88rem; color: #4a463f; }
.price { font-family: var(--mono); font-weight: 600; }
.opt:has(input:checked) { background: rgba(168, 45, 23, .08); }

.field { margin-bottom: 1rem; }
.field label { display: block; font-weight: 600; margin-bottom: .25rem; }
.field input, .field select, .field textarea { width: 100%; font: inherit; padding: .55rem .6rem; border: 2px solid var(--ink); background: #fff; color: var(--ink); }
.field [aria-invalid="true"] { border-color: var(--oxide); }
.err { color: var(--oxide); font-weight: 600; margin: .25rem 0 0; min-height: 0; }
.err:empty { display: none; }

.tag { position: relative; background: #d9c49a; border: 2px solid var(--ink); padding: 3rem 1.4rem 1.4rem; font-family: var(--mono); clip-path: polygon(0 0, calc(100% - 28px) 0, 100% 28px, 100% 100%, 0 100%); }
.tag-hole { position: absolute; top: 1rem; left: 1.2rem; width: 1.1rem; height: 1.1rem; border-radius: 50%; background: var(--kraft); border: 2px solid var(--ink); }
.tag-h { font-family: var(--display); font-size: 2rem; text-transform: uppercase; margin: 0; line-height: 1; }
.tag-meta { margin: .2rem 0 1rem; font-size: .85rem; }
.tag-lines { list-style: none; margin: 0 0 1rem; padding: 0; min-height: 3rem; }
.tag-lines li { display: flex; justify-content: space-between; gap: 1rem; padding: .3rem 0; border-bottom: 1px dashed var(--ink); }
.tag-lines li.empty { border: 0; font-style: italic; }
.tag-total { display: flex; justify-content: space-between; align-items: baseline; font-size: 1rem; margin: 0 0 .5rem; border-top: 3px solid var(--ink); padding-top: .6rem; }
.tag-total strong { font-family: var(--display); font-size: 2.6rem; color: var(--oxide); }
.tag-total strong.bump { animation: bump .25s ease-out; }
@keyframes bump { from { transform: scale(1.18); } to { transform: scale(1); } }

.steps { counter-reset: s; list-style: none; padding: 0; display: grid; gap: 1rem; max-width: 44rem; }
.steps li { counter-increment: s; position: relative; padding-left: 3.4rem; }
.steps li::before { content: counter(s); position: absolute; left: 0; top: -.2rem; width: 2.4rem; height: 2.4rem; display: grid; place-items: center; background: var(--ink); color: var(--paper); font-family: var(--display); font-size: 1.5rem; }

.foot { background: var(--ink); color: var(--paper); padding: 2rem clamp(1rem, 4vw, 3rem); }
.foot a { color: #f0b7a8; }
.foot .fine { color: #cfc8b8; }

@media (min-width: 860px) {
  .hero { grid-template-columns: 1.2fr 1fr; }
  .hours-wrap { grid-template-columns: auto 1fr; gap: 4rem; }
  .builder { grid-template-columns: 1.5fr 1fr; }
  .tag { position: sticky; top: 1rem; }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .tag-total strong.bump { animation: none; }
}
```

## File: `main.js`

```js
// Replace with the shop's real address when the concept becomes a real shop.
const SHOP_EMAIL = "workshop@example.com";
const SHOP_PHONE = "0113 496 0142";
const TZ = "Europe/London";
const DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const WEEKDAY_INDEX = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };

// The hours table in index.html is the only source of opening hours.
const hours = {};
document.querySelectorAll(".hours tr[data-day]").forEach((row) => {
  const day = Number(row.dataset.day);
  hours[day] = row.dataset.open ? { open: row.dataset.open, close: row.dataset.close } : null;
});

const toMinutes = (hhmm) => {
  const [h, m] = hhmm.split(":").map(Number);
  return h * 60 + m;
};

// Current weekday and minutes-since-midnight in Leeds, regardless of the visitor's time zone.
function londonNow() {
  const parts = new Intl.DateTimeFormat("en-GB", {
    timeZone: TZ, weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false,
  }).formatToParts(new Date());
  const get = (type) => parts.find((p) => p.type === type).value;
  return {
    day: WEEKDAY_INDEX[get("weekday")],
    minutes: (Number(get("hour")) % 24) * 60 + Number(get("minute")), // some engines return "24" at midnight
  };
}

function londonDateISO() {
  return new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());
}

function renderStatus() {
  const el = document.getElementById("open-status");
  const { day, minutes } = londonNow();
  const today = hours[day];

  document.querySelectorAll(".hours tr[data-day]").forEach((row) => {
    row.classList.toggle("is-today", Number(row.dataset.day) === day);
  });

  if (today && minutes >= toMinutes(today.open) && minutes < toMinutes(today.close)) {
    el.textContent = `Open now · until ${today.close} today`;
    el.className = "status is-open";
    return;
  }

  let when = "";
  if (today && minutes < toMinutes(today.open)) {
    when = `today at ${today.open}`;
  } else {
    for (let i = 1; i <= 7; i++) {
      const d = (day + i) % 7;
      if (hours[d]) {
        when = `${i === 1 ? "tomorrow" : DAY_NAMES[d]} at ${hours[d].open}`;
        break;
      }
    }
  }
  el.textContent = `Closed now · opens ${when}`;
  el.className = "status is-closed";
}

const money = (n) => `£${n}`;
const form = document.getElementById("book");
const linesEl = document.getElementById("tag-lines");
const totalEl = document.getElementById("tag-total");
let lastTotal = null;

function tagItems() {
  const items = [];
  const pkg = form.querySelector('input[name="pkg"]:checked');
  if (pkg && Number(pkg.dataset.price) > 0) {
    items.push({ name: pkg.dataset.name, qty: 1, price: Number(pkg.dataset.price) });
  }
  form.querySelectorAll('input[type="number"][data-price]').forEach((input) => {
    const qty = Math.max(0, Math.min(4, parseInt(input.value, 10) || 0));
    if (qty > 0) items.push({ name: input.dataset.name, qty, price: Number(input.dataset.price) });
  });
  return items;
}

function renderTag() {
  const items = tagItems();
  const total = items.reduce((sum, it) => sum + it.qty * it.price, 0);
  linesEl.innerHTML = "";
  if (items.length === 0) {
    const li = document.createElement("li");
    li.className = "empty";
    li.textContent = "Nothing on the tag yet.";
    linesEl.append(li);
  } else {
    items.forEach((it) => {
      const li = document.createElement("li");
      const left = document.createElement("span");
      left.textContent = it.qty > 1 ? `${it.name} × ${it.qty}` : it.name;
      const right = document.createElement("span");
      right.textContent = money(it.qty * it.price);
      li.append(left, right);
      linesEl.append(li);
    });
  }
  totalEl.textContent = money(total);
  if (lastTotal !== null && lastTotal !== total) {
    totalEl.classList.remove("bump");
    void totalEl.offsetWidth; // restart the animation
    totalEl.classList.add("bump");
  }
  lastTotal = total;
}

const dateInput = document.getElementById("f-date");
dateInput.min = londonDateISO();

function dateMessage() {
  if (!dateInput.value) return "Choose a drop-off day.";
  if (dateInput.value < dateInput.min) return "That day has already passed.";
  const day = new Date(`${dateInput.value}T12:00:00`).getDay();
  if (!hours[day]) return "We're closed that day. Pick Tuesday to Saturday.";
  return "";
}

function fieldMessage(el) {
  if (el === dateInput) return dateMessage();
  if (el.validity.valueMissing) return "This field is needed.";
  if (el.validity.typeMismatch) return "Enter a valid email address.";
  return "";
}

function showFieldError(el) {
  const msg = fieldMessage(el);
  const out = form.querySelector(`.err[data-for="${el.id}"]`);
  out.textContent = msg;
  el.setAttribute("aria-invalid", msg ? "true" : "false");
  if (msg) el.setAttribute("aria-describedby", out.id || (out.id = `${el.id}-err`));
  return msg;
}

form.addEventListener("input", (e) => {
  if (e.target.name === "pkg" || e.target.type === "number") renderTag();
  if (e.target.matches("#f-name, #f-email, #f-bike, #f-date") && e.target.getAttribute("aria-invalid") === "true") {
    showFieldError(e.target);
  }
});
form.addEventListener("change", (e) => {
  if (e.target.matches("#f-date")) showFieldError(e.target);
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const formErr = document.getElementById("form-err");
  const sendStatus = document.getElementById("send-status");
  formErr.textContent = "";
  sendStatus.textContent = "";

  const fields = ["f-name", "f-email", "f-bike", "f-date"].map((id) => document.getElementById(id));
  const firstBad = fields.find((el) => showFieldError(el));
  const items = tagItems();

  if (items.length === 0) {
    formErr.textContent = "Add a service or a single job to your tag first.";
    form.querySelector('input[name="pkg"]:checked').focus();
    return;
  }
  if (firstBad) {
    firstBad.focus();
    return;
  }

  const total = items.reduce((sum, it) => sum + it.qty * it.price, 0);
  const value = (id) => document.getElementById(id).value.trim();
  const body = [
    "Hello Tannery Row Cycles,",
    "",
    `Name: ${value("f-name")}`,
    `Email: ${value("f-email")}`,
    `Bike: ${value("f-bike")}`,
    `Drop-off day: ${value("f-date")}`,
    "",
    "JOB TAG",
    ...items.map((it) => `- ${it.name}${it.qty > 1 ? ` x ${it.qty}` : ""}: ${money(it.qty * it.price)}`),
    `Labour from: ${money(total)} (plus parts, agreed before fitting)`,
    "",
    `Notes: ${value("f-notes") || "none"}`,
  ].join("\n");

  const subject = `Booking request: ${value("f-date")} drop-off`;
  sendStatus.textContent = `Your email app should open with the job tag. If it doesn't, call ${SHOP_PHONE}.`;
  window.location.href = `mailto:${SHOP_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
});

renderStatus();
renderTag();
setInterval(renderStatus, 60000);
```

## Design notes

- **World:** a workshop counter. The job tag, the tag you write for every bike that comes in, is the one signature object; the page is built so the visitor fills it in rather than reads a price list. The kraft-card tag with a punched hole and clipped corner is CSS only.
- **Palette:** kraft paper (`#e8dcc4`), workshop ink (`#1d1b18`), oxide red (`#a82d17`) for stamps and totals, a frame green (`#2e4a3c`) for the bike and the open-now line.
- **Type:** Barlow Condensed uppercase for headings (workshop signage), Barlow for text, the system monospace for hours, prices and the tag (till-roll feel).
- **Vocabulary used on purpose:** index (gears), true (a wheel), bleed (hydraulic brakes), hanger alignment, bottom bracket, headset, cassette, tubeless, chain wear, torque. A cyclist should recognise their own bike's problems, not generic "maintenance".
- **Honesty:** no reviews, ratings, years in business or logos. The footer and the hours section say it is a concept shop with illustrative details. The phone number is in the UK Ofcom range reserved for drama use (0113 496 0xxx) and the email is on `example.com`, so neither belongs to a real party.
- Do not change file contents to "improve" these choices.

## Checks already run

None. The files above were written but never opened in a browser, linted, served or replayed, because command execution was unavailable when this prompt was produced. Treat everything below as unverified.

## Not verified

- Page load and console: no browser was opened, so console errors and failed requests are unchecked.
- Layout: no check at 390, 768, 1280 or 1920 px; horizontal overflow is unmeasured. The two-column grids at 860 px and the `:has()` selectors in `styles.css` (needs a current Chrome, Safari or Firefox) are untested.
- Behaviour: open-now logic (including the Europe/London conversion and the midnight "24" handling), the tag total, date validation, the `mailto:` hand-off and the focus moves on invalid submit are all unrun.
- Reduced motion, contrast ratios (the oxide red on kraft/paper is estimated at about 4.9:1, not measured) and keyboard focus visibility are untested.
- Google Fonts loading is untested; offline, the system fallbacks apply.
- Replay: the file sections were not round-tripped through the replay script.
