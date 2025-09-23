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

    // highlight current page link
    const path = window.location.pathname.replace(/\/+$/, ""); // normalize
    this.querySelectorAll("nav a").forEach(a => {
      const href = a.getAttribute("href").replace(/\/+$/, "");
      if (href === path) {
        a.style.textDecoration = "underline";
        a.style.textUnderlineOffset = "4px";
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
  </footer>
`;

class SiteFooter extends HTMLElement {
  connectedCallback() {
    this.appendChild(footerTpl.content.cloneNode(true));
    this.querySelector('#year').textContent = new Date().getFullYear();
  }
}
customElements.define('site-footer', SiteFooter);
