// 飞栗系列全案模板 —— 框架常量(与 rhythm.md 时间码一致)
export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;

// 起承转合四段(90s = 2700 帧)
export const SCENES = [
  {name: 'hook',    label: '起 · 钩子(0-8s)',    from: 0,    duration: 240},
  {name: 'context', label: '承 · 场景(8-30s)',   from: 240,  duration: 660},
  {name: 'howto',   label: '转 · 手把手(30-70s)', from: 900,  duration: 1200},
  {name: 'closing', label: '合 · 收尾(70-90s)',  from: 2100, duration: 600},
] as const;
