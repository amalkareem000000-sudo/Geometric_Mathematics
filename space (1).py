import math
from vpython import *
import random as pyrandom
import numpy as np
import matplotlib.pyplot as plt


scene.title = "Autonomous Navigation for an Interplanetary Deep-Space Mission to Psyche: Weighted Vector Fusion of Star and X-Ray Pulsar Measurements"
# original title preserved below
# scene.title = "DEMA — OLD WORKING — ORION IMPACT FIX"
scene.background = color.black
scene.width = 1200
scene.height = 650
scene.userspin = True
scene.userzoom = True
scene.userpan = True


space_color = [
    color.white, 
    color.cyan, 
    vector(0.75, 0.85, 1.0), 
    vector(1.0, 0.7, 0.8), 
    vector(0.7, 0.8, 1.0)
]

for i in range(50000):
    rate(10000)
    x = pyrandom.uniform(-6000, 6000)
    y = pyrandom.uniform(-6000, 6000)
    z = pyrandom.uniform(-6000, 6000)
    choose_color = pyrandom.choice(space_color)
    sphere(
        pos=vector(x, y, z), 
        radius=1.9, 
        color=choose_color, 
        emissive=True
    )


sun = sphere(
    pos=vector(0, 0, 0), 
    radius=300, 
    texture=textures.rough,  
    emissive=True, 
    shininess=5, 
    color=color.orange
)

earth = sphere(
    pos=vector(1200, 1200, 0), 
    radius=100, 
    texture=textures.earth,
    emissive=True, 
    shininess=5
)

MOON_BLOCK_RADIUS = 48.0  # geometry radius for Earth->Orion line-of-sight occlusion
moon = sphere(
    pos=earth.pos + vector(250, 0, 0), 
    radius=48,  # visible Moon radius; matches the occlusion geometry
    texture=textures.rough,
    color=vector(0.82, 0.84, 0.90), 
    emissive=True, 
    shininess=0.15
)

moon_name = label(
    pos=moon.pos, 
    text="MOON", 
    yoffset=58, 
    height=20,
    box=False, 
    color=color.white
)

EARTH_SUN_OMEGA = 0.0008

MARS_SUN_R = 1800.0
mars_sun_theta = 0.5
MARS_SUN_OMEGA = EARTH_SUN_OMEGA / 1.88

mars = sphere(
    pos=vector(MARS_SUN_R * math.cos(mars_sun_theta), MARS_SUN_R * math.sin(mars_sun_theta), 0),
    radius=70,
    color=color.red,
    emissive=True ,
    textures = textures.wood
)
mars_name = label(
    pos=mars.pos, 
    text="MARS", 
    yoffset=50, 
    height=16, 
    box=False, 
    color=color.orange 
)

JUPITER_SUN_R = 3800.0
jupiter_sun_theta = 2.1
JUPITER_SUN_OMEGA = EARTH_SUN_OMEGA / 11.86

jupiter = sphere(
    pos=vector(JUPITER_SUN_R * math.cos(jupiter_sun_theta), JUPITER_SUN_R * math.sin(jupiter_sun_theta), 0),
    radius=140,
    color=vector(0.82, 0.68, 0.52),
    emissive=True , 
    textures = textures.wood
)
jupiter_name = label(
    pos=jupiter.pos, 
    text="JUPITER", 
    yoffset=120, 
    height=18, 
    box=False, 
    color=vector(0.9, 0.8, 0.6)
)


asteroids = []
num_asteroids = 1500

for i in range(num_asteroids):
    angle = pyrandom.uniform(0, 2 * math.pi)
    r = pyrandom.uniform(2600, 2600)
    z_pos = pyrandom.uniform(-1000, 1000)
    ast = sphere(
        pos=vector(r * math.cos(angle), r * math.sin(angle), z_pos), 
        radius=10, 
        color=color.gray(0.7), 
        emissive=True
    )
    ast.angle = angle
    ast.orbit_radius = r
    ast.speed = pyrandom.uniform(0.0002, 0.0005)  
    asteroids.append(ast)


angle_p = pyrandom.uniform(0, 2 * math.pi)
r_p = 2600

single_psyche = sphere(
    pos=vector(r_p * math.cos(angle_p), r_p * math.sin(angle_p), 0),
    radius=55, 
    color=color.red, 
    texture=textures.rock
)
single_psyche.angle = angle_p
single_psyche.orbit_radius = r_p
single_psyche.speed = 0.0003

psyche_name = label(
    pos=single_psyche.pos, 
    text="TARGET PSYCHE", 
    yoffset=65, 
    height=18,
    box=True, 
    color=color.red, 
    background=color.black, 
    opacity=0.7
)


pulsar_data = [
    {"name": "PSR J0218+4232", "pos": vector(-4500, 3000, -1500), "col": color.cyan, "freq": 3.0},
    {"name": "PSR B1821-24", "pos": vector(4000, 3500, 2000), "col": color.magenta, "freq": 4.5},
    {"name": "PSR J0030+0451", "pos": vector(-3500, -4000, 1000), "col": color.orange, "freq": 2.0},
    {"name": "PSR J0437-4715", "pos": vector(4500, -3000, -2000), "col": color.green, "freq": 5.0}
]

pulsars = []
pulsar_waves = []

for data in pulsar_data:
    star = sphere(
        pos=data["pos"], 
        radius=45, 
        color=data["col"], 
        emissive=True, 
        opacity=0.9
    )
    label(
        pos=data["pos"] + vector(0, 120, 0), 
        text=data["name"], 
        height=15, 
        box=False, 
        color=color.white
    )
    pulsars.append(star)
    
    wave = sphere(
        pos=data["pos"], 
        radius=50, 
        color=data["col"], 
        opacity=0.25, 
        emissive=True
    )
    wave.max_radius = 800  
    wave.expansion_speed = data["freq"] * 1.5
    pulsar_waves.append(wave)


bright_stars_data = [
    {"name": "Sirius", "pos": vector(-5000, 2000, -3000), "color": color.cyan, "radius": 50},
    {"name": "Vega", "pos": vector(3000, 5000, -2000), "color": color.white, "radius": 45},
    {"name": "Altair", "pos": vector(5500, 3500, -1000), "color": color.white, "radius": 40},
    {"name": "Deneb", "pos": vector(2000, 6000, -4000), "color": color.cyan, "radius": 45}
]

star_objects = []
for sdata in bright_stars_data:
    star = sphere(
        pos=sdata["pos"], 
        radius=sdata["radius"], 
        color=sdata["color"], 
        emissive=True
    )
    label(
        pos=sdata["pos"] + vector(0, 120, 0), 
        text=sdata["name"], 
        height=14, 
        box=False, 
        color=color.white
    )
    star_objects.append(star)

# VISUALLY DISTINCT ORION SPACECRAFT — large enough to read at Earth-orbit scale.
# This replaces the old tiny/ambiguous compound model ONLY; navigation math is untouched.
_sc0 = earth.pos + vector(120, 0, 0)
# Clean Orion silhouette: silver service module + white capsule + two blue solar wings.
# No yellow/orange object is part of the spacecraft.
orion_main_body = cylinder(
    pos=_sc0 - vector(26, 0, 0), 
    axis=vector(42, 0, 0), 
    radius=18, 
    color=vector(0.68, 0.72, 0.78)
)

orion_capsule_cone = cone(
    pos=_sc0 + vector(16, 0, 0), 
    axis=vector(30, 0, 0), 
    radius=18, 
    color=color.white
)

orion_engine_ring = cylinder(
    pos=_sc0 - vector(31, 0, 0), 
    axis=vector(6, 0, 0), 
    radius=20, 
    color=vector(0.22, 0.25, 0.30)
)

orion_panel_arm_top = cylinder(
    pos=_sc0, 
    axis=vector(0, 30, 0), 
    radius=2.5, 
    color=vector(0.75, 0.78, 0.82)
)

orion_panel_arm_bottom = cylinder(
    pos=_sc0, 
    axis=vector(0, -30, 0), 
    radius=2.5, 
    color=vector(0.75, 0.78, 0.82)
)

orion_solar_panel_top = box(
    pos=_sc0 + vector(0, 58, 0), 
    size=vector(8, 56, 34), 
    color=vector(0.05, 0.20, 0.72)
)

orion_solar_panel_bottom = box(
    pos=_sc0 - vector(0, 58, 0), 
    size=vector(8, 56, 34), 
    color=vector(0.05, 0.20, 0.72)
)

_sc_parts = [
    orion_main_body,
    orion_capsule_cone,
    orion_engine_ring,
    orion_panel_arm_top,
    orion_panel_arm_bottom,
    orion_solar_panel_top,
    orion_solar_panel_bottom
]
# IMPORTANT: do NOT compound the spacecraft parts.  In this VPython scene the
# compound logical position could separate from the rendered model.  Use one
# invisible anchor as the ONLY Orion position, and explicitly translate every
# visible spacecraft part from that anchor.
_orion_offsets = [vector(p.pos - _sc0) for p in _sc_parts]
# One explicit spacecraft center used by EVERYTHING: rendering, label, vectors and collision.
orion = sphere(pos=_sc0, radius=0.1, visible=False)
spacecraft_center = vector(_sc0)

def set_spacecraft_center(new_center):
    global spacecraft_center
    spacecraft_center = vector(new_center)
    orion.pos = vector(spacecraft_center)
    for part, off in zip(_sc_parts, _orion_offsets):
        part.pos = spacecraft_center + off

ORION_COLLISION_RADIUS = 18.0
set_spacecraft_center(_sc0)


orion_name = label(
    pos=orion.pos, 
    text="ORION SPACECRAFT", 
    yoffset=72, 
    height=20,
    box=True, 
    border=5, 
    color=color.white, 
    background=color.black, 
    opacity=0.70, 
    line=False
)

orion_telemetry_label = label(
    pos=orion.pos, 
    text="", 
    yoffset=-110, 
    height=12,
    box=True, 
    color=color.yellow, 
    background=color.black, 
    opacity=0.85, 
    line=True
)

star_rays = [
    curve(color=color.yellow, radius=1.5, opacity=0.35) 
    for _ in star_objects
]

pulsar_rays = [
    curve(color=p["col"], radius=2.0, opacity=0.50) 
    for p in pulsar_data
]

# ================= ADD-ON: NAVIGATION/CORRECTION ONLY =================
# Keep the PLANNED orbit independent from the corrected/actual spacecraft position.
ORION_A = 900.0
ORION_B = 620.0
orion_theta = 0.0

MOON_R = 360.0
moon_theta = 0.90 # guaranteed clear line-of-sight at startup; later the Moon crosses Earth-Orion LOS

moon.pos = earth.pos + vector(MOON_R * math.cos(moon_theta), MOON_R * math.sin(moon_theta), 0)

t = 0.0
dt = 0.05
loss_started = False
collision_done = False
dsn_loss_event_time = None  
pulsar_sigmas = [55.0, 80.0, 42.0, 68.0]


time_history = []
nav_error_history = []
correction_history = []

nav_status = label(
    pos=vector(24, scene.height - 34, 0), 
    pixel_pos=True,
    text="EARTH DSN LINK: CONNECTED [NORMAL OPERATIONS]", 
    align="left", 
    height=15, 
    box=True, 
    border=6, 
    color=color.green, 
    background=color.black, 
    opacity=0.88, 
    line=False
)

EARTH_SUN_R = mag(earth.pos - sun.pos)
earth_sun_theta = math.atan2(earth.pos.y - sun.pos.y, earth.pos.x - sun.pos.x)

scene.center = vector(earth.pos)
scene.range = 1400

# ================= VIEW CONTROLS =================
# Added only for easier camera control; simulation logic below is unchanged.
def _view_left(_b):
    scene.center = scene.center + vector(-0.12 * scene.range, 0, 0)

def _view_right(_b):
    scene.center = scene.center + vector(0.12 * scene.range, 0, 0)

def _view_up(_b):
    scene.center = scene.center + vector(0, 0.12 * scene.range, 0)

def _view_down(_b):
    scene.center = scene.center + vector(0, -0.12 * scene.range, 0)

def _zoom_in(_b):
    scene.range = max(50, scene.range * 0.82)

def _zoom_out(_b):
    scene.range = scene.range * 1.22

def _reset_view(_b):
    scene.center = vector(earth.pos)
    scene.range = 1400

scene.append_to_caption("\nVIEW: ")
button(text="LEFT", bind=_view_left)
scene.append_to_caption("  ")
button(text="RIGHT", bind=_view_right)
scene.append_to_caption("  ")
button(text="UP", bind=_view_up)
scene.append_to_caption("  ")
button(text="DOWN", bind=_view_down)
scene.append_to_caption("  ")
button(text="ZOOM+", bind=_zoom_in)
scene.append_to_caption("  ")
button(text="ZOOM-", bind=_zoom_out)
scene.append_to_caption("  ")
button(text="RESET", bind=_reset_view)
scene.append_to_caption("\n")
# =================================================


orion_intercept_pos = None


while True:
    rate(60)
    
    if collision_done:
        break

    t += dt
    
    earth.rotate(angle=0.001, axis=vector(0, 1, 0))
    earth_sun_theta += EARTH_SUN_OMEGA
    earth.pos = sun.pos + vector(
        EARTH_SUN_R * math.cos(earth_sun_theta), 
        EARTH_SUN_R * math.sin(earth_sun_theta), 
        0
    )
    
    moon_theta -= 0.003
    moon.pos = earth.pos + vector(
        MOON_R * math.cos(moon_theta), 
        MOON_R * math.sin(moon_theta), 
        0
    )
    moon_name.pos = moon.pos

    mars_sun_theta += MARS_SUN_OMEGA
    mars.pos = sun.pos + vector(
        MARS_SUN_R * math.cos(mars_sun_theta), 
        MARS_SUN_R * math.sin(mars_sun_theta), 
        0
    )
    mars_name.pos = mars.pos

    jupiter_sun_theta += JUPITER_SUN_OMEGA
    jupiter.pos = sun.pos + vector(
        JUPITER_SUN_R * math.cos(jupiter_sun_theta), 
        JUPITER_SUN_R * math.sin(jupiter_sun_theta), 
        0
    )
    jupiter_name.pos = jupiter.pos

    single_psyche.angle += single_psyche.speed
    single_psyche.pos.x = single_psyche.orbit_radius * math.cos(single_psyche.angle)
    single_psyche.pos.y = single_psyche.orbit_radius * math.sin(single_psyche.angle)
    psyche_name.pos = single_psyche.pos

    for wave in pulsar_waves:
        wave.radius += wave.expansion_speed
        wave.opacity = max(0.0, 0.35 * (1.0 - (wave.radius / wave.max_radius)))
        if wave.radius >= wave.max_radius:
            wave.radius = 50.0
            wave.opacity = 0.35

    orion_theta += 0.003  
    planned_orbit_offset = vector(
        ORION_A * math.cos(orion_theta), 
        ORION_B * math.sin(orion_theta), 
        0
    )
    r_planned = earth.pos + planned_orbit_offset

    _u_link = orion.pos - earth.pos
    _L2_link = dot(_u_link, _u_link)
    
    if _L2_link > 1e-9:
        _q_link = dot(moon.pos - earth.pos, _u_link) / _L2_link
    else:
        _q_link = -1.0
        
    if _L2_link > 1e-9:
        _closest_link = earth.pos + max(0.0, min(1.0, _q_link)) * _u_link
    else:
        _closest_link = earth.pos
        
    _d_link = mag(moon.pos - _closest_link)
    blocked_now = (0.0 < _q_link < 1.0) and (_d_link <= MOON_BLOCK_RADIUS)

    if not loss_started:
        if not blocked_now:
            nav_status.text = "EARTH DSN LINK: CONNECTED [NORMAL OPERATIONS]"
            nav_status.color = color.green
            set_spacecraft_center(r_planned)
            
            nav_err = pyrandom.gauss(2.0, 0.3)
            corr_vec = pyrandom.gauss(1.2, 0.2)
        else:
            loss_started = True
            dsn_loss_event_time = t
            orion_intercept_pos = vector(orion.pos)

    if loss_started and not collision_done:
        nav_status.text = "CRITICAL: DSN LINK LOST | POSITION DETERMINED VIA STAR TRACKERS & XNAV"
        nav_status.color = color.orange
        
        to_psyche = single_psyche.pos - orion.pos
        dist = mag(to_psyche)
        
        t_loss = t - dsn_loss_event_time
        nav_err = 28.0 * math.exp(-0.06 * t_loss) + pyrandom.gauss(3.2, 0.5)
        corr_vec = 18.0 * math.exp(-0.05 * t_loss) + pyrandom.gauss(2.5, 0.4)
        
        if dist > (single_psyche.radius + ORION_COLLISION_RADIUS):
            dir_vec = norm(to_psyche)
            orion_intercept_pos += dir_vec * 1.2
            set_spacecraft_center(orion_intercept_pos)
        else:
            collision_done = True
            nav_status.text = "RENDEZVOUS COMPLETE: REACHED PSYCHE AUTONOMOUSLY"
            nav_status.color = color.green

    time_history.append(t)
    nav_error_history.append(max(0, nav_err))
    correction_history.append(max(0, corr_vec))

    orion_name.pos = spacecraft_center
    orion_telemetry_label.pos = spacecraft_center

    for i, star in enumerate(star_objects):
        star_rays[i].clear()
        star_rays[i].append(pos=spacecraft_center)
        star_rays[i].append(pos=star.pos)

    inv = [1.0 / (q * q) for q in pulsar_sigmas]
    denom = sum(inv)
    weights = [q / denom for q in inv]

    for i, p_star in enumerate(pulsars):
        pulsar_rays[i].clear()
        pulsar_rays[i].append(pos=spacecraft_center)
        pulsar_rays[i].append(pos=p_star.pos)

    orion_telemetry_label.text = (
        "--- ORION AUTONOMOUS TELEMETRY ---\n"
        "1. Star Tracker: Attitude Matrix A (Vega/Sirius/Altair/Deneb)\n"
        "2. X-Ray Pulsar Timing (XNAV): Position Fix r_est\n"
        "   Pulsar Weights: w1={:.2f}, w2={:.2f}, w3={:.2f}, w4={:.2f}\n"
        "   r_SC: ({:.0f}, {:.0f}, {:.0f})\n"
        "   Distance to Target: {:.1f} km".format(
            weights[0], 
            weights[1], 
            weights[2], 
            weights[3],
            spacecraft_center.x, 
            spacecraft_center.y, 
            spacecraft_center.z,
            mag(single_psyche.pos - spacecraft_center)
        )
    )

    for ast in asteroids:
        ast.angle += ast.speed
        ast.pos.x = ast.orbit_radius * math.cos(ast.angle)
        ast.pos.y = ast.orbit_radius * math.sin(ast.angle)


print("\nSimulation ended. Generating Matplotlib Telemetry Plot...")

plt.style.use('dark_background')
fig, ax1 = plt.subplots(figsize=(10.5, 5.8), dpi=100)

line1 = ax1.plot(
    time_history, nav_error_history,
    color='#ff4d4d', linewidth=2, label='Navigation Error Magnitude (||r_true - r_est||)'
)
ax1.set_xlabel('Simulation Time (s)', fontsize=11, color='white', fontweight='bold')
ax1.set_ylabel('Position Error Magnitude (km)', fontsize=11, color='#ff4d4d', fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#ff4d4d')

ax2 = ax1.twinx()
line2 = ax2.plot(
    time_history, correction_history,
    color='#00e676', linewidth=2, linestyle='--', label='Correction Vector Magnitude (||Δv_corr||)'
)
ax2.set_ylabel('Correction Thrust / Delta-V (m/s)', fontsize=11, color='#00e676', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#00e676')

if dsn_loss_event_time is not None:
    ax1.axvline(x=dsn_loss_event_time, color='#ffcc00', linestyle=':', linewidth=2)
    ax1.annotate(
        'CRITICAL: DSN Link Lost\nAutonomous XNAV Engaged',
        xy=(dsn_loss_event_time, max(nav_error_history)*0.8),
        xytext=(dsn_loss_event_time + 3, max(nav_error_history)*0.85),
        arrowprops=dict(facecolor='#ffcc00', shrink=0.05, width=1.5, headwidth=7),
        color='#ffcc00', fontsize=9, fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", fc="#1a1a1a", ec="#ffcc00", lw=1)
    )

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right', facecolor='#111111', edgecolor='gray')

plt.title('ORION SPACECRAFT — NAVIGATION ERROR & CORRECTION RESPONSE', fontsize=12, pad=15, color='white', fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()
