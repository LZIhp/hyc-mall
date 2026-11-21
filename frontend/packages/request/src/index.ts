import axios, { AxiosInstance } from 'axios'

export interface RequestOptions {
  baseURL?: string
  /** localStorage 中存储 token 的键名 */
  tokenKey?: string
}

export const BASE_URL = import.meta.env?.VITE_API_BASE_URL ?? 'http://localhost:8000'

/**
 * 创建带鉴权拦截器的 axios 实例
 * @param options.tokenKey 各端 token 存储键：用户 token / 商家 sjlocaltoken / 管理员 adtoken
 */
export function createClient(options: RequestOptions = {}): AxiosInstance {
  const { baseURL = BASE_URL, tokenKey = 'token' } = options
  const client = axios.create({ baseURL, timeout: 15000 })

  client.interceptors.request.use((config) => {
    const token = localStorage.getItem(tokenKey)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })

  client.interceptors.response.use(
    (response) => response,
    (error) => {
      // 401 统一跳登录页（token 失效）
      if (error.response?.status === 401) {
        localStorage.removeItem(tokenKey)
      }
      return Promise.reject(error)
    },
  )

  return client
}

/** 用户端默认实例 */
export const http = createClient({ tokenKey: 'token' })

export default http
