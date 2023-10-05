<template>
  <n-card class="page-card new-page-card" size="huge">
    <n-h2> {{ id ? 'Редактирование' : 'Добавление' }} страницы: </n-h2>
    <n-divider />

    <n-form ref="formRef" :model="page" size="large">
      <n-form-item path="name" label="Название">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-input
          v-else
          v-model:value="page.name"
          placeholder="Введите название страницы"
        />
      </n-form-item>
      <n-form-item path="visible" label="Отображение страницы">
        <n-switch v-model:value="page.visible" size="large" :disabled="loading">
          <template #checked> Видимый </template>
          <template #unchecked> Невидимый </template>
        </n-switch>
      </n-form-item>
      <n-form-item path="content" label="Содержание страницы">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <div v-else class="quill-editor-container w-100">
          <QuillEditor
            v-model:content="page.content"
            content-type="html"
            theme="snow"
          />
        </div>
      </n-form-item>
      <SeoInputs v-model:item="page" />
      <div class="page-actions mt-4 float-end">
        <n-button type="tertiary" @click="handlePage">
          {{ id ? 'Обновить' : 'Добавить' }} страницу
        </n-button>
      </div>
    </n-form>
  </n-card>
</template>

<script lang="ts" setup>
import type { PageInterface } from '~/interfaces/page'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
const { vueApp } = useNuxtApp()

/// ///
// Components
const SeoInputs = defineAsyncComponent(
  () => import('~/components/ui/management/seoInputs.vue')
)

if (!process.server) {
  const { QuillEditor } = await import('@vueup/vue-quill')
  if (!vueApp._context.components.QuillEditor)
    vueApp.component('QuillEditor', QuillEditor)
}

/// ///
// Props
const props = defineProps<{
  id?: string
}>()

/// ///
// Variables
const store = storePages()
const page = ref<PageInterface>({ visible: true })

const loading = ref<boolean>(false)
if (props.id) {
  loading.value = true
}

/// ///
// Functions
async function handlePage(e: MouseEvent) {
  e.preventDefault()
  if (!page.value.meta_url) {
    page.value.meta_url = translit(page.value.name || '')
  }
  if (!page.value.meta_title) {
    page.value.meta_title = page.value.name || ''
  }
  if (!page.value.meta_description) {
    page.value.meta_description = page.value.content || ''
  }
  const prepared: PageInterface = {
    ...cleanObject(unref(page))
  }
  if (!props.id) {
    try {
      await store.createPage(prepared)
      $router().push('/management/pages')
      $notification('Страница добавлена', 'success')
      page.value = {}
    } catch {
      $notification('Ошибка добавления страницы', 'error')
    }
  } else {
    try {
      await store.updatePage(prepared)
      $router().push('/management/pages')
      $notification('Страница Обновлена', 'success')
    } catch {
      $notification('Ошибка обновления', 'error')
    }
  }
}

async function recievePage(id: string | undefined) {
  if (id) {
    const response: PageInterface = { ...(await store.getPageById(id)) }
    page.value = response
    loading.value = false
  }
}

recievePage(props.id)
</script>

<style lang="scss">
.quill-editor-container,
.ql-editor {
  min-height: 220px;
}
</style>
