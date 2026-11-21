import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('admin-auth', () => {
  const token = ref(localStorage.getItem('adtoken') || '')

  function setToken(value: string) {
    token.value = value
    localStorage.setItem('adtoken', value)
  }

  function logout() {
    token.value = ''
    localStorage.removeItem('adtoken')
  }

  return { token, setToken, logout }
})
