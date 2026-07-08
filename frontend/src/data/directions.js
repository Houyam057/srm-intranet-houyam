// Données extraites de l'objet DIRS du mockup original.
// Dans une vraie appli, ceci viendrait d'un appel API (GET /api/directions).

export const DIRS = {
  dg:          { name: "Direction Générale", mgr: "DRISSI KAMILI Bouchra", pole: "—", eff: 2 },
  exploit:     { name: "Direction en charge des Exploitations", mgr: "HAJJAJ Younes", pole: "Direction Générale", eff: 1 },
  eau:         { name: "Direction Exploitation Eau Potable", mgr: "KANICE Mohammed", pole: "Pôle Exploitations", eff: 1 },
  assain:      { name: "Direction Exploitation Assainissement Liquide", mgr: "KANICE Mohammed", pole: "Pôle Exploitations", eff: 1 },
  elec:        { name: "Direction Exploitation Électricité", mgr: "ESSAIDI Othmane", pole: "Pôle Exploitations", eff: 1 },
  normal:      { name: "Direction Normalisation, Qualité et Performances Techniques", mgr: "BAISSA Salma", pole: "Pôle Exploitations", eff: 1 },
  support:     { name: "Direction en charge des Fonctions Support", mgr: "BEN ABDESSADAK Nisrine", pole: "Direction Générale", eff: 1 },
  achats:      { name: "Direction Achats, Moyens Généraux et Logistique", mgr: "OUALI Zouhair", pole: "Pôle Fonctions Support", eff: 2 },
  daf:         { name: "Direction Administrative et Financière", mgr: "BEN ABDESSADAK Nisrine", pole: "Pôle Fonctions Support", eff: 1 },
  juridique:   { name: "Direction Juridique et Assurances", mgr: "AMRANI Mohamed", pole: "Pôle Fonctions Support", eff: 1 },
  dsi:         { name: "Direction Systèmes d'Information et Transformation Digitale", mgr: "BAKALI TAHIRI Mohamed", pole: "Pôle Fonctions Support", eff: 1 },
  audit:       { name: "Direction Audit Interne", mgr: "ELKHAMLICHI Mehdia", pole: "Direction Générale", eff: 1 },
  clientele:   { name: "Direction Clientèle", mgr: "OUJGHA Radouane", pole: "Direction Générale", eff: 3 },
  controle:    { name: "Direction Contrôle Permanent", mgr: "BENNOUNA Maha", pole: "Direction Générale", eff: 5 },
  qse:         { name: "Direction Développement et Suivi des Performances, QSE", mgr: "TAIMI Omar", pole: "Direction Générale", eff: 2 },
  gouvernance: { name: "Direction Gouvernance, Gestion des Contrats et Relations Institutionnelles", mgr: "EL ALAOUI EL ABIDI Kawla", pole: "Direction Générale", eff: 1 },
  invest:      { name: "Direction des Investissements", mgr: "ERRAYSSOUNY Anouar", pole: "Direction Générale", eff: 4 },
  rh:          { name: "Direction du Capital Humain", mgr: "GHAMMAD Souhail", pole: "Direction Générale", eff: 1 }
}

// Structure du sous-menu "Nos Directions" (groupe > items) — reprend le HTML statique du mockup
export const NAV_DIRECTIONS = [
  { group: "DIRECTION GÉNÉRALE", items: [{ key: "dg", label: "Direction Générale" }] },
  {
    group: "PÔLE EXPLOITATIONS",
    items: [
      { key: "exploit", label: "Dir. en charge des Exploitations" },
      { key: "eau", label: "Exploitation Eau Potable" },
      { key: "assain", label: "Exploitation Assainissement Liquide" },
      { key: "elec", label: "Exploitation Électricité" },
      { key: "normal", label: "Normalisation, Qualité & Perf. Techniques" }
    ]
  },
  {
    group: "PÔLE FONCTIONS SUPPORT",
    items: [
      { key: "support", label: "Dir. en charge des Fonctions Support" },
      { key: "achats", label: "Achats, Moyens Généraux & Logistique" },
      { key: "daf", label: "Administrative et Financière" },
      { key: "juridique", label: "Juridique et Assurances" },
      { key: "dsi", label: "Systèmes d'Information & Transf. Digitale", me: true }
    ]
  },
  {
    group: "RATTACHÉES À LA DG",
    items: [
      { key: "comm", label: "Communication Externe & Marketing" },
      { key: "audit", label: "Audit Interne" },
      { key: "clientele", label: "Clientèle" },
      { key: "controle", label: "Contrôle Permanent" },
      { key: "qse", label: "Développement & Suivi des Performances, QSE" },
      { key: "gouvernance", label: "Gouvernance, Contrats & Rel. Institutionnelles" },
      { key: "invest", label: "Investissements" },
      { key: "rh", label: "Capital Humain" }
    ]
  }
]

// Pôles + directions affichés sur le hub "Mes Directions" (avec verrouillage selon profil)
export const DIRECTION_GROUPS = [
  {
    chip: "PÔLE EXPLOITATIONS",
    title: "Direction en charge des Exploitations",
    mgr: "HAJJAJ Younes",
    cards: [
      { key: "eau", eff: 1, locked: true },
      { key: "assain", eff: 1, locked: true },
      { key: "elec", eff: 1, locked: true },
      { key: "normal", eff: 1, locked: true }
    ]
  },
  {
    chip: "PÔLE FONCTIONS SUPPORT",
    title: "Direction en charge des Fonctions Support",
    mgr: "BEN ABDESSADAK Nisrine",
    cards: [
      { key: "achats", eff: 2, locked: true },
      { key: "daf", eff: 1, locked: true },
      { key: "juridique", eff: 1, locked: true },
      { key: "dsi", eff: 1, locked: false, mine: true }
    ]
  }
]
