/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html","./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        'primary-green': '#2E7D32',
        'dark-green':    '#0a1f0c',
        'mid-green':     '#1a4a1e',
        'light-green':   '#E8F5E9',
        'water-blue':    '#0288D1',
        'sky-blue':      '#2196F3',
        'warning':       '#F59E0B',
        'danger':        '#DC2626',
      },
      fontFamily: { sans: ['Inter','system-ui','sans-serif'] },
      boxShadow: {
        'glow-g': '0 0 24px rgba(46,125,50,.4)',
        'glow-b': '0 0 24px rgba(2,136,209,.4)',
        'glow-r': '0 0 24px rgba(220,38,38,.4)',
        'soft':   '0 2px 8px rgba(0,0,0,.06)',
        'deep':   '0 8px 32px rgba(0,0,0,.14)',
      },
      borderRadius: { '2xl':'16px','3xl':'24px','4xl':'32px' },
    },
  },
  plugins: [],
}
