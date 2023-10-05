<template>
  <n-text class="shop-reply">
    <div v-if="info.length" class="quoted-background p-4">
      <div class="col-12 mb-1"><strong>Информация от магазина:</strong></div>

      <div class="track-info">{{ info }}</div>
    </div>
  </n-text>
</template>

<script lang="ts" setup>
/// ///
// Props
defineProps<{
  info: string
}>()
</script>

<style lang="scss" scoped>
.quoted-background {
  background-color: #fafafc;
}
</style>
