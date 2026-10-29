export function triggerCsvDownload(csvString, filename='telemetry.csv') {
  const blob = new Blob([csvString], { type: 'text/csv' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = filename; a.click();
}
