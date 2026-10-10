import { readFileSync, readdirSync, statSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourcePages = JSON.parse(readFileSync(path.join(root, "evidence", "pages.json"), "utf8")).pages;
const sourceMedia = JSON.parse(readFileSync(path.join(root, "evidence", "media.json"), "utf8")).media;
const sitePages = JSON.parse(readFileSync(path.join(root, "src", "_data", "sitePages.json"), "utf8"));
const dist = path.join(root, "dist");
const errors = [];
const expect = (condition, message) => { if (!condition) errors.push(message); };

expect(sourcePages.length === 10, "Zdrojová evidence nemá deset stránek.");
expect(sitePages.length === sourcePages.length, "Kostra nemá stejný počet stránek jako zdroj.");
const sourcePaths = sourcePages.map(page => page.path);
const targetPaths = sitePages.map(page => page.path);
expect(JSON.stringify(targetPaths) === JSON.stringify(sourcePaths), "URL nebo jejich pořadí nesouhlasí se zdrojovým archivem.");

const allowedFiles = new Set(["assets/css/site.css", "assets/js/gallery.js", "404.html", "sitemap.xml", "robots.txt", ".htaccess"]);
for (const medium of sourceMedia) {
  const stem = `assets/images/${medium.id}`;
  if (medium.selected_original.format === "SVG") allowedFiles.add(`${stem}.svg`);
  else {
    allowedFiles.add(`${stem}.jpg`);
    allowedFiles.add(`${stem}-700.webp`);
    allowedFiles.add(`${stem}-1400.webp`);
  }
}
for (const [index, page] of sitePages.entries()) {
  const expected = sourcePages[index];
  expect(page.title === expected?.title, `${page.path}: původní title nesouhlasí.`);
  expect(page.path === "/" || /^\/[a-z0-9-]+\/$/.test(page.path), `${page.path}: cesta nemá koncové lomítko.`);
  const output = page.path === "/" ? "index.html" : `${page.path.slice(1)}index.html`;
  expect(page.output === output, `${page.path}: výstupní soubor neodpovídá URL.`);
  allowedFiles.add(output);
  let html;
  try { html = readFileSync(path.join(dist, output), "utf8"); }
  catch { errors.push(`${page.path}: chybí HTML výstup.`); continue; }
  expect(html.includes('<html lang="cs">'), `${page.path}: chybí lang=cs.`);
  const scripts = [...html.matchAll(/<script\b[^>]*>[\s\S]*?<\/script>/g)].map(match => match[0]);
  expect(JSON.stringify(scripts) === JSON.stringify(['<script src="/assets/js/gallery.js" defer></script>']), `${page.path}: nečekaný skript.`);
  expect(html.includes('<meta charset="utf-8">'), `${page.path}: chybí UTF-8.`);
  expect(html.includes('name="viewport"'), `${page.path}: chybí viewport.`);
  expect(html.includes(`<title>${page.title}</title>`), `${page.path}: nesouhlasí title.`);
  expect(html.includes(`href="https://www.imbolg-harmony.cz${page.path}"`), `${page.path}: nesouhlasí canonical.`);
  expect(html.includes('href="#hlavni-obsah"'), `${page.path}: chybí přeskočení na obsah.`);
  expect(html.includes('<main id="hlavni-obsah"'), `${page.path}: chybí hlavní oblast.`);
  expect(html.includes('<details class="mobile-menu">'), `${page.path}: chybí menu bez JS.`);
  const navs = [...html.matchAll(/<nav\b[^>]*aria-label="Hlavní navigace"[^>]*>([\s\S]*?)<\/nav>/g)];
  expect(navs.length === 2, `${page.path}: očekávána desktopová a mobilní navigace.`);
  for (const [navIndex, nav] of navs.entries()) {
    const links = [...nav[1].matchAll(/<a href="([^"]+)"([^>]*)>([^<]+)<\/a>/g)];
    expect(JSON.stringify(links.map(link => link[1])) === JSON.stringify(targetPaths), `${page.path}: navigace ${navIndex + 1} mění původní pořadí.`);
    expect(JSON.stringify(links.map(link => link[3])) === JSON.stringify(sitePages.map(item => item.label)), `${page.path}: navigace ${navIndex + 1} mění popisky.`);
    expect(links.filter(link => link[2].includes('aria-current="page"')).map(link => link[1]).join() === page.path, `${page.path}: chybné aria-current v navigaci ${navIndex + 1}.`);
  }
}

function visit(directory) {
  for (const item of readdirSync(directory, { withFileTypes: true })) {
    const full = path.join(directory, item.name);
    if (item.isDirectory()) visit(full);
    else if (item.isFile()) {
      const relative = path.relative(dist, full).replaceAll(path.sep, "/");
      expect(allowedFiles.has(relative), `Nečekaný soubor ve veřejném buildu: ${relative}`);
    } else errors.push(`Neobvyklý typ souboru ve veřejném buildu: ${full}`);
  }
}
visit(dist);
for (const relative of allowedFiles) {
  try { expect(statSync(path.join(dist, relative)).isFile(), `Chybí veřejný soubor: ${relative}`); }
  catch { errors.push(`Chybí veřejný soubor: ${relative}`); }
}

if (errors.length) {
  for (const error of errors) console.error(error);
  process.exitCode = 1;
} else {
  console.log("A3: 10 URL, titulky, pořadí menu, aria-current a čistý dist ověřeny proti A2.");
  console.log("Úplnost textů, médií, galerií a PHP se v A3 nekontroluje; patří do A4 a A5.");
}
