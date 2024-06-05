def aashto(_2mm, _425micro_m, _75micro_m, liquid_limit, plastic_limit, PI):

        #AASHTO Classification list 
        AASHTO = [
                ("A-1-a: Stone Fragments (Gravel and Sand). Rating: Excellent to Good", "A-1-b: Stone Fragments (Gravel and Sand). Rating: Excellent to Good"),
                "A-3: Fine Sand. Rating: Excellent to Good",
                ("A-2-4: Silty or Clayey Gravel Sand. Rating: Good", 
                "A-2-5: Silty or Clayey Gravel Sand. Rating: Good", 
                "A-2-6: Silty or Clayey Gravel Sand. Rating: Good", 
                "A-2-7: Silty or Clayey Gravel Sand. Rating: Good"),
                "A-4: Silty Soil. Rating: Fair", "A-5: Silty Soil. Rating: Fair",
                "A-6: Silty Soil. Rating: Fair",
                ("A-7-5: Clayey Soil. Rating: Poor", "A-7-6: Clayey Soil. Rating: Poor")
        ]


        # Conditional Statements to Classify AASHTO
        if _2mm <= 50 and _425micro_m <= 30 and _75micro_m <= 15 and PI <= 6:
            AASHTO_soil_classification = AASHTO[0][0]
        elif _425micro_m <= 50 and _75micro_m <= 25 and PI <= 6:
            AASHTO_soil_classification = AASHTO[0][1]
        elif _75micro_m <= 10 and PI == 0:
            AASHTO_soil_classification = AASHTO[1]
        elif _75micro_m <= 35 and liquid_limit <= 40 and PI <= 10:
            AASHTO_soil_classification = AASHTO[2][0]
        elif _75micro_m <= 35 and liquid_limit >= 41 and PI <= 10:
            AASHTO_soil_classification = AASHTO[2][1]
        elif _75micro_m <= 35 and liquid_limit <= 40 and PI >= 11:
            AASHTO_soil_classification = AASHTO[2][2]
        elif _75micro_m <= 35 and liquid_limit >= 41 and PI >= 11:
            AASHTO_soil_classification = AASHTO[2][3]
        elif liquid_limit <= 40 and PI <= 10:
            AASHTO_soil_classification = AASHTO[3]
        elif liquid_limit >= 41 and PI <= 10:
            AASHTO_soil_classification = AASHTO[4]
        elif liquid_limit <= 40 and PI >= 11:
            AASHTO_soil_classification = AASHTO[5]
        elif liquid_limit >= 41 and PI >= 11 and plastic_limit > 30:
            AASHTO_soil_classification = AASHTO[6][0]
        elif liquid_limit >= 41 and PI >= 11 and plastic_limit < 30:
            AASHTO_soil_classification = AASHTO[6][1]
        else: pass

        #Store AASHTO Classification for Soil Report in soil_list
        return AASHTO_soil_classification