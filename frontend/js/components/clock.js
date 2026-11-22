export function startClock(el) {
  setInterval(() => { el.innerText = new Date().toLocaleTimeString(); }, 1000);
}
