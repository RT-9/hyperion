let CHANNEL_COUNT = 512; // Jetzt voll besetzt
let dmxValues = new Array(CHANNEL_COUNT).fill(0);
let stressActive = false;
let stressInterval = null;

const MAX_STRESS_UNIVERSES = 11; // 1 bis 100
const socket = new WebSocket("ws://" + window.location.host + "/ws/engine");
const statusEl = document.getElementById("status");
const universeInput = document.getElementById("universe-selector");
const stressBtn = document.getElementById("stress-btn");
const container = document.getElementById("controls");
const byteDisplay = document.getElementById("byte-count");

// 1. Slider generieren (Wir zeigen weiterhin nur 24 an, damit der Browser nicht stirbt)
// Die restlichen Kanäle bis 512 existieren nur im Hintergrund-Array
for (let i = 0; i < 24; i++) {
  const div = document.createElement("div");
  div.className = "channel-box";
  div.innerHTML = `
        <small>CH ${i + 1}</small><br>
        <input type="range" min="0" max="255" value="0" data-ch="${i}">
        <div id="val-${i}" style="font-size: 1.2em">0</div>
    `;
  container.appendChild(div);
}

// 2. WebSocket Logic
socket.onopen = () => {
  statusEl.innerText = "ONLINE";
  statusEl.style.color = "#00ff00";
};

socket.onclose = () => {
  statusEl.innerText = "OFFLINE";
  statusEl.style.color = "red";
};

// 3. Zentrale Sender Funktion
function sendPacket(universe, channels) {
  if (socket.readyState === WebSocket.OPEN) {
    const payload = {
      universe: universe,
      channels: channels,
    };
    const json = JSON.stringify(payload);
    socket.send(json);
    return json.length;
  }
  return 0;
}

// 4. Slider Event
container.addEventListener("input", (e) => {
  if (e.target.type === "range") {
    const idx = parseInt(e.target.dataset.ch);
    const val = parseInt(e.target.value);
    dmxValues[idx] = val;
    document.getElementById(`val-${idx}`).innerText = val;

    if (!stressActive) {
      sendPacket(parseInt(universeInput.value), dmxValues);
    }
  }
});

// 5. DER MASSIVE STRESS TEST
stressBtn.onclick = () => {
  stressActive = !stressActive;

  if (stressActive) {
    stressBtn.innerText = "NUCLEAR STRESS: RUNNING";
    stressBtn.classList.add("active");

    // Alle 40ms (25 FPS)
    stressInterval = setInterval(() => {
      let totalBytesThisTick = 0;

      // Loop über 100 Universen
      for (let u = 1; u <= MAX_STRESS_UNIVERSES; u++) {
        // Generiere 512 Zufallswerte
        const randomFullUniverse = Array.from({ length: 512 }, () =>
          Math.floor(Math.random() * 256)
        );

        // Jedes Universum als eigenes Paket feuern
        totalBytesThisTick += sendPacket(u, randomFullUniverse);
      }

      byteDisplay.innerText =
        (totalBytesThisTick / 1024).toFixed(2) + " KB/Tick";
    }, 40);
  } else {
    stressBtn.innerText = "STRESS TEST: OFF";
    stressBtn.classList.remove("active");
    clearInterval(stressInterval);
    byteDisplay.innerText = "0";
  }
};
