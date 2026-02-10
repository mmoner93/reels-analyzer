<template>
  <div class="tasks-page">
    <div class="page-header">
      <h1>Instagram Reel Processor</h1>
      <button @click="showAddModal = true" class="btn btn-primary">
        + Add New Task
      </button>
    </div>
    
    <div class="filters">
      <button 
        @click="refreshTasks" 
        :disabled="loading"
        class="btn btn-secondary"
      >
        🔄 {{ loading ? 'Refreshing...' : 'Refresh' }}
      </button>
      
      <label class="auto-refresh">
        <input type="checkbox" v-model="autoRefresh" />
        Auto-refresh (5s)
      </label>
    </div>
    
    <div v-if="error" class="error-banner">
      {{ error }}
    </div>
    
    <div v-if="tasks.length === 0 && !loading" class="empty-state">
      <p>No tasks yet. Click "Add New Task" to get started!</p>
    </div>
    
    <div class="tasks-list">
      <TaskCard
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        @view-transcript="viewTranscript"
        @cancel="cancelTask"
      />
    </div>
    
    <AddTaskModal
      v-if="showAddModal"
      @close="showAddModal = false"
      @task-added="handleTaskAdded"
    />
    
    <TranscriptModal
      v-if="selectedTask"
      :task="selectedTask"
      @close="selectedTask = null"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { tasksApi, type Task } from '../services/api'
import TaskCard from '../components/TaskCard.vue'
import AddTaskModal from '../components/AddTaskModal.vue'
import TranscriptModal from '../components/TranscriptModal.vue'

const tasks = ref<Task[]>([])
const loading = ref(false)
const error = ref('')
const showAddModal = ref(false)
const selectedTask = ref<Task | null>(null)
const autoRefresh = ref(true)
let refreshInterval: number | null = null

const loadTasks = async () => {
  loading.value = true
  error.value = ''
  
  try {
    tasks.value = await tasksApi.listTasks()
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load tasks'
  } finally {
    loading.value = false
  }
}

const refreshTasks = () => {
  loadTasks()
}

const handleTaskAdded = () => {
  loadTasks()
}

const viewTranscript = (taskId: number) => {
  const task = tasks.value.find(t => t.id === taskId)
  if (task) {
    selectedTask.value = task
  }
}

const cancelTask = async (taskId: number) => {
  if (!confirm('Are you sure you want to cancel this task?')) {
    return
  }
  
  try {
    await tasksApi.cancelTask(taskId)
    await loadTasks()
  } catch (err: any) {
    alert(err.response?.data?.detail || 'Failed to cancel task')
  }
}

const setupAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  
  if (autoRefresh.value) {
    refreshInterval = setInterval(() => {
      loadTasks()
    }, 5000)
  }
}

// Watch autoRefresh changes
const stopWatcher = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
}

onMounted(() => {
  loadTasks()
  setupAutoRefresh()
})

onUnmounted(() => {
  stopWatcher()
})

// Re-setup interval when autoRefresh changes
const updateAutoRefresh = () => {
  setupAutoRefresh()
}

// Manual watcher since we can't use watch in this format
setInterval(() => {
  const currentAutoRefresh = autoRefresh.value
  if (currentAutoRefresh && !refreshInterval) {
    setupAutoRefresh()
  } else if (!currentAutoRefresh && refreshInterval) {
    stopWatcher()
  }
}, 100)
</script>

<style scoped>
.tasks-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0;
  color: #333;
}

.filters {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 24px;
}

.auto-refresh {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.error-banner {
  background: #fee;
  color: #c00;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
}

.tasks-list {
  display: flex;
  flex-direction: column;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #5a6268;
}
</style>
