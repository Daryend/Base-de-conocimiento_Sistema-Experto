# 🥊 Sistema Experto — Deportes de Combate

Sistema experto basado en **reglas SI-ENTONCES** (forward chaining) que recomienda qué deporte de combate deberías practicar —**Boxeo, Kickboxing/Muay Thai, Jiu Jitsu Brasileño, Lucha Olímpica o MMA**— a partir de 10 preguntas sobre tus características físicas, preferencias y objetivos.

Incluye **dos versiones equivalentes**, con la misma base de conocimiento:

| Versión | Tecnología | Archivo |
|---|---|---|
| 🖥️ Escritorio | Python + Tkinter | `sistema_experto_combate.py` |
| 🌐 Web | HTML + CSS + JavaScript (sin dependencias) | `sistema_experto.html` |

---

## 📋 Descripción

Este proyecto es una implementación didáctica de un **sistema experto clásico**, con las cuatro piezas típicas de la disciplina claramente separadas en el código:

1. **Base de Hechos** — las respuestas del usuario al cuestionario.
2. **Base de Conocimiento** — 15 reglas SI-ENTONCES, escritas a partir de conocimiento del dominio (deportes de combate).
3. **Motor de Inferencia** — recorre las reglas con *forward chaining*, evalúa cuáles se cumplen contra los hechos y acumula puntajes por cada hipótesis (deporte).
4. **Módulo de Explicación** — la interfaz no solo muestra el resultado, sino también **qué reglas se dispararon** y por qué, para que la recomendación sea trazable y no una "caja negra".

El sistema tiene **interacción alta**: se hacen 10 preguntas antes de ejecutar la inferencia, cubriendo contextura física, alcance, preferencia golpe/agarre, tolerancia al contacto, resistencia, velocidad/fuerza, experiencia previa, objetivo, flexibilidad y estilo de pelea.

---

## ✨ Características

- 🧠 Motor de inferencia por **encadenamiento hacia adelante** con acumulación de puntajes.
- 📊 Ranking final de las 5 disciplinas con su puntaje, no solo la ganadora.
- 🔎 **Explicabilidad**: lista exacta de qué reglas SI-ENTONCES se dispararon.
- 🎨 Interfaz con barra de progreso, ícono animado por deporte y modo claro/oscuro (versión web).
- 🔄 Botón para reiniciar el cuestionario sin cerrar la app.
- 🚫 Sin dependencias externas: la versión web es un único `.html` autocontenido, y la de escritorio solo usa la librería estándar de Python (`tkinter`).

---

## 🚀 Cómo usarlo

### Versión de escritorio (Python)

Requiere **Python 3.8+** (Tkinter viene incluido en la instalación estándar de Python en Windows y macOS; en Linux puede requerir instalarlo aparte).

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/sistema-experto-combate.git
cd sistema-experto-combate

# Ejecutar
python sistema_experto_combate.py
```

> En Linux, si `tkinter` no está instalado:
> `sudo apt-get install python3-tk` (Debian/Ubuntu)

### Versión web (HTML)

No requiere instalación ni servidor. Simplemente:

```bash
# Abrir directamente en el navegador
open sistema_experto.html      # macOS
start sistema_experto.html     # Windows
xdg-open sistema_experto.html  # Linux
```

O subilo a cualquier hosting estático (GitHub Pages, Netlify, Vercel) para compartirlo con un link.

---

## 🧩 Estructura del proyecto

```
sistema-experto-combate/
├── sistema_experto_combate.py   # Versión de escritorio (Tkinter)
├── sistema_experto.html         # Versión web (HTML/CSS/JS)
└── README.md
```

---

## 🔬 Arquitectura del sistema experto

```
┌─────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│  Base de Hechos  │ --> │  Motor de Inferencia │ --> │ Módulo de Salida /  │
│  (respuestas del │     │  (forward chaining,  │     │ Explicación (GUI)   │
│    usuario)      │     │  evalúa 15 reglas)    │     │                     │
└─────────────────┘     └──────────────────────┘     └────────────────────┘
                                    ↑
                         ┌──────────────────────┐
                         │ Base de Conocimiento  │
                         │  15 reglas SI-ENTONCES│
                         └──────────────────────┘
```

**Ejemplo de regla:**

```python
regla(
    "R1",
    "Si preferís golpear a distancia y tenés alcance largo, entonces sugiere Boxeo",
    lambda h: h.get("preferencia_golpe_agarre") == "Golpear a distancia"
              and h.get("altura_alcance") == "Largos",
    {"Boxeo": 3},
)
```

Cada regla es evaluada contra la base de hechos; si su condición se cumple, aporta puntaje a una o más hipótesis. Al finalizar el recorrido de las 15 reglas, se ordenan las hipótesis por puntaje y la de mayor puntaje es la recomendación final.

---

## 🛠️ Tecnologías utilizadas

- **Python 3** + **Tkinter** (interfaz de escritorio nativa, sin dependencias externas)
- **HTML5 / CSS3 / JavaScript** puro (interfaz web, sin frameworks ni librerías)

---

## 📌 Posibles mejoras futuras

- [ ] Agregar más reglas / disciplinas (ej. Karate, Taekwondo, Sambo).
- [ ] Persistir el historial de resultados (localStorage en la web / archivo JSON en escritorio).
- [ ] Exportar el resultado y la traza de reglas como PDF.
- [ ] Versión con motor de reglas basado en un lenguaje declarativo (ej. `experta` en Python) en vez de funciones lambda.

---

## 👤 Autor

Proyecto desarrollado como práctica de **sistemas expertos basados en reglas** (Inteligencia Artificial).

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Podés usarlo, modificarlo y compartirlo libremente citando la fuente.
