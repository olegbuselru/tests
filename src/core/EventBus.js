export class EventBus {
  constructor() { this.listeners = new Map(); }
  on(event, handler) { if (!this.listeners.has(event)) this.listeners.set(event, []); this.listeners.get(event).push(handler); }
  emit(event, payload) { (this.listeners.get(event) || []).forEach((h) => h(payload)); }
}
