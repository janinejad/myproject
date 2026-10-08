/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        background: '#FDF8F3', // رنگ پس‌زمینه
        primary: {
          DEFAULT: '#FF9933',  // رنگ اول (نارنجی)
          hover: '#E68524',
        },
        secondary: {
          DEFAULT: '#1A1A80',  // رنگ دوم (سرمه‌ای)
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