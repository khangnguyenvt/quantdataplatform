"use client";
import { useState } from "react";
import EventCard from "@/components/EventCard";

export default function Timeline() {
  const [ticker, setTicker] = useState("");
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const search = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticker.trim()) return;
    
    setLoading(true);
    setError("");
    
    try {
      const r = await fetch(`http://localhost:8000/api/events?ticker=${ticker.toUpperCase()}&page_size=50`);
      if (!r.ok) throw new Error("Failed to fetch");
      const data = await r.json();
      setEvents(data.events || []);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Entity Timeline</h1>
        <p className="text-gray-400">Search for a ticker to see a chronological feed of its events.</p>
      </div>

      <form onSubmit={search} className="flex gap-4">
        <input 
          type="text"
          value={ticker}
          onChange={e => setTicker(e.target.value)}
          placeholder="Enter Ticker (e.g. PFE, JPM)"
          className="bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
        />
        <button type="submit" className="bg-blue-600 px-6 py-2 rounded-lg font-medium hover:bg-blue-500">
          Search
        </button>
      </form>

      {loading && <div className="text-gray-500">Loading...</div>}
      {error && <div className="text-red-400">{error}</div>}

      <div className="relative border-l border-gray-800 ml-4 pl-8 space-y-8 py-4">
        {events.map((e: any) => (
          <div key={e.id} className="relative">
            <div className="absolute -left-[41px] top-4 w-4 h-4 rounded-full bg-blue-500 border-4 border-black" />
            <EventCard event={e} />
          </div>
        ))}
      </div>
    </div>
  );
}
