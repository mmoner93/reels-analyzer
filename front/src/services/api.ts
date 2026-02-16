import axios from 'axios'

// Use relative URL in production (Docker), localhost in development
const API_BASE_URL = import.meta.env.PROD 
  ? '/api' 
  : 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor to handle 401
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export interface Task {
  id: number
  url: string
  status: string
  transcript: string | null
  error_message: string | null
  language: string | null
  topics: string | null
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  url: string
}

export const tasksApi = {
  createTask(data: TaskCreate): Promise<Task> {
    return api.post('/tasks', data).then(response => response.data)
  },

  listTasks(): Promise<Task[]> {
    return api.get('/tasks').then(response => response.data)
  },

  getTask(taskId: number): Promise<Task> {
    return api.get(`/tasks/${taskId}`).then(response => response.data)
  },

  cancelTask(taskId: number): Promise<Task> {
    return api.patch(`/tasks/${taskId}/cancel`).then(response => response.data)
  },

  getTranscript(taskId: number): Promise<any> {
    return api.get(`/tasks/${taskId}/transcript`).then(response => response.data)
  }
}
