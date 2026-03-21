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
        "panel-hover": "0 2px 8px rgba(15, 23, 42, 0.1), 0 1px 2px rgba(15, 23, 42, 0.06)",
        "panel-lg": "0 4px 16px rgba(15, 23, 42, 0.08), 0 1px 3px rgba(15, 23, 42, 0.05)",
        glow: "0 0 20px rgba(56, 152, 195, 0.15)",
      },
      borderRadius: {
        xl: "0.5rem",
        "2xl": "0.75rem",
      },
      keyframes: {
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        slideIn: {
          "0%": { opacity: "0", transform: "translateX(-6px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
        scaleIn: {
          "0%": { opacity: "0", transform: "scale(0.95)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      animation: {
        fadeUp: "fadeUp 180ms ease-out",
        slideIn: "slideIn 200ms cubic-bezier(0.2, 0.8, 0.2, 1)",
        scaleIn: "scaleIn 200ms cubic-bezier(0.2, 0.8, 0.2, 1)",
        shimmer: "shimmer 2s linear infinite",
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

