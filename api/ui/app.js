let sentimentChart = null;
let ratingChart = null;

function animateNumber(el, value) {
  let start = 0;
  const duration = 600;
  const step = value / (duration / 16);

  const counter = setInterval(() => {
    start += step;
    if (start >= value) {
      el.innerText = value;
      clearInterval(counter);
    } else {
      el.innerText = Math.floor(start);
    }
  }, 16);
}

async function analyze() {
  const appId = document.getElementById("appId").value;
  const limit = document.getElementById("limit").value;
  const btn = document.getElementById("analyzeBtn");

  if (!appId) {
    alert("App ID wajib diisi");
    return;
  }

  btn.innerText = "Analyzing...";
  btn.classList.add("loading");

  const res = await fetch("/analyze/google-play", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      app_id: appId,
      limit: parseInt(limit)
    })
  });

  const data = await res.json();

  btn.innerText = "Analyze";
  btn.classList.remove("loading");

  // === STATS ===
  animateNumber(
    document.getElementById("pos"),
    data.sentiment_distribution?.Positive || 0
  );
  animateNumber(
    document.getElementById("neg"),
    data.sentiment_distribution?.Negative || 0
  );
  animateNumber(
    document.getElementById("neu"),
    data.sentiment_distribution?.Neutral || 0
  );

  document.getElementById("summaryText").innerText =
    data.summary || "Tidak ada ringkasan.";

  renderCharts(data);
  renderKeywords(data)
}

function renderCharts(data) {
  renderSentimentChart(data.sentiment_distribution);
  renderRatingChart(data.rating_distribution);
}

/* =========================
   SENTIMENT PIE
========================= */
function renderSentimentChart(dist) {
  if (!dist) return;

  const ctx = document.getElementById("sentimentChart");

  sentimentChart?.destroy();

  sentimentChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Positive", "Negative", "Neutral"],
      datasets: [{
        data: [
          dist.Positive || 0,
          dist.Negative || 0,
          dist.Neutral || 0
        ],
        backgroundColor: ["#22c55e", "#ef4444", "#facc15"],
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      cutout: "65%",
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: "#e5e7eb" }
        }
      }
    }
  });
}

/* =========================
   RATING BAR
========================= */
function renderRatingChart(ratingDist) {
  if (!ratingDist) {
    console.warn("rating_distribution tidak ada dari backend");
    return;
  }

  const ctx = document.getElementById("ratingChart");

  ratingChart?.destroy();

  ratingChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: Object.keys(ratingDist),
      datasets: [{
        label: "Jumlah Review",
        data: Object.values(ratingDist),
        backgroundColor: "#38bdf8"
      }]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          ticks: { color: "#e5e7eb" },
          grid: { display: false }
        },
        y: {
          ticks: { color: "#e5e7eb" },
          grid: { color: "#1e293b" }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function renderKeywords(data) {
  const negEl = document.getElementById("negKeywords");
  const posEl = document.getElementById("posKeywords");

  // NEGATIVE
  if (data.top_negative_keywords && data.top_negative_keywords.length > 0) {
    negEl.innerHTML = data.top_negative_keywords
      .map(k => `<li>${k[0]}</li>`)
      .join("");
  } else {
    negEl.innerHTML = `<li class="muted">Belum ada data</li>`;
  }

  // POSITIVE
  if (data.top_positive_keywords && data.top_positive_keywords.length > 0) {
    posEl.innerHTML = data.top_positive_keywords
      .map(k => `<li>${k[0]}</li>`)
      .join("");
  } else {
    posEl.innerHTML = `<li class="muted">Belum ada data</li>`;
  }
}

function showPage(page, el) {
  document.getElementById("playstore-page").style.display =
    page === "playstore" ? "block" : "none";

  document.getElementById("manual-page").style.display =
    page === "manual" ? "block" : "none";

  document.querySelectorAll(".sidebar li").forEach(li =>
    li.classList.remove("active")
  );

  el.classList.add("active");
  document.querySelector(".main").scrollTop = 0;
}


async function analyzeManual() {
  const text = document.getElementById("manualText").value.trim();
  const ratingVal = document.getElementById("manualRating").value;

  if (!text) {
    alert("Teks wajib diisi");
    return;
  }

  const res = await fetch("/analyze/manual-text", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text,
      rating: ratingVal ? parseInt(ratingVal) : null
    })
  });

  const data = await res.json();
  const model = data.model_output;

    const btn = document.querySelector(".btn-primary");
    btn.classList.add("loading");
    btn.innerText = "Analyzing...";

    /* setelah response */
    btn.classList.remove("loading");
    btn.innerText = "Analyze";

  // SHOW CARD
  document.getElementById("manualEmpty").classList.add("hidden");
  document.getElementById("manualCard").classList.remove("hidden");

  // LABEL
  const label = model.label.toLowerCase();
  const badge = document.getElementById("resultLabel");
  badge.innerText = model.label;
  badge.className = `badge ${label}`;

  // CONFIDENCE
  const confidence = model.confidence * 100;
  document.getElementById("resultConfidence").innerText =
    confidence.toFixed(2) + "%";
  document.getElementById("confidenceFill").style.width =
    confidence + "%";

  // PROBABILITIES
  document.getElementById("probPos").innerText =
    model.probabilities.Positive.toFixed(4);
  document.getElementById("probNeu").innerText =
    model.probabilities.Neutral.toFixed(4);
  document.getElementById("probNeg").innerText =
    model.probabilities.Negative.toFixed(4);

  // DECISION ENGINE
  const decisionBox = document.getElementById("decisionBox");
  if (data.decision) {
    decisionBox.classList.remove("hidden");
    document.getElementById("finalSentiment").innerText =
      data.decision.final_sentiment;
    document.getElementById("decisionReason").innerText =
      data.decision.reason;
  } else {
    decisionBox.classList.add("hidden");
  }
}


