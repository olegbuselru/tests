import { EventBus } from './core/EventBus.js';
import { StateManager } from './core/StateManager.js';
import { InputManager } from './core/InputManager.js';
import { AudioManager } from './core/AudioManager.js';
import { SaveManager } from './core/SaveManager.js';
import { SceneManager } from './core/SceneManager.js';
import { StatsSystem } from './systems/StatsSystem.js';
import { InventorySystem } from './systems/InventorySystem.js';
import { QuestSystem } from './systems/QuestSystem.js';
import { DialogueSystem } from './systems/DialogueSystem.js';
import { CombatSystem } from './systems/CombatSystem.js';
import { UIManager } from './ui/UIManager.js';
import { CLASSES, DIALOGUES, ITEMS, CHAPTERS } from './content/data.js';
import { createWorldScene } from './scenes/WorldScene.js';
import { createCinematicScene } from './scenes/CinematicScene.js';

const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');

class Game {
  constructor() {
    this.bus = new EventBus();
    this.state = new StateManager();
    this.input = new InputManager();
    this.audio = new AudioManager();
    this.save = new SaveManager(this.state);
    this.scene = new SceneManager();
    this.stats = new StatsSystem();
    this.inventory = new InventorySystem();
    this.quest = new QuestSystem();
    this.ui = new UIManager(this.state.state);
    this.combat = new CombatSystem(this.audio);
    this.dialogue = new DialogueSystem(DIALOGUES, this.state.state, this.ui, this.bus, this.audio);
    this.last = performance.now();
    this.paused = false;
  }

  init() {
    this.input.init();
    this.audio.init();
    this.wireUI();
    this.registerScenes();
    requestAnimationFrame(() => this.loop());
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') this.togglePause();
      if (e.key === ' ') this.dialogue.skipTyping();
    });
  }

  wireUI() {
    document.querySelectorAll('button[data-action]').forEach((b) => {
      b.addEventListener('click', () => this.handleAction(b.dataset.action));
    });
    document.getElementById('music-volume').oninput = (e) => this.audio.setMusicVolume(Number(e.target.value));
    document.getElementById('sfx-volume').oninput = (e) => this.audio.setSfxVolume(Number(e.target.value));
    this.populateClassPanel();
  }

  populateClassPanel() {
    const root = document.getElementById('class-options');
    root.innerHTML = '';
    Object.values(CLASSES).forEach((c) => {
      const div = document.createElement('div');
      div.className = 'class-card';
      div.innerHTML = `<h3>${c.name}</h3><p>${c.desc}</p><button>Выбрать</button>`;
      div.querySelector('button').onclick = () => {
        this.state.state.player = this.stats.createPlayer(c.id);
        this.state.state.chapter = 1;
        this.ui.show('class-panel', false);
        this.dialogue.start('introEcho', () => this.startChapter(1));
      };
      root.appendChild(div);
    });
  }

  handleAction(action) {
    this.audio.beep(740, 70);
    if (action === 'new-game') { this.ui.screen('title-screen'); this.ui.show('class-panel', true); }
    if (action === 'continue' && this.save.hasSave()) { this.save.load(); this.startChapter(this.state.state.chapter || 1); }
    if (action === 'settings') this.ui.show('settings-panel', true);
    if (action === 'close-settings') this.ui.show('settings-panel', false);
    if (action === 'resume') this.togglePause(false);
    if (action === 'to-title') location.reload();
    if (action === 'restart') location.reload();
    if (action === 'inventory') { this.ui.show('inventory-panel', true); this.ui.populateInventory(this.state.state.inventory, ITEMS); }
    if (action === 'journal') { this.ui.show('journal-panel', true); this.ui.populateJournal(this.quest.list(this.state.state)); }
    if (action === 'attack') this.combat.basicAttack(this.state.state.player, this.scene.current?.enemies || []);
    if (action === 'ability') this.combat.useAbility(this.state.state.player, this.scene.current?.enemies || []);
    if (action === 'interact') this.input.keys.add('e');
    if (action === 'chapter-continue') this.ui.show('chapter-screen', false);
  }

  registerScenes() {
    this.scene.register('introCinematic', () => createCinematicScene({
      game: this,
      lines: [
        'Дождь. Переход. Скрежет тормозов — и белый шум.',
        'Ты пытался спасти человека на переходе. Успел. А потом — тишина.',
        'Между мирами голос шепчет: “Цена уплачена. История продолжается.”'
      ],
      onComplete: () => this.ui.show('class-panel', true)
    }));
    this.scene.register('chapter1', () => createWorldScene({ game: this, chapter: 1 }));
    this.scene.register('chapter2Transition', () => createCinematicScene({
      game: this,
      lines: ['Ночь сгущается над деревней Крайлист.', 'Нера: “Если ты правда пришел из другого мира... возможно, ты ключ.”'],
      onComplete: () => this.startChapter(2)
    }));
    this.scene.register('chapter2', () => createWorldScene({ game: this, chapter: 2 }));
  }

  startChapter(index) {
    this.state.state.chapter = index;
    this.ui.screen('title-screen');
    this.ui.show('title-screen', false);
    this.ui.show('death-screen', false);
    this.ui.show('chapter-screen', true);
    document.getElementById('chapter-title').textContent = CHAPTERS[index].name;
    document.getElementById('chapter-text').textContent = index === 1
      ? 'Ты просыпаешься у древнего святилища. Эхо мира ведет тебя к первому выбору.'
      : 'Деревня на краю леса ждет твоего решения. Руины не любят живых.';
    setTimeout(() => {
      this.ui.show('chapter-screen', false);
      this.scene.change(index === 1 ? 'chapter1' : 'chapter2');
    }, 1800);
  }

  progressChapter() {
    if (this.state.state.chapter === 1) {
      this.scene.change('chapter2Transition');
      this.state.state.chapter = 2;
      return;
    }
    this.ui.show('chapter-screen', true);
    document.getElementById('chapter-title').textContent = 'ФИНАЛ ВЕРТИКАЛЬНОГО СРЕЗА';
    document.getElementById('chapter-text').textContent = 'Осколок реагирует на твою кровь. В небесах открывается вторая трещина. Продолжение следует...';
    this.save.save();
  }

  onDeath() { this.ui.show('death-screen', true); this.paused = true; }

  togglePause(force) {
    this.paused = typeof force === 'boolean' ? force : !this.paused;
    this.ui.show('pause-panel', this.paused);
  }

  loop() {
    const now = performance.now();
    const dt = Math.min((now - this.last) / 1000, 0.033);
    this.last = now;
    if (!this.paused) this.scene.update(dt);
    this.scene.render(ctx);
    requestAnimationFrame(() => this.loop());
  }
}

const game = new Game();
game.init();
game.scene.change('introCinematic');
