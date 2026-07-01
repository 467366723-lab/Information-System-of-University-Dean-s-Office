const API_BASE = 'http://localhost:5000/api';

function showMessage(text, isSuccess) {
    const box = document.getElementById('message-box');
    box.textContent = text;
    box.className = isSuccess ? 'success' : 'error';
    setTimeout(() => {
        box.className = '';
    }, 3000);
}

function saveCache(key, data) {
    localStorage.setItem(key, JSON.stringify(data));
}

function loadCache(key) {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : [];
}

function renderStudents(data) {
    const tbody = document.getElementById('stu-tbody');
    tbody.innerHTML = '';
    data.forEach(stu => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${stu.student_id}</td>
            <td>${stu.name}</td>
            <td>${stu.grade}</td>
            <td><button class="btn danger" onclick="deleteStudent('${stu.student_id}')">Delete</button></td>
        `;
        tbody.appendChild(tr);
    });
}

function renderCourses(data) {
    const tbody = document.getElementById('course-tbody');
    tbody.innerHTML = '';
    data.forEach(course => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${course.course_id}</td>
            <td>${course.name}</td>
            <td>${course.credits}</td>
            <td><button class="btn danger" onclick="deleteCourse('${course.course_id}')">Delete</button></td>
        `;
        tbody.appendChild(tr);
    });
}

function renderGrades(data) {
    const tbody = document.getElementById('grade-tbody');
    tbody.innerHTML = '';
    data.forEach(grade => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${grade.student_id}</td>
            <td>${grade.course_id}</td>
            <td>${grade.score}</td>
            <td><button class="btn danger" onclick="deleteGrade('${grade.student_id}', '${grade.course_id}')">Delete</button></td>
        `;
        tbody.appendChild(tr);
    });
}

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        const tabId = btn.getAttribute('data-tab');
        document.getElementById(tabId + '-tab').classList.add('active');
        if (tabId === 'students') loadStudents();
        if (tabId === 'courses') loadCourses();
        if (tabId === 'grades') loadGrades();
    });
});

async function loadStudents() {
    try {
        const res = await fetch(`${API_BASE}/students`);
        const data = await res.json();
        saveCache('students', data);
        renderStudents(data);
    } catch (err) {
        const cached = loadCache('students');
        if (cached.length > 0) {
            renderStudents(cached);
            showMessage('Loaded from local cache', true);
        } else {
            showMessage('Failed to load students', false);
        }
    }
}

async function addStudent() {
    const id = document.getElementById('stu-id').value.trim();
    const name = document.getElementById('stu-name').value.trim();
    const grade = document.getElementById('stu-grade').value.trim();
    if (!id || !name || !grade) {
        showMessage('All fields cannot be empty', false);
        return;
    }
    if (!/^S\d+$/.test(id)) {
        showMessage('ID must start with S followed by numbers', false);
        return;
    }
    const gradeNum = parseInt(grade);
    if (isNaN(gradeNum) || gradeNum < 1900 || gradeNum > 2100) {
        showMessage('Grade must be between 1900 and 2100', false);
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/students`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: id,
                name: name,
                grade: gradeNum
            })
        });
        if (res.status === 201) {
            showMessage('Student added successfully', true);
            document.getElementById('stu-id').value = '';
            document.getElementById('stu-name').value = '';
            document.getElementById('stu-grade').value = '';
            loadStudents();
        } else if (res.status === 409) {
            showMessage('Student ID already exists', false);
        } else {
            const errData = await res.json();
            showMessage(errData.error || 'Add failed', false);
        }
    } catch (err) {
        showMessage('Network error', false);
    }
}

async function deleteStudent(studentId) {
    if (!confirm('Confirm deletion')) return;
    try {
        const res = await fetch(`${API_BASE}/students/${studentId}`, {
            method: 'DELETE'
        });
        const resData = await res.json();
        if (res.status === 200) {
            showMessage('Student deleted successfully', true);
            loadStudents();
        } else {
            showMessage(resData.error || 'Delete failed', false);
        }
    } catch (err) {
        showMessage('Network error', false);
    }
}

async function loadCourses() {
    try {
        const res = await fetch(`${API_BASE}/courses`);
        const data = await res.json();
        saveCache('courses', data);
        renderCourses(data);
    } catch (err) {
        const cached = loadCache('courses');
        if (cached.length > 0) {
            renderCourses(cached);
            showMessage('Loaded from local cache', true);
        } else {
            showMessage('Failed to load courses', false);
        }
    }
}

async function addCourse() {
    const id = document.getElementById('course-id').value.trim();
    const name = document.getElementById('course-name').value.trim();
    const credits = document.getElementById('course-credits').value.trim();
    if (!id || !name || !credits) {
        showMessage('All fields cannot be empty', false);
        return;
    }
    if (!/^C\d+$/.test(id)) {
        showMessage('Course ID must start with C followed by numbers', false);
        return;
    }
    const creditsNum = parseInt(credits);
    if (isNaN(creditsNum) || creditsNum < 1 || creditsNum > 20) {
        showMessage('Credits must be between 1 and 20', false);
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/courses`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                course_id: id,
                name: name,
                credits: creditsNum
            })
        });
        if (res.status === 201) {
            showMessage('Course added successfully', true);
            document.getElementById('course-id').value = '';
            document.getElementById('course-name').value = '';
            document.getElementById('course-credits').value = '';
            loadCourses();
        } else if (res.status === 409) {
            showMessage('Course ID already exists', false);
        } else {
            const errData = await res.json();
            showMessage(errData.error || 'Add failed', false);
        }
    } catch (err) {
        showMessage('Network error', false);
    }
}

async function deleteCourse(courseId) {
    if (!confirm('Confirm deletion')) return;
    try {
        const res = await fetch(`${API_BASE}/courses/${courseId}`, {
            method: 'DELETE'
        });
        const resData = await res.json();
        if (res.status === 200) {
            showMessage('Course deleted successfully', true);
            loadCourses();
        } else {
            showMessage(resData.error || 'Delete failed', false);
        }
    } catch (err) {
        showMessage('Network error', false);
    }
}

async function loadGrades() {
    try {
        const res = await fetch(`${API_BASE}/grades`);
        const data = await res.json();
        saveCache('grades', data);
        renderGrades(data);
    } catch (err) {
        const cached = loadCache('grades');
        if (cached.length > 0) {
            renderGrades(cached);
            showMessage('Loaded from local cache', true);
        } else {
            showMessage('Failed to load grades', false);
        }
    }
}

async function addGrade() {
    const stuId = document.getElementById('grade-stu-id').value.trim();
    const courseId = document.getElementById('grade-course-id').value.trim();
    const score = document.getElementById('grade-score').value.trim();
    if (!stuId || !courseId || !score) {
        showMessage('All fields cannot be empty', false);
        return;
    }
    if (!/^S\d+$/.test(stuId)) {
        showMessage('Student ID must start with S followed by numbers', false);
        return;
    }
    if (!/^C\d+$/.test(courseId)) {
        showMessage('Course ID must start with C followed by numbers', false);
        return;
    }
    const scoreNum = parseInt(score);
    if (isNaN(scoreNum) || scoreNum < 0 || scoreNum > 100) {
        showMessage('Score must be between 0 and 100', false);
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/grades`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: stuId,
                course_id: courseId,
                score: scoreNum
            })
        });
        if (res.status === 201) {
            showMessage('Grade added successfully', true);
            document.getElementById('grade-stu-id').value = '';
            document.getElementById('grade-course-id').value = '';
            document.getElementById('grade-score').value = '';
            loadGrades();
        } else if (res.status === 409) {
            showMessage('Grade record already exists', false);
        } else {
            const errData = await res.json();
            showMessage(errData.error || 'Add failed', false);
        }
    } catch (err) {
        showMessage('Network error', false);
    }
}

async function deleteGrade(studentId, courseId) {
    if (!confirm('Confirm deletion')) return;
    try {
        const res = await fetch(`${API_BASE}/grades/${studentId}/${courseId}`, {
            method: 'DELETE'
        });
        const resData = await res.json();
        if (res.status === 200) {
            showMessage('Grade deleted successfully', true);
            loadGrades();
        } else {
            showMessage(resData.error || 'Delete failed', false);
        }
    } catch (err) {
        showMessage('Network error', false);
    }
}

window.onload = loadStudents;