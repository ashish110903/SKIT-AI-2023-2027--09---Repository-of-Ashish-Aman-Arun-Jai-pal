export function filterStations(stations, query) {
  return stations.filter(s => s.name.toLowerCase().includes(query.toLowerCase()));
}
