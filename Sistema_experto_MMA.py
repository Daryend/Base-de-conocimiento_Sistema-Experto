import tkinter as tk
from tkinter import ttk, messagebox
import math
 
# ----------------------------------------------------------------------------
# 1) BASE DE HECHOS
# ----------------------------------------------------------------------------
hechos = {}
 
# ----------------------------------------------------------------------------
# 2) PREGUNTAS
# ----------------------------------------------------------------------------
PREGUNTAS = [
    {
        "clave": "contextura",
        "texto": "1) ¿Cómo describirías tu contextura?",
        "opciones": ["Delgada/ágil", "Promedio/atlética", "Musculosa/fuerte"],
    },
    {
        "clave": "altura_alcance",
        "texto": "2) En relación a tu edad/grupo, ¿tu altura y alcance de brazos son...?",
        "opciones": ["Cortos", "Promedio", "Largos"],
    },
    {
        "clave": "preferencia_golpe_agarre",
        "texto": "3) Si tuvieras que elegir, ¿preferís golpear a distancia o ir al agarre/lucha?",
        "opciones": ["Golpear a distancia", "Me da igual", "Ir al agarre/lucha/piso"],
    },
    {
        "clave": "tolerancia_contacto",
        "texto": "4) ¿Qué tan cómodo estás con el contacto físico fuerte (golpes, piso)?",
        "opciones": ["Prefiero poco contacto", "Contacto moderado", "Full contact, no me importa"],
    },
    {
        "clave": "resistencia",
        "texto": "5) ¿Cómo es tu resistencia cardiovascular?",
        "opciones": ["Baja", "Promedio", "Alta"],
    },
    {
        "clave": "velocidad_fuerza",
        "texto": "6) ¿Qué predomina en vos?",
        "opciones": ["Velocidad/reflejos", "Equilibrado entre ambas", "Fuerza bruta"],
    },
    {
        "clave": "experiencia_previa",
        "texto": "7) ¿Tenés experiencia previa en algún deporte de combate?",
        "opciones": ["Ninguna", "Algo de boxeo/artes marciales", "Lucha/rugby/deportes de agarre"],
    },
    {
        "clave": "objetivo",
        "texto": "8) ¿Cuál es tu objetivo principal al practicar un deporte de combate?",
        "opciones": ["Defensa personal", "Competir seriamente", "Fitness/ejercicio"],
    },
    {
        "clave": "flexibilidad",
        "texto": "9) ¿Cómo es tu flexibilidad?",
        "opciones": ["Baja", "Promedio", "Alta"],
    },
    {
        "clave": "tolerancia_dolor_paciencia",
        "texto": "10) En una pelea larga, ¿preferís resolver rápido y explosivo, o ser paciente "
                 "y desgastar al rival?",
        "opciones": ["Rápido y explosivo", "Depende del momento", "Paciente, desgastar al rival"],
    },
]
 
# ----------------------------------------------------------------------------
# 3) BASE DE CONOCIMIENTO: reglas SI-ENTONCES
# ----------------------------------------------------------------------------
HIPOTESIS = ["Boxeo", "Kickboxing / Muay Thai", "Jiu Jitsu Brasileño", "Lucha Olímpica", "MMA"]
 
# Metadata visual y descriptiva por hipótesis (usada por la interfaz de resultado)
SPORT_INFO = {
    "Boxeo": {
        "color": "#c0392b",
        "emoji": "🥊",
        "frase": "Distancia, footwork y manos rápidas. El arte de golpear sin ser golpeado.",
    },
    "Kickboxing / Muay Thai": {
        "color": "#e67e22",
        "emoji": "🦵",
        "frase": "El 'arte de las ocho extremidades': puños, codos, rodillas y patas.",
    },
    "Jiu Jitsu Brasileño": {
        "color": "#2980b9",
        "emoji": "🤼",
        "frase": "Técnica y palanca por sobre la fuerza bruta. Gana quien controla el piso.",
    },
    "Lucha Olímpica": {
        "color": "#27ae60",
        "emoji": "🤸",
        "frase": "Derribos, control y una base física a prueba de todo.",
    },
    "MMA": {
        "color": "#8e44ad",
        "emoji": "🥋",
        "frase": "Todas las artes combinadas. El deporte de combate más completo.",
    },
}
 
 
def construir_reglas():
    reglas = []
 
    def regla(id_, descripcion, condicion, aportes):
        reglas.append({"id": id_, "descripcion": descripcion, "condicion": condicion, "aportes": aportes})
 
    # R1
    regla(
        "R1", "Si preferís golpear a distancia y tenés alcance largo, entonces sugiere Boxeo",
        lambda h: h.get("preferencia_golpe_agarre") == "Golpear a distancia"
        and h.get("altura_alcance") == "Largos",
        {"Boxeo": 3},
    )
    # R2
    regla(
        "R2", "Si preferís golpear a distancia y tenés buena resistencia, entonces sugiere Boxeo / Kickboxing",
        lambda h: h.get("preferencia_golpe_agarre") == "Golpear a distancia" and h.get("resistencia") == "Alta",
        {"Boxeo": 2, "Kickboxing / Muay Thai": 2},
    )
    # R3
    regla(
        "R3", "Si predomina la fuerza bruta y tolerás mucho contacto, entonces sugiere Kickboxing / Muay Thai",
        lambda h: h.get("velocidad_fuerza") == "Fuerza bruta"
        and h.get("tolerancia_contacto") == "Full contact, no me importa",
        {"Kickboxing / Muay Thai": 3},
    )
    # R4
    regla(
        "R4", "Si sos paciente para desgastar al rival y tenés alta resistencia, entonces sugiere Muay Thai",
        lambda h: h.get("tolerancia_dolor_paciencia") == "Paciente, desgastar al rival"
        and h.get("resistencia") == "Alta",
        {"Kickboxing / Muay Thai": 2},
    )
    # R5
    regla(
        "R5", "Si preferís ir al agarre/derribo y tenés contextura robusta, entonces sugiere Lucha Olímpica",
        lambda h: h.get("preferencia_golpe_agarre") == "Ir al agarre/lucha/piso"
        and h.get("contextura") == "Musculosa/fuerte",
        {"Lucha Olímpica": 3},
    )
    # R6
    regla(
        "R6", "Si tenés experiencia en lucha/rugby, entonces sugiere fuertemente Lucha Olímpica",
        lambda h: h.get("experiencia_previa") == "Lucha/rugby/deportes de agarre",
        {"Lucha Olímpica": 3, "MMA": 1},
    )
    # R7
    regla(
        "R7", "Si preferís ir al piso y tenés alta flexibilidad, entonces sugiere Jiu Jitsu Brasileño",
        lambda h: h.get("preferencia_golpe_agarre") == "Ir al agarre/lucha/piso"
        and h.get("flexibilidad") == "Alta",
        {"Jiu Jitsu Brasileño": 3},
    )
    # R8
    regla(
        "R8", "Si tu objetivo es defensa personal y preferís poco contacto, entonces sugiere BJJ (control sin golpear)",
        lambda h: h.get("objetivo") == "Defensa personal" and h.get("tolerancia_contacto") == "Prefiero poco contacto",
        {"Jiu Jitsu Brasileño": 2},
    )
    # R9
    regla(
        "R9", "Si te da igual golpear o agarrar y tu objetivo es competir seriamente, entonces sugiere MMA",
        lambda h: h.get("preferencia_golpe_agarre") == "Me da igual" and h.get("objetivo") == "Competir seriamente",
        {"MMA": 3},
    )
    # R10
    regla(
        "R10", "Si tolerás full contact y tenés experiencia mixta, entonces sugiere MMA",
        lambda h: h.get("tolerancia_contacto") == "Full contact, no me importa"
        and h.get("experiencia_previa") == "Algo de boxeo/artes marciales",
        {"MMA": 3},
    )
    # R11
    regla(
        "R11", "Si predomina la velocidad/reflejos y el alcance es corto, entonces sugiere Boxeo estilo infighter",
        lambda h: h.get("velocidad_fuerza") == "Velocidad/reflejos" and h.get("altura_alcance") == "Cortos",
        {"Boxeo": 2},
    )
    # R12
    regla(
        "R12", "Si buscás fitness/ejercicio y baja tolerancia al contacto, entonces sugiere Boxeo (técnica) o BJJ suave",
        lambda h: h.get("objetivo") == "Fitness/ejercicio" and h.get("tolerancia_contacto") == "Prefiero poco contacto",
        {"Boxeo": 1, "Jiu Jitsu Brasileño": 1},
    )
    # R13
    regla(
        "R13", "Si no tenés experiencia previa, contextura media y resistencia media, entonces perfil generalista -> MMA",
        lambda h: h.get("experiencia_previa") == "Ninguna"
        and h.get("contextura") == "Promedio/atlética"
        and h.get("resistencia") == "Promedio",
        {"MMA": 2},
    )
    # R14
    regla(
        "R14", "Si sos rápido/explosivo y preferís golpear, entonces sugiere Kickboxing / Muay Thai",
        lambda h: h.get("tolerancia_dolor_paciencia") == "Rápido y explosivo"
        and h.get("preferencia_golpe_agarre") == "Golpear a distancia",
        {"Kickboxing / Muay Thai": 2},
    )
    # R15
    regla(
        "R15", "Si contextura robusta, fuerza bruta y tolerancia full contact, entonces sugiere Lucha Olímpica o MMA",
        lambda h: h.get("contextura") == "Musculosa/fuerte"
        and h.get("velocidad_fuerza") == "Fuerza bruta"
        and h.get("tolerancia_contacto") == "Full contact, no me importa",
        {"Lucha Olímpica": 2, "MMA": 2},
    )
 
    return reglas
 
 
# ----------------------------------------------------------------------------
# 4) MOTOR DE INFERENCIA
# ----------------------------------------------------------------------------
def motor_inferencia(hechos, reglas):
    puntajes = {h: 0 for h in HIPOTESIS}
    reglas_disparadas = []
 
    for r in reglas:
        try:
            if r["condicion"](hechos):
                reglas_disparadas.append(r)
                for hipotesis, peso in r["aportes"].items():
                    puntajes[hipotesis] += peso
        except Exception:
            continue
 
    ranking = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
    return ranking, reglas_disparadas, puntajes
 
 
# ----------------------------------------------------------------------------
# 5) INTERFAZ GRÁFICA
# ----------------------------------------------------------------------------
FONT_TITULO = ("Segoe UI", 15, "bold")
FONT_PREGUNTA = ("Segoe UI", 13, "bold")
FONT_NORMAL = ("Segoe UI", 10)
BG = "#f4f4f7"
 
 
class SistemaExpertoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto — Perfil de Deportista de Combate")
        self.root.geometry("660x480")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
 
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure("TFrame", background=BG)
        self.style.configure("TLabel", background=BG, font=FONT_NORMAL)
        self.style.configure("Progreso.Horizontal.TProgressbar", troughcolor="#e0e0e5", background="#8e44ad")
 
        self.reglas = construir_reglas()
        self.indice_pregunta = 0
        self.resultado_frame = None  # frame del resultado, para poder destruirlo al reiniciar
 
        # --- Header ---
        header = ttk.Frame(root, padding=(25, 18, 25, 0))
        header.pack(fill="x")
        ttk.Label(header, text="🥊 Sistema Experto de Deportes de Combate", font=FONT_TITULO).pack(anchor="w")
        ttk.Label(
            header, text="Respondé 10 preguntas y el motor de inferencia te recomendará una disciplina.",
            font=FONT_NORMAL
        ).pack(anchor="w", pady=(2, 10))
 
        self.progreso = ttk.Progressbar(
            header, style="Progreso.Horizontal.TProgressbar", length=610,
            maximum=len(PREGUNTAS), value=0
        )
        self.progreso.pack(fill="x")
 
        # --- Contenedor principal (se reutiliza para preguntas y resultado) ---
        self.contenedor = ttk.Frame(root, padding=25)
        self.contenedor.pack(fill="both", expand=True)
 
        self.iniciar_cuestionario()
 
    # ---------------------- FLUJO DE PREGUNTAS ----------------------
    def limpiar_contenedor(self):
        for w in self.contenedor.winfo_children():
            w.destroy()
 
    def iniciar_cuestionario(self):
        hechos.clear()
        self.indice_pregunta = 0
        self.progreso.config(value=0)
        self.limpiar_contenedor()
 
        self.lbl_progreso = ttk.Label(self.contenedor, text="", font=("Segoe UI", 9), foreground="#666")
        self.lbl_progreso.pack(anchor="w")
 
        self.lbl_pregunta = ttk.Label(
            self.contenedor, text="", font=FONT_PREGUNTA, wraplength=590, justify="left"
        )
        self.lbl_pregunta.pack(anchor="w", pady=(8, 18))
 
        self.opcion_var = tk.StringVar()
        self.radios_frame = ttk.Frame(self.contenedor)
        self.radios_frame.pack(anchor="w", fill="x")
 
        self.btn_siguiente = ttk.Button(self.contenedor, text="Siguiente ▶", command=self.siguiente)
        self.btn_siguiente.pack(anchor="e", pady=(30, 0))
 
        self.mostrar_pregunta()
 
    def mostrar_pregunta(self):
        for widget in self.radios_frame.winfo_children():
            widget.destroy()
 
        p = PREGUNTAS[self.indice_pregunta]
        total = len(PREGUNTAS)
        self.lbl_progreso.config(text=f"Pregunta {self.indice_pregunta + 1} de {total}")
        self.lbl_pregunta.config(text=p["texto"])
        self.progreso.config(value=self.indice_pregunta)
 
        self.opcion_var.set("")
        for op in p["opciones"]:
            rb = ttk.Radiobutton(self.radios_frame, text=op, value=op, variable=self.opcion_var)
            rb.pack(anchor="w", pady=4)
 
        self.btn_siguiente.config(
            text="Finalizar e Inferir 🥊" if self.indice_pregunta == total - 1 else "Siguiente ▶"
        )
 
    def siguiente(self):
        seleccion = self.opcion_var.get()
        if not seleccion:
            messagebox.showwarning("Falta responder", "Por favor elegí una opción antes de continuar.")
            return
 
        p = PREGUNTAS[self.indice_pregunta]
        hechos[p["clave"]] = seleccion
 
        if self.indice_pregunta < len(PREGUNTAS) - 1:
            self.indice_pregunta += 1
            self.mostrar_pregunta()
        else:
            self.progreso.config(value=len(PREGUNTAS))
            self.ejecutar_inferencia()
 
    # ---------------------- INFERENCIA Y RESULTADO ----------------------
    def ejecutar_inferencia(self):
        ranking, reglas_disparadas, puntajes = motor_inferencia(hechos, self.reglas)
        self.mostrar_resultado(ranking, reglas_disparadas)
 
    def mostrar_resultado(self, ranking, reglas_disparadas):
        self.limpiar_contenedor()
 
        top_hipotesis, top_puntaje = ranking[0]
        info = SPORT_INFO[top_hipotesis]
 
        # --- Ilustración dinámica (Canvas animado) ---
        canvas = tk.Canvas(self.contenedor, width=610, height=150, bg=BG, highlightthickness=0)
        canvas.pack(pady=(0, 10))
        self._animar_resultado(canvas, info)
 
        ttk.Label(
            self.contenedor, text=top_hipotesis, font=("Segoe UI", 18, "bold"), foreground=info["color"]
        ).pack()
        ttk.Label(
            self.contenedor, text=info["frase"], font=("Segoe UI", 10, "italic"),
            wraplength=560, justify="center"
        ).pack(pady=(2, 12))
 
        # --- Ranking + explicación en pestañas para no saturar la pantalla ---
        notebook = ttk.Notebook(self.contenedor)
        notebook.pack(fill="both", expand=True)
 
        tab_ranking = ttk.Frame(notebook, padding=12)
        tab_explicacion = ttk.Frame(notebook, padding=12)
        notebook.add(tab_ranking, text="📊 Ranking")
        notebook.add(tab_explicacion, text=f"🔎 Reglas disparadas ({len(reglas_disparadas)}/{len(self.reglas)})")
 
        max_p = max(1, ranking[0][1])
        for hip, punt in ranking:
            fila = ttk.Frame(tab_ranking)
            fila.pack(fill="x", pady=3)
            ttk.Label(fila, text=f"{SPORT_INFO[hip]['emoji']} {hip}", width=28, anchor="w").pack(side="left")
            barra = tk.Canvas(fila, width=250, height=14, bg="#e0e0e5", highlightthickness=0)
            barra.pack(side="left", padx=6)
            ancho = int(250 * (punt / max_p)) if max_p else 0
            barra.create_rectangle(0, 0, ancho, 14, fill=SPORT_INFO[hip]["color"], width=0)
            ttk.Label(fila, text=str(punt)).pack(side="left")
 
        texto = tk.Text(tab_explicacion, wrap="word", font=("Consolas", 9), height=10, bd=0)
        texto.pack(fill="both", expand=True)
        if reglas_disparadas:
            for r in reglas_disparadas:
                texto.insert("end", f"[{r['id']}] {r['descripcion']}\n\n")
        else:
            texto.insert("end", "Ninguna regla se disparó con las respuestas dadas.\n")
        texto.config(state="disabled")
 
        # --- Botones finales ---
        botones = ttk.Frame(self.contenedor)
        botones.pack(fill="x", pady=(12, 0))
        ttk.Button(botones, text="🔄 Volver a intentar", command=self.iniciar_cuestionario).pack(side="left")
        ttk.Button(botones, text="Salir", command=self.root.destroy).pack(side="right")
 
    def _animar_resultado(self, canvas, info, paso=0):
        """Pequeña animación de 'entrada': un círculo que crece con el emoji del deporte."""
        canvas.delete("all")
        radio_max = 55
        radio = int(radio_max * min(1.0, (paso + 1) / 10))
        cx, cy = 305, 75
        canvas.create_oval(
            cx - radio, cy - radio, cx + radio, cy + radio,
            fill=info["color"], outline=""
        )
        if radio > 25:
            fuente_size = int(28 * (radio / radio_max))
            canvas.create_text(cx, cy, text=info["emoji"], font=("Segoe UI Emoji", max(10, fuente_size)))
        if paso < 9:
            canvas.after(35, lambda: self._animar_resultado(canvas, info, paso + 1))
 
 
# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExpertoGUI(root)
    root.mainloop()