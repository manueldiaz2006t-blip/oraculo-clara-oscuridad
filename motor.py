import os
from flask import Flask, render_template_string, request
import psycopg2

app = Flask(__name__)

# DICCIONARIO DE IMÁGENES (La tinta visual)
IMAGENES_ARCANOS = {
    0: "https://abrepuertasespiritual.cl/cartas/0.png",
    1: "https://abrepuertasespiritual.cl/cartas/1.png",
    2: "https://abrepuertasespiritual.cl/cartas/2.png",
    3: "https://abrepuertasespiritual.cl/cartas/3.png",
    4: "https://abrepuertasespiritual.cl/cartas/4.png",
    5: "https://abrepuertasespiritual.cl/cartas/5.png",
    6: "https://abrepuertasespiritual.cl/cartas/6.png",
    7: "https://abrepuertasespiritual.cl/cartas/7.png",
    8: "https://abrepuertasespiritual.cl/cartas/8.png",
    9: "https://abrepuertasespiritual.cl/cartas/9.png",
    10: "https://abrepuertasespiritual.cl/cartas/10.png"
}

PLANTILLA_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Clara Oscuridad</title>
    <style>
        body {
            background-color: #050510; 
            background-image: url('https://images.unsplash.com/photo-1507400492013-162706c8c05e?q=80&w=1920&auto=format&fit=crop'); 
            background-size: 100% 100%;
            background-position: center;
            color: #111111; 
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding-top: 10vh;
            text-align: center;
            transition: color 2s ease-in-out;
            animation: respirar-universo 40s ease-in-out infinite;
            overflow-x: hidden;
        }

        @keyframes respirar-universo {
            0% { background-size: 100% 100%; }
            50% { background-size: 130% 130%; }
            100% { background-size: 100% 100%; }
        }

        body::before {
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.05) 0%, transparent 70%);
            pointer-events: none;
            animation: shimmer 8s ease-in-out infinite;
            z-index: 0;
        }

        @keyframes shimmer {
            0% { opacity: 0.3; }
            50% { opacity: 1; }
            100% { opacity: 0.3; }
        }

        .lema-susurro {
            max-width: 700px;
            font-size: 16px;
            letter-spacing: 2px;
            line-height: 2;
            color: #a0a0a0; 
            text-shadow: 0 0 10px rgba(0, 0, 0, 0.9);
            margin-bottom: 4vh;
            transition: color 2s ease-in-out;
            position: relative;
            z-index: 1;
        }

        .flecha-indicadora {
            font-size: 28px;
            color: #a0a0a0; 
            animation: respirar 2s infinite;
            margin-bottom: 12vh;
            transition: color 2s ease-in-out;
            text-shadow: 0 0 8px rgba(0, 0, 0, 0.8);
            position: relative;
            z-index: 1;
        }

        @keyframes respirar {
            0% { transform: translateY(0px); opacity: 0.4; }
            50% { transform: translateY(12px); opacity: 1; }
            100% { transform: translateY(0px); opacity: 0.4; }
        }

        .contenedor {
            max-width: 650px;
            width: 90%;
            background: rgba(5, 5, 16, 0.80); 
            padding: 40px;
            border-radius: 4px;
            border: 1px solid #222;
            position: relative;
            z-index: 1;
        }
        
        .seccion { 
            margin-bottom: 30px; 
            text-align: left; 
            border-left: 1px solid #333; 
            padding-left: 15px;
        }
        .titulo-seccion { color: #333; font-size: 11px; text-transform: uppercase; transition: color 2s ease-in-out;}
        
        /* ESTILOS PARA LA CARTA FÍSICA */
        .contenedor-carta {
            margin-bottom: 30px;
            opacity: 0;
            transform: scale(0.8);
            transition: all 1.5s ease-in-out;
        }
        body.iluminado .contenedor-carta {
            opacity: 1;
            transform: scale(1);
        }
        .carta-img {
            width: 180px;
            border-radius: 8px;
            border: 2px solid #333;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
            transition: border-color 2s ease-in-out, box-shadow 2s ease-in-out;
        }
        body.iluminado .carta-img {
            border-color: #d4af37;
            box-shadow: 0 0 25px rgba(212, 175, 55, 0.4);
        }

        body.iluminado { color: #d4af37; }
        body.iluminado .lema-susurro { color: #d4af37; }
        body.iluminado .flecha-indicadora { color: #d4af37; display: none; }
        body.iluminado .titulo-seccion { color: #ffe066; }
        body.iluminado .contenedor { border-color: #8b7355; }
        
        .formulario-input {
            background: transparent;
            border: 1px solid #444;
            color: #a0a0a0;
            padding: 10px;
            font-size: 18px;
            text-align: center;
            width: 80px;
            font-family: inherit;
            margin-bottom: 20px;
            transition: all 2s ease;
        }
        body.iluminado .formulario-input { border-color: #d4af37; color: #d4af37; }
        .formulario-input:focus { outline: none; border-color: #888; }

        #boton-form {
            background: transparent;
            border: 1px solid #444; 
            color: #666;
            padding: 12px 25px;
            cursor: pointer;
            font-family: inherit;
            font-size: 11px;
            letter-spacing: 1px;
            transition: all 2s ease;
            margin-bottom: 30px;
        }
        body.iluminado #boton-form { border-color: #8b7355; color: #d4af37; display: none; }
        
        .mensaje-error { color: #8b0000; font-size: 12px; margin-bottom: 20px; }
    </style>
</head>
<body>
    
    <div class="lema-susurro">
        La vida es un arte que no se termina de artificar; es un arte que viene de otros mundos, escrito con tinta negra en papel oscuro… para leerlo, cierra tus ojos e ilumina tu mente para leer lo escrito con clara oscuridad.
    </div>

    <div class="flecha-indicadora">↓</div>

    <div class="contenedor">
        <form action="/revelar" method="POST">
            <label style="color: #555; font-size: 12px; display: block; margin-bottom: 10px;">ELIGE LA TINTA (0 AL 15)</label>
            <input type="number" name="numero_arcano" class="formulario-input" min="0" max="15" required autofocus>
            <br>
            <button type="submit" id="boton-form">ILUMINAR MENTE</button>
        </form>

        {% if error %}
            <div class="mensaje-error">{{ error }}</div>
        {% endif %}

        {% if mecanismo %}
            <!-- LA CARTA APARECE AQUÍ -->
            <div class="contenedor-carta">
                <img src="{{ imagen_url }}" alt="{{ nombre_arcano }}" class="carta-img">
            </div>

            <div class="seccion">
                <div class="titulo-seccion">{{ nombre_arcano }} - Mecanismo Cósmico</div>
                <div>{{ mecanismo }}</div>
            </div>

            <div class="seccion">
                <div class="titulo-seccion">Sombra (Klipá)</div>
                <div>{{ sombra }}</div>
            </div>

            <div class="seccion">
                <div class="titulo-seccion">Tikkun (Acción)</div>
                <div>{{ tikkun }}</div>
            </div>
            
            <script>
                document.body.classList.add('iluminado');
            </script>
        {% endif %}
    </div>

</body>
</html>
"""

# FUNCIÓN PARA CONECTAR A LA BASE DE DATOS
def get_db_connection():
    db_url = os.environ.get("DATABASE_URL", "dbname='db_clara_oscuridad' user='postgres' password='12345678' host='localhost' port='5432'")
    return psycopg2.connect(db_url)

# FUNCIÓN MÁGICA: Construye la base de datos si está vacía (Para la nube)
def inicializar_base_de_datos():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Crea la tabla si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS arcanos (
            id SERIAL PRIMARY KEY,
            numero INTEGER UNIQUE,
            nombre VARCHAR(50),
            mecanismo_cosmico TEXT,
            sombra_klipa TEXT,
            tikkun_accion TEXT
        );
    """)
    
    # Verifica si ya tiene datos
    cur.execute("SELECT COUNT(*) FROM arcanos;")
    cantidad = cur.fetchone()[0]
    
    # Si está vacía, inserta los 11 Arcanos
    if cantidad == 0:
        cur.execute("""
        INSERT INTO arcanos (numero, nombre, mecanismo_cosmico, sombra_klipa, tikkun_accion) VALUES 
        (0, 'El Loco', 'Representa la fuerza de vida pura antes de chocar con el espacio vacío. Es el impulso cuántico que aún no ha decidido qué partícula ser.', 'En el ser humano, la distorsión es el escapismo. Incapacidad de comprometerse con la forma por miedo a fracasar.', 'Hoy, toma un riesgo calculado que tu lógica rechaza. Enséñale a tu alma que el vacío no te traga.'),
        (1, 'El Mago', 'Es el puente entre el infinito (Kether) y la materia (Malkuth). Representa la capacidad del universo de concentrar todas las fuerzas dispersas en un solo punto de voluntad.', 'El manipulador. El charlatán que usa su inteligencia y su capacidad de comunicación para engañar, robar energía o crear ilusiones.', 'Artifica el enfoque: Hoy, elige UNA sola intención. Toma un objeto físico y concéntrate en él durante 2 minutos visualizando que a través de él fluye la luz de tu Sefirá.'),
        (2, 'La Sacerdotisa', 'Es la energía de Chokmah recibida en Binah. Es la luna que no tiene luz propia, sino que refleja la luz del sol. Representa el subconsciente universal.', 'El bloqueo emocional. El secreto tóxico. Es cuando la intuición se convierte en paranoia, o cuando te refugias tanto en tu mundo interior que te desconectas.', 'Artifica el silencio: Hoy, no reacciones inmediatamente ante ninguna provocación. Retírate a un lugar oscuro o cierra los ojos por 5 minutos antes de responder.'),
        (3, 'La Emperatriz', 'Es la fuerza de Binah materializándose. Es Venus. Es el útero cósmico que toma la semilla abstracta y la convierte en naturaleza, abundancia y sentimiento.', 'El apego material y el smothering (asfixia emocional). El exceso de protección que sofoca al otro. La creencia de que tu valor depende de cuánto posees.', 'Artifica la fertilidad: Regala algo tuyo (tiempo, comida, un objeto bello) a alguien que no lo espera. No lo hagas para recibir gracias; hazlo para ejercitar el músculo de la abundancia.'),
        (4, 'El Emperador', 'Es la energía de Chesed tomando estructura. Es Aries. Si la Emperatriz es la naturaleza salvaje, el Emperador es el agricultor que pone cercos y canales.', 'El tirano. El controlador rígido que no soporta la espontaneidad. El miedo obsesivo a perder el control que te lleva a micro-gestionar cada detalle.', 'Artifica la estructura: Elige una zona de tu vida que es puro caos y ponle UNA regla firme hoy. No lo hagas con ira, hazlo con el amor de un arquitecto.'),
        (5, 'El Hierofante', 'Es la energía de Geburah canalizada a través de la tradición. Es Tauro. Es el puente entre la humanidad y lo divino a través de la estructura del conocimiento.', 'El dogma ciego. El fanatismo religioso o ideológico. Seguir las reglas de otros sin cuestionarlas, entregando tu libre albedrío.', 'Artifica la duda santa: Cuestiona una creencia que tienes desde la infancia. No para destruirla, sino para ver si realmente te sirve a TI hoy.'),
        (6, 'Los Enamorados', 'Es la fuerza central de Tiferet (La Belleza). Representa la fricción y la inevitable alquimia que ocurre cuando dos polaridades se encuentran.', 'La indecisión paralizante. El triángulo amoroso o la división interna. Entregar tu poder de decisión a los demás por miedo a equivocarte.', 'Artifica la elección: Hoy, toma una decisión que has estado postergando. No elijas la opción perfecta, elige la que alinee tu mente con tu intuición.'),
        (7, 'El Carro', 'Es la energía de Netzaj (La Victoria). Es la fuerza de voluntad pura en movimiento. Es el carro de guerra que penetra el caos para imponer el orden del espíritu.', 'La agresión desmedida y el autoritarismo. Forzar situaciones cuando el timing no es correcto. Avanzar por pura fuerza bruta aplastando a los demás.', 'Artifica el avance: Toma acción directa sobre algo que has estado postergando. Pero hazlo con el control del Emperador, no con la furia del tirano.'),
        (8, 'La Justicia', 'Es el equilibrio exacto entre las fuerzas de Netzaj y Hod. Es la ley de causa y efecto (Karma) manifestada. Es la espada de la verdad que corta la ilusión.', 'El legalismo frío y la falta de compasión. Juzgar a otros con dureza para proyectar tus propias sombras.', 'Artifica el equilibrio: Perdona una deuda literal o emocional hoy. Suelta la necesidad de tener la razón.'),
        (9, 'El Ermitaño', 'Es la energía de Yesod (El Fundamento) llevada hacia adentro. Es la luz interna que no necesita el sol externo. Es la sabiduría del silencio.', 'El aislamiento por miedo o misantropía. La arrogancia espiritual de creerse iluminado y superior al mundo material.', 'Artifica el retiro: Apaga tu teléfono durante 30 minutos. Siéntate en silencio absoluto. No medites, solo escucha la voz de tu oscuridad.'),
        (10, 'La Rueda de la Fortuna', 'Es la energy de Malkuth (El Reino) interactuando con el eje central del universo. Representa el ciclo eterno: lo que sube debe bajar.', 'La resistencia al cambio. Aferrarse al pico del éxito o deprimirse en el valle del fracaso, olvidando que la rueda siempre gira.', 'Artifica la fluidez: Acepta un cambio de planes repentino hoy sin quejarte. Fluye con la rueda como el agua.')
        ON CONFLICT (numero) DO NOTHING;
        """)
        conn.commit()
    
    cur.close()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def pagina_principal():
    return render_template_string(PLANTILLA_HTML)

@app.route('/revelar', methods=['POST'])
def revelar_arcano():
    error = None
    mecanismo = sombra = tikkun = nombre_arcano = imagen_url = None

    try:
        numero = request.form['numero_arcano']
        
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, mecanismo_cosmico, sombra_klipa, tikkun_accion FROM arcanos WHERE numero = %s;", (numero,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado:
            nombre_arcano = resultado[0]
            mecanismo = resultado[1]
            sombra = resultado[2]
            tikkun = resultado[3]
            # Buscamos la imagen en nuestro diccionario
            imagen_url = IMAGENES_ARCANOS.get(int(numero), "")
        else:
            error = "Esa tinta aún no ha sido mezclada en la oscuridad. Elige un número del 0 al 15."

    except Exception as e:
        error = f"Error en la matrix: {e}"

    return render_template_string(PLANTILLA_HTML, error=error, nombre_arcano=nombre_arcano, mecanismo=mecanismo, sombra=sombra, tikkun=tikkun, imagen_url=imagen_url)

# Ejecutamos la creación de la base de datos al iniciar
inicializar_base_de_datos()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)