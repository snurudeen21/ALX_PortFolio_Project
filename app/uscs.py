def uscs(PI, liquid_limit, C_of_C, C_of_U, _5mm, _75micro_m, graph_check):
  
    #USCS Classification list
    USCS = [
            ("GW: Well-graded gravels and gravel-sand mixtures, little or no fines", 
            "GP: Poorly-graded gravels and gravel-sand mixtures, little or no fines", 
            "GM: Silty gravels, gravel-sand-silt mixtures", "GC: Clayey gravels, gravel-sand-clay mixtures",
            "GM - GC: Silty gravel with clay", "GW - GM: Well graded gravel with silt"
            ),
            ("SW: Well-graded sands and gravelly sands, little or no fines", 
            "SP: Poorly-graded sands and gravelly sands, little or no fines", 
            "SM: Silty sands", "SC: Clayey sands", 
            "SM - SC: Silty sand with clay",
            "SP - SC: Poorly graded sand with clay"),
            ("CL: Inorganic Clays of low to medium Plasticity",
            "ML: Inorganic Silts, very fine sand, Rock Flour of medium to low plasticity or\n OL: Organic Silt and Organic Silt Clay of low Plasticity",
            "CL - ML: Silty Clay with Sand"),
            ("CH: Inorganic Clay of high Plasticty", 
            "MH: Inorganic Silt, Micaceous, Diatomaceous fine sand or silt of high Plasticity or\n OH: Organic Clay of medium to high Plasticity")
    ]


    # Conditional Statements to Classify USCS
    if _75micro_m < 50:
        if _5mm < 50:
            if _75micro_m < 5:
                if C_of_U > 4 and C_of_C >= 1 and C_of_C <= 3:
                    USCS_soil_classification = USCS[0][0]
                else:
                    USCS_soil_classification = USCS[0][1]
                    
            elif _75micro_m > 12:
                if graph_check < 0.73 or PI < 4:
                    USCS_soil_classification = USCS[0][2]
                elif graph_check > 0.73 and PI > 7:
                    USCS_soil_classification = USCS[0][3]
                else:
                    USCS_soil_classification = USCS[0][2],"-",USCS[0][3]
                
            elif _75micro_m >= 5 and _75micro_m <= 12:
                USCS_soil_classification = USCS[0][0],"-",USCS[0][2]

        else:
            if _75micro_m < 5:
                if C_of_U > 6 and C_of_C >= 1 and C_of_C <= 3:
                    USCS_soil_classification = USCS[1][0]
                else:
                    USCS_soil_classification = USCS[1][1]

            elif _75micro_m > 12:
                if graph_check < 0.73 or PI < 4:
                    USCS_soil_classification = USCS[1][2]
                elif graph_check > 0.73 and PI > 7:
                    USCS_soil_classification = USCS[1][3]
                else:
                    USCS_soil_classification = USCS[1][2],"-",USCS[1][3]
            elif _75micro_m >= 5 and _75micro_m <= 12:
                USCS_soil_classification = USCS[1][1],"-",USCS[1][3]

    else:
        if liquid_limit <= 50:
            if graph_check > 0.73:
                USCS_soil_classification = USCS[2][0]
            else:
                USCS_soil_classification = USCS[2][1]
        elif liquid_limit > 50:
            if graph_check > 0.73:
                USCS_soil_classification = USCS[3][0]
            else:
                USCS_soil_classification = USCS[3][1]

    #Store USCS classification for Soil Report in soil_list
    return USCS_soil_classification