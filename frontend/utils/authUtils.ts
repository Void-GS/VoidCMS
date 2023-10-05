import { useAuthStore } from '@/store/authentication'

export function $auth() {
  return useAuthStore()
}
