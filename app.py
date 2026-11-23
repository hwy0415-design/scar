import json
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# 1. 데이터 구조: 냉각수와 레이싱 섹터를 리스트로 저장
# =========================================================

coolant_list = [
    "물-에틸렌글리콜",
    "절연 냉각유",
    "액체 질소"
]

track_sectors = [
    {"name": "SECTOR 1", "type": "직선 코스"},
    {"name": "SECTOR 2", "type": "커브 코스"},
    {"name": "SECTOR 3", "type": "울퉁불퉁한 코스"}
]


# =========================================================
# 2. 함수(def): 냉각수 설정에 따른 냉각 효율 계산
# =========================================================

def simulate_race(coolant, flow_rate, battery_output):
    # if-elif-else: 선택한 냉각수에 따라 가상 냉각 효율 결정
    if coolant == "물-에틸렌글리콜":
        cooling_efficiency = 1.0
    elif coolant == "절연 냉각유":
        cooling_efficiency = 0.9
    elif coolant == "액체 질소":
        cooling_efficiency = 1.2
    else:
        cooling_efficiency = 0.0

    # 교육용 게임 모델의 시작 온도 계산
    initial_temperature = (
        38
        + (battery_output - 50) * 0.22
        - (flow_rate - 1) * 0.75 * cooling_efficiency
    )

    # if-elif-else: 배터리 온도 상태 분류
    if initial_temperature < 40:
        temperature_status = "과냉각"
    elif initial_temperature <= 80:
        temperature_status = "적합"
    else:
        temperature_status = "과열"

    return initial_temperature, temperature_status, cooling_efficiency


# =========================================================
# 3. Streamlit 페이지 설정
# =========================================================

st.set_page_config(
    page_title="THERMAL RUSH",
    page_icon="🏎️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #070d19 0%, #101b32 100%);
    color: #f4f8ff;
}
h1, h2, h3 {
    color: #55d9ff !important;
}
div[data-testid="stMetric"] {
    background: #14243b;
    border: 1px solid #294d70;
    border-radius: 12px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. 게임 제목과 안내
# =========================================================

st.title("🏎️ THERMAL RUSH")
st.subheader("F1 HYPERCAR BATTERY COOLING RACE")
st.write(
    "냉각 시스템을 직접 설정하고 세 가지 특수 트랙을 주행하세요. "
    "빠른 기록뿐 아니라 배터리 온도 관리도 중요합니다."
)


# =========================================================
# 5. 냉각 시스템 설정
# =========================================================

st.markdown("### ⚙️ 배터리 냉각 시스템 설정")

setting_col1, setting_col2, setting_col3 = st.columns(3)

with setting_col1:
    coolant = st.selectbox("냉각수 종류", coolant_list)

with setting_col2:
    flow_rate = st.slider(
        "냉각수 유량 (L/min)",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.5
    )

with setting_col3:
    battery_output = st.slider(
        "배터리 출력 (%)",
        min_value=50,
        max_value=100,
        value=75,
        step=5
    )


# =========================================================
# 6. 설정값을 바탕으로 초기 냉각 상태 계산
# =========================================================

initial_temperature, initial_status, cooling_efficiency = simulate_race(
    coolant,
    flow_rate,
    battery_output
)

st.markdown("### 📊 선택한 냉각 시스템")

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("냉각수", coolant)
metric_col2.metric("예상 초기 온도", f"{initial_temperature:.1f} ℃")
metric_col3.metric("초기 배터리 상태", initial_status)

st.caption(
    "※ 냉각 효율과 온도 변화는 실제 F1 차량의 실험값이 아닌 "
    "게임 진행을 위한 교육용 가상 모델입니다."
)


# =========================================================
# 7. for 반복문: 섹터 목록을 게임 데이터로 변환
# =========================================================

sector_data = []

# for 반복문으로 각 섹터의 번호, 이름, 코스 유형을 차례로 저장
for sector_number, sector_info in enumerate(track_sectors):
    sector_data.append({
        "number": sector_number + 1,
        "name": sector_info["name"],
        "type": sector_info["type"]
    })


# =========================================================
# 8. Python 설정을 JavaScript 게임에 전달
# =========================================================

game_config = {
    "coolant": coolant,
    "flow_rate": flow_rate,
    "battery_output": battery_output,
    "initial_temperature": initial_temperature,
    "cooling_efficiency": cooling_efficiency,
    "track_sectors": sector_data
}


# =========================================================
# 9. 레이싱 게임: HTML / CSS / JavaScript
# =========================================================

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    padding: 10px;
    color: #f4f8ff;
    background: #080e1b;
    font-family: Arial, "Malgun Gothic", sans-serif;
}

.game_shell {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 14px;
    background: linear-gradient(145deg, #111e34, #091321);
    border: 1px solid #285078;
    border-radius: 18px;
    box-shadow: 0 15px 45px rgba(0,0,0,.35);
}

.top_line {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}

.game_logo {
    color: #59ddff;
    font-size: 23px;
    font-weight: 900;
    letter-spacing: 2px;
}

.track_badge {
    color: #d7f7ff;
    background: #173752;
    border: 1px solid #31799a;
    border-radius: 20px;
    padding: 7px 13px;
    font-size: 12px;
    font-weight: bold;
}

.hud {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 8px;
    margin-bottom: 10px;
}

.hud_card {
    min-width: 0;
    padding: 9px 5px;
    text-align: center;
    background: #172942;
    border: 1px solid #294968;
    border-radius: 10px;
}

.hud_label {
    color: #9bb8d2;
    font-size: 10px;
    letter-spacing: 1px;
}

.hud_value {
    margin-top: 5px;
    color: #5cddff;
    font-size: clamp(15px, 2.4vw, 22px);
    font-weight: 900;
}

.canvas_wrap {
    position: relative;
    overflow: hidden;
    border: 2px solid #3ba8d1;
    border-radius: 13px;
    background: #101c2b;
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    aspect-ratio: 1000 / 620;
    outline: none;
}

.bottom_info {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 10px;
    padding: 11px 13px;
    color: #c5d8e9;
    background: #172942;
    border-radius: 10px;
    font-size: 12px;
    line-height: 1.7;
}

.key {
    display: inline-block;
    padding: 2px 6px;
    margin: 1px;
    color: #071321;
    background: #65dcff;
    border-radius: 4px;
    font-weight: bold;
}

button {
    border: 0;
    border-radius: 9px;
    padding: 12px 24px;
    color: #06111e;
    background: linear-gradient(90deg, #49d7ff, #8af0ff);
    font-weight: 900;
    font-size: 15px;
    cursor: pointer;
    box-shadow: 0 5px 18px rgba(44, 194, 239, .22);
}

button:hover { filter: brightness(1.12); transform: translateY(-1px); }

.overlay {
    position: absolute;
    inset: 0;
    z-index: 5;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 22px;
    text-align: center;
    background: rgba(4, 10, 20, .78);
    backdrop-filter: blur(5px);
}

.overlay h2 {
    margin: 0 0 8px;
    color: #65e4ff;
    font-size: clamp(25px, 5vw, 46px);
    letter-spacing: 3px;
    text-shadow: 0 0 22px rgba(62, 207, 255, .45);
}

.overlay p {
    max-width: 620px;
    color: #d6e7f5;
    line-height: 1.8;
    font-size: 13px;
}

.result_overlay {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 10;
    overflow-y: auto;
    align-items: center;
    justify-content: center;
    padding: 16px;
    background: rgba(2, 7, 17, .88);
    backdrop-filter: blur(8px);
}

.result_panel {
    width: min(600px, 96%);
    padding: 22px;
    text-align: center;
    background: linear-gradient(145deg, #172b47, #0b1729);
    border: 2px solid #3c9cc3;
    border-radius: 18px;
    box-shadow: 0 0 45px rgba(35, 177, 225, .22);
}

.result_kicker {
    color: #91c9e5;
    font-size: 12px;
    letter-spacing: 3px;
    font-weight: bold;
}

.result_grade {
    margin: 4px 0;
    color: #ffe17b;
    font-size: clamp(54px, 10vw, 82px);
    line-height: 1.1;
    font-weight: 1000;
    text-shadow: 0 0 28px rgba(255, 211, 86, .25);
}

.result_status {
    margin: 8px 0 3px;
    color: #71e7ff;
    font-size: clamp(27px, 5vw, 39px);
    font-weight: 900;
}

.result_temp {
    color: white;
    font-size: clamp(30px, 6vw, 45px);
    font-weight: 900;
}

.result_description {
    color: #bdd0e1;
    font-size: 12px;
    margin: 7px 0 14px;
}

.result_stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin: 14px 0;
}

.result_stat {
    padding: 10px;
    background: #1c3553;
    border: 1px solid #315777;
    border-radius: 9px;
}

.result_stat span {
    display: block;
    color: #9bb8d2;
    font-size: 11px;
}

.result_stat strong {
    display: block;
    margin-top: 4px;
    color: white;
    font-size: 20px;
}

.sector_results {
    margin: 12px 0;
    text-align: left;
    color: #d9e8f5;
    font-size: 12px;
    line-height: 1.8;
}

.sector_result_row {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    padding: 6px 2px;
    border-bottom: 1px solid #2b4966;
}

@media (max-width: 600px) {
    .hud { grid-template-columns: repeat(3, 1fr); }
    .game_shell { padding: 8px; }
    .bottom_info { font-size: 11px; }
}
</style>
</head>

<body>
<div class="game_shell">

    <div class="top_line">
        <div class="game_logo">THERMAL RUSH</div>
        <div class="track_badge" id="background_name">TRACK LOADING</div>
    </div>

    <div class="hud">
        <div class="hud_card">
            <div class="hud_label">SPEED</div>
            <div class="hud_value" id="speed_value">0</div>
        </div>
        <div class="hud_card">
            <div class="hud_label">BATTERY TEMP</div>
            <div class="hud_value" id="temp_value">0℃</div>
        </div>
        <div class="hud_card">
            <div class="hud_label">RACE TIME</div>
            <div class="hud_value" id="time_value">0.0s</div>
        </div>
        <div class="hud_card">
            <div class="hud_label">SECTOR</div>
            <div class="hud_value" id="sector_value">1 / 3</div>
        </div>
        <div class="hud_card">
            <div class="hud_label">NITRO</div>
            <div class="hud_value" id="nitro_value">READY</div>
        </div>
    </div>

    <div class="canvas_wrap">
        <canvas id="race_canvas" width="1000" height="620" tabindex="0"></canvas>

        <div class="overlay" id="start_overlay">
            <h2>THERMAL RUSH</h2>
            <p>
                직선 · 커브 · 험로를 통과하고 배터리 온도를 관리하세요.<br>
                매 경기마다 배경 테마가 무작위로 선택됩니다.
            </p>
            <p>
                <b>W / ↑</b> 가속 &nbsp; <b>S / ↓</b> 감속<br>
                <b>A / ←</b> 왼쪽 &nbsp; <b>D / →</b> 오른쪽<br>
                <b>SHIFT</b> 드리프트 &nbsp; <b>SPACE</b> 니트로
            </p>
            <button id="start_button">START RACE</button>
        </div>

        <div class="result_overlay" id="result_overlay">
            <div class="result_panel">
                <div class="result_kicker" id="result_kicker">RACE COMPLETE</div>
                <div class="result_grade" id="result_grade">S</div>
                <div class="result_status" id="result_status">적합</div>
                <div class="result_temp" id="result_temp">65.0℃</div>
                <div class="result_description" id="result_description">
                    배터리 온도 상태와 주행 기록
                </div>
                <div class="result_stats">
                    <div class="result_stat">
                        <span>완주 시간</span>
                        <strong id="result_time">0.0초</strong>
                    </div>
                    <div class="result_stat">
                        <span>선택 냉각수</span>
                        <strong id="result_coolant">-</strong>
                    </div>
                </div>
                <div class="sector_results" id="sector_results"></div>
                <button id="restart_button">RACE AGAIN</button>
            </div>
        </div>
    </div>

    <div class="bottom_info">
        <div>
            <b>CONTROL</b><br>
            <span class="key">W</span>/<span class="key">↑</span> 가속
            <span class="key">S</span>/<span class="key">↓</span> 감속
            <span class="key">A</span>/<span class="key">D</span> 조향
            <span class="key">SHIFT</span> 드리프트
            <span class="key">SPACE</span> 니트로
        </div>
        <div id="game_message">START RACE를 눌러 게임을 시작하세요.</div>
    </div>

</div>

<script>
const game_config = __CONFIG__;

const canvas = document.getElementById("race_canvas");
const ctx = canvas.getContext("2d");

const canvas_width = canvas.width;
const canvas_height = canvas.height;
const horizon_y = 205;
const road_base_width = 760;
const sector_length = 1050;
const total_distance = sector_length * 3;

const background_themes = [
    {
        name: "NEON CITY",
        sky_top: "#101a3c",
        sky_bottom: "#bd4b78",
        ground: "#172b35",
        mountain: "#273653",
        accent: "#36dfff"
    },
    {
        name: "DESERT RUN",
        sky_top: "#472c48",
        sky_bottom: "#f0a45c",
        ground: "#80543c",
        mountain: "#bd7951",
        accent: "#ffe08a"
    },
    {
        name: "ALPINE CIRCUIT",
        sky_top: "#173b60",
        sky_bottom: "#a9d5e4",
        ground: "#244c43",
        mountain: "#d6e6ed",
        accent: "#9ff3ff"
    },
    {
        name: "COASTAL NIGHT",
        sky_top: "#061b32",
        sky_bottom: "#236c83",
        ground: "#123d43",
        mountain: "#164b5d",
        accent: "#61ffe0"
    }
];

let selected_theme = background_themes[
    Math.floor(Math.random() * background_themes.length)
];

let race_running = false;
let race_finished = false;
let last_frame_time = 0;
let race_time = 0;
let distance_travelled = 0;
let car_speed = 0;
let player_position = 0;
let steering_velocity = 0;
let car_tilt = 0;
let battery_temp = game_config.initial_temperature;
let nitro_remaining = 1;
let nitro_active_time = 0;
let camera_shake = 0;
let road_curve = 0;
let sector_records = [];
let current_sector = 0;
let current_sector_start_time = 0;
let keys = {};

const speed_value = document.getElementById("speed_value");
const temp_value = document.getElementById("temp_value");
const time_value = document.getElementById("time_value");
const sector_value = document.getElementById("sector_value");
const nitro_value = document.getElementById("nitro_value");
const game_message = document.getElementById("game_message");
const start_overlay = document.getElementById("start_overlay");
const result_overlay = document.getElementById("result_overlay");

function choose_random_theme() {
    selected_theme = background_themes[
        Math.floor(Math.random() * background_themes.length)
    ];
    document.getElementById("background_name").textContent =
        selected_theme.name;
}

function get_sector_index(world_distance) {
    return Math.min(
        2,
        Math.floor(Math.max(0, world_distance) / sector_length)
    );
}

function get_track_shape(world_distance) {
    const sector_index = get_sector_index(world_distance);
    const local_distance = world_distance - sector_index * sector_length;

    if (sector_index === 0) {
        return {curve: 0, bump: 0, label: "직선 코스"};
    } else if (sector_index === 1) {
        const curve_value = Math.sin(local_distance / sector_length * Math.PI * 2);
        return {curve: curve_value * 0.95, bump: 0, label: "커브 코스"};
    } else {
        const bump_value =
            Math.sin(local_distance * 0.055) * 0.65 +
            Math.sin(local_distance * 0.12) * 0.28;
        return {curve: 0.12, bump: bump_value, label: "울퉁불퉁한 코스"};
    }
}

function draw_background() {
    const sky_gradient = ctx.createLinearGradient(0, 0, 0, horizon_y);
    sky_gradient.addColorStop(0, selected_theme.sky_top);
    sky_gradient.addColorStop(1, selected_theme.sky_bottom);
    ctx.fillStyle = sky_gradient;
    ctx.fillRect(0, 0, canvas_width, horizon_y + 5);

    ctx.fillStyle = selected_theme.mountain;
    ctx.beginPath();
    ctx.moveTo(0, horizon_y);
    for (let x_pos = 0; x_pos <= canvas_width; x_pos += 80) {
        const peak = 90 + Math.abs(Math.sin(x_pos * 0.013)) * 90;
        ctx.lineTo(x_pos, peak);
    }
    ctx.lineTo(canvas_width, horizon_y);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = selected_theme.ground;
    ctx.fillRect(0, horizon_y, canvas_width, canvas_height - horizon_y);

    // 배경 테마에 따라 장식물의 색과 모양을 바꿔 깊이감을 표현
    for (let scenery_index = 0; scenery_index < 12; scenery_index++) {
        const scenery_x = (scenery_index * 103 + 35) % canvas_width;
        const scenery_y = horizon_y + 12 + (scenery_index % 3) * 9;
        ctx.fillStyle = selected_theme.accent;
        ctx.globalAlpha = 0.22;
        ctx.fillRect(scenery_x, scenery_y, 3, 30 + scenery_index % 4 * 8);
    }
    ctx.globalAlpha = 1;
}

function get_road_center(world_distance, depth) {
    const shape = get_track_shape(world_distance);
    const curve_shift = shape.curve * depth * depth * 175;
    const wave_shift = Math.sin(world_distance * 0.0015) * depth * 18;
    return canvas_width / 2 - curve_shift - wave_shift;
}

function draw_road() {
    const slice_count = 95;
    const visible_distance = 1900;

    for (let slice_index = 0; slice_index < slice_count; slice_index++) {
        const near_depth = slice_index / slice_count;
        const far_depth = (slice_index + 1) / slice_count;

        const near_y = horizon_y + Math.pow(near_depth, 1.72) * (canvas_height - horizon_y);
        const far_y = horizon_y + Math.pow(far_depth, 1.72) * (canvas_height - horizon_y);

        const near_world = distance_travelled + (1 - near_depth) * visible_distance;
        const far_world = distance_travelled + (1 - far_depth) * visible_distance;

        const near_shape = get_track_shape(near_world);
        const far_shape = get_track_shape(far_world);

        const near_width = 55 + near_depth * road_base_width / 2;
        const far_width = 55 + far_depth * road_base_width / 2;

        const near_center = get_road_center(near_world, near_depth);
        const far_center = get_road_center(far_world, far_depth);

        const stripe = Math.floor(near_world / 90) % 2;
        const road_color = stripe ? "#343b48" : "#2c3441";
        const rumble_color = stripe ? "#f4f4f4" : "#e14f59";

        // 도로 바깥의 색상 띠
        ctx.fillStyle = rumble_color;
        ctx.beginPath();
        ctx.moveTo(near_center - near_width - 18 * near_depth, near_y);
        ctx.lineTo(near_center + near_width + 18 * near_depth, near_y);
        ctx.lineTo(far_center + far_width + 18 * far_depth, far_y);
        ctx.lineTo(far_center - far_width - 18 * far_depth, far_y);
        ctx.closePath();
        ctx.fill();

        // 도로 표면
        ctx.fillStyle = road_color;
        ctx.beginPath();
        ctx.moveTo(near_center - near_width, near_y);
        ctx.lineTo(near_center + near_width, near_y);
        ctx.lineTo(far_center + far_width, far_y);
        ctx.lineTo(far_center - far_width, far_y);
        ctx.closePath();
        ctx.fill();

        // 도로 중앙의 점선
        if (Math.floor(near_world / 125) % 2 === 0) {
            ctx.strokeStyle = "rgba(235,245,255,.58)";
            ctx.lineWidth = 2 + near_depth * 2;
            ctx.beginPath();
            ctx.moveTo(near_center, near_y);
            ctx.lineTo(far_center, far_y);
            ctx.stroke();
        }

        // Sector 3의 울퉁불퉁한 도로에 요철 표시
        if (near_shape.bump !== 0 && near_depth > 0.38) {
            const bump_y = near_y - near_shape.bump * near_depth * 10;
            ctx.strokeStyle = "rgba(255,220,135,.7)";
            ctx.lineWidth = 2 + near_depth * 2;
            ctx.beginPath();
            ctx.moveTo(near_center - near_width * 0.7, bump_y);
            ctx.lineTo(near_center + near_width * 0.7, bump_y);
            ctx.stroke();
        }
    }
}

function draw_track_sign() {
    const sector_index = get_sector_index(distance_travelled);
    const sector_info = game_config.track_sectors[sector_index];

    ctx.fillStyle = "rgba(5,12,24,.68)";
    ctx.fillRect(18, 18, 245, 62);

    ctx.fillStyle = "#69e4ff";
    ctx.font = "bold 18px Arial";
    ctx.fillText(sector_info.name, 32, 43);

    ctx.fillStyle = "#ffffff";
    ctx.font = "14px Arial";
    ctx.fillText(sector_info.type, 32, 65);
}

function draw_car() {
    const car_x = canvas_width / 2 + player_position * 270;
    const car_y = canvas_height - 105 + camera_shake * 0.4;

    ctx.save();
    ctx.translate(car_x, car_y);
    ctx.rotate(car_tilt);

    // 바닥 그림자
    ctx.fillStyle = "rgba(0,0,0,.38)";
    ctx.beginPath();
    ctx.ellipse(0, 15, 58, 19, 0, 0, Math.PI * 2);
    ctx.fill();

    // 차체를 다각형으로 그려 입체적인 레이싱카 형태 표현
    ctx.fillStyle = "#04bfe9";
    ctx.beginPath();
    ctx.moveTo(-17, 37);
    ctx.lineTo(-29, 8);
    ctx.lineTo(-24, -25);
    ctx.lineTo(-13, -42);
    ctx.lineTo(13, -42);
    ctx.lineTo(24, -25);
    ctx.lineTo(29, 8);
    ctx.lineTo(17, 37);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = "#e8faff";
    ctx.beginPath();
    ctx.moveTo(-12, -19);
    ctx.lineTo(-8, -34);
    ctx.lineTo(8, -34);
    ctx.lineTo(12, -19);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = "#10243a";
    ctx.fillRect(-10, -12, 20, 19);

    ctx.fillStyle = "#07101c";
    ctx.fillRect(-34, -20, 9, 22);
    ctx.fillRect(25, -20, 9, 22);
    ctx.fillRect(-29, 20, 8, 16);
    ctx.fillRect(21, 20, 8, 16);

    ctx.fillStyle = "#ffefaa";
    ctx.fillRect(-18, 31, 9, 5);
    ctx.fillRect(9, 31, 9, 5);

    // 니트로 사용 시 배기 불꽃
    if (nitro_active_time > 0) {
        ctx.fillStyle = "#ff9d3c";
        ctx.beginPath();
        ctx.moveTo(-10, 38);
        ctx.lineTo(-5, 65 + Math.random() * 12);
        ctx.lineTo(0, 38);
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(5, 38);
        ctx.lineTo(10, 62 + Math.random() * 10);
        ctx.lineTo(15, 38);
        ctx.fill();
    }

    ctx.restore();
}

function draw_speed_effect() {
    if (car_speed < 90) return;

    ctx.strokeStyle = "rgba(190,235,255,.16)";
    ctx.lineWidth = 2;

    for (let effect_index = 0; effect_index < 13; effect_index++) {
        const effect_x = (effect_index * 89 + race_time * 170) % canvas_width;
        const effect_y = (effect_index * 47 + race_time * 250) % canvas_height;
        ctx.beginPath();
        ctx.moveTo(effect_x, effect_y);
        ctx.lineTo(effect_x, effect_y + 18 + car_speed * 0.12);
        ctx.stroke();
    }
}

function draw_game() {
    ctx.save();

    if (camera_shake > 0) {
        ctx.translate(
            (Math.random() - 0.5) * camera_shake,
            (Math.random() - 0.5) * camera_shake
        );
    }

    draw_background();
    draw_road();
    draw_speed_effect();
    draw_track_sign();
    draw_car();

    ctx.restore();
}

function update_hud() {
    speed_value.textContent = Math.round(car_speed * 1.35) + " km/h";
    temp_value.textContent = battery_temp.toFixed(1) + "℃";
    time_value.textContent = race_time.toFixed(1) + "s";

    const sector_index = get_sector_index(distance_travelled);
    sector_value.textContent = (sector_index + 1) + " / 3";

    nitro_value.textContent = nitro_remaining > 0 ? "READY" : "USED";

    if (battery_temp < 40) {
        temp_value.style.color = "#78bdff";
    } else if (battery_temp <= 80) {
        temp_value.style.color = "#5ce5a0";
    } else {
        temp_value.style.color = "#ff626c";
    }
}

function save_sector_record(sector_index) {
    const sector_info = game_config.track_sectors[sector_index];

    sector_records.push({
        name: sector_info.name,
        type: sector_info.type,
        time: (race_time - current_sector_start_time).toFixed(2),
        temperature: battery_temp.toFixed(1)
    });

    current_sector_start_time = race_time;
}

function classify_temperature() {
    // 요청한 온도 기준을 그대로 적용
    if (battery_temp < 40) {
        return "과냉각";
    } else if (battery_temp <= 80) {
        return "적합";
    } else {
        return "과열";
    }
}

function calculate_grade() {
    // 완주 시간 기준: S 32초 이하, A 42초 이하, 그 외 B
    if (race_time <= 32) {
        return "S";
    } else if (race_time <= 42) {
        return "A";
    } else {
        return "B";
    }
}

function finish_race(overheated) {
    if (race_finished) return;

    race_finished = true;
    race_running = false;

    const temperature_status = classify_temperature();
    const grade = overheated ? "FAIL" : calculate_grade();
    const result_title = overheated ? "BATTERY OVERHEAT" : "RACE COMPLETE";

    document.getElementById("result_kicker").textContent = result_title;
    document.getElementById("result_grade").textContent = grade;
    document.getElementById("result_status").textContent = temperature_status;
    document.getElementById("result_temp").textContent =
        battery_temp.toFixed(1) + "℃";
    document.getElementById("result_time").textContent =
        race_time.toFixed(2) + "초";
    document.getElementById("result_coolant").textContent =
        game_config.coolant;

    let description = "";
    if (temperature_status === "과냉각") {
        description = "배터리 온도가 기준보다 낮습니다. 냉각 조건을 다시 조정해 보세요.";
    } else if (temperature_status === "적합") {
        description = "배터리 온도가 적정 범위에 있습니다. 냉각 시스템 관리 성공!";
    } else {
        description = "배터리 온도가 기준을 초과했습니다. 냉각 성능을 높여 보세요.";
    }

    if (overheated) {
        description = "배터리 온도가 100℃를 넘어 레이스가 중단되었습니다.";
    }

    document.getElementById("result_description").textContent = description;

    let sector_html = "";
    for (let record_index = 0; record_index < sector_records.length; record_index++) {
        const record = sector_records[record_index];
        sector_html +=
            '<div class="sector_result_row">' +
            '<span><b>' + record.name + '</b> · ' + record.type +
            '<br>온도 ' + record.temperature + '℃</span>' +
            '<b>' + record.time + '초</b></div>';
    }

    document.getElementById("sector_results").innerHTML = sector_html;
    result_overlay.style.display = "flex";
    game_message.textContent = "레이스 종료 — 결과를 확인하세요.";
}

function update_physics(delta_time) {
    const accelerate = keys["w"] || keys["arrowup"];
    const brake = keys["s"] || keys["arrowdown"];
    const steer_left = keys["a"] || keys["arrowleft"];
    const steer_right = keys["d"] || keys["arrowright"];
    const drift_pressed = keys["shift"];

    // 가속과 감속을 즉시 바꾸지 않고 관성으로 부드럽게 변화
    const target_acceleration = accelerate ? 92 : 0;
    car_speed += (target_acceleration - (car_speed > 0 ? 12 : 0)) * delta_time;

    if (brake) {
        car_speed -= 115 * delta_time;
    }

    if (keys[" "] && nitro_remaining > 0 && nitro_active_time <= 0) {
        nitro_active_time = 1.7;
        nitro_remaining = 0;
    }

    if (nitro_active_time > 0) {
        car_speed += 65 * delta_time;
        nitro_active_time -= delta_time;
    }

    car_speed = Math.max(0, Math.min(175, car_speed));

    // 조향 입력도 즉시 이동시키지 않고 속도를 서서히 변화시킴
    let steering_input = 0;
    if (steer_left) steering_input -= 1;
    if (steer_right) steering_input += 1;

    const steering_response = drift_pressed ? 3.8 : 2.7;
    steering_velocity += (
        steering_input * steering_response - steering_velocity * 2.2
    ) * delta_time;

    const speed_factor = 0.35 + car_speed / 175 * 0.85;
    player_position += steering_velocity * speed_factor * delta_time;
    player_position = Math.max(-1.15, Math.min(1.15, player_position));

    // 커브 구간에서는 도로가 휘는 방향에 맞춰 차량의 기울기를 계산
    const current_shape = get_track_shape(distance_travelled);
    road_curve += (current_shape.curve - road_curve) * Math.min(1, delta_time * 2.5);

    const target_tilt = -steering_velocity * 0.13 - road_curve * 0.12;
    car_tilt += (target_tilt - car_tilt) * Math.min(1, delta_time * 5);

    // 트랙 바깥으로 나가면 속도가 줄어듦
    if (Math.abs(player_position) > 0.88) {
        car_speed = Math.max(25, car_speed - 48 * delta_time);
        game_message.textContent = "TRACK LIMIT! 도로 안쪽으로 복귀하세요.";
    } else if (drift_pressed && Math.abs(steering_velocity) > 0.2) {
        game_message.textContent = "DRIFTING!";
    } else if (nitro_active_time > 0) {
        game_message.textContent = "NITRO BOOST!";
    } else {
        game_message.textContent = "안정적으로 주행 중입니다.";
    }

    // 주행 거리 계산
    distance_travelled += car_speed * 0.75 * delta_time;
    race_time += delta_time;

    // 울퉁불퉁한 Sector 3에서 화면 진동과 차량 흔들림 적용
    const updated_shape = get_track_shape(distance_travelled);
    if (get_sector_index(distance_travelled) === 2) {
        camera_shake = Math.abs(updated_shape.bump) * Math.min(7, car_speed / 22);
        car_tilt += updated_shape.bump * 0.004;
    } else {
        camera_shake *= 0.85;
    }

    // 배터리 발열과 냉각의 단순화된 게임 모델
    const heat_rate =
        (game_config.battery_output / 100) *
        (0.65 + car_speed / 175 * 0.75);

    const cooling_rate =
        game_config.flow_rate *
        0.08 *
        game_config.cooling_efficiency;

    battery_temp += (heat_rate - cooling_rate) * delta_time;

    // 섹터 경계 통과 시 각 구간의 기록 저장
    const next_sector = get_sector_index(distance_travelled);
    if (next_sector > current_sector) {
        save_sector_record(current_sector);
        current_sector = next_sector;
    }

    if (battery_temp > 100) {
        finish_race(true);
        return;
    }

    if (distance_travelled >= total_distance) {
        // 마지막 섹터 기록도 누락되지 않도록 저장
        if (sector_records.length < 3) {
            save_sector_record(2);
        }
        finish_race(false);
    }
}

function game_loop(timestamp) {
    if (!race_running) return;

    if (last_frame_time === 0) {
        last_frame_time = timestamp;
    }

    const delta_time = Math.min((timestamp - last_frame_time) / 1000, 0.04);
    last_frame_time = timestamp;

    update_physics(delta_time);
    draw_game();
    update_hud();

    if (race_running) {
        requestAnimationFrame(game_loop);
    }
}

function start_race() {
    choose_random_theme();

    race_running = true;
    race_finished = false;
    last_frame_time = 0;

    race_time = 0;
    distance_travelled = 0;
    car_speed = 0;
    player_position = 0;
    steering_velocity = 0;
    car_tilt = 0;
    battery_temp = game_config.initial_temperature;
    nitro_remaining = 1;
    nitro_active_time = 0;
    camera_shake = 0;
    road_curve = 0;

    sector_records = [];
    current_sector = 0;
    current_sector_start_time = 0;
    keys = {};

    start_overlay.style.display = "none";
    result_overlay.style.display = "none";

    canvas.focus();
    draw_game();
    update_hud();

    game_message.textContent = "레이스 시작! 직선 코스를 통과하세요.";
    requestAnimationFrame(game_loop);
}

window.addEventListener("keydown", function(event) {
    const key_name = event.key.toLowerCase();

    if ([
        "arrowup", "arrowdown", "arrowleft", "arrowright", " "
    ].includes(key_name)) {
        event.preventDefault();
    }

    keys[key_name] = true;
});

window.addEventListener("keyup", function(event) {
    keys[event.key.toLowerCase()] = false;
});

window.addEventListener("blur", function() {
    for (const key_name in keys) {
        keys[key_name] = false;
    }
});

document.getElementById("start_button").addEventListener("click", start_race);
document.getElementById("restart_button").addEventListener("click", start_race);

choose_random_theme();
draw_game();
update_hud();
</script>
</body>
</html>
"""

game_html = game_html.replace(
    "__CONFIG__",
    json.dumps(game_config, ensure_ascii=False)
)

components.html(
    game_html,
    height=900,
    scrolling=False
)
