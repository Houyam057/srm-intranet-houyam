<script setup>
import { reactive, ref } from "vue";
import { MapPin, Phone } from "lucide-vue-next";

const form = reactive({
    subject: "",
    category: "",
    message: ""
});

function submitForm() {
    console.log(form);

    // Appel API ici

    alert("Votre demande a été envoyée.");

    const { subject, category, message } = form;
    
    emit('submit',{
            subject,
            category,
            message
    })
}


const open = ref(false);


const categories = [
    "Support informatique",
    "Ressources Humaines",
    "Maintenance",
    "Suggestion",
    "Autre"
];


function selectCategory(category) {

    form.category = category;

    open.value = false;
}
</script>
<template>
    <div class="page page-direction show">
        <div class="crumbs">
            Accueil <span class="sep">›</span>
            <span class="cur">HelpDesk</span>
        </div>
        <section class="sections">
            <div class="large-div" style="margin-left:14px; margin-right:14px; margin-top:5px;">
                <div class="card-h">
                    <h3>Besoin d'aide ?</h3>
                </div>

                <form @submit.prevent="submitForm">
                    <div class="form-group">
                        <label class="floating-label">
                            <span>Sujet</span>
                            <input v-model="form.subject" name="subject" type="text" required
                                placeholder="Sujet de votre demande" autocomplete="subject" />
                        </label>
                    </div>
                    <br>
                    <div class="form-group">
                        <label class="floating-label">
                            <span>Catégorie</span>

                            <div class="dropdown">

                                <button type="button" class="form-select dropdown__button" @click="open = !open">
                                    {{ form.category || "Sélectionnez une catégorie" }}
                                </button>


                                <div v-if="open" class="dropdown__list">

                                    <button v-for="item in categories" :key="item" type="button"
                                        class="dropdown__option" @click="selectCategory(item)">
                                        {{ item }}
                                    </button>

                                </div>

                            </div>

                        </label>
                    </div>
                    <br>
                    <div class="form-group">
                        <label class="floating-label">
                            <span>Message</span>
                            <textarea v-model="form.message" name="message" type="text" required
                                placeholder="Votre message..." autocomplete="message"></textarea>
                        </label>
                    </div>
                    <br>
                    <button type="submit" class="btn-primary">
                        Envoyer la demande
                    </button>
                </form>
            </div>

               <div class="info" style="margin-right:14px; margin-top:5px;">
                <div class="card-h">
                    <h3>Informations utiles</h3>
                </div>
                <div class="info-list">
                    <div class="info-item" style="margin-top:10%;margin-bottom:10%">
                        <MapPin class="info-icon" />
                        <div>
                            <span class="info-title">Adresse</span>
                            <div class="text-static">
                                <p>Siège de l'entreprise</p>
                            </div>
                        </div>
                    </div>
                    <div class="info-item" style="margin-bottom:10%">
                        <Phone class="info-icon" />
                        <div>
                            <span class="info-title">Téléphone</span>
                            <div class="text-static">
                                <p>+212 5 XX XX XX XX</p>
                            </div>
                        </div>
                    </div>
                    <div class="info-item" >
                        <Phone class="info-icon" />
                        <div>
                            <span class="info-title">Support</span>
                            <div class="text-static">
                                <p>+212 5 XX XX XX XX</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.sections {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-lg);
    padding: var(--space-xl);
}

.large-div {
    padding: 20px 22px;
    grid-column: span 2;
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    box-shadow: var(--shadow)
}

.info {
    padding: 20px 22px;
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    box-shadow: var(--shadow)
}

.info-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 25px;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 14px;
    border-radius: 12px;
    transition: .25s ease;
}

.info-icon {
    width: 24px;
    height: 24px;
    color: var(--brand-accent);
    flex-shrink: 0;
}

.info-title {
    display: block;
    margin-bottom: 6px;
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: 0.02em;

}

.info-item p {
    margin: 0;
    font-size: .9rem;
    font-weight: 500;
    color: var(--muted);
}
</style>