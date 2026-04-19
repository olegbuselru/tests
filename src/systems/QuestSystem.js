import { QUESTS } from '../content/data.js';

export class QuestSystem {
  start(state, id) { if (!state.quests[id]) state.quests[id] = { ...QUESTS[id], status: 'active', progress: 0 }; }
  complete(state, id) { if (state.quests[id]) state.quests[id].status = 'completed'; }
  list(state) { return Object.values(state.quests); }
}
