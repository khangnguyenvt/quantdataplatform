"use client";
import { useState } from "react";
import { Send, Bot, Database } from "lucide-react";

export default function Chat() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setLoading(true);
    setError("");
    
    try {
      const r = await fetch("http://localhost:8000/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: query })
      });
      
      if (!r.ok) {
        throw new Error("Failed to query");
      }
      
      const data = await r.json();
      setResult(data);
    } catch (e: any) {
      setError(e.message || "Error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">AI Chat (NL2SQL)</h1>
        <p className="text-gray-400">Ask questions in plain English and let Gemini generate the SQL.</p>
      </div>

      <form onSubmit={handleAsk} className="relative">
        <input 
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. Which banks failed the 2023 DFAST stress test?"
          className="w-full bg-gray-900 border border-gray-700 rounded-xl px-6 py-4 pr-16 text-white focus:outline-none focus:border-blue-500 transition-colors placeholder:text-gray-600"
        />
        <button 
          type="submit" 
          disabled={loading || !query.trim()}
          className="absolute right-2 top-2 p-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-white disabled:opacity-50 transition-colors"
        >
          <Send className="w-5 h-5" />
        </button>
      </form>

      {error && <div className="text-red-400">{error}</div>}
      
      {loading && (
        <div className="flex items-center gap-3 text-gray-400 animate-pulse p-4">
          <Bot className="w-5 h-5" /> <span>Thinking... generating SQL...</span>
        </div>
      )}

      {result && !loading && (
        <div className="space-y-6">
          <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
            <div className="bg-black/50 px-4 py-3 border-b border-gray-800 flex items-center gap-2 text-gray-400 text-sm font-mono">
              <Database className="w-4 h-4" /> Generated SQL
            </div>
            <pre className="p-4 text-sm text-green-400 overflow-x-auto">
              {result.sql_generated}
            </pre>
          </div>
          
          <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
             <div className="px-4 py-3 border-b border-gray-800 text-white font-medium">
               Result Data ({result.events?.length || 0} rows)
             </div>
             <div className="p-4 overflow-x-auto">
                <table className="w-full text-left text-sm text-gray-400">
                  <thead className="text-xs text-gray-500 uppercase bg-black/30">
                    <tr>
                      {result.events?.length > 0 ? (
                        Object.keys(result.events[0]).map(k => <th key={k} className="px-4 py-2">{k}</th>)
                      ) : (
                        <th className="px-4 py-2">No data</th>
                      )}
                    </tr>
                  </thead>
                  <tbody>
                    {result.events?.map((row: any, i: number) => (
                      <tr key={i} className="border-b border-gray-800 hover:bg-gray-800/50">
                        {Object.values(row).map((val: any, j: number) => (
                          <td key={j} className="px-4 py-2 truncate max-w-[200px]">
                            {typeof val === 'object' ? JSON.stringify(val) : String(val)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
             </div>
          </div>
        </div>
      )}
    </div>
  );
}
