import { writable, derived } from 'svelte/store';

export const apiData = writable([]);

export const tiles = derived(apiData, ($apiData) => {
  if ($apiData) {
    console.log(Object.values($apiData).map(v => {return v.props}))
    return Object.values($apiData).map(v => {return v.props})
  }
  return [];
});
