/* Fill the printable document from the link that opened it, then let the browser save it as PDF. */
(function () {
  const P = new URLSearchParams(location.search), $ = (s, c = document) => c.querySelector(s);
  const type = P.get('type') || 'receipt';
  const KIND = { ticket: 'Entry ticket', receipt: 'Payment receipt', invoice: 'Tax invoice' };
  const set = (k, v) => { if (v) document.querySelectorAll(`[data-f="${k}"]`).forEach(e => e.textContent = v); };
  set('kind', KIND[type] || KIND.receipt);
  ['id', 'to', 'org', 'item', 'sub', 'date', 'line', 'base', 'fee', 'total', 'method'].forEach(k => set(k, P.get(k)));
  document.querySelectorAll('[data-show]').forEach(e => e.hidden = e.dataset.show !== type);
  document.querySelectorAll('[data-hide]').forEach(e => e.hidden = e.dataset.hide === type);
  document.title = `${KIND[type] || 'Document'} ${P.get('id') || ''} | FestHey`;
  const back = $('[data-back]');
  if (document.referrer && new URL(document.referrer).origin === location.origin) back.addEventListener('click', ev => { ev.preventDefault(); history.back(); });
  $('[data-print]').addEventListener('click', () => window.print());
  if (P.get('print') === '1') setTimeout(() => window.print(), 600);
})();
