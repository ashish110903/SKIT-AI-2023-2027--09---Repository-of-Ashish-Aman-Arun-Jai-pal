export const $ = (sel) => document.querySelector(sel);
export const $$ = (sel) => document.querySelectorAll(sel);
export const setText = (sel, txt) => { const el = $(sel); if (el) el.textContent = txt; };
