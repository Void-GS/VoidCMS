<template>
  <div
    id="loader"
    class="d-flex align-items-center justify-content-center flex-grow-1"
  >
    <div class="loader-root-container pr-5 scale-in-center">
      <div class="loader-container">
        <div
          v-for="(n, index) in num"
          :key="index"
          class="circle"
          :data-index="n"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const num = 16
</script>

<style scoped lang="scss">
$COUNT: 16;
$SIZE: 120px;
$STEP: calc($SIZE / $COUNT);
$SPEED: 12s;
$COLOR: #cccccc;
$COLORBORDER: #dddddd;

* {
  box-sizing: border-box;
}

.loader-container {
  position: relative;
  display: block;
  width: $SIZE;
  height: $SIZE;
  transform-style: preserve-3d;
  transform: perspective(1000px) rotateY(45deg) rotateX(45deg);
}

@for $n from 0 through $COUNT {
  $localSize: calc($SIZE - ($STEP * $n));
  $offset: calc(($STEP * $n) / 2);

  .circle:nth-child(#{$n}) {
    position: absolute;
    background: transparent;
    border: 2px solid $COLOR;
    border-radius: 50%;
    left: $offset;
    top: $offset;
    width: $localSize;
    height: $localSize;
    animation: spin calc(#{$SPEED} / #{$n}) infinite linear;
  }
}

.circle:nth-child(2n) {
  border: 2px dashed $COLORBORDER;
}

.circle:last-child {
  display: none;
}

@keyframes spin {
  0% {
    transform: rotateX(0deg);
  }
  100% {
    transform: rotateX(360deg);
  }
}
</style>
