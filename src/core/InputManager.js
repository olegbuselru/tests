export class InputManager {
  constructor() { this.keys = new Set(); }
  init() {
    window.addEventListener('keydown', (e) => this.keys.add(e.key.toLowerCase()));
    window.addEventListener('keyup', (e) => this.keys.delete(e.key.toLowerCase()));
  }
  down(key) { return this.keys.has(key.toLowerCase()); }
}
