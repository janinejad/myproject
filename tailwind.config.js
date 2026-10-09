/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        bgMain: '#FDF8F3',
        brandPrimary: {
          DEFAULT: '#FF9933',
          hover: '#e08324',
        },
        brandSecondary: {
          DEFAULT: '#1A1A80',
          hover: '#131366',
        }
      },
      fontFamily: {
        sans: ['Vazirmatn', 'sans-serif'],
      }
    },
  },
  plugins: [],
}