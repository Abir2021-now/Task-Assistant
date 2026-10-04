const taskList = document.getElementById("task-list");
const taskForm = document.getElementById("task-form");
const titleInput = document.getElementById("title");
const priorityInput = document.getElementById("priority");
const status = document.getElementById("status");
const searchInput = document.getElementById("search");
const summary = document.getElementById("summary");
const clearCompletedButton = document.getElementById("clear-completed");
const filterButtons = Array.from(document.querySelectorAll(".filter-btn"));

let allTasks = [];
let filter = "all";

function setStatus(message, isError = false) {
  status.textContent = message;
  status.classList.toggle("error", isError);
}

function updateSummary() {
  const total = allTasks.length;
  const done = allTasks.filter((task) => task.completed).length;
  const open = total - done;
  summary.textContent = `${open} open • ${done} done`;
}

function getVisibleTasks() {
  const query = searchInput.value.trim().toLowerCase();

  return allTasks.filter((task) => {
    const matchesQuery = task.title.toLowerCase().includes(query);
    const matchesFilter =
      filter === "all"
        ? true
        : filter === "open"
          ? !task.completed
          : task.completed;

    return matchesQuery && matchesFilter;
  });
}

function renderTasks() {
  const visibleTasks = getVisibleTasks();
  taskList.innerHTML = "";

  if (!visibleTasks.length) {
    taskList.innerHTML = "<li class='empty'>No tasks match your current view.</li>";
    return;
  }

  visibleTasks.forEach((task) => {
    const li = document.createElement("li");
    li.className = "task-item" + (task.completed ? " done" : "");

    const summaryBlock = document.createElement("div");
    summaryBlock.className = "task-summary";
    summaryBlock.innerHTML = `
      <span class="task-title">${task.title}</span>
      <span class="priority ${task.priority}">${task.priority}</span>
    `;

    const actions = document.createElement("div");
    actions.className = "task-actions";

    const completeButton = document.createElement("button");
    completeButton.textContent = task.completed ? "Completed" : "Complete";
    completeButton.disabled = task.completed;
    completeButton.onclick = async () => {
      const response = await fetch(`/api/tasks/${task.id}/complete`, { method: "PUT" });
      if (!response.ok) {
        setStatus("Unable to mark task as complete.", true);
        return;
      }
      setStatus("Task marked complete.");
      await loadTasks();
    };

    const editButton = document.createElement("button");
    editButton.textContent = "Edit";
    editButton.className = "secondary";
    editButton.onclick = async () => {
      const nextTitle = prompt("Edit task title", task.title);
      if (nextTitle === null) return;

      const trimmedTitle = nextTitle.trim();
      if (!trimmedTitle) {
        setStatus("Task title cannot be empty.", true);
        return;
      }

      const nextPriorityValue = prompt(
        "Edit priority (high, medium, low)",
        task.priority,
      );

      const nextPriority = nextPriorityValue ? nextPriorityValue.trim().toLowerCase() : task.priority;
      const normalizedPriority = ["high", "medium", "low"].includes(nextPriority)
        ? nextPriority
        : task.priority;

      const response = await fetch(`/api/tasks/${task.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: trimmedTitle,
          priority: normalizedPriority,
        }),
      });

      if (!response.ok) {
        setStatus("Unable to update task.", true);
        return;
      }

      setStatus("Task updated successfully.");
      await loadTasks();
    };

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.className = "danger";
    deleteButton.onclick = async () => {
      const response = await fetch(`/api/tasks/${task.id}`, { method: "DELETE" });
      if (!response.ok) {
        setStatus("Unable to delete task.", true);
        return;
      }
      setStatus("Task deleted.");
      await loadTasks();
    };

    actions.appendChild(completeButton);
    actions.appendChild(editButton);
    actions.appendChild(deleteButton);
    li.appendChild(summaryBlock);
    li.appendChild(actions);
    taskList.appendChild(li);
  });
}

async function loadTasks() {
  const response = await fetch("/api/tasks");
  if (!response.ok) {
    setStatus("Unable to fetch tasks.", true);
    return;
  }

  allTasks = await response.json();
  updateSummary();
  renderTasks();
}

async function createTask(event) {
  event.preventDefault();

  const title = titleInput.value.trim();
  const priority = priorityInput.value;

  if (!title) {
    setStatus("Task title is required.", true);
    return;
  }

  const response = await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, priority }),
  });

  if (!response.ok) {
    setStatus("Failed to create task.", true);
    return;
  }

  titleInput.value = "";
  priorityInput.value = "medium";
  setStatus("Task created successfully.");
  await loadTasks();
}

async function clearCompleted() {
  const completed = allTasks.filter((task) => task.completed);

  for (const task of completed) {
    await fetch(`/api/tasks/${task.id}`, { method: "DELETE" });
  }

  setStatus("Completed tasks cleared.");
  await loadTasks();
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    filter = button.dataset.filter;
    filterButtons.forEach((item) => item.classList.toggle("active", item === button));
    renderTasks();
  });
});

searchInput.addEventListener("input", renderTasks);
clearCompletedButton.addEventListener("click", clearCompleted);
taskForm.addEventListener("submit", createTask);

loadTasks();
