library(hash)

immune_cells = c("Bas", "Bmem", "Bnv", "CD4mem", "CD4nv", "CD8mem", "CD8nv", "Eos", "Mono", "Neu", "NK", "Treg")

broad_drug_groups = hash(
  'CVD medication'= c(
    "Antianginal drug", 
    "Antiarrhythmic drug", 
    "Cholesterol drug", 
    "Heart failure drug", 
    "Hypertension drug", 
    "Aspirin",
    "Pulmonary hypertension drug",
    "Hypotension drug", 
    "Phosphodiesterase inhibitors",
    "Antidiuretic drug"
    ),
  'Neurological medication' = c(
    "ADHD_narcolepsy drug", 
    "Anticholinergic drug", 
    "Antiemetic drug", 
    "Antiepileptic drug", 
    "Antipsychotic drug", 
    "Anxiety drug", 
    "Depression drug", 
    "Insomnia drug", 
    "Migraine drug", 
    "Alzheimer's drug", 
    "Vertigo",
    "Cholinergic agonist drug"
    ),
  'Pain & Rheuma medication' = c(
    "Antiinflammatory drug", 
    "Gout drug", 
    "Analgesic NSAID", 
    "Analgesic opiate", 
    "Analgesic other",
    "Nonsteroid cream",
    "Muscle relaxant drug",
    "Hydroxychloroquine"
    ),
  'Respiratory medication' = c(
    "COPD inhaler", 
    "Epinephrine", 
    "Antihistamine drug",
    "Steroid inhaler",
    "Nonsteroid inhaler"
    ),
  'Infection medication' = c(
    "Antiviral drug", 
    "Antiseptic drug", 
    "Cough drug", 
    "Decongestant drug", 
    "Antibiotic", 
    "Antifungal drug", 
    "Malaria drug", 
    "HIV ART drug",
    "Anesthetic drug"
    ),
  'Immunomodulatory medication' = c(
    "Bone marrow stimulant", 
    # "bone marrow suppressants (duplicated)",
    "Immunoglobulin drug",
    "Cancer drug",
    "Immunosuppressant drug"
  ),
  'Other antidegenerative medication' = c(
    "Bladder relaxant drug", 
    "Prostate hyperplasia drug", 
    "Glaucoma drug", 
    "Macular degeneration drug", 
    "Osteoporosis drug"
    ),
  'Metabolic disease medication' = c(
    "PAP sleep apnea",
    "Antidiabetic drug", 
    "Weight loss drug",
    "Gaucher's disease"
  ),
  'Supplement & vitamin' = c(
    "Supplement calcium & vitD",
    "Supplement cannabis",
    "Supplement probiotic",
    "Supplement iron",
    "Supplement mineral",
    "Supplement omega", 
    "Supplement or multivitamin"
    ),
  'Vaccine' = c(
    "Vaccine COVID",
    "Vaccine influenza",
    "Vaccine shingles",
    "Vaccine other"
  ),
  'Hormonal medication' = c(
    "Estrogen systemic",
    "Estrogen topical",
    "Steroid systemic",
    "Steroid topical",
    "Steroid ophthalmic",
    "Hyperthyroidism drug",
    "Hypothyroidism drug",
    "Testosterone topical",
    "Testosterone systemic"
  ),
  'GI tract medication' = c(
    "IBS_diarrhoea drug", 
    "Laxative", 
    "Acid reflux drug",
    "Antiflatulent drug"
  )
  # ,
  # 'Other' = c(
  #   "Other",
  #   "Eye drops")
)




