export class UIManager {
  constructor(state) { this.state = state; }
  q(id) { return document.getElementById(id); }
  show(id, on = true) { this.q(id).classList.toggle('hidden', !on); }
  screen(id) {
    document.querySelectorAll('.screen').forEach((e) => e.classList.add('hidden'));
    this.show(id, true);
  }
  openDialogue() { this.show('dialogue-panel', true); }
  closeDialogue() { this.show('dialogue-panel', false); }
  setDialogue(speaker, text, choices) {
    this.q('dialogue-speaker').textContent = speaker;
    this.q('dialogue-text').textContent = text;
    const box = this.q('dialogue-choices'); box.innerHTML = '';
    choices.forEach((c) => { const b = document.createElement('button'); b.textContent = c.label; b.onclick = c.onClick; box.appendChild(b); });
  }
  updateHud() {
    const p = this.state.player; if (!p) return;
    this.q('hp-value').textContent = `${Math.ceil(p.hp)}/${p.maxHp}`;
    this.q('mana-value').textContent = `${Math.ceil(p.mana)}/${p.maxMana}`;
    this.q('lv-value').textContent = p.level;
    this.q('xp-value').textContent = `${p.xp}/${p.xpToNext}`;
    this.q('hp-bar').style.width = `${(p.hp / p.maxHp) * 100}%`;
    this.q('mana-bar').style.width = `${(p.mana / p.maxMana) * 100}%`;
  }
  setQuestText(text) { this.q('active-quest').textContent = text; }
  setContext(text) { this.q('context-hint').textContent = text || ''; }
  populateInventory(items, itemDict) {
    const list = this.q('inventory-list'); list.innerHTML = '';
    items.forEach((i) => { const li = document.createElement('li'); li.textContent = `${itemDict[i].name}: ${itemDict[i].desc}`; list.appendChild(li); });
  }
  populateJournal(quests) {
    const list = this.q('journal-list'); list.innerHTML = '';
    quests.forEach((q) => { const li = document.createElement('li'); li.textContent = `[${q.status}] ${q.title} — ${q.description}`; list.appendChild(li); });
  }
}
