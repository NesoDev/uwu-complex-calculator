<template>
  <div class="home-page">
    <ComplexityAnalyzer />
  </div>
</template>

<script>
import ComplexityAnalyzer from '@/components/ComplexityAnalyzer.vue'

export default {
  name: 'HomePage',
  components: {
    ComplexityAnalyzer
  }
}
</script>

<style scoped>
.home-page {
  padding: 20px;
}
</style>
