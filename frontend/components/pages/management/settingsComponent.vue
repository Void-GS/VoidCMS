<template>
  <n-card class="page-card new-settings-card" size="huge">
    <n-h2> {{ id ? 'Редактирование' : 'Добавление' }} настроек: </n-h2>
    <n-divider />

    <n-form ref="formRef" :model="settings" size="large">
      <div class="images d-flex flex-wrap align-items-center">
        <n-form-item
          class="col-md"
          path="app_logo"
          label="Логотип(Форматы: .png / .svg)"
        >
          <n-upload
            :file-list="previewFileListLogo"
            class="d-flex align-items-center justify-content-center"
            accept=".svg,.png"
            list-type="image-card"
            :max="1"
            :on-update:file-list="UploadLogo"
            :on-remove="handleRemoveImage"
            @preview="handlePreview"
          />
          <n-modal
            v-model:show="showModal"
            preset="card"
            style="width: 600px"
            title="Логотип"
          >
            <img :src="previewImageUrl" style="width: 100%" />
          </n-modal>
        </n-form-item>
        <n-form-item
          class="col-md ps-md-2"
          path="app_favicon"
          label="Фавикон(форматы: .png / .ico / .svg)"
        >
          <n-upload
            :file-list="previewFileListFavicon"
            accept=".ico,.png,.svg"
            list-type="image-card"
            class="d-flex align-items-center justify-content-center"
            :max="1"
            :on-update:file-list="UploadFavicon"
            :on-remove="handleRemoveImage"
            @preview="handlePreview"
          />
        </n-form-item>
        <n-form-item
          class="col-md ps-md-2"
          path="app_background"
          label="Фоновое изображение(форматы: .png / .svg / .jpg)"
        >
          <n-upload
            :file-list="previewFileListBackground"
            accept=".jpg,.png,.svg"
            class="d-flex align-items-center justify-content-center"
            list-type="image-card"
            :max="1"
            :on-update:file-list="UploadBackground"
            :on-remove="handleRemoveImage"
            @preview="handlePreview"
          />
        </n-form-item>
      </div>
      <n-form-item path="app_name" label="Название магазина">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-input
          v-else
          v-model:value="settings.app_name"
          placeholder="Введите название Магазина"
        />
      </n-form-item>
      <n-form-item path="app_url" label="Домен в интернете">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-input
          v-else
          v-model:value="settings.app_url"
          placeholder="Введите название Магазина"
        />
      </n-form-item>
      <n-form-item path="app_description" label="Описание магазина">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-input
          v-else
          v-model:value="settings.app_description"
          type="textarea"
          placeholder="Введите описание магазина"
        />
      </n-form-item>
      <n-form-item path="mantinance" label="Режим обслуживания">
        <n-switch
          v-model:value="settings.mantinance"
          size="large"
          :disabled="loading"
        >
          <template #checked> Включено </template>
          <template #unchecked> Выключено </template>
        </n-switch>
      </n-form-item>
      <div class="settings-actions mt-4 float-end">
        <n-button type="tertiary" @click="handlePage">
          {{ id ? 'Обновить' : 'Добавить' }} настройки
        </n-button>
      </div>
    </n-form>
  </n-card>
</template>

<script lang="ts" setup>
import type { UploadFileInfo } from 'naive-ui'
import type { SettingsInterface } from '~/interfaces/settings'

/// ///
// Props
const props = defineProps<{
  id?: string
}>()

/// ///
// Variables
const store = storeSettings()
const settings = ref<SettingsInterface>({ mantinance: false })
const loading = ref<boolean>(false)

const previewImageUrl = ref('')
const showModal = ref(false)
const previewFileListLogo = ref<UploadFileInfo[]>([])
const previewFileListBackground = ref<UploadFileInfo[]>([])
const previewFileListFavicon = ref<UploadFileInfo[]>([])

if (props.id) {
  loading.value = true
}

/// ///
// Functions
function handlePreview(fileEvt: UploadFileInfo) {
  const { url, file } = fileEvt
  let link
  if (url) {
    link = url
  } else if (file) {
    link = URL.createObjectURL(file)
  }
  previewImageUrl.value = link || ''
  showModal.value = true
}

function UploadLogo(evt: UploadFileInfo[]) {
  handleImageUpload(evt, 'logo')
}

function UploadFavicon(evt: UploadFileInfo[]) {
  handleImageUpload(evt, 'favicon')
}

function UploadBackground(evt: UploadFileInfo[]) {
  handleImageUpload(evt, 'background')
}

function handleImageUpload(
  evt: UploadFileInfo[],
  type: 'logo' | 'favicon' | 'background'
) {
  if (type === 'favicon') {
    previewFileListFavicon.value = evt
  } else if (type === 'logo') {
    previewFileListLogo.value = evt
  } else {
    previewFileListBackground.value = evt
  }
  if (evt[0]?.file) {
    settings.value[`app_${type}_upload`] = evt[0].file
  }
}

async function handlePage(e: MouseEvent) {
  e.preventDefault()
  const prepared: SettingsInterface = {
    ...cleanObject(unref(settings))
  }
  if (!props.id) {
    try {
      await store.createSettings(prepared)
      $router().push('/management/settings')
      $notification('Настройки добавлены', 'success')
      settings.value = {}
    } catch {
      $notification('Ошибка добавления настроек', 'error')
    }
  } else {
    try {
      await store.updateSettings(prepared)
      $router().push('/management/settings')
      $notification('Настройки Обновлены', 'success')
    } catch {
      $notification('Ошибка обновления', 'error')
    }
  }
}

async function recieveSettings(id: string | undefined) {
  if (id) {
    const response: SettingsInterface = { ...(await store.getSettingsById(id)) }
    if (response?.id) {
      if (response.app_logo) {
        previewFileListLogo.value.push({
          id: String(response.app_logo.id),
          name: String(response.app_logo.name),
          status: 'finished',
          url: `${$config().api}${String(response.app_logo.url)}`
        })
        delete response.app_logo
      }
      if (response.app_favicon) {
        previewFileListFavicon.value.push({
          id: String(response.app_favicon.id),
          name: String(response.app_favicon.name),
          status: 'finished',
          url: `${$config().api}${String(response.app_favicon.url)}`
        })
        delete response.app_favicon
      }
      if (response.app_background) {
        previewFileListBackground.value.push({
          id: String(response.app_background.id),
          name: String(response.app_background.name),
          status: 'finished',
          url: `${$config().api}${String(response.app_background.url)}`
        })
        delete response.app_background
      }
      settings.value = response
      loading.value = false
    }
  }
}
recieveSettings(props.id)

onMounted(() => {
  settings.value.app_url = window.location.host
})
</script>

<style lang="scss">
.quill-editor-container,
.ql-editor {
  min-height: 220px;
}
</style>
