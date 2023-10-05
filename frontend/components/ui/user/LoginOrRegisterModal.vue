<template>
  <n-config-provider :theme="darkTheme">
    <n-modal
      v-model:show="showModalLocal"
      class="login-card"
      preset="card"
      title="Личный Кабинет"
      :bordered="false"
      size="large"
    >
      <n-tabs
        v-model:value="currentTab"
        justify-content="space-evenly"
        class="mb-4"
        size="large"
        type="line"
      >
        <n-tab name="signin"> Вход </n-tab>
        <n-tab name="signup"> Регистрация </n-tab>
      </n-tabs>
      <n-form ref="formRef" :model="credentials" :rules="registerRules">
        <n-form-item path="email" label="Email">
          <n-input
            v-model:value="credentials.email"
            name="email"
            placeholder="Введите email"
            size="large"
            type="text"
          />
        </n-form-item>
        <n-form-item path="password" size="large" label="Пароль">
          <n-input
            v-model:value="credentials.password"
            name="password"
            type="password"
            placeholder="Введите пароль"
            show-password-on="click"
            @input="handlePasswordInput"
            @keydown.enter.prevent
          />
        </n-form-item>
        <template v-if="currentTab === 'signup'">
          <n-form-item
            ref="phoneRef"
            name="phone"
            first
            path="phone"
            label="Введите номер"
            size="large"
          >
            <n-input-group>
              <n-input-group-label size="large"> +7 </n-input-group-label>
              <input
                v-model="credentials.phone"
                v-maska
                class="phone-input"
                type="text"
                data-maska="(###) ###-##-##"
                placeholder="Введите 10 цифр"
              />
            </n-input-group>
          </n-form-item>
          <n-form-item
            ref="rPasswordFormItemRef"
            name="new-password"
            first
            path="reenteredPassword"
            label="Повтор пароля"
            size="large"
          >
            <n-input
              v-model:value="credentials.reenteredPassword"
              :disabled="!credentials.password"
              placeholder="Повторите пароль"
              type="password"
              @keydown.enter.prevent
            />
          </n-form-item>
        </template>
        <div class="hcaptcha">
          <vue-hcaptcha
            ref="hcaptcha"
            :sitekey="$config.public.hcaptcha"
            theme="dark"
            size="invisible"
            @verify="hcaptchaHandler(true)"
            @error="hcaptchaHandler(false)"
          />
        </div>
        <n-row :gutter="[0, 24]">
          <n-col :span="24">
            <div style="display: flex; justify-content: flex-end">
              <n-button
                :disabled="credentials.email === null"
                round
                size="large"
                @click="handleValidateButtonClick"
              >
                {{ currentTab != 'signin' ? 'Зарегистрироваться' : 'Войти' }}
              </n-button>
            </div>
          </n-col>
        </n-row>
      </n-form>
    </n-modal>
  </n-config-provider>
</template>

<script lang="ts" setup>
import {
  type FormInst,
  type FormItemInst,
  type FormItemRule,
  type FormRules,
  type FormValidationError,
  darkTheme
} from 'naive-ui'

import VueHcaptcha from '@hcaptcha/vue3-hcaptcha'
import type { ClientInterface } from '~/interfaces/client'
import type { loginOrRegisterInterface } from '~/interfaces/loginOrRegister'

/// ///
// Props
const props = defineProps<{ showModal: boolean }>()

/// ///
// Variables
const defaultCredentials: loginOrRegisterInterface = {}
const auth = $auth()

const formRef = ref<FormInst | null>(null)
const rPasswordFormItemRef = ref<FormItemInst | null>(null)
const credentials = ref<loginOrRegisterInterface>(defaultCredentials)
const currentTab = ref<string>('signin')

// Captcha
const hcaptcha = ref<VueHcaptcha | null>(null)
const captchaStatus = ref<boolean>(false)

const showModalLocal = computed({
  get() {
    return props.showModal
  },
  set(value: boolean) {
    emit('update:show-modal', value)
  }
})

/// ///
// Emits
const emit = defineEmits(['update:show-modal'])

/// /////
// Rules
const registerRules: FormRules = {
  email: [
    {
      required: true,
      validator: (rule, value) => {
        if (!value) {
          return false
        } else if (!/\S+@\S+\.\S+/.test(value)) {
          return false
        }
        return true
      },
      message: 'Email должен быть заполнен корректно',
      trigger: ['blur']
    }
  ],
  password: [
    {
      required: true,
      validator: (rule, value) => {
        if (!value) {
          return false
        } else if (value.length < 6) {
          return false
        }
        return true
      },
      message: 'Пароль должен содержать не меньше 6 символов',
      trigger: ['blur']
    }
  ],
  phone: [
    {
      required: true,
      validator: (rule, value) => {
        const cleanVal = value.replace(/\D/g, '')
        if (!cleanVal) {
          return false
        } else if (!/^\d+$/.test(cleanVal)) {
          return false
        } else if (cleanVal.length < 10) {
          return false
        }
        return true
      },
      message: 'Номер телефона должен содержать 10 цифр',
      trigger: ['blur']
    }
  ],
  reenteredPassword: [
    {
      required: true,
      message: 'Повтор пароля необходим для регистрации',
      trigger: ['input', 'blur']
    },
    {
      validator: validatePasswordStartWith,
      message: 'Пароли не совпадают!',
      trigger: 'input'
    },
    {
      validator: validatePasswordSame,
      message: 'Пароли не совпадают!',
      trigger: ['blur', 'password-input']
    }
  ]
}

/// ///
// Functions
function validatePasswordStartWith(rule: FormItemRule, value: string): boolean {
  return (
    !!credentials.value.password &&
    credentials.value.password.startsWith(value) &&
    credentials.value.password.length >= value.length
  )
}

function handlePasswordInput() {
  if (credentials.value.reenteredPassword) {
    rPasswordFormItemRef.value?.validate({ trigger: 'password-input' })
  }
}

function validatePasswordSame(rule: FormItemRule, value: string): boolean {
  return value === credentials.value.password
}

async function handleValidateButtonClick(e?: MouseEvent) {
  e?.preventDefault()
  let validation = false
  await formRef.value?.validate(
    (errors: Array<FormValidationError> | undefined) => {
      if (!errors) {
        if (captchaStatus.value) {
          validation = true
        } else {
          hcaptcha.value?.execute()
        }
      }
    }
  )
  if (validation) {
    if (currentTab.value === 'signin') {
      try {
        await auth.signIn(unref(credentials) as ClientInterface)
        const user = unref(auth.user)
        showModalLocal.value = false
        $notification(
          `Добро пожаловать ${user?.name || user?.email}`,
          'success'
        )
        storeCart().getCart()
        if (!user?.name || !user?.address) {
          $router().push('/profile')
          $notification(
            'Заполните данные профиля, вам будет проще оформлять заказы',
            'warning'
          )
        }
      } catch (error) {
        $notification('Ошибка входа: Неверные учетные данные', 'error')
      }
    } else {
      try {
        await auth.signUp(unref(credentials) as ClientInterface)

        $notification(`Пользователь зарегистрирован успешно.`, 'success')
        currentTab.value = 'signin'
      } catch (error) {
        $notification(
          'Ошибка регистрации: Пользователь уже существует',
          'error'
        )
      }
    }
  }
}

function hcaptchaHandler(evt: boolean) {
  captchaStatus.value = evt
  if (!evt) {
    $notification('Подвтердите что вы не робот.', 'error')
  } else {
    handleValidateButtonClick()
  }
}
</script>

<style lang="scss">
.login-card {
  min-width: 360px;
  max-width: 600px;
}
</style>
