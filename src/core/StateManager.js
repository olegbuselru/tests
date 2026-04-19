export class StateManager {
  constructor() {
    this.state = {
      screen: 'title',
      chapter: 0,
      flags: {},
      relationships: {},
      player: null,
      quests: {},
      inventory: [],
      dialoguesSeen: {}
    };
  }
  set(path, value) { this.state[path] = value; }
  get(path) { return this.state[path]; }
}
