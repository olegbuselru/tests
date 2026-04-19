export class AudioManager {
  constructor() { this.musicVolume = 0.5; this.sfxVolume = 0.7; this.ctx = null; }
  init() { this.ctx = new (window.AudioContext || window.webkitAudioContext)(); }
  beep(freq = 440, ms = 120, gain = this.sfxVolume) {
    if (!this.ctx) return;
    const o = this.ctx.createOscillator(); const g = this.ctx.createGain();
    o.frequency.value = freq; g.gain.value = gain * 0.12; o.connect(g).connect(this.ctx.destination);
    o.start(); o.stop(this.ctx.currentTime + ms / 1000);
  }
  setMusicVolume(v) { this.musicVolume = v; }
  setSfxVolume(v) { this.sfxVolume = v; }
}
