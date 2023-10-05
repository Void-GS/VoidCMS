<template>
  <n-button tertiary size="medium" @click="activate(true)">
    <template #icon>
      <n-icon><SearchOutline /></n-icon>
    </template>
  </n-button>
  <n-config-provider :theme="darkTheme">
    <n-modal
      id="search-modal"
      v-model:show="active"
      transform-origin="center"
      :bordered="false"
      class="search-modal user-select-none p-4 col-12 col-md-8 col-lg-7 col-xl-6"
      style="position: fixed; top: 5%; left: 0; right: 0"
      :on-update:show="activate"
    >
      <div class="content d-flex flex-column" :class="{ active }">
        <form class="search-input col-12">
          <n-input
            ref="barRef"
            v-model="query"
            placeholder="Поиск..."
            type="text"
            size="large"
            @input="searchQuery"
          >
            <template #prefix>
              <n-icon class="me-2" color="white" size="22">
                <SearchOutline />
              </n-icon>
            </template>
          </n-input>
        </form>
        <div class="search-results-container mt-4">
          <n-scrollbar
            style="max-height: 75vh"
            class="d-flex flex-column"
            trigger="none"
          >
            <template
              v-if="!search?.categories?.length && !search?.products?.length"
            >
              <div
                class="d-flex flex-grow-1 align-items-center justify-content-center"
              >
                <n-empty
                  :description="
                    query
                      ? 'По вашему запросу нет совпадений'
                      : 'Введите поисковый запрос'
                  "
                />
              </div>
            </template>
            <div v-else class="search-results pb-3">
              <div v-if="search.categories?.length" class="search-categories">
                <n-h3 class="d-flex align-items-center px-3 mt-3 mb-3">
                  <n-icon size="22" class="me-3">
                    <LibraryOutline />
                  </n-icon>
                  Категории
                </n-h3>
                <n-divider class="my-0 mb-4" />

                <SearchItem
                  v-for="category in search.categories"
                  :key="category.id"
                  class="px-2 mb-2"
                  :category="category"
                  @update="activate(false)"
                />
              </div>
              <div v-if="search.products?.length" class="search-products mt-4">
                <n-h3 class="d-flex align-items-center px-3 mt-3 mb-3">
                  <n-icon size="22" class="me-3">
                    <CubeOutline />
                  </n-icon>
                  Товары
                </n-h3>
                <n-divider class="my-0 mb-4" />
                <SearchItem
                  v-for="product in search.products"
                  :key="product.id"
                  class="px-2 mb-2"
                  :product="product"
                  @update="activate(false)"
                />
              </div>
            </div>
          </n-scrollbar>
        </div>
      </div>
    </n-modal>
  </n-config-provider>
</template>

<script lang="ts" setup>
import { darkTheme } from 'naive-ui'

import { CubeOutline, LibraryOutline, SearchOutline } from '@vicons/ionicons5'

/// ///
// Components
const SearchItem = defineAsyncComponent(
  () => import('~/components/ui/layout/SearchItemComponent.vue')
)

/// ///
// Variables
const barRef = ref<HTMLInputElement>()
const active = ref<boolean>(false)
const query = ref<String>('')
const searchStore = storeSearch()
const { search } = storeToRefs(searchStore)
let searchTimer: ReturnType<typeof setTimeout> | null = null

/// ///
// Functions
function activate(value: boolean) {
  active.value = value
  if (active.value) {
    nextTick(() => {
      barRef.value?.focus()
    })
  } else {
    nextTick(() => {
      barRef.value?.blur()
      query.value = ''
      searchStore.clearResults()
    })
  }
}

function searchQuery(evt: string) {
  if (searchTimer) {
    clearTimeout(searchTimer)
  }

  searchTimer = setTimeout(() => {
    query.value = evt
    searchStore.getResults(query.value)
  }, 450)
}
</script>

<style lang="scss" scoped>
.search-input {
  opacity: 0;
  transform: translateY(-200px);
  transition: opacity 0.3s ease-out, transform 0.3s ease-out;
}

.active {
  .search-input {
    opacity: 1;
    transform: translateY(0);
    transition: opacity 0.3s ease-out, transform 0.3s ease-out;
  }
}
</style>
