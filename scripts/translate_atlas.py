#!/usr/bin/env python3
"""
Medical terminology translator for Human Atlas (BodyParts3D FMA concepts and parts)
Translates all anatomical concepts and parts into French and Arabic using official Terminologia Anatomica (TA98 / UMD).
"""
import json, re

# Comprehensive dictionary for anatomical nouns, adjectives, and expressions
EXACT_MAP = {
    # Main Organs & Viscera
    "heart": ("Cœur", "القلب"),
    "brain": ("Cerveau", "الدماغ"),
    "liver": ("Foie", "الكبد"),
    "stomach": ("Estomac", "المعدة"),
    "spleen": ("Rate", "الطحال"),
    "pancreas": ("Pancréas", "البنكرياس"),
    "urinary bladder": ("Vessie", "المثانة البولية"),
    "bladder": ("Vessie", "المثانة"),
    "trachea": ("Trachée", "الرغامي"),
    "esophagus": ("Œsophage", "المريء"),
    "oesophagus": ("Œsophage", "المريء"),
    "gallbladder": ("Vésicule biliaire", "المرارة"),
    "gall bladder": ("Vésicule biliaire", "المرارة"),
    "kidney": ("Rein", "الكلية"),
    "right kidney": ("Rein droit", "الكلية اليمنى"),
    "left kidney": ("Rein gauche", "الكلية اليسرى"),
    "duodenum": ("Duodénum", "الاثني عشر"),
    "jejunum": ("Jéjunum", "الصائم"),
    "ileum": ("Iléon", "اللفائفي"),
    "cecum": ("Cæcum", "الأعور"),
    "appendix": ("Appendice", "الزائدة الدودية"),
    "vermiform appendix": ("Appendice vermiforme", "الزائدة الدودية"),
    "colon": ("Côlon", "القولون"),
    "ascending colon": ("Côlon ascendant", "القولون الصاعد"),
    "transverse colon": ("Côlon transverse", "القولون المستعرض"),
    "descending colon": ("Côlon descendant", "القولون النازل"),
    "sigmoid colon": ("Côlon sigmoïde", "القولون السيني"),
    "rectum": ("Rectum", "المستقيم"),
    "anus": ("Anus", "الشرج"),
    "anal canal": ("Canal anal", "القناة الشرجية"),
    "testis": ("Testicule", "الخصية"),
    "right testis": ("Testicule droit", "الخصية اليمنى"),
    "left testis": ("Testicule gauche", "الخصية اليسرى"),
    "epididymis": ("Épididyme", "البربخ"),
    "prostate": ("Prostate", "البروستاتا"),
    "penis": ("Pénis", "القضيب"),
    "scrotum": ("Scrotum", "كيس الصفن"),
    "skin": ("Peau", "الجلد"),
    "diaphragm": ("Diaphragme", "الحجاب الحاجز"),
    "thymus": ("Thymus", "الغدة الصعترية"),
    "thyroid gland": ("Glande thyroïde", "الغدة الدرقية"),
    "pituitary gland": ("Glande hypophyse", "الغدة النخامية"),
    "pineal gland": ("Glande pinéale", "الغدة الصنوبرية"),
    "pineal body": ("Corps pinéal", "الجسم الصنوبري"),
    "tongue": ("Langue", "اللسان"),
    "eye": ("Œil", "العين"),
    "eyeball": ("Globe oculaire", "مقلة العين"),
    "cornea": ("Cornée", "القرنية"),
    "iris": ("Iris", "القزحية"),
    "lens": ("Cristallin", "العدسة"),
    "retina": ("Rétine", "الشبكية"),
    "sclera": ("Sclère", "الصلبة"),
    "ear": ("Oreille", "الأذن"),
    "tympanic membrane": ("Membrane tympanique", "غشاء الطبل"),

    # Main Vessels
    "aorta": ("Aorte", "الأبهر"),
    "ascending aorta": ("Aorte ascendante", "الأبهر الصاعد"),
    "arch of aorta": ("Crosse de l'aorte", "قوس الأبهر"),
    "descending aorta": ("Aorte descendante", "الأبهر النازل"),
    "thoracic aorta": ("Aorte thoracique", "الأبهر الصدري"),
    "abdominal aorta": ("Aorte abdominale", "الأبهر البطني"),
    "superior vena cava": ("Veine cave supérieure", "الوريد الأجوف العلوي"),
    "inferior vena cava": ("Veine cave inférieure", "الوريد الأجوف السفلي"),
    "pulmonary trunk": ("Tronc pulmonaire", "الجذع الرئوي"),
    "celiac trunk": ("Tronc cœliaque", "الجذع البطني"),
    "coeliac trunk": ("Tronc cœliaque", "الجذع البطني"),
    "hepatic portal vein": ("Veine porte hépatique", "الوريد البابي الكبدي"),
    "portal vein": ("Veine porte", "الوريد البابي"),
    "azygos vein": ("Veine azygos", "الوريد الفرد"),
    "hemiazygos vein": ("Veine hémi-azygos", "الوريد نصف الفرد"),

    # Central Nervous System
    "spinal cord": ("Moelle épinière", "الحبل الشوكي"),
    "brainstem": ("Tronc cérébral", "جذع الدماغ"),
    "cerebellum": ("Cervelet", "المخيخ"),
    "cerebral hemisphere": ("Hémisphère cérébral", "نصف الكرة المخية"),
    "telencephalon": ("Télencéphale", "الدماغ الانتهائي"),
    "diencephalon": ("Diencéphale", "الدماغ البيني"),
    "mesencephalon": ("Mésencéphale", "الدماغ المتوسط"),
    "midbrain": ("Mésencéphale", "الدماغ المتوسط"),
    "pons": ("Pont", "الجسر"),
    "medulla oblongata": ("Moelle allongée", "النخاع المستطيل"),
    "thalamus": ("Thalamus", "المهاد"),
    "hypothalamus": ("Hypothalamus", "تحت المهاد"),
    "epithalamus": ("Épithalamus", "فوق المهاد"),
    "hippocampus": ("Hippocampe", "الحصين"),
    "amygdala": ("Amygdale", "اللوزة الدماغية"),
    "corpus callosum": ("Corps calleux", "الجسم الثفني"),
    "fornix": ("Fornix", "القبو"),
    "caudate nucleus": ("Noyau caudé", "النواة المذنبة"),
    "putamen": ("Putamen", "اللحاء"),
    "globus pallidus": ("Globus pallidus", "الكرة الشاحبة"),
    "cerebral cortex": ("Cortex cérébral", "القشرة المخية"),

    # Skeletal elements
    "skull": ("Crâne", "الجمجمة"),
    "mandible": ("Mandibule", "الفك السفلي"),
    "maxilla": ("Maxillaire", "الفك العلوي"),
    "sternum": ("Sternum", "القص"),
    "clavicle": ("Clavicule", "الترقوة"),
    "scapula": ("Scapula", "لوح الكتف"),
    "humerus": ("Humérus", "العضد"),
    "radius": ("Radius", "الكعبرة"),
    "ulna": ("Ulna", "الزند"),
    "femur": ("Fémur", "عظم الفخذ"),
    "patella": ("Patella", "الرضفة"),
    "tibia": ("Tibia", "الظنبوب"),
    "fibula": ("Fibula", "الشظية"),
    "pelvis": ("Bassin", "الحوض"),
    "sacrum": ("Sacrum", "العجز"),
    "coccyx": ("Coccyx", "العصعص"),
    "atlas": ("Atlas", "الفهقة"),
    "axis": ("Axis", "المحور"),
    "hyoid bone": ("Os hyoïde", "العظم اللامي"),
    "calcaneus": ("Calcanéus", "عظم العقب"),
    "talus": ("Talus", "عظم الكاحل"),
    "navicular": ("Naviculaire", "العظم الزورقي"),
    "cuboid": ("Cuboïde", "العظم النردي"),
    "cuneiform": ("Cunéiforme", "العظم الإسفيني"),
    "scaphoid": ("Scaphoïde", "العظم الزورقي لليد"),
    "lunate": ("Lunatum", "العظم الهلالي"),
    "triquetrum": ("Triquetrum", "العظم المثلثي"),
    "pisiform": ("Pisiforme", "العظم الحمصي"),
    "trapezium": ("Trapèze", "العظم المربعي"),
    "trapezoid": ("Trapézoïde", "العظم شبه المنحرف"),
    "capitate": ("Capitatum", "العظم الكبير"),
    "hamate": ("Hamatum", "العظم الكلابي"),
}

# Anatomical noun base mapping (with gender in French: 'm' or 'f', 'pl', and vowels)
NOUNS = {
    "artery": {"fr": "artère", "gen": "f", "ar": "شريان", "ar_f": False},
    "arteries": {"fr": "artères", "gen": "f", "ar": "شرايين", "ar_f": True},
    "vein": {"fr": "veine", "gen": "f", "ar": "وريد", "ar_f": False},
    "veins": {"fr": "veines", "gen": "f", "ar": "أوردة", "ar_f": True},
    "nerve": {"fr": "nerf", "gen": "m", "ar": "عصب", "ar_f": False},
    "nerves": {"fr": "nerfs", "gen": "m", "ar": "أعصاب", "ar_f": True},
    "muscle": {"fr": "muscle", "gen": "m", "ar": "عضلة", "ar_f": True},
    "muscles": {"fr": "muscles", "gen": "m", "ar": "عضلات", "ar_f": True},
    "bone": {"fr": "os", "gen": "m", "ar": "عظم", "ar_f": False},
    "bones": {"fr": "os", "gen": "m", "ar": "عظام", "ar_f": True},
    "cartilage": {"fr": "cartilage", "gen": "m", "ar": "غضروف", "ar_f": False},
    "ligament": {"fr": "ligament", "gen": "m", "ar": "رباط", "ar_f": False},
    "ligaments": {"fr": "ligaments", "gen": "m", "ar": "أربطة", "ar_f": True},
    "tendon": {"fr": "tendon", "gen": "m", "ar": "وتر", "ar_f": False},
    "tendons": {"fr": "tendons", "gen": "m", "ar": "أوتار", "ar_f": True},
    "branch": {"fr": "branche", "gen": "f", "ar": "فرع", "ar_f": False},
    "branches": {"fr": "branches", "gen": "f", "ar": "فروع", "ar_f": True},
    "trunk": {"fr": "tronc", "gen": "m", "ar": "جذع", "ar_f": False},
    "trunks": {"fr": "troncs", "gen": "m", "ar": "جذوع", "ar_f": True},
    "segment": {"fr": "segment", "gen": "m", "ar": "قطعة", "ar_f": True},
    "segments": {"fr": "segments", "gen": "m", "ar": "قطع", "ar_f": True},
    "tree": {"fr": "arbre", "gen": "m", "ar": "شجرة", "ar_f": True},
    "lobe": {"fr": "lobe", "gen": "m", "ar": "فص", "ar_f": False},
    "lobes": {"fr": "lobes", "gen": "m", "ar": "فصوص", "ar_f": True},
    "lobule": {"fr": "lobule", "gen": "m", "ar": "فصيص", "ar_f": False},
    "head": {"fr": "tête", "gen": "f", "ar": "رأس", "ar_f": False},
    "body": {"fr": "corps", "gen": "m", "ar": "جسم", "ar_f": False},
    "neck": {"fr": "col", "gen": "m", "ar": "عنق", "ar_f": False},
    "tail": {"fr": "queue", "gen": "f", "ar": "ذيل", "ar_f": False},
    "base": {"fr": "base", "gen": "f", "ar": "قاعدة", "ar_f": True},
    "apex": {"fr": "apex", "gen": "m", "ar": "قمة", "ar_f": True},
    "root": {"fr": "racine", "gen": "f", "ar": "جذر", "ar_f": False},
    "wall": {"fr": "paroi", "gen": "f", "ar": "جدار", "ar_f": False},
    "surface": {"fr": "face", "gen": "f", "ar": "سطح", "ar_f": False},
    "margin": {"fr": "bord", "gen": "m", "ar": "حافة", "ar_f": True},
    "border": {"fr": "bord", "gen": "m", "ar": "حافة", "ar_f": True},
    "sulcus": {"fr": "sillon", "gen": "m", "ar": "ثلم", "ar_f": False},
    "gyrus": {"fr": "gyrus", "gen": "m", "ar": "تلفيف", "ar_f": False},
    "fossa": {"fr": "fosse", "gen": "f", "ar": "حفرة", "ar_f": True},
    "canal": {"fr": "canal", "gen": "m", "ar": "قناة", "ar_f": True},
    "duct": {"fr": "conduit", "gen": "m", "ar": "قناة", "ar_f": True},
    "cavity": {"fr": "cavité", "gen": "f", "ar": "تجويف", "ar_f": False},
    "chamber": {"fr": "chambre", "gen": "f", "ar": "غرفة", "ar_f": True},
    "sinus": {"fr": "sinus", "gen": "m", "ar": "جيب", "ar_f": False},
    "atrium": {"fr": "atrium", "gen": "m", "ar": "أذين", "ar_f": False},
    "ventricle": {"fr": "ventricule", "gen": "m", "ar": "بطين", "ar_f": False},
    "valve": {"fr": "valve", "gen": "f", "ar": "صمام", "ar_f": False},
    "cusp": {"fr": "cuspide", "gen": "f", "ar": "شرفة", "ar_f": True},
    "septum": {"fr": "septum", "gen": "m", "ar": "حاجز", "ar_f": False},
    "plexus": {"fr": "plexus", "gen": "m", "ar": "ضفيرة", "ar_f": True},
    "ganglion": {"fr": "ganglion", "gen": "m", "ar": "عقدة", "ar_f": True},
    "gland": {"fr": "glande", "gen": "f", "ar": "غدة", "ar_f": True},
    "fascia": {"fr": "fascia", "gen": "m", "ar": "لفافة", "ar_f": True},
    "membrane": {"fr": "membrane", "gen": "f", "ar": "غشاء", "ar_f": False},
    "vertebra": {"fr": "vertèbre", "gen": "f", "ar": "فقرة", "ar_f": True},
    "vertebrae": {"fr": "vertèbres", "gen": "f", "ar": "فقرات", "ar_f": True},
    "rib": {"fr": "côte", "gen": "f", "ar": "ضلع", "ar_f": False},
    "ribs": {"fr": "côtes", "gen": "f", "ar": "أضلاع", "ar_f": True},
    "tooth": {"fr": "dent", "gen": "f", "ar": "سن", "ar_f": True},
    "teeth": {"fr": "dents", "gen": "f", "ar": "أسنان", "ar_f": True},
    "phalanx": {"fr": "phalange", "gen": "f", "ar": "سلامى", "ar_f": True},
    "phalanges": {"fr": "phalanges", "gen": "f", "ar": "سلاميات", "ar_f": True},
    "finger": {"fr": "doigt", "gen": "m", "ar": "إصبع اليد", "ar_f": False},
    "toe": {"fr": "orteil", "gen": "m", "ar": "إصبع القدم", "ar_f": False},
    "foot": {"fr": "pied", "gen": "m", "ar": "قدم", "ar_f": True},
    "hand": {"fr": "main", "gen": "f", "ar": "يد", "ar_f": True},
    "arm": {"fr": "bras", "gen": "m", "ar": "ذراع", "ar_f": True},
    "forearm": {"fr": "avant-bras", "gen": "m", "ar": "ساعد", "ar_f": False},
    "leg": {"fr": "jambe", "gen": "f", "ar": "ساق", "ar_f": True},
    "thigh": {"fr": "cuisse", "gen": "f", "ar": "فخذ", "ar_f": True},
    "knee": {"fr": "genou", "gen": "m", "ar": "ركبة", "ar_f": True},
    "ankle": {"fr": "cheville", "gen": "f", "ar": "كاحل", "ar_f": False},
    "hip": {"fr": "hanche", "gen": "f", "ar": "ورك", "ar_f": False},
    "shoulder": {"fr": "épaule", "gen": "f", "ar": "كتف", "ar_f": True},
    "chest": {"fr": "thorax", "gen": "m", "ar": "صدر", "ar_f": False},
    "thorax": {"fr": "thorax", "gen": "m", "ar": "صدر", "ar_f": False},
    "abdomen": {"fr": "abdomen", "gen": "m", "ar": "بطن", "ar_f": False},
    "pelvis": {"fr": "bassin", "gen": "m", "ar": "حوض", "ar_f": False},
    "jaw": {"fr": "mâchoire", "gen": "f", "ar": "فك", "ar_f": False},
    "upper jaw": {"fr": "mâchoire supérieure", "gen": "f", "ar": "الفك العلوي", "ar_f": False},
    "lower jaw": {"fr": "mâchoire inférieure", "gen": "f", "ar": "الفك السفلي", "ar_f": False},
    "gingiva": {"fr": "gencive", "gen": "f", "ar": "لثة", "ar_f": True},
    "lip": {"fr": "lèvre", "gen": "f", "ar": "شفة", "ar_f": True},
    "eyelid": {"fr": "paupière", "gen": "f", "ar": "جفن", "ar_f": False},
    "eyebrow": {"fr": "sourcil", "gen": "m", "ar": "حاجب", "ar_f": False},
    "palate": {"fr": "palais", "gen": "m", "ar": "حنك", "ar_f": False},
    "nose": {"fr": "nez", "gen": "m", "ar": "أنف", "ar_f": False},
    "mouth": {"fr": "bouche", "gen": "f", "ar": "فم", "ar_f": False},
    "throat": {"fr": "gorge", "gen": "f", "ar": "حلق", "ar_f": False},
    "tributary": {"fr": "affluent", "gen": "m", "ar": "رافد", "ar_f": False},
    "tributaries": {"fr": "affluents", "gen": "m", "ar": "روافد", "ar_f": True},
    "part": {"fr": "partie", "gen": "f", "ar": "جزء", "ar_f": False},
    "subdivision": {"fr": "subdivision", "gen": "f", "ar": "قسم فرعي", "ar_f": False},
    "organ": {"fr": "organe", "gen": "m", "ar": "عضو", "ar_f": False},
    "system": {"fr": "système", "gen": "m", "ar": "جهاز", "ar_f": False},
    "space": {"fr": "espace", "gen": "m", "ar": "حيز", "ar_f": False},
    "layer": {"fr": "couche", "gen": "f", "ar": "طبقة", "ar_f": True},
    "sheath": {"fr": "gaine", "gen": "f", "ar": "غمد", "ar_f": False},
    "capsule": {"fr": "capsule", "gen": "f", "ar": "محفظة", "ar_f": True},
    "arch": {"fr": "arcade", "gen": "f", "ar": "قوس", "ar_f": True},
    "process": {"fr": "processus", "gen": "m", "ar": "نتوء", "ar_f": False},
    "tubercle": {"fr": "tubercule", "gen": "m", "ar": "حديبة", "ar_f": True},
    "tuberosity": {"fr": "tubérosité", "gen": "f", "ar": "أحدوبة", "ar_f": True},
    "crest": {"fr": "crête", "gen": "f", "ar": "عرف", "ar_f": False},
    "spine": {"fr": "épine", "gen": "f", "ar": "شوكة", "ar_f": True},
    "line": {"fr": "ligne", "gen": "f", "ar": "خط", "ar_f": False},
    "anastomosis": {"fr": "anastomose", "gen": "f", "ar": "مفاغرة", "ar_f": True},
}

# Anatomical adjectives with gender concordance
ADJECTIVES = {
    "right": {"fr_m": "droit", "fr_f": "droite", "ar_m": "الأيمن", "ar_f": "اليمنى"},
    "left": {"fr_m": "gauche", "fr_f": "gauche", "ar_m": "الأيسر", "ar_f": "اليسرى"},
    "anterior": {"fr_m": "antérieur", "fr_f": "antérieure", "ar_m": "الأمامي", "ar_f": "الأمامية"},
    "posterior": {"fr_m": "postérieur", "fr_f": "postérieure", "ar_m": "الخلفي", "ar_f": "الخلفية"},
    "superior": {"fr_m": "supérieur", "fr_f": "supérieure", "ar_m": "العلوي", "ar_f": "العلوية"},
    "inferior": {"fr_m": "inférieur", "fr_f": "inférieure", "ar_m": "السفلي", "ar_f": "السفلية"},
    "medial": {"fr_m": "médial", "fr_f": "médiale", "ar_m": "الإنسي", "ar_f": "الإنسية"},
    "lateral": {"fr_m": "latéral", "fr_f": "latérale", "ar_m": "الوحشي", "ar_f": "الوحشية"},
    "intermediate": {"fr_m": "intermédiaire", "fr_f": "intermédiaire", "ar_m": "المتوسط", "ar_f": "المتوسطة"},
    "internal": {"fr_m": "interne", "fr_f": "interne", "ar_m": "الداخلي", "ar_f": "الداخلية"},
    "external": {"fr_m": "externe", "fr_f": "externe", "ar_m": "الخارجي", "ar_f": "الخارجية"},
    "superficial": {"fr_m": "superficiel", "fr_f": "superficielle", "ar_m": "السطحي", "ar_f": "السطحية"},
    "deep": {"fr_m": "profond", "fr_f": "profonde", "ar_m": "العميق", "ar_f": "العميقة"},
    "proximal": {"fr_m": "proximal", "fr_f": "proximale", "ar_m": "الداني", "ar_f": "الدانية"},
    "distal": {"fr_m": "distal", "fr_f": "distale", "ar_m": "القاصي", "ar_f": "القاصية"},
    "ascending": {"fr_m": "ascendant", "fr_f": "ascendante", "ar_m": "الصاعد", "ar_f": "الصاعدة"},
    "descending": {"fr_m": "descendant", "fr_f": "descendante", "ar_m": "النازل", "ar_f": "النازلة"},
    "transverse": {"fr_m": "transverse", "fr_f": "transverse", "ar_m": "المستعرض", "ar_f": "المستعرضة"},
    "oblique": {"fr_m": "oblique", "fr_f": "oblique", "ar_m": "المائل", "ar_f": "المائلة"},
    "longitudinal": {"fr_m": "longitudinal", "fr_f": "longitudinale", "ar_m": "الطولي", "ar_f": "الطولية"},
    "first": {"fr_m": "premier", "fr_f": "première", "ar_m": "الأول", "ar_f": "الأولى"},
    "second": {"fr_m": "deuxième", "fr_f": "deuxième", "ar_m": "الثاني", "ar_f": "الثانية"},
    "third": {"fr_m": "troisième", "fr_f": "troisième", "ar_m": "الثالث", "ar_f": "الثالثة"},
    "fourth": {"fr_m": "quatrième", "fr_f": "quatrième", "ar_m": "الرابع", "ar_f": "الرابعة"},
    "fifth": {"fr_m": "cinquième", "fr_f": "cinquième", "ar_m": "الخامس", "ar_f": "الخامسة"},
    "sixth": {"fr_m": "sixième", "fr_f": "sixième", "ar_m": "السادس", "ar_f": "السادسة"},
    "seventh": {"fr_m": "septième", "fr_f": "septième", "ar_m": "السابع", "ar_f": "السابعة"},
    "eighth": {"fr_m": "huitième", "fr_f": "huitième", "ar_m": "الثامن", "ar_f": "الثامنة"},
    "ninth": {"fr_m": "neuvième", "fr_f": "neuvième", "ar_m": "التاسع", "ar_f": "التاسعة"},
    "tenth": {"fr_m": "dixième", "fr_f": "dixième", "ar_m": "العاشر", "ar_f": "العاشرة"},
    "eleventh": {"fr_m": "onzième", "fr_f": "onzième", "ar_m": "الحادي عشر", "ar_f": "الحادية عشرة"},
    "twelfth": {"fr_m": "douzième", "fr_f": "douzième", "ar_m": "الثاني عشر", "ar_f": "الثانية عشرة"},
    "major": {"fr_m": "majeur", "fr_f": "majeure", "ar_m": "الكبير", "ar_f": "الكبيرة"},
    "minor": {"fr_m": "mineur", "fr_f": "mineure", "ar_m": "الصغير", "ar_f": "الصغيرة"},
    "great": {"fr_m": "grand", "fr_f": "grande", "ar_m": "الكبير", "ar_f": "الكبيرة"},
    "greater": {"fr_m": "grand", "fr_f": "grande", "ar_m": "الكبير", "ar_f": "الكبيرة"},
    "lesser": {"fr_m": "petit", "fr_f": "petite", "ar_m": "الصغير", "ar_f": "الصغيرة"},
    "small": {"fr_m": "petit", "fr_f": "petite", "ar_m": "الصغير", "ar_f": "الصغيرة"},
    "long": {"fr_m": "long", "fr_f": "longue", "ar_m": "الطويل", "ar_f": "الطويلة"},
    "short": {"fr_m": "court", "fr_f": "courte", "ar_m": "القصير", "ar_f": "القصيرة"},
    "common": {"fr_m": "commun", "fr_f": "commune", "ar_m": "المشترك", "ar_f": "المشتركة"},
    "proper": {"fr_m": "propre", "fr_f": "propre", "ar_m": "الخاص", "ar_f": "الخاصة"},
    "accessory": {"fr_m": "accessoire", "fr_f": "accessoire", "ar_m": "الإضافي", "ar_f": "الإضافية"},
    "middle": {"fr_m": "moyen", "fr_f": "moyenne", "ar_m": "الأوسط", "ar_f": "الوسطى"},
    "central": {"fr_m": "central", "fr_f": "centrale", "ar_m": "المركزي", "ar_f": "المركزية"},
    "segmental": {"fr_m": "segmentaire", "fr_f": "segmentaire", "ar_m": "القطعي", "ar_f": "القطعية"},
    "subsegmental": {"fr_m": "sous-segmentaire", "fr_f": "sous-segmentaire", "ar_m": "تحت القطعي", "ar_f": "تحت القطعية"},
    "coronary": {"fr_m": "coronaire", "fr_f": "coronaire", "ar_m": "التاجي", "ar_f": "التاجية"},
    "pulmonary": {"fr_m": "pulmonaire", "fr_f": "pulmonaire", "ar_m": "الرئوي", "ar_f": "الرئوية"},
    "cardiac": {"fr_m": "cardiaque", "fr_f": "cardiaque", "ar_m": "القلبي", "ar_f": "القلبية"},
    "hepatic": {"fr_m": "hépatique", "fr_f": "hépatique", "ar_m": "الكبدي", "ar_f": "الكبدية"},
    "renal": {"fr_m": "rénal", "fr_f": "rénale", "ar_m": "الكلوي", "ar_f": "الكلوية"},
    "splenic": {"fr_m": "splénique", "fr_f": "splénique", "ar_m": "الطحالي", "ar_f": "الطحالية"},
    "gastric": {"fr_m": "gastrique", "fr_f": "gastrique", "ar_m": "المعدي", "ar_f": "المعدية"},
    "pancreatic": {"fr_m": "pancréatique", "fr_f": "pancréatique", "ar_m": "البنكرياسي", "ar_f": "البنكرياسية"},
    "mesenteric": {"fr_m": "mésentérique", "fr_f": "mésentérique", "ar_m": "المساريقي", "ar_f": "المساريقية"},
    "celiac": {"fr_m": "cœliaque", "fr_f": "cœliaque", "ar_m": "البطني", "ar_f": "البطنية"},
    "coeliac": {"fr_m": "cœliaque", "fr_f": "cœliaque", "ar_m": "البطني", "ar_f": "البطنية"},
    "intercostal": {"fr_m": "intercostal", "fr_f": "intercostale", "ar_m": "الوربي", "ar_f": "الوربية"},
    "cervical": {"fr_m": "cervical", "fr_f": "cervicale", "ar_m": "العنقي", "ar_f": "العنقية"},
    "thoracic": {"fr_m": "thoracique", "fr_f": "thoracique", "ar_m": "الصدري", "ar_f": "الصدرية"},
    "lumbar": {"fr_m": "lombaire", "fr_f": "lombaire", "ar_m": "القطني", "ar_f": "القطنية"},
    "sacral": {"fr_m": "sacré", "fr_f": "sacrée", "ar_m": "العجزي", "ar_f": "العجزية"},
    "coccygeal": {"fr_m": "coccygien", "fr_f": "coccygienne", "ar_m": "العصعصي", "ar_f": "العصعصية"},
    "cerebral": {"fr_m": "cérébral", "fr_f": "cérébrale", "ar_m": "المخي", "ar_f": "المخية"},
    "cerebellar": {"fr_m": "cérébelleux", "fr_f": "cérébelleuse", "ar_m": "المخيخي", "ar_f": "المخيخية"},
    "temporal": {"fr_m": "temporal", "fr_f": "temporale", "ar_m": "الصدغي", "ar_f": "الصدغية"},
    "frontal": {"fr_m": "frontal", "fr_f": "frontale", "ar_m": "الجبهي", "ar_f": "الجبهية"},
    "parietal": {"fr_m": "pariétal", "fr_f": "pariétale", "ar_m": "الجداري", "ar_f": "الجدارية"},
    "occipital": {"fr_m": "occipital", "fr_f": "occipitale", "ar_m": "القذالي", "ar_f": "القذالية"},
    "cranial": {"fr_m": "crânien", "fr_f": "crânienne", "ar_m": "القحفي", "ar_f": "القحفية"},
    "facial": {"fr_m": "facial", "fr_f": "faciale", "ar_m": "الوجهي", "ar_f": "الوجهية"},
    "brachial": {"fr_m": "brachial", "fr_f": "brachiale", "ar_m": "العضدي", "ar_f": "العضدية"},
    "radial": {"fr_m": "radial", "fr_f": "radiale", "ar_m": "الكعبري", "ar_f": "الكعبرية"},
    "ulnar": {"fr_m": "ulnaire", "fr_f": "ulnaire", "ar_m": "الزندي", "ar_f": "الزندية"},
    "axillary": {"fr_m": "axillaire", "fr_f": "axillaire", "ar_m": "الإبطي", "ar_f": "الإبطية"},
    "subclavian": {"fr_m": "subclavier", "fr_f": "subclavière", "ar_m": "تحت الترقوي", "ar_f": "تحت الترقوية"},
    "femoral": {"fr_m": "fémoral", "fr_f": "fémorale", "ar_m": "الفخزي", "ar_f": "الفخذية"},
    "tibial": {"fr_m": "tibial", "fr_f": "tibiale", "ar_m": "الظنبوبي", "ar_f": "الظنبوبية"},
    "fibular": {"fr_m": "fibulaire", "fr_f": "fibulaire", "ar_m": "الشظوي", "ar_f": "الشظوية"},
    "peroneal": {"fr_m": "péronier", "fr_f": "péronière", "ar_m": "الشظوي", "ar_f": "الشظوية"},
    "popliteal": {"fr_m": "poplité", "fr_f": "poplitée", "ar_m": "المأبضي", "ar_f": "المأبضية"},
    "iliac": {"fr_m": "iliaque", "fr_f": "iliaque", "ar_m": "الحرقفي", "ar_f": "الحرقفية"},
    "carotid": {"fr_m": "carotide", "fr_f": "carotide", "ar_m": "السباتي", "ar_f": "السباتية"},
    "jugular": {"fr_m": "jugulaire", "fr_f": "jugulaire", "ar_m": "الوداجي", "ar_f": "الوداجية"},
    "palmar": {"fr_m": "palmaire", "fr_f": "palmaire", "ar_m": "الراحي", "ar_f": "الراحية"},
    "plantar": {"fr_m": "plantaire", "fr_f": "plantaire", "ar_m": "الأخمصي", "ar_f": "الأخمصية"},
    "digital": {"fr_m": "digital", "fr_f": "digitale", "ar_m": "الإصبعي", "ar_f": "الإصبعية"},
    "metacarpal": {"fr_m": "métacarpien", "fr_f": "métacarpienne", "ar_m": "السنعي", "ar_f": "السنعية"},
    "metatarsal": {"fr_m": "métatarsien", "fr_f": "métatarsienne", "ar_m": "المشطي", "ar_f": "المشطية"},
    "carpal": {"fr_m": "carpien", "fr_f": "carpienne", "ar_m": "الرسغي", "ar_f": "الرسغية"},
    "tarsal": {"fr_m": "tarsien", "fr_f": "tarsienne", "ar_m": "الرصغي", "ar_f": "الرصغية"},
    "intervertebral": {"fr_m": "intervertébral", "fr_f": "intervertébrale", "ar_m": "بين الفقرات", "ar_f": "بين الفقرات"},
    "costal": {"fr_m": "costal", "fr_f": "costale", "ar_m": "الضلعي", "ar_f": "الضلعية"},
    "bronchial": {"fr_m": "bronchique", "fr_f": "bronchique", "ar_m": "القصببي", "ar_f": "القصبية"},
    "bronchopulmonary": {"fr_m": "broncho-pulmonaire", "fr_f": "broncho-pulmonaire", "ar_m": "القصببي الرئوي", "ar_f": "القصبية الرئوية"},
    "biliary": {"fr_m": "biliaire", "fr_f": "biliaire", "ar_m": "الصفراوي", "ar_f": "الصفراوية"},
    "urinary": {"fr_m": "urinaire", "fr_f": "urinaire", "ar_m": "البولي", "ar_f": "البولية"},
    "vascular": {"fr_m": "vasculaire", "fr_f": "vasculaire", "ar_m": "الوعائي", "ar_f": "الوعائية"},
    "arterial": {"fr_m": "artériel", "fr_f": "artérielle", "ar_m": "الشرياني", "ar_f": "الشريانية"},
    "venous": {"fr_m": "veineux", "fr_f": "veineuse", "ar_m": "الوريدي", "ar_f": "الوريدية"},
    "lymphatic": {"fr_m": "lymphatique", "fr_f": "lymphatique", "ar_m": "اللمفاوي", "ar_f": "اللمفاوية"},
    "muscular": {"fr_m": "musculaire", "fr_f": "musculaire", "ar_m": "العضلي", "ar_f": "العضلية"},
    "skeletal": {"fr_m": "squelettique", "fr_f": "squelettique", "ar_m": "الهيكلي", "ar_f": "الهيكلية"},
    "connective": {"fr_m": "conjonctif", "fr_f": "conjonctive", "ar_m": "الضام", "ar_f": "الضامة"},
    "autonomic": {"fr_m": "autonome", "fr_f": "autonome", "ar_m": "الذاتي", "ar_f": "الذاتية"},
    "sympathetic": {"fr_m": "sympathique", "fr_f": "sympathique", "ar_m": "الودي", "ar_f": "الودية"},
    "parasympathetic": {"fr_m": "parasympathique", "fr_f": "parasympathique", "ar_m": "نظير الودي", "ar_f": "نظير الودية"},
    "sensory": {"fr_m": "sensoriel", "fr_f": "sensorielle", "ar_m": "الحسي", "ar_f": "الحسية"},
    "optic": {"fr_m": "optique", "fr_f": "optique", "ar_m": "البصري", "ar_f": "البصرية"},
    "auditory": {"fr_m": "auditif", "fr_f": "auditive", "ar_m": "السمعي", "ar_f": "السمعية"},
    "ciliary": {"fr_m": "ciliaire", "fr_f": "ciliaire", "ar_m": "الهدبي", "ar_f": "الهدبية"},
    "ethmoidal": {"fr_m": "ethmoïdal", "fr_f": "ethmoïdale", "ar_m": "الغربالي", "ar_f": "الغربالية"},
    "sphenoidal": {"fr_m": "sphénoïdal", "fr_f": "sphénoïdale", "ar_m": "الوتدي", "ar_f": "الوتدية"},
    "maxillary": {"fr_m": "maxillaire", "fr_f": "maxillaire", "ar_m": "الفكي العلوي", "ar_f": "الفكية العلوية"},
    "mandibular": {"fr_m": "mandibulaire", "fr_f": "mandibulaire", "ar_m": "الفكي السفلي", "ar_f": "الفكية السفلية"},
    "lingual": {"fr_m": "lingual", "fr_f": "linguale", "ar_m": "اللساني", "ar_f": "اللسانية"},
    "palatine": {"fr_m": "palatin", "fr_f": "palatine", "ar_m": "الحنكي", "ar_f": "الحنكية"},
    "pharyngeal": {"fr_m": "pharyngé", "fr_f": "pharyngée", "ar_m": "البلعومي", "ar_f": "البلعومية"},
    "laryngeal": {"fr_m": "laryngé", "fr_f": "laryngée", "ar_m": "الحنجري", "ar_f": "الحنجرية"},
    "tracheal": {"fr_m": "trachéal", "fr_f": "trachéale", "ar_m": "الرغامي", "ar_f": "الرغامية"},
    "esophageal": {"fr_m": "œsophagien", "fr_f": "œsophagienne", "ar_m": "المريئي", "ar_f": "المريئية"},
    "duodenal": {"fr_m": "duodénal", "fr_f": "duodénale", "ar_m": "العفجي", "ar_f": "العفجية"},
    "colic": {"fr_m": "colique", "fr_f": "colique", "ar_m": "القولوني", "ar_f": "القولونية"},
    "rectal": {"fr_m": "rectal", "fr_f": "rectale", "ar_m": "المستقيمي", "ar_f": "المستقيمية"},
    "interventricular": {"fr_m": "interventriculaire", "fr_f": "interventriculaire", "ar_m": "بين البطينين", "ar_f": "بين البطينين"},
    "ventricular": {"fr_m": "ventriculaire", "fr_f": "ventriculaire", "ar_m": "البطيني", "ar_f": "البطينية"},
    "atrial": {"fr_m": "atrial", "fr_f": "atriale", "ar_m": "الأذيني", "ar_f": "الأذينية"},
    "septal": {"fr_m": "septal", "fr_f": "septale", "ar_m": "الحاجزي", "ar_f": "الحاجزية"},
    "perforating": {"fr_m": "perforant", "fr_f": "perforante", "ar_m": "الثاقب", "ar_f": "الثاقبة"},
    "communicating": {"fr_m": "communicant", "fr_f": "communicante", "ar_m": "الموصل", "ar_f": "الموصلة"},
    "circumflex": {"fr_m": "circonflexe", "fr_f": "circonflexe", "ar_m": "المنعطف", "ar_f": "المنعطفة"},
    "marginal": {"fr_m": "marginal", "fr_f": "marginale", "ar_m": "الحافي", "ar_f": "الحافية"},
    "apical": {"fr_m": "apical", "fr_f": "apicale", "ar_m": "القمي", "ar_f": "القمية"},
    "basal": {"fr_m": "basal", "fr_f": "basale", "ar_m": "القاعدي", "ar_f": "القاعدية"},
    "lateralis": {"fr_m": "latéral", "fr_f": "latérale", "ar_m": "الوحشي", "ar_f": "الوحشية"},
    "medialis": {"fr_m": "médial", "fr_f": "médiale", "ar_m": "الإنسي", "ar_f": "الإنسية"},
    "superioris": {"fr_m": "supérieur", "fr_f": "supérieure", "ar_m": "العلوي", "ar_f": "العلوية"},
    "inferioris": {"fr_m": "inférieur", "fr_f": "inférieure", "ar_m": "السفلي", "ar_f": "السفلية"},
    "anterioris": {"fr_m": "antérieur", "fr_f": "antérieure", "ar_m": "الأمامي", "ar_f": "الأمامية"},
    "posterioris": {"fr_m": "postérieur", "fr_f": "postérieure", "ar_m": "الخلفي", "ar_f": "الخلفية"},
    "longus": {"fr_m": "long", "fr_f": "longue", "ar_m": "الطويل", "ar_f": "الطويلة"},
    "brevis": {"fr_m": "court", "fr_f": "courte", "ar_m": "القصير", "ar_f": "القصيرة"},
    "magnus": {"fr_m": "grand", "fr_f": "grande", "ar_m": "الكبير", "ar_f": "الكبيرة"},
    "major": {"fr_m": "majeur", "fr_f": "majeure", "ar_m": "الكبير", "ar_f": "الكبيرة"},
    "maximus": {"fr_m": "grand", "fr_f": "grande", "ar_m": "الأكبر", "ar_f": "الكبرى"},
    "minimus": {"fr_m": "petit", "fr_f": "petite", "ar_m": "الأصغر", "ar_f": "الصغرى"},
    "medius": {"fr_m": "moyen", "fr_f": "moyenne", "ar_m": "الأوسط", "ar_f": "الوسطى"},
    "profundus": {"fr_m": "profond", "fr_f": "profonde", "ar_m": "العميق", "ar_f": "العميقة"},
    "superficialis": {"fr_m": "superficiel", "fr_f": "superficielle", "ar_m": "السطحي", "ar_f": "السطحية"},
    "rectus": {"fr_m": "droit", "fr_f": "droite", "ar_m": "المستقيم", "ar_f": "المستقيمة"},
    "obliquus": {"fr_m": "oblique", "fr_f": "oblique", "ar_m": "المائل", "ar_f": "المائلة"},
    "transversus": {"fr_m": "transverse", "fr_f": "transverse", "ar_m": "المستعرض", "ar_f": "المستعرضة"},
    "extensor": {"fr_m": "extenseur", "fr_f": "extenseur", "ar_m": "الباسطة", "ar_f": "الباسطة"},
    "flexor": {"fr_m": "fléchisseur", "fr_f": "fléchisseur", "ar_m": "القابضة", "ar_f": "القابضة"},
    "abductor": {"fr_m": "abducteur", "fr_f": "abducteur", "ar_m": "المبعدة", "ar_f": "المبعدة"},
    "adductor": {"fr_m": "adducteur", "fr_f": "adducteur", "ar_m": "المقربة", "ar_f": "المقربة"},
    "pronator": {"fr_m": "pronateur", "fr_f": "pronateur", "ar_m": "الكابة", "ar_f": "الكابة"},
    "supinator": {"fr_m": "supinateur", "fr_f": "supinateur", "ar_m": "الاستلقائية", "ar_f": "الاستلقائية"},
    "levator": {"fr_m": "élévateur", "fr_f": "élévateur", "ar_m": "الرافعة", "ar_f": "الرافعة"},
    "depressor": {"fr_m": "abaisseur", "fr_f": "abaisseur", "ar_m": "الخافضة", "ar_f": "الخافضة"},
    "sphincter": {"fr_m": "sphincter", "fr_f": "sphincter", "ar_m": "المصرة", "ar_f": "المصرة"},
    "dilator": {"fr_m": "dilatateur", "fr_f": "dilatateur", "ar_m": "الموسعة", "ar_f": "الموسعة"},
    "constrictor": {"fr_m": "constricteur", "fr_f": "constricteur", "ar_m": "المضيقة", "ar_f": "المضيقة"},
    "secondary": {"fr_m": "définitif", "fr_f": "définitive", "ar_m": "الدائم", "ar_f": "الدائمة"},
    "primary": {"fr_m": "primaire", "fr_f": "primaire", "ar_m": "الأولي", "ar_f": "الأولية"},
    "molar": {"fr_m": "molaire", "fr_f": "molaire", "ar_m": "الضرس", "ar_f": "الضرس"},
    "premolar": {"fr_m": "prémolaire", "fr_f": "prémolaire", "ar_m": "الضاحك", "ar_f": "الضاحك"},
    "canine": {"fr_m": "canine", "fr_f": "canine", "ar_m": "الناب", "ar_f": "الناب"},
    "incisor": {"fr_m": "incisive", "fr_f": "incisive", "ar_m": "القاطع", "ar_f": "القاطع"},
}

def french_article(noun_text, gen, is_plural=False):
    """Returns 'le', 'la', 'l'', 'les' or appropriate preposition 'de la', 'du', 'de l'', 'des'"""
    first_char = noun_text.lower()[0] if noun_text else ''
    is_vowel = first_char in 'aeiouyhéèêàâîïôûù'
    if is_plural:
        return ("les " + noun_text, "des " + noun_text)
    if is_vowel:
        return ("l'" + noun_text, "de l'" + noun_text)
    if gen == 'f':
        return ("la " + noun_text, "de la " + noun_text)
    return ("le " + noun_text, "du " + noun_text)

def translate_atom(phrase):
    """Translate a simple phrase without 'of'"""
    phrase = phrase.strip()
    p_lower = phrase.lower()

    if p_lower in EXACT_MAP:
        return EXACT_MAP[p_lower]

    words = phrase.split()
    if not words:
        return (phrase, phrase)

    # Check if ends with a known noun
    noun_match = None
    matched_noun_key = None
    for noun_len in range(3, 0, -1):
        if len(words) >= noun_len:
            sub = " ".join(words[-noun_len:]).lower()
            if sub in NOUNS:
                noun_match = NOUNS[sub]
                matched_noun_key = sub
                words_before = words[:-noun_len]
                break

    if not noun_match:
        # Check if first word is a noun
        first = words[0].lower()
        if first in NOUNS:
            noun_match = NOUNS[first]
            matched_noun_key = first
            words_before = words[1:]
        else:
            # Fallback direct word translation
            fr_parts = []
            ar_parts = []
            for w in words:
                wl = w.lower()
                if wl in ADJECTIVES:
                    fr_parts.append(ADJECTIVES[wl]['fr_m'])
                    ar_parts.append(ADJECTIVES[wl]['ar_m'])
                elif wl in NOUNS:
                    fr_parts.append(NOUNS[wl]['fr'])
                    ar_parts.append(NOUNS[wl]['ar'])
                elif wl in EXACT_MAP:
                    fr_parts.append(EXACT_MAP[wl][0])
                    ar_parts.append(EXACT_MAP[wl][1])
                else:
                    fr_parts.append(w)
                    ar_parts.append(w)
            return (" ".join(fr_parts).capitalize(), " ".join(ar_parts))

    # We have a noun! Build adjectives in appropriate order and gender
    gen = noun_match['gen']
    is_f = (gen == 'f')
    ar_is_f = noun_match.get('ar_f', is_f)

    fr_adjs = []
    ar_adjs = []

    for w in words_before:
        wl = w.lower()
        if wl in ADJECTIVES:
            adj = ADJECTIVES[wl]
            fr_adjs.append(adj['fr_f'] if is_f else adj['fr_m'])
            ar_adjs.append(adj['ar_f'] if ar_is_f else adj['ar_m'])
        elif wl in NOUNS:
            fr_adjs.append(NOUNS[wl]['fr'])
            ar_adjs.append(NOUNS[wl]['ar'])
        elif wl in EXACT_MAP:
            fr_adjs.append(EXACT_MAP[wl][0])
            ar_adjs.append(EXACT_MAP[wl][1])
        else:
            fr_adjs.append(w)
            ar_adjs.append(w)

    fr_noun = noun_match['fr']
    ar_noun = noun_match['ar']

    # French: Noun + Adjectives
    if fr_adjs:
        fr_result = f"{fr_noun} {' '.join(fr_adjs)}"
    else:
        fr_result = fr_noun
    fr_result = fr_result[0].upper() + fr_result[1:]

    # Arabic: Noun (definite) + Adjectives
    # If ar_noun doesn't start with ال, add it unless it's an idafa or already has it
    ar_noun_def = ar_noun if ar_noun.startswith("ال") or " " in ar_noun else f"ال{ar_noun}"
    if ar_adjs:
        ar_result = f"{ar_noun_def} {' '.join(ar_adjs)}"
    else:
        ar_result = ar_noun_def

    return (fr_result, ar_result)

def translate_concept(name):
    """Translate full concept name handling 'of' prepositions"""
    name_clean = name.strip()
    name_lower = name_clean.lower()

    if name_lower in EXACT_MAP:
        return EXACT_MAP[name_lower]

    # Split by ' of '
    parts = name_clean.split(' of ')
    if len(parts) == 1:
        return translate_atom(parts[0])

    # Multiple parts: A of B (of C...)
    # In French: A de B (de C)
    # In Arabic: A B (إضافة: الأول نكرة والثاني معرفة)
    fr_chunks = []
    ar_chunks = []

    for idx, p in enumerate(parts):
        fr_p, ar_p = translate_atom(p)
        if idx == 0:
            fr_chunks.append(fr_p)
            # In Arabic, the first part of Idafa is indefinite (remove initial 'ال')
            if ar_p.startswith("ال") and not ar_p.startswith("التي") and not ar_p.startswith("الذي"):
                ar_p_indef = ar_p[2:]
            else:
                ar_p_indef = ar_p
            ar_chunks.append(ar_p_indef)
        else:
            # French preposition: de l', du, de la, de
            first_c = fr_p.lower()[0] if fr_p else ''
            # Determine article
            # Check gender if we know it
            p_noun = p.split()[-1].lower()
            gen = NOUNS.get(p_noun, {}).get('gen', 'm')
            is_plural = p_noun.endswith('s')
            nom, prep = french_article(fr_p, gen, is_plural)
            fr_chunks.append(prep)

            # Arabic genitive: prepend 'لـ' if second level of of, or direct genitive
            if idx > 1:
                ar_chunks.append("لـ" + ar_p)
            else:
                ar_chunks.append(ar_p)

    fr_final = " ".join(fr_chunks)
    ar_final = " ".join(ar_chunks)
    return (fr_final, ar_final)

def main():
    atlas_path = 'public/models/atlas.json'
    with open(atlas_path) as f:
        atlas = json.load(f)

    concepts = atlas['concepts']
    parts = atlas['parts']

    print(f"Translating {len(concepts)} concepts and {len(parts)} parts...")
    
    concept_map = {}
    for c in concepts:
        fr, ar = translate_concept(c['name'])
        c['name_fr'] = fr
        c['name_ar'] = ar
        concept_map[c['id']] = (fr, ar)
        concept_map[c['name'].lower()] = (fr, ar)

    for p in parts:
        if p.get('conceptId') in concept_map:
            fr, ar = concept_map[p['conceptId']]
            p['name_fr'] = fr
            p['name_ar'] = ar
        elif p['name'].lower() in concept_map:
            fr, ar = concept_map[p['name'].lower()]
            p['name_fr'] = fr
            p['name_ar'] = ar
        else:
            fr, ar = translate_concept(p['name'])
            p['name_fr'] = fr
            p['name_ar'] = ar

    # Write back to atlas.json
    with open(atlas_path, 'w', encoding='utf-8') as f:
        json.dump(atlas, f, ensure_ascii=False, separators=(',', ':'))

    print("Successfully updated atlas.json with name_fr and name_ar!")

    # Also save translations dictionary for reference/testing
    sample_out = []
    for c in concepts[:30]:
        sample_out.append({
            "en": c['name'],
            "fr": c['name_fr'],
            "ar": c['name_ar']
        })
    print("\nFirst 30 translations sample:")
    print(json.dumps(sample_out, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
