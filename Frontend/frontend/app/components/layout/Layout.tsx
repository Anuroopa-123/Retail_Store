import Sidebar from "./sidebar";
import "./layout.css";

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({
  children,
}: LayoutProps) {
  return (
    <div className="app-layout">
      <Sidebar />

      <main className="content">
        {children}
      </main>
    </div>
  );
}