<template>
  <div id="footer" class="footer-container mt-5">
    <div
      v-if="socials.length"
      class="footer-socials d-flex align-items-center justify-content-center flex-wrap flex-md-nowrap"
    >
      <div
        v-for="social in socials"
        :key="social.type"
        class="footer-social d-flex align-items-center justify-content-center mx-4"
      >
        <nuxt-link :to="social.url">
          <n-icon size="24" color="#323232">
            <component :is="socialTypeToIcon(social.type)" />
          </n-icon>
        </nuxt-link>
      </div>
    </div>
    <div
      v-if="pagesGetter.length"
      class="footer-links d-flex align-items-center justify-content-center justify-content-md-center flex-wrap flex-md-nowrap mt-3"
    >
      <div
        v-for="page in pagesGetter"
        :key="page.meta_url"
        class="footer-link mx-4"
      >
        <nuxt-link :to="`/pages/${page.meta_url}`">
          <strong>{{ page.name }}</strong>
        </nuxt-link>
      </div>
    </div>
    <div class="footer-info mt-3 mb-3 px-3">
      {{
        settingsByMetaGetter?.app_name ||
        'Необходима настройка параметров домена'
      }}© {{ new Date().getFullYear() }}. Все права защищены.
    </div>
  </div>
</template>

<script lang="ts" setup>
/// ///
// Variables
const pagesStore = storePages()
const { pagesGetter } = storeToRefs(pagesStore)
const socialsStore = storeSocials()
const { socials } = storeToRefs(socialsStore)
const { settingsByMetaGetter } = storeToRefs(storeSettings())

await pagesStore.getPages()
await socialsStore.getSocials()
</script>

<style lang="scss" scoped>
.footer-links {
  text-transform: uppercase;
  color: #3c3c3c;
  a {
    text-decoration: none;
  }
}
.footer-info {
  color: #c1c1c1;
  text-align: center;
  a {
    color: #c1c1c1;
  }
}
</style>
