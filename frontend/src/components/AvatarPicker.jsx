export const AVATAR_BACKGROUNDS = [
  '#2C2C2A',
  '#F2D9A8',
  '#E24B4A',
  '#BFD9F2',
  '#F6E4D7',
  '#233142',
  '#F5C6B8',
  '#3A2E28',
  '#BFE8D4',
  '#1A1A1A',
]

export const AVATAR_LABELS = [
  '팝콘',
  '필름 릴',
  '클래퍼보드',
  '3D 안경',
  '영화 티켓',
  '카메라',
  '콜라+팝콘 콤보',
  'VHS 테이프',
  '트로피',
  '무대 커튼',
]

function PopcornGlyph() {
  return (
    <>
      <circle cx="42" cy="40" r="9" fill="#F6F1E7" />
      <circle cx="52" cy="36" r="10" fill="#F6F1E7" />
      <circle cx="62" cy="41" r="9" fill="#F6F1E7" />
      <path d="M39 44 L45 73 Q45 76 48 76 L56 76 Q59 76 59 73 L65 44 Z" fill="#F6F1E7" />
      <path d="M46 44 L49 76 L52.5 76 L50.5 44 Z" fill="#E24B4A" />
      <path d="M58 44 L55 76 L58.5 76 L61 44 Z" fill="#E24B4A" />
    </>
  )
}

function FilmReelGlyph() {
  return (
    <>
      <circle cx="50" cy="50" r="19" fill="none" stroke="#2C2C2A" strokeWidth="5" />
      <circle cx="50" cy="50" r="5" fill="#2C2C2A" />
      {[0, 60, 120, 180, 240, 300].map((angle) => {
        const rad = (angle * Math.PI) / 180
        const cx = 50 + Math.cos(rad) * 12
        const cy = 50 + Math.sin(rad) * 12
        return <circle key={angle} cx={cx} cy={cy} r="4" fill="#2C2C2A" />
      })}
    </>
  )
}

function ClapperboardGlyph() {
  return (
    <>
      <rect x="30" y="46" width="40" height="27" rx="3" fill="#FBF6EC" />
      <rect x="30" y="46" width="40" height="27" rx="3" fill="none" stroke="#1A1A1A" strokeWidth="2.5" />
      <g transform="rotate(-12 50 39)">
        <rect x="28" y="33" width="44" height="10" rx="2" fill="#1A1A1A" />
        <rect x="31" y="33" width="5" height="10" fill="#FBF6EC" />
        <rect x="41" y="33" width="5" height="10" fill="#FBF6EC" />
        <rect x="51" y="33" width="5" height="10" fill="#FBF6EC" />
        <rect x="61" y="33" width="5" height="10" fill="#FBF6EC" />
      </g>
    </>
  )
}

function GlassesGlyph() {
  return (
    <>
      <rect x="26" y="47" width="20" height="15" rx="4" fill="#E24B4A" stroke="#1A1A1A" strokeWidth="3" />
      <rect x="54" y="47" width="20" height="15" rx="4" fill="#5DCAA5" stroke="#1A1A1A" strokeWidth="3" />
      <line x1="46" y1="54" x2="54" y2="54" stroke="#1A1A1A" strokeWidth="3" />
      <line x1="26" y1="51" x2="18" y2="47" stroke="#1A1A1A" strokeWidth="3" strokeLinecap="round" />
      <line x1="74" y1="51" x2="82" y2="47" stroke="#1A1A1A" strokeWidth="3" strokeLinecap="round" />
    </>
  )
}

function TicketGlyph() {
  return (
    <g transform="rotate(-10 50 50)">
      <rect x="24" y="38" width="52" height="26" rx="4" fill="#E24B4A" />
      <line x1="50" y1="38" x2="50" y2="64" stroke="#F6E4D7" strokeWidth="2" strokeDasharray="3,3" />
      <path d="M33 51 l1.6 3.3 3.6 0.5 -2.6 2.6 0.6 3.6 -3.2 -1.7 -3.2 1.7 0.6 -3.6 -2.6 -2.6 3.6 -0.5 Z" fill="#F6E4D7" />
      <line x1="58" y1="47" x2="70" y2="47" stroke="#F6E4D7" strokeWidth="2" strokeLinecap="round" />
      <line x1="58" y1="53" x2="70" y2="53" stroke="#F6E4D7" strokeWidth="2" strokeLinecap="round" />
      <line x1="58" y1="59" x2="66" y2="59" stroke="#F6E4D7" strokeWidth="2" strokeLinecap="round" />
    </g>
  )
}

function CameraGlyph() {
  return (
    <>
      <rect x="40" y="36" width="14" height="8" rx="2" fill="#F6F1E7" />
      <rect x="26" y="43" width="48" height="26" rx="4" fill="#F6F1E7" />
      <circle cx="50" cy="57" r="10" fill="#1A1A1A" />
      <circle cx="50" cy="57" r="5" fill="#5DCAA5" />
      <circle cx="66" cy="49" r="2.2" fill="#E24B4A" />
    </>
  )
}

function ComboGlyph() {
  return (
    <>
      <path d="M25 42 L31 70 Q31 73 34 73 L40 73 Q43 73 43 70 L46 42 Z" fill="#FBF6EC" />
      <path d="M30 42 L34 73 L37 73 L34.5 42 Z" fill="#E24B4A" />
      <rect x="26" y="38" width="19" height="6" rx="2" fill="#E24B4A" />
      <path d="M56 48 L58 74 Q58 76 60 76 L70 76 Q72 76 72 74 L74 48 Z" fill="#F6F1E7" />
      <path d="M60 48 L61.5 76 L64 76 L63 48 Z" fill="#E24B4A" />
      <path d="M70 48 L68.5 76 L66 76 L67 48 Z" fill="#E24B4A" />
      <circle cx="59" cy="42" r="6" fill="#F6F1E7" />
      <circle cx="65" cy="39" r="7" fill="#F6F1E7" />
      <circle cx="71" cy="43" r="6" fill="#F6F1E7" />
    </>
  )
}

function VhsGlyph() {
  return (
    <>
      <rect x="20" y="38" width="60" height="32" rx="4" fill="#F6F1E7" />
      <rect x="26" y="44" width="48" height="13" rx="2" fill="#1A1A1A" />
      <circle cx="38" cy="50.5" r="5" fill="#F6F1E7" />
      <circle cx="62" cy="50.5" r="5" fill="#F6F1E7" />
      <rect x="26" y="60" width="48" height="6" rx="1.5" fill="#E24B4A" opacity="0.85" />
    </>
  )
}

function TrophyGlyph() {
  return (
    <>
      <path d="M38 36 h24 v10 q0 13 -12 13 q-12 0 -12 -13 Z" fill="#F5C84C" />
      <path d="M38 40 q-9 0 -9 8 q0 7 9 7" stroke="#F5C84C" strokeWidth="3.5" fill="none" />
      <path d="M62 40 q9 0 9 8 q0 7 -9 7" stroke="#F5C84C" strokeWidth="3.5" fill="none" />
      <rect x="46.5" y="58" width="7" height="9" fill="#F5C84C" />
      <rect x="38" y="67" width="24" height="6" rx="2" fill="#F5C84C" />
      <circle cx="50" cy="44" r="3.5" fill="#E24B4A" />
    </>
  )
}

function CurtainGlyph() {
  return (
    <>
      <path d="M26 28 Q38 50 26 76 L38 76 Q48 50 38 28 Z" fill="#8B060D" />
      <path d="M74 28 Q62 50 74 76 L62 76 Q52 50 62 28 Z" fill="#8B060D" />
      <path d="M26 28 Q38 50 26 76 L32 76 Q42 50 32 28 Z" fill="#E24B4A" opacity="0.7" />
      <path d="M74 28 Q62 50 74 76 L68 76 Q58 50 68 28 Z" fill="#E24B4A" opacity="0.7" />
      <circle cx="27" cy="29" r="3.2" fill="#F5C84C" />
      <circle cx="73" cy="29" r="3.2" fill="#F5C84C" />
      <ellipse cx="50" cy="58" rx="9" ry="16" fill="#F6E4D7" opacity="0.18" />
    </>
  )
}

const AVATAR_GLYPHS = [
  PopcornGlyph,
  FilmReelGlyph,
  ClapperboardGlyph,
  GlassesGlyph,
  TicketGlyph,
  CameraGlyph,
  ComboGlyph,
  VhsGlyph,
  TrophyGlyph,
  CurtainGlyph,
]

export function AvatarIcon({ avatarId, size = 40 }) {
  const index = ((avatarId ?? 1) - 1 + AVATAR_GLYPHS.length) % AVATAR_GLYPHS.length
  const background = AVATAR_BACKGROUNDS[index]
  const Glyph = AVATAR_GLYPHS[index]
  const label = AVATAR_LABELS[index]

  return (
    <svg width={size} height={size} viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img">
      <title>{`아바타 - ${label}`}</title>
      <circle cx="50" cy="50" r="50" fill={background} />
      <Glyph />
    </svg>
  )
}

function AvatarPicker({ value, onChange }) {
  return (
    <div className="avatar-picker" role="radiogroup" aria-label="아바타 선택">
      {AVATAR_GLYPHS.map((_, index) => {
        const avatarId = index + 1
        const selected = value === avatarId

        return (
          <button
            key={avatarId}
            type="button"
            className={`avatar-picker-item${selected ? ' selected' : ''}`}
            aria-pressed={selected}
            aria-label={AVATAR_LABELS[index]}
            onClick={() => onChange(avatarId)}
          >
            <AvatarIcon avatarId={avatarId} size={48} />
          </button>
        )
      })}
    </div>
  )
}

export default AvatarPicker
