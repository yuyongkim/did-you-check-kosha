import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./hooks/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "hsl(var(--primary))",
        secondary: "hsl(var(--secondary))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: "hsl(var(--card))",
        "card-foreground": "hsl(var(--card-foreground))",
        border: "hsl(var(--border))",
        accent: "hsl(var(--accent))",
        "accent-foreground": "hsl(var(--accent-foreground))",
        muted: "hsl(var(--muted))",
        "muted-foreground": "hsl(var(--muted-foreground))",
        danger: "hsl(var(--danger))",
        destructive: "hsl(var(--destructive))",
        warning: "hsl(var(--warning))",
        success: "hsl(var(--success))",
        "chart-piping": "hsl(var(--chart-piping))",
        "chart-vessel": "hsl(var(--chart-vessel))",
        "chart-rotating": "hsl(var(--chart-rotating))",
        "chart-electrical": "hsl(var(--chart-electrical))",
        "chart-instrumentation": "hsl(var(--chart-instrumentation))",
        "chart-steel": "hsl(var(--chart-steel))",
        "chart-civil": "hsl(var(--chart-civil))",
      },
      boxShadow: {
        panel: "0 1px 2px rgba(15, 23, 42, 0.08)",
      },
      borderRadius: {
        xl: "0.5rem",
      },
      keyframes: {
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        fadeUp: "fadeUp 180ms ease-out",
      },
      fontFamily: {
        sans: ["var(--font-sans)", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;

