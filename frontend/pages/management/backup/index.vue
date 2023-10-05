<template>
  <div id="backup" class="backup d-flex align-items-center col-12 col-md-6">
    <n-spin :show="loading" class="col-12" size="large">
      <n-card class="backup-card">
        <n-h2> Резервное копирование и восстановление </n-h2>
        <div v-if="success === undefined" class="backup-actions">
          <n-button
            size="large"
            class="col-12"
            type="primary"
            @click="downloadBackup"
          >
            <template #icon>
              <n-icon>
                <cloud-download-outline />
              </n-icon>
            </template>
            Создать резервную копию
          </n-button>
          <n-upload
            :default-upload="false"
            list-type="image"
            :multiple="false"
            accept=".zip"
            class="col-12 mt-4"
            :max="1"
            @change="uploadBackup"
          >
            <n-button class="w-100" size="large">
              <template #icon>
                <n-icon>
                  <cloud-upload-outline />
                </n-icon>
              </template>
              Восстановить из резервной копии
            </n-button>
          </n-upload>
        </div>
        <div
          v-else
          class="result d-flex flex-wrap align-items-center justify-content-center col-12 p-5"
        >
          <n-icon
            size="82"
            class="col-12"
            :color="success === false ? 'red' : 'green'"
          >
            <CloseCircleOutline v-if="success === false" />
            <CheckmarkDoneCircleOutline v-else />
          </n-icon>
          <n-h4 class="my-0 text-center mt-5 col-12">
            {{ success === false ? statusText.error : statusText.success }}
          </n-h4>
          <NuxtLink to="/" class="mt-5">
            <n-button
              tertiary
              :type="success === false ? 'error' : 'success'"
              size="large"
            >
              <template #icon>
                <n-icon>
                  <home-outline />
                </n-icon>
              </template>
              Вернуться на главную
            </n-button>
          </NuxtLink>
        </div>
      </n-card>
      <template #description>
        <n-text>
          Процесс может занять некоторое время, будьте терпеливы. ;)
        </n-text>
      </template>
    </n-spin>
  </div>
</template>

<script lang="ts" setup>
import {
  CheckmarkDoneCircleOutline,
  CloseCircleOutline,
  CloudDownloadOutline,
  CloudUploadOutline,
  HomeOutline
} from '@vicons/ionicons5'

import type { UploadFileInfo } from 'naive-ui'

const statusText = {
  success: 'Резервная копия восстановлена успешно.',
  error:
    'Ошибка восстановления резервной копии: вероятно файл поврежден или имеет не верный формат.'
}

/// ///
// Variables
const success = ref<boolean | undefined>()
const loading = ref<boolean>(false)

/// ///
// Functions
async function downloadBackup() {
  loading.value = true
  const response: Blob | MediaSource = await $fetch(`/settings/backup`, {
    method: 'GET',
    responseType: 'blob'
  })
  const url = await window.URL.createObjectURL(response)
  window.location.assign(url)
  loading.value = false
}

async function uploadBackup(options: {
  file: UploadFileInfo
  fileList: Array<UploadFileInfo>
  event?: Event
}) {
  const formData = new FormData()
  formData.append('backup_file', options.file.file as Blob, 'backup.zip')

  loading.value = true
  try {
    await $fetch(`/settings/backup`, {
      method: 'POST',
      body: formData
    })
    success.value = true
    $notification(statusText.success, 'success', 4000)
    await $auth().getSession()
  } catch {
    success.value = false
    $notification(statusText.error, 'error', 4000)
  }
  loading.value = false
}
</script>

<style lant="ts" scoped>
.result {
  background: #fafafc;
}
</style>
