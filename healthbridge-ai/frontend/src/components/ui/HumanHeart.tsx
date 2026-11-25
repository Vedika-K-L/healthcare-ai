import { useId } from 'react';

type HumanHeartProps = {
  className?: string;
};

/** A softly glowing anatomical illustration for the HealthBridge landing page. */
export function HumanHeart({ className = '' }: HumanHeartProps) {
  const id = useId().replace(/:/g, '');
  const muscle = 'url(#' + id + '-muscle)';
  const artery = 'url(#' + id + '-artery)';
  const vein = 'url(#' + id + '-vein)';

  return (
    <div className={'human-heart-stage relative flex min-h-[360px] items-center justify-center overflow-hidden rounded-[28px] bg-[#090611] p-6 ' + className}>
      <span className="human-heart-star heart-star-one" aria-hidden="true" />
      <span className="human-heart-star heart-star-two" aria-hidden="true" />
      <span className="human-heart-star heart-star-three" aria-hidden="true" />
      <svg
        className="human-heart-svg"
        viewBox="0 0 320 360"
        role="img"
        aria-labelledby={id + '-title ' + id + '-description'}
        xmlns="http://www.w3.org/2000/svg"
      >
        <title id={id + '-title'}>Anatomical human heart</title>
        <desc id={id + '-description'}>
          A luminous medical illustration showing the atria, ventricles, aorta, pulmonary artery, veins, and coronary arteries.
        </desc>
        <defs>
          <linearGradient id={id + '-muscle'} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#ff9a91" /><stop offset=".44" stopColor="#e73f55" /><stop offset="1" stopColor="#741632" />
          </linearGradient>
          <linearGradient id={id + '-artery'} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#ffc0ad" /><stop offset="1" stopColor="#be2847" />
          </linearGradient>
          <linearGradient id={id + '-vein'} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#a9edff" /><stop offset="1" stopColor="#397bb9" />
          </linearGradient>
        </defs>
        <path d="M119 148C111 116 112 76 119 39M196 150C208 115 209 79 203 43" fill="none" stroke={vein} strokeLinecap="round" strokeWidth="25" />
        <path d="M119 51V27M203 53L207 28" fill="none" stroke="#a5e9fa" strokeLinecap="round" strokeWidth="15" />
        <path d="M153 151C131 127 128 99 143 72C156 48 180 49 190 70C200 92 187 120 176 145" fill="none" stroke={artery} strokeLinecap="round" strokeLinejoin="round" strokeWidth="29" />
        <path d="M151 72C147 54 143 40 136 29M181 69C185 51 193 40 203 31" fill="none" stroke="#f8897f" strokeLinecap="round" strokeWidth="13" />
        <path d="M158 166C143 143 128 132 108 128C91 125 78 132 68 145" fill="none" stroke={vein} strokeLinecap="round" strokeLinejoin="round" strokeWidth="22" />
        <path d="M159 145C136 119 104 117 79 135C48 157 45 201 59 239C76 283 119 323 160 347C198 326 238 290 259 249C279 210 276 164 246 139C222 118 188 121 159 145Z" fill={muscle} stroke="#ffb0a2" strokeOpacity=".8" strokeWidth="4" />
        <path d="M82 151C99 132 126 136 145 155L151 200C131 191 109 192 88 208C76 190 74 165 82 151Z" fill="#fa887e" opacity=".94" />
        <path d="M174 155C194 135 220 133 240 151C251 167 249 191 239 207C218 192 195 191 169 201Z" fill="#cb3850" opacity=".96" />
        <path d="M157 183C151 226 153 282 160 337" fill="none" stroke="#68182f" strokeLinecap="round" strokeWidth="8" opacity=".82" />
        <path d="M91 211C111 197 133 199 151 211C148 255 152 296 160 337C129 317 101 284 85 251C79 235 81 221 91 211Z" fill="#b72c48" opacity=".76" />
        <path d="M169 210C190 197 215 199 235 214C244 226 239 245 229 263C211 292 186 318 160 337C166 294 168 251 169 210Z" fill="#851d39" opacity=".78" />
        <path d="M159 177C143 193 126 204 109 213C98 220 95 233 101 245M145 202C131 219 126 238 130 257M168 187C185 198 200 208 214 224C221 233 220 244 214 253M183 202C196 220 201 237 197 253" fill="none" stroke="#ffc0ad" strokeLinecap="round" strokeLinejoin="round" strokeWidth="5" />
        <path d="M159 145C136 119 104 117 79 135C48 157 45 201 59 239C76 283 119 323 160 347C198 326 238 290 259 249C279 210 276 164 246 139C222 118 188 121 159 145Z" fill="none" stroke="#ffd1c5" strokeOpacity=".55" strokeWidth="2" />
      </svg>
    </div>
  );
}

export default HumanHeart;
