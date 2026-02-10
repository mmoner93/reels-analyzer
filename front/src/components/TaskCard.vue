<template>
  <div class="task-card">
    <div class="task-header">
      <span class="task-id">#{{ task.id }}</span>
      <span :class="['task-status', `status-${task.status}`]">
        {{ task.status.toUpperCase() }}
      </span>
    </div>
    
    <div class="task-url">
      <strong>URL:</strong> {{ task.url }}
    </div>
    
    <div class="task-info">
      <div><strong>Created:</strong> {{ formatDate(task.created_at) }}</div>
      <div v-if="task.language"><strong>Language:</strong> {{ task.language }}</div>
      <div v-if="task.topics"><strong>Topics:</strong> {{ task.topics }}</div>
    </div>
    
    <div v-if="task.error_message" class="task-error">
      <strong>Error:</strong> {{ task.error_message }}
    </div>
    
    <div class="task-actions">
      <button 
        v-if="task.status === 'completed'" 
        @click="$emit('view-transcript', task.id)"
        class="btn btn-primary"
      >
        View Transcript
      </button>
      
      <button 
        v-if="task.status === 'pending' || task.status === 'processing'" 
        @click="$emit('cancel', task.id)"
        class="btn btn-danger"
      >
        Cancel
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '../services/api'

defineProps<{
  task: Task
}>()

defineEmits<{
  viewTranscript: [taskId: number]
  cancel: [taskId: number]
}>()

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}
</script>

<style scoped>
.task-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background: white;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.task-id {
  font-weight: bold;
  color: #666;
}

.task-status {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.status-pending { background: #ffd; color: #660; }
.status-processing { background: #ddf; color: #006; }
.status-completed { background: #dfd; color: #060; }
.status-failed { background: #fdd; color: #600; }
.status-cancelled { background: #ddd; color: #666; }

.task-url {
  margin-bottom: 12px;
  word-break: break-all;
}

.task-info {
  display: grid;
  gap: 4px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #666;
}

.task-error {
  color: #c00;
  margin-bottom: 12px;
  padding: 8px;
  background: #fee;
  border-radius: 4px;
}

.task-actions {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
}
</style>
