import json

import streamlit as st
import streamlit.components.v1 as components

from backend import engine, storage, ui
from backend.indicators import HAZARD_ACTIONS, INDICATORS, REGIONS

env, day = st.session_state.env, st.session_state.day
df = storage.history(env, day)
cur = df.iloc[-1]
rs = engine.region_status(df)

st.title("3D body map")
st.caption("Drag to rotate, scroll to zoom. Pick a body area below to highlight it. The heart beats at your heart rate.")

region = st.radio("Body area", list(REGIONS), format_func=lambda r: REGIONS[r]["title"], horizontal=True)

PAGE = """
<div id="v" style="width:100%;height:520px"></div>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
const D = __DATA__;
const box = document.getElementById('v');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(40, box.clientWidth / box.clientHeight, 0.1, 100);
camera.position.set(0, 1.4, 8);
const renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(box.clientWidth, box.clientHeight);
box.appendChild(renderer.domElement);
scene.add(new THREE.HemisphereLight(0xbcd6ff, 0x14213a, 1.1));
const sun = new THREE.DirectionalLight(0xffffff, 1.3); sun.position.set(3, 5, 5); scene.add(sun);
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1, 0); controls.enablePan = false; controls.enableDamping = true;
controls.autoRotate = true; controls.autoRotateSpeed = 0.8;

const shellMat = new THREE.MeshPhysicalMaterial({color: D.colors.body, transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide});
function shell(geo, x, y, z, rz) { const m = new THREE.Mesh(geo, shellMat); m.position.set(x, y, z); m.rotation.z = rz || 0; scene.add(m); }
shell(new THREE.SphereGeometry(0.55, 32, 24), 0, 2.75, 0);
shell(new THREE.CylinderGeometry(0.62, 0.55, 1.5, 32), 0, 1.7, 0);
shell(new THREE.CylinderGeometry(0.55, 0.5, 1.2, 32), 0, 0.55, 0);
[-1, 1].forEach(s => {
  shell(new THREE.CylinderGeometry(0.17, 0.14, 1.6, 16), s * 0.95, 1.5, 0, -s * 0.12);
  shell(new THREE.CylinderGeometry(0.25, 0.18, 2.2, 16), s * 0.3, -1.2, 0);
});

const organs = {};
function organ(geo, region, x, y, z, sx, sy, sz) {
  const c = D.colors[region];
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({color: c, emissive: c, emissiveIntensity: 0.35, roughness: 0.4}));
  m.position.set(x, y, z); m.scale.set(sx || 1, sy || 1, sz || 1); scene.add(m);
  (organs[region] = organs[region] || []).push(m);
  return m;
}
organ(new THREE.SphereGeometry(0.38, 32, 24), 'brain', 0, 2.8, 0, 1, 0.85, 1.05);
const heart = organ(new THREE.SphereGeometry(0.26, 32, 24), 'heart', 0.14, 1.85, 0.12, 1, 1.15, 0.9);
organ(new THREE.TorusKnotGeometry(0.2, 0.07, 80, 10, 2, 3), 'gut', 0, 0.55, 0.05);
for (let i = 0; i < 12; i++) organ(new THREE.CylinderGeometry(0.07, 0.07, 0.1, 12), 'bone', 0, 2.15 - i * 0.17, -0.2);
[-1, 1].forEach(s => {
  organ(new THREE.CylinderGeometry(0.07, 0.06, 2.0, 12), 'bone', s * 0.3, -1.2, 0);
  organ(new THREE.CylinderGeometry(0.06, 0.05, 1.0, 12), 'bone', s * 0.95, 1.5, 0).rotation.z = -s * 0.12;
});

const clock = new THREE.Clock();
(function loop() {
  requestAnimationFrame(loop);
  const t = clock.getElapsedTime();
  const beat = (t * D.hr / 60) % 1, p = Math.pow(Math.max(0, Math.sin(beat * Math.PI * 2)), 6);
  heart.scale.set(1 + 0.14 * p, 1.15 + 0.16 * p, 0.9 + 0.14 * p);
  for (const r in organs) organs[r].forEach(m => { m.material.emissiveIntensity = (r === D.selected) ? 0.6 + 0.4 * Math.sin(t * 4) : 0.35; });
  shellMat.opacity = D.selected === 'body' ? 0.24 + 0.1 * Math.sin(t * 4) : 0.16;
  controls.update();
  renderer.render(scene, camera);
})();
</script>
"""

data = {"colors": {r: ui.COLORS[s] for r, s in rs.items()}, "selected": region, "hr": float(cur["hr"])}
components.html(PAGE.replace("__DATA__", json.dumps(data)), height=540)

# ---- details for the selected area ----
info = REGIONS[region]
st.subheader(info["title"])
st.markdown(ui.badge(rs[region]), unsafe_allow_html=True)
st.write(info["info"])
for key in info["indicators"]:
    ind = INDICATORS[key]
    s = engine.status_of(key, cur[key])
    a, b, c = st.columns([3, 2, 2])
    a.markdown(f"**{ind['name']}**")
    b.markdown(f"{float(cur[key]):g} {ind['unit']}")
    c.markdown(ui.badge(s), unsafe_allow_html=True)
    st.caption(f"Normal: {ind['normal'][0]} to {ind['normal'][1]}. {ind['why']}")
st.markdown("**What to do**")
for tip in HAZARD_ACTIONS[info["hazard"]]:
    st.write(f"- {tip}")
