import { CLASSES } from '../content/data.js';

export class StatsSystem {
  createPlayer(classId) {
    const c = CLASSES[classId];
    return {
      classId,
      level: 1,
      xp: 0,
      xpToNext: 100,
      maxHp: c.hp,
      hp: c.hp,
      maxMana: c.mana,
      mana: c.mana,
      atk: 12,
      pos: { x: 120, y: 360 },
      cooldowns: {},
      speed: 180
    };
  }
  grantXp(player, amount) {
    player.xp += amount;
    while (player.xp >= player.xpToNext) {
      player.xp -= player.xpToNext;
      player.level += 1;
      player.xpToNext = Math.floor(player.xpToNext * 1.35);
      player.maxHp += 18; player.maxMana += 10; player.atk += 3;
      player.hp = player.maxHp; player.mana = player.maxMana;
    }
  }
}
