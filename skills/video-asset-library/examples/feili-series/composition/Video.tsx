// 飞栗系列全案模板 —— 主 Composition(场景骨架,内容留槽位)
// 配合 rhythm.md 填内容;时长框架见 constants.ts
import React from 'react';
import {Composition, Sequence} from 'remotion';
import {SCENES, FPS, WIDTH, HEIGHT} from './constants';

// ASSET: 各场景组件替换为实际内容组件(从 code-components/ 引用或项目内新建)
const ScenePlaceholder: React.FC<{label: string}> = ({label}) => (
  <div style={{
    width: '100%', height: '100%', background: '#F6F6F1',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontFamily: 'Noto Sans SC', color: '#6B7280', fontSize: 32,
  }}>
    {label}
  </div>
);

export const FeiliSeriesVideo: React.FC = () => (
  <>
    {SCENES.map((s) => (
      <Sequence key={s.name} from={s.from} durationInFrames={s.duration}>
        <ScenePlaceholder label={s.label} />
      </Sequence>
    ))}
  </>
);

export const RemotionRoot: React.FC = () => (
  <Composition
    id="FeiliSeries"
    component={FeiliSeriesVideo}
    durationInFrames={SCENES.reduce((acc, s) => acc + s.duration, 0)}
    fps={FPS}
    width={WIDTH}
    height={HEIGHT}
  />
);
