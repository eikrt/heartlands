import { writable, derived } from 'svelte/store';

export const apiData = writable([]);

export const tiles = derived(apiData, ($apiData) => {
  if ($apiData) {
    return Object.values($apiData).map(v => {return v.props})
  }
  return [];
});
