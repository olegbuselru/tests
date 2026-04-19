import { ABILITIES, CLASSES } from '../content/data.js';

const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);

export class CombatSystem {
  constructor(audio) { this.audio = audio; }
  basicAttack(player, enemies) {
    const target = enemies.find((e) => !e.dead && dist(player.pos, e.pos) < 75);
    if (!target) return false;
    target.hp -= player.atk;
    target.hitFlash = 0.2;
    this.audio.beep(250, 80);
    if (target.hp <= 0) { target.dead = true; target.state = 'death'; }
    return true;
  }
  useAbility(player, enemies) {
    const cls = CLASSES[player.classId]; const ability = ABILITIES[cls.skill];
    const cd = player.cooldowns[ability.name] || 0;
    if (cd > 0 || player.mana < ability.mana) return false;
    const target = enemies.find((e) => !e.dead && dist(player.pos, e.pos) < 180);
    if (!target) return false;
    player.mana -= ability.mana;
    player.cooldowns[ability.name] = ability.cooldown;
    target.hp -= ability.dmg; target.hitFlash = 0.35;
    this.audio.beep(560, 120);
    if (target.hp <= 0) { target.dead = true; target.state = 'death'; }
    return true;
  }
  tickCooldowns(player, dt) {
    Object.keys(player.cooldowns).forEach((k) => player.cooldowns[k] = Math.max(0, player.cooldowns[k] - dt));
  }
}
