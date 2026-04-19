import { ITEMS } from '../content/data.js';

export class InventorySystem {
  add(state, itemId) { state.inventory.push(itemId); }
  use(state, player, itemId) {
    const idx = state.inventory.indexOf(itemId);
    if (idx < 0) return false;
    const item = ITEMS[itemId];
    if (item.type === 'consumable' && item.hp) player.hp = Math.min(player.maxHp, player.hp + item.hp);
    state.inventory.splice(idx, 1);
    return true;
  }
}
