// Read-only A2 metadata: do not derive this baseline from the new site.
const pages = require("../../evidence/pages.json").pages;
module.exports = Object.fromEntries(pages.map(page => [page.path, {
  description: page.description,
  canonical: page.canonical
}]));
