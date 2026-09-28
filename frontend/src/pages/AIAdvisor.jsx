import React, { useState, useEffect } from 'react';
import { Cpu, CheckCircle2, Droplets, Clock, Loader2, Zap } from 'lucide-react';
import { fetchFields } from '../services/api';

const S = {
  IRRIGATE:       { l:'IRRIGATE',      c:'text-red-500',   b:'bg-red-50 border-red-200' },
  WAIT_FOR_RAIN:  { l:'WAIT FOR RAIN', c:'text-blue-500',  b:'bg-blue-50 border-blue-200' },
  NO_IRRIGATION:  { l:'NO IRRIGATION', c:'text-green-500', b:'bg-green-50 border-green-200' },
  MONITOR:        { l:'MONITOR',       c:'text-amber-500', b:'bg-amber-50 border-amber-200' },
  GOOD:           { l:'OPTIMAL',       c:'text-green-500', b:'bg-green-50 border-green-200' },
};

const CondRow = ({ icon, label, val, alert }) => (
  <div className={`flex items-center justify-between p-4 rounded-2xl mb-2 transition-colors
                   ${alert ? 'bg-red-50 text-red-900' : 'bg-gray-50 hover:bg-gray-100 text-gray-800'}`}>
    <div className="flex items-center gap-3 font-semibold">
      <span className="text-xl">{icon}</span>
      <span className={alert ? 'text-red-700' : 'text-gray-500'}>{label}</span>
    </div>
    <span className="text-xl font-black">{val}</span>
  </div>
);

export default function AIAdvisor() {
  const [fields, setFields] = useState([]);
  const [sel, setSel] = useState(null);
  const [rec, setRec] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    fetchFields().then(d => {
      setFields(d);
      setSel(d.find(f => f.status === 'IRRIGATE') || d[0]);
    }).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!sel) return;
    setAnalyzing(true);
    fetch(`http://127.0.0.1:8000/api/fields/${sel.id}/recommendation`)
      .then(r => r.json())
      .then(d => {
        setRec(null); // Force unmount to replay animations
        setTimeout(() => setRec(d), 50);
      })
      .finally(() => setAnalyzing(false));
  }, [sel]);

  if (loading) return <div className="h-48 shimmer" />;

  const st = rec ? (S[rec.status] || S.MONITOR) : S.MONITOR;

  return (
    <div className="max-w-[1000px] mx-auto space-y-8 pb-10">

      {/* ── Header ── */}
      <div className="anim-fade-up d0 text-center space-y-3">
        <div className="w-16 h-16 mx-auto rounded-full bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center anim-pulse-g shadow-glow-g">
          <Cpu className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl font-black tracking-tight text-gray-900">AI Advisor</h1>
        <p className="text-gray-500 font-medium">Rule-engine driven intelligence for every field.</p>
      </div>

      {/* ── Field Selector ── */}
      <div className="flex flex-wrap justify-center gap-3 anim-fade-up d1">
        {fields.map(f => (
          <button key={f.id} onClick={() => setSel(f)}
            className={`px-5 py-3 rounded-xl text-sm font-bold border-2 transition-all
                        ${sel?.id === f.id 
                          ? 'border-primary-green bg-green-50 text-primary-green shadow-glow-g' 
                          : 'border-transparent bg-white text-gray-500 hover:bg-gray-50'}`}>
            {f.name} <span className="opacity-50 font-normal ml-2">{f.crop}</span>
          </button>
        ))}
      </div>

      {/* ── Analysis Panel ── */}
      {sel && (
        <div className="card overflow-hidden anim-fade-up d2">
          
          {/* Header strip */}
          <div className="bg-dark-green px-8 py-6 text-white flex justify-between items-center">
            <div>
              <p className="text-green-400 font-bold text-xs uppercase tracking-widest mb-1">Target Field</p>
              <h2 className="text-2xl font-black">{sel.name}</h2>
            </div>
            <div className="text-right">
              <p className="text-white/50 text-xs font-bold uppercase tracking-widest mb-1">Crop Stage</p>
              <p className="font-bold">{sel.growth_stage}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2">
            {/* Left: Telemetry */}
            <div className="p-8 border-r border-gray-100">
              <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest mb-6">Live Telemetry</h3>
              <CondRow icon="🌱" label="Soil Moisture" val={`${sel.soil_moisture ?? '--'}%`} alert={sel.soil_moisture < 35} />
              <CondRow icon="🌡️" label="Temperature"  val={`${sel.temperature ?? '--'}°C`} />
              <CondRow icon="💧" label="Humidity"     val={`${sel.humidity ?? '--'}%`} />
              <CondRow icon="🌧️" label="Rain Prob."   val={`${sel.rain_probability ?? '--'}%`} />
            </div>

            {/* Right: Recommendation */}
            <div className="p-8 bg-gray-50/50">
              <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest mb-6">Engine Verdict</h3>
              
              {analyzing ? (
                <div className="flex flex-col items-center justify-center h-48 text-gray-400 space-y-4">
                  <Loader2 className="w-8 h-8 anim-spin-slow text-primary-green" />
                  <p className="font-bold animate-pulse">Running rules...</p>
                </div>
              ) : rec && (
                <div className="anim-fade-in">
                  
                  {/* Verdict Badge */}
                  <div className={`inline-flex px-4 py-2 rounded-xl border-2 font-black text-sm tracking-wide mb-6 ${st.b} ${st.c}`}>
                    {st.l}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-4 mb-8">
                    <div className="flex-1 card-glass p-5 border-blue-100 bg-white">
                      <Droplets className="w-6 h-6 text-water-blue mb-2" />
                      <p className="text-gray-400 text-xs font-bold uppercase">Volume</p>
                      <p className="text-3xl font-black text-gray-800">{rec.waterAmount} L</p>
                    </div>
                    <div className="flex-1 card-glass p-5 border-amber-100 bg-white">
                      <Clock className="w-6 h-6 text-amber-500 mb-2" />
                      <p className="text-gray-400 text-xs font-bold uppercase">Time</p>
                      <p className="text-3xl font-black text-gray-800">{rec.recommendedTime || '—'}</p>
                    </div>
                  </div>

                  {/* Reasoning list */}
                  <div>
                    <h4 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                      <Zap className="w-4 h-4 text-primary-green" /> Reasoning
                    </h4>
                    <ul className="space-y-4">
                      {rec.reasons.map((r, i) => (
                        <li key={i} className="flex gap-3 text-sm font-medium text-gray-600 anim-slide-left" style={{ animationDelay: `${i*100}ms` }}>
                          <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0" />
                          <span>{r}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
