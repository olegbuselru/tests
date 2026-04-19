export class DialogueSystem {
  constructor(data, state, ui, bus, audio) {
    this.data = data; this.state = state; this.ui = ui; this.bus = bus; this.audio = audio;
    this.current = null; this.nodeKey = null; this.typingTimer = null;
  }
  start(id, onEnd) { this.current = this.data[id]; this.nodeKey = 'start'; this.onEnd = onEnd; this.ui.openDialogue(); this.renderNode(); }
  applyEffects(node) {
    if (node.effect?.rel) {
      const [npc, delta] = node.effect.rel;
      this.state.relationships[npc] = (this.state.relationships[npc] || 0) + delta;
    }
    if (node.setFlag) this.state.flags[node.setFlag[0]] = node.setFlag[1];
  }
  renderNode() {
    const node = this.current[this.nodeKey];
    this.ui.setDialogue(node.speaker, '', []);
    let i = 0;
    clearInterval(this.typingTimer);
    this.typingTimer = setInterval(() => {
      i += 1;
      this.ui.setDialogue(node.speaker, node.text.slice(0, i), []);
      this.audio.beep(900, 15, 0.15);
      if (i >= node.text.length) {
        clearInterval(this.typingTimer);
        this.ui.setDialogue(node.speaker, node.text, (node.choices || []).map((c) => ({
          label: c.text,
          onClick: () => {
            this.applyEffects(c);
            if (c.next) { this.nodeKey = c.next; this.renderNode(); }
            else this.end();
          }
        })));
        if (!node.choices && node.next) { this.nodeKey = node.next; setTimeout(() => this.renderNode(), 600); }
        if (!node.choices && !node.next) this.end();
      }
    }, 18);
  }
  skipTyping() {
    if (!this.current) return;
    clearInterval(this.typingTimer);
    const node = this.current[this.nodeKey];
    this.ui.setDialogue(node.speaker, node.text, (node.choices || []).map((c) => ({ label: c.text, onClick: () => {
      this.applyEffects(c);
      if (c.next) { this.nodeKey = c.next; this.renderNode(); } else this.end();
    }})));
  }
  end() { this.ui.closeDialogue(); const cb = this.onEnd; this.current = null; if (cb) cb(); this.bus.emit('dialogue:end'); }
}
