const thread = document.getElementById("thread");
const form = document.getElementById("composer");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const statusDot = document.getElementById("status");

let history = [];   // [{role, content}] sent to the backend each turn
let busy = false;

// --- health check -----------------------------------------------------------
fetch("/api/health")
  .then((r) => (r.ok ? statusDot.classList.add("live") : statusDot.classList.add("down")))
  .catch(() => statusDot.classList.add("down"));

// --- rendering --------------------------------------------------------------
function addBubble(role, text = "") {
  document.querySelector(".empty")?.remove();
  const el = document.createElement("div");
  el.className = `msg ${role}`;
  el.textContent = text;
  thread.appendChild(el);
  thread.scrollTop = thread.scrollHeight;
  return el;
}

function autoGrow() {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 180) + "px";
}

// --- sending ----------------------------------------------------------------
async function send(text) {
  busy = true;
  sendBtn.disabled = true;
  addBubble("user", text);
  history.push({ role: "user", content: text });

  const bubble = addBubble("assistant");
  bubble.classList.add("caret");
  let reply = "";

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: history }),
    });
    if (!res.ok) throw new Error(`Server returned ${res.status}`);

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      const lines = buffer.split("\n\n");
      buffer = lines.pop();                       // keep the partial event

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const data = line.slice(6);
        if (data === "[DONE]") continue;

        const parsed = JSON.parse(data);
        if (parsed.error) throw new Error(parsed.error);
        reply += parsed.token;
        bubble.textContent = reply;
        thread.scrollTop = thread.scrollHeight;
      }
    }

    bubble.classList.remove("caret");
    if (reply) history.push({ role: "assistant", content: reply });
    else bubble.remove();
  } catch (err) {
    bubble.remove();
    history.pop();                                // drop the unanswered turn
    addBubble("error", `That message didn't go through: ${err.message}. Try again.`);
  } finally {
    busy = false;
    sendBtn.disabled = false;
    input.focus();
  }
}

// --- events -----------------------------------------------------------------
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text || busy) return;
  input.value = "";
  autoGrow();
  send(text);
});

input.addEventListener("input", autoGrow);

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    form.requestSubmit();
  }
});

document.getElementById("reset").addEventListener("click", () => {
  history = [];
  thread.innerHTML = '<p class="empty">Ask anything to start. Your conversation stays in this browser tab.</p>';
  input.focus();
});
