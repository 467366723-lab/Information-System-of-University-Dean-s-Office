const API_BASE = 'http://localhost:5000/api';

function showMessage(text, isSuccess) {
    const box = document.getElementById('message-box');
    box.textContent = text;
    box.className = isSuccess ? 'success' : 'error';
    setTimeout(() => {
        box.className = '';
    }, 3000);
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
    });
});

async function loadStudents() {
    try {
        const res = await fetch(`${API_BASE}/students`);
        const data = await res.json();
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
    } catch (err) {
        showMessage('Failed to load students', false);
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
        // Fix: Parse backend error message
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
    } catch (err) {
        showMessage('Failed to load courses', false);
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
        // Fix: Parse backend error message
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

window.onload = loadStudents;