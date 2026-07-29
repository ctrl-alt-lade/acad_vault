let allCourses = [];
let activeLevel = 0; // 0 = All
let activeSemester = 1;

document.addEventListener("DOMContentLoaded", () => {
    fetchCourses();
});

// Fetch courses from FastAPI backend
async function fetchCourses() {
    try {
        const response = await fetch("/api/courses");
        allCourses = await response.json();
        renderCourses();
    } catch (error) {
        console.error("Error fetching courses:", error);
    }
}

// Render Course Cards
function renderCourses() {
    const container = document.getElementById("courseContainer");
    const searchVal = document.getElementById("searchInput").value.toLowerCase().trim();

    const filtered = allCourses.filter(course => {
        const matchesLevel = activeLevel === 0 || course.level === activeLevel;
        const matchesSemester = course.semester === activeSemester;
        const matchesSearch = course.course_code.toLowerCase().includes(searchVal) || 
                              course.title.toLowerCase().includes(searchVal);
        return matchesLevel && matchesSemester && matchesSearch;
    });

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-12 text-slate-500 border border-dashed border-slate-800 rounded-2xl">
                <p class="text-sm">No courses found matching your filter.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = filtered.map(course => `
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between hover:border-slate-700 transition shadow-sm">
            <div>
                <div class="flex items-center space-x-2 mb-1">
                    <span class="text-xs font-bold text-brand-400 bg-brand-500/10 px-2 py-0.5 rounded">${course.course_code}</span>
                    <span class="text-[10px] text-slate-500 uppercase font-semibold">${course.level}L</span>
                </div>
                <h3 class="text-sm font-semibold text-white leading-snug">${course.title}</h3>
            </div>
            
            <!-- Redirects through /api/go/{course_code} to trigger click tracking -->
            <a href="/api/go/${encodeURIComponent(course.course_code)}" 
               target="_blank" 
               class="text-xs font-medium bg-slate-800 hover:bg-brand-600 hover:text-white text-slate-200 border border-slate-700 hover:border-brand-500 px-3 py-2 rounded-lg transition whitespace-nowrap">
                Access Materials &rarr;
            </a>
        </div>
    `).join('');
}

function filterCourses() {
    renderCourses();
}

function setLevel(lvl) {
    activeLevel = lvl;
    document.querySelectorAll('.level-btn').forEach(btn => {
        btn.classList.remove('bg-brand-600', 'text-white');
        btn.classList.add('text-slate-400');
    });
    const activeBtn = document.getElementById(`lvl-${lvl === 0 ? 'all' : lvl}`);
    activeBtn.classList.add('bg-brand-600', 'text-white');
    activeBtn.classList.remove('text-slate-400');
    renderCourses();
}

function setSemester(sem) {
    activeSemester = sem;
    document.querySelectorAll('.sem-btn').forEach(btn => {
        btn.classList.remove('bg-brand-600', 'text-white');
        btn.classList.add('text-slate-400');
    });
    const activeBtn = document.getElementById(`sem-${sem}`);
    activeBtn.classList.add('bg-brand-600', 'text-white');
    activeBtn.classList.remove('text-slate-400');
    renderCourses();
}

// Modal Toggle
function openRequestModal() {
    document.getElementById("requestModal").classList.remove("hidden");
}

function closeRequestModal() {
    document.getElementById("requestModal").classList.add("hidden");
}

// Submit Material Request
async function submitRequest(event) {
    event.preventDefault();
    
    const payload = {
        student_name: document.getElementById("reqName").value,
        phone_number: document.getElementById("reqPhone").value,
        level: parseInt(document.getElementById("reqLevel").value),
        requested_topic: document.getElementById("reqTopic").value
    };

    try {
        const response = await fetch("/api/requests", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert("Request submitted! Gracious or DML will contact you shortly.");
            closeRequestModal();
            document.getElementById("requestForm").reset();
        } else {
            alert("Error submitting request. Please try again.");
        }
    } catch (err) {
        console.error("Submit error:", err);
    }
}