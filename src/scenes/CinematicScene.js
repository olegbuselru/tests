export function createCinematicScene({ lines, onComplete, game }) {
  let idx = 0;
  let timer = 0;
  const duration = 4.2;
  return {
    enter() { game.ui.show('hud', false); game.ui.setContext(''); },
    update(dt) {
      timer += dt;
      if (timer >= duration) { timer = 0; idx += 1; if (idx >= lines.length) onComplete(); }
      if (game.input.down(' ')) { idx += 1; timer = 0; if (idx >= lines.length) onComplete(); }
    },
    render(ctx) {
      ctx.fillStyle = '#03050d'; ctx.fillRect(0, 0, 1280, 720);
      ctx.fillStyle = '#dbe9ff'; ctx.font = '31px Segoe UI'; ctx.textAlign = 'center';
      ctx.fillText(lines[Math.min(idx, lines.length - 1)] || '', 640, 360);
      ctx.font = '18px Segoe UI'; ctx.fillStyle = '#8ea7d8';
      ctx.fillText('Space — далее', 640, 670);
    }
  };
}
