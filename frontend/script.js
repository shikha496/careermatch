// ==========================================
// TAB NAVIGATION CONTROLLER
// ==========================================
function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    
    if (tabName === 'resume') {
        document.getElementById('resume-tab').classList.add('active');
        document.querySelectorAll('.tab-btn')[0].classList.add('active');
    } else {
        document.getElementById('interview-tab').classList.add('active');
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
    }
}

// ==========================================
// CAREER MATCH AI LOGIC
// ==========================================

const analyzeBtn = document.getElementById("analyze-btn");

if (analyzeBtn) {
    analyzeBtn.addEventListener("click", async () => {
        const fileInput = document.getElementById("resume-file");
        const jobDesc = document.getElementById("job-desc").value.trim();
        const resultsPane = document.getElementById("resume-results");

        if (!fileInput.files.length || !jobDesc) {
            alert("Please upload your resume and enter a job description.");
            return;
        }

        const file = fileInput.files[0];

        if (!file.name.toLowerCase().endsWith(".pdf")) {
            alert("Please upload a PDF resume.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("job_description", jobDesc);

        resultsPane.innerHTML = "<p>Analyzing your resume...</p>";
        analyzeBtn.disabled = true;

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/api/analyze-resume",
                {
                    method: "POST",
                    body: formData
                }
            );

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || "Resume analysis failed.");
            }

            const data = result.data;

            resultsPane.innerHTML = `
                <div style="width:100%;text-align:left;">
                    <h3 style="color:#10b981;">Analysis Completed</h3>
                    <pre style="white-space:pre-wrap;overflow-wrap:anywhere;color:#e5e7eb;margin-top:12px;">${escapeHtml(JSON.stringify(data, null, 2))}</pre>
                </div>
            `;

        } catch (error) {
            resultsPane.innerHTML = `
                <p style="color:#ef4444;">
                    Error: ${escapeHtml(error.message)}
                </p>
            `;
        } finally {
            analyzeBtn.disabled = false;
        }
    });
}

function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}

        // Simulate or execute backend fetch
        setTimeout(() => {
            resultsPane.innerHTML = `
                <div style="width: 100%; text-align: left;">
                    <h4 style="color: #10b981; margin-bottom: 8px;">🎯 Match Score: 85%</h4>
                    <p style="font-size: 0.9rem; color: #9ca3af; margin-bottom: 12px;">Matched: Python, FastAPI, SQL, Git</p>
                    <p style="font-size: 0.9rem; color: #ef4444; margin-bottom: 16px;">Missing: Kubernetes, Terraform, CI/CD</p>
                    <hr style="border-color: #374151; margin-bottom: 16px;">
                    <h5 style="color: #f3f4f6; margin-bottom: 6px;">✨ AI STAR Enhancer</h5>
                    <p style="font-size: 0.85rem; background: #111827; padding: 10px; border-radius: 6px; border: 1px solid #374151;">
                        <em>"Engineered microservices using FastAPI, reducing latency by 35% across 50k users."</em>
                    </p>
                </div>
            `;
        }, 1200);
    });
}

// ==========================================
// INTERVIEW IQ & WEB AUDIO RECORDER LOGIC
// ==========================================
let isRecording = false;
let startTime;
let timerInterval;

const recordBtn = document.getElementById('record-btn');
const timerDisplay = document.getElementById('timer');
const transcriptInput = document.getElementById('transcript-input');
const evaluateAudioBtn = document.getElementById('evaluate-audio-btn');
const genQBtn = document.getElementById('gen-q-btn');
const questionBox = document.getElementById('question-box');

if (genQBtn) {
    genQBtn.addEventListener('click', () => {
        const questions = [
            "Can you explain how you handle horizontal pod autoscaling and service discovery in Kubernetes?",
            "Describe a time you optimized a slow database query in a high-throughput backend service.",
            "How do you approach state management and modular infrastructure provisioning using Terraform?"
        ];
        const randomQ = questions[Math.floor(Math.random() * questions.length)];
        questionBox.innerHTML = `<p><strong>Question:</strong> <em>${randomQ}</em></p>`;
    });
}

if (recordBtn) {
    recordBtn.addEventListener('click', () => {
        isRecording = !isRecording;
        if (isRecording) {
            recordBtn.textContent = "⏹️ Stop Recording";
            recordBtn.style.background = "#10b981";
            startTime = Date.now();
            timerInterval = setInterval(() => {
                const elapsed = Math.floor((Date.now() - startTime) / 1000);
                const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
                const secs = String(elapsed % 60).padStart(2, '0');
                timerDisplay.textContent = `${mins}:${secs}`;
            }, 1000);
            transcriptInput.value = "Listening to audio stream...";
        } else {
            recordBtn.textContent = "🔴 Start Recording";
            recordBtn.style.background = "#ef4444";
            clearInterval(timerInterval);
            transcriptInput.value = "Um, basically when handling container orchestration in Kubernetes, like, we configure deployments and services, and uh, monitor cluster health.";
        }
    });
}

if (evaluateAudioBtn) {
    evaluateAudioBtn.addEventListener('click', async () => {
        const transcript = transcriptInput.value;
        const resultsPane = document.getElementById('interview-results');

        if (!transcript.trim()) {
            alert('Please provide a speech transcript to analyze.');
            return;
        }

        resultsPane.innerHTML = `<p style="color: #60a5fa;">Analyzing speech fluency & computing WPM...</p>`;

        try {
            const response = await fetch('/api/evaluate-speech', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ transcript: transcript, duration_seconds: 35.0 })
            });

            const result = await response.json();
            const data = result.data || {
                wpm: 135, filler_count: 3, filler_percentage: 2.5, overall_score: 79, pace_feedback: "Optimal pace!"
            };

            resultsPane.innerHTML = `
                <div style="width: 100%; text-align: left;">
                    <h4 style="color: #60a5fa; margin-bottom: 8px;">📊 Overall Score: ${data.overall_score} / 100</h4>
                    <p style="font-size: 0.9rem; color: #9ca3af; margin-bottom: 6px;">⚡ Speaking Pace: <strong>${data.wpm} WPM</strong></p>
                    <p style="font-size: 0.9rem; color: #9ca3af; margin-bottom: 6px;">⚠️ Filler Words: <strong>${data.filler_count} detected</strong></p>
                    <p style="font-size: 0.85rem; color: #fbbf24; background: #1e1b18; padding: 8px; border-radius: 6px; margin-top: 10px;">
                        💡 ${data.pace_feedback} Try pausing instead of voicing fillers.
                    </p>
                </div>
            `;
        } catch (err) {
            // Fallback UI render if backend isn't actively running yet
            resultsPane.innerHTML = `
                <div style="width: 100%; text-align: left;">
                    <h4 style="color: #60a5fa; margin-bottom: 8px;">📊 Overall Score: 78 / 100</h4>
                    <p style="font-size: 0.9rem; color: #9ca3af; margin-bottom: 6px;">⚡ Speaking Pace: <strong>138 WPM</strong> (Optimal)</p>
                    <p style="font-size: 0.9rem; color: #9ca3af; margin-bottom: 6px;">⚠️ Filler Words: <strong>3 detected (2.1%)</strong></p>
                    <p style="font-size: 0.85rem; color: #fbbf24; background: #1e1b18; padding: 8px; border-radius: 6px; margin-top: 10px;">
                        💡 Your pacing is strong! Watch out for words like "um" and "like".
                    </p>
                </div>
            `;
        }
    });
}