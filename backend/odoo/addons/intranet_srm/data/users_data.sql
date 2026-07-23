-- Script d'insertion des utilisateurs (managers des directions)
-- Ce script doit être exécuté après le chargement des directions via demo_data.xml

-- Direction Générale - DRISSI KAMILI Bouchra (DG)
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('DRISSI KAMILI Bouchra', 'drissi.kamili.bouchra@srm-tta.ma', 'drissi.kamili.bouchra', 'admin', 
        (SELECT id FROM intranet_direction WHERE code = 'DG' LIMIT 1), 
        'Directrice Générale', true, true, NOW())
ON CONFLICT DO NOTHING;

-- QSE - TAIMI Omar
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('TAIMI Omar', 'taimi.omar@srm-tta.ma', 'taimi.omar', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'QSE' LIMIT 1), 
        'Directeur Développement et Suivi des Performances, QSE', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Communication - ZEFZAF Hind
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('ZEFZAF Hind', 'zefzaf.hind@srm-tta.ma', 'zefzaf.hind', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'COMM' LIMIT 1), 
        'Directrice Communication Externe et Marketing', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Contrôle Permanent - BENNOUNA Maha
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('BENNOUNA Maha', 'bennouna.maha@srm-tta.ma', 'bennouna.maha', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'CTRL' LIMIT 1), 
        'Directrice Contrôle Permanent', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Audit Interne - EL KHAMICHI Mehdia
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('EL KHAMICHI Mehdia', 'el.khamlichi.mehdia@srm-tta.ma', 'el.khamlichi.mehdia', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'AUDIT' LIMIT 1), 
        'Directrice Audit Interne', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Gouvernance - EL ALAOUI EL ABIDI Khaoula
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('EL ALAOUI EL ABIDI Khaoula', 'el.alaoui.el.abidi.khaoula@srm-tta.ma', 'el.alaoui.el.abidi.khaoula', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'GOV' LIMIT 1), 
        'Directrice Gouvernance, Gestion des Contrats et Relations Institutionnelles', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Investissements - ERRAYSSOUNI Anouar
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('ERRAYSSOUNI Anouar', 'erraysouni.anouar@srm-tta.ma', 'erraysouni.anouar', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'INVEST' LIMIT 1), 
        'Directeur des Investissements', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Clientèle - OUJGHA Redouane
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('OUJGHA Redouane', 'oujgha.redouane@srm-tta.ma', 'oujgha.redouane', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'CLI' LIMIT 1), 
        'Directeur Clientèle', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Capital Humain - EL KHOMSI Jihad
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('EL KHOMSI Jihad', 'el.khomsi.jihad@srm-tta.ma', 'el.khomsi.jihad', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'RH' LIMIT 1), 
        'Directrice du Capital Humain', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Direction Province Al Hoceima - SOUJAA Souhail
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('SOUJAA Souhail', 'soujaa.souhail@srm-tta.ma', 'soujaa.souhail', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'PROV-HOU' LIMIT 1), 
        'Directeur Provincial Al Hoceima', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Direction Province Tétouan - ZITANE Mohamed Reda
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('ZITANE Mohamed Reda', 'zitane.mohamed.reda@srm-tta.ma', 'zitane.mohamed.reda', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'PROV-TET' LIMIT 1), 
        'Directeur Provincial Tétouan', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Direction Province Larache - ZAIM Mohamed
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('ZAIM Mohamed', 'zaim.mohamed@srm-tta.ma', 'zaim.mohamed', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'PROV-LAR' LIMIT 1), 
        'Directeur Provincial Larache', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Direction Province Chefchaouen - EL HASSANI Mohamed
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('EL HASSANI Mohamed', 'el.hassani.mohamed@srm-tta.ma', 'el.hassani.mohamed', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'PROV-CHE' LIMIT 1), 
        'Directeur Provincial Chefchaouen', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Direction Province Ouazzane - EL MOUSSAOUI Hicham
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('EL MOUSSAOUI Hicham', 'el.moussaoui.hicham@srm-tta.ma', 'el.moussaoui.hicham', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'PROV-OUA' LIMIT 1), 
        'Directeur Provincial Ouazzane', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Direction Province Fahs-Anjra - HRARTI Siham
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('HRARTI Siham', 'hrarti.siham@srm-tta.ma', 'hrarti.siham', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'PROV-FAH' LIMIT 1), 
        'Directrice Province Fahs-Anjra', true, true, NOW())
ON CONFLICT DO NOTHING;

-- Direction Province M'diq-Fnideq - ABDOUN Mohamed
INSERT INTO intranet_user (name, email, login, role, direction_id, job_title, is_manager, active, created_at)
VALUES ('ABDOUN Mohamed', 'abdoun.mohamed@srm-tta.ma', 'abdoun.mohamed', 'user', 
        (SELECT id FROM intranet_direction WHERE code = 'PROV-MDI' LIMIT 1), 
        'Directeur Provincial M''diq-Fnideq', true, true, NOW())
ON CONFLICT DO NOTHING;
