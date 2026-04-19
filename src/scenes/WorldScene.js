import { ENEMIES, NPCS, ITEMS, QUESTS } from '../content/data.js';

const d = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);

export function createWorldScene(ctxx) {
  const { game, chapter } = ctxx;
  const player = game.state.state.player;
  const npcs = chapter === 1
    ? [{ id: 'nera', x: 430, y: 330, color: '#dfc0ff' }, { id: 'altar', x: 930, y: 250, color: '#ffe7a3' }]
    : [{ id: 'elder', x: 260, y: 210, color: '#ffe09b' }, { id: 'mila', x: 370, y: 500, color: '#9dffcf' }, { id: 'tower', x: 1060, y: 220, color: '#b8b8ff' }];

  const enemies = [];
  const spawn = (type, x, y) => enemies.push({ ...ENEMIES[type], pos: { x, y }, maxHp: ENEMIES[type].hp, state: 'idle', dead: false, atkCooldown: 0, hitFlash: 0 });
  if (chapter === 1) { spawn('mossling', 650, 260); spawn('mossling', 740, 390); }
  if (chapter === 2) { spawn('hollowScout', 780, 420); spawn('ruinWarden', 1040, 300); }

  let kills = 0;
  let herbsCollected = 0;

  const onInteract = (id) => {
    if (id === 'nera') game.dialogue.start('neraFirst', () => game.ui.setContext('Нера кивает в сторону тропы.'));
    if (id === 'altar' && !game.state.state.flags.altarDone) {
      game.dialogue.start('altarChoice', () => {
        game.state.state.flags.altarDone = true;
        game.quest.complete(game.state.state, 'q1_main');
        game.progressChapter();
      });
    }
    if (id === 'elder') {
      const mercy = game.state.state.flags.altarMercy;
      game.ui.setContext(mercy ? 'Староста мягче с тобой: “Ты не как наемники.”' : 'Староста хмурится: “Сила — не оправдание.”');
      game.quest.start(game.state.state, 'q2_main');
      game.quest.start(game.state.state, 'q2_side_herbs');
      game.quest.start(game.state.state, 'q2_side_scout');
    }
    if (id === 'mila') {
      herbsCollected = Math.min(3, herbsCollected + 1);
      game.inventory.add(game.state.state, 'herb');
      game.ui.setContext(`Мила: “Спасибо... Уже ${herbsCollected}/3 трав.”`);
      if (herbsCollected === 3) game.quest.complete(game.state.state, 'q2_side_herbs');
    }
    if (id === 'tower') game.ui.setContext('Башня гудит. Страж уже чувствует тебя.');
  };

  return {
    enter() {
      game.ui.show('hud', true);
      game.ui.setQuestText(chapter === 1 ? QUESTS.q1_main.title : QUESTS.q2_main.title);
      if (chapter === 1) game.quest.start(game.state.state, 'q1_main');
    },
    update(dt) {
      if (game.paused || game.dialogue.current) return;
      const i = game.input;
      const mv = { x: 0, y: 0 };
      if (i.down('w') || i.down('arrowup')) mv.y -= 1;
      if (i.down('s') || i.down('arrowdown')) mv.y += 1;
      if (i.down('a') || i.down('arrowleft')) mv.x -= 1;
      if (i.down('d') || i.down('arrowright')) mv.x += 1;
      const len = Math.hypot(mv.x, mv.y) || 1;
      player.pos.x = Math.max(30, Math.min(1250, player.pos.x + (mv.x / len) * player.speed * dt));
      player.pos.y = Math.max(30, Math.min(690, player.pos.y + (mv.y / len) * player.speed * dt));

      game.combat.tickCooldowns(player, dt);
      player.mana = Math.min(player.maxMana, player.mana + 6 * dt);

      enemies.forEach((e) => {
        if (e.dead) return;
        const dist = d(player.pos, e.pos);
        e.hitFlash = Math.max(0, e.hitFlash - dt);
        if (dist < 260) e.state = 'aggro';
        if (e.state === 'aggro') {
          const nx = (player.pos.x - e.pos.x) / (dist || 1); const ny = (player.pos.y - e.pos.y) / (dist || 1);
          if (dist > 40) { e.pos.x += nx * e.speed * dt; e.pos.y += ny * e.speed * dt; }
          e.atkCooldown -= dt;
          if (dist < 42 && e.atkCooldown <= 0) {
            e.atkCooldown = 1.3;
            player.hp -= e.atk;
            game.audio.beep(160, 90);
          }
        }
      });

      if (player.hp <= 0) game.onDeath();

      if (i.down('j')) game.combat.basicAttack(player, enemies);
      if (i.down('k')) game.combat.useAbility(player, enemies);
      if (i.down('e')) {
        const near = npcs.find((n) => d(player.pos, n) < 60);
        if (near) onInteract(near.id);
      }

      enemies.forEach((e) => {
        if (e.dead && !e.rewarded) {
          e.rewarded = true;
          game.stats.grantXp(player, e.xp);
          kills += 1;
          if (chapter === 1 && kills >= 2) game.ui.setContext('Путь к алтарю открыт. Решение ждет тебя.');
          if (chapter === 2 && e.id === 'ruinWarden') {
            game.inventory.add(game.state.state, 'coreShard');
            game.quest.complete(game.state.state, 'q2_main');
            game.progressChapter();
          }
          if (chapter === 2 && e.id === 'hollowScout') game.quest.complete(game.state.state, 'q2_side_scout');
        }
      });

      if (chapter === 1 && kills < 2) game.ui.setQuestText(`Победи мшистых клыков: ${kills}/2`);
      if (chapter === 2) game.ui.setQuestText('Доберись до башни и добудь осколок');

      const nearNpc = npcs.find((n) => d(player.pos, n) < 70);
      game.ui.setContext(nearNpc ? `E: взаимодействовать (${NPCS[nearNpc.id]?.name || nearNpc.id})` : 'WASD: движение, J: атака, K: способность');
      game.ui.updateHud();
    },
    render(ctx) {
      ctx.clearRect(0, 0, 1280, 720);
      const g = ctx.createLinearGradient(0, 0, 0, 720);
      g.addColorStop(0, chapter === 1 ? '#1b2d45' : '#2d243f'); g.addColorStop(1, '#0a1222');
      ctx.fillStyle = g; ctx.fillRect(0, 0, 1280, 720);
      for (let i = 0; i < 60; i += 1) {
        ctx.fillStyle = `rgba(140,180,255,${0.03 + (i % 7) * 0.01})`;
        ctx.fillRect((i * 143 + performance.now() * 0.01) % 1280, (i * 97) % 720, 2, 2);
      }
      npcs.forEach((n) => { ctx.fillStyle = n.color; ctx.beginPath(); ctx.arc(n.x, n.y, 18, 0, Math.PI * 2); ctx.fill(); });
      enemies.forEach((e) => {
        if (e.dead) return;
        ctx.fillStyle = e.hitFlash > 0 ? '#fff' : (e.boss ? '#ff8cae' : '#89ff9d');
        ctx.beginPath(); ctx.arc(e.pos.x, e.pos.y, e.boss ? 28 : 16, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#0008'; ctx.fillRect(e.pos.x - 22, e.pos.y - 28, 44, 6);
        ctx.fillStyle = '#ff5f7d'; ctx.fillRect(e.pos.x - 22, e.pos.y - 28, 44 * (e.hp / e.maxHp), 6);
      });
      ctx.fillStyle = '#78d8ff'; ctx.beginPath(); ctx.arc(player.pos.x, player.pos.y, 17, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = '#d6f3ff'; ctx.stroke();
    }
  };
}
