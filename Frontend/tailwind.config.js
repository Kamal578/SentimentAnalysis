import { fontFamily } from 'tailwindcss/defaultTheme';

export const mode = 'jit';
export const purge = ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'];
export const darkMode = false;
export const theme = {
  extend: {
    fontFamily: {
      primary: ['Inter', ...fontFamily.sans],
    },
    screens: {
      xs: "320px",
      sm: "375px",
      sml: "500px",
      md: "667px",
      mdl: "768px",
      lg: "960px",
      lgl: "1024px",
      xl: "1280px",
    },
    colors: {
      primary: {
        400: '#00E0F3',
        500: '#00c4fd',
      },
      dark: '#333333',
    },
  },
};
export const variants = {
  extend: {},
};
