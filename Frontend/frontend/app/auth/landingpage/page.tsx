"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Anton, Inter, JetBrains_Mono } from "next/font/google";
import "./landingpage.css";

const display = Anton({ subsets: ["latin"], weight: "400", variable: "--font-display" });
const body = Inter({ subsets: ["latin"], variable: "--font-body" });
const mono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

type Theme = "light" | "dark";

const SERVICES = [
  {
    tag: "SKU-01",
    title: "Inventory Control",
    copy: "Know what's on the shelf before the customer does. Live stock counts across every store, synced to the second.",
  },
  {
    tag: "SKU-02",
    title: "Point of Sale",
    copy: "Ring up sales in seconds, online or in-store, with receipts, returns and refunds that reconcile themselves.",
  },
  {
    tag: "SKU-03",
    title: "Multi-Store Management",
    copy: "One tenant, every branch, one till tape. Switch storefronts without switching software.",
  },
  {
    tag: "SKU-04",
    title: "Staff & Payroll",
    copy: "Shifts, attendance, leave and payroll, sorted for every employee on the floor or in the back office.",
  },
  {
    tag: "SKU-05",
    title: "Sales Analytics",
    copy: "Reports that read like a receipt, not a riddle. Forecast demand before you run out, or overstock.",
  },
  {
    tag: "SKU-06",
    title: "Customer Ledger",
    copy: "Every regular, remembered. Purchase history, preferences and loyalty, kept in one running tally.",
  },
];

const GALLERY = [
  { name: "The Till", desc: "Point-of-sale screen", bars: [70, 40, 85, 55] },
  { name: "The Stockroom", desc: "Inventory board", bars: [60, 90, 45, 65] },
  { name: "The Ledger", desc: "Sales & reports", bars: [50, 75, 60, 80] },
  { name: "The Floor", desc: "Multi-store overview", bars: [80, 55, 70, 40] },
];

const BARCODE_WIDTHS = [3, 1, 2, 1, 4, 1, 1, 3, 2, 1, 4, 2, 1, 1, 3, 2, 4, 1, 2, 1, 3, 1, 2, 4, 1, 1, 2, 3];

function Barcode({ className = "" }: { className?: string }) {
  return (
    <div className={`barcode ${className}`} aria-hidden="true">
      {BARCODE_WIDTHS.map((w, i) => (
        <span key={i} style={{ width: `${w * 2}px` }} />
      ))}
    </div>
  );
}

export default function LandingPage() {
  const [theme, setTheme] = useState<Theme>("light");
  const [navOpen, setNavOpen] = useState(false);
  const [mapVisible, setMapVisible] = useState(false);
  const [tagTransform, setTagTransform] = useState("rotate(-3deg)");

  const contactRef = useRef<HTMLElement | null>(null);
  const galleryRef = useRef<HTMLElement | null>(null);
  const aboutRef = useRef<HTMLElement | null>(null);
  const servicesRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const saved = window.localStorage.getItem("tally-theme") as Theme | null;
    if (saved === "light" || saved === "dark") setTheme(saved);
  }, []);

  useEffect(() => {
    window.localStorage.setItem("tally-theme", theme);
  }, [theme]);

  function handleHeroMove(e: React.MouseEvent<HTMLDivElement>) {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    setTagTransform(`rotate(${-3 + x * 4}deg) translate(${x * 6}px, ${y * 6}px)`);
  }

  function scrollTo(ref: React.RefObject<HTMLElement | null>) {
    ref.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    setNavOpen(false);
  }

  function openContactWithMap() {
    contactRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    setMapVisible(true);
    setNavOpen(false);
  }

  function handleContactSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    // TODO: wire to FastAPI endpoint, e.g. POST /api/contact
    alert("Thanks — your message has been tallied. We'll get back to you shortly.");
    e.currentTarget.reset();
  }

  return (
    <div
      data-theme={theme}
      className={`tally-root ${display.variable} ${body.variable} ${mono.variable}`}
    >
      {/* ---------- NAV ---------- */}
      <header className="tally-nav">
        <div className="tally-nav-inner">
          <button className="tally-logo" onClick={() => scrollTo({ current: document.body })}>
            <span className="tally-logo-mark">T</span>
            <span>TALLY</span>
          </button>

          <nav className={`tally-links ${navOpen ? "is-open" : ""}`}>
            <button onClick={() => scrollTo(aboutRef)}>About</button>
            <button onClick={() => scrollTo(servicesRef)}>Services</button>
            <button onClick={() => scrollTo(galleryRef)}>Gallery</button>
            <button onClick={openContactWithMap}>Contact</button>
          </nav>

          <div className="tally-nav-actions">
            <button
              className="theme-toggle"
              role="switch"
              aria-checked={theme === "dark"}
              aria-label="Toggle dark mode"
              onClick={() => setTheme(theme === "light" ? "dark" : "light")}
            >
              <span className="theme-toggle-track">
                <span className="theme-toggle-label open">OPEN</span>
                <span className="theme-toggle-label closed">CLOSED</span>
                <span className="theme-toggle-knob" />
              </span>
            </button>

            <Link href="/auth/login" className="btn btn-ghost">
              Log in
            </Link>
            <Link href="/auth/register" className="btn btn-primary">
              Get started
            </Link>

            <button
              className="tally-burger"
              aria-label="Toggle menu"
              aria-expanded={navOpen}
              onClick={() => setNavOpen(!navOpen)}
            >
              <span />
              <span />
              <span />
            </button>
          </div>
        </div>
      </header>

      {/* ---------- HERO ---------- */}
      <section className="tally-hero" onMouseMove={handleHeroMove}>
        <div className="tally-hero-inner">
          <div className="price-tag" style={{ transform: tagTransform }}>
            <span className="price-tag-hole" aria-hidden="true" />
            <p className="price-tag-eyebrow">RETAIL OPERATIONS, TALLIED</p>
            <h1 className="price-tag-headline">
              EVERY SALE,
              <br />
              COUNTED.
            </h1>
            <p className="price-tag-sub">
              Tally is the multi-store platform for retailers who&apos;d rather sell than
              reconcile — inventory, point of sale, staff and sales, tallied in real time.
            </p>
            <div className="price-tag-actions">
              <Link href="/auth/register" className="btn btn-primary btn-lg">
                Start free trial
              </Link>
              <button className="btn btn-outline btn-lg" onClick={() => scrollTo(galleryRef)}>
                Watch it ring up
              </button>
            </div>
            <Barcode className="price-tag-barcode" />
          </div>
        </div>
      </section>

      {/* ---------- ABOUT ---------- */}
      <section className="tally-about" ref={aboutRef} id="about">
        <div className="section-inner about-grid">
          <div className="about-copy">
            <p className="eyebrow">About Tally</p>
            <h2>Built on the shop floor, not in a boardroom.</h2>
            <p>
              We spent years behind the counter — closing tills, chasing stock counts, and
              reconciling spreadsheets that never quite matched the drawer. Tally is the
              system we wished we had: one ledger for every storefront, updated the moment
              a sale happens, readable by anyone who has ever run a shop.
            </p>
            <p>
              Today, retailers use Tally to run single boutiques and sprawling multi-store
              chains alike, from the same dashboard, in the same currency of trust: an
              honest, running tally of everything that moved.
            </p>
          </div>
          <dl className="about-stats">
            <div>
              <dt>Storefronts tallied</dt>
              <dd>1,200+</dd>
            </div>
            <div>
              <dt>Countries</dt>
              <dd>38</dd>
            </div>
            <div>
              <dt>Uptime</dt>
              <dd>99.98%</dd>
            </div>
            <div>
              <dt>Receipts / month</dt>
              <dd>4.2M</dd>
            </div>
          </dl>
        </div>
      </section>

      {/* ---------- SERVICES ---------- */}
      <section className="tally-services" ref={servicesRef} id="services">
        <div className="section-inner">
          <p className="eyebrow">What Tally does</p>
          <h2>Everything the shop needs, one running total.</h2>
          <div className="services-grid">
            {SERVICES.map((s) => (
              <article className="service-card" key={s.tag}>
                <span className="service-tag">{s.tag}</span>
                <span className="service-punch" aria-hidden="true" />
                <h3>{s.title}</h3>
                <p>{s.copy}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* ---------- GALLERY ---------- */}
      <section className="tally-gallery" ref={galleryRef} id="gallery">
        <div className="section-inner">
          <p className="eyebrow">Inside Tally</p>
          <h2>A look at the counter.</h2>
          <div className="gallery-grid">
            {GALLERY.map((g) => (
              <figure className="gallery-card" key={g.name}>
                <div className="gallery-mock">
                  <div className="gallery-mock-bar" />
                  {g.bars.map((b, i) => (
                    <span key={i} style={{ height: `${b}%` }} />
                  ))}
                </div>
                <figcaption>
                  <strong>{g.name}</strong>
                  <span>{g.desc}</span>
                </figcaption>
              </figure>
            ))}
          </div>
        </div>
      </section>

      {/* ---------- CONTACT ---------- */}
      <section className="tally-contact" ref={contactRef} id="contact">
        <div className="section-inner contact-grid">
          <div className="contact-form-wrap">
            <p className="eyebrow">Get in touch</p>
            <h2>Talk to the counter.</h2>
            <p className="contact-intro">
              Questions about pricing, migrating an existing store, or rolling Tally out
              across multiple branches — send word and we&apos;ll tally a reply within one
              business day.
            </p>
            <form className="contact-form" onSubmit={handleContactSubmit}>
              <label>
                Name
                <input type="text" name="name" required placeholder="Your name" />
              </label>
              <label>
                Email
                <input type="email" name="email" required placeholder="you@yourstore.com" />
              </label>
              <label>
                Message
                <textarea name="message" required rows={4} placeholder="Tell us about your store" />
              </label>
              <button type="submit" className="btn btn-primary btn-lg">
                Send message
              </button>
            </form>
          </div>

          <aside className={`contact-side ${mapVisible ? "is-visible" : ""}`}>
            <div className="contact-info">
              <h3>Visit the HQ</h3>
              <p>148 Market Street, Suite 4<br />Springfield, USA</p>
              <p>
                <a href="tel:+15550123456">+1 (555) 012-3456</a>
                <br />
                <a href="mailto:hello@tally.app">hello@tally.app</a>
              </p>
              <button className="btn btn-outline" onClick={() => setMapVisible((v) => !v)}>
                {mapVisible ? "Hide map" : "Locate our HQ"}
              </button>
            </div>

            <div className="contact-map" aria-hidden={!mapVisible}>
              {mapVisible && (
                <iframe
                  title="Tally HQ location"
                  src="https://www.google.com/maps?q=Springfield+Market+Street&output=embed"
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                />
              )}
            </div>
          </aside>
        </div>
      </section>

      {/* ---------- FOOTER ---------- */}
      <footer className="tally-footer">
        <div className="section-inner footer-grid">
          <div className="footer-brand">
            <span className="tally-logo-mark">T</span>
            <p>
              Tally — the multi-store retail operations platform for people who&apos;d
              rather run the shop than the spreadsheet.
            </p>
          </div>

          <div className="footer-col">
            <h4>Product</h4>
            <button onClick={() => scrollTo(servicesRef)}>Features</button>
            <Link href="/auth/register">Pricing</Link>
            <button onClick={() => scrollTo(galleryRef)}>Gallery</button>
          </div>

          <div className="footer-col">
            <h4>Company</h4>
            <button onClick={() => scrollTo(aboutRef)}>About</button>
            <button onClick={openContactWithMap}>Contact</button>
            <Link href="/auth/login">Log in</Link>
          </div>

          <div className="footer-col">
            <h4>Resources</h4>
            <a href="#">Documentation</a>
            <a href="#">Support</a>
            <a href="#">System status</a>
          </div>
        </div>
        <div className="footer-bottom">
          <span>&copy; {new Date().getFullYear()} Tally. All sales counted.</span>
          <Barcode />
        </div>
      </footer>
    </div>
  );
}