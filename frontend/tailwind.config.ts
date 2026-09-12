import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./features/**/*.{ts,tsx}"],
  theme: { extend: { colors: { ink: "#0b1020", cloud: "#f7f8fc", electric: "#615fff", cyan: "#45d8ff" }, boxShadow: { soft: "0 16px 50px rgba(15, 23, 42, .09)", glow: "0 18px 50px rgba(97, 95, 255, .28)" }, borderRadius: { "4xl": "2rem" } } },
  plugins: []
} satisfies Config;
