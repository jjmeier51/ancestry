# Family Ancestry Website

A fast, private, dependency-free website for your family history and family
tree. Everything is plain HTML, CSS and JavaScript, so it runs from a folder on
your computer or from any static host such as GitHub Pages. There is no build
step, no database and nothing to install.

## What's included

| Page | What it does |
| --- | --- |
| **Home** | Overview statistics, the home person with parents and grandparents, featured stories, earliest ancestors, surname cloud |
| **Family Tree** | Interactive pedigree (ancestors) and descendant charts with pan, zoom and expandable generations; click anyone to re-centre the tree or open their profile |
| **People** | Searchable, filterable directory of everyone in the file, grouped by surname, first name or decade of birth |
| **Person** | Profile page: dates and places, biography, immediate family, grandparents, personal timeline, stories and photos, and a relationship calculator ("Emily is the great-granddaughter of Thomas") |
| **Timeline** | Every dated birth, marriage, death, story and custom event, grouped by decade, with filters |
| **Stories** | Long-form family stories linked to the people in them |
| **Gallery** | Photographs with captions, dates and the people pictured; lightbox view |

Global search in the header works on every page. The design adapts to phones
and to light/dark mode, and prints cleanly.

## Quick start

1. Open `index.html` in a browser. The site ships with a fictional sample
   family (the Hartwells) so you can see how everything works.
2. Replace the sample with your family. Either:
   - **Import a GEDCOM file.** Export a `.ged` from Ancestry, FamilySearch,
     MyHeritage, Gramps, RootsMagic, etc., then run:
     ```sh
     python3 scripts/gedcom_to_data.py path/to/export.ged -o data/family.js --title "The Smith Family" --root I1
     ```
   - **Or edit `data/family.js` by hand.** It is a readable JSON-style file;
     the format is described below.
3. Drop photographs into `images/` and reference them from the data file.
4. Refresh the browser.

## Publishing on GitHub Pages

1. Push this repository to GitHub.
2. On GitHub, open **Settings → Pages** and set **Source** to **GitHub Actions**.
3. Every push to `main` now deploys automatically via
   `.github/workflows/pages.yml`. Your site appears at
   `https://<username>.github.io/<repository>/`.

Because the data file is public once deployed, consider omitting exact birth
dates and places for living relatives. The importer keeps whatever your
genealogy program exported, so review `data/family.js` before publishing.

## Data format

`data/family.js` assigns one object to `window.FAMILY_DATA`:

```js
window.FAMILY_DATA = {
  "title": "The Hartwell Family",
  "subtitle": "Four generations, two continents, one family",
  "rootPerson": "I23",                 // the "home person" for the tree and relationships
  "people": [
    {
      "id": "I1",                        // unique; any string
      "given": "Thomas", "surname": "Hartwell", "suffix": "", "nickname": "",
      "sex": "M",                        // "M", "F" or "U"
      "birth": { "date": "1872-03-14", "place": "Bridport, Dorset, England" },
      "death": { "date": "1941-11-02", "place": "Rochester, New York, USA" },
      "burial": { "date": "", "place": "" },      // optional
      "occupation": "Blacksmith",                 // optional
      "photo": "images/thomas.jpg",               // optional portrait
      "bio": "Free text. Blank lines make paragraphs.",
      "events": [                                 // optional extra events for the timeline
        { "type": "event", "title": "Emigrated", "date": "1891", "place": "New York" }
      ],
      "facts": [ { "label": "Religion", "value": "Methodist" } ],   // optional extra rows
      "sources": [ "1900 US Census", "Dorset parish register" ]      // optional
    }
  ],
  "families": [
    {
      "id": "F1",
      "husband": "I1", "wife": "I2",     // either may be omitted
      "marriage": { "date": "1896-06-20", "place": "Rochester, New York, USA" },
      "children": ["I3", "I4", "I5"]     // in birth order (the site re-sorts by birth date anyway)
    }
  ],
  "stories": [
    { "id": "S1", "title": "The Crossing", "date": "1896", "people": ["I1", "I2"],
      "body": "Paragraphs separated by blank lines.", "image": "images/ship.jpg" }
  ],
  "photos": [
    { "src": "images/forge.jpg", "caption": "The forge, about 1905.", "date": "ABT 1905", "people": ["I1"] }
  ]
};
```

**Dates** can be `YYYY-MM-DD`, `YYYY-MM`, `YYYY`, GEDCOM style (`14 MAR 1872`),
or qualified (`ABT 1890`, `BEF 1900`, `AFT 1900`, `BET 1890 AND 1892`). Unknown
dates can simply be left out.

A person is treated as deceased if they have a `death` entry or were born more
than 105 years ago.

## Project layout

```
index.html, tree.html, people.html, person.html,
timeline.html, stories.html, gallery.html     # pages
css/style.css                                  # theme (light + dark)
js/data.js      # data access, date parsing, relationship calculator
js/ui.js        # header, search, person cards
js/tree.js      # pedigree & descendant chart rendering
js/*.js         # one script per page
data/family.js  # YOUR FAMILY DATA
images/         # photographs
scripts/gedcom_to_data.py   # GEDCOM importer
.github/workflows/pages.yml # GitHub Pages deployment
```

## Customising

- Colours and fonts are CSS variables at the top of `css/style.css`.
- The navigation links are the `NAV` list in `js/ui.js`.
- Node sizes and spacing for the tree are constants at the top of `js/tree.js`.
