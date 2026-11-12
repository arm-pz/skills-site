/* The floor under each hero: a field of dots in perspective, like a build grid, that ripples
   out from under the agent session each time a line in the replayed run passes (orange) or fails
   (red). On the homepage it fills the dark stage; on other pages it sits in the hero and takes
   the page's own ground, light or dark. Loaded by motion.js only when WebGL is on; the page reads the same without it.
   `state` is written by motion.js: p (scroll 0..1), px/py (pointer), ox/oy (where the session
   sits, in normalized device coordinates) and ping (1 pass, -1 fail). */
import {
  BufferAttribute, BufferGeometry, Clock, Color, PerspectiveCamera, Plane,
  NormalBlending, Points, Raycaster, Scene, ShaderMaterial, Vector2, Vector3, Vector4, WebGLRenderer,
} from 'three';

const SLOTS = 6;
const FLOOR = -1.4;

const VERT = /* glsl */`
uniform float uTime;uniform float uPx;uniform float uDim;
uniform vec4 uRip[${SLOTS}];/* x,z origin; start time; sign (1 pass, -1 fail) */
varying float vGlow;varying float vBad;varying float vFog;varying float vBase;
void main(){
  vec3 p=position;
  float glow=0.,bad=0.;
  for(int i=0;i<${SLOTS};i++){
    vec4 r=uRip[i];
    float age=uTime-r.z;
    if(age<0.||age>6.)continue;
    float d=length(p.xz-r.xy),front=d-age*2.6;
    float w=exp(-front*front*1.6)*exp(-age*.55)*smoothstep(0.,.25,age);
    p.y+=sin(front*4.)*w*.22;
    glow+=w;bad+=w*step(r.w,0.);
  }
  /* the floor breathes a little on its own */
  p.y+=sin(p.x*.7+uTime*.6)*cos(p.z*.6+uTime*.4)*.035;
  vGlow=min(glow,1.4);vBad=min(bad,1.);
  vec4 mv=modelViewMatrix*vec4(p,1.);
  vFog=smoothstep(26.,4.,-mv.z);
  vBase=.5+.5*sin(position.x*13.1+position.z*7.7);
  gl_PointSize=uPx*(1.+vGlow*1.4)/-mv.z;
  gl_Position=projectionMatrix*mv;
}`;

const FRAG = /* glsl */`
uniform float uDim;uniform vec3 uRest;uniform float uBase;
varying float vGlow;varying float vBad;varying float vFog;varying float vBase;
void main(){
  float d=length(gl_PointCoord-.5);
  float a=smoothstep(.5,.15,d);
  vec3 rest=uRest*(.55+.45*vBase);
  vec3 hot=mix(vec3(1.,.5,.22),vec3(1.,.28,.24),vBad);
  vec3 c=mix(rest,hot,min(vGlow,1.));
  float k=min(a*vFog*(uBase+vGlow*.9)*uDim,1.);
  gl_FragColor=vec4(c,k);
}`;

const lerp = (a, b, t) => a + (b - a) * t;

export function mount(canvas, state, opts) {
  const still = !!(opts && opts.still), page = !!(opts && opts.page);
  let renderer;
  try { renderer = new WebGLRenderer({ canvas, antialias: false, powerPreference: 'high-performance' }); }
  catch (e) { return null; }
  /* the ground: the stage's espresso on the homepage, the page's own background elsewhere */
  const uRest = { value: new Color(0.42, 0.33, 0.28) }, uBase = { value: 0.38 };
  function ground() {
    let bg = new Color(0x0c0807);
    if (page) {
      const m = getComputedStyle(document.body).backgroundColor.match(/[\d.]+/g);
      if (m) bg = new Color(+m[0] / 255, +m[1] / 255, +m[2] / 255);
    }
    const light = bg.r * 0.3 + bg.g * 0.59 + bg.b * 0.11 > 0.5;
    renderer.setClearColor(bg, 1);
    uRest.value.set(light ? 0x2a1f1a : 0x6b5448);
    uBase.value = light ? 0.3 : 0.38;
  }
  ground();
  const themeMq = matchMedia('(prefers-color-scheme: dark)');
  if (themeMq.addEventListener) themeMq.addEventListener('change', ground);
  new MutationObserver(ground).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  const scene = new Scene();
  const camera = new PerspectiveCamera(42, 1, 0.1, 80);

  /* the grid: square lattice on the floor plane, deeper than it is wide */
  const COLS = 96, ROWS = 64, STEP = 0.32, pos = new Float32Array(COLS * ROWS * 3);
  for (let r = 0, i = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++, i += 3) {
    pos[i] = (c - (COLS - 1) / 2) * STEP; pos[i + 1] = FLOOR; pos[i + 2] = 4 - r * STEP;
  }
  const geo = new BufferGeometry();
  geo.setAttribute('position', new BufferAttribute(pos, 3));
  const uRip = { value: Array.from({ length: SLOTS }, () => new Vector4(0, 0, -99, 1)) };
  const uTime = { value: 0 }, uPx = { value: 40 }, uDim = { value: 1 };
  const mat = new ShaderMaterial({ vertexShader: VERT, fragmentShader: FRAG,
    uniforms: { uTime, uPx, uDim, uRip, uRest, uBase }, transparent: true, depthWrite: false, blending: NormalBlending });
  const dots = new Points(geo, mat);
  dots.frustumCulled = false;
  scene.add(dots);

  let W = 0, H = 0;
  function resize() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h || (w === W && h === H)) return;
    W = w; H = h;
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    renderer.setPixelRatio(dpr);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    uPx.value = h * dpr * 0.022;
  }

  /* where on the floor the session sits: cast from its screen position down onto the plane */
  const ray = new Raycaster(), floor = new Plane(new Vector3(0, 1, 0), -FLOOR), hit = new Vector3(), ndc = new Vector2();
  function origin() {
    ndc.set(state.ox || 0.4, Math.min(state.oy == null ? -0.2 : state.oy, -0.05));
    ray.setFromCamera(ndc, camera);
    return ray.ray.intersectPlane(floor, hit) ? hit : hit.set(0, FLOOR, 0);
  }
  let slot = 0;
  function ping(sign) {
    const o = origin(), r = uRip.value[slot];
    r.x = o.x; r.y = o.z; r.z = uTime.value; r.w = sign;
    slot = (slot + 1) % SLOTS;
  }

  const clock = new Clock();
  let t = 0, px = 0, py = 0, sp = 0, raf = 0, running = false;

  function frame() {
    resize();
    const dt = Math.min(clock.getDelta(), 0.05);
    if (!still) t += dt;
    px = lerp(px, state.px || 0, 0.04); py = lerp(py, state.py || 0, 0.04);
    sp = lerp(sp, state.p || 0, still ? 1 : 0.1);
    if (page) { camera.position.set(px * 0.5, 0.7 - py * 0.2 + sp * 0.8, 6); camera.lookAt(px * 0.2, -1.0, -4); }
    else { camera.position.set(px * 0.6, 1.1 - py * 0.25 + sp * 1.2, 7); camera.lookAt(px * 0.2, -0.6 - sp * 0.4, -4); }
    if (state.ping) { ping(state.ping); state.ping = 0; }
    uTime.value = t;
    uDim.value = lerp(1, 0.55, sp) * Math.min(1, t / 1.2 + (still ? 1 : 0));
    renderer.render(scene, camera);
  }
  function loop() { if (!running) return; frame(); raf = requestAnimationFrame(loop); }
  function start() { if (running || still) return; running = true; clock.getDelta(); raf = requestAnimationFrame(loop); }
  function stop() { running = false; cancelAnimationFrame(raf); }

  const io = new IntersectionObserver((en) => { en[0].isIntersecting && !document.hidden ? start() : stop(); });
  io.observe(canvas);
  const vis = () => { document.hidden ? stop() : (canvas.getBoundingClientRect().bottom > 0 && start()); };
  document.addEventListener('visibilitychange', vis);
  const onResize = () => { if (still) frame(); };
  window.addEventListener('resize', onResize);
  canvas.addEventListener('webglcontextlost', (ev) => { ev.preventDefault(); stop(); });
  canvas.addEventListener('webglcontextrestored', () => start());

  frame();
  if (!still) start();
  return {
    dispose() { stop(); io.disconnect(); document.removeEventListener('visibilitychange', vis); window.removeEventListener('resize', onResize); renderer.dispose(); },
  };
}
