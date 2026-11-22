export function showToast(msg, type='info') {
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.innerText = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 4000);
}
