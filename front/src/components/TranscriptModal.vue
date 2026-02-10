<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>Task #{{ task.id }} - Transcript</h2>
        <button @click="$emit('close')" class="close-btn">&times;</button>
      </div>
      
      <div class="transcript-info">
        <div v-if="task.language" class="info-item">
          <strong>Language:</strong> {{ task.language }}
        </div>
        <div v-if="task.topics" class="info-item">
          <strong>Topics:</strong> {{ task.topics }}
        </div>
      </div>
      
      <div class="transcript-content">
        <p>{{ task.transcript }}</p>
      </div>
      
      <div class="modal-actions">
        <button @click="copyToClipboard" class="btn btn-secondary">
          Copy to Clipboard
        </button>
        <button @click="$emit('close')" class="btn btn-primary">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from '../services/api'

const props = defineProps<{
  task: Task
}>()

const emit = defineEmits<{
  close: []
}>()

const copyToClipboard = () => {
  if (props.task.transcript) {
    navigator.clipboard.writeText(props.task.transcript)
    alert('Transcript copied to clipboard!')
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 24px;
  max-width: 800px;
  width: 90%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h2 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #999;
}

.close-btn:hover {
  color: #333;
}

.transcript-info {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
  padding: 12px;
  background: #f5f5f5;
  border-radius: 4px;
}

.info-item {
  font-size: 14px;
}

.transcript-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #fafafa;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 16px;
}

.transcript-content p {
  margin: 0;
  line-height: 1.6;
  white-space: pre-wrap;
}

.modal-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn {
  padding: 10px 20px;
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

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}
</style>
