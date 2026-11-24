# Billed-prompts til Gemini

32 prompts – én til hver scene i spillet, i samme stil som Ravnetårnet (`assets/art/egne/ravnetaarnet.jpg`).

## Sådan gør du

1. Åbn **gemini.google.com** og start en ny chat.
2. **Upload Ravnetårnet-billedet** (`assets/art/egne/ravnetaarnet.jpg`) i den første besked og skriv:
   > *Use this image as the style reference for all the pictures I ask for in this chat: same oil-painting style, colors, light and level of detail. Don't copy its content.*
3. Kopiér så én prompt ad gangen (det engelske i kassen) og send den. Promptene er på engelsk, fordi billedgeneratorer forstår det bedst.
4. Er du tilfreds, så **download billedet** og gem det i mappen `assets/art/egne/` med præcis det **filnavn**, der står ved prompten (`.jpg` eller `.png` er begge fine).
5. Bliver et billede skævt (fx tekst i billedet eller forkert format), så skriv: *"Try again, wide 16:9, no text."*
6. Når du har gemt nogle billeder, så kør (fra projektmappen):

   ```bash
   python tools/art/brug_egne.py
   ```

   Scriptet finder dine billeder i `assets/art/egne/` og sætter dem ind i de rigtige afsnit. Du kan køre det så tit du vil – også når kun nogle af billederne er færdige.

**Stil-halen** er allerede med i hver prompt, så alle billeder passer sammen:
*Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, soft painterly clouds, atmospheric depth and mist, realistic evergreen trees. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.*

---

## Kapitel 1 – Ravnetårnets Hemmelighed

### 1. `vildmose-landsby.jpg` – afsnit 1
```
A small medieval village called Vildmose at dusk under a full moon: a handful of thatched-roof half-timbered cottages with warm glowing windows and chimney smoke, a muddy dirt road leading out of the village, a wooden fence, a dark forest on one side and a misty river valley on the other. An old village elder in a hooded cloak holds a lantern at the edge of the village. Cool blue moonlight mixed with warm window light. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, soft painterly clouds, atmospheric depth and mist, realistic evergreen trees. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 2. `den-sorte-gryde.jpg` – afsnit 41
```
Interior of a cozy medieval tavern called "The Black Cauldron": rough stone walls, heavy wooden ceiling beams, bundles of dried herbs hanging from the beams, a shelf of bottles, a big stone fireplace with a roaring fire and a black iron cauldron. At a wooden table a dark hooded stranger with glowing yellow eyes shakes a dice cup; an old woman in a shawl sits by the fire. Warm golden firelight and deep shadows. Detailed traditional oil painting, romantic fantasy style, rich textured brushwork, warm candlelit atmosphere. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 3. `graaskoven.jpg` – afsnit 24
```
A dense, ancient grey forest with tall mossy trees and shafts of soft light falling through the misty canopy. A narrow dirt path winds into the forest. Beside the path an old, very thin man with a white beard sits leaning against a huge oak tree, holding a walking stick. Quiet, mysterious mood with grey-green tones and golden light rays. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, atmospheric depth and mist, realistic trees. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 4. `stencirklen.jpg` – afsnit 30
```
A forest clearing with a circle of seven tall, mossy standing stones. In the middle stands a stone altar with an ancient sword stuck halfway into it; faint glowing blue runes run down the blade. Dark pine forest all around, low mist on the ground, a soft magical blue glow around the sword, late afternoon light. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, atmospheric depth and mist, realistic evergreen trees. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 5. `ulvene.jpg` – afsnit 52
```
Two lean, snarling grey wolves with bared teeth stepping out from a dark pine forest at dusk, facing the viewer across a small clearing with thorny brambles in the foreground. A thin crescent moon in a dusky red-purple sky, glowing eyes in the dark trees behind them. Tense, dangerous mood. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, atmospheric depth and mist, realistic evergreen trees. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 6. `soelvaa-faergen.jpg` – afsnit 9
```
A wide, fast-flowing silver river in a green valley with distant snow-capped mountains. A flat wooden ferry raft lies at the muddy riverbank; a tall hooded ferryman stands on it leaning on a long pole, with a small lantern hanging from a post. Reeds and cattails in the foreground, a pine forest on the far bank, soft clouds and calm reflective water. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, atmospheric depth and mist, realistic evergreen trees. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 7. `troldebroen.jpg` – afsnit 21
```
An old arched stone bridge over a rushing river in a mountain valley. A huge mossy river troll with grey stone-like skin, seaweed in its beard, small yellow eyes and a big wooden club is climbing up over the side of the bridge, blocking the way. Pine forest and distant mountains behind, dramatic afternoon light. Fairy-tale, slightly humorous but menacing. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, atmospheric depth and mist, realistic evergreen trees. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 8. `ravnesumpen.jpg` – afsnit 55
```
A misty swamp behind a dark stone tower: black still water, dead white birch trees standing like bones in the fog, reeds and moss. Small glowing blue will-o'-the-wisp lights dance over the water. The silhouette of the tower rises in the fog in the background. Eerie, quiet, cold blue-grey twilight. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, atmospheric depth and thick mist, reflective water. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 9. `kaelderen.jpg` – afsnit 68
```
A damp stone dungeon cellar under a tower. A single shaft of pale daylight falls from a barred grate high in the vaulted ceiling. A young woman in a simple dress sits chained to the wall in the light, looking up hopefully. Straw on the floor, water dripping, rats with small red eyes in the dark corners. Dark, moody, but with a ray of hope. Detailed traditional oil painting, fantasy style, rich textured brushwork, dramatic chiaroscuro lighting. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 10. `skeletvagten.jpg` – afsnit 66
```
A narrow stone spiral staircase inside a dark wizard's tower, lit by a single burning wall torch. A skeleton guard in rusty chainmail comes down the stairs holding a crooked knife, with faint red glowing eye sockets. Warm torchlight on old stone walls, deep shadows above. Spooky fairy-tale mood. Detailed traditional oil painting, fantasy style, rich textured brushwork, dramatic torchlight. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 11. `morvaks-kammer.jpg` – afsnit 29
```
A round wizard's chamber at the top of a tower: bookshelves packed with old books, glass bottles and strange instruments, a large round window showing the moon. An old sorcerer in a pointed hat and dark robes sleeps in a red armchair with his chin on his chest. On the table in front of him lies a glowing blue moonstone amulet. A black raven sits on top of a bookshelf. Candlelight and magical blue glow. Detailed traditional oil painting, fantasy style, rich textured brushwork, cozy but mysterious atmosphere. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 12. `hjemkomsten.jpg` – afsnit 98 og 100
```
Sunrise over a small medieval village with thatched cottages in a green valley with distant mountains. A young hero in a cloak, seen from behind, walks home along the road beside a young woman. In the village square a glowing blue moonstone amulet hangs again on a wooden post. Villagers come out to greet them. Golden sunrise light, pink and gold clouds, a feeling of joy and homecoming. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, soft painterly clouds, atmospheric depth. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 13. `alkymistvaerkstedet.jpg` – afsnit 46
```
A wizard's alchemy workshop inside a stone tower: bubbling glass flasks over small blue flames, copper tubes, shelves full of colorful potions, one bottle of glowing red potion with a label. A small green horned imp with big golden eyes and a long tail sits in a hanging birdcage, pleading. An arched window shows the night sky. Warm and magical light. Detailed traditional oil painting, fantasy style, rich textured brushwork, whimsical atmosphere. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 14. `marnas-hytte.jpg` – afsnit 19
```
Interior of a small fisherwoman's wooden hut by a river: fishing nets and dried fish hanging from the rafters, a stone hearth with a fire and a soup pot, a small window showing the river. A sturdy, kind-faced fisherwoman with a red headscarf, green dress and white apron stirs the pot with a ladle. A steaming bowl of soup on a rough wooden table. Warm, cozy firelight. Detailed traditional oil painting, fantasy style, rich textured brushwork. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 15. `ulvehulen.jpg` – afsnit 56
```
A wolves' den under the roots of a huge fallen tree in a forest. Inside the dim cave three small grey wolf cubs huddle together. Further back lie the remains of an unlucky traveler: an old chainmail shirt and a small leather pouch of coins. Daylight from the forest outside shines into the den, roots hang from the ceiling. Detailed traditional oil painting, romantic fantasy style, rich textured brushwork, atmospheric light. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 16. `ravnens-angreb.jpg` – afsnit 92
```
A giant black raven, as big as an eagle, with glowing red eyes and spread wings dives from a fiery sunset sky toward a young hero standing on a grassy hill. The hero raises a sword and holds a glowing blue amulet. In the distance a dark stone tower stands on a hill. Dramatic orange, pink and purple sunset, dynamic action. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, soft painterly clouds. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 17. `den-moerke-fremmede.jpg` – afsnit 42
```
Close-up in a dim tavern corner: a mysterious hooded stranger with glowing yellow eyes and a crooked smile sits at a wooden table. In front of him lies an unrolled hand-drawn parchment map of a tower, next to a dice cup and a tankard. A single candle lights the scene. Stone wall behind him. Secretive, mysterious mood. Detailed traditional oil painting, fantasy style, rich textured brushwork, candlelit chiaroscuro. Wide 16:9 format. The map has drawings only, no readable text, no letters, no frame, no border, no watermark.
```

### 18. `skattekammeret.jpg` – afsnit 87
```
A hidden vaulted treasure chamber inside a stone tower, lit by a wall torch. Piles of gold coins and gems on the floor, a round green dragon-hide shield hanging on the wall, crossed swords, and in the middle an old iron-bound wooden chest with its lid slightly open and golden light glowing from inside. Warm golden atmosphere. Detailed traditional oil painting, fantasy style, rich textured brushwork. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 19. `edderkoppekloeften.jpg` – afsnit 32
```
A narrow rocky ravine with steep cliff walls draped in thick grey spider webs. A giant spider, as big as a calf, with eight red eyes lowers itself on a silver thread from above. Behind it hangs a white silk cocoon that is moving – someone is trapped inside. Pale light from the sky far above, dark and dangerous mood. Detailed traditional oil painting, fantasy style, rich textured brushwork, atmospheric depth. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 33. `sumptrolden.jpg` – afsnit 63
```
A hero wades knee-deep through a dark, stinking swamp at twilight. Right in front of him a swamp troll rises out of the black water: a hulking lump of mud, tangled roots, dripping moss and rotting reeds shaped like a huge creature, with two small glowing yellow eyes and a wide mouth full of black teeth. Dead white birch trees stand in the fog around them, and the dark silhouette of a stone tower looms in the mist behind. Cold blue-grey light, ripples in the murky water, tense and dangerous fairy-tale mood. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, atmospheric depth and thick mist, reflective water. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

---

## Kapitel 2 – Skyggekongen

### 20. `maanesten-i-moerke.jpg` – afsnit 101
```
Night in a small medieval village with thatched cottages. On a wooden post in the village square hangs a moonstone amulet that has turned pitch black and gives off a dark red-purple aura. Thin, tall shadow creatures with long fingers and red eyes glide between the houses. Crows sit on the fences. Cold purple night sky with a thin moon. Ominous, eerie mood. Detailed traditional oil painting, dark fantasy landscape style, rich textured brushwork, atmospheric mist. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 21. `heden.jpg` – afsnit 102
```
A desolate grey moorland with purple heather under an overcast sky. An old wooden signpost with three arrow-shaped signs stands where the road splits in three; a crow sits on top. To the left rise snowy mountains, to the right the ruins of a ruined city in a cloud of dust, straight ahead a narrow path leads down into a misty bog. A dead tree with crows. Lonely, wide, adventurous mood. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, soft painterly clouds, atmospheric depth. Wide 16:9 landscape format. The signs are blank, no text, no letters, no frame, no border, no watermark.
```

### 22. `heksehytten.jpg` – afsnit 104
```
A crooked witch's hut on tall wooden stilts in the middle of a misty bog, with a sagging thatched roof, a smoking chimney and green light shining from the windows. A ladder leads up to the door, where a small hunched old witch in a pointed hat looks out. Below, a cauldron bubbles over a fire with green steam. Dead trees, reeds and still water with reflections. Mysterious but cozy fairy-tale mood. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, atmospheric mist. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 23. `bjergpasset.jpg` – afsnit 110
```
A high snowy mountain pass with towering snow-capped peaks. A narrow path runs along a cliff edge; a frozen icy waterfall glows pale blue against the rock, and the dark mouth of a cave opens further up. A small cloaked traveler walks along the path through falling snow. Cold blue and white light with a touch of warm sunlight on the peaks. Majestic and harsh. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, soft painterly clouds, atmospheric depth. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 24. `mineskakten.jpg` – afsnit 114
```
The entrance tunnel of an ancient dwarven mine, seen in deep perspective: old wooden support frames, iron rails leading into darkness, an abandoned ore cart full of rocks. A burning torch on the wall lights the foreground; deep in the darkness several pairs of small glowing yellow goblin eyes stare out. Mysterious and tense. Detailed traditional oil painting, fantasy style, rich textured brushwork, dramatic torchlight. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 25. `dvaergeporten.jpg` – afsnit 116
```
A gigantic dwarven gate carved into the rock face of a mountain: two huge wooden doors covered with glowing golden runes, framed by a carved stone arch. On each side stands a tall stone statue of a dwarf warrior with a horned helmet, long beard and battle axe. Stone steps lead up to the gate. Majestic, ancient atmosphere with warm golden glow on cold stone. Detailed traditional oil painting, fantasy style, rich textured brushwork. Wide 16:9 format. The runes are decorative symbols only, no readable text, no letters, no frame, no border, no watermark.
```

### 26. `dvaergesmedjen.jpg` – afsnit 118
```
A great dwarven forge deep inside a mountain: a huge stone furnace with roaring orange fire, an anvil with glowing hot metal, tools and chains on the stone walls. An old dwarf smith with a long white braided beard, leather apron and helmet swings a heavy hammer; sparks fly everywhere. Intense warm orange firelight and deep shadows. Detailed traditional oil painting, fantasy style, rich textured brushwork, dramatic lighting. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 27. `askeborg.jpg` – afsnit 120
```
The ruins of a once proud city, now covered in grey ash: broken stone houses, collapsed arches and crumbling towers. Thin dark shadow figures glide silently between the ruins. In the background on a hill stands a black castle with sharp spires and purple light in its windows. Crows on the ruins, a hazy grey-purple sky. Melancholic and ominous. Detailed traditional oil painting, dark fantasy landscape style, rich textured brushwork, atmospheric depth and dust haze. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 28. `kloakken.jpg` – afsnit 125
```
A dark vaulted brick sewer tunnel under a ruined city, with murky green water flowing through it and stone walkways along the sides. A giant segmented grey worm with a round mouth full of teeth rises out of the water. Rats on the ledges, a pale beam of light from a grate above. Disgusting but exciting fantasy mood. Detailed traditional oil painting, fantasy style, rich textured brushwork, dramatic lighting. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 29. `spoegelsespigen.jpg` – afsnit 128
```
A ruined cobblestone street between broken stone houses covered in ash. A translucent ghost girl with a small golden crown, glowing softly pale blue, stands in the middle of the street and holds a small lantern with warm light, gently guiding the way. Sad, gentle and magical mood, grey-blue haze. Detailed traditional oil painting, fantasy style, rich textured brushwork, atmospheric mist. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 30. `skyggeborgen.jpg` – afsnit 130
```
A towering black castle with sharp spear-like spires on a cliff, purple light glowing from its narrow windows. The sky above swirls in a slow purple vortex as if the castle pulls in all the light. A long stone stairway leads up to the gate across a chasm; a tiny cloaked hero stands at the foot of the stairs. Ravens circle the towers. Epic, dark fantasy. Detailed traditional oil painting, dark fantasy landscape style, rich textured brushwork, dramatic clouds. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```

### 31. `tronsalen.jpg` – afsnit 136
```
An enormous dark throne room with tall stone pillars disappearing into darkness and a red carpet leading to a black stone throne. On the throne sits the Shadow King: tall and thin, dark robes, a crown made of living shadow, glowing pale violet eyes. Behind the throne pulses a large purple crystal like a heart. Shadow creatures rise along the walls. Ominous final-boss atmosphere with purple light. Detailed traditional oil painting, dark fantasy style, rich textured brushwork, dramatic lighting. Wide 16:9 format. No text, no letters, no frame, no border, no watermark.
```

### 32. `lysets-sejr.jpg` – afsnit 149 og 150
```
A joyful night festival in a small medieval village with thatched cottages: a moonstone amulet on a wooden post in the village square shines brilliant silver-blue light in rays across the whole sky. Villagers dance with raised arms, strings of warm lanterns hang between the houses, a full moon and stars above, mountains in the background. Magical, happy, triumphant mood. Detailed traditional oil painting, romantic fantasy landscape style, rich textured brushwork, soft painterly clouds, atmospheric depth. Wide 16:9 landscape format. No text, no letters, no frame, no border, no watermark.
```
