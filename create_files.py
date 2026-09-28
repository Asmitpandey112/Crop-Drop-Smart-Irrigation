import os
import json

base_dir = r"C:\Users\ASMIT PANDEY\.gemini\antigravity\scratch\cropdrop\frontend"

files = {
    "src/index.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --primary-green: #2E7D32;
  --dark-green: #123524;
  --light-green: #E8F5E9;
  --water-blue: #0288D1;
  --sky-blue: #2196F3;
  --warning: #F59E0B;
  --danger: #DC2626;
  --background: #F6F8F5;
}

body {
  background-color: var(--background);
  color: #333;
}
""",
    "tailwind.config.js": """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-green': '#2E7D32',
        'dark-green': '#123524',
        'light-green': '#E8F5E9',
        'water-blue': '#0288D1',
        'sky-blue': '#2196F3',
        'warning': '#F59E0B',
        'danger': '#DC2626',
        'background-color': '#F6F8F5',
      }
    },
  },
  plugins: [],
}
""",
    "src/data/mockData.js": """export const mockFields = [
  {
    id: '1',
    name: 'North Field',
    crop: 'Tomato',
    growthStage: 'Flowering',
    area: 2.5,
    soilMoisture: 27,
    temperature: 33,
    humidity: 58,
    rainProbability: 15,
    status: 'IRRIGATE',
    recommendedWater: 420,
    recommendedTime: '6:00 PM',
  },
  {
    id: '2',
    name: 'East Field',
    crop: 'Rice',
    growthStage: 'Vegetative',
    area: 5.0,
    soilMoisture: 70,
    temperature: 28,
    humidity: 80,
    rainProbability: 40,
    status: 'GOOD',
    recommendedWater: 0,
    recommendedTime: null,
  },
  {
    id: '3',
    name: 'South Field',
    crop: 'Wheat',
    growthStage: 'Maturation',
    area: 10.0,
    soilMoisture: 45,
    temperature: 25,
    humidity: 60,
    rainProbability: 85,
    status: 'WAIT_FOR_RAIN',
    recommendedWater: 0,
    recommendedTime: null,
  }
];

export const mockMoistureHistory = [
  { time: '09:00', moisture: 42 },
  { time: '11:00', moisture: 39 },
  { time: '13:00', moisture: 35 },
  { time: '15:00', moisture: 30 },
  { time: '17:00', moisture: 27 },
];

export const mockWaterUsage = [
  { day: 'Mon', usage: 300, avoided: 120 },
  { day: 'Tue', usage: 0, avoided: 450 },
  { day: 'Wed', usage: 250, avoided: 50 },
  { day: 'Thu', usage: 400, avoided: 0 },
  { day: 'Fri', usage: 0, avoided: 380 },
  { day: 'Sat', usage: 350, avoided: 100 },
  { day: 'Sun', usage: 0, avoided: 420 },
];
""",
    "src/components/Sidebar.jsx": """import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Map, Cpu, Droplets, BarChart2, Sprout } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { name: 'Dashboard', path: '/', icon: Home },
    { name: 'My Fields', path: '/fields', icon: Map },
    { name: 'AI Advisor', path: '/advisor', icon: Cpu },
    { name: 'Simulator', path: '/simulator', icon: Droplets },
    { name: 'Analytics', path: '/analytics', icon: BarChart2 },
  ];

  return (
    <div className="w-64 bg-dark-green text-white h-screen fixed left-0 top-0 flex flex-col shadow-xl">
      <div className="p-6 flex items-center space-x-3 border-b border-gray-700">
        <Sprout className="w-8 h-8 text-light-green" />
        <span className="text-2xl font-bold tracking-wider">CropDrop<span className="text-xl">🌾</span></span>
      </div>
      <nav className="flex-1 px-4 py-6 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors duration-200 ${
                  isActive ? 'bg-primary-green text-white shadow-md' : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`
              }
            >
              <Icon className="w-5 h-5" />
              <span className="font-medium">{item.name}</span>
            </NavLink>
          );
        })}
      </nav>
      <div className="p-4 border-t border-gray-700 text-sm text-gray-400 text-center">
        Prototype Mode
      </div>
    </div>
  );
};

export default Sidebar;
""",
    "src/layouts/AppLayout.jsx": """import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';

const AppLayout = () => {
  return (
    <div className="flex min-h-screen bg-background-color font-sans">
      <Sidebar />
      <div className="flex-1 ml-64 p-8 overflow-y-auto h-screen">
        <Outlet />
      </div>
    </div>
  );
};

export default AppLayout;
""",
    "src/pages/Dashboard.jsx": """import React from 'react';
import { mockFields } from '../data/mockData';
import { AlertCircle, Droplet, Sprout, Map, Activity } from 'lucide-react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const fieldsRequiringAttention = mockFields.filter(f => f.status === 'IRRIGATE').length;
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Overview</h1>
          <p className="text-gray-500 mt-1">Simulated agricultural dashboard</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="p-3 bg-light-green rounded-xl text-primary-green">
            <Map className="w-8 h-8" />
          </div>
          <div>
            <p className="text-sm text-gray-500 font-medium">Total Fields</p>
            <p className="text-2xl font-bold text-gray-800">{mockFields.length}</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="p-3 bg-red-50 rounded-xl text-danger">
            <AlertCircle className="w-8 h-8" />
          </div>
          <div>
            <p className="text-sm text-gray-500 font-medium">Needs Attention</p>
            <p className="text-2xl font-bold text-gray-800">{fieldsRequiringAttention}</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="p-3 bg-blue-50 rounded-xl text-water-blue">
            <Droplet className="w-8 h-8" />
          </div>
          <div>
            <p className="text-sm text-gray-500 font-medium">Today's Usage</p>
            <p className="text-2xl font-bold text-gray-800">350 L</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="p-3 bg-green-50 rounded-xl text-primary-green">
            <Sprout className="w-8 h-8" />
          </div>
          <div>
            <p className="text-sm text-gray-500 font-medium">Water Avoided</p>
            <p className="text-2xl font-bold text-gray-800">420 L</p>
          </div>
        </div>
      </div>

      <h2 className="text-xl font-bold text-gray-800 mt-10 mb-4">Current Recommendations</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {mockFields.filter(f => f.status === 'IRRIGATE').map(field => (
          <div key={field.id} className="bg-white rounded-2xl p-6 shadow-sm border border-red-100 flex flex-col md:flex-row md:items-center justify-between">
            <div className="flex items-start space-x-4">
              <div className="w-3 h-3 mt-2 rounded-full bg-danger"></div>
              <div>
                <h3 className="text-lg font-bold text-gray-800">{field.name} <span className="text-sm font-normal text-gray-500 ml-2">{field.crop} • {field.area} ac</span></h3>
                <p className="text-danger font-semibold mt-1">Irrigation Recommended</p>
                <div className="flex items-center space-x-4 mt-3 text-sm text-gray-600">
                  <span className="flex items-center"><Activity className="w-4 h-4 mr-1 text-gray-400" /> Moisture: {field.soilMoisture}%</span>
                  <span className="flex items-center"><Droplet className="w-4 h-4 mr-1 text-water-blue" /> Suggest: {field.recommendedWater} L</span>
                </div>
              </div>
            </div>
            <Link to={`/fields/${field.id}`} className="mt-4 md:mt-0 px-4 py-2 bg-danger text-white rounded-lg hover:bg-red-700 transition font-medium text-sm text-center">
              View Details
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
""",
    "src/pages/FieldsList.jsx": """import React from 'react';
import { mockFields } from '../data/mockData';
import { Link } from 'react-router-dom';
import { Droplet, AlertTriangle, CheckCircle, CloudRain, MapPin } from 'lucide-react';

const FieldsList = () => {
  const getStatusDisplay = (status) => {
    switch (status) {
      case 'IRRIGATE': return { color: 'bg-red-50 border-red-200 text-danger', icon: AlertTriangle, text: 'Irrigation Recommended', dot: 'bg-danger' };
      case 'WAIT_FOR_RAIN': return { color: 'bg-blue-50 border-blue-200 text-sky-blue', icon: CloudRain, text: 'Rain Expected', dot: 'bg-sky-blue' };
      case 'GOOD': return { color: 'bg-green-50 border-green-200 text-primary-green', icon: CheckCircle, text: 'Good', dot: 'bg-primary-green' };
      default: return { color: 'bg-yellow-50 border-yellow-200 text-warning', icon: AlertTriangle, text: 'Monitor', dot: 'bg-warning' };
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">My Fields</h1>
          <p className="text-gray-500 mt-1">Manage and monitor all your plots</p>
        </div>
        <button className="px-5 py-2.5 bg-primary-green text-white rounded-xl hover:bg-green-700 font-medium transition shadow-sm">
          + Add Field
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockFields.map((field) => {
          const status = getStatusDisplay(field.status);
          const Icon = status.icon;
          
          return (
            <Link to={`/fields/${field.id}`} key={field.id} className={`block bg-white rounded-2xl overflow-hidden border border-gray-100 hover:shadow-lg transition-all duration-300 group`}>
              <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h2 className="text-xl font-bold text-gray-800 group-hover:text-primary-green transition-colors flex items-center"><MapPin className="w-5 h-5 mr-1 text-gray-400" />{field.name}</h2>
                    <p className="text-gray-500 text-sm mt-1">{field.crop} {field.crop === 'Tomato' ? '🍅' : field.crop === 'Rice' ? '🌾' : '🌱'} • {field.area} acres</p>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-xs font-bold flex items-center border ${status.color}`}>
                     <span className={`w-2 h-2 rounded-full mr-1.5 ${status.dot}`}></span>
                     {status.text}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 mt-6 p-4 bg-gray-50 rounded-xl">
                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Moisture</p>
                    <p className="text-lg font-bold text-gray-800 flex items-center mt-1"><Droplet className="w-4 h-4 mr-1 text-water-blue" /> {field.soilMoisture}%</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wider font-semibold">Rain Prob.</p>
                    <p className="text-lg font-bold text-gray-800 flex items-center mt-1"><CloudRain className="w-4 h-4 mr-1 text-sky-blue" /> {field.rainProbability}%</p>
                  </div>
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export default FieldsList;
""",
    "src/pages/FieldDetails.jsx": """import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { mockFields, mockMoistureHistory } from '../data/mockData';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Droplet, Thermometer, CloudRain, Activity, ArrowLeft } from 'lucide-react';

const FieldDetails = () => {
  const { id } = useParams();
  const field = mockFields.find(f => f.id === id) || mockFields[0];

  return (
    <div className="space-y-6">
      <Link to="/fields" className="flex items-center text-primary-green hover:text-green-800 font-medium text-sm transition">
        <ArrowLeft className="w-4 h-4 mr-1" /> Back to Fields
      </Link>
      
      <div className="flex flex-col md:flex-row md:justify-between md:items-end">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">{field.name}</h1>
          <p className="text-gray-500 mt-2 flex items-center space-x-2">
            <span className="px-3 py-1 bg-gray-100 rounded-full text-sm">{field.crop}</span>
            <span className="px-3 py-1 bg-gray-100 rounded-full text-sm">{field.growthStage}</span>
            <span className="px-3 py-1 bg-gray-100 rounded-full text-sm">{field.area} acres</span>
          </p>
        </div>
        {field.status === 'IRRIGATE' && (
          <div className="mt-4 md:mt-0 p-4 bg-red-50 border border-red-100 rounded-xl text-danger">
            <p className="font-bold">Recommendation</p>
            <p className="text-lg">Irrigate {field.recommendedWater} L at {field.recommendedTime}</p>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex flex-col justify-between">
          <div className="text-gray-500 text-sm font-medium flex items-center"><Droplet className="w-4 h-4 mr-1.5 text-water-blue"/> Soil Moisture</div>
          <div className="text-3xl font-bold text-gray-800 mt-2">{field.soilMoisture}%</div>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex flex-col justify-between">
          <div className="text-gray-500 text-sm font-medium flex items-center"><Thermometer className="w-4 h-4 mr-1.5 text-warning"/> Temperature</div>
          <div className="text-3xl font-bold text-gray-800 mt-2">{field.temperature}°C</div>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex flex-col justify-between">
          <div className="text-gray-500 text-sm font-medium flex items-center"><Activity className="w-4 h-4 mr-1.5 text-primary-green"/> Humidity</div>
          <div className="text-3xl font-bold text-gray-800 mt-2">{field.humidity}%</div>
        </div>
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex flex-col justify-between">
          <div className="text-gray-500 text-sm font-medium flex items-center"><CloudRain className="w-4 h-4 mr-1.5 text-sky-blue"/> Rain Prob.</div>
          <div className="text-3xl font-bold text-gray-800 mt-2">{field.rainProbability}%</div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mt-6">
        <h2 className="text-xl font-bold text-gray-800 mb-6">Soil Moisture History (Today)</h2>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={mockMoistureHistory}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
              <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fill: '#6B7280'}} dy={10} />
              <YAxis domain={[0, 100]} axisLine={false} tickLine={false} tick={{fill: '#6B7280'}} dx={-10} />
              <Tooltip 
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
              />
              <Line type="monotone" dataKey="moisture" stroke="#0288D1" strokeWidth={3} dot={{r: 4, fill: '#0288D1', strokeWidth: 2, stroke: '#fff'}} activeDot={{r: 6}} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default FieldDetails;
""",
    "src/pages/AIAdvisor.jsx": """import React from 'react';
import { CheckCircle2, Cpu, Droplet, Clock } from 'lucide-react';

const AIAdvisor = () => {
  return (
    <div className="max-w-4xl mx-auto py-8">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-gray-800 flex justify-center items-center">
          <Cpu className="w-10 h-10 mr-3 text-primary-green" /> CropDrop AI Advisor
        </h1>
        <p className="text-gray-500 mt-3 text-lg">Smart irrigation recommendations based on environmental data</p>
      </div>

      <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100">
        <div className="p-8 border-b border-gray-100 bg-gray-50">
          <div className="flex justify-between items-end">
            <div>
              <h2 className="text-2xl font-bold text-gray-800">North Field</h2>
              <p className="text-gray-500 mt-1">Tomato • Flowering • 2.5 acres</p>
            </div>
            <div className="text-right">
              <span className="inline-block px-4 py-2 bg-red-100 text-danger font-bold rounded-lg tracking-wide">
                🔴 IRRIGATION RECOMMENDED
              </span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-gray-100">
          <div className="p-8">
            <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-6">Current Conditions</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center pb-3 border-b border-gray-50">
                <span className="text-gray-600 font-medium">🌱 Soil Moisture</span>
                <span className="font-bold text-gray-800">27%</span>
              </div>
              <div className="flex justify-between items-center pb-3 border-b border-gray-50">
                <span className="text-gray-600 font-medium">🌡️ Temperature</span>
                <span className="font-bold text-gray-800">33°C</span>
              </div>
              <div className="flex justify-between items-center pb-3 border-b border-gray-50">
                <span className="text-gray-600 font-medium">💧 Humidity</span>
                <span className="font-bold text-gray-800">58%</span>
              </div>
              <div className="flex justify-between items-center pb-3 border-b border-gray-50">
                <span className="text-gray-600 font-medium">🌧️ Rain Probability</span>
                <span className="font-bold text-gray-800">15%</span>
              </div>
            </div>
          </div>

          <div className="p-8 bg-white">
            <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-6">Action Plan</h3>
            
            <div className="flex space-x-6 mb-8">
              <div className="flex-1 bg-blue-50 p-4 rounded-2xl flex flex-col items-center justify-center border border-blue-100">
                <Droplet className="w-8 h-8 text-water-blue mb-2" />
                <span className="text-sm text-gray-500 font-medium">Amount</span>
                <span className="text-2xl font-bold text-water-blue">420 L</span>
              </div>
              <div className="flex-1 bg-yellow-50 p-4 rounded-2xl flex flex-col items-center justify-center border border-yellow-100">
                <Clock className="w-8 h-8 text-warning mb-2" />
                <span className="text-sm text-gray-500 font-medium">Time</span>
                <span className="text-2xl font-bold text-warning">6:00 PM</span>
              </div>
            </div>

            <div>
              <h4 className="font-bold text-gray-800 mb-4">Why?</h4>
              <ul className="space-y-3">
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 text-primary-green mr-2 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700">Soil moisture (27%) is below the target (35%) for Tomato.</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 text-primary-green mr-2 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700">Rain probability is extremely low (15%).</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 text-primary-green mr-2 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700">High temperature (33°C) increases evapotranspiration.</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle2 className="w-5 h-5 text-primary-green mr-2 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700">Crop is in flowering stage, requiring consistent moisture.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAdvisor;
""",
    "src/pages/Simulator.jsx": """import React, { useState } from 'react';
import { Droplet, Thermometer, CloudRain, Settings2 } from 'lucide-react';

const Simulator = () => {
  const [moisture, setMoisture] = useState(27);
  const [temp, setTemp] = useState(33);
  const [rain, setRain] = useState(15);
  const [result, setResult] = useState(null);

  const analyzeField = () => {
    // Simple mock logic matching backend Phase 5 concept
    if (moisture < 35 && rain < 40) {
      setResult({ status: 'IRRIGATE', water: 420, color: 'text-danger', bg: 'bg-red-50' });
    } else if (rain >= 70) {
      setResult({ status: 'WAIT FOR RAIN', water: 0, color: 'text-sky-blue', bg: 'bg-blue-50' });
    } else if (moisture >= 60) {
      setResult({ status: 'NO IRRIGATION', water: 0, color: 'text-primary-green', bg: 'bg-green-50' });
    } else {
      setResult({ status: 'MONITOR', water: 0, color: 'text-warning', bg: 'bg-yellow-50' });
    }
  };

  const loadScenario = (type) => {
    if (type === 'dry') { setMoisture(25); setRain(10); setTemp(34); }
    if (type === 'rain') { setMoisture(25); setRain(85); setTemp(24); }
    if (type === 'moist') { setMoisture(70); setRain(20); setTemp(28); }
    setResult(null);
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Irrigation Simulator</h1>
        <p className="text-gray-500 mt-1">What-if scenarios and logic prototype</p>
      </div>

      <div className="flex flex-wrap gap-3 mb-8">
        <button onClick={() => loadScenario('dry')} className="px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium hover:bg-gray-50">Dry Field Scenario</button>
        <button onClick={() => loadScenario('rain')} className="px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium hover:bg-gray-50">Rain Coming Scenario</button>
        <button onClick={() => loadScenario('moist')} className="px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium hover:bg-gray-50">Moist Field Scenario</button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center"><Settings2 className="mr-2" /> Parameters</h2>
          
          <div className="space-y-8">
            <div>
              <div className="flex justify-between mb-2">
                <label className="font-medium text-gray-700 flex items-center"><Droplet className="w-4 h-4 mr-2 text-water-blue"/> Soil Moisture</label>
                <span className="font-bold">{moisture}%</span>
              </div>
              <input type="range" min="0" max="100" value={moisture} onChange={(e) => setMoisture(e.target.value)} className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-green" />
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <label className="font-medium text-gray-700 flex items-center"><Thermometer className="w-4 h-4 mr-2 text-warning"/> Temperature</label>
                <span className="font-bold">{temp}°C</span>
              </div>
              <input type="range" min="0" max="50" value={temp} onChange={(e) => setTemp(e.target.value)} className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-warning" />
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <label className="font-medium text-gray-700 flex items-center"><CloudRain className="w-4 h-4 mr-2 text-sky-blue"/> Rain Probability</label>
                <span className="font-bold">{rain}%</span>
              </div>
              <input type="range" min="0" max="100" value={rain} onChange={(e) => setRain(e.target.value)} className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-sky-blue" />
            </div>
            
            <button onClick={analyzeField} className="w-full py-4 bg-primary-green text-white font-bold rounded-xl hover:bg-green-700 transition shadow-md">
              ANALYZE FIELD
            </button>
          </div>
        </div>

        <div className="bg-gray-50 p-8 rounded-2xl border border-gray-200 flex flex-col justify-center items-center min-h-[400px]">
          {result ? (
            <div className="text-center w-full animate-in fade-in zoom-in duration-300">
              <div className={`inline-block px-6 py-3 rounded-xl font-bold text-xl mb-6 border ${result.bg} ${result.color} border-current/20`}>
                {result.status}
              </div>
              
              <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 w-full">
                <p className="text-gray-500 text-sm font-bold uppercase tracking-wider mb-2">Recommended Water</p>
                <p className="text-5xl font-extrabold text-gray-800">{result.water} L</p>
                
                {result.water === 0 && result.status !== 'NO IRRIGATION' && (
                  <div className="mt-6 p-4 bg-green-50 text-primary-green rounded-lg text-sm font-medium">
                    Potential water avoided: 420 L
                    <p className="text-xs mt-1 text-gray-500 font-normal">This is a simulated estimate.</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-400">
              <Cpu className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p className="font-medium">Adjust parameters and click Analyze</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Simulator;
""",
    "src/pages/Analytics.jsx": """import React from 'react';
import { mockWaterUsage } from '../data/mockData';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Analytics = () => {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-800">Analytics</h1>
        <p className="text-gray-500 mt-1">Water usage and savings</p>
      </div>

      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
        <h2 className="text-xl font-bold text-gray-800 mb-6">Weekly Water Impact (Simulated)</h2>
        <div className="h-96 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={mockWaterUsage}
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
              <XAxis dataKey="day" axisLine={false} tickLine={false} />
              <YAxis axisLine={false} tickLine={false} />
              <Tooltip 
                cursor={{fill: '#F3F4F6'}}
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
              />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              <Bar dataKey="usage" name="Actual Usage (L)" fill="#0288D1" radius={[4, 4, 0, 0]} />
              <Bar dataKey="avoided" name="Avoided Usage (L)" fill="#2E7D32" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
""",
    "src/App.jsx": """import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import Dashboard from './pages/Dashboard';
import FieldsList from './pages/FieldsList';
import FieldDetails from './pages/FieldDetails';
import AIAdvisor from './pages/AIAdvisor';
import Simulator from './pages/Simulator';
import Analytics from './pages/Analytics';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="fields" element={<FieldsList />} />
          <Route path="fields/:id" element={<FieldDetails />} />
          <Route path="advisor" element={<AIAdvisor />} />
          <Route path="simulator" element={<Simulator />} />
          <Route path="analytics" element={<Analytics />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
"""
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
print("Files created successfully.")
