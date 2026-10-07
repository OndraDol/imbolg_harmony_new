const path = require("node:path");

const fs = require("node:fs");
const pages = require(path.join(__dirname, "..", "content", "pages.json"));
const template = fs.readFileSync(path.join(__dirname, "..", "..", "server", "app", "templates", "contact-form.html"), "utf8");
const emptyForm = template.replace(/__[A-Z_]+__/g, "");
const pending = /<div data-form-pending="A5">[\s\S]*?<\/button>\s*<\/div>\s*<\/div>/g;
if ((pages.home.match(pending) || []).length !== 1) throw new Error("Expected one archived home form");
module.exports = { ...pages, home: pages.home.replace(pending, emptyForm) };
