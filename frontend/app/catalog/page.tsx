export default function Catalog() {
  const sources = [
    {
      name: "ClinicalTrials.gov",
      vertical: "Pharma / Biotech",
      updateFreq: "Every 6 hours",
      fields: "Phase, Status, Indication, Enrollment"
    },
    {
      name: "PatentsView",
      vertical: "Technology & IP",
      updateFreq: "Weekly",
      fields: "Title, Assignee, Tech Clusters, CPC Codes"
    },
    {
      name: "Fed CCAR / DFAST",
      vertical: "Financials (Stress Tests)",
      updateFreq: "Annually",
      fields: "Test Year, Scenarios, CET1 Ratios, Loss Projections"
    }
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Data Catalog</h1>
        <p className="text-gray-400">Supported data sources and schema overview.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sources.map(s => (
          <div key={s.name} className="bg-gray-900 border border-gray-800 p-6 rounded-xl">
            <h3 className="text-xl font-bold text-white mb-1">{s.name}</h3>
            <p className="text-blue-400 text-sm mb-4">{s.vertical}</p>
            
            <div className="space-y-3">
              <div>
                <span className="block text-xs text-gray-500 uppercase font-semibold tracking-wider">Update Frequency</span>
                <span className="text-gray-300">{s.updateFreq}</span>
              </div>
              <div>
                <span className="block text-xs text-gray-500 uppercase font-semibold tracking-wider">Structured Fields</span>
                <span className="text-gray-300 text-sm">{s.fields}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
