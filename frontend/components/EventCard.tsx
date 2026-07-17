import { cn } from "@/lib/utils";

interface Event {
  id: string;
  event_type: string;
  source: string;
  entity_name: string;
  ticker?: string;
  published_at: string;
  headline: string;
  structured_fields: any;
}

export default function EventCard({ event }: { event: Event }) {
  const date = new Date(event.published_at).toLocaleDateString();
  
  return (
    <div className="bg-gray-900 border border-gray-800 p-5 rounded-xl hover:border-gray-700 transition-colors">
      <div className="flex justify-between items-start mb-3">
        <div className="flex gap-2 items-center">
          <span className="font-bold text-white">{event.entity_name}</span>
          {event.ticker && (
            <span className="text-xs bg-blue-900/50 text-blue-400 px-2 py-0.5 rounded-full border border-blue-800">
              ${event.ticker}
            </span>
          )}
        </div>
        <span className="text-xs text-gray-500">{date}</span>
      </div>
      
      <p className="text-gray-300 font-medium mb-4">{event.headline}</p>
      
      <div className="flex flex-wrap gap-2 mt-4">
        <Badge label="Type" value={event.event_type.replace("_", " ")} />
        <Badge label="Source" value={event.source} />
        {event.structured_fields?.phase && (
          <Badge label="Phase" value={event.structured_fields.phase} />
        )}
        {event.structured_fields?.test_year && (
          <Badge label="Year" value={event.structured_fields.test_year} />
        )}
      </div>
    </div>
  );
}

function Badge({ label, value }: { label: string, value: string | number }) {
  return (
    <div className="text-xs flex items-center border border-gray-800 rounded bg-black overflow-hidden">
      <span className="px-2 py-1 text-gray-500 border-r border-gray-800">{label}</span>
      <span className="px-2 py-1 text-gray-300 capitalize">{value}</span>
    </div>
  );
}
