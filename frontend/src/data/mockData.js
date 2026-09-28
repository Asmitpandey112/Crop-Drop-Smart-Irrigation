export const mockFields = [
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
