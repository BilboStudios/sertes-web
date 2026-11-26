// SERTES — comportamiento común de todas las páginas.

document.querySelectorAll('.year').forEach(el => { el.textContent = new Date().getFullYear(); });

// Menú plegado
const burger = document.querySelector('.burger'), menu = document.getElementById('menu');
if (burger && menu) {
  const setMenu = open => {
    menu.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open);
    burger.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  };
  burger.addEventListener('click', () => setMenu(!menu.classList.contains('open')));
  menu.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('click', e => { if (!e.target.closest('.site')) setMenu(false); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
}

// Selector de equipos (portada)
const tabs = [...document.querySelectorAll('.gear-list button')];
if (tabs.length) {
  const BASE = 'https://sertes.es/wp-content/uploads/2026/11/';
  const frame = document.getElementById('frame'), title = document.getElementById('viewer-title'), list = document.getElementById('viewer-tags');
  const photos = tabs.map(t => {
    const im = new Image();
    im.alt = ''; im.decoding = 'async'; im.src = BASE + t.dataset.img;
    frame.appendChild(im);
    return im;
  });
  const pick = i => {
    tabs.forEach((t, k) => {
      t.setAttribute('aria-selected', k === i);
      t.tabIndex = k === i ? 0 : -1;
      photos[k].classList.toggle('on', k === i);
    });
    title.textContent = tabs[i].firstChild.textContent.trim();
    list.replaceChildren(...tabs[i].dataset.l.split('|').map(x => Object.assign(document.createElement('li'), { textContent: x })));
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => pick(i));
    t.addEventListener('mouseenter', () => { if (matchMedia('(hover:hover) and (min-width:761px)').matches) pick(i); });
    t.addEventListener('keydown', e => {
      const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
      if (!d) return;
      e.preventDefault();
      const k = (i + d + tabs.length) % tabs.length;
      pick(k); tabs[k].focus();
    });
  });
  pick(0);
}

// Formulario. Versión estática: abre el programa de correo con la solicitud redactada.
// Al integrarlo en WordPress, sustituir por el envío del formulario del sitio.
const form = document.getElementById('form');
if (form) {
  const asunto = new URLSearchParams(location.search).get('asunto');
  if (asunto) form.asunto.value = asunto;
  form.addEventListener('submit', e => {
    e.preventDefault();
    const d = new FormData(form);
    const body = ['Nombre: ' + d.get('nombre'), 'Correo: ' + d.get('email'), 'Teléfono: ' + (d.get('telefono') || '-'), 'Empresa: ' + (d.get('empresa') || '-'), '', d.get('mensaje')].join('\n');
    location.href = 'mailto:sertes@sertes.es?subject=' + encodeURIComponent(d.get('asunto') || 'Solicitud de asistencia desde la web') + '&body=' + encodeURIComponent(body);
  });
}
