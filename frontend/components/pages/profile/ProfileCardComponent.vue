<template>
  <div
    id="profile"
    class="d-flex flex-column justify-content-center align-items-center flex-grow-1"
  >
    <n-card class="profile-card" title="Профиль">
      <n-form
        v-if="credentials"
        ref="formRef"
        :model="credentials"
        size="large"
        form-props
      >
        <n-form-item path="name" label="Имя">
          <n-input v-model:value="credentials.name" placeholder="Введите Имя" />
        </n-form-item>
        <n-form-item path="last_name" label="Фамилия">
          <n-input
            v-model:value="credentials.last_name"
            placeholder="Введите Фамилию"
          />
        </n-form-item>
        <n-form-item path="address" label="Адрес">
          <n-input
            v-model:value="credentials.address"
            placeholder="Введите адрес включая почтовый индекс"
          />
        </n-form-item>
        <n-form-item
          name="phone"
          first
          path="phone"
          label="Номер телефона"
          size="large"
        >
          <n-input-group>
            <n-input-group-label size="large"> +7 </n-input-group-label>
            <input
              v-model="credentials.phone"
              v-maska
              class="phone-input light"
              type="text"
              data-maska="(###) ###-##-##"
              placeholder="Введите 10 цифр"
            />
          </n-input-group>
        </n-form-item>
        <n-form-item path="email" label="Email">
          <n-input
            v-model:value="credentials.email"
            :input-props="{ autocomplete: 'off' }"
          />
        </n-form-item>
        <div class="password-section">
          <n-collapse>
            <n-collapse-item title="Управление паролем" class="py-2">
              <n-form-item path="password" label="Пароль">
                <n-input
                  v-model:value="credentials.password"
                  :input-props="{
                    type: 'password',
                    autocomplete: 'new-password'
                  }"
                  type="password"
                  placeholder="Введите пароль"
                />
              </n-form-item>
              <n-form-item first path="reenteredPassword" label="Повтор пароля">
                <n-input
                  v-model:value="credentials.reenteredPassword"
                  :disabled="!credentials.password"
                  :input-props="{ type: 'password', autocomplete: 'off' }"
                  type="password"
                  placeholder="Повторите пароль"
                />
              </n-form-item>
            </n-collapse-item>
          </n-collapse>
        </div>
        <n-row :gutter="[0, 24]">
          <n-col :span="24">
            <div style="display: flex; justify-content: flex-end">
              <n-button
                :disabled="credentials.password === null"
                round
                color="black"
                @click="updateInfo"
              >
                Обновить информацию
              </n-button>
            </div>
          </n-col>
        </n-row>
      </n-form>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import { useAuthStore } from '~/store/authentication'
import type { ClientInterface } from '~/interfaces/client'

const credentials = ref<ClientInterface | undefined>()

const auth = useAuthStore()

function populateForm(): void {
  if (auth.user) {
    credentials.value = Object.assign({}, unref($auth().user))
  }
}

async function updateInfo(e: MouseEvent): Promise<void> {
  e.preventDefault()
  const payload = unref(credentials)
  if (payload) {
    await auth.updateUserInfo(payload)
    $notification('Данные пользователя успешно обновлены!', 'success')
    $router().push('/')
  }
}

onMounted(() => {
  populateForm()
})
</script>

<style lang="scss">
.profile-card {
  max-width: 800px;
  width: 90%;
}
</style>
