/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}",],
  theme: {
    extend: {
      colors: {
        customYellow: '#FFF5CD',
        customOrange: '#E78F81',
        customLightOrange: '#FFCFB3',
      },
    },
  },
  plugins: [],
}

