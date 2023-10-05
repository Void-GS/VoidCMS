<template>
  <n-collapse>
    <n-collapse-item title="SEO параметры">
      <div class="px-4">
        <span>
          Вы можете оставить поля пустыми, тогда они будут заполнены
          автоматически на основе введенного имени и описания
        </span>
        <n-form-item class="mt-4" path="meta_url" label="Короткий адрес">
          <n-input
            :value="item.meta_url"
            placeholder="Введите seo адрес"
            @input="updateItem('meta_url', $event)"
          />
        </n-form-item>
        <n-form-item path="meta_title" label="Заголовок">
          <n-input
            :value="item.meta_title"
            placeholder="Введите seo заголовок"
            @input="updateItem('meta_title', $event)"
          />
        </n-form-item>
        <n-form-item path="meta_description" label="Описание">
          <n-input
            :value="item.meta_description"
            placeholder="Введите seo описание"
            @input="updateItem('meta_description', $event)"
          />
        </n-form-item>
        <n-form-item path="meta_keywords" label="Ключевые слова">
          <n-input
            :value="item.meta_keywords"
            placeholder="Введите seo ключевые слова категории через запятую ,"
            @input="updateItem('meta_keywords', $event)"
          />
        </n-form-item>
        <n-blockquote align-text>
          SEO необходим для грамотной индексации вашего страницы, продукта или
          категории в глобальных поисковиках таких как Google, Yandex и др.
        </n-blockquote>
      </div>
    </n-collapse-item>
  </n-collapse>
</template>

<script lang="ts" setup>
import type { CategoryInterface } from '~/interfaces/category'
import type { PageInterface } from '~/interfaces/page'
import type { ProductInterface } from '~/interfaces/product'

const props = defineProps<{
  item: CategoryInterface | ProductInterface | PageInterface
}>()

const emit = defineEmits(['update:item'])

function updateItem(
  key: 'meta_title' | 'meta_description' | 'meta_url' | 'meta_keywords',
  value: string
) {
  const updatedItem = Object.assign({}, props.item)
  updatedItem[key] = value
  emit('update:item', updatedItem)
}
</script>
