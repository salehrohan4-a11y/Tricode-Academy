#!/usr/bin/env python3
"""TRICODE Academy static site generator.
Run: python3 build.py  -> writes the 9 HTML pages, sitemap.xml and robots.txt.
Shared header/footer live here so every page stays consistent. The output is plain static HTML.
"""
import os

OUT = "tricode-academy"
SITE = "https://www.example.com"  # TODO: replace with the real domain (sitemap + Open Graph)

ICONS = {
 "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
 "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
 "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
 "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
 "phone-app": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>',
 "terminal": '<polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>',
 "hash": '<path d="M4 9h16M4 15h16M10 3L8 21M16 3l-2 18"/>',
 "pen": '<path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><circle cx="11" cy="11" r="2"/>',
 "video": '<polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/>',
 "spark": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 17v4M17 19h4"/>',
 "cart": '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/>',
 "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
 "megaphone": '<path d="M3 11v2a1 1 0 0 0 1 1h3l8 5V5L7 10H4a1 1 0 0 0-1 1z"/><path d="M19 8a5 5 0 0 1 0 8"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l1.9-5.4A8.5 8.5 0 1 1 21 11.5z"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 6L2 7"/>',
 "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "check": '<polyline points="20 6 9 17 4 12"/>',
 "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
 "x": '<path d="M18 6L6 18M6 6l12 12"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
 "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5v14z"/><path d="M20 17v4H6.5A2.5 2.5 0 0 1 4 18.5"/>',
 "camera": '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
 "user": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
 "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 "wallet": '<path d="M20 12V8H6a2 2 0 0 1 0-4h12v4"/><path d="M4 6v12a2 2 0 0 0 2 2h14v-4"/><path d="M18 12a2 2 0 0 0 0 4h4v-4z"/>',
 "smartphone": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>',
 "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
 "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z"/><circle cx="12" cy="12" r="3"/>',
 "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
}

def ic(name, cls="h-5 w-5"):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (cls, ICONS[name]))

NAV = [("index.html", "Home"), ("about.html", "About Us"), ("courses.html", "Courses"),
       ("teachers.html", "Teachers"), ("gallery.html", "Gallery"), ("contact.html", "Contact")]

LOGO_MARK = '<img src="assets/img/logo-mark.png" alt="" width="320" height="314" class="brand-mark">'

def header(active):
    links = ""
    mlinks = ""
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links += '<a href="%s" class="nav-link"%s><span>%s</span></a>' % (href, cur, label)
        mlinks += '<a href="%s" class="m-link"%s><span>%s</span>%s</a>' % (href, cur, label, ic("arrow", "h-4 w-4"))
    return '''
<a href="#main" class="skip-link">Skip to content</a>
<header id="site-header" class="site-header">
  <div class="nav-shell">
    <div class="nav-bar">
      <a href="index.html" class="brand" aria-label="TRICODE Academy home">
        %s
        <span class="brand-text"><span class="brand-name">TRICODE</span><span class="brand-sub">Academy</span></span>
      </a>
      <nav class="nav-center" aria-label="Main navigation"><div class="nav-group">%s</div></nav>
      <div class="nav-right">
        <a href="apply.html" class="btn btn-primary nav-cta">Apply Now</a>
        <button id="menu-btn" type="button" class="menu-btn" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu">
          <span class="icon-open">%s</span><span class="icon-close">%s</span>
        </button>
      </div>
    </div>
    <div id="mobile-menu" class="mobile-menu">
      <nav class="mobile-panel" aria-label="Mobile navigation">%s</nav>
    </div>
  </div>
</header>''' % (LOGO_MARK, links, ic("menu", "h-6 w-6"), ic("x", "h-6 w-6"), mlinks)

FOOTER = '''
<footer class="footer-bg text-white">
  <div class="container-x grid gap-10 py-14 sm:grid-cols-2 lg:grid-cols-4">
    <div class="sm:col-span-2 lg:col-span-1">
      <a href="index.html" class="flex items-center gap-2.5" aria-label="TRICODE Academy home">
        <span class="grid h-11 w-11 place-items-center rounded-xl bg-white"><img src="assets/img/logo-mark.png" alt="" width="32" height="32" class="h-8 w-8" loading="lazy"></span>
        <span class="leading-none"><span class="block text-xl font-extrabold tracking-wide">TRICODE</span>
        <span class="block pt-0.5 text-[0.6rem] font-semibold uppercase tracking-[0.32em] text-sky-300">Academy</span></span>
      </a>
      <p class="mt-4 max-w-xs text-sm leading-relaxed text-white/70">Education, Technology, Innovation. Practical skills for the students of tomorrow.</p>
      <a href="apply.html" class="btn btn-light mt-6">Apply Now</a>
    </div>
    <div>
      <h2 class="footer-h">Explore</h2>
      <ul class="footer-list">
        <li><a href="about.html">About Us</a></li><li><a href="courses.html">Courses</a></li>
        <li><a href="programs.html">Programs &amp; Fees</a></li><li><a href="teachers.html">Teachers</a></li>
        <li><a href="gallery.html">Gallery</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Students</h2>
      <ul class="footer-list">
        <li><a href="apply.html">Apply Online</a></li><li><a href="rules.html">Rules &amp; Regulations</a></li>
        <li><a href="contact.html">Contact &amp; Location</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Contact</h2>
      <ul class="footer-list">
        <li class="text-white/60">Address: to be added</li>
        <li class="text-white/60">Phone / WhatsApp: to be added</li>
        <li class="text-white/60">Email: to be added</li>
        <li>Classes Mon&ndash;Fri, 4:00&ndash;6:20 PM</li>
      </ul>
    </div>
  </div>
  <div class="border-t border-white/10">
    <div class="container-x flex flex-col gap-2 py-5 text-xs text-white/60 sm:flex-row sm:justify-between">
      <p>&copy; 2026 TRICODE Academy. All rights reserved.</p>
      <p>Education &middot; Technology &middot; Innovation</p>
    </div>
  </div>
</footer>'''

def page(fname, title, desc, body, active=None):
    html = '''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="theme-color" content="#272665">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TRICODE Academy">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(site)s/%(fname)s">
<meta property="og:image" content="%(site)s/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="%(site)s/%(fname)s">
<link rel="icon" type="image/png" href="assets/img/logo-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script>document.documentElement.classList.add('js');</script>
<script src="https://cdn.tailwindcss.com"></script>
<script src="assets/js/tailwind-config.js"></script>
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="bg-white font-sans text-slate-600 antialiased">
%(header)s
<main id="main">
%(body)s
</main>
%(footer)s
<script src="assets/js/main.js" defer></script>
</body>
</html>
''' % dict(title=title, desc=desc, site=SITE, fname=fname, header=header(active or fname), body=body, footer=FOOTER)
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)

# ---------- reusable blocks ----------
def eyebrow(t):
    return '<p class="eyebrow">%s</p>' % t

def section_head(eb, title, sub="", center=False):
    c = " text-center mx-auto" if center else ""
    s = '<p class="mt-4 text-base leading-relaxed text-slate-600 sm:text-lg">%s</p>' % sub if sub else ""
    return '<div class="max-w-2xl reveal%s">%s<h2 class="h2 mt-3">%s</h2>%s</div>' % (c, eyebrow(eb), title, s)

def page_hero(eb, title, sub):
    return '''<section class="page-hero">
  <div class="container-x relative py-14 sm:py-20">
    <p class="eyebrow !text-sky-200">%s</p>
    <h1 class="mt-3 max-w-3xl text-[2rem] font-extrabold leading-[1.1] tracking-tight text-white sm:text-5xl">%s</h1>
    <p class="mt-4 max-w-2xl text-base leading-relaxed text-white/75 sm:text-lg">%s</p>
  </div>
</section>''' % (eb, title, sub)

def cta_band():
    return '''<section class="py-16 sm:py-24">
  <div class="container-x">
    <div class="cta-card reveal">
      <div class="relative max-w-xl">
        <h2 class="text-[1.75rem] font-extrabold leading-tight text-white sm:text-4xl">Start building skills that matter.</h2>
        <p class="mt-3 text-base text-white/75 sm:text-lg">Choose a course, pick a class shift and join TRICODE Academy. Applying takes only a few minutes.</p>
        <div class="mt-7 flex flex-col gap-3 sm:flex-row">
          <a href="apply.html" class="btn btn-light">Apply Now %s</a>
          <a href="programs.html" class="btn btn-ghost">View Programs &amp; Fees</a>
        </div>
      </div>
    </div>
  </div>
</section>''' % ic("arrow", "h-4 w-4")

MAIN_COURSES = [
 ("Web Development", "code", "Learn to design and build modern, responsive websites from the ground up."),
 ("Java / Android", "phone-app", "Learn Java programming and move on to building Android applications."),
 ("Python", "terminal", "A clear, beginner-friendly route into programming and problem solving."),
 ("C#", "hash", "Structured programming with C# for building real software."),
 ("Graphic Design", "pen", "Create logos, posters and social media visuals with professional design tools."),
 ("Video Editing", "video", "Cut, edit and finish videos with industry-standard editing workflows."),
]
SHORT_COURSES = [
 ("AI Power Pack", "spark", "Practical, hands-on skills for using AI tools in study and work."),
 ("WordPress + WooCommerce", "cart", "Build and manage websites and online stores with WordPress."),
 ("CIT / MS Office", "file", "Essential computer and office skills: Word, Excel and PowerPoint."),
 ("Digital Marketing", "megaphone", "Understand how businesses reach customers and grow online."),
]

def course_card(name, icon, desc, kind):
    if kind == "main":
        meta = ('<ul class="mt-5 flex flex-wrap gap-2 text-xs font-semibold">'
                '<li class="chip">3 levels: Basic &middot; Mid &middot; Advance</li>'
                '<li class="chip">40-min classes</li><li class="chip">Mon&ndash;Fri</li></ul>')
        tag = "Main course"
    else:
        meta = ('<ul class="mt-5 flex flex-wrap gap-2 text-xs font-semibold">'
                '<li class="chip">Short course</li><li class="chip chip-soft">Duration &amp; fee: to be confirmed</li></ul>')
        tag = "Short course"
    return '''<article class="card group flex h-full flex-col reveal">
  <div class="flex items-start justify-between">
    <span class="icon-tile">%s</span>
    <span class="text-[0.7rem] font-bold uppercase tracking-widest text-brand-blue/80">%s</span>
  </div>
  <h3 class="mt-5 text-lg font-bold text-navy">%s</h3>
  <p class="mt-2 flex-1 text-[0.95rem] leading-relaxed">%s</p>
  %s
  <a href="apply.html" class="mt-6 inline-flex items-center gap-2 text-sm font-bold text-brand-mid transition group-hover:gap-3 hover:text-navy">Apply for this course %s</a>
</article>''' % (ic(icon, "h-6 w-6"), tag, name, desc, meta, ic("arrow", "h-4 w-4"))

def programs_block(compact=False):
    def plan(level, months, monthly, total, full, note=""):
        tot = ('<div class="row"><dt>Total fee</dt><dd>%s</dd></div>' % total) if total else \
              '<div class="row"><dt>Total fee</dt><dd class="text-slate-500 text-sm font-semibold">To be confirmed</dd></div>'
        fullrow = ('<div class="row"><dt>Pay in full</dt><dd class="text-brand-mid">%s</dd></div>' % full) if full else \
                  '<div class="row"><dt>Pay in full</dt><dd class="text-slate-500 text-sm font-semibold">To be confirmed</dd></div>'
        return '''<article class="plan reveal">
  <p class="text-xs font-bold uppercase tracking-[0.25em] text-brand-blue">%s</p>
  <p class="mt-3 text-3xl font-extrabold text-navy">%s<span class="text-base font-semibold text-slate-500"> / month</span></p>
  <p class="mt-1 text-sm font-semibold text-slate-500">%s duration</p>
  <dl class="mt-6 divide-y divide-navy/10 border-t border-navy/10">
    <div class="row"><dt>Duration</dt><dd>%s</dd></div>
    <div class="row"><dt>Monthly fee</dt><dd>%s</dd></div>
    %s%s
  </dl>
  <a href="apply.html" class="btn btn-primary mt-6 w-full">Apply for %s</a>
</article>''' % (level, monthly, months, months, monthly, tot, fullrow, level)
    plans = (plan("Basic", "2 months", "Rs. 2,000", "Rs. 4,000", "Rs. 3,500") +
             plan("Mid", "4 months", "Rs. 2,500", None, None) +
             plan("Advance", "6 months", "Rs. 3,000", "Rs. 18,000", "Rs. 17,000"))
    shifts = ""
    for n, t in [(1, "4:00 &ndash; 4:40 PM"), (2, "4:50 &ndash; 5:30 PM"), (3, "5:40 &ndash; 6:20 PM")]:
        shifts += '''<div class="shift reveal"><span class="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-navy text-sm font-extrabold text-white">%d</span>
<div><p class="text-xs font-bold uppercase tracking-widest text-brand-blue">Shift %d</p><p class="text-lg font-bold text-navy">%s</p></div></div>''' % (n, n, t)
    days = "".join('<span class="chip">%s</span>' % d for d in ["Mon", "Tue", "Wed", "Thu", "Fri"])
    return '''<div class="grid gap-5 md:grid-cols-3">%s</div>
<div class="mt-10 rounded-3xl border border-navy/10 bg-brand-mist p-6 sm:p-8 reveal">
  <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
    <div><h3 class="text-xl font-bold text-navy">Class timetable</h3>
    <p class="mt-1 text-sm">Each class is 40 minutes. Choose the shift that suits you.</p></div>
    <div class="flex flex-wrap gap-2">%s</div>
  </div>
  <div class="mt-6 grid gap-3 sm:grid-cols-3">%s</div>
</div>''' % (plans, days, shifts)

# ---------- HOME ----------
def hero_visual():
    return '''<div class="hero-visual" aria-hidden="true">
  <div class="glow glow-a"></div><div class="glow glow-b"></div>
  <div class="code-window">
    <div class="flex items-center gap-1.5 border-b border-white/10 px-4 py-3">
      <span class="h-2.5 w-2.5 rounded-full bg-white/25"></span><span class="h-2.5 w-2.5 rounded-full bg-white/25"></span><span class="h-2.5 w-2.5 rounded-full bg-brand-cyan"></span>
      <span class="ml-3 text-[0.7rem] font-semibold tracking-wide text-white/50">tricode.academy</span>
    </div>
    <pre class="px-5 py-4 text-[0.72rem] leading-6 sm:text-[0.8rem] sm:leading-7"><code><span class="t-dim">01</span>  <span class="t-key">const</span> student = {
<span class="t-dim">02</span>    skills: [<span class="t-str">"Web"</span>, <span class="t-str">"Python"</span>,
<span class="t-dim">03</span>             <span class="t-str">"Design"</span>, <span class="t-str">"Video"</span>],
<span class="t-dim">04</span>    learning: <span class="t-str">"practical"</span>,
<span class="t-dim">05</span>    ready: <span class="t-key">true</span>
<span class="t-dim">06</span>  };</code></pre>
  </div>
  <div class="float-chip chip-1">%s<span>Web Development</span></div>
  <div class="float-chip chip-2">%s<span>Graphic Design</span></div>
  <div class="float-chip chip-3">%s<span>Python</span></div>
</div>''' % (ic("code", "h-4 w-4"), ic("pen", "h-4 w-4"), ic("terminal", "h-4 w-4"))

def home():
    why = [("laptop", "Practical Learning", "Learn by doing. Every class focuses on skills you can use."),
           ("users", "Expert Teachers", "Guidance from instructors who teach technology and creative skills."),
           ("monitor", "Modern Lab", "A computer lab where each student gets real hands-on time."),
           ("briefcase", "Job-Ready Skills", "Skills chosen for study, freelancing and the modern workplace.")]
    why_html = ""
    for i, t, d in why:
        icon = {"laptop": "monitor"}.get(i, i)
        why_html += '<div class="reveal"><span class="icon-tile">%s</span><h3 class="mt-4 text-lg font-bold text-navy">%s</h3><p class="mt-2 text-[0.95rem] leading-relaxed">%s</p></div>' % (ic(icon, "h-6 w-6"), t, d)
    cards = "".join(course_card(n, i, d, "main") for n, i, d in MAIN_COURSES)
    people = ""
    for role, label in [("Administrator", "Admin"), ("Instructor", "Teacher"), ("Instructor", "Teacher")]:
        people += '''<article class="card reveal text-center"><div class="avatar mx-auto">%s</div>
<h3 class="mt-4 text-lg font-bold text-navy">Name to be added</h3><p class="text-sm font-semibold text-brand-mid">%s</p></article>''' % (ic("user", "h-10 w-10"), role)
    gal = ""
    for i in range(4):
        gal += '<div class="ph-tile aspect-square reveal">%s<span>Academy photo</span></div>' % ic("camera", "h-6 w-6")
    return '''
<section class="hero">
  <div class="hero-grid" aria-hidden="true"></div>
  <div class="container-x relative grid items-center gap-10 py-12 sm:py-16 lg:grid-cols-[1.05fr_0.95fr] lg:gap-14 lg:py-24">
    <div>
      <p class="inline-flex items-center gap-2 rounded-full border border-brand-blue/30 bg-white/70 px-3.5 py-1.5 text-[0.72rem] font-bold uppercase tracking-[0.18em] text-navy backdrop-blur">
        <span class="h-1.5 w-1.5 rounded-full bg-brand-cyan"></span>Education &middot; Technology &middot; Innovation</p>
      <h1 class="mt-5 text-[2.15rem] font-extrabold leading-[1.08] tracking-tight text-navy sm:text-5xl lg:text-[3.4rem]">
        Learn practical tech &amp; creative skills that <span class="grad-text">build your future.</span></h1>
      <p class="mt-5 max-w-xl text-base leading-relaxed sm:text-lg">TRICODE Academy teaches web development, programming, graphic design and video editing through hands-on classes, so students leave with skills they can actually use.</p>
      <div class="mt-8 flex flex-col gap-3 sm:flex-row">
        <a href="apply.html" class="btn btn-primary">Apply Now %s</a>
        <a href="courses.html" class="btn btn-outline">Explore Courses</a>
      </div>
      <dl class="mt-9 grid max-w-md grid-cols-3 gap-4 border-t border-navy/10 pt-6">
        <div><dt class="text-xs font-semibold uppercase tracking-wider text-slate-500">Courses</dt><dd class="text-2xl font-extrabold text-navy">10</dd></div>
        <div><dt class="text-xs font-semibold uppercase tracking-wider text-slate-500">Levels</dt><dd class="text-2xl font-extrabold text-navy">3</dd></div>
        <div><dt class="text-xs font-semibold uppercase tracking-wider text-slate-500">Class days</dt><dd class="text-2xl font-extrabold text-navy">Mon&ndash;Fri</dd></div>
      </dl>
    </div>
    %s
  </div>
</section>

<section class="py-16 sm:py-24">
  <div class="container-x">
    %s
    <div class="mt-10 grid gap-8 sm:grid-cols-2 lg:grid-cols-4 lg:gap-10">%s</div>
  </div>
</section>

<section class="bg-brand-mist py-16 sm:py-24">
  <div class="container-x">
    <div class="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
      %s
      <a href="courses.html" class="link-arrow reveal">All courses %s</a>
    </div>
    <div class="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">%s</div>
  </div>
</section>

<section class="py-16 sm:py-24">
  <div class="container-x grid items-center gap-10 lg:grid-cols-2 lg:gap-16">
    <div class="about-visual reveal" aria-hidden="true">
      <img src="assets/img/logo-mark.png" alt="" class="relative z-10 h-28 w-28 sm:h-36 sm:w-36" loading="lazy">
    </div>
    <div class="reveal">
      %s<h2 class="h2 mt-3">A modern academy built around practical skills.</h2>
      <p class="mt-4 text-base leading-relaxed sm:text-lg">TRICODE Academy brings education, technology and innovation together. We teach the skills students need in today&rsquo;s digital world, in a friendly environment with a practical, step-by-step approach.</p>
      <a href="about.html" class="btn btn-outline mt-7">Read our story %s</a>
    </div>
  </div>
</section>

<section class="bg-brand-mist py-16 sm:py-24">
  <div class="container-x">
    <div class="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
      %s
      <a href="programs.html" class="link-arrow reveal">Full programs %s</a>
    </div>
    <div class="mt-10">%s</div>
  </div>
</section>

<section class="py-16 sm:py-24">
  <div class="container-x">
    <div class="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
      %s
      <a href="teachers.html" class="link-arrow reveal">Meet everyone %s</a>
    </div>
    <div class="mt-10 grid gap-5 sm:grid-cols-3">%s</div>
  </div>
</section>

<section class="bg-brand-mist py-16 sm:py-24">
  <div class="container-x">
    <div class="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
      %s
      <a href="gallery.html" class="link-arrow reveal">Open gallery %s</a>
    </div>
    <div class="mt-10 grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4">%s</div>
  </div>
</section>

<section class="py-16 sm:py-24">
  <div class="container-x grid gap-8 lg:grid-cols-2 lg:gap-12">
    <div class="reveal">
      %s<h2 class="h2 mt-3">Visit or contact us</h2>
      <ul class="mt-6 space-y-4">
        <li class="contact-row">%s<span>Address: <em class="not-italic text-slate-500">to be added</em></span></li>
        <li class="contact-row">%s<span>Phone: <em class="not-italic text-slate-500">to be added</em></span></li>
        <li class="contact-row">%s<span>WhatsApp: <em class="not-italic text-slate-500">to be added</em></span></li>
        <li class="contact-row">%s<span>Classes Monday&ndash;Friday, 4:00&ndash;6:20 PM</span></li>
      </ul>
      <a href="contact.html" class="btn btn-outline mt-7">Contact &amp; directions</a>
    </div>
    <div class="map-box reveal" role="img" aria-label="Map placeholder: location to be added">%s<p class="font-bold text-navy">Map coming soon</p><p class="text-sm">The verified academy location will appear here.</p></div>
  </div>
</section>
%s''' % (ic("arrow", "h-4 w-4"), hero_visual(),
         section_head("Why TRICODE", "Learning that leads somewhere.", "Four reasons students and parents choose us."), why_html,
         section_head("Courses", "Skills for the digital world.", "Six main courses to build deep skills."), ic("arrow", "h-4 w-4"), cards,
         eyebrow("About TRICODE"), ic("arrow", "h-4 w-4"),
         section_head("Programs", "Clear levels. Simple fees.", "Pick a level, pick a shift, start learning."), ic("arrow", "h-4 w-4"), programs_block(),
         section_head("Teachers", "Meet the people behind TRICODE."), ic("arrow", "h-4 w-4"), people,
         section_head("Gallery", "Life at the academy."), ic("arrow", "h-4 w-4"), gal,
         eyebrow("Location &amp; Contact"), ic("pin", "h-5 w-5"), ic("phone", "h-5 w-5"), ic("chat", "h-5 w-5"), ic("clock", "h-5 w-5"),
         ic("pin", "h-8 w-8"), cta_band())

page("index.html", "TRICODE Academy | Practical Technology & Creative Skills",
     "TRICODE Academy teaches web development, Java, Python, C#, graphic design and video editing with hands-on classes. Apply online today.",
     home())

# ---------- ABOUT ----------
def about():
    pillars = [("target", "Our Mission", "Draft: To give every student practical, job-ready technology and creative skills through clear, hands-on teaching."),
               ("eye", "Our Vision", "Draft: To be a trusted academy where education, technology and innovation come together to prepare confident learners.")]
    pil = "".join('<article class="card reveal"><span class="icon-tile">%s</span><h3 class="mt-5 text-xl font-bold text-navy">%s</h3><p class="mt-2 leading-relaxed">%s</p></article>' % (ic(i, "h-6 w-6"), t, d) for i, t, d in pillars)
    steps = [("Learn the idea", "Short, clear explanations in each 40-minute class."), ("Practise on a computer", "Students apply it straight away in the lab."),
             ("Build and improve", "Small tasks grow into real, usable skills."), ("Level up", "Move from Basic to Mid to Advance at your own pace.")]
    st = "".join('<li class="flex gap-4 reveal"><span class="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-navy text-sm font-extrabold text-white">%d</span><div><h3 class="font-bold text-navy">%s</h3><p class="mt-1 text-[0.95rem]">%s</p></div></li>' % (i + 1, a, b) for i, (a, b) in enumerate(steps))
    why = "".join('<li class="flex items-start gap-3">%s<span>%s</span></li>' % ('<span class="mt-0.5 grid h-6 w-6 shrink-0 place-items-center rounded-full bg-brand-cyan/15 text-brand-mid">' + ic("check", "h-3.5 w-3.5") + '</span>', t)
                  for t in ["Practical, hands-on learning in every class", "Three clear levels: Basic, Mid and Advance", "Flexible class shifts, Monday to Friday", "Technology and creative courses in one academy"])
    return page_hero("About Us", "Education, technology and innovation, together.", "The story and approach behind TRICODE Academy.") + '''
<section class="py-16 sm:py-24">
  <div class="container-x grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:gap-16">
    <div class="reveal">
      %s<h2 class="h2 mt-3">Our story</h2>
      <p class="mt-5 text-lg leading-relaxed text-navy/90">TRICODE Academy was created to give students a modern, practical place to learn technology and creative skills.</p>
      <p class="mt-4 leading-relaxed">Our name and our logo reflect three ideas that guide everything we teach: education, technology and innovation. Students come to learn skills such as web development, programming, graphic design and video editing in a friendly, focused environment.</p>
      <p class="mt-4 rounded-2xl border border-dashed border-brand-blue/40 bg-brand-mist p-4 text-sm text-slate-600"><strong class="text-navy">Content note:</strong> Founding year, founder&rsquo;s message and milestones will be added once supplied by the academy.</p>
    </div>
    <div class="about-visual reveal min-h-[260px]" aria-hidden="true"><img src="assets/img/logo-mark.png" alt="" class="relative z-10 h-32 w-32 sm:h-44 sm:w-44" loading="lazy"></div>
  </div>
</section>
<section class="bg-brand-mist py-16 sm:py-24">
  <div class="container-x grid gap-5 md:grid-cols-2">%s</div>
</section>
<section class="py-16 sm:py-24">
  <div class="container-x grid gap-12 lg:grid-cols-2 lg:gap-16">
    <div>%s<ul class="mt-8 space-y-4 reveal">%s</ul></div>
    <div>%s<ol class="mt-8 space-y-6">%s</ol></div>
  </div>
</section>
%s''' % (eyebrow("Academy Introduction"), pil, section_head("Why TRICODE", "What makes us different."), why,
         section_head("Teaching Approach", "Practical, step by step."), st, cta_band())

page("about.html", "About Us | TRICODE Academy", "Learn the story, mission, vision and practical teaching approach behind TRICODE Academy.", about())

# ---------- COURSES ----------
def courses():
    m = "".join(course_card(n, i, d, "main") for n, i, d in MAIN_COURSES)
    s = "".join(course_card(n, i, d, "short") for n, i, d in SHORT_COURSES)
    return page_hero("Courses", "Skills for the digital world.", "Six main courses and four short courses, taught practically.") + '''
<section class="py-16 sm:py-24"><div class="container-x">
  %s<div class="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">%s</div>
  <p class="mt-6 text-sm reveal">All main courses run across three levels (Basic, Mid, Advance). See <a href="programs.html" class="font-bold text-brand-mid underline underline-offset-4">Programs &amp; Fees</a>.</p>
</div></section>
<section class="bg-brand-mist py-16 sm:py-24"><div class="container-x">
  %s<div class="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">%s</div>
  <p class="mt-6 text-sm reveal">Short-course duration, fee and detailed outcomes will be added once confirmed by the academy.</p>
</div></section>
%s''' % (section_head("Main Courses", "Build deep, lasting skills."), m, section_head("Short Courses", "Focused skills, faster."), s, cta_band())

page("courses.html", "Courses | TRICODE Academy", "Web Development, Java/Android, Python, C#, Graphic Design, Video Editing plus short courses in AI, WordPress, MS Office and Digital Marketing.", courses())

# ---------- PROGRAMS ----------
def programs():
    return page_hero("Programs", "Fees & timetable in one place.", "Three levels, simple monthly fees and three daily class shifts.") + '''
<section class="py-16 sm:py-24"><div class="container-x">%s<div class="mt-10">%s</div>
<p class="mt-6 text-sm reveal">The Mid-level total fee is awaiting confirmation and is not published yet. Please contact the academy for details.</p></div></section>
%s''' % (section_head("Levels & Fees", "Choose your level."), programs_block(), cta_band())

page("programs.html", "Programs, Fees & Timetable | TRICODE Academy", "TRICODE Academy levels, fees and class timetable. Basic, Mid and Advance programs, Monday to Friday in three shifts.", programs(), "programs.html")

# ---------- TEACHERS ----------
def teachers():
    def card(role, subject):
        return '''<article class="card reveal overflow-hidden !p-0"><div class="ph-photo relative aspect-[4/3]">
<img src="assets/img/team/PLACEHOLDER.jpg" alt="" class="absolute inset-0 h-full w-full object-cover" loading="lazy" onerror="this.remove()">
<span class="grid place-items-center text-brand-blue/60">%s</span></div>
<div class="p-6"><h3 class="text-lg font-bold text-navy">Name to be added</h3><p class="text-sm font-semibold text-brand-mid">%s</p>
<p class="mt-1 text-sm text-slate-500">Subject: %s</p><p class="mt-3 text-[0.95rem]">Short biography will appear here once approved.</p></div></article>''' % (ic("user", "h-14 w-14"), role, subject)
    return page_hero("Teachers", "The people behind TRICODE.", "Our admin and instructors in one place.") + '''
<section class="py-16 sm:py-24"><div class="container-x">
  %s<div class="mt-8 grid gap-5 sm:max-w-sm">%s</div>
  <div class="mt-16">%s<div class="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">%s</div></div>
  <p class="mt-8 text-sm reveal">Photos, names, qualifications and bios are shown only after approval by each person.</p>
</div></section>
%s''' % (section_head("Admin", "Academy administration"), card("Administrator", "Academy management"),
         section_head("Instructors", "Our teachers"), card("Instructor", "To be added") * 3, cta_band())

page("teachers.html", "Teachers | TRICODE Academy", "Meet the administrator and instructors of TRICODE Academy.", teachers())

# ---------- GALLERY ----------
def gallery():
    items = [("Computer lab", "tall"), ("Classroom", ""), ("Events", ""), ("Students at work", "tall"), ("Activities", ""), ("Student projects", ""), ("Academy", ""), ("Workshops", "")]
    out = ""
    for i, (label, kind) in enumerate(items, 1):
        span = "row-span-2" if kind == "tall" else ""
        out += '''<figure class="gallery-item %s reveal"><button type="button" class="gallery-btn" data-label="%s" aria-label="Open photo: %s">
<span class="ph-tile absolute inset-0">%s<span>%s</span></span>
<img src="assets/img/gallery/gallery-%02d.jpg" alt="TRICODE Academy: %s" class="absolute inset-0 h-full w-full object-cover" loading="lazy" onerror="this.remove()">
</button></figure>''' % (span, label, label, ic("camera", "h-6 w-6"), label, i, label)
    return page_hero("Gallery", "Life at TRICODE Academy.", "Classroom, lab, events and student activities.") + '''
<section class="py-16 sm:py-24"><div class="container-x">
  <div class="gallery-grid">%s</div>
  <p class="mt-8 text-sm reveal">Real academy photos will replace these tiles. Save images as <code>assets/img/gallery/gallery-01.jpg</code>, <code>gallery-02.jpg</code> and so on. Student photos are used only with permission.</p>
</div></section>
<div id="lightbox" class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button type="button" class="lightbox-close" aria-label="Close photo viewer">%s</button>
  <img id="lightbox-img" src="" alt="">
</div>
%s''' % (out, ic("x", "h-6 w-6"), cta_band())

page("gallery.html", "Gallery | TRICODE Academy", "Photos from TRICODE Academy: classroom, computer lab, events and student activities.", gallery())

# ---------- RULES ----------
def rules():
    cats = [("clock", "Attendance & Timing", ["Classes run Monday to Friday in 40-minute shifts.", "Shift 1: 4:00-4:40 PM. Shift 2: 4:50-5:30 PM. Shift 3: 5:40-6:20 PM.", "Attendance and late-arrival rules: to be supplied by the academy."]),
            ("users", "Conduct", ["Respect for teachers, staff and fellow students.", "Care of computers and academy property.", "Full conduct rules: to be supplied by the academy."]),
            ("smartphone", "Mobile Phones", ["Mobile phone policy: to be supplied by the academy."]),
            ("wallet", "Fees & Payments", ["Fees are listed on the Programs page.", "Pay-in-full options are available for Basic and Advance levels.", "Due dates and refund rules: to be supplied by the academy."]),
            ("shield", "Other Rules", ["Additional academy rules: to be supplied by the academy."])]
    out = ""; n = 1
    for icon, title, items in cats:
        lis = ""
        for it in items:
            pending = "to be supplied" in it
            cls = "text-slate-400" if pending else ""
            lis += '<li class="flex gap-3"><span class="num">%02d</span><span class="%s">%s</span></li>' % (n, cls, it); n += 1
        out += '<article class="card reveal"><div class="flex items-center gap-3"><span class="icon-tile">%s</span><h2 class="text-lg font-bold text-navy">%s</h2></div><ul class="mt-5 space-y-3 text-[0.95rem]">%s</ul></article>' % (ic(icon, "h-6 w-6"), title, lis)
    return page_hero("Rules & Regulations", "Simple rules for a great learning space.", "Please read these before joining.") + '''
<section class="py-16 sm:py-24"><div class="container-x"><div class="grid gap-5 md:grid-cols-2">%s</div></div></section>
%s''' % (out, cta_band())

page("rules.html", "Rules & Regulations | TRICODE Academy", "Attendance, timing, conduct, phone and fee rules for students at TRICODE Academy.", rules(), "rules.html")

# ---------- CONTACT ----------
def contact():
    def row(icon, label, val):
        return '<li class="card flex items-start gap-4 reveal !p-5"><span class="icon-tile !h-11 !w-11 shrink-0">%s</span><div><p class="text-xs font-bold uppercase tracking-widest text-brand-blue">%s</p><p class="mt-1 font-semibold text-navy">%s</p></div></li>' % (ic(icon, "h-5 w-5"), label, val)
    tbd = '<span class="text-slate-400">To be added</span>'
    return page_hero("Contact", "We would love to hear from you.", "Visit the academy, call or message us on WhatsApp.") + '''
<section class="py-16 sm:py-24"><div class="container-x grid gap-8 lg:grid-cols-[0.9fr_1.1fr] lg:gap-12">
  <ul class="space-y-4">%s%s%s%s%s</ul>
  <div>
    <!-- MAP: when the verified location is supplied, replace the placeholder block below with:
    <iframe src="GOOGLE_MAPS_EMBED_URL" title="TRICODE Academy location" class="h-full w-full rounded-3xl border-0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe> -->
    <div class="map-box aspect-[4/3] sm:aspect-[16/10] reveal" role="img" aria-label="Map placeholder: location to be added">%s<p class="font-bold text-navy">Map coming soon</p><p class="max-w-xs text-sm">The verified academy location and directions will appear here.</p></div>
    <a href="#" class="btn btn-outline mt-5 w-full pointer-events-none opacity-60 sm:w-auto" aria-disabled="true" tabindex="-1">%s Get directions (coming soon)</a>
  </div>
</div></section>
%s''' % (row("pin", "Address", tbd), row("phone", "Phone", tbd), row("chat", "WhatsApp", tbd), row("mail", "Email", tbd),
         row("clock", "Class timings", "Monday&ndash;Friday<br><span class='text-sm font-medium text-slate-600'>4:00&ndash;4:40, 4:50&ndash;5:30, 5:40&ndash;6:20 PM</span>"),
         ic("pin", "h-8 w-8"), ic("pin", "h-4 w-4"), cta_band())

page("contact.html", "Contact & Location | TRICODE Academy", "Contact TRICODE Academy: address, phone, WhatsApp, class timings and map.", contact())

# ---------- APPLY ----------
def apply_page():
    def field(id_, label, type_="text", req=True, ac="", ph=""):
        r = ' required' if req else ''
        star = ' <span class="text-brand-mid" aria-hidden="true">*</span>' if req else ''
        a = ' autocomplete="%s"' % ac if ac else ''
        return '<div><label for="%s" class="label">%s%s</label><input id="%s" name="%s" type="%s"%s%s placeholder="%s" class="input"></div>' % (id_, label, star, id_, id_, type_, r, a, ph)
    opts = lambda items: "".join('<option value="%s">%s</option>' % (i, i) for i in items)
    courses = ["Web Development", "Java / Android", "Python", "C#", "Graphic Design", "Video Editing", "AI Power Pack", "WordPress + WooCommerce", "CIT / MS Office", "Digital Marketing"]
    return page_hero("Apply Online", "Apply to TRICODE Academy.", "Fill in the form below. It only takes a couple of minutes.") + '''
<section class="py-14 sm:py-20"><div class="container-x grid gap-10 lg:grid-cols-[1.2fr_0.8fr] lg:gap-14">
  <!-- FORM: set data-endpoint to the official Google Form / form-handler URL when supplied. -->
  <form id="apply-form" class="space-y-5 reveal" novalidate data-endpoint="" aria-describedby="form-status">
    <div class="grid gap-5 sm:grid-cols-2">%s%s%s%s</div>
    %s
    <div class="grid gap-5 sm:grid-cols-2">
      <div><label for="course" class="label">Course <span class="text-brand-mid" aria-hidden="true">*</span></label><select id="course" name="course" required class="input"><option value="">Select a course</option>%s</select></div>
      <div><label for="level" class="label">Level <span class="text-brand-mid" aria-hidden="true">*</span></label><select id="level" name="level" required class="input"><option value="">Select a level</option>%s</select></div>
    </div>
    <div><label for="shift" class="label">Preferred class shift <span class="text-brand-mid" aria-hidden="true">*</span></label><select id="shift" name="shift" required class="input"><option value="">Select a shift</option>%s</select></div>
    <div><label for="message" class="label">Message (optional)</label><textarea id="message" name="message" rows="3" class="input" placeholder="Anything you would like us to know"></textarea></div>
    <div class="hidden" aria-hidden="true"><label>Leave empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
    <button type="submit" class="btn btn-primary w-full sm:w-auto">Submit application %s</button>
    <p id="form-status" class="text-sm font-semibold" role="status" aria-live="polite"></p>
  </form>
  <aside class="space-y-4 reveal">
    <div class="card"><h2 class="text-lg font-bold text-navy">Before you apply</h2>
      <ul class="mt-4 space-y-3 text-[0.95rem]"><li class="flex gap-3">%s<span>Choose a course and level.</span></li><li class="flex gap-3">%s<span>Pick a class shift (Mon&ndash;Fri).</span></li><li class="flex gap-3">%s<span>Check fees on the <a class="font-bold text-brand-mid underline underline-offset-4" href="programs.html">Programs page</a>.</span></li></ul></div>
    <p class="text-sm">Form fields can be matched to the academy&rsquo;s official admission form once it is supplied.</p>
  </aside>
</div></section>''' % (
        field("fullname", "Student full name", ac="name"), field("guardian", "Father / guardian name"),
        field("phone", "Phone / WhatsApp", "tel", ac="tel"), field("email", "Email (optional)", "email", False, "email"),
        field("city", "City / area", req=False, ac="address-level2"),
        opts(courses), opts(["Basic (2 months)", "Mid (4 months)", "Advance (6 months)"]),
        opts(["Shift 1: 4:00-4:40 PM", "Shift 2: 4:50-5:30 PM", "Shift 3: 5:40-6:20 PM"]),
        ic("arrow", "h-4 w-4"),
        '<span class="text-brand-mid">%s</span>' % ic("check", "h-5 w-5"), '<span class="text-brand-mid">%s</span>' % ic("check", "h-5 w-5"), '<span class="text-brand-mid">%s</span>' % ic("check", "h-5 w-5"))

page("apply.html", "Apply Online | TRICODE Academy", "Apply online to TRICODE Academy. Choose your course, level and class shift in a simple form.", apply_page(), "apply.html")

# ---------- sitemap / robots ----------
pages = ["index", "about", "courses", "programs", "teachers", "gallery", "rules", "contact", "apply"]
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
            "".join("  <url><loc>%s/%s.html</loc></url>\n" % (SITE, p) for p in pages) + "</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)
print("built", len(pages), "pages")
