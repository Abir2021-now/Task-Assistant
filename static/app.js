const taskList = document.getElementById("task-list");
const taskForm = document.getElementById("task-form");
const titleInput = document.getElementById("title");
const priorityInput = document.getElementById("priority");
const status = document.getElementById("status");

async function loadTasks() {
  const response = await fetch("/api/tasks");
  const tasks = await response.json();

  taskList.innerHTML = "";

  if (!tasks.length) {
    taskList.innerHTML = "<li class='empty'>No tasks yet.</li>";
    return;
  }

  tasks.forEach((task) => {
    const li = document.createElement("li");
    li.className = "task-item" + (task.completed ? " done" : "");

    const summary = document.createElement("div");
    summary.className = "task-summary";
    summary.innerHTML = `
      <strong>${task.title}</strong>
      <span class="priority ${task.priority}">${task.priority}</span>
    `;

    const actions = document.createElement("div");
    actions.className = "task-actions";

    const completeButton = document.createElement("button");
    completeButton.textContent = task.completed ? "Completed" : "Complete";
    completeButton.disabled = task.completed;
    completeButton.onclick = async () => {
      await fetch(`/api/tasks/${task.id}/complete`, { method: "PUT" });
      loadTasks();
    };

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.className = "danger";
    deleteButton.onclick = async () => {
      await fetch(`/api/tasks/${task.id}`, { method: "DELETE" });
      loadTasks();
    };

    actions.appendChild(completeButton);
    actions.appendChild(deleteButton);
    li.appendChild(summary);
    li.appendChild(actions);
    taskList.appendChild(li);
  });
}

taskForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const title = titleInput.value.trim();
  const priority = priorityInput.value;

  if (!title) {
    status.textContent = "Task title is required.";
    return;
  }

  const response = await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, priority }),
  });

  if (!response.ok) {
    status.textContent = "Failed to create task.";
    return;
  }

  status.textContent = "Task created successfully.";
  titleInput.value = "";
  await loadTasks();
});

loadTasks();
