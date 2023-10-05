<template>
  <Profile class="navbar-compensation" />
</template>

<script lang="ts" setup>
const Profile = defineAsyncComponent(
  () => import('~/components/pages/profile/ProfileCardComponent.vue')
)
</script>
