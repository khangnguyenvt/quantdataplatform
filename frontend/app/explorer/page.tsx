"use client";
import { useState, useEffect } from "react";
import EventCard from "@/components/EventCard";

export default function Explorer() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";
    fetch(`${apiUrl}/events?page_size=20`)
      .then(r => {
        if (!r.ok) throw new Error("Failed to fetch");
        return r.json();
      })
      .then(data => {
        setEvents(data.events || []);
        setLoading(false);
      })
      .catch(e => {
        setError("Failed to load events. Ensure backend is running.");
        setLoading(false);
      });
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Data Explorer</h1>
        <p className="text-gray-400">Browse the latest ingested events across all verticals.</p>
      </div>

      {loading && <div className="text-gray-500 animate-pulse">Loading events...</div>}
      {error && <div className="text-red-400 bg-red-950/50 p-4 rounded-lg border border-red-900">{error}</div>}
      
      {!loading && !error && (
        <div className="grid grid-cols-1 gap-4">
          {events.length === 0 ? (
            <div className="text-gray-500">No events found.</div>
          ) : (
            events.map((e: any) => <EventCard key={e.id} event={e} />)
          )}
        </div>
      )}
    </div>
  );
}
