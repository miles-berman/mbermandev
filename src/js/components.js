// components.js

// ---- Header ----
const headerTpl = document.createElement('template');
headerTpl.innerHTML = `
  <header>
    <a href="/"><img src="/assets/logo.png" alt="Miles Berman Logo" style="height: 40px;"/></a>
    <nav>
      <a href="/work.html">Work</a>
      <a href="/about.html">About</a>
      <a href="/contact.html" class="cta">Contact</a>
    </nav>
  </header>
`;

class SiteHeader extends HTMLElement {
  connectedCallback() {
    this.appendChild(headerTpl.content.cloneNode(true));
    this.highlightActiveLink("nav a");
  }

  highlightActiveLink(selector) {
    const path = window.location.pathname.replace(/\/+$/, ""); // normalize
    this.querySelectorAll(selector).forEach(a => {
      const href = a.getAttribute("href").replace(/\/+$/, "");
      if (href === path) {
        a.classList.add("active");
      }
    });
  }
}
customElements.define('site-header', SiteHeader);

// ---- Footer ----
const footerTpl = document.createElement('template');
footerTpl.innerHTML = `
  <footer>
    © <span id="year"></span> Miles Berman. All rights reserved.
    <ul>
        <li><a href="/">Home</a></li>
      <li><a href="/work.html">Work</a></li>
      <li><a href="/about.html">About</a></li>
      <li><a href="/contact.html" class="cta">Contact</a></li>
      <li><a href="/privacy.html">Privacy</a></li>
    </ul>
  </footer>
`;

class SiteFooter extends HTMLElement {
  connectedCallback() {
    this.appendChild(footerTpl.content.cloneNode(true));
    this.querySelector('#year').textContent = new Date().getFullYear();
    this.highlightActiveLink("ul a");
  }

  highlightActiveLink(selector) {
    const path = window.location.pathname.replace(/\/+$/, ""); // normalize
    this.querySelectorAll(selector).forEach(a => {
      const href = a.getAttribute("href").replace(/\/+$/, "");
      if (href === path) {
        a.classList.add("active");
      }
    });
  }
}
customElements.define('site-footer', SiteFooter);
