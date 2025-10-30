import { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

export function ErrorBox({ children }: Props) {
  return (
    <div className="container">
      <div className="card" style={{ border: "1px solid rgba(248, 113, 113, 0.4)", color: "#fecaca" }}>
        {children}
      </div>
    </div>
  );
}
