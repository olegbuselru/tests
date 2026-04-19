export class SceneManager {
  constructor() { this.registry = new Map(); this.current = null; }
  register(id, sceneFactory) { this.registry.set(id, sceneFactory); }
  change(id, context) {
    if (this.current?.exit) this.current.exit();
    this.current = this.registry.get(id)(context);
    if (this.current.enter) this.current.enter();
  }
  update(dt) { this.current?.update?.(dt); }
  render(ctx) { this.current?.render?.(ctx); }
}
