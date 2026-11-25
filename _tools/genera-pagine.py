#!/usr/bin/env python3
"""Genera le pagine /commercial /wedding /event /agenzie partendo da index.html.
Header, stili, lightbox, privacy, contatti, footer e script vengono copiati dalla home,
così restano sempre uguali. Rilanciare questo script dopo ogni modifica alla home:
    python3 _tools/genera-pagine.py
"""
import os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
BASE = 'https://federicogennaro.it'
WA = 'https://wa.me/393397305267?text='

def cut(s, start, end):
    a = s.index(start); b = s.index(end, a)
    return s[:a] + s[b:]

def card(slug):
    """Copia la card del portfolio della home."""
    i = SRC.index(f'data-project="{slug}"')
    a = SRC.rindex('<button', 0, i)
    b = SRC.index('</button>', i) + len('</button>')
    c = SRC[a:b].replace(' data-aos="fade-up"', '')
    return '          ' + c

PAGES = {
 'commercial': dict(
   title='Video Commercial e Reel a Ragusa — Federico Gennaro, Videomaker',
   desc='Spot, reel e contenuti social per aziende e brand. Videomaker a Modica, in provincia di Ragusa: riprese, montaggio e consegna pronta per i social.',
   kicker='Commercial', h1='Video che fanno<br>lavorare il tuo brand.',
   sub='Spot, reel e contenuti social per aziende e brand, dalla provincia di Ragusa.',
   imgs=['portfolio-polara.jpg','portfolio-tenuta-donna-fina.jpg','portfolio-despar.jpg'],
   works=['polara','tenuta-donna-fina','despar','ard-discount','cantina-frasca','ottica-moncada','ritratti-in-corso'],
   steps=[('Obiettivo','Partiamo da cosa deve ottenere il video, a chi parla e dove verrà pubblicato.'),
          ('Riprese','In sede o in esterna, con un set agile che non blocca il tuo lavoro.'),
          ('Montaggio e consegna','Video pronti per social e web, nei formati che ti servono.')],
   tipo='Commercial', wa='Ciao Federico, vorrei informazioni per un video commercial'),
 'wedding': dict(
   title='Videomaker Matrimoni a Ragusa — Federico Gennaro',
   desc='Video di matrimonio a Modica, Ragusa e in tutta la Sicilia. Il vostro giorno raccontato con discrezione ed emozione da Federico Gennaro, videomaker.',
   kicker='Wedding', h1='Il vostro giorno,<br>da rivivere ogni volta.',
   sub='Video di matrimonio raccontati con discrezione ed emozione.',
   imgs=['portfolio-carmelo-noemi.jpg','portfolio-vito-alice.jpg'],
   works=['carmelo-noemi','vito-alice'],
   steps=[('Ci conosciamo','Mi raccontate chi siete e come immaginate il vostro giorno.'),
          ('Il matrimonio','Ci sono, senza farmi notare, nei momenti che contano.'),
          ('Il vostro film','Un racconto montato con cura, da rivedere negli anni.')],
   tipo='Wedding', wa='Ciao Federico, vorrei informazioni per il video del nostro matrimonio'),
 'event': dict(
   title='Video Eventi e Aftermovie in Sicilia — Federico Gennaro, Videomaker',
   desc='Aftermovie, reel e contenuti per festival, serate, DJ set ed eventi aziendali. Videomaker a Modica (Ragusa), disponibile in tutta la Sicilia.',
   kicker='Event', h1="L'energia del tuo evento,<br>pronta per i social.",
   sub='Aftermovie e reel per festival, serate, DJ set ed eventi aziendali.',
   imgs=['portfolio-euphoria.jpg','portfolio-miami-music-week.jpg','portfolio-welcome-2023.jpg'],
   works=['welcome-2023','euphoria','miami-music-week-ade'],
   steps=[('Prima','Definiamo momenti chiave e contenuti da pubblicare.'),
          ('Durante','Palco, pubblico, dettagli: tutta l\'atmosfera della serata.'),
          ('Dopo','Aftermovie e reel pronti da pubblicare mentre se ne parla ancora.')],
   tipo='Event', wa='Ciao Federico, vorrei informazioni per il video di un evento'),
 'agenzie': dict(
   title='Videomaker per Agenzie di Comunicazione in Sicilia — Federico Gennaro',
   desc='Riprese e montaggio per le agenzie di comunicazione e i loro clienti. Videomaker con base a Modica (Ragusa), disponibile in tutta la Sicilia.',
   kicker='Per agenzie', h1='Il video per i tuoi clienti,<br>in buone mani.',
   sub='Collaboro con agenzie di comunicazione per riprese e montaggio dei loro progetti.',
   imgs=['portfolio-despar.jpg','portfolio-ard-discount.jpg','portfolio-euphoria.jpg'],
   works=['despar','ard-discount','polara','euphoria','tenuta-donna-fina','cantina-frasca'],
   works_title='Alcuni progetti',
   steps=[('Brief','Mi passi obiettivi e linee guida del cliente, io mi adatto al vostro stile.'),
          ('Produzione','Riprese e montaggio in autonomia, con un solo referente.'),
          ('Consegna','Contenuti pronti, nei formati che servono ai tuoi canali.')],
   tipo=None, wa='Ciao Federico, scrivo da un\'agenzia di comunicazione e vorrei collaborare'),
}

def build(slug, p):
    s = SRC
    # --- head: meta specifiche della pagina
    s = re.sub(r'<title>.*?</title>', f'<title>{html.escape(p["title"])}</title>', s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + html.escape(p['desc']), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + html.escape(p['title']), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + html.escape(p['desc']), s, count=1)
    s = s.replace('<meta property="og:url" content="https://federicogennaro.it/">', f'<meta property="og:url" content="{BASE}/{slug}/">')
    s = s.replace('<link rel="canonical" href="https://federicogennaro.it/">', f'<link rel="canonical" href="{BASE}/{slug}/">')
    a = s.index('<script type="application/ld+json">'); b = s.index('</script>', a) + len('</script>\n')
    s = s[:a] + s[b:]
    # --- togli le sezioni della home (dall'hero al portfolio, clienti, recensioni)
    s = cut(s, '  <!-- ================= HERO ================= -->', '  <!-- ================= VIDEO LIGHTBOX ================= -->')
    s = cut(s, '  <!-- ================= CLIENTI / LOGHI ================= -->', '  <!-- ================= CONTATTI ================= -->')
    # --- contenuto della pagina
    imgs = ''.join(f'<img src="/assets/images/{i}" alt="" loading="eager">' for i in p['imgs'])
    cards = '\n'.join(card(w) for w in p['works'])
    steps = ''.join(f'''
        <div class="pg-step" data-aos="fade-up" data-aos-delay="{n*80}">
          <span class="pg-step-n">0{n+1}</span>
          <h3>{t}</h3>
          <p>{d}</p>
        </div>''' for n, (t, d) in enumerate(p['steps']))
    wa = WA + p['wa'].replace(' ', '%20').replace("'", '%27').replace(',', '%2C')
    content = f'''  <!-- ================= PAGINA {slug.upper()} (generata da _tools/genera-pagine.py) ================= -->
  <section class="pg-hero">
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <a href="/" class="pg-back"><i data-lucide="arrow-left" class="h-4 w-4"></i>Home</a>
      <div class="pg-hero-grid">
        <div data-aos="fade-up">
          <span class="text-xs font-semibold uppercase tracking-[0.2em] text-acid">{p["kicker"]}</span>
          <h1 class="pg-h1">{p["h1"]}</h1>
          <p class="pg-sub">{p["sub"]}</p>
          <div class="pg-ctas">
            <a href="#contatti" class="pg-btn pg-btn-main">Raccontami il progetto <i data-lucide="arrow-up-right" class="h-4 w-4"></i></a>
            <a href="{wa}" target="_blank" rel="noopener" class="pg-btn pg-btn-ghost"><i class="fa-brands fa-whatsapp text-lg"></i>WhatsApp</a>
          </div>
        </div>
        <div class="cat-tile pg-reel" data-loop="" data-aos="fade-up" data-aos-delay="120">
          <div class="cat-media">{imgs}</div>
          <span class="cat-badge"><i></i>Showreel</span>
        </div>
      </div>
    </div>
  </section>

  <section id="portfolio" class="pg-sec relative scroll-mt-24">
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <h2 class="font-display font-bold text-2xl sm:text-3xl" data-aos="fade-up">{p.get("works_title", "Lavori")}</h2>
      <div class="pf-wrap relative -mx-5 sm:-mx-8">
        <div class="pf-arrows hidden"><button type="button" id="portfolio-prev"></button><button type="button" id="portfolio-next"></button></div>
        <div id="portfolio-scroll" class="no-scrollbar flex gap-6 overflow-x-auto snap-x snap-proximity scroll-smooth px-5 sm:px-8 pb-2">
{cards}
        </div>
      </div>
    </div>
  </section>

  <section class="pg-sec relative">
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <h2 class="font-display font-bold text-2xl sm:text-3xl" data-aos="fade-up">Come lavoro</h2>
      <div class="pg-steps">{steps}
      </div>
    </div>
  </section>

'''
    s = s.replace('  <!-- ================= VIDEO LIGHTBOX ================= -->', content + '  <!-- ================= VIDEO LIGHTBOX ================= -->', 1)
    # --- contatti: tipo di progetto già selezionato, WhatsApp con testo dedicato
    if p['tipo']:
        s = s.replace(f'value="{p["tipo"]}"', f'value="{p["tipo"]}" checked', 1)
    s = s.replace('https://wa.me/393397305267?text=Ciao%20Federico%2C%20vorrei%20informazioni%20per%20un%20progetto', wa)
    if slug == 'agenzie':
        s = s.replace('<p class="ct-label">Che tipo di progetto hai in mente?</p>', '<p class="ct-label">Per che tipo di progetto?</p>')
        s = s.replace('placeholder="Il tuo nome"', 'placeholder="Nome e agenzia"')
    s = s.replace('value="Nuovo messaggio dal sito federicogennaro.it"', f'value="Nuovo messaggio dal sito federicogennaro.it — pagina {p["kicker"]}"')
    s = s.replace('value="https://federicogennaro.it/?inviato=1#contatti"', f'value="{BASE}/{slug}/?inviato=1#contatti"')
    # --- link e percorsi: la pagina sta in una sottocartella
    s = s.replace('<a href="#top" aria-label="Federico Gennaro — torna in cima"', '<a href="/" aria-label="Federico Gennaro — home"')
    s = re.sub(r'''(src=|url\(|href=)(["']?)assets/''', r'\1\2/assets/', s)
    s = s.replace('data-poster="assets/', 'data-poster="/assets/')
    return s

CSS = '''<style id="pagine-categoria">
  .pg-hero{position:relative;padding:8rem 0 4rem}
  @media (min-width:640px){.pg-hero{padding:9.5rem 0 5rem}}
  .pg-back{display:inline-flex;align-items:center;gap:.4rem;font-size:.85rem;color:rgba(255,255,255,.55);margin-bottom:1.5rem;transition:color .2s}
  .pg-back:hover{color:#c6ff2e}
  .pg-hero-grid{display:grid;gap:2rem;align-items:center}
  @media (min-width:1024px){.pg-hero-grid{grid-template-columns:5fr 7fr;gap:3rem}}
  .pg-h1{margin-top:1rem;font-family:Benzin,system-ui,sans-serif;font-weight:800;font-size:clamp(2rem,4.2vw,3.4rem);line-height:1.05;letter-spacing:-.02em}
  .pg-sub{margin-top:1rem;color:rgba(255,255,255,.6);font-size:1.05rem;line-height:1.55;max-width:30rem}
  .pg-ctas{margin-top:1.75rem;display:flex;flex-wrap:wrap;gap:.75rem}
  .pg-btn{display:inline-flex;align-items:center;gap:.5rem;border-radius:9999px;padding:.85rem 1.4rem;font-weight:600;font-size:.95rem;transition:all .25s}
  .pg-btn-main{background:linear-gradient(to right,#c6ff2e,#7ed321);color:#0a0b0d;box-shadow:0 0 60px -12px rgba(198,255,46,.45)}
  .pg-btn-main:hover{opacity:.9}
  .pg-btn-ghost{border:1px solid rgba(255,255,255,.15);color:rgba(255,255,255,.9)}
  .pg-btn-ghost:hover{border-color:rgba(198,255,46,.6);color:#c6ff2e}
  .pg-reel{cursor:default}
  .pg-reel::after{background:linear-gradient(to top,rgba(10,11,13,.35),rgba(10,11,13,0) 50%)}
  .pg-sec{padding-bottom:4.5rem}
  @media (min-width:640px){.pg-sec{padding-bottom:6rem}}
  .pg-steps{margin-top:1.75rem;display:grid;gap:1rem}
  @media (min-width:768px){.pg-steps{grid-template-columns:repeat(3,minmax(0,1fr));gap:1.25rem}}
  .pg-step{border:1px solid #262936;background:#161922;border-radius:1.25rem;padding:1.5rem}
  .pg-step-n{font-size:.75rem;letter-spacing:.2em;font-weight:600;color:#c6ff2e}
  .pg-step h3{margin-top:.6rem;font-family:Benzin,system-ui,sans-serif;font-weight:700;font-size:1.1rem}
  .pg-step p{margin-top:.5rem;font-size:.9rem;line-height:1.55;color:rgba(255,255,255,.55)}
</style>
'''

for slug, p in PAGES.items():
    out = build(slug, p).replace('</head>', CSS + '</head>', 1)
    os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
    open(os.path.join(ROOT, slug, 'index.html'), 'w', encoding='utf-8').write(out)
    print('scritta', slug + '/index.html')
