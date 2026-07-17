import Link from "next/link";
import { Activity } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="border-b border-gray-800 bg-black sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 text-xl font-bold text-white">
          <Activity className="h-6 w-6 text-blue-500" />
          QuantData
        </Link>
        <div className="flex gap-6 text-sm text-gray-400">
          <Link href="/explorer" className="hover:text-white transition-colors">Explorer</Link>
          <Link href="/chat" className="hover:text-white transition-colors">AI Chat</Link>
          <Link href="/timeline" className="hover:text-white transition-colors">Timeline</Link>
          <Link href="/catalog" className="hover:text-white transition-colors">Catalog</Link>
        </div>
      </div>
    </nav>
  );
}
