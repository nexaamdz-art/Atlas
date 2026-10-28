export type Lang = 'en' | 'fr' | 'ar';

export const TRANSLATIONS = {
  en: {
    appTitle: 'Atlas',
    modeledPieces: 'modeled pieces',
    sourceCredit: 'BodyParts3D',
    findStructure: 'Find a structure',
    aboutAtlas: 'About this atlas',
    systems: 'Systems',
    all: 'All',
    skeleton: 'Skeleton',
    organs: 'Organs',
    hideAll: 'Hide all',
    piecesVisible: 'pieces visible',
    searchPlaceholder: 'Heart, femur, cranial nerve…',
    searchNote: 'Start with a major organ, or search every named structure.',
    noResults: 'No structures match your search.',
    showingMatches: (count: number) => `Showing up to ${count} matches. Refine your search to find smaller structures.`,
    piece: 'piece',
    pieces: 'pieces',
    viewThreeQuarter: '¾ view',
    viewFront: 'Front view',
    viewSide: 'Side view',
    viewBack: 'Back view',
    rotateBody: 'Rotate body',
    pauseRotation: 'Pause rotation',
    reset: 'Reset',
    fullscreen: 'Fullscreen',
    exitFullscreen: 'Exit fullscreen',
    explodeAnatomy: 'Explode anatomy',
    assembled: 'Assembled',
    everyPiece: 'Every piece',
    controlsHint: 'Drag to orbit · Pinch to zoom · Tap to inspect',
    sourceCreditsBtn: 'Source & credits',
    preparingAnatomy: 'Preparing the anatomy',
    loadingPiece: (loaded: number, total: string) => `${loaded}% · Loading ${total} pieces`,
    reloadViewer: 'Reload viewer',
    atlasReference: 'Atlas reference',
    selectedPieces: 'Selected pieces',
    includedStructures: 'Included structures',
    morePieces: (n: number) => `And ${n} more modeled pieces.`,
    viewAnatomicalSource: 'View anatomical source',
    isolateStructure: 'Isolate structure',
    showSurrounding: 'Show surrounding anatomy',
    clearSelection: 'Clear selection',
    aboutEyebrow: 'SOURCE & SCOPE',
    aboutTitle: 'A body, revealed.',
    aboutDesc: 'Explore the adult male reference anatomy from BodyParts3D.',
    aboutCopyMale: 'Male · BodyParts3D',
    aboutCopyBody: '2,234 individual meshes and 3,432 named concepts from an adult male reference anatomy.',
    aboutCopyDisclaimer: 'This reference does not contain every human structure or variation. Named concepts can contain multiple pieces; each source mesh is rendered once.',
    aboutCopyColors: 'Colors and system groupings are designed for exploration. The geometry is simplified for the web, and short explanations provide general educational context. This is an anatomical reference, not a diagnostic or surgical tool.',
    sourceHeading: 'Source',
    licenseText: 'BodyParts3D, © The Database Center for Life Science licensed under CC Attribution 4.0 International.',
    datasetLicense: 'Dataset license',
    originalGeometry: 'Original geometry & metadata',
    sourcePublication: 'Read the source publication',
  },
  fr: {
    appTitle: 'Atlas',
    modeledPieces: 'pièces modélisées',
    sourceCredit: 'BodyParts3D',
    findStructure: 'Rechercher une structure',
    aboutAtlas: 'À propos de cet atlas',
    systems: 'Systèmes',
    all: 'Tous',
    skeleton: 'Squelette',
    organs: 'Organes',
    hideAll: 'Tout masquer',
    piecesVisible: 'pièces visibles',
    searchPlaceholder: 'Cœur, fémur, nerf crânien…',
    searchNote: 'Commencez par un organe majeur ou recherchez n’importe quelle structure.',
    noResults: 'Aucune structure ne correspond à votre recherche.',
    showingMatches: (count: number) => `Affichage jusqu\'à ${count} résultats. Affinez votre recherche pour les petites structures.`,
    piece: 'pièce',
    pieces: 'pièces',
    viewThreeQuarter: 'Vue ¾',
    viewFront: 'Vue de face',
    viewSide: 'Vue de profil',
    viewBack: 'Vue de dos',
    rotateBody: 'Rotation du corps',
    pauseRotation: 'Pause de la rotation',
    reset: 'Réinitialiser',
    fullscreen: 'Plein écran',
    exitFullscreen: 'Quitter le plein écran',
    explodeAnatomy: 'Éclater l’anatomie',
    assembled: 'Assemblé',
    everyPiece: 'Toutes les pièces',
    controlsHint: 'Glisser pour orbiter · Pincer pour zoomer · Toucher pour inspecter',
    sourceCreditsBtn: 'Source et crédits',
    preparingAnatomy: 'Préparation de l’anatomie',
    loadingPiece: (loaded: number, total: string) => `${loaded}% · Chargement de ${total} pièces`,
    reloadViewer: 'Recharger la visualisation',
    atlasReference: 'Référence de l’atlas',
    selectedPieces: 'Pièces sélectionnées',
    includedStructures: 'Structures incluses',
    morePieces: (n: number) => `Et ${n} autres pièces modélisées.`,
    viewAnatomicalSource: 'Voir la source anatomique',
    isolateStructure: 'Isoler la structure',
    showSurrounding: 'Afficher l’anatomie environnante',
    clearSelection: 'Effacer la sélection',
    aboutEyebrow: 'SOURCE ET PORTÉE',
    aboutTitle: 'Un corps, révélé.',
    aboutDesc: 'Explorez l’anatomie de référence masculine adulte de BodyParts3D.',
    aboutCopyMale: 'Homme · BodyParts3D',
    aboutCopyBody: '2 234 maillages individuels et 3 432 concepts nommés issus d’une anatomie de référence masculine adulte.',
    aboutCopyDisclaimer: 'Cette référence ne contient pas toutes les structures ou variations humaines. Les concepts nommés peuvent contenir plusieurs pièces.',
    aboutCopyColors: 'Les couleurs et regroupements sont conçus pour l’exploration. La géométrie est simplifiée pour le web.',
    sourceHeading: 'Source',
    licenseText: 'BodyParts3D, © The Database Center for Life Science sous licence CC Attribution 4.0 International.',
    datasetLicense: 'Licence du jeu de données',
    originalGeometry: 'Géométrie d’origine et métadonnées',
    sourcePublication: 'Lire la publication source',
  },
  ar: {
    appTitle: 'أطلس',
    modeledPieces: 'قطعة مصممة',
    sourceCredit: 'BodyParts3D',
    findStructure: 'البحث عن هيكل',
    aboutAtlas: 'حول الأطلس',
    systems: 'الأجهزة',
    all: 'الكل',
    skeleton: 'الهيكل العظمي',
    organs: 'الأعضاء',
    hideAll: 'إخفاء الكل',
    piecesVisible: 'قطع مرئية',
    searchPlaceholder: 'القلب، عظم الفخذ، العصب القحفي…',
    searchNote: 'ابدأ بعضو رئيسي، أو ابحث في كل هيكل مسمى.',
    noResults: 'لا توجد هياكل تطابق بحثك.',
    showingMatches: (count: number) => `عرض ما يصل إلى ${count} نتيجة. دقق بحثك للعثور على الهياكل الأصغر.`,
    piece: 'قطعة',
    pieces: 'قطع',
    viewThreeQuarter: 'عرض ¾',
    viewFront: 'عرض أمامي',
    viewSide: 'عرض جانبي',
    viewBack: 'عرض خلفي',
    rotateBody: 'دوران الجسم',
    pauseRotation: 'إيقاف الدوران',
    reset: 'إعادة تعيين',
    fullscreen: 'ملء الشاشة',
    exitFullscreen: 'الخروج من ملء الشاشة',
    explodeAnatomy: 'تفكيك التشريح',
    assembled: 'مجتمع',
    everyPiece: 'كل قطعة',
    controlsHint: 'اسحب للدوران · قرص للتكبير · انقر للفحص',
    sourceCreditsBtn: 'المصادر والاعتمادات',
    preparingAnatomy: 'جاري تحضير التشريح',
    loadingPiece: (loaded: number, total: string) => `${loaded}% · جاري تحميل ${total} قطعة`,
    reloadViewer: 'إعادة تحميل العارض',
    atlasReference: 'مرجع الأطلس',
    selectedPieces: 'القطع المحددة',
    includedStructures: 'الهياكل المضمنة',
    morePieces: (n: number) => `و ${n} قطعة أخرى مصممة.`,
    viewAnatomicalSource: 'عرض المصدر التشريحي',
    isolateStructure: 'عزل الهيكل',
    showSurrounding: 'إظهار التشريح المحيط',
    clearSelection: 'مسح التحديد',
    aboutEyebrow: 'المصدر والنطاق',
    aboutTitle: 'جسم، مكشوف.',
    aboutDesc: 'استكشف تشريح مرجع الذكور البالغين من BodyParts3D.',
    aboutCopyMale: 'ذكر · BodyParts3D',
    aboutCopyBody: '2,234 شبكة فردية و 3,432 مفهوماً مسماً من تشريح مرجعي لذكر بالغ.',
    aboutCopyDisclaimer: 'لا يحتوي هذا المرجع على كل هيكل أو تنوع بشري. قد تحتوي المفاهيم المسماة على عدة قطع.',
    aboutCopyColors: 'تم تصميم الألوان وتجمعات الأنظمة للاستكشاف. تم تبسيط الهندسة للويب.',
    sourceHeading: 'المصدر',
    licenseText: 'BodyParts3D، © مركز قاعدة بيانات علوم الحياة مرخص بموجب ترخيص CC Attribution 4.0 الدولي.',
    datasetLicense: 'ترخيص مجموعة البيانات',
    originalGeometry: 'الهندسة الأصلية والبيانات الوصفية',
    sourcePublication: 'قراءة المنشور المصدر',
  }
};

export const SYSTEM_TRANSLATIONS: Record<string, { en: { name: string; desc: string }; fr: { name: string; desc: string }; ar: { name: string; desc: string } }> = {
  skeletal: {
    en: { name: 'Skeleton', desc: 'Bones form the supporting framework of the body, protect organs, and provide attachment points for muscles.' },
    fr: { name: 'Squelette', desc: 'Les os forment la structure de support du corps, protègent les organes et fournissent des points d’attache aux muscles.' },
    ar: { name: 'الهيكل العظمي', desc: 'تشكل العظام الإطار الداعم للجسم، وتحمي الأعضاء، وتوفر نقاط اتصال للعضلات.' }
  },
  muscular: {
    en: { name: 'Muscles', desc: 'Skeletal muscles generate movement by pulling on their attachments. Together with tendons, they move joints, stabilize posture, and produce heat.' },
    fr: { name: 'Muscles', desc: 'Les muscles squelettiques génèrent le mouvement en tirant sur leurs attaches.' },
    ar: { name: 'العضلات', desc: 'تولد عضلات الهيكل العظمي الحركة عن طريق سحب مرفقاتها.' }
  },
  cardiac: {
    en: { name: 'Heart', desc: 'The heart is a muscular pump with four chambers. Its valves direct blood forward through the pulmonary and systemic circuits.' },
    fr: { name: 'Cœur', desc: 'Le cœur est une pompe musculaire à quatre chambres.' },
    ar: { name: 'القلب', desc: 'القلب هو مضخة عضلية ذات أربع حجرات.' }
  },
  sensory: {
    en: { name: 'Sensory organs', desc: 'These structures contribute to special senses, including sight, hearing, and balance.' },
    fr: { name: 'Organes sensoriels', desc: 'Ces structures contribuent aux sens spéciaux, notamment la vue, l’ouïe et l’équilibre.' },
    ar: { name: 'الأعضاء الحسية', desc: 'تساهم هذه الهياكل في الحواس الخاصة، بما في ذلك البصر والسمع والتوازن.' }
  },
  arterial: {
    en: { name: 'Arteries', desc: 'The heart drives blood through the circulation. Arteries carry blood away from the heart to supply tissues.' },
    fr: { name: 'Artères', desc: 'Le cœur propulse le sang dans la circulation. Les artériels transportent le sang loin du cœur.' },
    ar: { name: 'الشرايين', desc: 'يدفع القلب الدم عبر الدورة الدموية. تنقل الشرايين الدم بعيداً عن القلب.' }
  },
  venous: {
    en: { name: 'Veins', desc: 'Veins return blood toward the heart. Superficial and deep networks collect blood from the tissues.' },
    fr: { name: 'Veines', desc: 'Les veines ramènent le sang vers le cœur.' },
    ar: { name: 'الأوردة', desc: 'تعيد الأوردة الدم نحو القلب.' }
  },
  nervous: {
    en: { name: 'Nervous system', desc: 'The brain, spinal cord, and peripheral nerves carry and process signals.' },
    fr: { name: 'Système nerveux', desc: 'Le cerveau, la moelle épinière et les nerfs périphériques transportent et traitent les signaux.' },
    ar: { name: 'الجهاز العصبي', desc: 'يحمل الدماغ والحبل الشوكي والأعصاب الطرفية الإشارات ويعالجونها.' }
  },
  respiratory: {
    en: { name: 'Respiratory', desc: 'The airways conduct air to the lungs, where oxygen and carbon dioxide move between air and blood.' },
    fr: { name: 'Respiratoire', desc: 'Les voies aériennes conduisent l’air vers les poumons.' },
    ar: { name: 'الجهاز التنفسي', desc: 'تنقل الممرات الهوائية الهواء إلى الرئتين.' }
  },
  digestive: {
    en: { name: 'Digestive', desc: 'The digestive tract breaks down food, absorbs nutrients and water, and moves waste onward.' },
    fr: { name: 'Digestif', desc: 'Le tube digestif décompose les aliments, absorbe les nutriments et l’eau.' },
    ar: { name: 'الجهاز الهضمي', desc: 'يقوم الجهاز الهضمي بتكسير الطعام، وامتصاص العناصر الغذائية والماء.' }
  },
  urinary: {
    en: { name: 'Urinary', desc: 'The kidneys filter blood and regulate fluid, electrolyte, and acid–base balance.' },
    fr: { name: 'Urinaire', desc: 'Les reins filtrent le sang et régulent l’équilibre hydrique et électrolytique.' },
    ar: { name: 'الجهاز البولي', desc: 'تقوم الكلى بتصفية الدم وتنظيم توازن السوائل والإلكتروليتات.' }
  },
  lymphatic: {
    en: { name: 'Lymphatic', desc: 'Lymphatic vessels return excess tissue fluid to the circulation.' },
    fr: { name: 'Lymphatique', desc: 'Les vaisseaux lymphatiques renvoient l’excès de liquide tissulaire dans la circulation.' },
    ar: { name: 'الجهاز اللمفاوي', desc: 'تعيد الأوعية اللمفاوية السوائل النسيجية الزائدة إلى الدورة الدموية.' }
  },
  endocrine: {
    en: { name: 'Endocrine', desc: 'Endocrine organs release hormones into the blood to coordinate processes such as metabolism.' },
    fr: { name: 'Endocrinien', desc: 'Les organes endocriniens libèrent des hormones dans le sang.' },
    ar: { name: 'الغدد الصماء', desc: 'تفرز أعضاء الغدد الصماء الهرمونات في الدم لتنسيق العمليات.' }
  },
  reproductive: {
    en: { name: 'Reproductive', desc: 'The male reproductive structures represented here contribute to sperm production and transport.' },
    fr: { name: 'Reproducteur', desc: 'Les structures reproductrices représentées ici contribuent à la production de spermatozoïdes.' },
    ar: { name: 'الجهاز التناسلي', desc: 'تساهم الهياكل التناسلية الممثلة هنا في إنتاج الحيوانات المنوية ونقلها.' }
  },
  integumentary: {
    en: { name: 'Body surface', desc: 'The body surface provides an outer anatomical reference and protective barrier.' },
    fr: { name: 'Surface corporelle', desc: 'La surface corporelle fournit une référence anatomique externe et une barrière protectrice.' },
    ar: { name: 'سطح الجسم', desc: 'يوفر سطح الجسم مرجعاً تشريحياً خارجيام وحاجزاً وقائياً.' }
  },
  connective: {
    en: { name: 'Connective tissue', desc: 'Cartilage, ligaments, and other connective tissues support, connect, and separate structures.' },
    fr: { name: 'Tissu conjonctif', desc: 'Le cartilage, les ligaments et autres tissus conjonctifs soutiennent, connectent et séparent les structures.' },
    ar: { name: 'النسيج الضام', desc: 'يدعم الغضروف والأربطة والأنسجة الضامة الأخرى الهياكل ويفصل بينها.' }
  }
};

export const EXPLANATION_TRANSLATIONS: Record<string, { en: string; fr: string; ar: string }> = {
  'heart': {
    en: 'A muscular pump in the chest. Its right side sends blood to the lungs; its left side sends blood through the systemic circulation.',
    fr: 'Une pompe musculaire dans la poitrine. Son côté droit envoie le sang vers les poumons ; son côté gauche l’envoie dans la circulation systémique.',
    ar: 'مضخة عضلية في الصدر. يرسل جانبها الأيمن الدم إلى الرئتين، بينما يرسل جانبها الأيسر الدم عبر الدورة الدموية الجهازية.'
  },
  'liver': {
    en: 'A large organ beneath the right side of the diaphragm. It processes absorbed nutrients, produces bile, and synthesizes proteins.',
    fr: 'Un grand organe situé sous le côté droit du diaphragme. Il traite les nutriments absorbés, produit la bile et synthétise les protéines.',
    ar: 'عضو كبير يقع تحت الجانب الأيمن من الحجاب الحاجز. يعالج العناصر الغذائية الممتصة، وينتج الصفراء، ويصنع البروتينات.'
  },
  'brain': {
    en: 'The central organ of the nervous system. Its interconnected regions support perception, movement, memory, and language.',
    fr: 'L’organe central du système nerveux. Ses régions interconnectées soutiennent la perception, le mouvement, la mémoire et le langage.',
    ar: 'العضو المركزي في الجهاز العصبي. تدعم مناطقه المتصلة الإدراك والحركة والذاكرة واللغة.'
  },
  'stomach': {
    en: 'A muscular chamber between the esophagus and small intestine. It stores and mixes food with acid and enzymes.',
    fr: 'Une chambre musculaire entre l’œsophage et l’intestin grêle. Elle stocke et mélange les aliments avec l’acide et les enzymes.',
    ar: 'حجرة عضلية بين المريء والأمعاء الدقيقة. تخزن الطعام وتمزجه مع الحمض والإنزيمات.'
  },
  'spleen': {
    en: 'A lymphoid organ in the upper left abdomen. It filters blood, removes aging blood cells, and participates in immune responses.',
    fr: 'Un organe lymphoïde situé dans la partie supérieure gauche de l’abdomen. Il filtre le sang et participe aux réponses immunitaires.',
    ar: 'عضو لمفاوي في الجزء العلوي الأيسر من البطن. يصفّي الدم، ويزيل خلايا الدم الهرمة، ويشارك في الاستجابات المناعية.'
  },
  'pancreas': {
    en: 'An abdominal organ with digestive and endocrine roles. It supplies enzymes to the small intestine and releases hormones.',
    fr: 'Un organe abdominal ayant des rôles digestifs et endocriniens. Il fournit des enzymes à l’intestin grêle et libère des hormones.',
    ar: 'عضو بطني له أدوار هضمية وغدد صماء. يزود الأمعاء الدقيقة بالإنزيمات ويفرز الهرمونات.'
  },
  'urinary bladder': {
    en: 'A muscular reservoir in the pelvis that stores urine arriving from the kidneys through the ureters.',
    fr: 'Un réservoir musculaire dans le pelvis qui stocke l’urine provenant des reins par les uretères.',
    ar: 'خزان عضلي في الحوض يخزن البول القادم من الكلى عبر الحالبين.'
  },
  'trachea': {
    en: 'The main airway connecting the larynx to the bronchi. Its cartilage supports keep the airway open during breathing.',
    fr: 'La principale voie aérienne reliant le larynx aux bronches. Ses anneaux cartilagineux maintiennent la voie ouverte.',
    ar: 'المجرى الهوائي الرئيسي الذي يوصل الحنجرة بالقصبات الهوائية. تحافظ دعامات الغضروف على انفتاح المجرى.'
  },
  'diaphragm': {
    en: 'A broad muscle separating the chest and abdomen. When it contracts, it increases chest volume and helps draw air into the lungs.',
    fr: 'Un muscle large séparant la poitrine et l’abdomen. Lorsqu’il se contracte, il augmente le volume thoracique.',
    ar: 'عضو عضلي عريض يفصل بين الصدر والبطن. عندما ينقبض، يزيد حجم الصدر ويساعد في سحب الهواء إلى الرئتين.'
  }
};
