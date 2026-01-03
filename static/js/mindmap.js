// static/js/mindmap.js

window.generateMindmap = async function () {
  const text = document.getElementById("doc_text").textContent;

  const form = new URLSearchParams();
  form.append("text", text);

  try {
    const res = await fetch("/mindmap", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form,
    });

    const data = await res.json();

    document.getElementById("mindmap_code").textContent = data.mindmap;
    document.getElementById(
      "mindmap_preview"
    ).innerHTML = `<div class="mermaid">${data.mindmap}</div>`;

    mermaid.initialize({ startOnLoad: true });
    mermaid.run();
  } catch {
    document.getElementById("mindmap_code").textContent = "Mindmap failed.";
  }
};
