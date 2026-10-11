/* DatatalkwithAnkit — site script */
(function () {
  'use strict';
  var EMAIL = 'dongare.ankit29@gmail.com';

  /* Contact form backend. Paste a Formspree endpoint here
     (https://formspree.io/f/xxxxxxx) to send messages directly.
     Left empty, the form opens the visitor's mail app instead. */
  var FORM_ENDPOINT = '';

  /* ---------- theme ---------- */
  var root = document.documentElement;
  function setTheme(t) {
    if (t === 'light') root.setAttribute('data-theme', 'light');
    else root.removeAttribute('data-theme');
    try { localStorage.setItem('theme', t); } catch (e) {}
  }
  var btn = document.querySelector('.theme');
  if (btn) {
    btn.addEventListener('click', function () {
      setTheme(root.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
    });
  }

  /* ---------- will-it-fit calculator ---------- */
  var fit = document.getElementById('fit');
  if (fit) {
    var GPUS = [
      { key: 'h200', name: 'NVIDIA H200', mem: 141, rate: 2.60 },
      { key: 'mi',   name: 'AMD MI300X',  mem: 192, rate: 1.71 }
    ];
    var BYTES = { fp16: 2, fp8: 1, int4: 0.5 };
    var LABEL = { fp16: 'FP16', fp8: 'FP8', int4: 'INT4' };
    var state = { size: 70, prec: 'fp16' };
    var MAX_BLOCKS = 8;

    function money(n) { return '$' + n.toFixed(2); }

    function render() {
      var need = state.size * BYTES[state.prec] * 1.2;
      document.getElementById('fit-need').innerHTML =
        'A ' + state.size + 'B model at ' + LABEL[state.prec] + ' needs about ' + Math.round(need) + ' GB' +
        '<span>Weights, plus 20% headroom for the KV cache.</span>';

      var best = null;
      GPUS.forEach(function (g) {
        var n = Math.max(1, Math.ceil(need / g.mem));
        var perGpu = Math.min(100, (need / n) / g.mem * 100);
        var cost = n * g.rate;
        if (!best || cost < best.cost) best = { name: g.name, cost: cost, n: n };

        var row = document.getElementById('fit-' + g.key);
        var blocks = '';
        var shown = Math.min(n, MAX_BLOCKS);
        for (var i = 0; i < shown; i++) {
          blocks += '<span class="gpu" aria-hidden="true"><i style="height:' + perGpu.toFixed(0) + '%"></i></span>';
        }
        if (n > MAX_BLOCKS) blocks += '<span class="fit-more">+' + (n - MAX_BLOCKS) + ' more</span>';
        row.querySelector('.fit-blocks').innerHTML = blocks;
        row.querySelector('.fit-out').innerHTML =
          '<strong>' + n + (n === 1 ? ' GPU' : ' GPUs') + '</strong>' +
          '<span>about ' + money(cost) + ' per hour</span>';
        row.setAttribute('aria-label', g.name + ': ' + n + (n === 1 ? ' GPU' : ' GPUs') + ', about ' + money(cost) + ' per hour');
      });
      document.getElementById('fit-best').textContent =
        'Cheapest here: ' + best.n + ' ' + best.name + (best.n === 1 ? '' : 's') + ' at about ' + money(best.cost) + ' per hour.';
    }

    function wire(groupId, key, parse) {
      var group = document.getElementById(groupId);
      group.addEventListener('click', function (ev) {
        var b = ev.target.closest('button');
        if (!b) return;
        group.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        state[key] = parse(b.dataset.v);
        render();
      });
    }
    wire('fit-size', 'size', function (v) { return parseFloat(v); });
    wire('fit-prec', 'prec', function (v) { return v; });
    render();
  }

  /* ---------- blog filters ---------- */
  var filters = document.getElementById('filters');
  if (filters) {
    var rows = document.querySelectorAll('[data-tags]');
    filters.addEventListener('click', function (ev) {
      var b = ev.target.closest('button');
      if (!b) return;
      filters.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true');
      var tag = b.dataset.tag;
      var shown = 0;
      rows.forEach(function (r) {
        var on = tag === 'all' || r.dataset.tags.split(' ').indexOf(tag) > -1;
        r.hidden = !on;
        if (on) shown++;
      });
      var empty = document.getElementById('empty');
      if (empty) empty.hidden = shown > 0;
    });
  }

  /* ---------- newsletter ---------- */
  var sub = document.getElementById('subscribe');
  if (sub) {
    sub.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var email = sub.querySelector('input[type=email]').value.trim();
      var note = sub.parentNode.querySelector('.note');
      if (!email) { note.textContent = 'Enter your email address to subscribe.'; return; }
      location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Newsletter signup') +
        '&body=' + encodeURIComponent('Please add me to the newsletter: ' + email);
    });
  }

  /* ---------- contact ---------- */
  var contact = document.getElementById('contact-form');
  if (contact) {
    contact.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var name = contact.querySelector('[name=name]').value.trim();
      var email = contact.querySelector('[name=email]').value.trim();
      var msg = contact.querySelector('[name=message]').value.trim();
      var note = contact.querySelector('.note');
      var send = contact.querySelector('button');
      if (!msg) { note.textContent = 'Write a message before sending.'; return; }

      if (!FORM_ENDPOINT) {
        location.href = 'mailto:' + EMAIL + '?subject=' +
          encodeURIComponent('Hello from your website' + (name ? ' (' + name + ')' : '')) +
          '&body=' + encodeURIComponent(msg + '\n\n' + name + (email ? ' <' + email + '>' : ''));
        return;
      }
      send.disabled = true;
      send.textContent = 'Sending';
      fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, email: email, message: msg })
      }).then(function (res) {
        if (!res.ok) throw new Error('send failed');
        contact.reset();
        send.textContent = 'Sent';
        note.textContent = 'Message sent. I usually reply within two days.';
      }).catch(function () {
        send.disabled = false;
        send.textContent = 'Send message';
        note.textContent = 'The message did not send. Email ' + EMAIL + ' directly.';
      });
    });
  }

  /* ---------- copy link ---------- */
  var copy = document.getElementById('copy-link');
  if (copy) {
    copy.addEventListener('click', function () {
      var done = function () { copy.textContent = 'Link copied'; };
      try {
        navigator.clipboard.writeText(location.href).then(done, function () { prompt('Copy this link', location.href); });
      } catch (e) { prompt('Copy this link', location.href); }
    });
  }
})();
