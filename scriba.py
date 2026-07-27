import psycopg2

print("Abriendo el portal a la Clara Oscuridad...")

try:
    # 1. El Scribe se conecta a la base de datos
    conexion = psycopg2.connect(
        dbname='db_clara_oscuridad', # Asegúrate de que este sea el nombre de tu base de datos
        user='postgres',              # Tu usuario de pgAdmin (casi siempre es 'postgres')
        password='tu_contraseña',     # <<<< CAMBIA ESTO POR TU CONTRASEÑA DE POSTGRES
        host='localhost',
        port='5432'
    )

    # 2. Creamos la "pluma" que escribirá y leerá
    scriba = conexion.cursor()

    # 3. El Scribe busca en la oscuridad la tinta del Arcano 0 (El Loco)
    # Le pedimos solo las columnas profundas que creamos
    scriba.execute("SELECT mecanismo_cosmico, sombra_klipa, tikkun_accion FROM arcanos WHERE numero = 0;")

    # 4. Recogemos el mensaje
    revelacion = scriba.fetchone()

    if revelacion:
        print("\n" + "="*50)
        print("REVELACIÓN DEL SISTEMA PARA HOY")
        print("="*50)
        print(f"\nMecanismo Cósmico: \n{revelacion[0]}")
        print(f"\nTu Sombra (Klipá) a vigilar: \n{revelacion[1]}")
        print(f"\nTu Tikkun (Acción de Alquimia): \n{revelacion[2]}")
        print("="*50 + "\n")
    else:
        print("El Scribe no encontró la tinta en la base de datos.")

    # 5. Cerramos el portal para no dejar fugas de energía
    scriba.close()
    conexion.close()

except Exception as error:
    print(f"Error en la conexión con el otro mundo: {error}")