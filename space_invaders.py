import tkinter as tk
import random
import time

class SpaceInvadersDeluxe:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Invaders: Falcon Assault")
        self.root.resizable(False, False)

        # Dimensiones de la pantalla
        self.width = 600
        self.height = 700

        # Canvas con fondo espacial profundo
        self.canvas = tk.Canvas(
            root, width=self.width, height=self.height, bg="#04050d", highlightthickness=0
        )
        self.canvas.pack()

        # Variables de estado
        self.score = 0
        self.lives = 3
        self.wave = 1
        self.game_over = False
        self.invulnerable_frames = 0

        # Control de enfriamiento de ráfaga (300 ms)
        self.last_shot_time = 0.0
        self.shoot_cooldown = 0.300

        # Entidades activas
        self.player_lasers = []
        self.alien_lasers = []
        self.aliens = []
        self.player_items = []
        self.pressed_keys = set()

        # Generación del cielo estrellado y nebulosa
        self.draw_starfield()

        # Elementos iniciales
        self.init_hud()
        self.init_player()
        self.start_wave(self.wave)

        # Controles
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

        # Bucle de juego (~60 FPS)
        self.game_loop()

    # ==================== FONDO ESTRELLADO ====================
    def draw_starfield(self):
        """Genera un fondo estelar denso con varias capas y colores galácticos."""
        # Capa 1: Micro-estrellas distantes (polvo espacial tenue)
        for _ in range(120):
            x = random.randint(0, self.width)
            y = random.randint(46, self.height)
            col = random.choice(["#223355", "#334466", "#445577", "#2e1f4d"])
            self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=col, outline="")

        # Capa 2: Estrellas brillantes de colores astronómicos
        star_palette = ["#FFFFFF", "#D0E7FF", "#FFF8D6", "#99CCFF", "#FFB6C1", "#00FFFF"]
        for _ in range(70):
            x = random.randint(0, self.width)
            y = random.randint(46, self.height)
            size = random.choice([1, 2, 2])
            col = random.choice(star_palette)
            self.canvas.create_oval(x, y, x + size, y + size, fill=col, outline="")

        # Capa 3: Estrellas titilantes grandes en cruz
        for _ in range(8):
            cx = random.randint(20, self.width - 20)
            cy = random.randint(60, self.height - 120)
            self.canvas.create_line(cx - 3, cy, cx + 3, cy, fill="#FFFFFF", width=1)
            self.canvas.create_line(cx, cy - 3, cx, cy + 3, fill="#FFFFFF", width=1)
            self.canvas.create_rectangle(cx, cy, cx + 1, cy + 1, fill="#99E6FF", outline="")

    # ==================== PANEL SUPERIOR (HUD) ====================
    def init_hud(self):
        # Marco del panel de instrumentos superior
        self.canvas.create_rectangle(0, 0, self.width, 42, fill="#080b18", outline="")
        self.canvas.create_line(0, 42, self.width, 42, fill="#00E5FF", width=2)
        self.canvas.create_line(0, 44, self.width, 44, fill="#1a2540", width=1)

        self.score_text = self.canvas.create_text(
            15, 21, anchor="w", fill="#00FFCC",
            font=("Courier", 13, "bold"), text=f"SCORE: {self.score:05d}"
        )
        self.wave_text = self.canvas.create_text(
            self.width / 2, 21, anchor="center", fill="#FFE600",
            font=("Courier", 13, "bold"), text=f"SECTOR {self.wave}"
        )
        self.lives_text = self.canvas.create_text(
            self.width - 15, 21, anchor="e", fill="#FF3366",
            font=("Courier", 13, "bold"), text=f"LIVES: {'♥ ' * self.lives}"
        )

    def update_hud(self):
        self.canvas.itemconfig(self.score_text, text=f"SCORE: {self.score:05d}")
        self.canvas.itemconfig(self.wave_text, text=f"SECTOR {self.wave}")
        hearts = "♥ " * max(0, self.lives)
        self.canvas.itemconfig(self.lives_text, text=f"LIVES: {hearts}")

    # ==================== NAVE JUGADOR: HALCÓN MILENARIO ====================
    def init_player(self):
        self.player_x = self.width / 2
        self.player_y = self.height - 65
        self.player_speed = 6.5
        self.draw_player()

    def draw_player(self):
        for item in self.player_items:
            self.canvas.delete(item)
        self.player_items.clear()

        x, y = self.player_x, self.player_y

        # 1. Resplandor del Hiperimpulsor (arco de plasma cian)
        engine_glow = self.canvas.create_arc(
            x - 18, y + 10, x + 18, y + 27,
            start=180, extent=180, fill="#00E5FF", outline="#B3F5FF", width=1.5
        )

        # 2. Casco circular principal (placas de blindaje)
        hull_base = self.canvas.create_oval(
            x - 24, y - 10, x + 24, y + 21,
            fill="#B8BDBA", outline="#545957", width=2
        )
        # Rejillas circulares de escape traseras
        vent1 = self.canvas.create_oval(x - 12, y + 10, x - 6, y + 16, fill="#4A4F4D", outline="")
        vent2 = self.canvas.create_oval(x + 6, y + 10, x + 12, y + 16, fill="#4A4F4D", outline="")
        vent3 = self.canvas.create_oval(x - 3, y + 12, x + 3, y + 18, fill="#4A4F4D", outline="")

        # 3. Mandíbulas delanteras (fosas de carga anguladas)
        left_mandible = self.canvas.create_polygon(
            [x - 18, y - 5, x - 18, y - 28, x - 6, y - 28, x - 6, y - 8],
            fill="#C5CAC7", outline="#545957", width=1.5
        )
        right_mandible = self.canvas.create_polygon(
            [x + 6, y - 8, x + 6, y - 28, x + 18, y - 28, x + 18, y - 5],
            fill="#C5CAC7", outline="#545957", width=1.5
        )
        # Ranura oscura entre mandíbulas
        cargo_slot = self.canvas.create_rectangle(
            x - 6, y - 18, x + 6, y - 6,
            fill="#1E2120", outline="#3E4240"
        )

        # 4. Cabina asimétrica (lateral derecha)
        cockpit_corridor = self.canvas.create_polygon(
            [x + 16, y - 6, x + 27, y - 4, x + 27, y + 3, x + 16, y + 5],
            fill="#9EA4A1", outline="#545957"
        )
        cockpit_glass = self.canvas.create_polygon(
            [x + 25, y - 13, x + 30, y - 13, x + 30, y - 2, x + 25, y - 2],
            fill="#23D9D9", outline="#0C656B"
        )

        # 5. Torreta central cuádruple con cañón doble rojo
        turret_mount = self.canvas.create_oval(
            x - 6, y + 1, x + 6, y + 11,
            fill="#5E6361", outline="#2F3331", width=1.5
        )
        gun_l = self.canvas.create_line(x - 2, y + 3, x - 2, y - 14, fill="#FF1744", width=2)
        gun_r = self.canvas.create_line(x + 2, y + 3, x + 2, y - 14, fill="#FF1744", width=2)

        self.player_items.extend([
            engine_glow, hull_base, vent1, vent2, vent3,
            left_mandible, right_mandible, cargo_slot,
            cockpit_corridor, cockpit_glass, turret_mount, gun_l, gun_r
        ])

    # ==================== FORMACIÓN ALIENÍGENA ====================
    def start_wave(self, wave_num):
        for p in self.player_lasers:
            self.canvas.delete(p)
        for al in self.alien_lasers:
            self.canvas.delete(al)
        for alien in self.aliens:
            for item in alien["parts"]:
                self.canvas.delete(item)

        self.player_lasers.clear()
        self.alien_lasers.clear()
        self.aliens.clear()

        # Ajuste de dificultad por oleada
        speed_factor = min(2.6, 1.0 + (wave_num - 1) * 0.22)
        self.alien_speed_x = 2.0 * speed_factor
        self.alien_drop_y = 16
        self.fire_chance = min(0.065, 0.015 + (wave_num - 1) * 0.006)

        rows = 3
        cols = 8
        spacing_x = 58
        spacing_y = 50
        start_x = 55
        start_y = 75

        for r in range(rows):
            for c in range(cols):
                cx = start_x + c * spacing_x
                cy = start_y + r * spacing_y

                # Fila 0: Naves aliens (platillos nodriza)
                if r == 0:
                    alien_obj = self.create_ufo_craft(cx, cy)
                # Filas 1 y 2: Aliens (marcianos con tentáculos)
                elif r == 1:
                    alien_obj = self.create_martian(cx, cy, color="#00FF7F", eye_color="#FF0055")
                else:
                    alien_obj = self.create_martian(cx, cy, color="#FF0077", eye_color="#00FFFF")

                self.aliens.append(alien_obj)

        self.update_hud()

    def create_ufo_craft(self, x, y):
        """Nave Platillo: Anillo exterior elíptico, cúpula y toberas de luz."""
        # Resplandor gravitatorio inferior
        glow = self.canvas.create_oval(x - 12, y + 6, x + 12, y + 12, fill="#400080", outline="")
        # Cúpula de cristal transparente
        dome = self.canvas.create_oval(x - 10, y - 13, x + 10, y - 1, fill="#00E5FF", outline="#FFFFFF", width=1.2)
        # Piloto marcianito visible tras el domo
        pilot = self.canvas.create_oval(x - 3, y - 9, x + 3, y - 3, fill="#39FF14", outline="")
        # Platillo elíptico metálico
        hull = self.canvas.create_oval(x - 22, y - 6, x + 22, y + 8, fill="#6610F2", outline="#C4B5FD", width=1.5)
        # Estroboscopios / propulsores inferiores
        b1 = self.canvas.create_oval(x - 16, y + 1, x - 11, y + 6, fill="#FFE600", outline="")
        b2 = self.canvas.create_oval(x - 3, y + 2, x + 3, y + 7, fill="#FF0055", outline="")
        b3 = self.canvas.create_oval(x + 11, y + 1, x + 16, y + 6, fill="#FFE600", outline="")

        parts = [glow, dome, pilot, hull, b1, b2, b3]
        return {"type": "ufo", "parts": parts, "collision_id": hull, "score": 150}

    def create_martian(self, x, y, color, eye_color):
        """Marciano: Antenas con esferas, cuerpo con cabeza acampanada y patas múltiples."""
        # Antenas curvas
        ant_l = self.canvas.create_line(x - 6, y - 8, x - 14, y - 17, fill=color, width=2)
        ant_r = self.canvas.create_line(x + 6, y - 8, x + 14, y - 17, fill=color, width=2)
        tip_l = self.canvas.create_oval(x - 17, y - 20, x - 11, y - 14, fill="#FFF", outline=color)
        tip_r = self.canvas.create_oval(x + 11, y - 20, x + 17, y - 14, fill="#FFF", outline=color)

        # Cabeza abombada marciana
        head = self.canvas.create_polygon(
            [x - 14, y - 9, x + 14, y - 9, x + 17, y + 2, x - 17, y + 2],
            fill=color, outline="#FFFFFF", width=1.2
        )
        # Ojos fluorescentes
        eye_l = self.canvas.create_polygon(
            [x - 11, y - 5, x - 3, y - 7, x - 5, y + 1],
            fill=eye_color, outline="#000"
        )
        eye_r = self.canvas.create_polygon(
            [x + 11, y - 5, x + 3, y - 7, x + 5, y + 1],
            fill=eye_color, outline="#000"
        )

        # Abdomen y tentáculos inferiores
        body = self.canvas.create_rectangle(x - 12, y + 2, x + 12, y + 8, fill=color, outline="")
        leg1 = self.canvas.create_line(x - 11, y + 8, x - 15, y + 15, fill=color, width=2)
        leg2 = self.canvas.create_line(x - 4, y + 8, x - 4, y + 16, fill=color, width=2)
        leg3 = self.canvas.create_line(x + 4, y + 8, x + 4, y + 16, fill=color, width=2)
        leg4 = self.canvas.create_line(x + 11, y + 8, x + 15, y + 15, fill=color, width=2)

        parts = [ant_l, ant_r, tip_l, tip_r, head, eye_l, eye_r, body, leg1, leg2, leg3, leg4]
        return {"type": "martian", "parts": parts, "collision_id": head, "score": 90}

    # ==================== ENTRADA Y DISPARO ====================
    def on_key_press(self, event):
        self.pressed_keys.add(event.keysym)
        if event.keysym in ("r", "R") and self.game_over:
            self.restart_game()

    def on_key_release(self, event):
        self.pressed_keys.discard(event.keysym)

    def handle_continuous_shooting(self):
        """Mantiene fuego en ráfaga cada 300 ms mientras la barra esté presionada."""
        if "space" in self.pressed_keys and not self.game_over:
            current_time = time.time()
            if current_time - self.last_shot_time >= self.shoot_cooldown:
                self.shoot_player_laser()
                self.last_shot_time = current_time

    def shoot_player_laser(self):
        # Disparo doble desde los cañones del Halcón
        lx = self.player_x
        ly = self.player_y - 25
        laser_l = self.canvas.create_rectangle(lx - 4, ly - 14, lx - 1, ly, fill="#FF1744", outline="#FFD700")
        laser_r = self.canvas.create_rectangle(lx + 1, ly - 14, lx + 4, ly, fill="#FF1744", outline="#FFD700")
        self.player_lasers.extend([laser_l, laser_r])

    # ==================== FÍSICA Y ACTUALIZACIÓN ====================
    def update_player(self):
        dx = 0
        if "Left" in self.pressed_keys:
            dx -= self.player_speed
        if "Right" in self.pressed_keys:
            dx += self.player_speed

        if dx != 0:
            new_x = self.player_x + dx
            if 34 <= new_x <= self.width - 34:
                self.player_x = new_x
                for item in self.player_items:
                    self.canvas.move(item, dx, 0)

        # Parpadeo de invulnerabilidad
        if self.invulnerable_frames > 0:
            self.invulnerable_frames -= 1
            visible = (self.invulnerable_frames // 4) % 2 == 0
            state = "normal" if visible else "hidden"
            for item in self.player_items:
                self.canvas.itemconfig(item, state=state)
        else:
            for item in self.player_items:
                self.canvas.itemconfig(item, state="normal")

    def update_lasers(self):
        for laser in self.player_lasers[:]:
            self.canvas.move(laser, 0, -12)
            coords = self.canvas.coords(laser)
            if coords and coords[3] < 45:
                self.canvas.delete(laser)
                self.player_lasers.remove(laser)

        for a_laser in self.alien_lasers[:]:
            self.canvas.move(a_laser, 0, 6.5)
            coords = self.canvas.coords(a_laser)
            if coords and coords[1] > self.height:
                self.canvas.delete(a_laser)
                self.alien_lasers.remove(a_laser)

    def update_aliens(self):
        if not self.aliens:
            return

        hit_edge = False
        for alien in self.aliens:
            bbox = self.canvas.bbox(alien["collision_id"])
            if bbox:
                if (bbox[2] + self.alien_speed_x >= self.width - 10) or (bbox[0] + self.alien_speed_x <= 10):
                    hit_edge = True
                    break

        if hit_edge:
            self.alien_speed_x = -self.alien_speed_x
            for alien in self.aliens:
                for part in alien["parts"]:
                    self.canvas.move(part, 0, self.alien_drop_y)
        else:
            for alien in self.aliens:
                for part in alien["parts"]:
                    self.canvas.move(part, self.alien_speed_x, 0)

        # Proyectiles de plasma enemigo
        if random.random() < self.fire_chance and len(self.alien_lasers) < 5:
            shooter = random.choice(self.aliens)
            bbox = self.canvas.bbox(shooter["collision_id"])
            if bbox:
                mid_x = (bbox[0] + bbox[2]) / 2
                bottom_y = bbox[3] + 2
                color = "#00FFCC" if shooter["type"] == "ufo" else "#39FF14"
                plasma = self.canvas.create_oval(
                    mid_x - 3, bottom_y, mid_x + 3, bottom_y + 12,
                    fill=color, outline="#FFFFFF", width=1
                )
                self.alien_lasers.append(plasma)

        # Invasión exitosa (colisión con la nave)
        for alien in self.aliens:
            bbox = self.canvas.bbox(alien["collision_id"])
            if bbox and bbox[3] >= self.player_y - 12:
                self.trigger_player_hit(fatal=True)
                return

    # ==================== COLISIONES ====================
    def check_collisions(self):
        # Disparos del Halcón vs Formación invasora
        for laser in self.player_lasers[:]:
            l_box = self.canvas.bbox(laser)
            if not l_box:
                continue

            hit = False
            for alien in self.aliens[:]:
                a_box = self.canvas.bbox(alien["collision_id"])
                if a_box and self.boxes_overlap(l_box, a_box):
                    for part in alien["parts"]:
                        self.canvas.delete(part)
                    self.aliens.remove(alien)

                    self.canvas.delete(laser)
                    if laser in self.player_lasers:
                        self.player_lasers.remove(laser)

                    self.score += alien["score"]
                    self.update_hud()

                    # Aceleración progresiva
                    if self.alien_speed_x > 0:
                        self.alien_speed_x += 0.04
                    else:
                        self.alien_speed_x -= 0.04
                    hit = True
                    break
            if hit:
                continue

        # Proyectiles enemigos vs Halcón Milenario
        if self.invulnerable_frames == 0:
            player_box = [self.player_x - 22, self.player_y - 20, self.player_x + 22, self.player_y + 20]
            for a_laser in self.alien_lasers[:]:
                al_box = self.canvas.bbox(a_laser)
                if al_box and self.boxes_overlap(al_box, player_box):
                    self.canvas.delete(a_laser)
                    self.alien_lasers.remove(a_laser)
                    self.trigger_player_hit()
                    break

        # Limpieza de sector y salto al siguiente nivel
        if not self.aliens and not self.game_over:
            self.wave += 1
            self.score += 500
            self.start_wave(self.wave)

    def boxes_overlap(self, b1, b2):
        return not (b1[2] < b2[0] or b1[0] > b2[2] or b1[3] < b2[1] or b1[1] > b2[3])

    def trigger_player_hit(self, fatal=False):
        if fatal:
            self.lives = 0
        else:
            self.lives -= 1
            self.invulnerable_frames = 90

        self.update_hud()

        if self.lives <= 0:
            self.end_game()

    def end_game(self):
        self.game_over = True
        for laser in self.player_lasers + self.alien_lasers:
            self.canvas.delete(laser)
        self.player_lasers.clear()
        self.alien_lasers.clear()

        # Ventana modal de derrota
        self.canvas.create_rectangle(
            self.width / 2 - 180, self.height / 2 - 75,
            self.width / 2 + 180, self.height / 2 + 75,
            fill="#080b18", outline="#FF0055", width=3
        )
        self.canvas.create_text(
            self.width / 2, self.height / 2 - 35,
            text="GAME OVER", fill="#FF2A2A", font=("Courier", 26, "bold")
        )
        self.canvas.create_text(
            self.width / 2, self.height / 2 + 3,
            text=f"Score: {self.score:05d}  |  Sector: {self.wave}",
            fill="#FFFFFF", font=("Courier", 13)
        )
        self.canvas.create_text(
            self.width / 2, self.height / 2 + 42,
            text="Presiona 'R' para reiniciar", fill="#00E5FF", font=("Courier", 12, "italic")
        )

    def restart_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.lives = 3
        self.wave = 1
        self.game_over = False
        self.invulnerable_frames = 0
        self.last_shot_time = 0.0
        self.player_lasers.clear()
        self.alien_lasers.clear()
        self.aliens.clear()
        self.player_items.clear()
        self.pressed_keys.clear()

        self.draw_starfield()
        self.init_hud()
        self.init_player()
        self.start_wave(self.wave)

    def game_loop(self):
        if not self.game_over:
            self.handle_continuous_shooting()
            self.update_player()
            self.update_lasers()
            self.update_aliens()
            self.check_collisions()

        self.root.after(16, self.game_loop)


if __name__ == "__main__":
    app_root = tk.Tk()
    game = SpaceInvadersDeluxe(app_root)
    app_root.mainloop()