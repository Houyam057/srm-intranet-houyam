<script setup>
import { ref, computed } from "vue";

const search = ref("");

const formations = ref([
    { id: 1, title: "Excel Avancé", category: "Bureautique", level: "Intermédiaire", duration: "8 heures", trainer: "Service Informatique", status: "En cours", progress: 65, date: "20 Septembre 2026", places: 12, color: "navy", icon: "📊" },
    { id: 2, title: "Power BI", category: "Business Intelligence", level: "Débutant", duration: "12 heures", trainer: "Consultant BI", status: "Disponible", progress: 0, date: "12 Octobre 2026", places: 18, color: "blue", icon: "📈" },
    { id: 3, title: "Leadership", category: "Management", level: "Avancé", duration: "6 heures", trainer: "Direction RH", status: "Terminée", progress: 100, date: "5 Août 2026", places: 0, color: "green", icon: "👥" },
    { id: 4, title: "CyberSécurité", category: "Sécurité", level: "Intermédiaire", duration: "10 heures", trainer: "DSI", status: "Disponible", progress: 0, date: "30 Septembre 2026", places: 20, color: "red", icon: "🛡️" },
    { id: 5, title: "Gestion des Achats", category: "Achats", level: "Expert", duration: "15 heures", trainer: "Direction Achats", status: "En cours", progress: 45, date: "15 Novembre 2026", places: 10, color: "navy", icon: "📦" },
    { id: 6, title: "Communication Professionnelle", category: "RH", level: "Débutant", duration: "4 heures", trainer: "Direction RH", status: "Disponible", progress: 0, date: "3 Décembre 2026", places: 25, color: "blue", icon: "💬" }
]);

const badges = ref([
    { title: "Excel Expert", icon: "🏆" },
    { title: "Power BI", icon: "📈" },
    { title: "Leadership", icon: "👑" },
    { title: "Cyber", icon: "🛡️" }
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
        <!-- HERO -->
        <section class="hero">
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

        <!-- KPI -->
        <div class="kpi-row">
            <div class="card">
                <div class="card-pad">
                    <div class="kpi">
                        <div class="head"><div class="ic ic-navy">📚</div> Catalogue</div>
                        <div class="val">{{ stats.total }}</div>
                        <div class="lbl">Formations disponibles</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-pad">
                    <div class="kpi">
                        <div class="head"><div class="ic ic-green">✅</div> Terminées</div>
                        <div class="val">{{ stats.completed }}</div>
                        <div class="lbl">Certifiées</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-pad">
                    <div class="kpi">
                        <div class="head"><div class="ic ic-red">⏳</div> En cours</div>
                        <div class="val">{{ stats.progress }}</div>
                        <div class="lbl">Formations actives</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-pad">
                    <div class="kpi">
                        <div class="head"><div class="ic">🏅</div> Badges</div>
                        <div class="val">{{ badges.length }}</div>
                        <div class="lbl">Débloqués</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- RECHERCHE -->
        <div class="card">
            <div class="card-pad">
                <div class="card-h"><h3>Catalogue des formations</h3></div>
                <input v-model="search" class="search-input" placeholder="Rechercher une formation...">
            </div>
        </div>

        <!-- CATALOGUE -->
        <div class="formation-grid">
            <div class="formation-card" v-for="formation in filteredFormations" :key="formation.id">
                <div class="formation-top">
                    <div class="formation-icon" :style="{background:getColor(formation.color)}">{{ formation.icon }}</div>
                    <div>
                        <h3>{{ formation.title }}</h3>
                        <span>{{ formation.category }}</span>
                    </div>
                </div>
                <div class="formation-info">
                    <p>👨‍🏫 {{ formation.trainer }}</p>
                    <p>🎯 {{ formation.level }}</p>
                    <p>⏱ {{ formation.duration }}</p>
                    <p>📅 {{ formation.date }}</p>
                </div>
                <div class="progress-bar"><div class="progress-fill" :style="{width:formation.progress+'%'}"></div></div>
                <div class="progress-label">{{ formation.progress }} %</div>
                <div class="formation-footer">
                    <span class="status" :class="getStatusClass(formation.status)">{{ formation.status }}</span>
                    <button v-if="formation.progress==0" class="btn-primary" @click="inscrire(formation)">S'inscrire</button>
                    <button v-else class="btn-primary" @click="continuer(formation)">Continuer</button>
                </div>
            </div>
        </div>

        <!-- MES FORMATIONS + BADGES -->
        <div class="two-cols">
            <div class="card">
                <div class="card-pad">
                    <div class="card-h"><h3>📖 Mes formations</h3></div>
                    <div class="my-training" v-for="formation in formations.filter(f=>f.progress>0)" :key="'my'+formation.id">
                        <div class="left">
                            <div class="mini-icon" :style="{background:getColor(formation.color)}">{{ formation.icon }}</div>
                            <div>
                                <strong>{{ formation.title }}</strong>
                                <p>{{ formation.progress }}% terminé</p>
                            </div>
                        </div>
                        <div class="right">
                            <div class="mini-progress"><div class="mini-fill" :style="{width:formation.progress+'%'}"></div></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-pad">
                    <div class="card-h"><h3>🏅 Mes badges</h3></div>
                    <div class="badge-grid">
                        <div class="badge-card" v-for="badge in badges" :key="badge.title">
                            <div class="badge-icon">{{ badge.icon }}</div>
                            <div>{{ badge.title }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- CERTIFICATS + RECOMMANDATIONS -->
        <div class="two-cols">
            <div class="card">
                <div class="card-pad">
                    <div class="card-h"><h3>📜 Mes certificats</h3></div>
                    <div class="certificate" v-for="cert in certificats" :key="cert.title">
                        <div>
                            <strong>{{ cert.title }}</strong>
                            <p>Obtenu le {{ cert.date }}</p>
                        </div>
                        <button class="btn-primary">Télécharger</button>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-pad">
                    <div class="card-h"><h3>⭐ Recommandées</h3></div>
                    <div class="recommended" v-for="formation in recommended" :key="'rec'+formation.id">
                        <div class="left">
                            <div class="mini-icon" :style="{background:getColor(formation.color)}">{{ formation.icon }}</div>
                            <div>
                                <strong>{{ formation.title }}</strong>
                                <p>{{ formation.duration }}</p>
                            </div>
                        </div>
                        <button class="btn-primary" @click="inscrire(formation)">Voir</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- COMPÉTENCES -->
        <div class="card">
            <div class="card-pad">
                <div class="card-h"><h3>📈 Mes compétences</h3></div>
                <div class="skill" v-for="skill in competences" :key="skill.name">
                    <div class="skill-header">
                        <span>{{ skill.name }}</span>
                        <strong>{{ skill.value }}%</strong>
                    </div>
                    <div class="skill-bar">
                        <div class="skill-fill" :style="{width:skill.value+'%'}"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- CALENDRIER + PROCHAINES SESSIONS -->
        <div class="two-cols">
            <div class="card">
                <div class="card-pad">
                    <div class="card-h"><h3>📅 Prochaines sessions</h3></div>
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">20 SEP</div>
                            <div class="timeline-content">
                                <strong>Excel Avancé</strong>
                                <p>Salle Formation A • 09:00</p>
                            </div>
                        </div>
                        <div class="timeline-item">
                            <div class="timeline-date">28 SEP</div>
                            <div class="timeline-content">
                                <strong>CyberSécurité</strong>
                                <p>Salle Informatique • 14:00</p>
                            </div>
                        </div>
                        <div class="timeline-item">
                            <div class="timeline-date">05 OCT</div>
                            <div class="timeline-content">
                                <strong>Leadership</strong>
                                <p>Salle Réunion • 09:30</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card">
            <div class="card-pad quote">
                <h2>💡 Citation du mois</h2>
                <blockquote>"L'apprentissage est un trésor qui suivra son propriétaire partout."</blockquote>
            </div>
        </div>
        </div>

        <!-- Citation -->
        
    </div>
</template>

<style scoped>
/* =====================================================
   FORMATION PAGE
===================================================== */

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
.eyebrow {
    display:inline-flex; align-items:center; gap:8px; padding:8px 14px;
    border-radius:50px; background:rgba(255,255,255,.12); font-size:13px;
}
.pills { display:flex; flex-wrap:wrap; gap:12px; margin-top:28px; }
.pills div {
    background:rgba(255,255,255,.15); backdrop-filter:blur(5px);
    border-radius:50px; padding:10px 18px; font-size:14px;
}
.tri-hero { width:90px; height:5px; background:#fff; border-radius:20px; }

/* ================= KPI ================= */
.kpi-row { display:grid; grid-template-columns:repeat(4,1fr); gap:20px; }
.kpi { display:flex; flex-direction:column; gap:10px; }
.kpi .head { display:flex; align-items:center; gap:10px; font-weight:700; color:var(--muted); }
.kpi .val { font-size:34px; font-weight:800; color:var(--navy); }
.kpi .lbl { color:var(--muted); font-size:14px; }
.ic {
    width:42px; height:42px; border-radius:12px; display:flex;
    align-items:center; justify-content:center; background:var(--blue-soft); font-size:20px;
}
.ic-green { background:#dcfce7; }
.ic-red { background:#fee2e2; }
.ic-navy { background:#dbeafe; }

/* ================= SEARCH ================= */
.search-input {
    width:100%; margin-top:15px; border:1px solid var(--line);
    border-radius:12px; padding:14px 18px; outline:none;
    font-size:15px; transition:.25s; background:white;
}
.search-input:focus {
    border-color:var(--blue); box-shadow:0 0 0 4px rgba(37,99,235,.12);
}

/* ================= GRID & CARDS ================= */
.formation-grid {
    display:grid; grid-template-columns:repeat(auto-fill,minmax(330px,1fr)); gap:24px;
}
.formation-card {
    background:#fff; border:1px solid var(--line); border-radius:18px;
    overflow:hidden; transition:.25s; box-shadow:var(--shadow);
}
.formation-card:hover { transform:scale(1.01); border-color:var(--blue); }

.formation-top {
    display:flex; align-items:center; gap:18px; padding:22px;
    border-bottom:1px solid var(--line);
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
.my-training {
    display:flex; justify-content:space-between; align-items:center;
    gap:18px; padding:16px 0; border-bottom:1px solid var(--line);
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
    gap:16px; padding:15px 0; border-bottom:1px solid var(--line);
}
.recommended:last-child { border-bottom:none; }

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

/* Motivation & Quote */
.motivation { text-align:center; }
.motivation-icon {
    width:90px; height:90px; margin:auto; border-radius:50%;
    background:var(--blue-soft); display:flex; align-items:center;
    justify-content:center; font-size:42px; margin-bottom:20px;
}
.quote { text-align:center; }
.quote blockquote {
    font-size:22px; font-style:italic; color:var(--ink);
    max-width:850px; margin:auto; line-height:1.8;
}
.quote blockquote::before { content:"“"; color:var(--blue); font-size:42px; }
.quote blockquote::after { content:"”"; color:var(--blue); font-size:42px; }

/* Buttons & Cards */
.btn-primary:hover { transform:translateY(-2px); }

/* Animations */
.formation-card, .card { animation:fadeUp .45s ease; }
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