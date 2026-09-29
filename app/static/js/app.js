/**
 * TaniCek AI - Frontend Application Logic
 */

let selectedFile = null;
let selectedSample = null;
let leafletMap = null;
let markersLayer = null;
let currentDiagnosisData = null;

document.addEventListener("DOMContentLoaded", () => {
    // Inisialisasi ikon Lucide
    if (window.lucide) {
        lucide.createIcons();
    }

    // Inisialisasi event listener
    initUploadEvents();
    initSettingsModal();
    initChat();
    initGPS();
    loadSamples();
    loadStatistics();

    // Inisialisasi tab pertama
    switchTab("tab-diagnose");
});

/* ==================== TAB NAVIGATION ==================== */
function switchTab(tabId) {
    document.querySelectorAll(".tab-content").forEach(el => el.classList.add("hidden"));
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.classList.remove("bg-white", "text-emerald-800", "shadow-sm");
        btn.classList.add("text-white", "hover:bg-white/10");
    });

    const activeContent = document.getElementById(tabId);
    if (activeContent) activeContent.classList.remove("hidden");

    const navBtnId = tabId.replace("tab-", "nav-");
    const activeBtn = document.getElementById(navBtnId);
    if (activeBtn) {
        activeBtn.classList.remove("text-white", "hover:bg-white/10");
        activeBtn.classList.add("bg-white", "text-emerald-800", "shadow-sm");
    }

    if (tabId === "tab-radar") {
        setTimeout(initOrRefreshMap, 200);
    } else if (tabId === "tab-history") {
        loadReports();
    }

    if (window.lucide) lucide.createIcons();
}

/* ==================== UPLOAD & SAMPLES ==================== */
function initUploadEvents() {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const previewContainer = document.getElementById("preview-container");
    const imagePreview = document.getElementById("image-preview");
    const placeholder = document.getElementById("upload-placeholder");
    const btnRemove = document.getElementById("btn-remove-image");
    const btnDiagnose = document.getElementById("btn-diagnose");

    dropZone.addEventListener("click", (e) => {
        if (e.target.closest("#btn-remove-image")) return;
        fileInput.click();
    });

    fileInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
            handleSelectedFile(e.target.files[0]);
        }
    });

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("border-emerald-600", "bg-emerald-100/50");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("border-emerald-600", "bg-emerald-100/50");
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("border-emerald-600", "bg-emerald-100/50");
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleSelectedFile(e.dataTransfer.files[0]);
        }
    });

    btnRemove.addEventListener("click", (e) => {
        e.stopPropagation();
        clearSelectedImage();
    });

    btnDiagnose.addEventListener("click", () => {
        runDiagnosis();
    });

    // Voice button
    document.getElementById("btn-read-aloud").addEventListener("click", speakDiagnosis);
}

function handleSelectedFile(file) {
    selectedFile = file;
    selectedSample = null;

    const reader = new FileReader();
    reader.onload = (e) => {
        showPreview(e.target.result);
    };
    reader.readAsDataURL(file);
}

function showPreview(url) {
    document.getElementById("upload-placeholder").classList.add("hidden");
    const previewContainer = document.getElementById("preview-container");
    const imagePreview = document.getElementById("image-preview");
    imagePreview.src = url;
    previewContainer.classList.remove("hidden");
    if (window.lucide) lucide.createIcons();
}

function clearSelectedImage() {
    selectedFile = null;
    selectedSample = null;
    document.getElementById("file-input").value = "";
    document.getElementById("preview-container").classList.add("hidden");
    document.getElementById("upload-placeholder").classList.remove("hidden");
}

async function loadSamples() {
    try {
        const resp = await fetch("/api/samples");
        const json = await resp.json();
        if (json.status === "success") {
            const container = document.getElementById("samples-container");
            container.innerHTML = "";
            json.samples.forEach(sample => {
                const card = document.createElement("div");
                card.className = "cursor-pointer rounded-xl border border-slate-200 hover:border-emerald-500 overflow-hidden bg-white shadow-sm hover:shadow transition group flex flex-col";
                card.innerHTML = `
                    <div class="h-16 w-full overflow-hidden bg-slate-100 relative">
                        <img src="${sample.url}" alt="${sample.name}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                        <span class="absolute bottom-1 left-1 bg-black/60 text-white text-[9px] px-1.5 py-0.5 rounded font-medium">${sample.crop}</span>
                    </div>
                    <div class="p-2 flex-grow flex flex-col justify-between">
                        <p class="text-[11px] font-bold text-slate-800 line-clamp-1">${sample.name}</p>
                        <p class="text-[9px] text-emerald-700 font-semibold mt-0.5">Uji Coba →</p>
                    </div>
                `;
                card.addEventListener("click", () => {
                    selectSampleImage(sample);
                });
                container.appendChild(card);
            });
        }
    } catch (e) {
        console.error("Gagal memuat sampel:", e);
    }
}

function selectSampleImage(sample) {
    selectedSample = sample.id;
    selectedFile = null;
    showPreview(sample.url);

    // Auto set crop selector
    const cropSelect = document.getElementById("select-crop");
    const cropLower = sample.crop.toLowerCase();
    if (cropLower.includes("padi")) cropSelect.value = "padi";
    else if (cropLower.includes("jagung")) cropSelect.value = "jagung";
    else if (cropLower.includes("cabai")) cropSelect.value = "cabai";
    else if (cropLower.includes("bawang")) cropSelect.value = "bawang";
    else if (cropLower.includes("tomat")) cropSelect.value = "tomat";
    else if (cropLower.includes("kedelai")) cropSelect.value = "kedelai";

    // Scroll slightly to upload area
    document.getElementById("drop-zone").scrollIntoView({ behavior: "smooth", block: "center" });
}

/* ==================== DIAGNOSIS API CALL ==================== */
async function runDiagnosis() {
    if (!selectedFile && !selectedSample) {
        alert("Silakan unggah foto daun atau pilih salah satu sampel daun siap uji!");
        return;
    }

    const emptyBox = document.getElementById("result-empty");
    const loadingBox = document.getElementById("result-loading");
    const resultBox = document.getElementById("result-display");

    emptyBox.classList.add("hidden");
    resultBox.classList.add("hidden");
    loadingBox.classList.remove("hidden");

    const formData = new FormData();
    if (selectedFile) {
        formData.append("image", selectedFile);
    } else if (selectedSample) {
        formData.append("sample_name", selectedSample);
    }

    formData.append("crop_hint", document.getElementById("select-crop").value);
    formData.append("location_name", document.getElementById("input-location").value || "Lahan Petani");

    // Ambil API key dari localStorage jika ada
    const customKey = localStorage.getItem("tanicek_gemini_api_key") || "";
    formData.append("api_key", customKey);

    try {
        const resp = await fetch("/api/diagnose", {
            method: "POST",
            body: formData
        });
        const res = await resp.json();

        loadingBox.classList.add("hidden");

        if (res.status === "success") {
            displayDiagnosisResult(res.data);
            resultBox.classList.remove("hidden");
            loadStatistics(); // Perbarui statistik terselamatkan
        } else {
            alert("Gagal melakukan analisis: " + (res.detail || "Terjadi kesalahan"));
            emptyBox.classList.remove("hidden");
        }
    } catch (err) {
        loadingBox.classList.add("hidden");
        emptyBox.classList.remove("hidden");
        alert("Terjadi kesalahan jaringan saat mendiagnosa.");
        console.error(err);
    }
}

function displayDiagnosisResult(data) {
    currentDiagnosisData = data;

    document.getElementById("res-badge-crop").innerText = data.crop_name || "Tanaman";
    document.getElementById("res-disease-name").innerText = data.disease_name;
    document.getElementById("res-scientific-name").innerText = data.scientific_name || "";
    document.getElementById("res-badge-engine").innerText = data.ai_engine || "TaniCek Vision Engine";

    // Severity Badge
    const sevBadge = document.getElementById("res-badge-severity");
    sevBadge.innerText = data.severity;
    if (data.severity === "Kritis") {
        sevBadge.className = "bg-rose-100 text-rose-800 text-xs font-bold px-2.5 py-0.5 rounded-full";
    } else if (data.severity === "Sedang") {
        sevBadge.className = "bg-amber-100 text-amber-800 text-xs font-bold px-2.5 py-0.5 rounded-full";
    } else {
        sevBadge.className = "bg-emerald-100 text-emerald-800 text-xs font-bold px-2.5 py-0.5 rounded-full";
    }

    // Confidence
    const conf = data.confidence || 90;
    document.getElementById("res-confidence-text").innerText = `${conf}%`;
    document.getElementById("res-confidence-bar").style.width = `${conf}%`;

    // Symptoms List
    const symList = document.getElementById("res-symptoms-list");
    symList.innerHTML = "";
    (data.symptoms || []).forEach(sym => {
        const li = document.createElement("li");
        li.className = "flex items-start space-x-2";
        li.innerHTML = `<span class="text-emerald-500 font-bold">•</span><span>${sym}</span>`;
        symList.appendChild(li);
    });

    document.getElementById("res-emergency-action").innerText = data.emergency_action || "Pertahankan pengawasan rutin.";
    document.getElementById("res-organic-solution").innerText = data.organic_solution || "Gunakan bahan nabati lokal.";
    document.getElementById("res-chemical-solution").innerText = data.chemical_solution || "Tidak diperlukan bila masih tahap awal.";
    document.getElementById("res-food-impact").innerText = data.food_security_impact || "Menjaga kontinuitas panen pangan.";
    document.getElementById("res-prevention").innerText = data.prevention || "Lakukan rotasi tanaman dan sanitasi lahan berkala.";

    // Render alternatif prediksi model neural network
    const altContainer = document.getElementById("res-alt-container");
    const altList = document.getElementById("res-alt-list");
    if (altContainer && altList) {
        if (data.alternative_predictions && data.alternative_predictions.length > 0) {
            altList.innerHTML = "";
            data.alternative_predictions.forEach(alt => {
                const chip = document.createElement("span");
                chip.className = "bg-slate-100 text-slate-700 px-2.5 py-1 rounded-lg text-xs font-medium border border-slate-200 inline-flex items-center space-x-1";
                chip.innerHTML = `<span>${alt.disease_name}</span> <strong class="text-emerald-700 ml-1 font-bold">${alt.confidence}%</strong>`;
                altList.appendChild(chip);
            });
            altContainer.classList.remove("hidden");
        } else {
            altContainer.classList.add("hidden");
        }
    }

    if (window.lucide) lucide.createIcons();
}

/* ==================== VOICE / TEXT-TO-SPEECH ==================== */
function speakDiagnosis() {
    if (!currentDiagnosisData) return;
    if (!('speechSynthesis' in window)) {
        alert("Browser Anda belum mendukung fitur Text-to-Speech.");
        return;
    }

    window.speechSynthesis.cancel(); // Hentikan suara sebelumnya jika ada

    const d = currentDiagnosisData;
    const textToRead = `Hasil diagnosa Tani Cek AI. Tanaman ${d.crop_name} terdeteksi mengalami ${d.disease_name}. Tingkat keparahan ${d.severity}. Tindakan darurat: ${d.emergency_action}. Rekomendasi nabati: ${d.organic_solution}.`;

    const utterance = new SpeechSynthesisUtterance(textToRead);
    utterance.lang = "id-ID";
    utterance.rate = 0.95; // Sedikit lebih santai agar mudah didengar di sawah

    // Cari suara bahasa Indonesia jika ada
    const voices = window.speechSynthesis.getVoices();
    const idVoice = voices.find(v => v.lang.includes("id") || v.lang.includes("ID"));
    if (idVoice) utterance.voice = idVoice;

    window.speechSynthesis.speak(utterance);
}

/* ==================== RADAR LEAFLET MAP ==================== */
function initOrRefreshMap() {
    const mapContainer = document.getElementById("outbreak-map");
    if (!mapContainer) return;

    if (!leafletMap) {
        // Koordinat tengah Pulau Jawa / Indonesia
        leafletMap = L.map("outbreak-map").setView([-6.9, 109.5], 7);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 18,
            attribution: '© <a href="https://openstreetmap.org">OpenStreetMap</a>'
        }).addTo(leafletMap);

        markersLayer = L.layerGroup().addTo(leafletMap);
    } else {
        leafletMap.invalidateSize();
    }

    // Ambil data titik sebaran
    fetch("/api/outbreak-map")
        .then(r => r.json())
        .then(res => {
            if (res.status === "success" && res.points) {
                markersLayer.clearLayers();
                res.points.forEach(pt => {
                    let color = "#10b981"; // Hijau Sehat
                    if (pt.severity === "Kritis") color = "#f43f5e"; // Merah
                    else if (pt.severity === "Sedang") color = "#f59e0b"; // Oranye

                    const marker = L.circleMarker([pt.latitude, pt.longitude], {
                        radius: 8,
                        fillColor: color,
                        color: "#ffffff",
                        weight: 2,
                        opacity: 1,
                        fillOpacity: 0.85
                    });

                    marker.bindPopup(`
                        <div style="font-family: inherit; font-size: 12px; line-height: 1.4;">
                            <strong style="color: #047857; font-size: 13px;">${pt.crop_name} - ${pt.disease_name}</strong><br>
                            <span>Tingkat: <b style="color: ${color};">${pt.severity}</b> (${pt.confidence}%)</span><br>
                            <span>Lokasi: ${pt.location_name}</span><br>
                            <span style="color: #64748b; font-size: 10px;">Dilaporkan: ${pt.timestamp}</span>
                        </div>
                    `);
                    markersLayer.addLayer(marker);
                });
            }
        })
        .catch(err => console.error("Gagal memuat peta wabah:", err));
}

/* ==================== CHAT PENYULUH AI ==================== */
function initChat() {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (!msg) return;

        chatInput.value = "";
        appendChatMessage("user", msg);

        // Loading bubble
        const loadingId = appendChatMessage("bot", "Mengetik jawaban...");

        const customKey = localStorage.getItem("tanicek_gemini_api_key") || "";

        try {
            const resp = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg, api_key: customKey })
            });
            const data = await resp.json();

            const loadingEl = document.getElementById(loadingId);
            if (loadingEl) {
                loadingEl.innerHTML = formatMarkdown(data.reply);
            }
        } catch (err) {
            const loadingEl = document.getElementById(loadingId);
            if (loadingEl) {
                loadingEl.innerHTML = "Maaf, terjadi gangguan saat menghubungi Penyuluh AI.";
            }
        }
    });
}

function askQuickPrompt(text) {
    document.getElementById("chat-input").value = text;
    document.getElementById("chat-form").dispatchEvent(new Event("submit"));
}

function appendChatMessage(sender, text) {
    const container = document.getElementById("chat-messages");
    const msgId = "msg-" + Date.now();

    const wrapper = document.createElement("div");
    if (sender === "user") {
        wrapper.className = "flex items-start justify-end space-x-3";
        wrapper.innerHTML = `
            <div class="bg-emerald-700 text-white rounded-2xl rounded-tr-none p-3.5 shadow-sm text-xs sm:text-sm max-w-xl leading-relaxed">
                ${escapeHtml(text)}
            </div>
            <div class="w-8 h-8 rounded-full bg-slate-300 text-slate-700 flex items-center justify-center flex-shrink-0 text-xs font-bold">Anda</div>
        `;
    } else {
        wrapper.className = "flex items-start space-x-3 max-w-2xl";
        wrapper.innerHTML = `
            <div class="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center flex-shrink-0 text-xs font-bold">AI</div>
            <div id="${msgId}" class="bg-white border border-slate-200 rounded-2xl rounded-tl-none p-4 shadow-sm text-xs sm:text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
                ${formatMarkdown(text)}
            </div>
        `;
    }

    container.appendChild(wrapper);
    container.scrollTop = container.scrollHeight;
    return msgId;
}

function formatMarkdown(text) {
    if (!text) return "";
    let formatted = escapeHtml(text);
    // Bold
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Bullet
    formatted = formatted.replace(/^\s*-\s+(.*)$/gm, '• $1');
    return formatted;
}

function escapeHtml(string) {
    return String(string)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/* ==================== RIWAYAT & STATISTIK ==================== */
async function loadReports() {
    const tbody = document.getElementById("history-tbody");
    tbody.innerHTML = `<tr><td colspan="6" class="text-center py-6 text-slate-400">Memuat riwayat pemeriksaan...</td></tr>`;

    try {
        const resp = await fetch("/api/reports");
        const res = await resp.json();
        if (res.status === "success" && res.reports) {
            tbody.innerHTML = "";
            res.reports.forEach(r => {
                let badgeClass = "bg-emerald-100 text-emerald-800";
                if (r.severity === "Kritis") badgeClass = "bg-rose-100 text-rose-800";
                else if (r.severity === "Sedang") badgeClass = "bg-amber-100 text-amber-800";

                const tr = document.createElement("tr");
                tr.className = "hover:bg-slate-50 transition border-b border-slate-100";
                tr.innerHTML = `
                    <td class="py-3 px-4 font-mono text-slate-500">${r.timestamp}</td>
                    <td class="py-3 px-4 font-semibold text-slate-800">${r.crop_name}</td>
                    <td class="py-3 px-4">${r.disease_name}</td>
                    <td class="py-3 px-4"><span class="${badgeClass} font-bold px-2 py-0.5 rounded-full text-[10px]">${r.severity}</span></td>
                    <td class="py-3 px-4 font-bold text-emerald-700">${r.confidence}%</td>
                    <td class="py-3 px-4 text-slate-500">${r.location_name || "-"}</td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center py-6 text-rose-500">Gagal memuat riwayat.</td></tr>`;
    }
}

async function loadStatistics() {
    try {
        const resp = await fetch("/api/statistics");
        const res = await resp.json();
        if (res.status === "success" && res.stats) {
            const savedTons = res.stats.estimated_saved_tons || 19.6;
            document.getElementById("header-saved-tons").innerText = `~${savedTons} Ton`;
        }
    } catch (e) {
        console.error(e);
    }
}

/* ==================== GPS GEOLOCATION ==================== */
function initGPS() {
    const btnGPS = document.getElementById("btn-get-gps");
    const inputLoc = document.getElementById("input-location");

    btnGPS.addEventListener("click", () => {
        if (!navigator.geolocation) {
            alert("Geolocation tidak didukung oleh browser Anda.");
            return;
        }
        btnGPS.classList.add("animate-pulse");
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                btnGPS.classList.remove("animate-pulse");
                const lat = pos.coords.latitude.toFixed(4);
                const lng = pos.coords.longitude.toFixed(4);
                inputLoc.value = `Koordinat GPS (${lat}, ${lng})`;
            },
            (err) => {
                btnGPS.classList.remove("animate-pulse");
                inputLoc.value = "Karawang, Jawa Barat (Default)";
            }
        );
    });
}

/* ==================== SETTINGS MODAL ==================== */
function initSettingsModal() {
    const modal = document.getElementById("modal-settings");
    const btnOpen = document.getElementById("btn-open-settings");
    const btnClose = document.getElementById("btn-close-settings");
    const btnSave = document.getElementById("btn-save-settings");
    const btnClear = document.getElementById("btn-clear-settings");
    const inputKey = document.getElementById("input-api-key");

    btnOpen.addEventListener("click", () => {
        inputKey.value = localStorage.getItem("tanicek_gemini_api_key") || "";
        modal.classList.remove("hidden");
    });

    btnClose.addEventListener("click", () => {
        modal.classList.add("hidden");
    });

    btnSave.addEventListener("click", () => {
        const key = inputKey.value.trim();
        if (key) {
            localStorage.setItem("tanicek_gemini_api_key", key);
            alert("API Key Google Gemini berhasil disimpan di browser Anda!");
        }
        modal.classList.add("hidden");
    });

    btnClear.addEventListener("click", () => {
        localStorage.removeItem("tanicek_gemini_api_key");
        inputKey.value = "";
        alert("API Key telah dihapus. Sistem akan menggunakan TaniCek Vision Engine lokal.");
        modal.classList.add("hidden");
    });
}
