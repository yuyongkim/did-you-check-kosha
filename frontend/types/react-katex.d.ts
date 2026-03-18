declare module "react-katex" {
  import type { ComponentType } from "react";

  interface MathComponentProps {
    math: string;
    errorColor?: string;
    renderError?: (error: unknown) => string;
  }

  export const BlockMath: ComponentType<MathComponentProps>;
  export const InlineMath: ComponentType<MathComponentProps>;
}
