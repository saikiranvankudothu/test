// static/js/summary.js

window.generateSummary = async function () {
  const text = document.getElementById("doc_text").textContent;

  document.getElementById("summaryOutput").style.display = "block";
  document.getElementById("summaryBox").textContent = "";

  const form = new URLSearchParams();
  form.append("text", text);

  try {
    const res = await fetch("/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form,
    });

    const data = await res.json();
    document.getElementById("summaryOutput").style.display = "none";
    document.getElementById("summaryBox").textContent = data.summary;
  } catch {
    document.getElementById("summaryOutput").style.display = "none";
    document.getElementById("summaryBox").textContent = "Summary failed.";
  }
};
