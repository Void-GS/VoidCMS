<template>
  <n-card class="page-card new-category-card w-100" size="huge">
    <n-h2> {{ id ? 'Редактирование' : 'Добавление' }} категории: </n-h2>
    <n-divider />

    <n-form ref="formRef" :model="category" size="large">
      <n-form-item path="image" label="Обложка категории">
        <n-upload
          :file-list="previewFileList"
          list-type="image-card"
          :max="1"
          :on-update:file-list="handleImageUpload"
          :on-remove="handleRemoveImage"
          @preview="handlePreview"
        />
        <n-modal
          v-model:show="showModal"
          preset="card"
          style="width: 600px"
          class="image-modal"
          title="Предпросмотр"
        >
          <img :src="previewImageUrl" style="width: 100%" />
        </n-modal>
      </n-form-item>
      <n-form-item path="title" label="Название">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-input
          v-else
          v-model:value="category.title"
          placeholder="Введите название категории"
        />
      </n-form-item>
      <n-form-item path="parentcategory" label="Родительская Категория">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-select
          v-else
          v-model:value="category.parent"
          filterable
          value-field="id"
          label-field="title"
          clearable
          placeholder="Выберите или начните вводить"
          :options="store.categoriesGetter"
        />
      </n-form-item>
      <n-form-item path="description" label="Описание категории">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-input
          v-else
          v-model:value="category.description"
          placeholder="Введите описание категории"
        />
      </n-form-item>
      <SeoInputs v-model:item="category" />
      <div class="category-actions mt-4 float-end">
        <n-button type="tertiary" @click="handleCategory">
          {{ id ? 'Обновить' : 'Добавить' }} категорию
        </n-button>
      </div>
    </n-form>
  </n-card>
</template>

<script lang="ts" setup>
import type { UploadFileInfo } from 'naive-ui'
import type { CategoryInterface } from '~/interfaces/category'
import { useStoreCategories } from '~/store/categories'

/// ///
// Components
const SeoInputs = defineAsyncComponent(
  () => import('~/components/ui/management/seoInputs.vue')
)

/// ///
// Props
const props = defineProps<{
  id?: string
}>()

/// ///
// Variables
const config = useRuntimeConfig()
const store = useStoreCategories()
const category = ref<CategoryInterface>({})
const showModal = ref(false)
const previewImageUrl = ref('')
const loading = ref<boolean>(false)
if (props.id) {
  loading.value = true
}

// Files
const previewFileList = ref<UploadFileInfo[]>([])

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

function handleImageUpload(evt: UploadFileInfo[]) {
  previewFileList.value = evt
  if (evt[0]?.file) {
    category.value.image_upload = evt[0].file
  }
}

async function handleCategory(e: MouseEvent) {
  e.preventDefault()
  if (!category.value.meta_url) {
    category.value.meta_url = translit(category.value.title || '')
  }
  if (!category.value.meta_title) {
    category.value.meta_title = category.value.title || ''
  }
  if (!category.value.meta_description) {
    category.value.meta_description = category.value.description || ''
  }
  const prepared: CategoryInterface = {
    ...cleanObject(unref(category))
  }
  if (!props.id) {
    try {
      await store.createCategory(prepared)
      $router().push('/management/categories')
      $notification('Категория добавлена', 'success')
      category.value = {}
    } catch {
      $notification('Ошибка добавления категории', 'error')
    }
  } else {
    try {
      await store.updateCategory(prepared)
      $router().push('/management/categories')
      $notification('Категория Обновлена', 'success')
    } catch {
      $notification('Ошибка обновления', 'error')
    }
  }
}

async function recieveCategory(id: string | undefined) {
  if (id) {
    const response: CategoryInterface | undefined = {
      ...(await store.getCategoryById(id))
    }
    if (response?.id) {
      if (response.image) {
        previewFileList.value.push({
          id: String(response.image.id),
          name: String(response.image.name),
          status: 'finished',
          url: `${config.public.api}${String(response.image.url)}`
        })
        delete response.image
      }
      category.value = response
      loading.value = false
    }
  }
}

recieveCategory(props.id)
</script>
