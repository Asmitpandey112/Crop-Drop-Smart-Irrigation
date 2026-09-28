from app.services.crop_profiles import CROP_PROFILES

def evaluate_irrigation(crop: str, growth_stage: str, soil_moisture: float, rain_probability: float, area: float):
    # Default to Tomato if unknown
    profile = CROP_PROFILES.get(crop, CROP_PROFILES["Tomato"])
    
    min_moisture = profile["moisture"]["min"]
    optimal_moisture = profile["moisture"]["optimal"]
    stage_factor = profile["growth_stages"].get(growth_stage, 1.0)
    
    RAIN_THRESHOLD_HIGH = 60.0
    RAIN_THRESHOLD_LOW = 30.0
    
    status = "MONITOR"
    water = 0.0
    reasons = []

    # Ensure valid defaults if sensor data is missing
    if soil_moisture is None:
        return {"status": "MONITOR", "water_amount": 0.0, "reasons": ["Awaiting sensor data"]}
    if rain_probability is None:
        rain_probability = 0.0

    if soil_moisture < min_moisture:
        if rain_probability >= RAIN_THRESHOLD_HIGH:
            status = "WAIT_FOR_RAIN"
            reasons.append(f"Soil moisture ({soil_moisture}%) is critically low, but high rain probability ({rain_probability}%) means we should wait.")
        else:
            status = "IRRIGATE"
            water = profile["water_requirement_base"] * stage_factor * area
            reasons.append(f"Soil moisture ({soil_moisture}%) is below {crop} minimum target ({min_moisture}%).")
            if rain_probability < RAIN_THRESHOLD_LOW:
                reasons.append(f"Rain probability is currently low ({rain_probability}%).")
            reasons.append(f"Crop is in {growth_stage} stage, requiring calculated dose.")
            
    elif soil_moisture < optimal_moisture:
        if rain_probability >= RAIN_THRESHOLD_HIGH:
            status = "WAIT_FOR_RAIN"
            reasons.append(f"Moisture is sub-optimal, but heavy rain is expected ({rain_probability}%).")
        elif rain_probability >= RAIN_THRESHOLD_LOW:
            status = "MONITOR"
            reasons.append(f"Moderate rain expected ({rain_probability}%), monitoring conditions closely.")
        else:
            status = "IRRIGATE"
            water = (profile["water_requirement_base"] * stage_factor * area) * 0.5 # half dose for sub-optimal
            reasons.append(f"Soil moisture is sub-optimal ({soil_moisture}%) and no rain is expected.")
            
    else:
        status = "NO_IRRIGATION"
        reasons.append(f"Soil moisture ({soil_moisture}%) is optimal or above optimal for {crop}.")

    return {
        "status": status,
        "water_amount": round(water, 1),
        "reasons": reasons
    }
