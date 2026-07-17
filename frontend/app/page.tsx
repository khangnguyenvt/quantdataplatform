import Link from "next/link";
import { ArrowRight, Search, MessageSquare, Clock, Database } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] text-center space-y-12">
      <div className="space-y-6 max-w-3xl">
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-7xl bg-gradient-to-r from-blue-400 to-emerald-400 text-transparent bg-clip-text">
          Alternative Data for Quants
        </h1>
        <p className="text-xl text-gray-400 max-w-2xl mx-auto">
          AI-powered ingestion and semantic querying for Clinical Trials, Patents, and Bank Stress Tests. Built for quantitative researchers.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl">
        <FeatureCard 
          href="/explorer"
          icon={<Search className="w-6 h-6 text-blue-400" />}
          title="Data Explorer"
          desc="Browse and filter through structured event tables."
        />
        <FeatureCard 
          href="/chat"
          icon={<MessageSquare className="w-6 h-6 text-emerald-400" />}
          title="AI Chat & NL2SQL"
          desc="Query the platform using natural language."
        />
        <FeatureCard 
          href="/timeline"
          icon={<Clock className="w-6 h-6 text-amber-400" />}
          title="Entity Timeline"
          desc="View a chronological feed of events for specific tickers."
        />
        <FeatureCard 
          href="/catalog"
          icon={<Database className="w-6 h-6 text-purple-400" />}
          title="Data Catalog"
          desc="View supported sources, schemas, and update frequencies."
        />
      </div>
    </div>
  );
}

function FeatureCard({ href, icon, title, desc }: any) {
  return (
    <Link href={href} className="group relative bg-gray-900 border border-gray-800 p-8 rounded-2xl hover:bg-gray-800/50 hover:border-gray-700 transition-all text-left overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-white/5 to-transparent blur-3xl opacity-0 group-hover:opacity-100 transition-opacity" />
      <div className="mb-4 bg-black/50 w-12 h-12 rounded-lg flex items-center justify-center border border-gray-800">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
        {title} <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
      </h3>
      <p className="text-gray-400">{desc}</p>
    </Link>
  );
}
