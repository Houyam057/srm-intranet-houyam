<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import NewsCard from "@/components/NewsCard.vue";
import OCRService from "@/services/ocrService";
import ParserService from "@/services/parserService";

// Assurez-vous d'importer votre icône depuis votre bibliothèque (ex: lucide-vue-next)
import { ArrowUpDown  , Repeat2 } from "lucide-vue-next"; 

const articles = ref([]);
const selectedArticle = ref(null);

// Gestion du défilement
const sidebarRef = ref(null);
let animationFrameId = null;
let currentScroll = 0;
const scrollSpeed = 0.2; 

// États pour votre bouton custom
const isLoopMode = ref(true);
const isScrollMode = computed(() => !isLoopMode.value); // Si ce n'est pas en loop, c'est en manuel

async function loadFlashInfos() {
  const cache = localStorage.getItem("flashInfos");
  if (cache) {
    articles.value = JSON.parse(cache);
    selectedArticle.value = articles.value[0];
    if (isLoopMode.value) startContinuousScroll();
    return;
  }

  const files = ["1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png"];
  const result = [];

  for (const file of files) {
    const ocr = await OCRService.extract(`/flashinfos/${file}`);
    const article = ParserService.parse(ocr, file);
    result.push(article);
  }

  articles.value = result;
  localStorage.setItem("flashInfos", JSON.stringify(result));
  if (result.length) {
    selectedArticle.value = result[0];
    if (isLoopMode.value) startContinuousScroll();
  }
}

// Votre fonction de bascule
function toggleViewMode() {
  isLoopMode.value = !isLoopMode.value;
  if (isLoopMode.value) {
    startContinuousScroll();
  } else {
    stopContinuousScroll();
  }
}

function handleManualScroll(event) {
  if (isScrollMode.value) {
    currentScroll = event.target.scrollTop;
  }
}

function startContinuousScroll() {
  if (!sidebarRef.value || !articles.value.length) return;

  const scroll = () => {
    if (sidebarRef.value) {
      currentScroll += scrollSpeed;
      sidebarRef.value.scrollTop = currentScroll;

      if (currentScroll >= sidebarRef.value.scrollHeight / 2) {
        currentScroll = 0;
        sidebarRef.value.scrollTop = 0;
      }
    }
    animationFrameId = requestAnimationFrame(scroll);
  };

  stopContinuousScroll(); 
  animationFrameId = requestAnimationFrame(scroll);
}

function stopContinuousScroll() {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
}

onMounted(loadFlashInfos);

onUnmounted(() => {
  stopContinuousScroll();
});
</script>

<template>
  <div class="flash-page">
    <div class="crumbs">
        Accueil <span class="sep">›</span>
        <span class="cur">Flash Infos</span>
        <div class="sidebar-controls">
          <button
            type="button"
            class="offers-toggle"
            :aria-pressed="isScrollMode"
            @click="toggleViewMode"
          >
            <ArrowUpDown   v-if="isLoopMode" :size="15" />
            <Repeat2     v-else :size="15" /> <span>{{ isLoopMode ? 'Scroll' : 'Loop' }}</span>
          </button>
        </div>
    </div>
    

    <div class="flash-container">
      <div class="viewer">
        <img
          v-if="selectedArticle"
          :src="selectedArticle.image"
          class="flash-image"
        />
        <div v-else class="placeholder">Chargement des images...</div>
      </div>

      <div class="sidebar-wrapper">
        <div 
          ref="sidebarRef" 
          class="sidebar"
          :class="{ 'scroll-manual': isScrollMode }"
          @mouseenter="isLoopMode && stopContinuousScroll()"
          @mouseleave="isLoopMode && startContinuousScroll()"
          @scroll="handleManualScroll"
        >
          <div class="scroll-content">
            <NewsCard
              v-for="article in articles"
              :key="'original-' + article.id"
              :article="article"
              :active="selectedArticle?.id === article.id"
              @select="selectedArticle = article"
            />
            
            <NewsCard
              v-for="article in articles"
              :key="'clone-' + article.id"
              :article="article"
              :active="selectedArticle?.id === article.id"
              @select="selectedArticle = article"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.flash-page { padding:40px; background:#f6f7fb; min-height:100vh; }
.page-header { margin-bottom:30px; }
.page-header h1 { font-size:34px; margin-bottom:8px; }
.page-header p { color:#777; }

.flash-container { display:grid; grid-template-columns:3fr 1fr; gap:30px; }

.viewer {
  background:white;
  border-radius:18px;
  padding:20px;
  box-shadow:0 10px 25px rgba(0,0,0,.08);
  min-height:620px;
  display:flex;
  align-items:center;
  justify-content:center;
}

.flash-image { width:100%; border-radius:12px; }
.placeholder { color:#888; font-style:italic; }

.sidebar-wrapper {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.sidebar-controls {
  display: flex;
  justify-content: flex-end;
  margin-left:auto;
}

/* --- VOTRE CSS EXACT --- */
.offers-toggle {
  position: relative;
  z-index: 3;
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm, 6px); /* Ajout d'un fallback si la variable n'est pas définie */
  border: none;
  border-radius: var(--radius-sm, 4px);
  padding-block: var(--space-sm, 6px);
  padding-inline: 0.75rem var(--space-md, 12px);
  background-color: var(--navy);
  color: var(--color-background, #ffffff);
  font-size: var(--font-size-xs, 12px);
  font-weight: var(--font-medium, 500);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.26);
  cursor: pointer;
  transition:
    background-color var(--transition-fast, 0.2s),
    box-shadow var(--transition-fast, 0.2s),
    transform var(--transition-fast, 0.2s);
}

.offers-toggle:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.3);
}

.offers-toggle[aria-pressed="true"] {
  background-color: #333; /* Exemple de couleur quand le mode manuel est activé */
}
/* ----------------------- */

.sidebar { 
  height: calc(85vh - 40px);
  overflow: hidden; 
  padding-right: 8px; 
}

.sidebar.scroll-manual {
  overflow-y: auto;
}

.sidebar.scroll-manual::-webkit-scrollbar { width: 6px; }
.sidebar.scroll-manual::-webkit-scrollbar-track { background: transparent; }
.sidebar.scroll-manual::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.sidebar.scroll-manual::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

.scroll-content {
  display: flex;
  flex-direction: column;
  gap: 15px; 
}
</style>