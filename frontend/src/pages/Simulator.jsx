import React, { useState } from 'react';
import { Droplet, Thermometer, CloudRain, Zap, RefreshCw, CheckCircle2, Sliders } from 'lucide-react';
import { predictIrrigation } from '../services/api';

const SCENARIOS = [
  { l: 'Dry Tomato',  i: '🍅', c: 'Tomato', s: 'Flowering', a: 2.5, m: 25, t: 34, r: 10, h: 45 },
  { l: 'Rain Coming', i: '🌧️', c: 'Tomato', s: 'Flowering', a: 2.5, m: 28, t: 24, r: 85, h: 75 },
  { l: 'Moist Rice',  i: '🌾', c: 'Rice',   s: 'Vegetative',a: 5.0, m: 70, t: 28, r: 20, h: 80 },
  { l: 'Wheat Warn',  i: '🌱', c: 'Wheat',  s: 'Heading',   a: 10,  m: 48, t: 25, r: 45, h: 60 },
];

const S = {
  IRRIGATE:      { l:'IRRIGATE',      badge:'badge-red',    bg:'bg-red-50',    icon:'🔴' },
  WAIT_FOR_RAIN: { l:'WAIT FOR RAIN', badge:'badge-blue',   bg:'bg-blue-50',   icon:'🔵' },
  NO_IRRIGATION: { l:'NO IRRIGATION', badge:'badge-green',  bg:'bg-green-50',  icon:'🟢' },
  MONITOR:       { l:'MONITOR',       badge:'badge-yellow', bg:'bg-amber-50',  icon:'🟡' },
};

const CustomSlider = ({ label, icon, val, min, max, unit, setVal, colorClass }) => (
  <div className="mb-8">
    <div className="flex justify-between items-end mb-3">
      <label className="text-sm font-bold text-gray-600 flex items-center gap-2">
        <span className="text-lg">{icon}</span> {label}
      </label>
      <span className={`text-xl font-black ${colorClass}`}>{val}{unit}</span>
    </div>
    <div className="progress-track h-3 bg-gray-100 relative">
      <div className="progress-fill h-full absolute left-0 top-0 pointer-events-none" 
           style={{ width: `${((val-min)/(max-min))*100}%`, background: 'currentColor' }} 
           className={`absolute h-full rounded-full ${colorClass}`} />
      <input type="range" min={min} max={max} value={val} onChange={e => setVal(Number(e.target.value))}
             className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10 m-0" />
      <div className="absolute top-1/2 -translate-y-1/2 w-6 h-6 bg-white border-4 rounded-full shadow-md pointer-events-none transition-all duration-75"
           style={{ left: `calc(${((val-min)/(max-min))*100}% - 12px)`, borderColor: 'currentColor' }}
           className={`absolute top-1/2 -translate-y-1/2 w-6 h-6 bg-white border-4 rounded-full shadow-md pointer-events-none transition-all duration-75 ${colorClass}`} />
    </div>
  </div>
);

export default function Simulator() {
  const [c, setC] = useState('Tomato');
  const [s, setS] = useState('Flowering');
  const [a, setA] = useState(2.5);
  const [m, setM] = useState(27);
  const [t, setT] = useState(33);
  const [r, setR] = useState(15);
  const [h, setH] = useState(58);
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [act, setAct] = useState(null);

  const CROPS = ['Tomato', 'Rice', 'Wheat'];
  const STAGES = { Tomato:['Seedling','Vegetative','Flowering','Fruiting'], Rice:['Vegetative','Reproductive','Ripening'], Wheat:['Tillering','Stem Extension','Heading','Maturation'] };

  const analyze = () => {
    setLoading(true);
    predictIrrigation({ soilMoisture: m, temperature: t, humidity: h, rainProbability: r, crop: c, growthStage: s, fieldArea: a })
      .then(d => { setRes(null); setTimeout(() => setRes(d), 50); })
      .finally(() => setLoading(false));
  };

  const load = (scn, i) => { setC(scn.c); setS(scn.s); setA(scn.a); setM(scn.m); setT(scn.t); setR(scn.r); setH(scn.h); setRes(null); setAct(i); };

  const st = res ? (S[res.status] || S.MONITOR) : null;

  return (
    <div className="max-w-[1100px] mx-auto space-y-8 pb-10">
      
      {/* ── Header ── */}
      <div className="text-center anim-fade-up d0">
        <h1 className="text-4xl font-black text-gray-900 mb-2 flex justify-center items-center gap-3">
          <Sliders className="w-8 h-8 text-water-blue" /> Simulator
        </h1>
        <p className="text-gray-500 font-medium">Test the rule engine with what-if scenarios.</p>
      </div>

      {/* ── Scenario Pills ── */}
      <div className="flex flex-wrap justify-center gap-3 anim-fade-up d1">
        {SCENARIOS.map((scn, i) => (
          <button key={scn.l} onClick={() => load(scn, i)}
            className={`px-5 py-2.5 rounded-full text-sm font-bold border-2 transition-all
              ${act === i ? 'border-water-blue bg-blue-50 text-water-blue shadow-glow-b' : 'border-gray-200 bg-white text-gray-500 hover:border-gray-300'}`}>
            <span className="mr-2 text-lg">{scn.i}</span> {scn.l}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 anim-fade-up d2">
        
        {/* ── Inputs (Left) ── */}
        <div className="lg:col-span-3 card p-8">
          <div className="grid grid-cols-2 gap-4 mb-8">
            <div>
              <label className="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Crop</label>
              <select value={c} onChange={e => { setC(e.target.value); setS(STAGES[e.target.value][0]); setRes(null); }}
                className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 font-bold text-gray-800 outline-none focus:border-water-blue focus:ring-2 focus:ring-water-blue/20 transition-all">
                {CROPS.map(cr => <option key={cr}>{cr}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Stage</label>
              <select value={s} onChange={e => { setS(e.target.value); setRes(null); }}
                className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 font-bold text-gray-800 outline-none focus:border-water-blue focus:ring-2 focus:ring-water-blue/20 transition-all">
                {STAGES[c].map(stg => <option key={stg}>{stg}</option>)}
              </select>
            </div>
          </div>

          <CustomSlider label="Soil Moisture" icon="🌱" val={m} min={0} max={100} unit="%" setVal={v=>{setM(v);setRes(null);}} colorClass="text-water-blue" />
          <CustomSlider label="Temperature"   icon="🌡️" val={t} min={0} max={50}  unit="°C" setVal={v=>{setT(v);setRes(null);}} colorClass="text-amber-500" />
          <CustomSlider label="Rain Prob."    icon="🌧️" val={r} min={0} max={100} unit="%" setVal={v=>{setR(v);setRes(null);}} colorClass="text-sky-500" />
          
          <button onClick={analyze} disabled={loading}
            className="w-full mt-4 py-4 rounded-xl bg-gradient-to-r from-blue-600 to-sky-500 text-white font-black text-lg shadow-glow-b hover:-translate-y-1 hover:shadow-lg transition-all flex items-center justify-center gap-2">
            {loading ? <RefreshCw className="w-5 h-5 anim-spin-slow" /> : <Zap className="w-5 h-5" />}
            {loading ? 'ANALYZING...' : 'RUN SIMULATION'}
          </button>
        </div>

        {/* ── Output (Right) ── */}
        <div className="lg:col-span-2 card p-8 bg-gray-50 flex flex-col justify-center min-h-[400px]">
          {res ? (
            <div className="anim-scale-up">
              <div className="text-center mb-8">
                <span className="text-5xl mb-4 block">{st.icon}</span>
                <span className={`badge ${st.badge} text-lg px-6 py-2`}>{st.l}</span>
              </div>
              
              <div className="card-glass p-6 text-center border-gray-200 shadow-soft mb-6 bg-white">
                <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Water Required</p>
                <p className="text-5xl font-black text-gray-900">{res.waterAmount} <span className="text-2xl text-gray-400">L</span></p>
              </div>

              {res.reasons?.length > 0 && (
                <div>
                  <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">Reasoning</p>
                  <ul className="space-y-3">
                    {res.reasons.map((rsn, i) => (
                      <li key={i} className="flex gap-3 text-sm font-medium text-gray-600 anim-slide-left" style={{ animationDelay: `${i*100}ms` }}>
                        <CheckCircle2 className="w-5 h-5 text-water-blue flex-shrink-0" />
                        {rsn}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center text-gray-400">
              <Droplet className="w-16 h-16 mx-auto mb-4 opacity-20" />
              <p className="font-bold text-lg text-gray-500">Awaiting Input</p>
              <p className="text-sm mt-2">Adjust sliders and run simulation.</p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
