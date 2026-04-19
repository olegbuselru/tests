export class SaveManager {
  constructor(state) { this.state = state; this.cache = null; }
  save() { this.cache = structuredClone(this.state.state); }
  load() { if (this.cache) this.state.state = structuredClone(this.cache); return this.cache; }
  hasSave() { return !!this.cache; }
}
