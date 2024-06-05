import MySQLdb

def my_server(a_5mm, b_2mm, c_425micro_m, d_75micro_m, finess_mod, C_of_C, C_of_U, liquid_limit_1, plastic_limit_1, PI, graph_check):
    db = MySQLdb.connect(host="54.237.73.218", user="nuru1", port=3306,
                                passwd="", db="soil_data_demo")
    cur = db.cursor()


    cur.execute("""
        CREATE TABLE IF NOT EXISTS soil_param_demo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            passing_sieve_5mm FLOAT,
            passing_sieve_2mm FLOAT,
            passing_sieve_425micro_m FLOAT,
            passing_sieve_75micro_m FLOAT,
            finess_modulus FLOAT,
            Coeff_of_Curvature FLOAT,
            Coeff_of_Uniformity FLOAT,
            liquid_limit_1 FLOAT,
            plastic_limit_1 FLOAT,
            PI FLOAT,
            graph_check FLOAT
        )
        """)

    cur.execute(
            'INSERT INTO soil_param_demo ('
        'passing_sieve_5mm, passing_sieve_2mm, passing_sieve_425micro_m, '
        'passing_sieve_75micro_m, finess_modulus, Coeff_of_Curvature, '
        'Coeff_of_Uniformity, liquid_limit_1, plastic_limit_1, PI, graph_check'
            ') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (
                a_5mm, b_2mm, c_425micro_m, d_75micro_m, finess_mod, C_of_C,
                C_of_U, liquid_limit_1, plastic_limit_1, PI, graph_check
            )
            )

    db.commit()

    db.close()

    return