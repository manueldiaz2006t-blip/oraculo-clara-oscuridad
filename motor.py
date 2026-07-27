import os
from flask import Flask, render_template_string, request
import psycopg2

app = Flask(__name__)

# DICCIONARIO DE IMÁGENES (La tinta visual)
IMAGENES_ARCANOS = {
    0: "https://placehold.co/180x300/0a0a0a/d4af37?text=0+El+Loco&font=playfair-display",
    1: "https://placehold.co/180x300/0a0a0a/d4af37?text=1+El+Mago&font=playfair-display",
    2: "https://placehold.co/180x300/0a0a0a/d4af37?text=2+Sacerdotisa&font=playfair-display",
    3: "https://placehold.co/180x300/0a0a0a/d4af37?text=3+Emperatriz&font=playfair-display",
    4: "https://placehold.co/180x300/0a0a0a/d4af37?text=4+Emperador&font=playfair-display",
    5: "https://placehold.co/180x300/0a0a0a/d4af37?text=5+Hierofante&font=playfair-display"
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
            <label style="color: #555; font-size: 12px; display: block; margin-bottom: 10px;">ELIGE LA TINTA (0 AL 5)</label>
            <input type="number" name="numero_arcano" class="formulario-input" min="0" max="5" required autofocus>
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

# FUNCIÓN PARA CONECTAR A LA BASE DE DATOS (LOCAL O EN LA NUBE)
def get_db_connection():
    # Render.com inyecta la URL de la base de datos en una variable de entorno
    # Si no existe (o sea, estamos en tu PC), usa tus datos locales
    db_url = os.environ.get("DATABASE_URL", "dbname='db_clara_oscuridad' user='postgres' password='12345678' host='localhost' port='5432'")
    return psycopg2.connect(db_url)

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
            error = "Esa tinta aún no ha sido mezclada en la oscuridad. Elige un número del 0 al 5."

    except Exception as e:
        error = f"Error en la matrix: {e}"

    return render_template_string(PLANTILLA_HTML, error=error, nombre_arcano=nombre_arcano, mecanismo=mecanismo, sombra=sombra, tikkun=tikkun, imagen_url=imagen_url)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)