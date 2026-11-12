"""Generate the public files after editing data/site.json or data/content.json."""
from html import escape
import json
import os
from pathlib import Path
import re
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
SITE = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
COPY = json.loads((ROOT / "data/content.json").read_text(encoding="utf-8"))
DOMAIN = SITE["domain"].rstrip("/")
PORTRAIT = "assets/portrait-charlotte-jaloux.jpg"
PHONE = "+1" + re.sub(r"\D", "", SITE["phone"])
MAP = "https://www.google.com/maps/dir/?" + urlencode({
    "api": 1,
    "destination": ", ".join([SITE["hospital"]["en"], SITE["address"]["en"],
                              SITE["city"], SITE["province"], SITE["postal"]]),
})
KEYS = tuple(COPY["fr"]["nav"])


def rel(path, target):
    return os.path.relpath(target, start=Path(path).parent).replace(os.sep, "/")


def route(lang, key):
    slug = COPY[lang]["nav"][key][1]
    return (("en/" if lang == "en" else "") + (slug + "/" if slug else ""))


def url(lang, key):
    return DOMAIN + "/" + route(lang, key)


def link(href, label, css=""):
    class_attr = f' class="{escape(css)}"' if css else ""
    return f'<a href="{escape(href)}"{class_attr}>{escape(label)}</a>'


def hospital(lang):
    return escape(SITE["hospital"][lang])


def contact_details(copy, compact=False):
    values = [
        (copy["phone_label"], link("tel:" + PHONE, SITE["phone"])),
        (copy["fax_label"], escape(SITE["fax"])),
        (copy["email_label"], link("mailto:" + SITE["email"], SITE["email"])),
    ]
    rows = "".join(f"<div><dt>{escape(label)}</dt><dd>{value}</dd></div>"
                   for label, value in values)
    css = " compact" if compact else ""
    return f'<dl class="contact-details{css}">{rows}</dl>'


def call(copy):
    return link("tel:" + PHONE, copy["call"], "button")


def directions(copy):
    return link(MAP, copy["directions"])


def areas(copy):
    rows = "".join(f'<article class="area"><h3>{escape(title)}</h3><p>{escape(text)}</p></article>'
                   for title, text in copy["areas"])
    return f'<div class="grid">{rows}</div>'


def heading(title, intro=""):
    description = f'<p class="intro">{escape(intro)}</p>' if intro else ""
    return f'<div class="page-heading wrap"><h1>{escape(title)}</h1>{description}</div>'


def home(lang, copy, path):
    return f'''<div class="wrap hero">
  <div>
    <p class="kicker">{escape(copy["name"])}, {escape(SITE["credentials"])}</p>
    <h1>{escape(copy["hero_title"])}</h1>
    <p class="intro">{escape(copy["home_intro"])}</p>
    <div class="actions">{call(copy)}{directions(copy)}</div>
    {contact_details(copy, compact=True)}
    <p class="hospital">{escape(SITE["address"][lang])} · {escape(copy["room_label"])} {escape(SITE["room"])}<br>{escape(SITE["city"])} ({escape(SITE["province"])}) {escape(SITE["postal"])} · {escape(SITE["country"])}<br>{escape(SITE["institution"][lang])}</p>
  </div>
  <figure class="portrait"><img src="{rel(path, PORTRAIT)}" alt="{escape(copy["alt"])}" width="1061" height="1483" fetchpriority="high"></figure>
</div>
<section class="section tint">
  <div class="wrap">
    <div class="section-title"><h2>{escape(copy["expertise_title"])}</h2><p>{escape(copy["expertise_intro"])}</p></div>
    {areas(copy)}
    <div class="actions">{link(rel(path, route(lang, "expertise") + "index.html"), copy["expertise_link"])}</div>
  </div>
</section>'''


def about(copy):
    rows = "".join(f"<div><dt>{escape(label)}</dt><dd>{escape(value)}</dd></div>"
                   for label, value in copy["training"])
    media = "".join(f"<li>{link(href, label)}</li>"
                    for href, label in zip(SITE["media"], copy["media_links"], strict=True))
    return f'''{heading(copy["nav"]["about"][0], copy["about_intro"])}
<div class="wrap page-body">
  <div class="narrow">
    <section><h2>{escape(copy["training_title"])}</h2><dl class="rows">{rows}</dl></section>
    <section><h2>{escape(copy["research_title"])}</h2>
      <p>{escape(copy["rank"])}. {escape(copy["research"])}</p>
      <ul class="source-links"><li>{link(SITE["profile"], copy["profile_link"])}</li><li>{link(SITE["publication"], copy["publication_link"])}</li></ul>
    </section>
    <section><h2>{escape(copy["media_title"])}</h2><ul class="source-links">{media}</ul></section>
  </div>
</div>'''


def expertise(lang, copy, path):
    contact_path = rel(path, route(lang, "contact") + "index.html")
    return f'''{heading(copy["expertise_title"], copy["expertise_intro"])}
<div class="wrap page-body">
  {areas(copy)}
  <div class="actions"><p>{escape(copy["scope"])}</p>{link(contact_path, copy["nav"]["contact"][0], "button")}</div>
</div>'''


def contact(lang, copy):
    institution = SITE["institution_url" if lang == "fr" else "institution_en_url"]
    return f'''{heading(copy["contact_title"], copy["contact_intro"])}
<div class="wrap page-body">
  <section class="contact-card narrow">
    <h2>{hospital(lang)}</h2>
    <p>{escape(SITE["institution"][lang])}</p>
    <address>{escape(SITE["address"][lang])}<br>{escape(copy["room_label"])} {escape(SITE["room"])}<br>{escape(SITE["city"])} ({escape(SITE["province"])}) {escape(SITE["postal"])}<br>{escape(SITE["country"])}</address>
    <div class="actions">{call(copy)}{directions(copy)}{link(institution, copy["institution_link"])}</div>
    {contact_details(copy)}
    <p class="notice">{escape(copy["email_note"])}</p>
  </section>
</div>'''


def faq(lang, copy, path):
    items = "".join(f'<details><summary>{escape(question)}</summary><p>{escape(answer)}</p></details>'
                    for question, answer in copy["faq"])
    return f'''{heading(copy["faq_title"])}
<div class="wrap page-body"><div class="narrow">
  {items}
  <div class="actions">{link(rel(path, route(lang, "contact") + "index.html"), copy["nav"]["contact"][0], "button")}</div>
</div></div>'''


def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")


def page(lang, key):
    copy = COPY[lang]
    other = "en" if lang == "fr" else "fr"
    path = route(lang, key) + "index.html"
    nav = []
    for item, (label, _) in copy["nav"].items():
        current = ' aria-current="page"' if item == key else ""
        nav.append(f'<a href="{rel(path, route(lang, item) + "index.html")}"{current}>{escape(label)}</a>')
    language = rel(path, route(other, key) + "index.html")
    contact_path = rel(path, route(lang, "contact") + "index.html")
    home_path = rel(path, route(lang, "home") + "index.html")
    body = {"home": lambda: home(lang, copy, path), "about": lambda: about(copy),
            "expertise": lambda: expertise(lang, copy, path), "contact": lambda: contact(lang, copy),
            "faq": lambda: faq(lang, copy, path)}[key]()
    title = (copy["name"] + " | " + copy["specialty"] if key == "home"
             else copy["nav"][key][0] + " | " + copy["name"])
    description = copy["descriptions"][key]
    portrait_url = DOMAIN + "/" + PORTRAIT
    structured = json.dumps({
        "@context": "https://schema.org", "@type": "Person", "name": SITE["name"],
        "honorificPrefix": "Dre" if lang == "fr" else "Dr.",
        "honorificSuffix": SITE["credentials"], "jobTitle": copy["specialty"],
        "url": url(lang, "home"), "image": portrait_url, "sameAs": [SITE["profile"]],
        "affiliation": {"@type": "Hospital", "name": SITE["hospital"][lang],
                        "url": SITE["institution_url" if lang == "fr" else "institution_en_url"]},
    }, ensure_ascii=False).replace("<", "\\u003c")
    write(path, f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="theme-color" content="#faf6f0">
  <link rel="canonical" href="{url(lang, key)}">
  <link rel="alternate" hreflang="fr" href="{url("fr", key)}">
  <link rel="alternate" hreflang="en" href="{url("en", key)}">
  <link rel="alternate" hreflang="x-default" href="{url("fr", key)}">
  <link rel="icon" href="{rel(path, "assets/favicon.svg")}" type="image/svg+xml">
  <link rel="stylesheet" href="{rel(path, "assets/style.css")}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{url(lang, key)}">
  <meta property="og:locale" content="{"fr_CA" if lang == "fr" else "en_CA"}">
  <meta property="og:image" content="{portrait_url}">
  <meta property="og:image:alt" content="{escape(copy["alt"])}">
  <meta name="twitter:card" content="summary">
  <script type="application/ld+json">{structured}</script>
</head>
<body>
  <a class="skip" href="#main">{escape(copy["skip"])}</a>
  <header class="header"><div class="wrap navrow">
    <a class="brand" href="{home_path}"><span class="monogram" aria-hidden="true">CJ</span><span class="brand-name">{escape(copy["name"])}</span></a>
    <nav class="navlinks" aria-label="{escape(copy["nav_label"])}">
      {" ".join(nav)}
      <a class="language" href="{language}" lang="{other}" hreflang="{other}">{escape(copy["language"])}</a>
    </nav>
  </div></header>
  <main id="main">{body}</main>
  <footer class="footer"><div class="wrap">
    <p>{escape(copy["name"])} · {hospital(lang)}</p>
    {link(contact_path, copy["nav"]["contact"][0])}
  </div></footer>
</body>
</html>
''')


for language in COPY:
    for key in KEYS:
        page(language, key)

entries = "\n".join(f"  <url><loc>{url(lang, key)}</loc></url>" for lang in COPY for key in KEYS)
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + entries + "\n</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
write(".nojekyll", "")
