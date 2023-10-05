<template>
  <n-card class="page-card new-page-card" size="huge">
    <n-h2> {{ id ? 'Редактирование' : 'Добавление' }} социальной сети: </n-h2>
    <n-divider />

    <n-form ref="formRef" :model="social" size="large">
      <n-form-item path="type" label="Тип ссылки">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-select
          v-else
          :options="options"
          placeholder="Выберите тип социально сети"
          size="medium"
          @update:value="updateType"
        />
      </n-form-item>
      <n-form-item
        path="url"
        label="Ссылка на соц. сеть(например: https://t.me/username)"
      >
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-input v-else v-model:value="social.url" placeholder="Введите URL" />
      </n-form-item>
      <div class="page-actions mt-4 float-end">
        <n-button type="tertiary" @click="handlePage">
          {{ id ? 'Обновить' : 'Добавить' }} соц. сеть
        </n-button>
      </div>
    </n-form>
  </n-card>
</template>

<script lang="ts" setup>
import type { SocialInterface } from 'interfaces/social'

/// ///
// Props
const props = defineProps<{
  id?: string
}>()

/// ///
// Variables
const options = [
  {
    label: 'Instagram',
    value: 'instagram'
  },
  {
    label: 'Telegram',
    value: 'telegram'
  },
  {
    label: 'WhatsApp',
    value: 'whatsapp'
  },
  {
    label: 'Facebook',
    value: 'facebook'
  },
  {
    label: 'Вконтакте',
    value: 'vk'
  },
  {
    label: 'Viber',
    value: 'viber'
  },
  {
    label: 'Twitter (X)',
    value: 'twitter'
  },
  {
    label: 'Email',
    value: 'email'
  }
]

const store = storeSocials()
const social = ref<SocialInterface>({})

const loading = ref<boolean>(false)
if (props.id) {
  loading.value = true
}

/// ///
// Functions
function updateType(
  value:
    | 'instagram'
    | 'facebook'
    | 'telegram'
    | 'whatsapp'
    | 'twitter'
    | 'vk'
    | 'viber'
    | 'email'
) {
  social.value.type = value
}

async function handlePage(e: MouseEvent) {
  e.preventDefault()
  const prepared: SocialInterface = {
    ...cleanObject(unref(social))
  }
  if (!props.id) {
    try {
      await store.createSocial(prepared)
      $router().push('/management/socials')
      $notification('Соц.сеть добавлена', 'success')
      social.value = {}
    } catch {
      $notification('Ошибка добавления', 'error')
    }
  } else {
    try {
      await store.updateSocial(prepared)
      $router().push('/management/socials')
      $notification('Соц.сеть Обновлена', 'success')
    } catch {
      $notification('Ошибка обновления', 'error')
    }
  }
}

async function recieveSocial(id: string | undefined) {
  if (id) {
    const response: SocialInterface = { ...(await store.getSocialById(id)) }
    social.value = response
    loading.value = false
  }
}

recieveSocial(props.id)
</script>

<style lang="scss">
.quill-editor-container,
.ql-editor {
  min-height: 220px;
}
</style>
