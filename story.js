// ============================================================
//  HISTORIEN
//  Hvert afsnit har et nummer, en tekst og en liste af valg.
//  Afsnit adskilles med en tom linje i teksten (\n\n).
//
//  Felter:
//    tekst      – historien (afsnit adskilt af tom linje)
//    effekter   – { evne, udholdenhed, held, guld: tal (+/-),
//                   giv: "ting" eller ["ting", ...], tag: ... }
//    valg       – [{ tekst, til, kraever?: "ting", mangler?: "ting", kraeverGuld?: tal }]
//                 Valg med "kraever" er skjulte, hvis man ikke har tingen.
//                 Valg med "mangler" er skjulte, hvis man HAR tingen.
//                 Lykke-valg: { tekst, test: "held", til: <heldig>, ellers: <uheldig> }
//                 Karisma-valg: { tekst, test: "karisma", til, ellers } (bruger ikke Karisma op)
//                 kraeverKarisma: N (kun med høj Karisma), hoejstKarisma: N (kun for de grove)
//    effekter.loeft – { evne: 2 } hæver både startværdi og nuværende værdi
//    slut       – "sejr" eller "død" (så vises ingen valg)
//    billede    – sti til et billede, fx "assets/art/scenes/graaskoven.jpg" (valgfrit)
//    billedtekst – kort tekst under billedet (bruges også som alt-tekst)
//    stemning   – baggrundens farve: landsby, skov, flod, taarn, kammer,
//                 fare, sejr eller død. Uden stemning beholdes den forrige.
//    kamp       – { navn, evne, udholdenhed } eller en liste af fjender,
//                 som bekæmpes én ad gangen. Valgene vises først, når
//                 alle fjender er besejret.
//    flygt      – { tekst?, til } gør det muligt at flygte fra kampen
//                 (koster 2 Udholdenhed)
//    fortsaet   – { til, tekst } på en sejr: fortsæt til næste kapitel med samme helt
//    kapitel    – overskrift, der vises over afsnitsnummeret (fx ved et nyt kapitel)
// ============================================================

window.STORY = {
  titel: "Ravnetårnets Hemmelighed",
  undertitel: "Et eventyr hvor DU bestemmer",
  start: 1,
  startGuld: 5,
  startInventar: ["Sværd", "Lædervest", "Fakkel"],
  forsidebillede: "assets/art/egne/ravnetaarnet.jpg",
  forsidestemning: "taarn",

  // Kapitler, man kan starte direkte i fra forsiden. Starter man i et senere
  // kapitel, får man et standard-udstyr i stedet for det, man ville have
  // samlet i de tidligere kapitler (loeft hæver evnerne permanent).
  kapitler: [
    { titel: "Kapitel 1 · Ravnetårnets Hemmelighed", start: 1 },
    {
      titel: "Kapitel 2 · Skyggekongen", start: 101,
      udstyr: { inventar: ["Sværd", "Lædervest", "Fakkel", "Månestenen"], guld: 8, loeft: { evne: 1, udholdenhed: 2 } },
    },
    {
      titel: "Kapitel 3 · Havets Sang", start: 151,
      udstyr: { inventar: ["Sværd", "Lædervest", "Fakkel", "Månestenen"], guld: 10, loeft: { evne: 2, udholdenhed: 4, held: 1 } },
    },
    {
      titel: "Kapitel 4 · Dragens Vinter", start: 201,
      udstyr: { inventar: ["Sværd", "Lædervest", "Fakkel", "Månestenen"], guld: 12, loeft: { evne: 3, udholdenhed: 6, held: 1 } },
    },
  ],

  // Genstande: beskrivelse (vises, når man klikker på tingen i oppakningen)
  // og evt. "brug": effekter, når man bruger den. Brugbare ting forsvinder
  // efter brug og kan bruges når som helst – også midt i en kamp.
  genstande: {
    "Sværd": { ikon: "🗡️", tekst: "Et godt, gammelt sværd fra landsbysmeden." },
    "Lædervest": { ikon: "🦺", tekst: "Tykt læder, der har reddet dig fra mangen en skramme." },
    "Fakkel": { ikon: "🔥", tekst: "Giver lys i mørke steder – og skræmmer det, der lever der." },
    "Månestenen": { ikon: "🌙", tekst: "Den gamle amulet, der holder ulvene væk fra Vildmose. Den lyser svagt blåt." },
    "Runesværd": { ikon: "⚔️", tekst: "Et sværd fra stencirklen. Runerne langs klingen gløder, når der er fare." },
    "Elverbue": { ikon: "🏹", tekst: "Liriels bue. Den rammer altid det, den sigtes efter." },
    "Sølvnøgle": { ikon: "🗝️", tekst: "Åbner alle låse, Morvak har lavet." },
    "Sølvspejl": { ikon: "🪞", tekst: "Morvaks gamle spejl. Den, der ser sig selv i det, mens hun kaster en forbandelse, rammer sig selv." },
    "Ringbrynje": { ikon: "⛓️", tekst: "En tung brynje fra ulvehulen." },
    "Dragehudsskjold": { ikon: "🛡️", tekst: "Let som et blad, men intet sværd skærer igennem det." },
    "Dværgestålsværd": { ikon: "⚔️", tekst: "Smedet om af Thrain i Jernbjerget. Klingen er blå som is." },
    "Havfolkets trefork": { ikon: "🔱", tekst: "Smedet af havfolket til at bekæmpe Havheksen." },
    "Frostskjold": { ikon: "🛡️", tekst: "Et skjold af hvidt metal fra en frossen kriger i gletsjeren." },
    "Frostkrone": { ikon: "👑", tekst: "En krone af blåt is, der aldrig smelter. Den gør tankerne klare." },
    "Isbrodder": { ikon: "🥾", tekst: "Dværgestål under støvlerne. Nu er blankis som et stuegulv." },
    "Kort over tårnet": { ikon: "🗺️", tekst: "Grimbolds tegning af Ravnetårnet med et kryds ved skattekammeret." },
    "Grimbolds kort": { ikon: "🗺️", tekst: "Tegninger af Frostjarlens isslot med en skjult dør på østsiden." },
    "Ordet »Korvus«": { ikon: "💬", tekst: "Ravnens rette navn. Den adlyder, når man kalder den ved det." },
    "Ordet »Sten, sov«": { ikon: "💬", tekst: "Ordene, der får Morvaks stengolem til at falde i søvn." },
    "Rygte om sumpstien": { ikon: "💬", tekst: "Følg de døde birketræer – aldrig de blå lys." },
    "Syn af tronen": { ikon: "👁️", tekst: "Du ved, at Vardraks krystal sidder bag hans trone." },
    "Sporet efter ægget": { ikon: "👣", tekst: "Grimbold stjal dragens æg og solgte det til Frostjarlen." },
    "Koboldens løfte": { ikon: "👺", tekst: "Kald på kobolden Pip, når du har brug for ham. Én gang." },
    "Nereas skæl": { ikon: "🐚", tekst: "Med det på tungen kan du ånde under vand. Én gang." },
    "Hvalbensfløjte": { ikon: "🎶", tekst: "Heddas fløjte. Blæs i den over revet, så kommer hvalerne." },
    "Bivoks": { ikon: "🕯️", tekst: "To små kugler voks til ørerne – mod sirenernes sang." },
    "Dragens æg": { ikon: "🥚", tekst: "Stort som en kiste og koldt som is. Noget bevæger sig derinde." },
    "Uglefjer": { ikon: "🪶", tekst: "Vis den til Isvinge, så ved hun, at du kommer som ven." },
    "Tom eliksirflaske": { ikon: "🧪", tekst: "Her var engang en eliksir med kæmpestyrke." },

    // Brugbare ting
    "Helbredende urter": { ikon: "🌿", tekst: "Gnid dem i et sår, så lukker det sig som ved trylleri.", brug: { udholdenhed: 8 } },
    "Tørret fisk": { ikon: "🐟", tekst: "Marnas røgede fisk. Salt og mættende.", brug: { udholdenhed: 4 } },
    "Heksesalve": { ikon: "🫙", tekst: "Grimhilds grønne salve. Den lugter af mose, men den virker.", brug: { udholdenhed: 6, held: 1 } },
    "Livseliksir": { ikon: "🧪", tekst: "En glødende rød eliksir fra Morvaks kiste.", brug: { udholdenhed: 12 } },
    "Dværgemjød": { ikon: "🍺", tekst: "Brokks bedste mjød. Den varmer helt ned i tæerne.", brug: { udholdenhed: 5, held: 1 } },
    "Havets perle": { ikon: "🫧", tekst: "En lille perle fra havfolket. Knus den, og havet giver dig kræfter.", brug: { udholdenhed: 8, held: 2 } },
  },

  // Følgesvende hjælper dig i kampe: hver runde er der en chance for, at de
  // gør skade på fjenden eller heler dig. De skilles fra dig, når et nyt
  // kapitel begynder (effekter: { forladAlle: true }).
  foelgesvende: {
    "Ilsa": { ikon: "⛓️", tekst: "Smedens datter fra Vildmose. Hun slår med sin gamle kæde.", chance: 0.35, skade: 1, handling: "Ilsa slår med kæden" },
    "Liriel": { ikon: "🗡️", tekst: "Elveren fra kløften. Hun gav dig sin bue, men hendes elverdolke er lige så hurtige.", chance: 0.5, skade: 1, handling: "Liriel kaster en elverdolk" },
    "Nerea": { ikon: "🧜", tekst: "Havfruen, der reddede dig. Hendes sang heler sår.", chance: 0.4, heling: 2, handling: "Nerea synger, og dine sår lukker sig" },
    "Brokk": { ikon: "🪓", tekst: "Dværgen fra Jernbjerget. Bred som en dør og stærk som en okse.", chance: 0.4, skade: 2, handling: "Brokk hugger med sin økse" },
  },

  // Præstationer, som huskes på tværs af gennemspilninger (se Opdagelser).
  // Betingelser: afsnit (besøgt), ting (fået), procent (af alle afsnit),
  // slutninger (antal fundet), doede (antal gange død).
  praestationer: [
    { id: "runesvaerd", titel: "Sværdet i stenen", tekst: "Trak Runesværdet ud af alteret i stencirklen.", ting: "Runesværd" },
    { id: "pip", titel: "En kobold i gæld", tekst: "Lukkede kobolden Pip ud af buret.", ting: "Koboldens løfte" },
    { id: "ilsa", titel: "Befrieren", tekst: "Satte Ilsa fri i tårnets kælder.", afsnit: 70 },
    { id: "spejl", titel: "Spejl, spejl", tekst: "Lod Morvaks egen forbandelse ramme ham selv.", afsnit: 80 },
    { id: "korvus", titel: "Ravnens navn", tekst: "Kaldte ravnen Korvus ved navn og fik den til at vende om.", afsnit: 94 },
    { id: "tudse", titel: "Kvæk!", tekst: "Svarede forkert på heksens gåde.", afsnit: 109 },
    { id: "dvaerg", titel: "Dværgeven", tekst: "Fik smedet dit sværd om i Jernbjerget.", ting: "Dværgestålsværd" },
    { id: "ylva", titel: "Lysbringeren", tekst: "Satte prinsesse Ylva fri og så hende blive kronet.", afsnit: 149 },
    { id: "havfrue", titel: "Reddet af havet", tekst: "Faldt over bord og blev reddet af havfruen Nerea.", afsnit: 163 },
    { id: "havfolk", titel: "Havfolkets ven", tekst: "Befriede havfolket i den sunkne by.", afsnit: 189 },
    { id: "skarre", titel: "Et ord er et ord", tekst: "Holdt din aftale med smugleren Skarre.", afsnit: 198 },
    { id: "morga", titel: "Havets Hjerte", tekst: "Bragte Havets Hjerte tilbage fra Ulmar.", afsnit: 195 },
    { id: "isvinge", titel: "Dragens ven", tekst: "Gav Isvinge sit æg tilbage.", afsnit: 238 },
    { id: "dragedraeber", titel: "Den bitre sejr", tekst: "Dræbte den sidste drage.", afsnit: 240 },
    { id: "saga", titel: "Hele sagaen", tekst: "Gennemførte alle fire kapitler.", nogenAfsnit: [249, 250] },
    { id: "opdager", titel: "Opdagelsesrejsende", tekst: "Har set halvdelen af alle afsnit.", procent: 50 },
    { id: "kortlaegger", titel: "Kortlægger", tekst: "Har set alle afsnit i eventyret.", procent: 100 },
    { id: "slutninger5", titel: "Mange veje", tekst: "Har fundet 5 forskellige slutninger.", slutninger: 5 },
    { id: "soelvtunge", titel: "Sølvtunge", tekst: "Talte dig til noget, andre må betale eller kæmpe for.", nogenAfsnit: [2, 5, 6, 8, 10, 12, 14] },
    { id: "grov", titel: "Grov, men ærlig", tekst: "Fik en trold eller en kæmpe til at grine med dine fornærmelser.", nogenAfsnit: [4, 15] },
    { id: "doed5", titel: "Ni liv? Ikke helt", tekst: "Er død 5 gange.", doede: 5 },
  ],

  intro:
    "I landsbyen Vildmose er Månestenen, den gamle amulet som holder ulvene borte fra markerne, blevet stjålet. Sporene fører mod Ravnetårnet, hvor troldmanden Morvak bor.\n\n" +
    "Du er landsbyens sidste håb. Slå dine evner med terningerne, og begynd så din rejse.",

  afsnit: {
    1: {
      stemning: "landsby",
      billede: "assets/art/egne/vildmose-landsby.jpg",
      billedtekst: "Landsbyen Vildmose i måneskin",
      tekst:
        "Landsbyens ældste trykker din hånd ved den sidste hytte og ser op på den fulde måne. \"Kom tilbage med Månestenen, før månen er fuld igen,\" hvisker hun. \"Ellers kommer ulvene.\"\n\n" +
        "Foran dig deler vejen sig. Til venstre fører en mudret vej ned mod floden Sølvå. Til højre forsvinder en sti ind i den mørke Gråskov.",
      valg: [
        { tekst: "Følg vejen ned til floden", til: 9 },
        { tekst: "Tag stien gennem Gråskoven", til: 24 },
        { tekst: "Kig ind på kroen »Den Sorte Gryde« først", til: 41 },
      ],
    },

    41: {
      stemning: "landsby",
      billede: "assets/art/egne/den-sorte-gryde.jpg",
      billedtekst: "Kroen »Den Sorte Gryde«",
      tekst:
        "Kroen er varm og lugter af røg og gryderet. Kroværten tørrer krus af og nikker mod en hylde med tørrede urter. \"Helbredende urter, to guldstykker bundtet. Dem får du brug for, hvor du skal hen.\"\n\n" +
        "I et hjørne sidder en mørk fremmed og ryster et terningebæger. Ved ilden sidder en gammel kone med et sjal over hovedet og ser på dig, som om hun har ventet på dig.",
      valg: [
        { tekst: "Køb helbredende urter", til: 58, kraeverGuld: 2, mangler: "Helbredende urter" },
        { tekst: "Spil terninger med den fremmede om 2 guld", test: "held", til: 16, ellers: 17, kraeverGuld: 2 },
        { tekst: "Sæt dig hos den gamle kone", til: 26, mangler: "Rygte om sumpstien" },
        { tekst: "Gå hen til den mørke fremmede i hjørnet", til: 42 },
        { tekst: "Forlad kroen og tag stien gennem Gråskoven", til: 24 },
        { tekst: "Forlad kroen og gå ned til floden", til: 9 },
      ],
    },

    42: {
      stemning: "landsby",
      billede: "assets/art/egne/den-moerke-fremmede.jpg",
      billedtekst: "Den mørke fremmede",
      tekst:
        "Den fremmede ser op, da du sætter dig. Under hætten skinner to gule øjne, og han smiler skævt. \"Jeg hedder Grimbold,\" siger han. \"Jeg tjente Morvak i tyve år, indtil han smed mig ud for at tabe en af hans kolber.\"\n\n" +
        "Han lægger en hånd på et sammenrullet stykke pergament. \"Jeg tegnede et kort over tårnet, før jeg gik. Der er et skattekammer bag en løs sten i vindeltrappen. Tre guld, så er det dit.\"",
      valg: [
        { tekst: "Køb kortet", til: 45, kraeverGuld: 3, mangler: "Kort over tårnet" },
        { tekst: "Prut om prisen", test: "karisma", til: 6, ellers: 7, mangler: "Kort over tårnet" },
        { tekst: "Gå tilbage til kroens stue", til: 41 },
      ],
    },

    45: {
      stemning: "landsby",
      tekst:
        "Grimbold ruller kortet ud. Med sirlige streger viser det tårnets trapper og et lille kryds ved den syvende trappeafsats. \"Tryk på stenen med ravnetegnet,\" hvisker han. \"Og rør ikke ved kisten, medmindre lykken er med dig.\"",
      effekter: { guld: -3, giv: "Kort over tårnet" },
      valg: [{ tekst: "Gå tilbage til kroens stue", til: 41 }],
    },

    58: {
      tekst: "Kroværten pakker urterne ind i et stykke lærred. \"Gnid dem i et sår, og det lukker sig som ved trylleri,\" siger han.",
      effekter: { guld: -2, giv: "Helbredende urter" },
      valg: [{ tekst: "Se dig om i kroen igen", til: 41 }],
    },

    16: {
      tekst: "Terningerne ruller hen over bordet, og du vinder. Den fremmede bander lavt og skubber mønterne over til dig.",
      effekter: { guld: 2 },
      valg: [{ tekst: "Se dig om i kroen igen", til: 41 }],
    },

    17: {
      tekst: "Den fremmede smiler skævt, da terningerne lander. Du har tabt, og han stryger dine mønter ned i sin pung.",
      effekter: { guld: -2 },
      valg: [{ tekst: "Se dig om i kroen igen", til: 41 }],
    },

    26: {
      tekst:
        "Den gamle kone griber din hånd med en tør, kold hånd. \"Du skal til Ravnetårnet,\" siger hun. Det er ikke et spørgsmål.\n\n" +
        "\"Bag tårnet ligger Ravnesumpen. Følg aldrig de blå lys, for de fører kun ned i dybet. Hold dig til de døde birketræer, så finder du en glemt kælderdør.\"\n\n" +
        "Hun slipper din hånd og stirrer ind i ilden igen.",
      effekter: { giv: "Rygte om sumpstien" },
      valg: [{ tekst: "Se dig om i kroen igen", til: 41 }],
    },

    24: {
      stemning: "skov",
      billede: "assets/art/egne/graaskoven.jpg",
      billedtekst: "Gråskoven",
      tekst:
        "Træerne står så tæt, at dagslyset bliver gråt. Efter en times gang hører du et svagt host. En gammel mand sidder lænet op ad en egestamme. Han er tynd som en pind, og hans læber er sprukne.\n\n" +
        "\"Vand…\" hvisker han. \"Bare en mundfuld vand, fremmede.\"",
      valg: [
        { tekst: "Giv ham vand fra din flaske", til: 37 },
        { tekst: "Gå videre. Det kan være en fælde", til: 52 },
        { tekst: "Følg en gammel, tilgroet sti dybere ind i skoven", til: 30 },
      ],
    },

    30: {
      stemning: "skov",
      billede: "assets/art/egne/stencirklen.jpg",
      billedtekst: "Sværdet i stencirklen",
      tekst:
        "Stien ender i en lysning, hvor syv mosgroede sten står i en cirkel. I midten står et alter, og i alteret sidder et sværd begravet til halvt op ad klingen. Runer løber ned ad bladet.\n\n" +
        "Det hvisker i trætoppene, selvom der ingen vind er.",
      valg: [
        { tekst: "Grib sværdet og træk", test: "held", til: 35, ellers: 39 },
        { tekst: "Knæl og bed ved alteret", til: 43 },
        { tekst: "Lad stedet være og gå videre", til: 47 },
      ],
    },

    35: {
      stemning: "skov",
      tekst:
        "Sværdet glider ud af stenen, som var det smurt med olie. Runerne gløder hvidt et øjeblik, og en kraft strømmer op gennem din arm.\n\n" +
        "Hviskenen i træerne bliver til en sagte sang og forsvinder så.",
      effekter: { loeft: { evne: 2 }, giv: "Runesværd" },
      valg: [{ tekst: "Gå videre gennem skoven", til: 47 }],
    },

    39: {
      stemning: "fare",
      tekst:
        "Sværdet sidder fast som var det vokset ind i stenen. En iskold stemme runger i dit hoved: \"UVÆRDIG!\"\n\n" +
        "Et stød kaster dig baglæns ud over græsset.",
      effekter: { udholdenhed: -3 },
      valg: [
        { tekst: "Knæl og bed om tilgivelse", til: 43 },
        { tekst: "Skynd dig væk fra stedet", til: 47 },
      ],
    },

    43: {
      stemning: "skov",
      tekst:
        "Du knæler ved alteret og lukker øjnene. En dyb ro falder over dig, og for første gang siden du forlod landsbyen er du ikke bange.",
      effekter: { held: 2, udholdenhed: 2 },
      valg: [{ tekst: "Gå videre gennem skoven", til: 47 }],
    },

    47: {
      stemning: "skov",
      tekst:
        "Ved skovkanten åbner landet sig. På en bakke rejser Ravnetårnet sig, sort og glat. Bag det breder en dampende sump sig, hvor døde birketræer stikker op af tågen som hvide knogler.",
      valg: [
        { tekst: "Gå op ad bakken til tårnets port", til: 61 },
        { tekst: "Gå ned i sumpen bag tårnet", til: 55 },
        { tekst: "Tag genvejen gennem den smalle kløft", til: 32 },
      ],
    },

    32: {
      stemning: "fare",
      billede: "assets/art/egne/edderkoppekloeften.jpg",
      billedtekst: "Edderkoppekløften",
      tekst:
        "Kløften er så smal, at du kan røre begge klippevægge på én gang. Spind hænger mellem stenene som grå gardiner, og der er helt stille.\n\n" +
        "Så ser du otte røde øjne over dig. En edderkop, stor som en kalv, firer sig ned i en sølvtråd. Bag den hænger en hvid kokon, og den bevæger sig.",
      kamp: { navn: "Kæmpeedderkop", evne: 7, udholdenhed: 8 },
      flygt: { tekst: "Løb tilbage ud af kløften", til: 47 },
      valg: [
        { tekst: "Skær kokonen op", til: 34 },
        { tekst: "Skynd dig videre gennem kløften", til: 61 },
      ],
    },

    34: {
      stemning: "skov",
      tekst:
        "Du skærer forsigtigt i spindet. Ud kommer en slank skikkelse med spidse ører og sølvhår. Det er en elver, der har hængt der i tre dage.\n\n" +
        "\"Jeg hedder Liriel,\" siger hun, mens hun gnider liv i sine arme. \"Jeg jagede Morvaks ravn, da edderkoppen tog mig. Tag min bue. Den rammer altid, hvad den sigtes efter, og du har mere brug for den end jeg lige nu.\"\n\n\"Og jeg følger dig til tårnet,\" tilføjer hun og trækker to lange elverdolke. \"Ravnen skylder mig en fjer.\"",
      effekter: { giv: "Elverbue", held: 2, foelge: "Liriel" },
      valg: [{ tekst: "Følg kløften til tårnets fod", til: 61 }],
    },

    37: {
      stemning: "skov",
      tekst:
        "Den gamle drikker grådigt. Så smiler han, og hans øjne glimter pludselig klogt.\n\n" +
        "\"Du har et godt hjerte. Det får du brug for.\" Han trykker en lille nøgle af sølv ned i din hånd. \"Morvaks dør er låst med trolddom, men denne nøgle åbner alle låse, han har lavet.\"\n\n" +
        "Da du ser op, er han væk. Kun en ravnefjer ligger, hvor han sad.",
      effekter: { giv: "Sølvnøgle", held: 1 },
      valg: [{ tekst: "Fortsæt mod tårnet", til: 47 }],
    },

    52: {
      stemning: "fare",
      billede: "assets/art/egne/ulvene.jpg",
      billedtekst: "Øjne i mørket",
      tekst:
        "Du skynder dig forbi. Den gamle mand kalder ikke efter dig.\n\n" +
        "Lidt efter bliver stien til et virvar af tornebuske. Da du endelig kæmper dig ud på den anden side, er dine arme fulde af blødende rifter.\n\n" +
        "Lugten af blod har vækket nogen. To magre ulve glider frem mellem træerne med blottede tænder. Du må kæmpe!",
      effekter: { udholdenhed: -3 },
      kamp: [
        { navn: "Grå ulv", evne: 5, udholdenhed: 5 },
        { navn: "Ulvetæve", evne: 6, udholdenhed: 4 },
      ],
      valg: [
        { tekst: "Læg de helbredende urter på dine sår", til: 59, kraever: "Helbredende urter" },
        { tekst: "Følg ulvenes spor tilbage til deres hule", til: 56 },
        { tekst: "Fortsæt mod tårnet", til: 47 },
      ],
    },

    56: {
      stemning: "skov",
      billede: "assets/art/egne/ulvehulen.jpg",
      billedtekst: "Ulvehulen",
      tekst:
        "Sporene fører til en hule under rødderne af et væltet træ. Indenfor piber tre små ulveunger, der kryber sammen i et hjørne. De er sultne og bange.\n\n" +
        "Bag dem ligger resterne af en rejsende, der ikke var lige så heldig som du. Han bærer stadig en ringbrynje, og en læderpung hænger ved hans bælte.",
      valg: [
        { tekst: "Tag ringbrynjen og pungen", til: 60 },
        { tekst: "Lad hulen være i fred og gå mod tårnet", til: 47 },
      ],
    },

    60: {
      stemning: "skov",
      tekst:
        "Brynjen er tung, men den passer. Ungerne knurrer så tappert, de kan, da du går. Du lægger et stykke tørret kød foran dem, og de holder op.",
      effekter: { loeft: { udholdenhed: 4 }, guld: 3, giv: "Ringbrynje" },
      valg: [{ tekst: "Gå mod tårnet", til: 47 }],
    },

    59: {
      stemning: "skov",
      tekst: "Du gnider urterne ind i bidene. Det svider som ild, men så lukker sårene sig og bliver til tynde, lyserøde ar.",
      effekter: { udholdenhed: 8, tag: "Helbredende urter" },
      valg: [{ tekst: "Fortsæt mod tårnet", til: 47 }],
    },


    // ---------- Karisma-scener (numre fra de ledige pladser under 100) ----------

    2: {
      stemning: "flod",
      tekst:
        "Du fortæller færgemanden om Vildmose, om den stjålne Månesten og om ulvene, der kommer ved fuldmåne. Han siger ingenting længe. Så skubber han hætten tilbage, og du ser et gammelt, vejrbidt ansigt.\n\n" +
        "\"Jeg voksede op i Vildmose,\" siger han. \"Hop om bord. Det her er gratis.\" Midt på floden læner han sig mod dig. \"Morvaks ravn vogter døren. Kald den ved dens rette navn, Korvus, og den lukker dig ind.\"",
      effekter: { giv: "Ordet »Korvus«" },
      valg: [{ tekst: "Gå mod tårnet", til: 61 }],
    },

    3: {
      stemning: "flod",
      tekst: "Færgemanden spytter i floden og vender sig væk. \"Alle har en trist historie. Tre guld, eller også kan du svømme.\"",
      valg: [
        { tekst: "Betal færgemanden", til: 73, kraeverGuld: 3 },
        { tekst: "Svøm over floden", til: 18 },
        { tekst: "Følg bredden mod nord og se efter en bro", til: 21 },
      ],
    },

    4: {
      stemning: "flod",
      tekst:
        "Du kalder trolden en tangbefængt sumpklump med en ånde værre end en død sild, og du siger, at hans bro ser ud, som om en ged har bygget den.\n\n" +
        "Der bliver helt stille. Så slår trolden sig på lårene og brøler af grin, så broen ryster. \"Ha! Endelig en med ordentlig mund på! Alle de andre siger »kære hr. trold« og »undskyld, hr. trold«.\" Han tørrer en tåre væk. \"Gå bare over, du. Du har gjort min dag.\"",
      valg: [{ tekst: "Gå over broen og mod tårnet", til: 61 }],
    },

    5: {
      stemning: "flod",
      tekst:
        "Du roser trolden for hans flotte bro, hans imponerende skæg og hans smukke stemme. Trolden rødmer under tangen. \"Synes du virkelig?\" Han kigger ned i vandet på sit eget spejlbillede.\n\n" +
        "\"Gå bare over,\" mumler han genert. \"Og tag lige det her. Jeg fandt det i floden.\" Han rækker dig et par blanke mønter.",
      effekter: { guld: 2 },
      valg: [{ tekst: "Gå over broen og mod tårnet", til: 61 }],
    },

    6: {
      stemning: "landsby",
      tekst:
        "Du roser Grimbolds tegnefærdigheder, fortæller ham, at Morvak var en tåbe at smide sådan en dygtig mand ud, og du griner af hans dårlige vittigheder. Grimbold smelter som smør. \"Ja, det var han! En tåbe!\" Han skubber kortet over bordet. \"En guld. Fordi det er dig.\"",
      effekter: { guld: -1, giv: "Kort over tårnet" },
      valg: [{ tekst: "Gå tilbage til kroens stue", til: 41 }],
    },

    7: {
      stemning: "landsby",
      tekst: "Grimbold ser koldt på dig med sine gule øjne. \"Tre guld. Ikke en kobberskilling mindre. Og spar mig for dit smil.\"",
      valg: [
        { tekst: "Køb kortet", til: 45, kraeverGuld: 3, mangler: "Kort over tårnet" },
        { tekst: "Gå tilbage til kroens stue", til: 41 },
      ],
    },

    8: {
      stemning: "skov",
      tekst:
        "Du bukker dybt og roser hendes hytte, hendes gryde og hendes flotte, spidse hat. Grimhild fniser som en ung pige. \"Det er hundrede år siden, nogen har sagt pænt goddag til mig!\" Hun klatrer ned ad stigen og tager dig ved armen. \"Kom. Selvfølgelig skal du have hjælp.\"",
      valg: [{ tekst: "Følg med heksen", til: 105 }],
    },

    10: {
      stemning: "hav",
      tekst:
        "Du fortæller Bram om Havets Hjerte og om, at du måske kan finde hans søn derude. Den gamle skipper ser længe ud over havet. Så lægger han sin ru hånd på din skulder. \"Behold dine penge. Hvis du kan bringe min dreng hjem, er det mig, der skylder dig.\"",
      effekter: { held: 1 },
      valg: [{ tekst: "Gå om bord på Mågen", til: 157 }],
    },

    11: {
      stemning: "hav",
      tekst: "Bram ryster på hovedet. \"Søde ord fylder ikke maven på mine folk. Betal, eller tag en skrubbe.\"",
      valg: [
        { tekst: "Betal tre guld", til: 158, kraeverGuld: 3 },
        { tekst: "Arbejd for overfarten", til: 159 },
      ],
    },

    12: {
      stemning: "fare",
      tekst:
        "\"Så smuk en perle,\" siger du og træder tættere på. \"Og så smuk en dronning til at bære den. Ingen i hele havet kan måle sig med dig.\" Morga smiler og læner sig frem, og for et øjeblik holder hun perlen løst. Du griber ud efter den. Hun skriger af raseri, men hun er ude af balance.",
      kamp: { navn: "Havheksen Morga (overrumplet)", evne: 7, udholdenhed: 7 },
      valg: [{ tekst: "Grib Havets Hjerte", til: 195 }],
    },

    14: {
      stemning: "is",
      tekst:
        "Du sætter dig ved fogedens ild og taler med ham om kulden, om kvæget og om hans børn, der ikke har set en sommer i år. Til sidst sukker han. \"Du er et ordentligt menneske. Tag min egen slæde og mine hunde. De kender vejen over gletsjeren. Bare kom med sommeren tilbage.\"",
      valg: [{ tekst: "Kør nordpå mod gletsjeren", til: 211 }],
    },

    15: {
      stemning: "is",
      tekst:
        "Du stiller dig foran kæmpen og kalder ham en overgroet istap med snot i skægget. Kæmpen stirrer på dig. Så begynder han at grine, så sneen falder af fjeldet. \"Ha! Ingen har talt sådan til mig i tusind år! Alle andre ryster i bukserne.\" Han træder til side. \"Gå bare, lille frækkert. Og sig til jarlen, at hans vagt holder fri.\"",
      valg: [{ tekst: "Gå gennem passet", til: 220 }],
    },

    9: {
      stemning: "flod",
      billede: "assets/art/egne/soelvaa-faergen.jpg",
      billedtekst: "Færgemanden ved Sølvå",
      tekst:
        "Floden Sølvå er bred og strømmer hurtigt. Ved bredden ligger en flad pram, og en færgemand med hætte står og læner sig mod sin stage.\n\n" +
        "\"Tre guldstykker for turen,\" siger han uden at se op. \"Eller også kan du svømme. Vandet er koldt i dag.\"",
      valg: [
        { tekst: "Betal færgemanden", til: 73, kraeverGuld: 3 },
        { tekst: "Svøm over floden", til: 18 },
        { tekst: "Følg bredden mod nord og se efter en bro", til: 21 },
        { tekst: "Fortæl færgemanden om Vildmose og bed om en gratis tur", test: "karisma", til: 2, ellers: 3 },
      ],
    },

    21: {
      stemning: "flod",
      billede: "assets/art/egne/troldebroen.jpg",
      billedtekst: "Trolden på stenbroen",
      tekst:
        "En time længere oppe ad floden spænder en gammel stenbro over vandet. Da du sætter foden på den, kravler en trold op over kanten. Den er grå som en klippe, og der hænger tang i dens skæg.\n\n" +
        "\"Ingen går over MIN bro uden at betale!\" brøler den. \"Fem guld, ellers tager jeg dit skind!\"",
      valg: [
        { tekst: "Betal trolden fem guld", til: 25, kraeverGuld: 5 },
        { tekst: "Smigr trolden", test: "karisma", til: 5, ellers: 27 },
        { tekst: "Fornærm trolden groft", til: 4, hoejstKarisma: 8 },
        { tekst: "Træk dit våben og kæmp", til: 27 },
        { tekst: "Gå tilbage til færgestedet", til: 9 },
      ],
    },

    25: {
      stemning: "flod",
      tekst: "Trolden bider i hver mønt for at se, om den er ægte. Så grynter den og træder til side. \"Gå så. Og kom aldrig tilbage.\"",
      effekter: { guld: -5 },
      valg: [{ tekst: "Gå over broen og mod tårnet", til: 61 }],
    },

    27: {
      stemning: "fare",
      tekst: "Trolden brøler og svinger en knortekølle, der er lige så tyk som dit lår.",
      kamp: { navn: "Brotrold", evne: 8, udholdenhed: 8 },
      flygt: { tekst: "Spring ned ad skrænten og løb", til: 9 },
      valg: [{ tekst: "Undersøg troldens hule under broen", til: 28 }],
    },

    28: {
      stemning: "flod",
      tekst:
        "Under broen lugter der af fisk og gammelt råddent tang. Mellem knogler og potteskår finder du en læderpung, som må have tilhørt en mindre heldig rejsende.",
      effekter: { guld: 6 },
      valg: [{ tekst: "Gå over broen og mod tårnet", til: 61 }],
    },

    73: {
      stemning: "flod",
      tekst:
        "Færgemanden stikker mønterne i lommen og skubber prammen ud. Midt på floden siger han lavt:\n\n" +
        "\"Skal du til tårnet? Så husk: Morvaks ravn vogter døren. Kald den ved dens rette navn, Korvus, og den lukker dig ind.\"\n\n" +
        "Prammen skurer mod den anden bred.",
      effekter: { guld: -3, giv: "Ordet »Korvus«" },
      valg: [{ tekst: "Gå mod tårnet", til: 61 }],
    },

    18: {
      stemning: "flod",
      tekst:
        "Vandet er iskoldt og tager pusten fra dig. Strømmen trækker dig langt ned ad floden, før du endelig får fat i en rod og hiver dig op på bredden.\n\n" +
        "Du ryster over hele kroppen, og din fakkel er gennemblødt.",
      effekter: { udholdenhed: -4, tag: "Fakkel" },
      valg: [
        { tekst: "Gå mod tårnet", til: 61 },
        { tekst: "Følg røgen fra en hytte længere nede ad floden", til: 19 },
      ],
    },

    19: {
      stemning: "flod",
      billede: "assets/art/egne/marnas-hytte.jpg",
      billedtekst: "Marnas hytte ved floden",
      tekst:
        "Hytten er lav og lugter af røget fisk. En bredskuldret kone åbner døren, før du når at banke på. Hun ser på dit drivvåde tøj og trækker dig ind til ilden uden et ord.\n\n" +
        "Mens du spiser hendes suppe, fortæller hun, at hun hedder Marna, og at hendes mand byggede stenene til Ravnetårnet for mange år siden. \"Morvak betalte ham aldrig,\" siger hun bittert. \"Men han hørte, hvordan troldmanden styrer sin stengolem. Råber man »Sten, sov!«, så står den stille som en klippe.\" Da du går, stikker hun dig et bundt røget fisk. \"Til turen,\" siger hun.",
      effekter: { udholdenhed: 4, giv: ["Ordet »Sten, sov«", "Tørret fisk"] },
      valg: [{ tekst: "Tak Marna og gå mod tårnet", til: 61 }],
    },

    61: {
      stemning: "taarn",
      billede: "assets/art/egne/ravnetaarnet.jpg",
      billedtekst: "Ravnetårnet",
      tekst:
        "Ravnetårnet rejser sig sort mod himlen. Det er bygget af glat sten uden en eneste fuge. Den eneste dør er af jern og har ingen håndtag.\n\n" +
        "Højt oppe i en vindueskarm sidder en stor sort ravn og ser ned på dig med et rødt øje.",
      valg: [
        { tekst: "Lås døren op med sølvnøglen", til: 85, kraever: "Sølvnøgle" },
        { tekst: "Kald ravnen ved navn: »Korvus!«", til: 85, kraever: "Ordet »Korvus«" },
        { tekst: "Klatr op ad muren til vinduet", test: "held", til: 46, ellers: 44 },
        { tekst: "Bank hårdt på jerndøren", til: 96 },
        { tekst: "Gå rundt om tårnet ned mod sumpen", til: 55 },
      ],
    },

    55: {
      stemning: "fare",
      billede: "assets/art/egne/ravnesumpen.jpg",
      billedtekst: "Ravnesumpen",
      tekst:
        "Bag tårnet bliver jorden blød og sugende. Tågen ligger tæt, og døde birketræer står hvide og nøgne i den. Ude over det sorte vand danser små blå lys, som om de vinker dig til sig.",
      valg: [
        { tekst: "Hold dig til de døde birketræer", til: 62, kraever: "Rygte om sumpstien" },
        { tekst: "Følg de blå lys", til: 57 },
        { tekst: "Vad lige over sumpen mod tårnets bagside", til: 63 },
        { tekst: "Gå tilbage til tårnets port", til: 61 },
      ],
    },

    57: {
      stemning: "fare",
      tekst:
        "Lysene trækker sig væk, hver gang du kommer nærmere. Pludselig forsvinder jorden under dig, og du synker til livet i iskold mudder. Lysene samles over dig og fniser med tynde stemmer.",
      valg: [{ tekst: "Kæmp dig fri", test: "held", til: 64, ellers: 65 }],
    },

    64: {
      stemning: "fare",
      tekst: "Dine fingre får fat i en birkerod. Med dine sidste kræfter trækker du dig op af mudderet. Lysene slukker skuffet, ét efter ét.",
      effekter: { udholdenhed: -2 },
      valg: [{ tekst: "Gå tilbage til sumpens kant", til: 55 }],
    },

    65: {
      stemning: "død",
      tekst: "Jo mere du kæmper, jo hurtigere synker du. Mudderet når dine skuldre, så din hage. Det sidste du ser, er de blå lys, der danser videre over vandet.",
      slut: "død",
      slutnavn: "Sunket i sumpen",
    },

    63: {
      stemning: "fare",
      billede: "assets/art/egne/sumptrolden.jpg",
      billedtekst: "Sumptrolden rejser sig",
      tekst:
        "Du vader ud i det stinkende vand. Midtvejs rejser en klump af mudder og rødder sig foran dig. Den har to små gule øjne og en mund fuld af sorte tænder. Det er en sumptrold!",
      kamp: { navn: "Sumptrold", evne: 8, udholdenhed: 9 },
      flygt: { tekst: "Vad tilbage mod tårnets port", til: 61 },
      valg: [{ tekst: "Vad videre mod tårnets bagside", til: 62 }],
    },

    62: {
      stemning: "taarn",
      tekst:
        "Ved foden af tårnets bagside, halvt skjult af rødder og mos, finder du en lav trædør. Den er ikke låst. Den har nok været glemt i hundrede år.",
      valg: [{ tekst: "Kryb ind ad den lave dør", til: 68 }],
    },

    68: {
      stemning: "taarn",
      billede: "assets/art/egne/kaelderen.jpg",
      billedtekst: "Fangen i kælderen",
      tekst:
        "Du står i en fugtig kælder, hvor vandet drypper fra loftet. I det svage lys fra en lyskasse ser du en ung kvinde, der er lænket til muren. Det er Ilsa, smedens datter fra Vildmose, som forsvandt sidste vinter.\n\n" +
        "\"Befri mig,\" hvisker hun. \"Så hjælper jeg dig. Jeg kender Morvaks hemmelighed.\"",
      valg: [
        { tekst: "Lås lænkerne op med sølvnøglen", til: 70, kraever: "Sølvnøgle" },
        { tekst: "Hug lænkerne over med dit sværd", til: 72 },
        { tekst: "Lad hende være og find trappen op", til: 74 },
      ],
    },

    72: {
      stemning: "fare",
      tekst:
        "Klang! Klang! Det tager mange hug, før lænken springer. Larmen har vækket noget. Ud af hullerne i muren vælter en flok store, grå rotter med røde øjne.",
      kamp: { navn: "Rotteflok", evne: 5, udholdenhed: 6 },
      valg: [{ tekst: "Hjælp Ilsa op at stå", til: 70 }],
    },

    70: {
      stemning: "taarn",
      tekst:
        "Ilsa gnider sine håndled. \"Tak. Hør nu godt efter: Morvak fik sin magt fra et spejl, og hans eget blik er hans svaghed. Ser han sig selv, mens han kaster en forbandelse, rammer den ham selv.\"\n\n" +
        "Hun trækker et lille sølvspejl frem fra sin kjole. \"Jeg stjal det fra ham. Og der er en skjult trappe herfra, der fører lige op til hans kammer.\"\n\n\"Og jeg går med dig,\" siger Ilsa og vikler den knækkede kæde om sin hånd. \"Jeg har en regning at gøre op med Morvak.\"",
      effekter: { giv: "Sølvspejl", held: 2, foelge: "Ilsa" },
      valg: [{ tekst: "Gå op ad den skjulte trappe", til: 29 }],
    },

    74: {
      stemning: "taarn",
      tekst:
        "Du vender ryggen til hendes bønner og finder en smal trappe op til tårnets hovedtrappe. Hendes gråd følger dig et stykke vej op.",
      effekter: { held: -1 },
      valg: [{ tekst: "Fortsæt op ad hovedtrappen", til: 66 }],
    },

    44: {
      stemning: "taarn",
      tekst:
        "Du finder små sprækker til fingrene og begynder at klatre. Halvvejs oppe skriger ravnen og hakker efter dine hænder.\n\n" +
        "Du mister grebet og falder ned i det våde græs med et brag.",
      effekter: { udholdenhed: -5 },
      valg: [
        { tekst: "Prøv at klatre igen", test: "held", til: 46, ellers: 44 },
        { tekst: "Opgiv og bank på døren i stedet", til: 96 },
      ],
    },

    46: {
      stemning: "taarn",
      billede: "assets/art/egne/alkymistvaerkstedet.jpg",
      billedtekst: "Troldmandens værksted",
      tekst:
        "Du svinger dig over vindueskarmen og lander i et værksted fuldt af bobler og damp. Glaskolber syder over små blå flammer, og på en hylde står en rød eliksir med en mærkat: KÆMPESTYRKE.\n\n" +
        "I et fuglebur under loftet sidder en lille grøn kobold med horn, spidse ører og en lang hale. Den ser på dig med store, gyldne øjne. \"Pst! Du der!\" hvisker den. \"Luk mig ud, så skylder jeg dig en tjeneste. En kobold holder altid sit ord!\"",
      varianter: [
        {
          kraever: ["Koboldens løfte", "Tom eliksirflaske"],
          billede: null,
          tekst:
            "Værkstedet bobler og syder som før, og de små blå flammer flakker under glaskolberne. Fugleburet under loftet står åbent og tomt, og på hylden står kun den tomme flaske, hvor den røde eliksir var.\n\n" +
            "Her er ikke mere at hente.",
        },
        {
          kraever: "Koboldens løfte",
          billede: null,
          tekst:
            "Værkstedet bobler og syder som før, og de små blå flammer flakker under glaskolberne. Fugleburet under loftet står åbent og tomt. Pip er væk, men du synes stadig, du kan lugte en svag duft af grøn røg.\n\n" +
            "På hylden står den røde eliksir med mærkaten KÆMPESTYRKE.",
        },
        {
          kraever: "Tom eliksirflaske",
          tekst:
            "Værkstedet bobler og syder som før. Den røde eliksir er drukket, og den tomme flaske står tilbage på hylden.\n\n" +
            "Kobolden i fugleburet trykker ansigtet mod tremmerne. \"Pst! Nu har du fået din styrke,\" hvisker den. \"Luk mig nu ud! En kobold holder altid sit ord!\"",
        },
      ],
      valg: [
        { tekst: "Åbn koboldens bur", til: 48, mangler: "Koboldens løfte" },
        { tekst: "Drik den røde eliksir", til: 49, mangler: "Tom eliksirflaske" },
        { tekst: "Gå ud ad døren til trappen", til: 53 },
      ],
    },

    48: {
      stemning: "taarn",
      tekst:
        "Kobolden springer ud af buret, svinger sig i halen fra en kæde og laver en kolbøtte i luften. \"Fri! Fri!\" Så bukker den dybt for dig.\n\n" +
        "\"Jeg hedder Pip. Når du har brug for mig, så kald på mig. Én gang, og kun én gang.\" Med et lille knald forsvinder den i en sky af grøn røg.",
      effekter: { giv: "Koboldens løfte" },
      valg: [{ tekst: "Se dig om i værkstedet igen", til: 46 }],
    },

    49: {
      stemning: "taarn",
      tekst:
        "Eliksiren brænder som peber i halsen. Dine muskler spænder sig og vokser, og et øjeblik er du sikker på, at du kunne løfte en hest. Men det snurrer også i hovedet, som om lykken er løbet ud af dig.",
      effekter: { loeft: { evne: 1 }, udholdenhed: 4, held: -2, giv: "Tom eliksirflaske" },
      valg: [{ tekst: "Se dig om i værkstedet igen", til: 46 }],
    },

    53: {
      stemning: "taarn",
      tekst:
        "Døren fører ud til den store vindeltrappe. Nedefra hører du knogler, der klaprer mod sten. Ovenfra kommer en svag snorken og et blåt skær.",
      valg: [
        { tekst: "Gå op mod det blå skær", til: 29 },
        { tekst: "Gå ned ad trappen", til: 66 },
        { tekst: "Følg kortet til stenen med ravnetegnet", til: 87, kraever: "Kort over tårnet" },
      ],
    },

    87: {
      stemning: "kammer",
      billede: "assets/art/egne/skattekammeret.jpg",
      billedtekst: "Morvaks skattekammer",
      tekst:
        "Du trykker på stenen med ravnetegnet, og en del af væggen glider til side. Bagved ligger et hvælvet kammer, hvor guldet ligger i bunker på gulvet.\n\n" +
        "På væggen hænger et rundt skjold af grønt dragehud. Midt i rummet står en kiste med jernbeslag, og låget står på klem.",
      valg: [
        { tekst: "Tag dragehudsskjoldet ned fra væggen", til: 88, mangler: "Dragehudsskjold" },
        { tekst: "Åbn kisten", test: "held", til: 89, ellers: 91 },
        { tekst: "Fyld lommerne med mønter fra bunkerne", til: 76 },
        { tekst: "Lad skatten være og gå videre op ad trappen", til: 66 },
      ],
    },

    88: {
      stemning: "kammer",
      tekst: "Skjoldet er let som et blad, men da du banker på det, klinger det som stål. Dragehud kan ikke brænde, og intet sværd kan skære igennem det.",
      effekter: { loeft: { udholdenhed: 3 }, giv: "Dragehudsskjold" },
      valg: [{ tekst: "Se dig om i skattekammeret igen", til: 87 }],
    },

    89: {
      stemning: "kammer",
      tekst:
        "Du løfter låget forsigtigt med spidsen af dit sværd. Klik! En lille nål skyder ud af låsen og ind i luften, hvor din hånd ville have været. I kisten ligger en pung med ædelstene. Ved siden af ligger en lille flaske med en glødende rød eliksir.",
      effekter: { guld: 8, held: 1, giv: "Livseliksir" },
      valg: [{ tekst: "Skynd dig videre op ad trappen", til: 66 }],
    },

    91: {
      stemning: "fare",
      tekst:
        "Du løfter låget, og en lille nål stikker dig i fingeren. Det svier, og en kvalm varme breder sig op ad armen. Giften er svag, men den tærer på dine kræfter. I kisten ligger trods alt en pung med ædelstene.",
      effekter: { udholdenhed: -4, guld: 8 },
      valg: [{ tekst: "Vakl videre op ad trappen", til: 66 }],
    },

    76: {
      stemning: "fare",
      tekst:
        "Du fylder lommerne, indtil de tynger. Men da du træder ud af kammeret, mærker du en isnende kulde. Morvak har lagt en forbandelse på sit guld, og den vil følge dig, så længe du bærer det.",
      effekter: { guld: 10, held: -3 },
      valg: [{ tekst: "Gå videre op ad trappen", til: 66 }],
    },

    96: {
      stemning: "fare",
      tekst:
        "Lyden af dine slag runger gennem tårnet. Så glider jerndøren langsomt op.\n\n" +
        "I døråbningen står en kæmpe af ler og sten, dobbelt så høj som en mand. Dens øjne gløder som kul. Det er en golem, og den løfter sine knytnæver.",
      valg: [
        { tekst: "Råb: »Sten, sov!«", til: 31, kraever: "Ordet »Sten, sov«" },
        { tekst: "Træk dit sværd og kæmp", til: 13 },
        { tekst: "Løb tilbage, før den når dig", til: 33 },
      ],
    },

    31: {
      stemning: "taarn",
      tekst:
        "Golemmen stivner midt i bevægelsen. Gløden i dens øjne blafrer og slukker, og med et dybt suk synker den sammen til en ubevægelig stenblok i døråbningen.\n\n" +
        "Der er lige præcis plads nok til, at du kan klemme dig forbi.",
      valg: [{ tekst: "Klem dig forbi golemmen og gå ind", til: 85 }],
    },

    33: {
      stemning: "taarn",
      tekst:
        "Du kaster dig til side, og golemmens knytnæve rammer jorden, så stenene flyver om ørerne på dig. Den er stærk, men langsom. Du når i sikkerhed bag et stort klippestykke.\n\n" +
        "Golemmen går tungt tilbage, og jerndøren lukker sig igen. En sten har ramt dig på skulderen.",
      effekter: { udholdenhed: -2 },
      valg: [{ tekst: "Gå tilbage til tårnets fod", til: 61 }],
    },

    13: {
      tekst:
        "Dit sværd hugger mod golemmens arm, men klingen knækker, som var den af glas. Kæmpen griber dig, og det sidste du hører, er ravnens hæse latter.",
      slut: "død",
      slutnavn: "Golemmens greb",
    },

    85: {
      stemning: "taarn",
      tekst:
        "Døren glider lydløst op, og ravnen letter fra karmen uden en lyd. Indenfor snor en vindeltrappe sig opad i halvmørket.\n\n" +
        "På et lille bord ved trappens fod står en flaske med en grøn væske, som lyser svagt.",
      valg: [
        { tekst: "Drik den grønne væske", til: 50 },
        { tekst: "Lad flasken stå og gå op ad trappen", til: 66 },
        { tekst: "Undersøg den lave dør bag trappen", til: 68 },
        { tekst: "Følg kortet til stenen med ravnetegnet", til: 87, kraever: "Kort over tårnet" },
      ],
    },

    66: {
      stemning: "fare",
      billede: "assets/art/egne/skeletvagten.jpg",
      billedtekst: "Skeletvagten på trappen",
      tekst:
        "Halvvejs oppe ad vindeltrappen klaprer det over dig. Et skelet i rustent brynje kommer ned ad trinene med en kroget kniv i den knoklede hånd. Morvak har sat en vagt.",
      kamp: { navn: "Skeletvagt", evne: 7, udholdenhed: 6 },
      flygt: { tekst: "Løb ned ad trappen og ud af tårnet", til: 61 },
      valg: [{ tekst: "Fortsæt op ad trappen", til: 29 }],
    },

    50: {
      stemning: "taarn",
      tekst:
        "Væsken smager af mynte og tordenvejr. En varme breder sig i kroppen, og dine sår holder op med at gøre ondt.",
      effekter: { udholdenhed: 6, held: 1 },
      valg: [{ tekst: "Gå op ad trappen", til: 66 }],
    },

    29: {
      stemning: "kammer",
      billede: "assets/art/egne/morvaks-kammer.jpg",
      billedtekst: "Morvaks kammer",
      tekst:
        "Øverst oppe kommer du ind i et rundt kammer fyldt med bøger og glas. Troldmanden Morvak sidder og sover i en lænestol med hagen nede på brystet.\n\n" +
        "På bordet foran ham ligger Månestenen og lyser blåt i mørket.",
      valg: [
        { tekst: "Hold sølvspejlet op foran troldmandens ansigt", til: 80, kraever: "Sølvspejl" },
        { tekst: "Angrib troldmanden med runesværdet", til: 84, kraever: "Runesværd" },
        { tekst: "Kald på kobolden Pip", til: 54, kraever: "Koboldens løfte" },
        { tekst: "Snig dig hen og tag amuletten", til: 77 },
        { tekst: "Væk troldmanden og forhandl med ham", til: 95 },
        { tekst: "Angrib troldmanden, mens han sover", til: 90, mangler: "Runesværd" },
      ],
    },

    54: {
      stemning: "kammer",
      tekst:
        "\"Pip!\" hvisker du. Med et lille knald sidder kobolden på din skulder. Den ser på den sovende troldmand og griner over hele ansigtet.\n\n" +
        "Pip lister hen over bordet, snupper Månestenen og binder i samme bevægelse Morvaks skæg fast til stolen. \"Så er vi kvit!\" fniser den, kaster amuletten til dig og forsvinder for altid.",
      effekter: { giv: "Månestenen", tag: "Koboldens løfte" },
      valg: [{ tekst: "Skynd dig ned ad trappen", til: 92 }],
    },

    95: {
      stemning: "kammer",
      tekst:
        "Du rømmer dig højt. Morvak åbner langsomt øjnene. Han virker hverken overrasket eller bange.\n\n" +
        "\"En helt fra Vildmose,\" siger han og smiler tyndt. \"Hvor kedeligt. Lad mig gøre dig et tilbud: Bliv min lærling. Jeg lærer dig at styre storme og stjerner. Du skal bare glemme den lille landsby.\"",
      valg: [
        { tekst: "Tag imod tilbuddet", til: 97 },
        { tekst: "Afvis ham og grib efter amuletten", test: "held", til: 99, ellers: 90 },
      ],
    },

    97: {
      stemning: "død",
      tekst:
        "Du rækker ham hånden. Morvak lærer dig meget, men det første han lærer dig er at glemme. Snart husker du hverken dit navn eller hvorfor du kom.\n\n" +
        "Den vinter kommer ulvene til Vildmose, og ingen helt kommer for at redde den.",
      slut: "død",
      slutnavn: "Morvaks lærling",
    },

    99: {
      stemning: "fare",
      tekst:
        "\"Aldrig!\" Du kaster dig over bordet. Morvaks forbandelse rammer stolen bag dig, som forvandles til sten. Du har Månestenen i hånden og er allerede på vej ud ad døren.",
      effekter: { giv: "Månestenen" },
      valg: [{ tekst: "Løb ned ad trappen", til: 92 }],
    },

    80: {
      stemning: "kammer",
      tekst:
        "Du stiller dig foran lænestolen med spejlet løftet og rømmer dig. Morvaks øjne springer op. Han rækker hånden frem og råber en forbandelse, men hans blik møder hans eget spejlbillede.\n\n" +
        "Forbandelsen slår tilbage mod ham selv. Fra fødderne og op bliver han grå, hård og tavs. Om et øjeblik står der kun en statue i stolen. Du tager Månestenen fra bordet.",
      effekter: { giv: "Månestenen" },
      valg: [{ tekst: "Forlad tårnet", til: 98 }],
    },

    84: {
      stemning: "fare",
      tekst:
        "Runerne på sværdet flammer op, idet du hæver det. Morvak vågner med et skrig og slynger en lynkugle mod dig, men klingen skærer den over. Nu må du kæmpe mod troldmanden selv!",
      kamp: { navn: "Morvak", evne: 9, udholdenhed: 8 },
      valg: [{ tekst: "Tag Månestenen og forlad tårnet", til: 86 }],
    },

    86: {
      stemning: "kammer",
      tekst: "Morvak falder sammen til en bunke grå aske og en tom kappe. Ravnen flyver skrigende ud ad vinduet og kommer aldrig igen. Du tager Månestenen fra bordet.",
      effekter: { giv: "Månestenen" },
      valg: [{ tekst: "Gå hjem til Vildmose", til: 98 }],
    },

    98: {
      stemning: "sejr",
      billede: "assets/art/egne/hjemkomsten.jpg",
      billedtekst: "Den store sejr",
      tekst:
        "Ravnetårnet står tomt bag dig, og Morvak kan aldrig mere gøre nogen ondt. Hele Vildmose møder dig ved landsbyens port med fakler og sang.\n\n" +
        "Den ældste hænger Månestenen tilbage på sin plads. Fra den dag fortælles historien om dig ved hver eneste ild i landet: helten, der ikke bare hentede amuletten hjem, men også gjorde en ende på troldmanden.",
      slut: "sejr",
      slutnavn: "Den store sejr",
      fortsaet: { til: 101, tekst: "Fortsæt til kapitel 2: Skyggekongen" },
    },

    90: {
      stemning: "fare",
      tekst:
        "Du løfter dit sværd, men Morvaks øjne springer op, før du når at hugge. Han hvisker et enkelt ord, og din krop bliver tung som sten.\n\n" +
        "Fra nu af står du som en statue i hans kammer, endnu et trofæ blandt mange.",
      slut: "død",
      slutnavn: "En statue i kammeret",
    },

    77: {
      stemning: "kammer",
      tekst:
        "Du lister hen over gulvet. Et bræt knirker, og troldmanden mumler i søvne, men han vågner ikke. Dine fingre lukker sig om Månestenen. Den er kold som is.\n\n" +
        "Udenfor skriger ravnen pludselig. Morvak rører på sig.",
      effekter: { giv: "Månestenen" },
      valg: [
        { tekst: "Løb ned ad trappen og ud", test: "held", til: 92, ellers: 81 },
      ],
    },

    81: {
      stemning: "fare",
      tekst:
        "Du er kun nået halvvejs ned ad trappen, da Morvaks stemme gjalder bag dig. Et lyn slår ned i væggen ved siden af dig, og sten og gnister regner ned over dig.",
      effekter: { udholdenhed: -6 },
      valg: [{ tekst: "Løb for livet", til: 92 }],
    },

    92: {
      stemning: "fare",
      billede: "assets/art/egne/ravnens-angreb.jpg",
      billedtekst: "Ravnen angriber",
      tekst:
        "Du er ude af tårnet og løber ned ad bakken. Så hører du vingeslag bag dig. Ravnen fra vindueskarmen styrter efter dig, og nu er den lige så stor som en ørn. Dens røde øjne lyser, og kløerne er rettet mod Månestenen.",
      valg: [
        { tekst: "Skyd ravnen med elverbuen", til: 36, kraever: "Elverbue" },
        { tekst: "Råb: »Korvus! Vend om!«", til: 94, kraever: "Ordet »Korvus«" },
        { tekst: "Vend dig og kæmp mod ravnen", til: 93 },
      ],
    },

    36: {
      stemning: "taarn",
      tekst:
        "Du lægger en pil på buen, sigter og slipper. Pilen synger gennem luften og rammer ravnen i vingen. Den tumler skrigende ned i et tjørnekrat og kommer ikke op igen.\n\n" +
        "Langt væk synes du at høre en elver le.",
      valg: [{ tekst: "Gå hjem mod Vildmose", til: 100 }],
    },

    93: {
      stemning: "fare",
      tekst: "Ravnen dykker skrigende ned over dig med kløer og næb.",
      kamp: { navn: "Korvus", evne: 7, udholdenhed: 6 },
      valg: [{ tekst: "Løb videre hjem mod Vildmose", til: 100 }],
    },

    94: {
      stemning: "taarn",
      tekst:
        "Ravnen bremser i luften, som om den var fløjet ind i en mur. Den ser forvirret på dig, skræpper en enkelt gang og flyver så væk mod nord. Den flyver ikke tilbage mod tårnet. Måske har den ventet længe på at blive kaldt ved sit navn af nogen andre end Morvak.",
      valg: [{ tekst: "Gå hjem mod Vildmose", til: 100 }],
    },

    100: {
      stemning: "sejr",
      billede: "assets/art/egne/hjemkomsten.jpg",
      billedtekst: "Hjemkomsten",
      tekst:
        "Bag dig gjalder Morvaks raseri ud over landet, men du løber og løber, til tårnet kun er en lille sort plet i horisonten.\n\n" +
        "Ved fuldmåne vender du hjem til Vildmose. Den ældste hænger Månestenen tilbage på sin plads, og den nat holder ulvene sig ude i skoven.",
      slut: "sejr",
      slutnavn: "Månestenen vender hjem",
      fortsaet: { til: 101, tekst: "Fortsæt til kapitel 2: Skyggekongen" },
    },

    // =========================================================
    //  KAPITEL 2: SKYGGEKONGEN (afsnit 101–150)
    // =========================================================

    101: {
      kapitel: "Kapitel 2 · Skyggekongen",
      stemning: "skygge",
      billede: "assets/art/egne/maanesten-i-moerke.jpg",
      billedtekst: "Månestenen bliver sort",
      tekst:
        "En måned er gået. Dine sår er helet, og Vildmose har fejret dig, til selv kroværten var træt af at synge. Men en nat vågner du ved, at hundene hyler.\n\n" +
        "Månestenen på sin pæl er ikke længere blå. Den er sort som kul, og rundt om husene glider skikkelser af skygge med lange fingre. Den ældste står i sin dør med et lys i hånden. \"Morvak var ikke alene,\" siger hun. \"Han tjente Skyggekongen Vardrak i ruinbyen Askeborg. Nu drikker Vardrak stenens lys.\"\n\n" +
        "\"Dværgene i Jernbjerget smedede stenen engang. Måske kan de hjælpe. Men skal skyggerne væk for altid, må nogen knuse Vardraks skyggekrystal.\"",
      effekter: { udholdenhed: 30, held: 6, forladAlle: true },
      valg: [
        { tekst: "Pak din oppakning og gå ud over heden", til: 102 },
        { tekst: "Søg først den gamle kone på kroen", til: 103, kraever: "Rygte om sumpstien" },
      ],
    },

    103: {
      stemning: "landsby",
      tekst:
        "Den gamle kone sidder ved ilden, som om hun aldrig har rejst sig. \"Jeg vidste, du ville komme,\" siger hun.\n\n" +
        "\"Skygger frygter sølv og ild. Tag den gamle vej forbi Grimhilds hytte ude i mosen. Hun er heks, men hun skylder mig en tjeneste. Sig, at konen fra Vildmose hilser.\"",
      effekter: { giv: "Konens hilsen" },
      valg: [{ tekst: "Gå ud over heden", til: 102 }],
    },

    102: {
      stemning: "aske",
      billede: "assets/art/egne/heden.jpg",
      billedtekst: "Vejviseren på heden",
      tekst:
        "Heden er øde og grå. Krager sidder i et dødt træ og følger dig med øjnene. Ved en gammel vejviser deler vejen sig i tre.\n\n" +
        "Mod venstre rejser Jernbjerget sig med sne på toppene. Mod højre ligger ruinerne af Askeborg i en sky af støv. Og ligeud forsvinder en smal sti ned i mosen.",
      valg: [
        { tekst: "Tag den smalle sti ned i mosen", til: 104 },
        { tekst: "Gå mod Jernbjerget og dværgene", til: 110 },
        { tekst: "Gå direkte mod ruinbyen Askeborg", til: 120 },
      ],
    },

    // ---------- Heksen Grimhild ----------

    104: {
      stemning: "skov",
      billede: "assets/art/egne/heksehytten.jpg",
      billedtekst: "Grimhilds hytte i mosen",
      tekst:
        "Midt i mosen står en hytte på høje, skæve pæle. Grønt lys siver ud ad vinduerne, og nedenfor bobler en gryde over et bål, som ingen passer.\n\n" +
        "Døren går op, og en lille krumbøjet kvinde med spids hat kigger ned på dig. \"Hvem traver rundt i min mose?\" kvækker hun.",
      valg: [
        { tekst: "Sig: »Konen fra Vildmose hilser«", til: 105, kraever: "Konens hilsen" },
        { tekst: "Bed hende om hjælp mod skyggerne", til: 106 },
        { tekst: "Charmér den gamle heks", til: 8, kraeverKarisma: 10 },
        { tekst: "Gå tilbage til heden", til: 102 },
      ],
    },

    105: {
      stemning: "skov",
      tekst:
        "Grimhild klatrer ned ad stigen med overraskende fart. \"Så den gamle kælling lever endnu,\" griner hun. \"Godt. Så skal du få hjælp.\"\n\n" +
        "Hun smører en salve på dine skrammer og stikker dig en lille pung. \"Sølvpulver. Kast det mod skyggerne, så brænder de som papir. Men der er kun til én gang.\" Hun giver dig også en lille krukke af sin grønne salve. \"Til senere. Du kommer til at få brug for den.\"",
      effekter: { tag: "Konens hilsen", udholdenhed: 6, giv: ["Sølvpulver", "Heksesalve"] },
      valg: [
        { tekst: "Drik af gryden, som Grimhild byder dig", til: 107 },
        { tekst: "Tag afsked og gå mod Jernbjerget", til: 110 },
        { tekst: "Tag afsked og gå mod Askeborg", til: 120 },
      ],
    },

    106: {
      stemning: "skov",
      tekst:
        "\"Hjælp?\" Grimhild ler, så det knirker. \"Intet er gratis i min mose. Enten betaler du fem guld, eller også svarer du på min gåde. Svarer du forkert, gør jeg dig til en tudse et lille stykke tid.\"",
      valg: [
        { tekst: "Betal fem guld", til: 105, kraeverGuld: 5 },
        { tekst: "Hør gåden", til: 108 },
        { tekst: "Gå tilbage til heden", til: 102 },
      ],
    },

    108: {
      stemning: "skov",
      tekst: "Grimhild læner sig ud over gelænderet. \"Hvad bliver større, jo mere man tager fra det?\"",
      valg: [
        { tekst: "»Et hul«", til: 105 },
        { tekst: "»En skygge«", til: 109 },
        { tekst: "»Tiden«", til: 109 },
      ],
    },

    109: {
      stemning: "fare",
      tekst:
        "\"Forkert!\" Grimhild knipser med fingrene. Verden bliver kæmpestor, og du sidder pludselig i mudderet og kvækker. Det varer en hel time, før du er dig selv igen, og du er både våd og ydmyget.",
      effekter: { udholdenhed: -2, held: -2 },
      valg: [{ tekst: "Hink tilbage til heden", til: 102 }],
    },

    107: {
      stemning: "skov",
      tekst:
        "Bryggen smager af tang og torden. Grimhild klukker. \"Nu går lykken dig lidt lettere i møde, min ven.\" Du føler dig underligt let om hjertet.",
      effekter: { loeft: { held: 1 }, udholdenhed: 3 },
      valg: [
        { tekst: "Gå mod Jernbjerget", til: 110 },
        { tekst: "Gå mod Askeborg", til: 120 },
      ],
    },

    // ---------- Jernbjerget ----------

    110: {
      stemning: "bjerg",
      billede: "assets/art/egne/bjergpasset.jpg",
      billedtekst: "Bjergpasset",
      tekst:
        "Vejen op i Jernbjerget bliver stejlere og koldere. Snefnug driver ind i ansigtet, og stien går langs en afgrund.\n\n" +
        "Foran dig spærrer et frosset vandfald vejen. Til højre gaber en gammel mineskakt, og lidt længere oppe ser du en hule, hvor du kunne søge ly for vinden.",
      valg: [
        { tekst: "Klatr over isfaldet", test: "held", til: 112, ellers: 113 },
        { tekst: "Gå ind i den gamle mineskakt", til: 114 },
        { tekst: "Søg ly i hulen", til: 111 },
      ],
    },

    111: {
      stemning: "fare",
      tekst:
        "Hulen er ikke tom. En hvid, pjusket kæmpe rejser sig fra en bunke knogler. Det er en snetrold, og den er sulten.",
      kamp: { navn: "Snetrold", evne: 8, udholdenhed: 9 },
      flygt: { tekst: "Løb ud i sneen igen", til: 110 },
      valg: [{ tekst: "Følg trollets fodspor op til dværgeporten", til: 116 }],
    },

    112: {
      stemning: "bjerg",
      tekst:
        "Du hugger trin i isen med dit sværd og kravler op, hånd for hånd. Øverst kan du se ind i en dal mellem tinderne, og der, hugget ind i klippen, ligger en kæmpe port.",
      valg: [{ tekst: "Gå hen til porten", til: 116 }],
    },

    113: {
      stemning: "fare",
      tekst:
        "Halvvejs oppe knækker isen. Du glider ned og slår hoved og skuldre mod klippen. Da du har fået vejret igen, finder du en anden vej rundt om vandfaldet, og den fører til en kæmpe port i klippen.",
      effekter: { udholdenhed: -5 },
      valg: [{ tekst: "Hink hen til porten", til: 116 }],
    },

    114: {
      stemning: "bjerg",
      billede: "assets/art/egne/mineskakten.jpg",
      billedtekst: "Den gamle dværgemine",
      tekst:
        "Mineskakten er bygget af dværge for længe siden. Gamle skinner fører ind i mørket, og en malmvogn står glemt ved indgangen. Langt inde blinker noget gult. Det er øjne.",
      valg: [
        { tekst: "Tænd din fakkel", til: 115, kraever: "Fakkel" },
        { tekst: "Famle dig frem i mørket", til: 117 },
      ],
    },

    115: {
      stemning: "bjerg",
      tekst:
        "Fakkellyset jager de gule øjne på flugt. Det var bare grottekobolder, og de hader ild. På væggen hænger en gammel stentavle med en indgraveret rune. Under den står der med dværgeskrift: Til venner af Jernbjerget.\n\n" +
        "Du tager tavlen med dig. Gangen fører opad og ud i lyset tæt ved en kæmpe port.",
      effekter: { giv: "Dværgerune" },
      valg: [{ tekst: "Gå hen til porten", til: 116 }],
    },

    117: {
      stemning: "fare",
      tekst: "I mørket kommer de krybende: en flok grottekobolder med rustne knive og gule øjne. De fniser, mens de omringer dig.",
      kamp: [
        { navn: "Grottekobold", evne: 5, udholdenhed: 4 },
        { navn: "Grottekoboldernes høvding", evne: 7, udholdenhed: 6 },
      ],
      valg: [{ tekst: "Følg gangen ud i lyset", til: 116 }],
    },

    116: {
      stemning: "bjerg",
      billede: "assets/art/egne/dvaergeporten.jpg",
      billedtekst: "Dværgeporten",
      tekst:
        "Porten er så høj som ti mænd og dækket af gyldne runer. På hver side står en dværg af sten med økse og hjelm. Der er ingen håndtag og ingen nøglehuller.",
      valg: [
        { tekst: "Læg dværgerunen mod porten", til: 118, kraever: "Dværgerune" },
        { tekst: "Bank på med sværdfæstet", til: 119 },
      ],
    },

    119: {
      stemning: "bjerg",
      tekst:
        "En luge åbner sig højt oppe, og et skægget ansigt kigger ned. \"Hvem banker?\" brummer det. \"Vi lukker ingen ind, siden Vardrak sendte sine skygger.\"\n\n" +
        "Du holder Månestenen op. Dværgen stirrer på den, og så går porten op med et drøn. \"Den sten smedede min oldefar,\" siger han. \"Jeg hedder Brokk. Kom ind.\"",
      valg: [{ tekst: "Følg Brokk ind i bjerget", til: 118 }],
    },

    118: {
      stemning: "smedje",
      billede: "assets/art/egne/dvaergesmedjen.jpg",
      billedtekst: "Smedjen i Jernbjerget",
      tekst:
        "Dybt inde i bjerget brænder dværgenes esse. Den gamle smed Thrain vejer Månestenen i sin hånd og ryster på hovedet. \"Den er bundet til Vardraks krystal. Jeg kan ikke rense den, så længe krystallen lever.\"\n\n" +
        "Men han tager dit sværd og lægger det i ilden. I en time hamrer han, mens gnisterne flyver. Da han giver det tilbage, er klingen blå som is og skarp som et ord.\n\n" +
        "\"Brokk viser dig vores gamle tunnel,\" siger Thrain. \"Den ender lige under Vardraks borg.\"",
      effekter: { tag: "Dværgerune", loeft: { evne: 2 }, udholdenhed: 4, giv: "Dværgestålsværd" },
      valg: [{ tekst: "Følg Brokk ind i tunnelen", til: 140 }],
    },

    140: {
      stemning: "bjerg",
      tekst:
        "Tunnelen er lang og lav. Brokk går foran med en lygte og fortæller historier om sin oldefar. Efter mange timer standser han. Et stykke af loftet er styrtet sammen, og kun en smal sprække er tilbage.\n\n" +
        "\"Herfra må du alene,\" siger han. \"Jeg er for bred om livet. Pas på stenene, de sidder løst.\"",
      valg: [{ tekst: "Kravl gennem sprækken", test: "held", til: 144, ellers: 146 }],
    },

    146: {
      stemning: "fare",
      tekst: "Midt i sprækken skrider stenene. Du får trukket dig fri, men en klippeblok rammer dig over ryggen.",
      effekter: { udholdenhed: -4 },
      valg: [{ tekst: "Kravl videre", til: 144 }],
    },

    144: {
      stemning: "skygge",
      tekst:
        "Tunnelen ender bag en væg af vintønder. Du er i Skyggeborgens vinkælder. Over dig hører du tunge skridt og en dyb, hul stemme, der giver ordrer.",
      valg: [{ tekst: "Snig dig op ad kældertrappen til tronsalen", til: 136 }],
    },

    // ---------- Askeborg ----------

    120: {
      stemning: "aske",
      billede: "assets/art/egne/askeborg.jpg",
      billedtekst: "Ruinbyen Askeborg",
      tekst:
        "Askeborg var engang en stolt by. Nu står kun ruinerne tilbage, og alt er dækket af grå aske. Skygger glider mellem husene uden en lyd. Bag byen tårner Skyggeborgen sig op med lilla lys i vinduerne.\n\n" +
        "Du kan gå ind ad den store byport, kravle ned i kloakken, eller følge en lille pige, der vinker til dig fra en ruin.",
      valg: [
        { tekst: "Gå ind ad den store byport", til: 121 },
        { tekst: "Kravl ned i kloakken", til: 125 },
        { tekst: "Følg den lille pige", til: 128 },
      ],
    },

    121: {
      stemning: "fare",
      tekst:
        "Inden for porten rejser to skikkelser sig fra asken. Det er skyggehunde med røde øjne og tænder som istapper. De knurrer, og asken hvirvler op om dem.",
      valg: [
        { tekst: "Kast sølvpulveret mod hundene", til: 122, kraever: "Sølvpulver" },
        { tekst: "Kæmp mod skyggehundene", til: 123 },
      ],
    },

    122: {
      stemning: "aske",
      tekst: "Sølvpulveret glitrer i luften. Hundene hyler, og der, hvor støvet rammer dem, brænder de op som papir. Kun to små askebunker er tilbage.",
      effekter: { tag: "Sølvpulver" },
      valg: [{ tekst: "Gå ind på torvet", til: 124 }],
    },

    123: {
      stemning: "fare",
      tekst: "Skyggehundene springer.",
      kamp: [
        { navn: "Skyggehund", evne: 6, udholdenhed: 5 },
        { navn: "Skyggehund", evne: 7, udholdenhed: 5 },
      ],
      valg: [{ tekst: "Gå ind på torvet", til: 124 }],
    },

    124: {
      stemning: "aske",
      tekst:
        "På byens torv står en statue af Vardrak med en krone af torne. Ved siden af den ligger en brønd med vand, så sort som blæk. Gaden op mod borgen er stejl og tom.",
      valg: [
        { tekst: "Kig ned i den sorte brønd", til: 126, mangler: "Syn af tronen" },
        { tekst: "Undersøg statuen", til: 127 },
        { tekst: "Gå op mod Skyggeborgen", til: 130 },
      ],
    },

    126: {
      stemning: "skygge",
      tekst:
        "Vandet bliver til et spejl. Du ser en tronsal, en skikkelse med en krone af skygge, og bag tronen en lilla krystal, der pulserer som et hjerte. Så griber kulden dig, og du trækker dig væk med rystende hænder.\n\n" +
        "Men nu ved du, hvor krystallen sidder.",
      effekter: { udholdenhed: -3, giv: "Syn af tronen" },
      valg: [{ tekst: "Gå tilbage til torvet", til: 124 }],
    },

    127: {
      stemning: "aske",
      tekst:
        "Bag statuens fod finder du et håndtag. Du hiver i det, og statuen drejer sig med en skurrende lyd. Bagved fører en skjult trappe op mod borgen. Nogen har kendt denne vej før dig.",
      effekter: { held: 1 },
      valg: [{ tekst: "Gå op ad den skjulte trappe", til: 130 }],
    },

    125: {
      stemning: "fare",
      billede: "assets/art/egne/kloakken.jpg",
      billedtekst: "Kloakken under Askeborg",
      tekst:
        "Kloakken stinker, og vandet går dig til knæene. Rotter piler langs kanten. Så bølger vandet, og en kæmpe orm med en mund fuld af tænder rejser sig foran dig.",
      kamp: { navn: "Kloakorm", evne: 7, udholdenhed: 8 },
      flygt: { tekst: "Kravl op af kloakken igen", til: 120 },
      valg: [{ tekst: "Undersøg ormens rede", til: 129 }],
    },

    129: {
      stemning: "aske",
      tekst:
        "I ormens rede mellem knogler og skrammel finder du en rusten nøgle med Vardraks tegn. Kloakken fører dig op gennem en rist lige under borgens mur.",
      effekter: { giv: "Rusten nøgle" },
      valg: [{ tekst: "Kravl op til Skyggeborgen", til: 130 }],
    },

    128: {
      stemning: "aske",
      billede: "assets/art/egne/spoegelsespigen.jpg",
      billedtekst: "Ylva",
      tekst:
        "Pigen er gennemsigtig som tåge, og hun bærer en lille gylden krone. \"Jeg hedder Ylva,\" hvisker hun. \"Jeg var prinsesse her, før Vardrak kom. Nu kan jeg ikke komme videre.\"\n\n" +
        "Hun fører dig gennem ruinerne ad veje, som skyggerne ikke kender. \"Hvis du besejrer ham,\" siger hun, \"så husk mig.\"",
      effekter: { giv: "Ylvas løfte", held: 2 },
      valg: [{ tekst: "Følg Ylva op til borgen", til: 130 }],
    },

    // ---------- Skyggeborgen ----------

    130: {
      stemning: "skygge",
      billede: "assets/art/egne/skyggeborgen.jpg",
      billedtekst: "Skyggeborgen",
      tekst:
        "Skyggeborgen er sort, og dens tårne er så spidse som spyd. Himlen over den drejer langsomt rundt, som om borgen trækker alt lyset til sig. En bred trappe fører op til hovedporten. Ved muren er en lav sidedør, og højt oppe står et vindue åbent.",
      valg: [
        { tekst: "Gå op ad hovedtrappen", til: 132 },
        { tekst: "Lås sidedøren op med den rustne nøgle", til: 134, kraever: "Rusten nøgle" },
        { tekst: "Klatr op til det åbne vindue", test: "held", til: 133, ellers: 131 },
      ],
    },

    131: {
      stemning: "fare",
      tekst: "Stenene er glatte af aske. Du glider og falder ned på trappen med et brag. Heldigvis hørte ingen det.",
      effekter: { udholdenhed: -4 },
      valg: [{ tekst: "Rejs dig og se dig om igen", til: 130 }],
    },

    132: {
      stemning: "fare",
      tekst:
        "Øverst på trappen står en ridder i rustning af sort aske. Hvor hans ansigt skulle være, gløder to kul. \"Ingen går forbi Askeridderen,\" siger han og hæver sit sværd.",
      kamp: { navn: "Askeridderen", evne: 9, udholdenhed: 10 },
      flygt: { tekst: "Løb ned til torvet", til: 124 },
      valg: [{ tekst: "Gå ind i tronsalen", til: 136 }],
    },

    133: {
      stemning: "skygge",
      tekst:
        "Vinduet fører ind på et smalt galleri højt over tronsalen. Lige under dig sidder Vardrak på sin trone, og bag den pulserer den lilla krystal. Ingen har set dig.",
      valg: [
        { tekst: "Spring ned og knus krystallen", test: "held", til: 145, ellers: 142 },
        { tekst: "Klatr forsigtigt ned ad en søjle", til: 136 },
      ],
    },

    134: {
      stemning: "skygge",
      tekst:
        "Den rustne nøgle passer, men den knækker i låsen, da du drejer den. Døren går dog op, og bagved ligger et fangehul. Bag tremmerne sidder en snes fanger: bønder, købmænd og et par dværge. De ser på dig med store øjne. \"Hjælp os,\" hvisker en af dem. \"Så hjælper vi dig.\"",
      effekter: { tag: "Rusten nøgle" },
      valg: [
        { tekst: "Tag fangevogterens nøgleknippe fra krogen og lås cellerne op", til: 135 },
        { tekst: "Skynd dig videre mod tronsalen", til: 136 },
      ],
    },

    135: {
      stemning: "skygge",
      tekst:
        "Fangevogterens nøgler passer i alle låse. Fangerne griber kæppe, kæder og hvad de ellers kan finde. \"Når du giver tegn,\" siger den største dværg, \"så stormer vi ind og holder hans skygger beskæftiget.\"",
      effekter: { giv: "Fangernes hjælp", held: 1 },
      valg: [{ tekst: "Gå op mod tronsalen", til: 136 }],
    },

    136: {
      stemning: "skygge",
      billede: "assets/art/egne/tronsalen.jpg",
      billedtekst: "Skyggekongen Vardrak",
      tekst:
        "Tronsalen er så stor, at loftet forsvinder i mørket. For enden sidder Vardrak på en trone af sort sten. Han er høj og mager, og hans krone er lavet af levende skygge. Bag tronen pulserer krystallen i lilla lys.\n\n" +
        "\"Månestenens bærer,\" siger han roligt. \"Tak, fordi du bragte den helt hen til mig.\" Skyggerne langs væggene rejser sig.",
      valg: [
        { tekst: "Kast sølvpulveret mod skyggerne", til: 137, kraever: "Sølvpulver" },
        { tekst: "Giv tegn til fangerne", til: 137, kraever: "Fangernes hjælp" },
        { tekst: "Skyd en pil mod krystallen med elverbuen", til: 138, kraever: "Elverbue" },
        { tekst: "Løb uden om tronen hen til krystallen", til: 141, kraever: "Syn af tronen" },
        { tekst: "Angrib Vardrak med dværgestålet", til: 139, kraever: "Dværgestålsværd" },
        { tekst: "Gå til angreb på Vardrak", til: 143, mangler: "Dværgestålsværd" },
      ],
    },

    137: {
      stemning: "fare",
      tekst:
        "Salen bliver fyldt med larm og lys. Skyggerne har travlt, og for et øjeblik står Vardrak alene uden sine tjenere. Han rejser sig fra tronen og trækker et sværd af mørke.",
      effekter: { tag: ["Sølvpulver", "Fangernes hjælp"] },
      kamp: { navn: "Vardrak (svækket)", evne: 8, udholdenhed: 9 },
      valg: [{ tekst: "Knus krystallen", til: 145 }],
    },

    138: {
      stemning: "skygge",
      tekst:
        "Vardrak griner, da du hæver buen. \"Ingen pil kan ramme mig.\" Men du sigter ikke efter ham. Elverpilen synger forbi hans øre og rammer krystallen midt i hjertet.\n\n" +
        "Der lyder et skrig, som om hele borgen skriger på én gang.",
      valg: [{ tekst: "Se krystallen splintres", til: 145 }],
    },

    139: {
      stemning: "fare",
      tekst:
        "Dværgestålet lyser blåt, da du trækker det. Vardraks smil forsvinder. \"Dværgearbejde,\" hvæser han og rejser sig fra tronen.",
      kamp: { navn: "Vardrak", evne: 10, udholdenhed: 12 },
      valg: [{ tekst: "Knus krystallen", til: 145 }],
    },

    141: {
      stemning: "fare",
      tekst:
        "Du ved præcis, hvor krystallen sidder. Mens Vardrak rejser sig, kaster du dig i et langt spring rundt om tronen.",
      valg: [{ tekst: "Hug mod krystallen", test: "held", til: 145, ellers: 143 }],
    },

    143: {
      stemning: "fare",
      tekst: "Vardrak er hurtigere, end du troede. Han står foran dig med et sværd af ren skygge, og hans øjne brænder.",
      kamp: { navn: "Vardrak", evne: 11, udholdenhed: 14 },
      valg: [{ tekst: "Knus krystallen", til: 145 }],
    },

    142: {
      stemning: "død",
      tekst:
        "Du lander skævt, og før du når krystallen, har skyggerne fået fat i dig. De er kolde som vinternat, og de bliver ved med at trække. Det sidste du ser, er Månestenen, der glider ud af din hånd og forsvinder i mørket.",
      slut: "død",
      slutnavn: "Opslugt af skyggerne",
    },

    145: {
      stemning: "kammer",
      tekst:
        "Krystallen springer i tusind stykker. En storm af skygger farer ud gennem vinduerne og bliver til ingenting i morgenlyset. Vardrak strækker en hånd ud mod dig, men han smuldrer til aske, før han når at sige noget.\n\n" +
        "I din oppakning bliver det varmt. Månestenen lyser igen, klarere og mere blå end nogensinde.",
      valg: [
        { tekst: "Kald på Ylva", til: 148, kraever: "Ylvas løfte" },
        { tekst: "Gå hjem mod Vildmose", til: 147 },
      ],
    },

    147: {
      stemning: "landsby",
      tekst:
        "Rejsen hjem tager mange dage, men den føles let. Krager flyver ikke længere efter dig. Ved Jernbjerget hilser dværgene fra deres port, og ude i mosen vinker en lille kvinde med spids hat.",
      valg: [{ tekst: "Gå det sidste stykke hjem", til: 150 }],
    },

    148: {
      stemning: "kammer",
      tekst:
        "\"Ylva!\" råber du. Hun kommer gående gennem en væg, og denne gang er hun ikke gennemsigtig. Krystallen holdt hende fanget. Nu er hun fri.\n\n" +
        "Hele Askeborgs folk kommer frem fra ruinerne: dem, der overlevede, og dem, der blev fanget som skygger. De falder på knæ for deres prinsesse. Hun tager din hånd. \"Askeborg skal genopbygges,\" siger hun, \"og du skal altid være velkommen her.\"",
      effekter: { tag: "Ylvas løfte" },
      valg: [{ tekst: "Bliv til kroningsfesten", til: 149 }],
    },

    149: {
      stemning: "sejr",
      billede: "assets/art/egne/lysets-sejr.jpg",
      billedtekst: "Lyset vender tilbage",
      tekst:
        "Ylva bliver kronet i den genopbyggede tronsal, og du står ved hendes side. Bagefter rejser du hjem til Vildmose med en karavane af dværge, bønder og købmænd.\n\n" +
        "Den nat hænger Månestenen igen på sin pæl, og dens sølvlys når helt ud til Askeborg. Fra den dag hedder du ikke bare helten fra Vildmose. Du hedder Lysbringeren.",
      slut: "sejr",
      slutnavn: "Lysbringeren",
      fortsaet: { til: 151, tekst: "Fortsæt til kapitel 3: Havets Sang" },
    },

    150: {
      stemning: "sejr",
      billede: "assets/art/egne/lysets-sejr.jpg",
      billedtekst: "Lyset vender tilbage",
      tekst:
        "Vildmose tager imod dig med fakler, lygter og sang. Den ældste hænger Månestenen tilbage på pælen, og den lyser så klart, at selv skyggerne under sengene forsvinder.\n\n" +
        "Den nat danser hele landsbyen under stenens lys. Skyggekongen er væk, og Vildmose har en helt, som har reddet den to gange.",
      slut: "sejr",
      slutnavn: "Helten fra Vildmose",
      fortsaet: { til: 151, tekst: "Fortsæt til kapitel 3: Havets Sang" },
    },

    // =========================================================
    //  KAPITEL 3: HAVETS SANG (afsnit 151–200)
    // =========================================================

    151: {
      kapitel: "Kapitel 3 · Havets Sang",
      stemning: "hav",
      billede: "assets/art/egne/havets-stilhed.jpg",
      billedtekst: "Havet er blevet tavst",
      tekst:
        "Foråret kommer til Vildmose, og Månestenen lyser klarere end nogensinde. Men en morgen står en udmattet budbringer fra havnebyen Saltvig ved landsbyens port.\n\n" +
        "\"Havet er blevet tavst,\" siger han. \"Ingen bølger synger, ingen fisk går i garnene, og skibe forsvinder sporløst. Om natten hører sømændene en sang ude fra skærene, og de, der følger den, kommer aldrig hjem.\"\n\n" +
        "Den nat viser Månestenen dig et syn: en sunket by af marmor dybt under vandet, og en kvinde med hår som tang, der holder en lysende perle i sine hænder. Havets Hjerte. Uden det mister havet sin sang.",
      effekter: { udholdenhed: 30, held: 6, forladAlle: true },
      valg: [{ tekst: "Rejs til Saltvig", til: 152 }],
    },

    152: {
      stemning: "hav",
      billede: "assets/art/egne/saltvig.jpg",
      billedtekst: "Havnen i Saltvig",
      tekst:
        "Saltvig ligger ved mundingen af Sølvå, hvor floden møder havet. Garnene hænger tomme til tørre, og mågerne er tavse. I havnen ligger kun to skibe, der er klar til at sejle.\n\n" +
        "Det ene er »Mågen«, en gammel, lappet kogge. Dens skipper, Bram, er gråhåret og har venlige øjne. Det andet er »Hajen«, et sort, smalt skib med røde sejl, som tilhører smugleren Skarre. Han smiler med en guldtand.",
      valg: [
        { tekst: "Spørg skipper Bram om plads på Mågen", til: 153 },
        { tekst: "Tal med smugleren Skarre", til: 156 },
        { tekst: "Gå ind på havnekroen og hør nyt", til: 154 },
      ],
    },

    154: {
      stemning: "landsby",
      billede: "assets/art/egne/havnekroen.jpg",
      billedtekst: "Havnekroen »Ankeret«",
      tekst:
        "Kroen lugter af tjære og saltvand. En gammel enbenet sømand vinker dig hen til sit bord. \"Skal du ud til skærene?\" spørger han. \"Så husk det her: Sirenernes sang får selv den stærkeste mand til at styre mod klipperne. Stop voks i ørerne, eller bind dig til masten.\"\n\n" +
        "Kroværten har et lille lerkrus med bivoks på hylden.",
      valg: [
        { tekst: "Køb bivoks til ørerne (1 guld)", til: 155, kraeverGuld: 1, mangler: "Bivoks" },
        { tekst: "Gå tilbage til havnen", til: 152 },
      ],
    },

    155: {
      stemning: "landsby",
      tekst: "Kroværten ruller to små kugler af gul bivoks og giver dig dem i en klud. \"Til ørerne,\" siger han og blinker. \"Ikke til brødet.\"",
      effekter: { guld: -1, giv: "Bivoks" },
      valg: [{ tekst: "Gå tilbage til havnen", til: 152 }],
    },

    153: {
      stemning: "hav",
      tekst:
        "Bram klør sig i skægget. \"Ud til skærene? Det er galskab. Men min søn sejlede derud for en måned siden og kom aldrig hjem.\" Han ser på dig. \"Tre guld for turen. Har du dem ikke, kan du skrubbe dæk.\"",
      valg: [
        { tekst: "Betal tre guld", til: 158, kraeverGuld: 3 },
        { tekst: "Arbejd for overfarten", til: 159 },
        { tekst: "Fortæl Bram, at du måske kan finde hans søn", test: "karisma", til: 10, ellers: 11 },
      ],
    },

    158: {
      stemning: "hav",
      tekst: "Bram stikker mønterne i lommen og giver dig hånden. Hans hånd er ru som tovværk. \"Vi sejler ved højvande.\"",
      effekter: { guld: -3 },
      valg: [{ tekst: "Gå om bord på Mågen", til: 157 }],
    },

    159: {
      stemning: "hav",
      tekst: "Du skrubber dæk, splejser tov og bærer tønder, til armene værker. Men da solen går ned, nikker Bram anerkendende. \"Du er sejere end du ser ud.\"",
      effekter: { udholdenhed: -2, held: 1 },
      valg: [{ tekst: "Sejl ud med Mågen", til: 157 }],
    },

    156: {
      stemning: "hav",
      tekst:
        "Skarre læner sig op ad rælingen. \"Havets Hjerte, siger du? Hvis den heks har perlen, har hun også alt guldet fra de skibe, hun har sænket.\" Han rækker hånden frem. \"Jeg sejler dig gratis derud. Til gengæld får jeg halvdelen af det guld, du finder. Aftale?\"",
      valg: [
        { tekst: "Giv ham hånden på det", til: 160 },
        { tekst: "Gå tilbage og find et andet skib", til: 152 },
      ],
    },

    160: {
      stemning: "hav",
      tekst:
        "Hajen skærer gennem bølgerne som en kniv. Første nat vågner du ved, at en mager sømand lister hen mod din oppakning med en kniv i hånden. Hans øjne skinner grådigt i månelyset. Han vil have Månestenen.",
      effekter: { giv: "Skarres aftale" },
      kamp: { navn: "Grådig sømand", evne: 7, udholdenhed: 6 },
      valg: [{ tekst: "Kast ham over bord og sov videre", til: 164 }],
    },

    164: {
      stemning: "hav",
      tekst:
        "Næste morgen ser Skarre på den tomme køje og trækker på skuldrene. \"Han var alligevel ikke god til at splejse tov.\" Men du ser, at han holder øje med dig nu. Ved middagstid dukker de første sorte skær op i horisonten, og sømændene bliver stille.",
      valg: [{ tekst: "Sejl mod skærene", til: 165 }],
    },

    157: {
      stemning: "hav",
      tekst:
        "Mågen knirker og stønner, men den holder kursen. På andendagen bliver himlen sort mod vest, og vinden begynder at hyle i riggen. Bram bider tænderne sammen. \"Hold fast i noget, der er sømmet fast!\"",
      valg: [{ tekst: "Stormen bryder løs", til: 161 }],
    },

    161: {
      stemning: "fare",
      billede: "assets/art/egne/stormen.jpg",
      billedtekst: "Stormen",
      tekst:
        "Bølger, høje som huse, slår ind over dækket. Masten bøjer sig som et siv, og tovværket hugger i dine hænder. Bram råber noget, men vinden river ordene væk.",
      valg: [{ tekst: "Kæmp dig hen til sejlet", test: "held", til: 162, ellers: 163 }],
    },

    162: {
      stemning: "hav",
      tekst:
        "Med fælles kræfter får I sejlet bjærget, og Mågen rider stormen af. Ved daggry er havet blankt og stille, alt for stille. Bram klapper dig på skulderen. \"Uden dig var vi gået ned.\"",
      effekter: { held: 1 },
      valg: [{ tekst: "Sejl videre mod skærene", til: 165 }],
    },

    163: {
      stemning: "fare",
      tekst:
        "En bølge river dig over bord. Det sorte vand lukker sig over dig, og du synker. Så griber en kold hånd om dit håndled. Et ansigt med sølvgrønt hår og øjne som perlemor ser på dig. Det er en havfrue.\n\n" +
        "Hun trækker dig op til overfladen og løfter dig op til rælingen. \"Jeg hedder Nerea,\" hvisker hun. \"Havet er sygt. Hvis du vil hjælpe os, så tag dette.\" Hun lægger et skinnende skæl i din hånd. \"Med det kan du ånde under vand. Men kun én gang.\"",
      effekter: { udholdenhed: -4, giv: "Nereas skæl" },
      valg: [{ tekst: "Hold dig fast og sejl videre", til: 165 }],
    },

    165: {
      stemning: "fare",
      billede: "assets/art/egne/sirenernes-skaer.jpg",
      billedtekst: "Sirenernes skær",
      tekst:
        "Skærene rejser sig af havet som sorte tænder. Så begynder sangen. Den er det smukkeste, du nogensinde har hørt, og den kalder på dig. Rorsmanden drejer langsomt roret mod klipperne med et drømmende smil på læben.",
      valg: [
        { tekst: "Stop bivoks i ørerne og tag roret", til: 166, kraever: "Bivoks" },
        { tekst: "Bind dig selv til masten", til: 167 },
      ],
    },

    167: {
      stemning: "fare",
      tekst:
        "Du surrer tovet om dig selv og masten, så hårdt du kan. Sangen river i dig, og du kæmper mod tovet, men det holder. Nu skal du bare få rorsmanden til at vågne.",
      valg: [{ tekst: "Råb til rorsmanden af alle kræfter", test: "held", til: 166, ellers: 168 }],
    },

    166: {
      stemning: "hav",
      tekst:
        "Du river roret til dig og styrer uden om de sorte klipper. Sangen bliver svagere og svagere bag jer, og sømændene ryster på hovedet som efter en lang søvn. Foran jer ligger åbent hav.",
      effekter: { tag: "Bivoks" },
      valg: [{ tekst: "Sejl videre", til: 169 }],
    },

    168: {
      stemning: "fare",
      tekst:
        "For sent! Skibet skraber mod klipperne med et skrig af splintret træ. Du bliver slynget mod rælingen. Vandet fosser ind, og I når lige akkurat at sætte jollen i vandet, før skibet synker. I ror mod et lys på en ø ude i horisonten.",
      effekter: { udholdenhed: -5 },
      valg: [{ tekst: "Ro mod lyset", til: 170 }],
    },

    169: {
      stemning: "fare",
      billede: "assets/art/egne/soeslangen.jpg",
      billedtekst: "Søslangen",
      tekst:
        "Vandet foran stævnen begynder at boble. Så rejser en kæmpe søslange sig af havet. Den har skæl som grønne skjolde og et hoved så stort som en båd, og dens øjne gløder af den samme syge farve, som havet har haft siden perlen forsvandt.",
      valg: [
        { tekst: "Skyd en pil mellem dens øjne med elverbuen", til: 171, kraever: "Elverbue" },
        { tekst: "Hold Månestenen op mod uhyret", til: 174 },
        { tekst: "Træk dit våben og kæmp", til: 172 },
      ],
    },

    171: {
      stemning: "hav",
      tekst:
        "Uhyret skriger og kaster hovedet tilbage. Et øjeblik efter glider det ned under bølgerne igen og forsvinder i dybet. Sømændene jubler.",
      valg: [{ tekst: "Sejl videre mod øen med fyrtårnet", til: 173 }],
    },

    174: {
      stemning: "fare",
      tekst: "Du løfter Månestenen højt. Den blå glød vokser og vokser, mens slangen hvæser mod dig.",
      valg: [{ tekst: "Lad stenen lyse med al sin kraft", test: "held", til: 171, ellers: 172 }],
    },

    172: {
      stemning: "fare",
      tekst: "Søslangen kaster sig over skibet. Du står ved rælingen med våbnet klar.",
      kamp: { navn: "Søslange", evne: 9, udholdenhed: 11 },
      valg: [{ tekst: "Sejl videre mod øen med fyrtårnet", til: 173 }],
    },

    173: {
      stemning: "hav",
      tekst: "Ved solnedgang kaster I anker ved en lille klippeø. Øverst på øen står et fyrtårn, men lampen er slukket.",
      valg: [{ tekst: "Gå i land", til: 170 }],
    },

    170: {
      stemning: "hav",
      billede: "assets/art/egne/fyrtaarnet.jpg",
      billedtekst: "Fyrtårnet på klippeøen",
      tekst:
        "En smal sti snor sig op til fyrtårnet. I døren står en gammel kvinde med hvidt hår og et sjal om skuldrene. \"Jeg hedder Hedda,\" siger hun. \"Fyret gik ud den nat, havet blev tavst. Siden da har jeg ikke kunnet tænde det.\"",
      valg: [
        { tekst: "Klatr op og prøv at tænde fyret", til: 175 },
        { tekst: "Spørg Hedda om Havheksen", til: 176 },
      ],
    },

    175: {
      stemning: "hav",
      tekst: "Øverst i tårnet står den store lampe med sine polerede spejle. Olien er der, men vægen vil ikke fænge, som om noget kvæler flammen.",
      valg: [
        { tekst: "Tænd vægen med din fakkel", til: 177, kraever: "Fakkel" },
        { tekst: "Slå gnister med dit sværd mod stenen", test: "held", til: 177, ellers: 178 },
      ],
    },

    178: {
      stemning: "fare",
      tekst: "Gnisterne springer, og pludselig blusser olien op i dit ansigt. Du brænder dine hænder, men flammen fænger.",
      effekter: { udholdenhed: -2 },
      valg: [{ tekst: "Se lyset sprede sig", til: 177 }],
    },

    177: {
      stemning: "sejr",
      tekst:
        "Fyret flammer op, og spejlene kaster en lang, gylden stråle ud over havet. Langt ude hører du en svag lyd, som når en hval synger.\n\n" +
        "Hedda har tårer i øjnene. Hun giver dig en lille fløjte af hvalben. \"Min mand var hvalfanger, før han blev fyrpasser. Blæs i den, når du står over revet, så kommer hvalerne.\"",
      effekter: { giv: "Hvalbensfløjte", held: 2 },
      valg: [{ tekst: "Sejl mod revet over den sunkne by", til: 179 }],
    },

    176: {
      stemning: "hav",
      tekst:
        "\"Morga,\" siger Hedda stille. \"Hun var engang en havfrue, men hun ville herske over hele havet. Nu bor hun i den sunkne by Ulmar under revet. Byen sank for tusind år siden.\"\n\n" +
        "\"For at komme derned skal du kunne ånde under vand. I bugten ligger en gammel dykkerklokke fra de gode dage, men jeg ved ikke, om den stadig holder tæt.\"",
      valg: [
        { tekst: "Prøv at tænde fyret for hende først", til: 175 },
        { tekst: "Sejl mod revet", til: 179 },
      ],
    },

    179: {
      stemning: "hav",
      tekst:
        "Over revet er vandet klart som glas. Dybt under jer ser du spirer af hvidt marmor og ødelagte kupler, og alt er dækket af tang. Det er den sunkne by Ulmar. Ingen fisk svømmer dernede.",
      valg: [
        { tekst: "Læg Nereas skæl på tungen og spring i", til: 180, kraever: "Nereas skæl" },
        { tekst: "Blæs i hvalbensfløjten", til: 182, kraever: "Hvalbensfløjte" },
        { tekst: "Dyk med den gamle dykkerklokke", til: 181 },
      ],
    },

    180: {
      stemning: "hav",
      tekst:
        "Skællet smelter på din tunge som is. Du springer i, og i stedet for vand fylder du lungerne med noget køligt og klart. Du kan ånde! Med lange svømmetag glider du ned mod byen.",
      effekter: { tag: "Nereas skæl" },
      valg: [{ tekst: "Svøm ned til Ulmar", til: 183 }],
    },

    182: {
      stemning: "hav",
      tekst:
        "Fløjtens tone er så lys, at du næsten ikke kan høre den. Men et øjeblik efter bryder en gammel, ar-dækket hval vandoverfladen. Den puster en kæmpe sølvskinnende luftboble omkring dig og bærer dig blidt ned i dybet.",
      effekter: { tag: "Hvalbensfløjte", held: 1 },
      valg: [{ tekst: "Lad hvalen bære dig ned", til: 183 }],
    },

    181: {
      stemning: "fare",
      tekst: "Dykkerklokken er af bronze og grøn af ir. Du kravler ind under den, og sømændene firer den langsomt ned i dybet. Halvvejs nede hører du en hvislende lyd.",
      valg: [{ tekst: "Hold vejret og håb", test: "held", til: 183, ellers: 184 }],
    },

    184: {
      stemning: "fare",
      tekst: "En revne! Vandet sprøjter ind, og luften forsvinder. Du må forlade klokken og svømme det sidste stykke med brændende lunger. Lige før du besvimer, finder du en luftlomme under en sunket kuppel.",
      effekter: { udholdenhed: -4 },
      valg: [{ tekst: "Kom til hægterne og se dig om", til: 183 }],
    },

    183: {
      stemning: "hav",
      billede: "assets/art/egne/ulmar.jpg",
      billedtekst: "Den sunkne by Ulmar",
      tekst:
        "Ulmar er smuk og trist på samme tid. Gader af hvidt marmor, statuer af havfolk, og lysende vandmænd, der svæver som lygter mellem søjlerne. Langt inde i byen gløder et grønligt lys fra et slot af perlemor.\n\n" +
        "Til venstre ligger et stort skibsvrag mellem klipperne. Til højre hører du svage, klagende stemmer bag en mur af koraller.",
      valg: [
        { tekst: "Følg lyset mod slottet", til: 185 },
        { tekst: "Undersøg skibsvraget", til: 186 },
        { tekst: "Følg de klagende stemmer", til: 187 },
      ],
    },

    186: {
      stemning: "fare",
      billede: "assets/art/egne/skibsvraget.jpg",
      billedtekst: "Skibsvraget",
      tekst:
        "Vraget er en gammel krigsgalej, og i dens lastrum glimter guld og en trefork af blåt metal. Men da du nærmer dig, rejser en kæmpe krabbe sig fra sandet. Dens klosaks er større end din overkrop.",
      kamp: { navn: "Kæmpekrabbe", evne: 8, udholdenhed: 8 },
      valg: [{ tekst: "Tag skatten fra vraget", til: 188 }],
    },

    188: {
      stemning: "hav",
      tekst:
        "Treforken er let i hånden og summer svagt, som om havet selv lever i den. Den blev smedet af havfolket til at bekæmpe Morga, står der med gamle tegn langs skaftet. Du fylder også lommerne med guld.",
      effekter: { giv: "Havfolkets trefork", loeft: { evne: 1 }, guld: 8 },
      valg: [{ tekst: "Svøm mod slottet", til: 185 }],
    },

    187: {
      stemning: "fare",
      billede: "assets/art/egne/havfolket.jpg",
      billedtekst: "Havfolkets fangenskab",
      tekst:
        "Bag koralmuren hænger bure af sort koral, og i dem sidder havfolk: mænd, kvinder og børn med fiskehaler og sørgmodige øjne. Blandt dem genkender du måske Nerea. To kæmpe ål med lysende tænder snor sig om burene som vagter.",
      kamp: [
        { navn: "Vagtål", evne: 7, udholdenhed: 6 },
        { navn: "Stor vagtål", evne: 8, udholdenhed: 7 },
      ],
      valg: [{ tekst: "Bryd burene op", til: 189 }],
    },

    189: {
      stemning: "hav",
      tekst:
        "Du hugger korallåsene over én efter én. Havfolket strømmer ud, og deres ældste, en gammel havmand med perler i skægget, lægger hånden på dit hoved. \"Vi står i gæld til dig. Når du kæmper mod Morga, kæmper vi med dig.\"\n\nHan giver dig en lille, glinsende perle, og havfruen Nerea svømmer op ved din side. \"Jeg følger dig til Morga,\" siger hun. \"Min sang kan hele dine sår.\"",
      effekter: { giv: ["Havfolkets løfte", "Havets perle"], held: 2, foelge: "Nerea" },
      valg: [{ tekst: "Svøm mod slottet", til: 185 }],
    },

    185: {
      stemning: "fare",
      billede: "assets/art/egne/havheksens-grotte.jpg",
      billedtekst: "Indgangen til Havheksens slot",
      tekst:
        "Slottets port er et kæmpe muslingeskal, der står på klem. Foran den ligger noget, du først tror er et klippefremspring. Så åbner det et øje. Det er en kæmpe blæksprutte, og dens arme er lange som master.",
      valg: [
        { tekst: "Giv havfolket tegn til at angribe", til: 192, kraever: "Havfolkets løfte" },
        { tekst: "Snig dig forbi i skyggen af søjlerne", test: "held", til: 191, ellers: 190 },
        { tekst: "Kæmp mod blæksprutten", til: 190 },
      ],
    },

    192: {
      stemning: "hav",
      tekst: "Havfolket strømmer frem fra alle sider med spyd og net. Blæksprutten sprøjter sort blæk og forsvinder i et virvar af arme. Vejen er fri.",
      effekter: { tag: "Havfolkets løfte" },
      valg: [{ tekst: "Svøm ind i slottet", til: 191 }],
    },

    190: {
      stemning: "fare",
      tekst: "Blæksprutten opdager dig, og dens arme kommer piskende mod dig.",
      kamp: { navn: "Kæmpeblæksprutte", evne: 9, udholdenhed: 10 },
      valg: [{ tekst: "Svøm ind i slottet", til: 191 }],
    },

    191: {
      stemning: "skygge",
      billede: "assets/art/egne/havheksen.jpg",
      billedtekst: "Havheksen Morga",
      tekst:
        "I slottets sal sidder Morga på en trone af koral. Hendes hår bølger som tang, og hendes hale er sort som blæk. I hænderne holder hun Havets Hjerte, en perle så stor som et æble, der lyser i alle havets farver.\n\n" +
        "\"Månestenens bærer,\" siger hun med en stemme som en bølge, der trækker sig tilbage. \"Lad os handle. Giv mig din sten, så får du min perle. Så kan din landsby få sit hav, og jeg får månen.\"",
      valg: [
        { tekst: "Hold sølvspejlet op foran hende", til: 196, kraever: "Sølvspejl" },
        { tekst: "Angrib hende med havfolkets trefork", til: 197, kraever: "Havfolkets trefork" },
        { tekst: "Smigr Morga og lok hende tættere på", test: "karisma", til: 12, ellers: 194 },
        { tekst: "Tag imod handlen", til: 193 },
        { tekst: "Afvis hende og angrib", til: 194 },
      ],
    },

    193: {
      stemning: "død",
      tekst:
        "Du rækker hende Månestenen. Morga smiler, og hendes smil er det sidste, du ser, før havet lukker sig om dig. Hun havde aldrig tænkt sig at give dig perlen.\n\n" +
        "Den nat bliver Månestenen sort i Vildmose, og ulvene kommer.",
      slut: "død",
      slutnavn: "Havheksens handel",
    },

    196: {
      stemning: "fare",
      tekst:
        "Morga hæver hånden for at kaste en forbandelse, men i det samme ser hun sit eget spejlbillede i Morvaks gamle sølvspejl. Forbandelsen slår tilbage mod hende selv. Hun skriger, og hendes greb om perlen løsner sig.",
      kamp: { navn: "Havheksen Morga (svækket)", evne: 7, udholdenhed: 8 },
      valg: [{ tekst: "Grib Havets Hjerte", til: 195 }],
    },

    197: {
      stemning: "fare",
      tekst:
        "Da Morga ser treforken, farer hun tilbage. \"Den blev smedet til at dræbe mig!\" hvæser hun. Men hun trækker en kniv af sort skal og går til angreb.",
      kamp: { navn: "Havheksen Morga", evne: 8, udholdenhed: 9 },
      valg: [{ tekst: "Grib Havets Hjerte", til: 195 }],
    },

    194: {
      stemning: "fare",
      tekst: "\"Så må du synke som alle de andre,\" siger Morga og rejser sig fra tronen. Vandet omkring hende bliver koldt og sort.",
      kamp: { navn: "Havheksen Morga", evne: 10, udholdenhed: 12 },
      valg: [{ tekst: "Grib Havets Hjerte", til: 195 }],
    },

    195: {
      stemning: "sejr",
      tekst:
        "Morga opløses i sort skum og forsvinder med strømmen. Havets Hjerte falder ned i dine hænder, og i samme øjeblik begynder havet at synge. Fisk strømmer ind gennem gaderne, havfolket danser, og langt over dig hører du hvalerne svare.\n\n" +
        "Hvalerne bærer dig op til overfladen, hvor skibet venter.",
      effekter: { giv: "Havets Hjerte" },
      valg: [
        { tekst: "Skarre venter ved rælingen med hånden fremme", til: 198, kraever: "Skarres aftale" },
        { tekst: "Sejl hjem mod Saltvig", til: 199, mangler: "Skarres aftale" },
      ],
    },

    198: {
      stemning: "hav",
      tekst:
        "\"Aftale er aftale,\" siger Skarre og ser på din pung. Du holder dit ord og deler guldet med ham. Han tæller det, griner og slår dig på skulderen. \"Du er den første ærlige person, jeg har sejlet med. Det må jeg vænne mig til.\"",
      effekter: { tag: "Skarres aftale", guld: -5 },
      valg: [{ tekst: "Sejl hjem mod Saltvig", til: 199 }],
    },

    199: {
      stemning: "landsby",
      tekst:
        "Da I sejler ind i Saltvig, står hele byen på kajen. Havets Hjerte bliver sat på sin plads i den gamle havkirke, og samme aften er garnene fulde af sild. Bram finder sin søn, som havde siddet fanget i Ulmar sammen med havfolket.",
      effekter: { tag: "Havets Hjerte" },
      valg: [{ tekst: "Fejr sejren", til: 200 }],
    },

    200: {
      stemning: "sejr",
      billede: "assets/art/egne/havets-sang.jpg",
      billedtekst: "Havet synger igen",
      tekst:
        "Den nat sidder du på kajen og ser solen gå ned i havet. Hvaler blæser springvand i horisonten, og bølgerne synger mod molen. I Vildmose fortæller de nu historien om den helt, der reddede både månen og havet.",
      slut: "sejr",
      slutnavn: "Havet synger igen",
      fortsaet: { til: 201, tekst: "Fortsæt til kapitel 4: Dragens Vinter" },
    },

    // =========================================================
    //  KAPITEL 4: DRAGENS VINTER (afsnit 201–250)
    // =========================================================

    201: {
      kapitel: "Kapitel 4 · Dragens Vinter",
      stemning: "is",
      billede: "assets/art/egne/evig-vinter.jpg",
      billedtekst: "Vinteren, der ikke vil slutte",
      tekst:
        "Sommeren kom aldrig til Vildmose det år. Sneen faldt midt i juli, floden frøs til, og om natten hørte man et brøl fra nord, så dybt at jorden rystede.\n\n" +
        "Nu folder den ældste et gammelt kort ud på bordet. \"I Nordfjeldene sover isdragen Isvinge,\" siger hun. \"Hun har sovet i tusind år. Hvis hun er vågnet, er det fordi nogen har gjort hende vred. Og så kommer vinteren for at blive.\"",
      effekter: { udholdenhed: 30, held: 6, forladAlle: true },
      valg: [
        { tekst: "Drag nordpå mod Frostby", til: 202 },
      ],
    },

    202: {
      stemning: "is",
      tekst:
        "Vejen nordpå er dækket af sne til knæene. Efter tre dage når du til et vejkryds. Mod øst ligger Jernbjerget, hvor dværgene bor. Mod nord fører vejen direkte til Frostby, den sidste by før fjeldene.",
      valg: [
        { tekst: "Søg hjælp hos dværgene først", til: 203 },
        { tekst: "Fortsæt direkte til Frostby", til: 204 },
      ],
    },

    203: {
      stemning: "smedje",
      tekst:
        "Brokk tager imod dig med et brøl af glæde og et krus varm mjød. \"Nordfjeldene? Så har du brug for de her.\" Han giver dig et par isbrodder af dværgestål, der kan spændes under støvlerne. \"Med dem kan du gå på blankis, som var det et stuegulv.\"\n\nSå tager han sin økse ned fra væggen. \"Og jeg går med dig. Jeg har altid villet se en drage – helst på afstand, men man kan jo ikke få alt.\"",
      effekter: { giv: ["Isbrodder", "Dværgemjød"], udholdenhed: 4, foelge: "Brokk" },
      valg: [{ tekst: "Tak Brokk og drag mod Frostby", til: 204 }],
    },

    204: {
      stemning: "is",
      billede: "assets/art/egne/frostby.jpg",
      billedtekst: "Frostby",
      tekst:
        "Frostby er en by af tømmerhuse begravet i sne. Folk går med bøjet hoved, og kun røgen fra skorstenene viser, at her bor nogen. Over byen ligger Frostjarlens stenhal.\n\n" +
        "Ved markedspladsen ser du en skikkelse, du kender: en mand med hætte og gule øjne. Det er Grimbold fra kroen i Vildmose. Han lister ind i et pakhus og ser sig nervøst over skulderen.",
      valg: [
        { tekst: "Følg efter Grimbold", til: 205, mangler: "Sporet efter ægget" },
        { tekst: "Gå op til Frostjarlens hal", til: 206 },
        { tekst: "Køb en hundeslæde på markedet (4 guld)", til: 207, kraeverGuld: 4 },
      ],
    },

    205: {
      stemning: "fare",
      tekst:
        "Inde i pakhuset står Grimbold bøjet over en tom trækasse fyldt med halm. I halmen er der et rundt aftryk, så stort som et vognhjul, og kanten er dækket af rimfrost.\n\n" +
        "\"Det var bare en sten,\" mumler han for sig selv. \"En stor, kold sten. Hvordan skulle jeg vide, at det var et drageæg?\"",
      valg: [
        { tekst: "Træd frem og konfronter ham", til: 208 },
        { tekst: "Bliv i skjul og lyt", til: 209 },
      ],
    },

    208: {
      stemning: "fare",
      tekst:
        "Grimbold farer sammen og falder over kassen. \"Du! Nej, nej, jeg vidste det ikke!\" Han rækker hænderne op. \"Frostjarlen Hrimgar betalte mig hundrede guld for at hente det i fjeldene. Det ligger nu i hans isslot bag gletsjeren.\"\n\n" +
        "Han roder i sin kappe og giver dig et sammenrullet pergament. \"Her er tegningerne af slottet. Der er en skjult dør på østsiden. Bare lad mig gå!\"",
      effekter: { giv: ["Grimbolds kort", "Sporet efter ægget"] },
      valg: [{ tekst: "Lad ham løbe og gå tilbage til markedet", til: 204 }],
    },

    209: {
      stemning: "fare",
      tekst:
        "Grimbold taler med sig selv, mens han tæller mønter. Han har stjålet dragens æg fra fjeldene og solgt det til Frostjarlen Hrimgar, som har bragt det til sit isslot bag gletsjeren. Jarlen vil opfostre dragen og bruge den som våben.\n\n" +
        "Du lister ud, før han ser dig. Nu ved du, hvorfor Isvinge er så vred.",
      effekter: { held: 1, giv: "Sporet efter ægget" },
      valg: [{ tekst: "Gå tilbage til markedet", til: 204 }],
    },

    206: {
      stemning: "is",
      tekst:
        "Frostjarlens hal er næsten tom. Kun hans foged, en mager mand med pelskrave, sidder ved ilden. \"Jarlen er ude i sit isslot,\" siger han kort. \"Men hvis du vil tjene en hundeslæde, kan du jage frostulvene, der angriber vores kvæg.\"",
      valg: [
        { tekst: "Tag imod opgaven", til: 210 },
        { tekst: "Overtal fogeden til at låne dig en slæde", til: 14, kraeverKarisma: 10 },
        { tekst: "Gå tilbage til markedet", til: 204 },
      ],
    },

    210: {
      stemning: "fare",
      tekst: "Uden for byen finder du flokken i sneen. To frostulve med hvid pels og øjne som blåt is går til angreb.",
      kamp: [
        { navn: "Frostulv", evne: 7, udholdenhed: 6 },
        { navn: "Frostulvenes leder", evne: 8, udholdenhed: 7 },
      ],
      valg: [{ tekst: "Hent din belønning: en hundeslæde", til: 211 }],
    },

    207: {
      stemning: "is",
      tekst: "En gammel kvinde sælger dig en slæde og seks hunde med blå øjne og tyk pels. \"De kender vejen over gletsjeren bedre end nogen mand,\" siger hun.",
      effekter: { guld: -4 },
      valg: [{ tekst: "Kør nordpå mod gletsjeren", til: 211 }],
    },

    211: {
      stemning: "is",
      billede: "assets/art/egne/gletsjeren.jpg",
      billedtekst: "Over gletsjeren",
      tekst:
        "Hundene trækker slæden ud over den store gletsjer. Isen er blå og knirker under mederne, og dybe sprækker åbner sig til begge sider. Foran dig spænder en smal bro af is over en kløft, der er så dyb, at du ikke kan se bunden.",
      valg: [
        { tekst: "Spænd isbrodderne på og led hundene over", til: 213, kraever: "Isbrodder" },
        { tekst: "Kør over isbroen", test: "held", til: 213, ellers: 212 },
        { tekst: "Tag den lange vej rundt om kløften", til: 214 },
      ],
    },

    212: {
      stemning: "fare",
      tekst:
        "Midt på broen knækker isen. Hundene når over, men du bliver slynget af slæden og falder ned i kløften. Du lander hårdt på en isskrænt langt nede. Ved siden af dig åbner sig en grotte af blå is.",
      effekter: { udholdenhed: -5 },
      valg: [{ tekst: "Kravl ind i isgrotten", til: 215 }],
    },

    215: {
      stemning: "is",
      tekst:
        "I grotten står en kriger frosset fast i isen, som han har stået i hundreder af år. På armen bærer han et skjold af hvidt metal med en drage indgraveret. Isen omkring skjoldet er smeltet en anelse, som om det venter på dig.\n\n" +
        "Du løsner skjoldet. Bagerst i grotten fører en tunnel opad, og du kan høre dine hunde gø.",
      effekter: { giv: "Frostskjold", loeft: { udholdenhed: 3 } },
      valg: [{ tekst: "Kravl op til hundene", til: 213 }],
    },

    214: {
      stemning: "is",
      tekst: "Den lange vej tager to dage. Kulden bider gennem din kappe, og om natten må du grave dig ned i sneen sammen med hundene for at holde varmen.",
      effekter: { udholdenhed: -3 },
      valg: [{ tekst: "Kør videre", til: 213 }],
    },

    213: {
      stemning: "is",
      billede: "assets/art/egne/nordlys.jpg",
      billedtekst: "Nordlysets dal",
      tekst:
        "Bag gletsjeren ligger en stille dal, hvor nordlyset danser i grønt og violet over himlen. Langt ude glimter isslottet som en krystal. På en sten ved vejen sidder en kæmpe sneugle og ser på dig med gyldne øjne.\n\n" +
        "Vejen deler sig. Den ene går gennem et pas, hvor noget stort bevæger sig i sneen. Den anden fører ind i nogle iskolde grotter.",
      valg: [
        { tekst: "Gå hen til sneuglen", til: 248, mangler: "Uglefjer" },
        { tekst: "Tag passet", til: 216 },
        { tekst: "Gå gennem isgrotterne", til: 217 },
      ],
    },

    248: {
      stemning: "is",
      tekst:
        "Uglen drejer hovedet og taler med en stemme som vind i fyrretræer. \"Isvinge er min gamle veninde. Hendes vrede er sorg, ikke ondskab. Giv hende ægget tilbage, og vinteren slutter.\"\n\n" +
        "Den lader en hvid fjer falde ned i din hånd. \"Vis hende denne, så ved hun, at du kommer som ven.\"",
      effekter: { giv: "Uglefjer", held: 1 },
      valg: [
        { tekst: "Tag passet", til: 216 },
        { tekst: "Gå gennem isgrotterne", til: 217 },
      ],
    },

    216: {
      stemning: "fare",
      billede: "assets/art/egne/frostkaempen.jpg",
      billedtekst: "Frostkæmpen i passet",
      tekst:
        "Midt i passet rejser en kæmpe sig af sneen. Han er tre gange så høj som en mand, hans skæg er af istapper, og hans øjne er blå som gletsjeren. \"Ingen går forbi Hrimgars vagt,\" buldrer han. \"Medmindre de kan svare på min gåde.\"",
      valg: [
        { tekst: "Vis ham dit sværd af dværgestål", til: 221, kraever: "Dværgestålsværd" },
        { tekst: "Svar på gåden", til: 218 },
        { tekst: "Kald ham en overgroet istap", til: 15, hoejstKarisma: 7 },
        { tekst: "Træk dit våben og kæmp", til: 219 },
      ],
    },

    221: {
      stemning: "is",
      tekst:
        "Kæmpen ser på det blå dværgestål og bøjer langsomt hovedet. \"Thrains arbejde. Hans folk og mit folk var venner engang.\" Han træder til side. \"Gå, dværgeven. Jeg har aldrig brudt mig om den jarl alligevel.\"",
      valg: [{ tekst: "Gå gennem passet", til: 220 }],
    },

    218: {
      stemning: "is",
      tekst: "Kæmpen bøjer sig ned, så hans ånde fryser i dit hår. \"Hvad bliver vådere, jo mere det tørrer?\"",
      valg: [
        { tekst: "»Et håndklæde«", til: 220 },
        { tekst: "»Is«", til: 222 },
        { tekst: "»Sne«", til: 222 },
      ],
    },

    222: {
      stemning: "fare",
      tekst: "\"Forkert!\" brøler kæmpen og slynger dig gennem luften. Du lander i en snedrive nede i dalen.",
      effekter: { udholdenhed: -3 },
      valg: [{ tekst: "Kom på benene igen", til: 213 }],
    },

    219: {
      stemning: "fare",
      tekst: "Kæmpen løfter en knytnæve så stor som en tønde.",
      kamp: { navn: "Frostkæmpe", evne: 10, udholdenhed: 12 },
      flygt: { tekst: "Løb tilbage ned i dalen", til: 213 },
      valg: [{ tekst: "Gå gennem passet", til: 220 }],
    },

    217: {
      stemning: "fare",
      tekst: "Grotterne lyser af blå krystaller. Midt i den største sal rejser en istrold sig fra gulvet. Dens krop er hård og gennemsigtig som is.",
      kamp: { navn: "Istrold", evne: 8, udholdenhed: 9 },
      valg: [{ tekst: "Følg grotten ud på den anden side", til: 220 }],
    },

    220: {
      stemning: "is",
      billede: "assets/art/egne/isslottet.jpg",
      billedtekst: "Frostjarlens isslot",
      tekst:
        "Isslottet rejser sig foran dig med tårne af klar is, der fanger nordlyset. Ved hovedporten står to vagter i hvide rustninger med lange spyd.",
      valg: [
        { tekst: "Find den skjulte dør på østsiden", til: 223, kraever: "Grimbolds kort" },
        { tekst: "Gå til angreb på vagterne ved porten", til: 224 },
        { tekst: "Klatr op ad isvæggen", test: "held", til: 225, ellers: 226 },
      ],
    },

    223: {
      stemning: "is",
      tekst: "Grimbolds kort er overraskende nøjagtigt. Bag en isblok på østsiden finder du en lille dør, der fører ind i slottets kældre.",
      valg: [{ tekst: "Snig dig ind", til: 225 }],
    },

    224: {
      stemning: "fare",
      tekst: "Vagterne sænker spydene og kommer mod dig.",
      kamp: [
        { navn: "Isvagt", evne: 8, udholdenhed: 7 },
        { navn: "Isvagt", evne: 8, udholdenhed: 7 },
      ],
      valg: [{ tekst: "Gå ind i slottet", til: 225 }],
    },

    226: {
      stemning: "fare",
      tekst: "Halvvejs oppe glider dine fingre på den blanke is. Du falder ned i sneen med et brag.",
      effekter: { udholdenhed: -4 },
      valg: [{ tekst: "Kom på benene igen", til: 220 }],
    },

    225: {
      stemning: "is",
      tekst:
        "Slottets gange er af klar is, og nordlyset skinner ned gennem loftet i grønne og violette strømme. Fra en gang til venstre kommer et blåt skær, der pulserer som et hjerte. Fra en gang til højre hører du stemmer og latter. Lige frem står en dør på klem til et kammer fuldt af glimtende ting.",
      valg: [
        { tekst: "Følg det blå skær", til: 227 },
        { tekst: "Følg stemmerne", til: 228 },
        { tekst: "Kig ind i kammeret med de glimtende ting", til: 247, mangler: "Frostkrone" },
      ],
    },

    247: {
      stemning: "kammer",
      tekst:
        "Kammeret er Frostjarlens skatkammer. Mellem kister af sølv ligger en smal krone af blåt is, der aldrig smelter. Da du sætter den på, bliver dine tanker klare og rolige.",
      effekter: { giv: "Frostkrone", loeft: { held: 2 } },
      valg: [{ tekst: "Gå tilbage til gangen", til: 225 }],
    },

    227: {
      stemning: "fare",
      billede: "assets/art/egne/dragens-aeg.jpg",
      billedtekst: "Dragens æg",
      tekst:
        "I en sal af blå is ligger ægget i en vugge af frost. Det er så stort som en kiste og dækket af skæl, der lyser som stjerner. Foran det står en isgolem, lavet af blokke af gletsjeris. Dens øjne tændes, da du træder ind.",
      valg: [
        { tekst: "Skyd en pil mod krystallen i golemmens bryst", til: 230, kraever: "Elverbue" },
        { tekst: "Kæmp mod isgolemmen", til: 229 },
      ],
    },

    230: {
      stemning: "fare",
      tekst: "Pilen rammer den lysende krystal i golemmens bryst. Den knækker med en lyd som en klokke, og golemmen falder sammen til en bunke isblokke.",
      valg: [{ tekst: "Løft ægget", til: 231 }],
    },

    229: {
      stemning: "fare",
      tekst: "Golemmen træder frem med drønende skridt, og isen revner under den.",
      kamp: { navn: "Isgolem", evne: 9, udholdenhed: 10 },
      valg: [{ tekst: "Løft ægget", til: 231 }],
    },

    231: {
      stemning: "fare",
      tekst:
        "Ægget er tungt og koldt, men da du løfter det, mærker du, at noget derinde bevæger sig. I det samme går døren op. I åbningen står Frostjarlen Hrimgar med sit sværd draget.\n\n" +
        "\"Tyv!\" brøler han. \"Det æg er mit!\"",
      effekter: { giv: "Dragens æg" },
      valg: [{ tekst: "Sæt ægget forsigtigt ned og kæmp", til: 232 }],
    },

    228: {
      stemning: "fare",
      billede: "assets/art/egne/frostjarlen.jpg",
      billedtekst: "Frostjarlen Hrimgar",
      tekst:
        "I tronsalen sidder Frostjarlen Hrimgar med en kappe af isbjørneskind og en krone af istapper. Hans hofmænd ler og drikker.\n\n" +
        "\"Helten fra Vildmose!\" råber han. \"Jeg har hørt om dig. Slut dig til mig! Når min drage vokser op, hersker vi to over hele Norden.\"",
      valg: [
        { tekst: "Lad som om du siger ja", til: 233 },
        { tekst: "Afvis ham og træk dit sværd", til: 232 },
      ],
    },

    233: {
      stemning: "fare",
      tekst: "Du bukker og smiler. Hrimgar ler og vil vise dig sin skat.",
      valg: [{ tekst: "Smil, nik og følg med", test: "karisma", til: 227, ellers: 232 }],
    },

    232: {
      stemning: "fare",
      tekst: "Hrimgar kaster sin kappe og hæver et sværd af blåt is. \"Så må du fryse som alle de andre!\"",
      kamp: { navn: "Frostjarlen Hrimgar", evne: 10, udholdenhed: 12 },
      valg: [{ tekst: "Se jarlen falde", til: 234 }],
    },

    234: {
      stemning: "is",
      tekst:
        "Hrimgars sværd splintres, og han falder på knæ. Uden for slottet lyder et brøl så højt, at isen i væggene revner. Hrimgar bliver hvid i ansigtet. \"Hun er her,\" hvisker han. \"Isvinge er kommet efter sit æg.\"",
      valg: [
        { tekst: "Løb efter ægget", til: 235, mangler: "Dragens æg" },
        { tekst: "Løb ud med ægget", til: 236, kraever: "Dragens æg" },
      ],
    },

    235: {
      stemning: "fare",
      tekst: "Du løber gennem de revnende gange, finder ægget i sin vugge og løfter det op. Bag dig styrter loftet sammen.",
      effekter: { giv: "Dragens æg" },
      valg: [{ tekst: "Løb ud", til: 236 }],
    },

    236: {
      stemning: "fare",
      tekst:
        "Slottet smuldrer omkring dig. Tårne af is styrter i grus, og du løber ud gennem porten med ægget i armene, mens slottet falder sammen bag dig i en sky af frostrøg.",
      valg: [{ tekst: "Se op mod himlen", til: 237 }],
    },

    237: {
      stemning: "fare",
      billede: "assets/art/egne/isvinge.jpg",
      billedtekst: "Isdragen Isvinge",
      tekst:
        "Isvinge lander foran dig, og jorden ryster. Hun er så stor som et kirketårn, med skæl af hvid krystal og vinger, der kaster skygge over hele dalen. Hendes øjne er dybe og blå som gletsjersprækker, og de er fulde af vrede.",
      valg: [
        { tekst: "Vis hende uglens fjer", til: 238, kraever: "Uglefjer" },
        { tekst: "Læg ægget foran hende og træd tilbage", til: 238 },
        { tekst: "Løb med ægget", til: 241 },
        { tekst: "Angrib dragen", til: 239 },
      ],
    },

    241: {
      stemning: "fare",
      tekst:
        "Du klemmer ægget ind til dig og løber ned ad skrænten. Bag dig lyder et brøl, og en kæmpe skygge glider hen over sneen. Isvinge letter fra jorden.",
      valg: [{ tekst: "Løb for livet mod klipperne", test: "held", til: 242, ellers: 243 }],
    },

    242: {
      stemning: "fare",
      tekst:
        "Du løber, men en skygge falder over dig, og en klo lander blidt i sneen foran dig og spærrer vejen. Isvinge bøjer hovedet ned mod dig. Først nu forstår du, at hun ikke vil skade ægget, og at hun ikke vil skade den, der bærer det.",
      valg: [{ tekst: "Giv hende ægget", til: 238 }],
    },

    243: {
      stemning: "død",
      tekst:
        "Du løber gennem sneen, men dragens ånde rammer dig som en vinterstorm. Du bliver stående midt i et skridt, frosset til en statue af is.\n\n" +
        "Isvinge tager sit æg og flyver mod nord. Vinteren bliver i Norden i hundrede år.",
      slut: "død",
      slutnavn: "Frosset til is",
    },

    239: {
      stemning: "fare",
      tekst: "Du hæver dit våben. Isvinge brøler, og sneen hvirvler op omkring jer.",
      kamp: { navn: "Isvinge", evne: 12, udholdenhed: 18 },
      valg: [{ tekst: "Se dragen falde", til: 240 }],
    },

    240: {
      stemning: "is",
      tekst:
        "Isvinge synker sammen i sneen. Hendes øjne finder ægget en sidste gang, og så lukker hun dem. Vinteren slutter, og foråret kommer til Norden.\n\n" +
        "Men da du går hjem med ægget i armene, føles sejren tom. Den sidste drage i verden er død, og det var ikke hende, der var skurken. I Vildmose fejrer de dig, men du ved, at du kunne have valgt anderledes.",
      slut: "sejr",
      slutnavn: "Dragedræberen",
    },

    238: {
      stemning: "sejr",
      tekst:
        "Isvinge bøjer sit enorme hoved og lægger snuden mod ægget. En dyb, blid lyd vibrerer i hendes bryst. Så ser hun på dig, og vreden i hendes øjne smelter som is i forårssol.\n\n" +
        "Omkring jer begynder sneen at tø. Det drypper fra istapperne, og i dalen bryder de første grønne strå frem gennem sneen. Isvinge sænker sin vinge mod jorden som en trappe.",
      effekter: { tag: ["Dragens æg", "Uglefjer"] },
      valg: [{ tekst: "Klatr op på dragens ryg", til: 244 }],
    },

    244: {
      stemning: "sejr",
      billede: "assets/art/egne/dragerytteren.jpg",
      billedtekst: "Hjem på dragens ryg",
      tekst:
        "Isvinge flyver sydpå med dig på ryggen og ægget i sine klør. Under jer smelter vinteren bort. Floderne bryder deres is, skovene bliver grønne, og fuglene vender hjem. Du ser Frostby, Jernbjerget, Saltvig og Ravnetårnet glide forbi dybt under jer.",
      valg: [{ tekst: "Land i Vildmose", til: 245 }],
    },

    245: {
      stemning: "landsby",
      tekst:
        "Isvinge lander på engen uden for Vildmose, og hele landsbyen løber ud for at se. Mellem dem står venner fra alle dine rejser, og den gamle kone fra kroen smiler, som om hun hele tiden vidste det.\n\n" +
        "Isvinge bøjer hovedet for dig. \"Når mit barn er klækket,\" siger hun med en stemme som vinterstorm og forårsregn, \"får det brug for en ven. Kom med os mod nord, hvis du vil. Eller bliv her, hvor du hører hjemme.\"",
      valg: [
        { tekst: "Bliv i Vildmose", til: 249 },
        { tekst: "Drag mod nord med Isvinge", til: 246 },
      ],
    },

    246: {
      stemning: "sejr",
      tekst:
        "Du siger farvel til Vildmose og klatrer op på dragens ryg igen. Hele landsbyen vinker, til I er en lille prik mod himlen.\n\n" +
        "I Nordfjeldene klækker ægget en forårsmorgen. Den lille drage er hvid som sne og har øjne som Månestenen, og den første, den ser, er dig.",
      valg: [{ tekst: "Se mod fremtiden", til: 250 }],
    },

    249: {
      stemning: "sejr",
      billede: "assets/art/egne/foraar-i-vildmose.jpg",
      billedtekst: "Foråret vender hjem",
      tekst:
        "Du bliver i Vildmose. Den sommer er den varmeste i mands minde. Månestenen lyser over landsbyen, havet synger i Saltvig, og hvert forår flyver en hvid drage forbi og vifter med vingerne.\n\n" +
        "Om aftenen sidder børnene om dig ved ilden og vil høre om ravnetårnet, skyggekongen, havheksen og isdragen. Og du fortæller, for det er de bedste historier, du kender.",
      slut: "sejr",
      slutnavn: "Hjemme i Vildmose",
    },

    250: {
      stemning: "sejr",
      billede: "assets/art/egne/dragerytteren.jpg",
      billedtekst: "Nye eventyr venter",
      tekst:
        "År senere flyver to drager over Norden, en stor og en lille, og på den lilles ryg sidder en rytter med en lysende sten om halsen.\n\n" +
        "I Vildmose fortæller de stadig om helten, der begyndte som en ganske almindelig landsbyboer og endte som dragernes ven. Og eventyret? Det er aldrig rigtigt slut.",
      slut: "sejr",
      slutnavn: "Dragernes ven",
    },
  },
};
