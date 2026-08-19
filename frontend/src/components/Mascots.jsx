export function PopcornMascot({ size = 140 }) {
  const width = size
  const height = size * (480 / 680)

  return (
    <svg width={width} height={height} viewBox="0 0 680 480" xmlns="http://www.w3.org/2000/svg" role="img">
      <title>FlixFit 팝콘 마스코트</title>
      <desc>팝콘 캐릭터가 리모컨을 든 모습</desc>
      <ellipse cx="340" cy="430" rx="120" ry="18" fill="#000000" opacity="0.12" />
      <g>
        <path d="M255 220 L285 420 Q285 435 300 435 L380 435 Q395 435 395 420 L425 220 Z" fill="#F6F1E7" />
        <path d="M270 250 L262 250 L285 420 Q285 435 300 435 L305 435 L282 260 Z" fill="#E24B4A" />
        <path d="M320 250 L310 250 L318 435 L335 435 L327 250 Z" fill="#E24B4A" />
        <path d="M368 250 L378 250 L363 435 L346 435 L358 250 Z" fill="#E24B4A" />
        <path d="M410 250 L418 250 L395 420 Q395 435 380 435 L375 435 L398 260 Z" fill="#E24B4A" />
      </g>
      <g>
        <circle cx="290" cy="215" r="26" fill="#FBF6EC" />
        <circle cx="322" cy="195" r="30" fill="#FBF6EC" />
        <circle cx="358" cy="192" r="30" fill="#FBF6EC" />
        <circle cx="392" cy="205" r="28" fill="#FBF6EC" />
        <circle cx="415" cy="228" r="24" fill="#FBF6EC" />
        <circle cx="270" cy="235" r="20" fill="#FBF6EC" />
        <circle cx="340" cy="180" r="24" fill="#FBF6EC" />
        <circle cx="378" cy="175" r="22" fill="#FBF6EC" />
        <circle cx="430" cy="245" r="20" fill="#FBF6EC" />
        <circle cx="305" cy="180" r="20" fill="#FBF6EC" />
      </g>
      <circle cx="360" cy="290" r="8" fill="#2C2C2A" />
      <circle cx="330" cy="290" r="8" fill="#2C2C2A" />
      <ellipse cx="332.5" cy="287.5" rx="2.5" ry="2.5" fill="#FFFFFF" />
      <ellipse cx="362.5" cy="287.5" rx="2.5" ry="2.5" fill="#FFFFFF" />
      <ellipse cx="316" cy="298" rx="7" ry="4" fill="#F0997B" opacity="0.6" />
      <ellipse cx="374" cy="298" rx="7" ry="4" fill="#F0997B" opacity="0.6" />
      <path d="M330 312 Q345 324 360 312" stroke="#2C2C2A" strokeWidth="3" fill="none" strokeLinecap="round" />
      <path d="M262 300 Q230 320 250 345" stroke="#F6F1E7" strokeWidth="16" fill="none" strokeLinecap="round" />
      <circle cx="255" cy="350" r="13" fill="#F6F1E7" />
      <g transform="translate(232,323) rotate(-8)">
        <rect x="0" y="0" width="22" height="52" rx="8" fill="#2C2C2A" />
        <rect x="4" y="5" width="14" height="9" rx="2.5" fill="#4A4A47" />
        <circle cx="11" cy="22" r="2.8" fill="#E24B4A" />
        <circle cx="11" cy="31" r="2.3" fill="#888" />
        <circle cx="11" cy="39" r="2.3" fill="#888" />
        <circle cx="11" cy="46" r="2.3" fill="#888" />
      </g>
      <path d="M418 300 Q450 320 430 345" stroke="#F6F1E7" strokeWidth="16" fill="none" strokeLinecap="round" />
      <circle cx="425" cy="350" r="13" fill="#F6F1E7" />
      <ellipse cx="288" cy="400" rx="14" ry="10" fill="#F6F1E7" />
      <ellipse cx="392" cy="400" rx="14" ry="10" fill="#F6F1E7" />
    </svg>
  )
}

export function TvIcon({ size = 28 }) {
  const width = size
  const height = size * (260 / 380)

  return (
    <svg width={width} height={height} viewBox="0 0 380 260" xmlns="http://www.w3.org/2000/svg" role="img">
      <title>FlixFit TV 아이콘</title>
      <desc>웃고 있는 심플한 TV 캐릭터</desc>
      <ellipse cx="200" cy="245" rx="150" ry="12" fill="#000" opacity="0.1" />
      <rect x="180" y="222" width="40" height="14" rx="3" fill="#1A1A1A" />
      <rect x="140" y="232" width="120" height="12" rx="4" fill="#1A1A1A" />
      <rect x="50" y="30" width="300" height="200" rx="16" fill="#1A1A1A" stroke="#3A3A3A" strokeWidth="4" />
      <rect x="66" y="46" width="268" height="168" rx="6" fill="#E24B4A" />
      <circle cx="170" cy="125" r="10" fill="#1A1A1A" />
      <circle cx="230" cy="125" r="10" fill="#1A1A1A" />
      <ellipse cx="173" cy="122" rx="3" ry="3" fill="#fff" />
      <ellipse cx="233" cy="122" rx="3" ry="3" fill="#fff" />
      <path d="M168 148 Q200 168 232 148" stroke="#1A1A1A" strokeWidth="4" fill="none" strokeLinecap="round" />
      <ellipse cx="145" cy="135" rx="10" ry="6" fill="#993C1D" opacity="0.5" />
      <ellipse cx="255" cy="135" rx="10" ry="6" fill="#993C1D" opacity="0.5" />
      <circle cx="328" cy="34" r="3.5" fill="#5DCAA5" />
    </svg>
  )
}

export function SofaDogIcon({ size = 28 }) {
  const width = size
  const height = size * (340 / 460)

  return (
    <svg width={width} height={height} viewBox="0 0 460 340" xmlns="http://www.w3.org/2000/svg" role="img">
      <title>FlixFit 비숑 프리제가 소파 정중앙에 앉아있는 마스코트</title>
      <desc>하얗고 폭신한 비숑 프리제가 리모컨을 들고 좁은 소파 정가운데 앉아있다</desc>
      <ellipse cx="230" cy="325" rx="100" ry="14" fill="#000" opacity="0.12" />
      <g>
        <rect x="140" y="220" width="180" height="70" rx="16" fill="#993C1D" />
        <rect x="112" y="188" width="30" height="105" rx="14" fill="#993C1D" />
        <rect x="318" y="188" width="30" height="105" rx="14" fill="#993C1D" />
        <rect x="140" y="192" width="180" height="46" rx="12" fill="#D85A30" />
        <rect x="147" y="280" width="13" height="30" rx="5" fill="#712B13" />
        <rect x="300" y="280" width="13" height="30" rx="5" fill="#712B13" />
        <rect x="194" y="280" width="13" height="30" rx="5" fill="#712B13" />
        <rect x="253" y="280" width="13" height="30" rx="5" fill="#712B13" />
      </g>
      <g transform="translate(43,58) scale(0.55)">
        <ellipse cx="340" cy="255" rx="80" ry="55" fill="#FBF9F4" />
        <circle cx="270" cy="250" r="26" fill="#FBF9F4" />
        <circle cx="410" cy="250" r="26" fill="#FBF9F4" />
        <circle cx="295" cy="215" r="24" fill="#FBF9F4" />
        <circle cx="385" cy="215" r="24" fill="#FBF9F4" />
        <circle cx="340" cy="300" r="26" fill="#FBF9F4" />
        <circle cx="280" cy="295" r="22" fill="#FBF9F4" />
        <circle cx="400" cy="295" r="22" fill="#FBF9F4" />
        <circle cx="340" cy="165" r="90" fill="#FFFFFF" />
        <circle cx="262" cy="150" r="34" fill="#FFFFFF" />
        <circle cx="418" cy="150" r="34" fill="#FFFFFF" />
        <circle cx="280" cy="95" r="30" fill="#FFFFFF" />
        <circle cx="400" cy="95" r="30" fill="#FFFFFF" />
        <circle cx="340" cy="80" r="32" fill="#FFFFFF" />
        <circle cx="255" cy="200" r="26" fill="#FFFFFF" />
        <circle cx="425" cy="200" r="26" fill="#FFFFFF" />
        <ellipse cx="285" cy="180" rx="18" ry="26" fill="#EFEAD8" transform="rotate(-15 285 180)" />
        <ellipse cx="395" cy="180" rx="18" ry="26" fill="#EFEAD8" transform="rotate(15 395 180)" />
        <circle cx="308" cy="165" r="10" fill="#2C2C2A" />
        <circle cx="372" cy="165" r="10" fill="#2C2C2A" />
        <circle cx="311" cy="161" r="3" fill="#FFFFFF" />
        <circle cx="375" cy="161" r="3" fill="#FFFFFF" />
        <ellipse cx="340" cy="182" rx="9" ry="7" fill="#2C2C2A" />
        <path d="M340 189 L340 197" stroke="#2C2C2A" strokeWidth="2.5" strokeLinecap="round" />
        <path d="M328 202 Q340 210 352 202" stroke="#2C2C2A" strokeWidth="2.5" fill="none" strokeLinecap="round" />
        <ellipse cx="290" cy="192" rx="10" ry="7" fill="#F5A6A6" opacity="0.7" />
        <ellipse cx="390" cy="192" rx="10" ry="7" fill="#F5A6A6" opacity="0.7" />
        <circle cx="290" cy="290" r="20" fill="#FFFFFF" />
        <circle cx="390" cy="290" r="20" fill="#FFFFFF" />
      </g>
      <g transform="translate(258,208) rotate(-10)">
        <rect x="0" y="0" width="12" height="26" rx="5" fill="#2C2C2A" />
        <circle cx="6" cy="7" r="1.8" fill="#E24B4A" />
        <circle cx="6" cy="13" r="1.5" fill="#888" />
        <circle cx="6" cy="18" r="1.5" fill="#888" />
      </g>
    </svg>
  )
}
