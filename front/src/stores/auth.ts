import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'

interface User {
  username: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)

  // We can't use router inside defineStore setup immediately if the router isn't installed yet,
  // but we can access it inside actions.
  // However, simpler is to return actions that the component calls, and the component handles redirect,
  // or pass router to logout.
  // Actually, using `useRouter` inside store setup works if store is used inside a component.
  // But if the store is initialized early, it might fail.
  // Safer to just update state here and let the caller handle redirect, OR import router instance directly (circular dependency risk).
  // I will skip automatic redirect in logout here and let the interceptor/component handle it.

  const isAuthenticated = computed(() => !!token.value)

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('token', newToken)
    decodeToken()
  }

  function decodeToken() {
    if (token.value) {
      try {
        const decoded: any = jwtDecode(token.value)
        user.value = { username: decoded.sub }
      } catch (e) {
        logout()
      }
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  // Initialize
  if (token.value) {
    decodeToken()
  }

  return { token, user, isAuthenticated, setToken, logout }
})
