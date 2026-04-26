def get_treatment_recommendation(disease):

    # Normalize model outputs
    disease_map = {
        "BlackPoint": "Black Point",
        "FusariumFootRot": "Fusarium Foot Rot",
        "LeafBlight": "Leaf Blight",
        "WheatBlast": "Wheat Blast",
        "Healthy": "Healthy Leaf",
        "HealthyLeaf": "Healthy Leaf"
    }

    disease = disease_map.get(disease, disease)

    treatments = {

        "Black Point": """
🚨 SPRAY TILT 1ml/10L water NOW
🔥 Remove black grains after harvest
🌾 Use clean seeds next time
⚠️ STOP excessive urea NOW
🕒 Spray before boot leaf stage""",

        "Fusarium Foot Rot": """
🚨 SPRAY CARBENDAZIM on base TODAY
✂️ Cut & burn dead plants
⏳ No wheat here for 2 years
💧 Improve field drainage
🌡️ Sow on time (not early)""",

        "Leaf Blight": """
🚨 2 NATIVO SPRAYS (10 days apart)
🔥 Burn spotted leaves immediately
💪 Add potash fertilizer now
☀️ Avoid evening irrigation
🌱 Use resistant varieties""",

        "Wheat Blast": """
🚨 TILT SPRAY on ears RIGHT NOW
🔥 Burn ALL white heads
🔄 Repeat spray after 7 days
🚫 Don't plant near blast areas
🌽 Plant maize border crops""",

        "Healthy Leaf": """
✅ NO SPRAY NEEDED
👀 Check fields daily for spots
🧹 Keep field weed-free
👍 Good farming!"""
    }

    return treatments.get(
        disease,
        "⚠️ No treatment recommendation available."
    )
