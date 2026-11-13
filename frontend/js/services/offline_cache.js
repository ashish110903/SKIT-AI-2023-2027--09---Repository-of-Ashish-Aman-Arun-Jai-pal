export const OfflineCache = {
  save(key, val) { localStorage.setItem(key, JSON.stringify(val)); },
  load(key) { const v = localStorage.getItem(key); return v ? JSON.parse(v) : null; }
};
