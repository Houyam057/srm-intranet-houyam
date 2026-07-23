<script setup>
import { ref, computed, watch } from "vue";
import {Check,Hourglass,Award,LibraryBig,Star,Shield ,UserStar ,ChartColumnBig, Crown  } from 'lucide-vue-next'

const search = ref("");
const pageStart = ref(0);
const cataloguePage = ref(0);
const PAGE_SIZE = 3;
const CATALOGUE_PAGE_SIZE = 5;

watch(search, () => { pageStart.value = 0; cataloguePage.value = 0; });

const formations = ref([
    { id: 1, title: "Excel Avancé", category: "Bureautique", level: "Intermédiaire", duration: "8 heures", trainer: "Service Informatique", status: "En cours", progress: 65, date: "20 Septembre 2026", places: 12, color: "navy", icon: "📊" },
    { id: 2, title: "Power BI", category: "Business Intelligence", level: "Débutant", duration: "12 heures", trainer: "Consultant BI", status: "Disponible", progress: 0, date: "12 Octobre 2026", places: 18, color: "blue", icon: "📈" },
    { id: 3, title: "Leadership", category: "Management", level: "Avancé", duration: "6 heures", trainer: "Direction RH", status: "Terminée", progress: 100, date: "5 Août 2026", places: 0, color: "green", icon: "👥" },
    { id: 4, title: "CyberSécurité", category: "Sécurité", level: "Intermédiaire", duration: "10 heures", trainer: "DSI", status: "Disponible", progress: 0, date: "30 Septembre 2026", places: 20, color: "red", icon: "🛡️" },
    { id: 5, title: "Gestion des Achats", category: "Achats", level: "Expert", duration: "15 heures", trainer: "Direction Achats", status: "En cours", progress: 45, date: "15 Novembre 2026", places: 10, color: "navy", icon: "📦" },
    { id: 6, title: "Communication Professionnelle", category: "RH", level: "Débutant", duration: "4 heures", trainer: "Direction RH", status: "Disponible", progress: 0, date: "3 Décembre 2026", places: 25, color: "blue", icon: "💬" },
]);

const badges = ref([
    { title: "Excel Expert", icon: UserStar  },
    { title: "Power BI", icon: ChartColumnBig },
    { title: "Leadership", icon: Crown },
    { title: "Cyber", icon: Shield }
]);

const certificats = ref([
    { title: "Excel Avancé", date: "10/06/2026" },
    { title: "Communication", date: "22/04/2026" },
    { title: "Power BI", date: "15/02/2026" }
]);

const competences = ref([
    { name: "Excel", value: 95 },
    { name: "Power BI", value: 72 },
    { name: "Python", value: 65 },
    { name: "Leadership", value: 88 },
    { name: "Communication", value: 91 }
]);

const filteredFormations = computed(() => {
    return formations.value.filter(f => 
        f.title.toLowerCase().includes(search.value.toLowerCase()) ||
        f.category.toLowerCase().includes(search.value.toLowerCase())
    );
});

const stats = computed(() => {
    const total = formations.value.length;
    const completed = formations.value.filter(f => f.progress === 100).length;
    const progress = formations.value.filter(f => f.progress > 0 && f.progress < 100).length;
    const available = formations.value.filter(f => f.progress === 0).length;

    return { total, completed, progress, available };
});

const recommended = computed(() => {
    return formations.value.filter(f => f.progress === 0).slice(0, 3);
});

const mesFormations = computed(() => formations.value.filter(f => f.progress > 0));
const visibleMesFormations = computed(() => mesFormations.value.slice(0, pageStart.value + PAGE_SIZE));
const hasMoreMesFormations = computed(() => pageStart.value + PAGE_SIZE < mesFormations.value.length);

function loadMoreMesFormations() {
    pageStart.value += PAGE_SIZE;
}

const visibleCatalogue = computed(() => filteredFormations.value.slice(0, cataloguePage.value + CATALOGUE_PAGE_SIZE));
const hasMoreCatalogue = computed(() => cataloguePage.value + CATALOGUE_PAGE_SIZE < filteredFormations.value.length);

function loadMoreCatalogue() {
    cataloguePage.value += CATALOGUE_PAGE_SIZE;
}

function inscrire(formation) {
    formation.status = "Inscrit";
    alert("Vous êtes inscrit à : " + formation.title);
}

function continuer(formation) {
    alert("Ouverture de : " + formation.title);
}

function getStatusClass(status) {
    switch (status) {
        case "Terminée": return "success";
        case "En cours": return "warning";
        case "Disponible": return "primary";
        case "Inscrit": return "info";
        default: return "";
    }
}

function getColor(color) {
    switch (color) {
        case "navy": return "#0f2f6b";
        case "green": return "#2e9e4f";
        case "red": return "#e2231a";
        default: return "#1f5fd6";
    }
}
</script>

<template>
    <div class="page show formation-page">
        <div class="crumbs">
            Accueil <span class="sep">›</span>
            <span class="cur">Formations & Compétences</span>
        </div>
        <!-- HERO -->
     <!--   <section class="hero">
            <div class="bg"></div>
            <div class="content">
                <div class="eyebrow">Plateforme de Formation</div>
                <h1>Formation & Compétences</h1>
                <div class="tri-hero"></div>
                <p class="sub">Développez vos compétences professionnelles grâce aux formations internes SRM-TTA.</p>
                <div class="pills">
                    <div>📚 {{ stats.total }} formations</div>
                    <div>🏆 {{ stats.completed }} terminées</div>
                    <div>📈 Développement continu</div>
                </div>
            </div>
        </section>
    -->
        <!-- KPI -->
        <div class="kpi-row">
            <div class="card-grid" >
            <div class="card">
                <div class="card-pad">
                    <div class="kpi" style="border: transparent;">
                        <div class="head"><div class="ic ic-navy"><LibraryBig /></div> <h2>Catalogue</h2></div>
                        <div class="val">{{ stats.total }}</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-pad">
                    <div class="kpi" style="border: transparent;">
                        <div class="head"><div class="ic ic-green"><Check /></div> <h2>Terminées</h2></div>
                        <div class="val">{{ stats.completed }}</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-pad">
                    <div class="kpi" style="border: transparent;">
                        <div class="head"><div class="ic ic-gold"><Hourglass /></div> <h2>En cours</h2></div>
                        <div class="val">{{ stats.progress }}</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-pad">
                    <div class="kpi" style="border: transparent;">
                        <div class="head"><div class="ic ic-blue"><Star /></div> <h2>Compétences</h2></div>
                        <div class="val">{{ badges.length }}</div>
                    </div>
                </div>
            </div>    
        </div>
        <div class="card">
                <div class="card-pad">
                    <div class="card-h"><h3>Mes Compétences</h3></div>
                    <div class="badge-grid">
                        <div class="badge-card" v-for="badge in badges" :key="badge.title">
                            <div class="badge-icon">  <component :is="badge.icon" :size="32" /></div>
                            <div>{{ badge.title }}</div>
                        </div>
                    </div>
                </div>
        </div>
            <div class="card">
                <div class="card-pad">
                    <div class="card-h"><h3>Mes formations</h3></div>
                    <div class="mes-formations-list">
                        <div class="my-training" v-for="formation in visibleMesFormations" :key="'my2'+formation.id">
                            <div class="left">
                                <div class="mini-icon" :style="{background:getColor(formation.color)}">{{ formation.icon }}</div>
                                <div>
                                    <strong>{{ formation.title }}</strong>
                                    <p>{{ formation.progress }}% terminé</p>
                                </div>
                            </div>

                        </div>
                        <div v-if="hasMoreMesFormations" class="load-more" @click="loadMoreMesFormations">
                            <span>Voir plus</span>
                            <span class="arrow">↓</span>
                        </div>
                    </div>
                </div>
            </div>
    </div>

        <!-- RECHERCHE -->
        <div class="card" style="padding: 2%;">
            <div class="card-pad">
                <div class="card-h"><h3>Rechercher la formation que vous souhaiter</h3></div>
                <input v-model="search" class="search-input" placeholder="Rechercher une formation...">
            </div>

        <!-- CATALOGUE -->
        <div class="catalogue-list" :class="{ 'catalogue-scrollable': hasMoreCatalogue }">
        <div class="formation-grid">
            <div class="formation-card" v-for="formation in visibleCatalogue" :key="formation.id">
                <div class="formation-top">
                    <div class="formation-icon" :style="{background:getColor(formation.color)}">{{ formation.icon }}</div>
                    <div style="    grid-column: span 2;">
                        <h3>{{ formation.title }}</h3>
                        <span>{{ formation.category }}</span>
                    </div>
                </div>
                <div class="formation-footer">
                    <span class="status" :class="getStatusClass(formation.status)">{{ formation.status }}</span>
                    <button v-if="formation.progress==0" class="btn-primary" @click="inscrire(formation)">S'inscrire</button>
                    <button v-else class="btn-primary" @click="continuer(formation)">Continuer</button>
                </div>
            </div>
            <div v-if="hasMoreCatalogue" class="load-more catalogue-load-more" @click="loadMoreCatalogue">
                <span>Voir plus</span>
                <span class="arrow">↓</span>
            </div>
        </div>
        </div>
    </div>

        <!-- MES FORMATIONS + BADGES -->
    </div>
</template>

<style scoped>


.formation-page { display:flex; flex-direction:column; gap:24px; }

/* ================= HERO ================= */
.hero {
    position:relative; overflow:hidden; border-radius:var(--radius); min-height:260px;
    color:#fff; background:linear-gradient(135deg,var(--navy),var(--blue)); box-shadow:var(--shadow);
}
.hero .bg {
    position:absolute; inset:0; opacity:.08;
    background: radial-gradient(circle at top right,#fff 2px,transparent 2px),
                radial-gradient(circle at bottom left,#fff 2px,transparent 2px);
    background-size:35px 35px;
}
.hero .content { position:relative; z-index:2; padding:42px; }
.hero h1 { margin:12px 0; font-size:42px; font-weight:800; }
.hero .sub { margin-top:12px; max-width:760px; line-height:1.7; opacity:.92; }
.hero .eyebrow {
    display:inline-flex; align-items:center; gap:8px; padding:8px 14px;
    border-radius:50px; background:rgba(255,255,255,.12); font-size:13px;
}
.hero .pills { display:flex; flex-wrap:wrap; gap:12px; margin-top:28px; }
.hero .pills div {
    background:rgba(255,255,255,.15); backdrop-filter:blur(5px);
    border-radius:50px; padding:10px 18px; font-size:14px;
}
.hero .tri-hero { width:90px; height:5px; background:#fff; border-radius:20px; }

/* ================= KPI ================= */
.kpi-row { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; }
.kpi { display:flex; flex-direction:column; gap:10px; }
.kpi .head { display:flex; align-items:center; gap:10px; font-weight:700; color:var(--muted); }
.kpi .val { font-size:32px;font-weight:800;letter-spacing:.5px }
.kpi .lbl { color:var(--muted); font-size:14px; }

.card-grid{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: 1fr 1fr;
  gap: 7px;
}
/* ================= SEARCH ================= */
.search-input {
    width:100%; margin-top:15px; border:2px solid var(--line);
    border-radius:12px; padding:14px 18px; outline:none;
    font-size:15px; transition:.25s; background:white;
}
.search-input:focus {
    border-color:var(--blue); box-shadow:0 0 0 4px rgba(37,99,235,.12);
}

/* ================= GRID & CARDS ================= */
.catalogue-scrollable {
    max-height: 460px;
    overflow-y: auto;
    scrollbar-gutter: stable;
}
.catalogue-load-more {
    min-height: 200px;
    height: auto;
    margin-top: 0;
    border:2px dashed var(--line); border-radius:18px;
}
.formation-grid {
    display:grid; grid-template-columns:repeat(auto-fill,minmax(330px,1fr)); gap:24px;margin:10px;
}
.formation-card {
    background:#fff; border:1px solid var(--line); border-radius:18px;
    overflow:hidden; transition:.25s; box-shadow:var(--shadow);
}
.formation-card:hover { transform:scale(1.01); border-color:var(--blue); }

.formation-top {
    display:grid;
    grid-template-columns: 1fr 1fr 1fr;
    align-items:center; gap:18px; padding:22px;
}

.formation-icon {
    width:64px; height:64px; border-radius:16px; color:white;
    display:flex; align-items:center; justify-content:center;
    font-size:28px; flex:none;
}
.formation-top h3 { margin:0; color:var(--ink); font-size:20px; }
.formation-top span { color:var(--muted); font-size:14px; }

.formation-info { padding:20px 22px; }
.formation-info p { margin:10px 0; color:var(--muted); }

.progress-bar {
    margin:0 22px; height:10px; background:#edf2f7;
    border-radius:20px; overflow:hidden;
}
.progress-fill {
    height:100%; border-radius:20px;
    background:linear-gradient(90deg, var(--blue), #4f8df7);
}
.progress-label { padding:10px 22px; color:var(--muted); font-size:13px; }

.formation-footer {
    display:flex; justify-content:space-between; align-items:center;
    padding:18px 22px 22px;
}

/* Status */
.status {
    padding:7px 14px; border-radius:30px; font-size:13px; font-weight:700;
}
.status.success { background:#dcfce7; color:#15803d; }
.status.warning { background:#fef3c7; color:#b45309; }
.status.primary { background:#dbeafe; color:#1d4ed8; }
.status.info { background:#ede9fe; color:#6d28d9; }

/* Layout */
.two-cols { display:grid; grid-template-columns:2fr 1fr; gap:22px; }

/* Mes formations */
.mes-formations-list {
    max-height: calc(4 * 78px);
    overflow-y: auto;
    scrollbar-gutter: stable;
}
.my-training {
    display:flex; justify-content:space-between; align-items:center;
    gap:18px; padding:16px 0; height:78px; box-sizing:border-box;
    border-bottom:1px solid var(--line);
}
.my-training:last-child { border-bottom:none; }
.left { display:flex; align-items:center; gap:15px; }
.mini-icon {
    width:46px; height:46px; border-radius:12px; color:#fff;
    display:flex; align-items:center; justify-content:center; font-size:22px;
}
.mini-progress {
    height:8px; background:#edf2f7; border-radius:20px; overflow:hidden;
}
.mini-fill {
    height:100%; background:linear-gradient(90deg, #16a34a, #4ade80);
}

/* Badges */
.badge-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:15px; }
.badge-card {
    border:1px solid var(--line); border-radius:14px; padding:18px;
    text-align:center; transition:.25s; cursor:pointer;
}
.badge-card:hover { transform:scale(1.01); border-color:var(--blue); box-shadow:var(--shadow); }
.badge-icon { font-size:38px; margin-bottom:12px; }

/* Certificats */
.certificate {
    display:flex; justify-content:space-between; align-items:center;
    padding:18px 0; border-bottom:1px solid var(--line);
}
.certificate:last-child { border-bottom:none; }

/* Recommandations */
.recommended {
    display:flex; justify-content:space-between; align-items:center;
    gap:16px; padding:22px 0; border-bottom:1px solid var(--line);
}
.recommended:last-child { border-bottom:none; }
.recommended .left { gap:18px; }
.recommended .mini-icon { width:54px; height:54px; font-size:26px; }
.recommended strong { font-size:16px; }
.recommended p { margin-top:4px; }

/* Compétences */
.skill { margin-top:18px; }
.skill-header { display:flex; justify-content:space-between; margin-bottom:8px; }
.skill-bar {
    height:10px; background:#edf2f7; border-radius:30px; overflow:hidden;
}
.skill-fill {
    height:100%; border-radius:30px;
    background:linear-gradient(90deg, var(--blue), #67a5ff);
}

/* Timeline */
.timeline { display:flex; flex-direction:column; gap:20px; }
.timeline-item {
    display:flex; align-items:flex-start; gap:18px; position:relative;
}
.timeline-item:not(:last-child)::before {
    content:""; position:absolute; left:32px; top:60px;
    width:2px; height:calc(100% + 12px); background:var(--line);
}
.timeline-date {
    width:64px; height:64px; flex:none; border-radius:16px;
    background:linear-gradient(135deg,var(--navy),var(--blue)); color:#fff;
    display:flex; align-items:center; justify-content:center;
    font-weight:700; box-shadow:var(--shadow);
}

/* Quote */
.quote { text-align:center; }
.quote blockquote {
    font-size:22px; font-style:italic; color:var(--ink);
    max-width:850px; margin:auto; line-height:1.8;
}
.quote blockquote::before { content:"\201C"; color:var(--blue); font-size:42px; }
.quote blockquote::after { content:"\201D"; color:var(--blue); font-size:42px; }

/* Load More */
.load-more {
    display:flex; align-items:center; justify-content:center; gap:10px;
    padding:0; height:78px; box-sizing:border-box; margin-top:0;
    border:2px dashed var(--line); border-radius:12px;
    cursor:pointer; transition:.25s;
}
.load-more:hover { border-color:var(--blue); background:var(--blue-soft); }
.load-more span { font-weight:700; color:var(--navy); font-size:14px; }
.load-more .arrow { font-size:18px; animation:bounce 1.5s infinite; }
@keyframes bounce {
    0%,100% { transform:translateY(0); }
    50% { transform:translateY(4px); }
}

/* Animations */
.formation-card { animation:fadeUp .45s ease; }
@keyframes fadeUp {
    from { opacity:0; transform:translateY(18px); }
    to { opacity:1; transform:translateY(0); }
}

/* Responsive */
@media(max-width:1200px) { .kpi-row { grid-template-columns:repeat(2,1fr); } }
@media(max-width:900px) {
    .two-cols, .formation-grid { grid-template-columns:1fr; }
}
@media(max-width:768px) {
    .hero .content { padding:28px; }
    .hero h1 { font-size:30px; }
    .kpi-row { grid-template-columns:1fr; }
    .formation-top, .formation-footer, .my-training, .recommended, .certificate { flex-direction:column; align-items:flex-start; }
    .right { width:100%; }
}
@media(max-width:500px) {
    .hero h1 { font-size:26px; }
    .timeline-item { flex-direction:column; }
    .timeline-item::before { display:none; }
}
</style>