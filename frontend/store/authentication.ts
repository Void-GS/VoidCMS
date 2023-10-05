import type { ClientInterface } from '~/interfaces/client'
import type { loginOrRegisterInterface } from '~/interfaces/loginOrRegister'

interface TokenResponseInterface {
  token?: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    rawToken: undefined as string | undefined,
    tokenPrefix: 'Token',
    user: undefined as ClientInterface | undefined
  }),
  getters: {
    isAuthenticated: (state) => {
      return !!state.user?.id
    },
    isAdmin: (state) => {
      return state.user?.role === 'admin'
    },
    token: (state) => {
      return state.rawToken
        ? `${state.tokenPrefix} ${state.rawToken}`
        : undefined
    }
  },
  actions: {
    async signIn(credentials: loginOrRegisterInterface) {
      const response: TokenResponseInterface = await $fetch('/login', {
        method: 'POST',
        body: generateForm(credentials)
      })
      this.setToken(response.token)
      await this.getSession()
    },

    async signOut() {
      await $fetch('/logout', {
        method: 'POST'
      })
      this.user = undefined
      this.setToken()
    },

    async signUp(credentials: loginOrRegisterInterface, autoSignIn = false) {
      await $fetch('/register', {
        method: 'POST',
        body: generateForm(credentials)
      })
      if (autoSignIn) {
        await this.signIn(credentials)
      }
    },

    async updateUserInfo(credentials: loginOrRegisterInterface) {
      const response: ClientInterface = await $fetch('/session', {
        method: 'PUT',
        body: generateForm(credentials)
      })
      this.user = response
    },

    async getSession() {
      if (this.rawToken) {
        try {
          const response: ClientInterface = await $fetch('/session', {
            method: 'GET'
          })
          this.user = response
          return response
        } catch (error) {
          this.setToken()
          this.user = undefined
        }
      }
    },
    // SetToken To storage
    setToken(token?: string) {
      this.rawToken = token
    }
  },
  persist: {
    paths: ['rawToken'],
    storage: persistedState.cookiesWithOptions({
      sameSite: 'strict'
    })
  }
})
