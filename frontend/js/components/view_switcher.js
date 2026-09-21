export function switchView(viewName) {
  document.querySelectorAll('.view-pane').forEach(el => el.classList.remove('active'));
  const target = document.getElementById(viewName);
  if (target) target.classList.add('active');
}
