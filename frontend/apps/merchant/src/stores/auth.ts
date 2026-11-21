import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('merchant-auth', () => {
  const token = ref(localStorage.getItem('sjlocaltoken') || '')

  function setToken(value: string) {
    token.value = value
    localStorage.setItem('sjlocaltoken', value)
  }

  function logout() {
    token.value = ''
    localStorage.removeItem('sjlocaltoken')
  }

  return { token, setToken, logout }
})
