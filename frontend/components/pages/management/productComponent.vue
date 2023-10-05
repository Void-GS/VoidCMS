<template>
  <n-card class="page-card new-category-card" size="huge">
    <n-h2> {{ id ? 'Редактирование' : 'Добавление' }} товара: </n-h2>
    <n-divider />

    <n-form ref="formRef" :model="product" size="large">
      <n-form-item path="image" label="Изображения товара">
        <n-upload
          :file-list="previewFileList"
          list-type="image-card"
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
          v-model:value="product.title"
          placeholder="Введите название товара"
        />
      </n-form-item>
      <n-form-item path="category" label="Категория">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-select
          v-else
          v-model:value="product.category"
          filterable
          clearable
          placeholder="Выберите или начните вводить"
          :options="categoriesGetter"
          value-field="id"
          label-field="title"
        />
      </n-form-item>
      <n-form-item path="content" label="Описание товара">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <div class="quill-editor-container w-100">
          <QuillEditor
            v-model:content="product.content"
            content-type="html"
            theme="snow"
          />
        </div>
      </n-form-item>
      <ComplectationOptions
        :loading="loading"
        :complectations-prop="product.complectations"
        @update="handleUpdateComplectations"
      />
      <div class="d-flex justify-content-between align-items-center flex-wrap">
        <n-form-item path="price" label="Цена товара">
          <n-skeleton
            v-if="loading"
            :width="280"
            size="medium"
            :sharp="false"
          />
          <n-input-number
            v-else
            v-model:value="price"
            :parse="parseCurrency"
            :format="formatCurrency"
            placeholder="Укажите цену"
          >
            <template #prefix> ₽ </template>
          </n-input-number>
        </n-form-item>
        <n-form-item path="visible" class="ms-sm-4" label="Отображение товара">
          <n-switch
            v-model:value="product.visible"
            size="large"
            :disabled="loading"
          >
            <template #checked> Видимый </template>
            <template #unchecked> Невидимый </template>
          </n-switch>
        </n-form-item>
        <n-form-item path="is_promotioned" label="Добавить в рекламный блок">
          <n-switch
            v-model:value="product.is_promotioned"
            size="large"
            :disabled="loading"
          >
            <template #checked> Да </template>
            <template #unchecked> Нет </template>
          </n-switch>
        </n-form-item>
      </div>
      <SeoInputs v-if="!loading" v-model:item="product" />
      <div class="category-actions mt-4 float-end">
        <n-button type="tertiary" :disabled="loading" @click="handleCategory">
          {{ id ? 'Обновить' : 'Добавить' }} товар
        </n-button>
      </div>
    </n-form>
  </n-card>
</template>

<script lang="ts" setup>
import type { UploadFileInfo } from 'naive-ui'

import type {
  ComplectationInterface,
  ProductInterface
} from '~/interfaces/product'
import { useStoreProducts } from '~/store/products'
import { useStoreCategories } from '~/store/categories'
import { sanitizeText } from '~/utils/sanitize'

import '@vueup/vue-quill/dist/vue-quill.snow.css'

/// ///
// Components
const ComplectationOptions = defineAsyncComponent(
  () => import('~/components/ui/management/complectationOptions.vue')
)

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
const store = useStoreProducts()
const storeCategories = useStoreCategories()
const { categoriesGetter } = storeToRefs(storeCategories)
const product = ref<ProductInterface>({})
const price = ref<number>(0)
const showModal = ref(false)
const previewImageUrl = ref('')
const loading = ref<boolean>(false)
const { vueApp } = useNuxtApp()

if (!process.server) {
  const { QuillEditor } = await import('@vueup/vue-quill')
  if (!vueApp._context.components.QuillEditor)
    vueApp.component('QuillEditor', QuillEditor)
}

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
  product.value.images_upload = evt.map((i) => i.file as File).filter(Boolean)
}

function parseCurrency(input: string) {
  const nums = input.replace(/(,|\$|\s)/g, '').trim()
  if (/^\d+(\.(\d+)?)?$/.test(nums)) return Number(nums)
  return nums === '' ? null : Number.NaN
}

function formatCurrency(value: number | null) {
  if (value === null) return ''
  return `${value.toLocaleString('en-EN')}`
}

async function handleCategory(e: MouseEvent) {
  e.preventDefault()
  if (!product.value.meta_url) {
    product.value.meta_url = translit(product.value.title || '')
  }
  if (!product.value.meta_title) {
    product.value.meta_title = product.value.title || ''
  }
  if (!product.value.meta_description) {
    product.value.meta_description = sanitizeText(product.value.content || '')
  }
  product.value.price = String(price.value)
  const prepared: ProductInterface = { ...cleanObject(unref(product)) }
  if (!props.id) {
    try {
      await store.createProduct(prepared)
      $router().push('/management/products')
      $notification('Товар добавлен', 'success')
      product.value = {}
    } catch {
      $notification('Ошибка добавления товара', 'error')
    }
  } else {
    try {
      await store.updateProduct(prepared)
      $router().push('/management/products')
      $notification('Товар обновлен', 'success')
    } catch {
      $notification('Ошибка обновления товара', 'error')
    }
  }
}

async function recieveProduct(id: string | undefined) {
  if (id) {
    const response: ProductInterface | undefined = {
      ...(await store.getProductById(id))
    }
    if (response?.id) {
      if (response.images && response.images.length) {
        previewFileList.value = response.images.map((i) => {
          return {
            id: String(i.id),
            name: String(i.name),
            status: 'finished',
            url: `${config.public.api}${String(i.url)}`
          }
        })
        delete response.images
      }
      if (typeof response.price === 'string') {
        price.value = Number(response.price)
      }
      product.value = response
      loading.value = false
    }
  }
}

function handleUpdateComplectations(evt: ComplectationInterface[]) {
  product.value.complectations = evt
}

await recieveProduct(props.id)
await storeCategories.getCategories()
</script>

<style lang="scss">
.quill-editor-container,
.ql-editor {
  min-height: 220px;
}
</style>
