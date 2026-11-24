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

  intro:
    "I landsbyen Vildmose er Månestenen, den gamle amulet som holder ulvene borte fra markerne, blevet stjålet. Sporene fører mod Ravnetårnet, hvor troldmanden Morvak bor.\n\n" +
    "Du er landsbyens sidste håb. Slå dine evner med terningerne, og begynd så din rejse.",

  afsnit: {
    1: {
      stemning: "landsby",
      billede: "assets/art/egne/vildmose-landsby.jpg",
      billedtekst: "Landsbyen Vildmose i måneskin",
      tekst:
        "Landsbyens ældste trykker din hånd ved den sidste hytte. \"Kom tilbage med Månestenen,\" hvisker hun. \"Ellers kommer ulvene, når månen er fuld.\"\n\n" +
        "Foran dig deler vejen sig. Til venstre forsvinder en sti ind i den mørke Gråskov. Til højre fører en mudret vej ned mod floden Sølvå.",
      valg: [
        { tekst: "Tag stien gennem Gråskoven", til: 24 },
        { tekst: "Følg vejen ned til floden", til: 9 },
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
        "\"Jeg hedder Liriel,\" siger hun, mens hun gnider liv i sine arme. \"Jeg jagede Morvaks ravn, da edderkoppen tog mig. Tag min bue. Den rammer altid, hvad den sigtes efter, og du har mere brug for den end jeg lige nu.\"",
      effekter: { giv: "Elverbue", held: 2 },
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
        "Mens du spiser hendes suppe, fortæller hun, at hun hedder Marna, og at hendes mand byggede stenene til Ravnetårnet for mange år siden. \"Morvak betalte ham aldrig,\" siger hun bittert. \"Men han hørte, hvordan troldmanden styrer sin stengolem. Råber man »Sten, sov!«, så står den stille som en klippe.\"",
      effekter: { udholdenhed: 4, giv: "Ordet »Sten, sov«" },
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
        "Hun trækker et lille sølvspejl frem fra sin kjole. \"Jeg stjal det fra ham. Og der er en skjult trappe herfra, der fører lige op til hans kammer.\"",
      effekter: { giv: "Sølvspejl", held: 2 },
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
        "I et fuglebur i hjørnet sidder en lille grøn nisse med horn og hale. \"Pst! Du der!\" hvisker den. \"Luk mig ud, så skylder jeg dig en tjeneste. En nisse holder altid sit ord!\"",
      valg: [
        { tekst: "Åbn nissens bur", til: 48, mangler: "Nissens løfte" },
        { tekst: "Drik den røde eliksir", til: 49, mangler: "Tom eliksirflaske" },
        { tekst: "Gå ud ad døren til trappen", til: 53 },
      ],
    },

    48: {
      stemning: "taarn",
      tekst:
        "Nissen springer ud af buret og laver en kolbøtte i luften. \"Fri! Fri!\" Så bukker den dybt for dig.\n\n" +
        "\"Når du har brug for mig, så kald på Pip. Én gang, og kun én gang.\" Med et lille knald forsvinder den i en sky af grøn røg.",
      effekter: { giv: "Nissens løfte" },
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
        "Du løfter låget forsigtigt med spidsen af dit sværd. Klik! En lille nål skyder ud af låsen og ind i luften, hvor din hånd ville have været. I kisten ligger en pung med ædelstene.",
      effekter: { guld: 8, held: 1 },
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
        { tekst: "Kald på nissen Pip", til: 54, kraever: "Nissens løfte" },
        { tekst: "Snig dig hen og tag amuletten", til: 77 },
        { tekst: "Væk troldmanden og forhandl med ham", til: 95 },
        { tekst: "Angrib troldmanden, mens han sover", til: 90, mangler: "Runesværd" },
      ],
    },

    54: {
      stemning: "kammer",
      tekst:
        "\"Pip!\" hvisker du. Med et lille knald sidder nissen på din skulder. Den ser på den sovende troldmand og griner over hele ansigtet.\n\n" +
        "Pip lister hen over bordet, snupper Månestenen og binder i samme bevægelse Morvaks skæg fast til stolen. \"Så er vi kvit!\" fniser den, kaster amuletten til dig og forsvinder for altid.",
      effekter: { giv: "Månestenen", tag: "Nissens løfte" },
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
      fortsaet: { til: 101, tekst: "Fortsæt til kapitel 2: Skyggekongen" },
    },

    90: {
      stemning: "fare",
      tekst:
        "Du løfter dit sværd, men Morvaks øjne springer op, før du når at hugge. Han hvisker et enkelt ord, og din krop bliver tung som sten.\n\n" +
        "Fra nu af står du som en statue i hans kammer, endnu et trofæ blandt mange.",
      slut: "død",
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
      effekter: { udholdenhed: 30, held: 6 },
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
        { tekst: "Gå tilbage til heden", til: 102 },
      ],
    },

    105: {
      stemning: "skov",
      tekst:
        "Grimhild klatrer ned ad stigen med overraskende fart. \"Så den gamle kælling lever endnu,\" griner hun. \"Godt. Så skal du få hjælp.\"\n\n" +
        "Hun smører en salve på dine skrammer og stikker dig en lille pung. \"Sølvpulver. Kast det mod skyggerne, så brænder de som papir. Men der er kun til én gang.\"",
      effekter: { udholdenhed: 6, giv: "Sølvpulver" },
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
        "Fakkellyset jager de gule øjne på flugt. Det var bare grottenisser, og de hader ild. På væggen hænger en gammel stentavle med en indgraveret rune. Under den står der med dværgeskrift: Til venner af Jernbjerget.\n\n" +
        "Du tager tavlen med dig. Gangen fører opad og ud i lyset tæt ved en kæmpe port.",
      effekter: { giv: "Dværgerune" },
      valg: [{ tekst: "Gå hen til porten", til: 116 }],
    },

    117: {
      stemning: "fare",
      tekst: "I mørket kommer de krybende: en flok grottenisser med rustne knive og gule øjne. De fniser, mens de omringer dig.",
      kamp: [
        { navn: "Grottenisse", evne: 5, udholdenhed: 4 },
        { navn: "Grottenissernes høvding", evne: 7, udholdenhed: 6 },
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
      effekter: { loeft: { evne: 2 }, udholdenhed: 4, giv: "Dværgestålsværd" },
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
        "Sidedøren fører ind i et fangehul. Bag tremmerne sidder en snes fanger: bønder, købmænd og et par dværge. De ser på dig med store øjne. \"Hjælp os,\" hvisker en af dem. \"Så hjælper vi dig.\"",
      valg: [
        { tekst: "Lås cellerne op med den rustne nøgle", til: 135 },
        { tekst: "Skynd dig videre mod tronsalen", til: 136 },
      ],
    },

    135: {
      stemning: "skygge",
      tekst:
        "Nøglen passer i alle låse. Fangerne griber kæppe, kæder og hvad de ellers kan finde. \"Når du giver tegn,\" siger den største dværg, \"så stormer vi ind og holder hans skygger beskæftiget.\"",
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
    },

    150: {
      stemning: "sejr",
      billede: "assets/art/egne/lysets-sejr.jpg",
      billedtekst: "Lyset vender tilbage",
      tekst:
        "Vildmose tager imod dig med fakler, lygter og sang. Den ældste hænger Månestenen tilbage på pælen, og den lyser så klart, at selv skyggerne under sengene forsvinder.\n\n" +
        "Den nat danser hele landsbyen under stenens lys. Skyggekongen er væk, og Vildmose har en helt, som har reddet den to gange.",
      slut: "sejr",
    },
  },
};
