
<script setup>
defineProps({
  article: {
    type: Object,
    required: true,
  },
  active: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["select"]);
</script>


<template>
  <div
    class="news-card"
    :class="{ active }"
    @click="$emit('select')"
  >
    <div class="news-date">
      {{ article.date }}
    </div>

    <h3 class="news-title">
      {{ article.title }}
    </h3>

    <p class="news-summary">
      {{ article.summary }}
    </p>

    <div class="read-more">
      En savoir plus →
    </div>
  </div>
</template>

<style scoped>

.news-card {
  background: white;
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 20px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: .25s;
  box-shadow: 0 5px 15px rgba(0,0,0,.08);
}

.news-card:hover{
  transform: translateY(-3px);
  border-color: var(--navy);
}

.news-card.active{
  border-color: var(--navy);
}

.news-date{
  color:#888;
  font-size:13px;
  margin-bottom:10px;
}

.news-title{
  font-size:18px;
  color:#1f2937;
  margin-bottom:12px;
  line-height:1.4;
}

.news-summary{
  color:#666;
  font-size:14px;
  line-height:1.7;
  display:-webkit-box;
  --webkit-line-clamp:4;
  --webkit-box-orient:vertical;
  overflow:hidden;
}

.read-more{
  margin-top:18px;
  color:var(--navy);
  font-weight:600;
}

</style>