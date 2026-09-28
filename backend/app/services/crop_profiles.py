# Configurable Crop Profiles for the Rule Engine

CROP_PROFILES = {
    "Tomato": {
        "moisture": {
            "min": 30.0,
            "optimal": 45.0,
            "max": 65.0
        },
        "water_requirement_base": 150.0, # base liters per acre
        "growth_stages": {
            "Seedling": 0.6,
            "Vegetative": 1.0,
            "Flowering": 1.5,
            "Fruiting": 1.3
        }
    },
    "Rice": {
        "moisture": {
            "min": 65.0,
            "optimal": 80.0,
            "max": 100.0
        },
        "water_requirement_base": 400.0,
        "growth_stages": {
            "Vegetative": 1.0,
            "Reproductive": 1.5,
            "Ripening": 0.7
        }
    },
    "Wheat": {
        "moisture": {
            "min": 35.0,
            "optimal": 55.0,
            "max": 75.0
        },
        "water_requirement_base": 120.0,
        "growth_stages": {
            "Tillering": 0.8,
            "Stem Extension": 1.2,
            "Heading": 1.5,
            "Maturation": 0.5
        }
    }
}
