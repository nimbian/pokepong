ROUTES = {}
TRAINERS = {}
MAPLIST = [[273,662],[273,613],[273,500],[273,390],
           [273,277],[329,277],[273,215],
           [385,215],[497,160],[600,160],
           [721,160],[721,109],[775,60],
           [721,221],[721,499],[721,550],
           [600,600],[889,160],[945,215],
           [945,277],[1010,325],[889,326],[610,326],
           [550,326],[721,326],[832,550],
           [945,550],[900,670],[775,710],
           [721,774],[439,326],[385,499],
           [497,774],[609,774],[609,726],
           [609,726],[609,726],[609,726],
           [525,886],[440,886],[385,886],
           [273,886],[273,886],
           [273,886],[273,886],[273,886],
           [273,780],[160,500],[160,375],
           [160,275],[160,275],[160,275],
           [160,275],[160,160],[160,160],
           [160,160],[160,160],[1010,277],
           [675,109],[675,109],[675,109]]
MAPROUTE = ['PALLET TOWN', 'ROUTE 1', 'VIRIDIAN CITY', 'ROUTE 2',
            'VIRIDIAN FOREST', "DIGLETT's CAVE", 'PEWTER CITY',
            'ROUTE 3', 'MT.MOON', 'ROUTE 4',
            'CERULEAN CITY', 'ROUTE 24', 'ROUTE 25',
            'ROUTE 5', 'ROUTE 6', 'VERMILION CITY',
            'S.S.ANNE', 'ROUTE 9', 'ROCK TUNNEL',
            'ROUTE 10', 'POKE~MON TOWER', 'ROUTE 8', 'ROUTE 7',
            'CELADON CITY', 'SAFFRON CITY', 'ROUTE 11',
            'ROUTE 12', 'ROUTE 13', 'ROUTE 14',
            'ROUTE 15', 'ROUTE 16', 'ROUTE 17',
            'ROUTE 18', 'FUCHSIA CITY', 'SAFARI ZONE MAIN AREA',
            'SAFARI ZONE AREA 1','SAFARI ZONE AREA 2', 'SAFARI ZONE AREA 3',
            'SEA ROUTE 19', 'SEAFOAM ISLANDS', 'SEA ROUTE 20',
            'CINNABAR ISLAND', 'POK~MON MAN. TRAINERS',
            'POK~MON MAN. FLOOR 1', 'POK~MON MAN. FLOOR 2', 'POK~MON MAN. FLOOR 3',
            'SEA ROUTE 21', 'ROUTE 22', 'ROUTE 23',
            'VICTORY ROAD TRAINERS', 'VICTORY ROAD FLOOR 1','VICTORY ROAD FLOOR 2',
            'VICTORY ROAD FLOOR 3', 'ELITE 4-1','ELITE 4-2',
            'ELITE 4-3','ELITE 4-4', 'POWER PLANT',
            'UNKNOWN DUNGEON FLOOR 2', 'UNKNOWN DUNGEON FLOOR 1', 'UNKNOWN DUNGEON BASEMENT 1']

#TODO route 12,13,14,15

#TODO route 22, POKEMON TOWER

#TODO Mr.Mime trade on rt 2
#TODO Jynx trade in Cerulean
#TODO fishing?
ROUTES['ROUTE 1'] = {
	'Pidgey': [[2,5], .55],
	'Rattata': [[2,4], .45]
}
ROUTES['ROUTE 2'] = {
	'Pidgey': [[3,5],.35],
	'Rattata': [[2,5],.35],
	'Caterpie': [[3,5],.15],
	'Weedle': [[3,5],.15]
}
ROUTES['ROUTE 22'] = {
	'Rattata': [[2,4],.4],
	'Spearow': [[3,5],.1],
	'Nidoran+': [[3,4],.25],
	'Nidoran=': [[3,4],.25]
}
ROUTES['VIRIDIAN FOREST'] = {
	'Caterpie': [[3,5],.35],
	'Metapod': [[4,6],.1],
	'Weedle': [[3,5],.35],
	'Kakuna': [[4,6],.1],
	'Pikachu': [[3,5],.1]
}
#TODO pewter break need badge to move on
ROUTES['ROUTE 3'] = {
	'Pidgey': [[6,8],.5],
	'Spearow': [[5,8],.4],
	'Jigglypuff': [[3,7],.1]
}

ROUTES['MT.MOON'] = {
	'Zubat': [[6,8],.5],
	'Geodude': [[8,10],.25],
	'Paras': [[10,12],.15],
	'Clefairy': [[10,12],.1]
}

ROUTES['ROUTE 4'] = {
	'Rattata': [[8,12],.3],
	'Spearow': [[8,12],.3],
	'Ekans': [[6,12],.2],
	'Sandshrew': [[6,12],.2],
}

ROUTES['ROUTE 24'] = {
	'Bellsprout': [[12,14],.2],
	'Oddish': [[12,14],.2],
	'Abra': [[8,12],.15],
	'Pidgey': [[12,13],.15],
	'Weedle': [[8,8],.15],
	'Caterpie': [[8,8],.15]
}
ROUTES['ROUTE 25'] = {
	'Bellsprout': [[12,14],.2],
	'Oddish': [[12,14],.2],
	'Abra': [[8,12],.15],
	'Pidgey': [[12,13],.15],
	'Weedle': [[8,8],.15],
	'Caterpie': [[8,8],.15]
}
ROUTES['ROUTE 5'] = {
	'Oddish': [[13,16],.25],
	'Bellsprout': [[13,16],.25],
	'Meowth': [[10,16],.2],
	'Mankey': [[10,16],.2],
	'Pidgey': [[13,16],.1]
}
ROUTES['ROUTE 6'] = {
	'Oddish': [[13,16],.25],
	'Bellsprout': [[13,16],.25],
	'Meowth': [[10,16],.2],
	'Mankey': [[10,16],.2],
	'Pidgey': [[13,16],.1]
}
#TODO SS.ANNE TRAINERS?
#TODO CERULEAN BREAK for cut
ROUTES['ROUTE 11'] = {
	'Spearow': [[13,17],.2],
	'Ekans': [[12,15],.3],
	'Sandshrew': [[12,15],.3],
	'Drowzee': [[15,19],.2]
}
ROUTES["DIGLETT's CAVE"] = {
	'Diglett': [[15,22],.95],
	'Dugtrio': [[29,31],.05]
}
ROUTES['ROUTE 9'] = {
	'Spearow': [[13,17],.2],
	'Ekans': [[11,17],.2],
	'Sandshrew': [[11,17],.2]
}
ROUTES['ROUTE 10'] = {
	'Spearow': [[13,17],.2],
	'Ekans': [[11,17],.2],
	'Sandshrew': [[11,17],.2],
	'Voltorb': [[14,17],.4]
}
ROUTES['ROCK TUNNEL'] = {
	'Zubat': [[15,16],.4],
	'Geodude': [[15,17],.25],
	'Machop': [[16,17],.2],
	'Onix': [[13,17],.15]
}
ROUTES['ROUTE 8'] = {
	'Pidgey': [[18,20],.06],
	'Ekans': [[17,19],.12],
	'Sandshrew': [[17,19],.12],
	'Meowth': [[18,20],.2],
	'Mankey': [[18,20],.2],
	'Growlithe': [[16,18],.15],
	'Vulpix': [[16,18],.15]
}
ROUTES['ROUTE 7'] = {
	'Pidgey': [[19,22],.06],
	'Bellsprout': [[19,22],.12],
	'Oddish': [[19,22],.12],
	'Meowth': [[17,20],.2],
	'Mankey': [[17,20],.2],
	'Growlithe': [[18,20],.15],
	'Vulpix': [[18,20],.15]
}
#TODO celadon eevee/porygon/dratini
#TODO celadon badge break
ROUTES['POKE~MON TOWER'] = {
	'Gastly': [[13,19],.8],
	'Haunter': [[20,25],.1],
	'Cubone': [[15,19],.1]
}

#TODO saffron city hitmonlee/chan?
#TODO Silphco Lapras
ROUTES['ROUTE 16'] = {
	'Rattata': [[18,22],.3],
	'Raticate': [[23,25],.05],
	'Spearow': [[20,22],.4],
	'Doduo': [[18,22],.25],
	'Snorlax': [[30,30],.05]
}
#TODO saffron badge break

ROUTES['ROUTE 17'] = {
	'Raticate': [[25,29],.3],
	'Spearow': [[20,22],.4],
	'Doduo': [[24,28],.25],
	'Fearow': [[25,27],.05]
}
ROUTES['ROUTE 18'] = {
	'Raticate': [[25,29],.2],
	'Spearow': [[20,22],.4],
	'Doduo': [[24,28],.25],
	'Fearow': [[25,29],.15]
}
ROUTES['SAFARI ZONE MAIN AREA'] = {
	'Nidoran=': [[22,22],.15],
	'Nidoran+': [[22,22],.15],
	'Nidorina': [[31,31],.04],
	'Nidorino': [[31,31],.04],
	'Exeggcute': [[24,25],.15],
	'Parasect': [[30,30],.05],
	'Venonat': [[22,22],.15],
	'Rhyhorn': [[25,25],.15],
	'Chansey': [[23,23],.02],
	'Scyther': [[23,23],.05],
	'Pinsir': [[23,23],.05],
}
ROUTES['SAFARI ZONE AREA 1'] = {
	'Nidoran=': [[24,24],.12],
	'Nidoran+': [[24,24],.12],
	'Nidorina': [[33,33],.08],
	'Nidorino': [[33,33],.08],
	'Exeggcute': [[23,25],.15],
	'Paras': [[22,22],.13],
	'Parasect': [[25,25],.05],
	'Doduo': [[26,26],.15],
	'Kangaskhan': [[25,25],.06],
	'Scyther': [[28,28],.03],
	'Pinsir': [[28,28],.03],
}
ROUTES['SAFARI ZONE AREA 2'] = {
	'Nidoran=': [[22,22],.12],
	'Nidoran+': [[22,22],.12],
	'Nidorina': [[30,30],.08],
	'Nidorino': [[30,30],.08],
	'Venomoth': [[32,32],.05],
	'Paras': [[23,23],.15],
	'Exeggcute': [[25,27],.15],
	'Rhyhorn': [[26,26],.15],
	'Chansey': [[26,26],.07],
	'Tauros': [[28,28],.03]
}
ROUTES['SAFARI ZONE AREA 3'] = {
	'Nidoran=': [[25,25],.12],
	'Nidoran+': [[25,25],.12],
	'Nidorina': [[33,33],.05],
	'Nidorino': [[33,33],.05],
	'Venonat': [[23,23],.15],
	'Doduo': [[26,26],.15],
	'Venomoth': [[31,31],.05],
	'Exeggcute': [[24,26],.19],
	'Tauros': [[26,26],.08],
	'Kangaskhan': [[28,28],.04]
}

ROUTES['ROUTE 12'] = {
	'Pidgey': [[23,27],.3],
	'Venonat': [[24,26],.2],
	'Bellsprout': [[22,26],.2],
	'Weepinbell': [[28,30],.05],
	'Oddish': [[22,26],.2],
	'Gloom': [[28,30],.05]
}

ROUTES['ROUTE 13'] = {
	'Pidgey': [[23,27],.25],
	'Venonat': [[24,26],.2],
	'Bellsprout': [[22,26],.2],
	'Weepinbell': [[28,30],.05],
	'Oddish': [[22,26],.2],
	'Gloom': [[28,30],.05],
	'Ditto': [[25,25],.05]
}

ROUTES['ROUTE 14'] = {
	'Pidgey': [[26,26],.15],
	'Pidgeotto': [[28,30],.05],
	'Venonat': [[24,26],.15],
	'Bellsprout': [[22,26],.2],
	'Weepinbell': [[30,30],.05],
	'Oddish': [[22,26],.2],
	'Gloom': [[30,30],.05],
	'Ditto': [[23,23],.15]
}

ROUTES['ROUTE 15'] = {
	'Pidgey': [[23,23],.15],
	'Pidgeotto': [[28,30],.05],
	'Venonat': [[26,28],.15],
	'Bellsprout': [[22,26],.2],
	'Weepinbell': [[30,30],.05],
	'Oddish': [[22,26],.2],
	'Gloom': [[30,30],.05],
	'Ditto': [[26,26],.15]
}

ROUTES['S.S. ANNE TRUCK'] = {
        'Mew': [[5,5],1]
}

ROUTES['SEA ROUTE 21'] = {
              'Rattata': [[21,23],.35],
              'Rattata': [[21,23],.35],
              'Raticate':[[30,30],.15],
              'Pidgey':[[21,23],.25],
              'Pidgeotto':[[30,32],.15],
              'Tangela':[[28,32],.10]
}

ROUTES['POK~MON MAN. FLOOR 1'] = {
              'Koffing':[[30,32],.2],
              'Weezing':[[37,39],.02],
              'Grimer':[[30,32],.2],
              'Muk':[[37,39],.02],
              'Vulpix':[[34,34],.1],
              'Growlithe':[[34,34],.1],
              'Ponyta':[[28,34],.36]

}

ROUTES['POK~MON MAN. FLOOR 2'] = {
              'Koffing':[[30,34],.2],
              'Weezing':[[37,39],.02],
              'Grimer':[[30,34],.2],
              'Muk':[[37,39],.02],
              'Vulpix':[[32,32],.1],
              'Growlithe':[[32,32],.1],
              'Ponyta':[[28,32],.36]
}

ROUTES['POK~MON MAN. FLOOR 3'] = {
              'Koffing':[[31,35],.2],
              'Weezing':[[38,42],.02],
              'Grimer':[[31,35],.2],
              'Muk':[[38,42],.02],
              'Vulpix':[[33,33],.1],
              'Growlithe':[[33,33],.1],
              'Ponyta':[[32,36],.26],
              'Magmar':[[34,34],.1]
}

ROUTES['POK~MON MAN. BASEMENT 1'] = {
              'Koffing':[[31,35],.2],
              'Weezing':[[40,42],.02],
              'Grimer':[[31,35],.2],
              'Muk':[[40,42],.02],
              'Vulpix':[[35,35],.1],
              'Growlithe':[[35,35],.1],
              'Ponyta':[[32,34],.3],
              'Magmar':[[38,38],.4]
}

ROUTES['POWER PLANT'] = {
               'Magnemite':[[21,23],.25],
               'Magneton':[[32,35],.09],
               'Pikachu':[[20,24],.25],
               'Raichu':[[33,36],.05],
               'Voltorb':[[21,23],.30],
               'Electabuzz':[[33,36],.05],
           'Zapdos':[[50,50],.01]
}

ROUTES['SEA ROUTE 19'] = {
              'Tentacool':[[5,40],1]
}

ROUTES['SEA ROUTE 20'] = {
              'Tentacool':[[5,40],1]
}

ROUTES['SEAFOAM ISLANDS FLOOR 1'] = {
               'Zubat':[[21,21],.10],
               'Golbat':[[29,29],.05],
               'Psyduck':[[28,30],.05],
               'Golduck':[[38,38],.01],
               'Slowpoke':[[28,30],.1],
               'Slowbro':[[38,38],.01],
               'Seel':[[30,30],.20],
               'Shellder':[[28,30],.12],
               'Krabby':[[28,30],.12],
               'Horsea':[[28,30],.12],
               'Staryu':[[28,30],.12]
}

ROUTES['SEAFOAM ISLANDS BASEMENT 1'] = {
               'Psyduck':[[28,30],.1],
               'Slowpoke':[[28,30],.1],
               'Seel':[[28,30],.10],
               'Dewgong':[[38,38],.03],
               'Shellder':[[32,32],.2],
               'Krabby':[[30,32],.15],
               'Kingler':[[37,37],.01],
               'Horsea':[[30,32],.15],
               'Seadra':[[37,37],.01],
               'Staryu':[[30,30],.15],
}

ROUTES['SEAFOAM ISLANDS BASEMENT 2'] = {
               'Golbat':[[30,30],.04],
               'Psyduck':[[30,32],.2],
               'Golduck':[[37,37],.01],
               'Slowpoke':[[30,32],.2],
               'Slowbro':[[37,37],.01],
               'Seel':[[30,32],.20],
               'Shellder':[[28,30],.07],
               'Krabby':[[28,30],.1],
               'Horsea':[[28,30],.1],
               'Staryu':[[28,30],.07]
}

ROUTES['SEAFOAM ISLANDS BASEMENT 3'] = {
               'Psyduck':[[31,33],.2],
               'Slowpoke':[[31,33],.2],
               'Seel':[[31,33],.11],
               'Dewgong':[[37,37],.01],
               'Shellder':[[29,31],.1],
               'Krabby':[[29,31],.1],
               'Kingler':[[39,39],.04],
               'Horsea':[[29,31],.1],
               'Seadra':[[39,39],.04],
               'Staryu':[[29,31],.1]
}

ROUTES['SEAFOAM ISLANDS BASEMENT 4'] = {
               'Golbat':[[32,32],.01],
               'Psyduck':[[29,31],.1],
               'Golduck':[[39,39],.04],
               'Slowpoke':[[29,31],.1],
               'Slowbro':[[39,39],.04],
               'Seel':[[29,31],.1],
               'Shellder':[[31,33],.13],
               'Krabby':[[31,33],.17],
               'Horsea':[[31,33],.17],
               'Staryu':[[31,33],.13],
           'Articuno':[[50,50],.01]
}

ROUTES['ROUTE 23'] = {
               'Spearow':[[26,26],.1],
               'Fearow':[[38,43],.2],
               'Ekans':[[26,26],.18],
               'Arbok':[[41,41],.02],
               'Sandshrew':[[26,26],.18],
               'Sandslash':[[41,41],.02],
               'Ditto':[[33,43],.30]
}

ROUTES['VICTORY ROAD FLOOR 1'] = {
               'Zubat':[[22,22],.15],
               'Golbat':[[41,41],.05],
               'Geodude':[[26,26],.15],
               'Graveler':[[42,42],.01],
               'Machop':[[24,24],.25],
               'Machoke':[[42,42],.05],
               'Onix':[[36,42],.30],
               'Marowak':[[43,43],.04]
}

ROUTES['VICTORY ROAD FLOOR 2'] = {
               'Zubat':[[26,26],.14],
               'Golbat':[[40,40],.05],
               'Geodude':[[24,24],.15],
               'Graveler':[[43,43],.05],
               'Machop':[[22,22],.25],
               'Machoke':[[41,41],.05],
               'Onix':[[36,42],.20],
               'Marowak':[[40,40],.05],
               'Moltres':[[50,50],.01]
}

ROUTES['VICTORY ROAD FLOOR 3'] = {
               'Zubat':[[22,22],.15],
               'Golbat':[[41,41],.05],
               'Geodude':[[26,26],.15],
               'Graveler':[[43,43],.05],
               'Machop':[[24,24],.25],
               'Machoke':[[42,45],.04],
               'Onix':[[42,45],.30],
               'Venomoth':[[40,40],.10]
}

ROUTES['UNKNOWN DUNGEON FLOOR 2'] = {
               'Venomoth':[[51,51],.15],
               'Dodrio':[[51,51],.25],
               'Kadabra':[[51,51],.15],
               'Electrode':[[52,52],.10],
               'Marowak':[[52,52],.10],
               'Rhydon':[[52,52],.10],
               'Wigglytuff':[[54,54],.05],
               'Chansey':[[56,56],.05],
               'Ditto':[[55,60],.05]
}

ROUTES['UNKNOWN DUNGEON FLOOR 1'] = {
               'Golbat':[[46,46],.25],
               'Hypno':[[46,46],.15],
               'Magneton':[[46,46],.15],
               'Sandslash':[[52,52],.05],
               'Parasect':[[52,52],.05],
               'Raichu':[[53,53],.04],
               'Arbok':[[52,52],.05],
               'Venomoth':[[49,49],.10],
               'Dodrio':[[49,49],.10],
               'Kadabra':[[49,49],.05],
               'Ditto':[[53,53],.01]
}

ROUTES['UNKNOWN DUNGEON BASEMENT 1'] = {

               'Marowak':[[55,55],.15],
               'Rhydon':[[55,55],.25],
               'Electrode':[[55,55],.15],
               'Sandslash':[[57,57],.03],
               'Parasect':[[64,64],.09],
               'Raichu':[[64,64],.10],
               'Arbok':[[57,57],.03],
               'Chansey':[[64,64],.10],
               'Ditto':[[63,67],.10],
               'Mewtwo':[[70,70],.01]

}

TRAINERS['SAFFRON CITY'] = [['Blackbelt', 900, [['Primeape', 36],
                                                ['Primeape', 36]]],
                            ['Blackbelt', 775, [['Mankey', 31],
                                                ['Mankey', 31],
                                                ['Primeape', 31]]],
                            ['Blackbelt', 925, [['Hitmonlee', 37],
                                                ['Hitmonchan', 37]]],
                            ['Blackbelt', 775, [['Machop', 31],
                                                ['Mankey', 31],
                                                ['Primeape', 31]]],
                            ['Blackbelt', 775, [['Machop', 31],
                                                ['Mankey', 31],
                                                ['Primeape', 31]]]]
TRAINERS['SEA ROUTE 19'] = [['Swimmer', 145, [['Goldeen', 29],
                                          ['Horsea', 29],
                                          ['Staryu', 29]]],
                        ['Swimmer', 150, [['Tentacool', 30],
                                          ['Shellder', 30]]],
                        ['Swimmer', 150, [['Horsea', 30],
                                          ['Horsea', 30]]],
                        ['Swimmer', 150, [['Poliwag', 30],
                                          ['Poliwhirl', 30]]],
                        ['Swimmer', 135, [['Horsea', 27],
                                          ['Tentacool', 27],
                                          ['Tentacool', 27],
                                          ['Goldeen', 27]]],
                        ['Swimmer', 145, [['Goldeen', 29],
                                          ['Shellder', 29],
                                          ['Seaking', 29]]],
                        ['Beauty', 2100, [['Goldeen', 30],
                                          ['Seaking', 30]]],
                        ['Beauty', 2030, [['Staryu', 29],
                                          ['Staryu', 29],
                                          ['Staryu', 29]]],
                        ['Swimmer', 135, [['Tentacool', 27],
                                          ['Tentacool', 27],
                                          ['Staryu', 27],
                                          ['Horsea', 27],
                                          ['Tentacruel', 27]]],
                        ['Swimmer', 135, [['Tentacool', 27],
                                         ['Tentacool', 27],
                                         ['Staryu', 27],
                                         ['Horsea', 27],
                                         ['Tentacruel', 27]]]]
TRAINERS['ROUTE 3'] = [['Lass', 135, [['Pidgey', 9],
                                         ['Pidgey', 9]]],
                       ['Bug Catcher', 100, [['Caterpie', 10],
                                         ['Weedle', 10],
                                         ['Caterpie', 10]]],
                       ['Youngster', 165, [['Rattata', 11],
                                         ['Ekans', 11]]],
                       ['Bug Catcher', 90, [['Weedle', 9],
                                         ['Kakuna', 9],
                                         ['Caterpie', 9],
                                         ['Metapod', 9]]],
                       ['Lass', 150, [['Rattata', 10],
                                         ['Nidoran=', 10]]],
                       ['Youngster', 210, [['Spearow', 14],
                                         ['Spearow', 14]]],
                       ['Bug Catcher', 110, [['Caterpie', 11],
                                         ['Metapod', 11]]],
                       ['Bug Catcher', 110, [['Caterpie', 11],
                                         ['Metapod', 11]]]]
TRAINERS['POKEMON TOWER'] = [['Channeler', 660, [['Gastly', 23],
                                         ['Gastly', 23]]],
                       ['Channeler', 660, [['Gastly', 22],
                                         ['Gastly', 22]]],
                       ['Channeler', 720, [['Gastly', 24],
                                         ['Gastly', 24]]],
                       ['Channeler', 690, [['Gastly', 23],
                                         ['Gastly', 23]]],
                       ['Channeler', 660, [['Gastly', 22],
                                         ['Gastly', 22]]],
                       ['Channeler', 720, [['Gastly', 24],
                                         ['Gastly', 24]]],
                       ['Channeler', 660, [['Gastly', 22],
                                         ['Gastly', 22]]],
                       ['Channeler', 720, [['Gastly', 24],
                                         ['Gastly', 24]]],
                       ['Channeler', 660, [['Haunter', 22],
                                         ['Haunter', 22]]],
                       ['Channeler', 690, [['Haunter', 23],
                                         ['Haunter', 23]]],
                       ['Channeler', 660, [['Gastly', 22],
                                         ['Gastly', 22],
                                         ['Gastly', 22]]],
                       ['Channeler', 720, [['Gastly', 24],
                                         ['Gastly', 24]]],
                       ['Channeler', 720, [['Gastly', 24],
                                         ['Gastly', 24]]],
                       ['Rocket', 750, [['Zubat', 25],
                                         ['Zubat', 25],
                                         ['Golbat', 25]]],
                       ['Rocket', 780, [['Koffing', 26],
                                         ['Drowzee', 26]]],
                       ['Rocket', 780, [['Koffing', 26],
                                         ['Drowzee', 26]]]]
TRAINERS['ROUTE 6'] = [['Bug Catcher', 160, [['Weedle', 16],
                                         ['Caterpie', 16],
                                         ['Weedle', 16]]],
                       ['Jr. Trainer =', 320, [['Squirtle', 20],
                                         ['Squirtle', 20]]],
                       ['Jr. Trainer +', 400, [['Rattata', 16],
                                         ['Pikachu', 16]]],
                       ['Bug Catcher', 200, [['Butterfree', 20],
                                         ['Butterfree', 20]]],
                       ['Jr. Trainer +', 320, [['Pidgey', 16],
                                         ['Pidgey', 16],
                                         ['Pidgey', 16]]],
                       ['Jr. Trainer +', 320, [['Pidgey', 16],
                                         ['Pidgey', 16],
                                         ['Pidgey', 16]]]]
TRAINERS['ROUTE 8'] = [['Lass', 330, [['Clefairy', 22],
                                         ['Clefairy', 22]]],
                       ['Gambler', 1680, [['Growlithe', 24],
                                         ['Vulpix', 24]]],
                       ['Super Nerd', 550, [['Grimer', 22],
                                         ['Muk', 22],
                                         ['Grimer', 22]]],
                       ['Lass', 345, [['Nidoran+', 23],
                                         ['Nidorina', 23]]],
                       ['Super Nerd', 650, [['Koffing', 26],
                                         ['Koffing', 26]]],
                       ['Lass', 360, [['Meowth', 24],
                                         ['Meowth', 24],
                                         ['Meowth', 24]]],
                       ['Lass', 285, [['Pidgey', 19],
                                         ['Rattata', 19],
                                         ['Nidoran=', 19],
                                         ['Meowth', 19],
                                         ['Pikachu', 19]]],
                       ['Gambler', 1540, [['Poliwag', 22],
                                         ['Poliwag', 22],
                                         ['Poliwhirl', 22]]],
                       ['Gambler', 1540, [['Poliwag', 22],
                                         ['Poliwag', 22],
                                         ['Poliwhirl', 22]]]]
TRAINERS['ROUTE 9'] = [['Jr. Trainer +', 360, [['Oddish', 18],
                                         ['Bellsprout', 18],
                                         ['Oddish', 18],
                                         ['Bellsprout', 18]]],
                       ['Hiker', 700, [['Machop', 20],
                                         ['Onix', 20]]],
                       ['Jr. Trainer =', 420, [['Growlithe', 21],
                                         ['Charmander', 21]]],
                       ['Bug Catcher', 190, [['Beedrill', 19],
                                         ['Beedrill', 19]]],
                       ['Bug Catcher', 200, [['Caterpie', 20],
                                         ['Weedle', 20],
                                         ['Venonat', 20]]],
                       ['Jr. Trainer =', 380, [['Rattata', 19],
                                         ['Diglett', 19],
                                         ['Ekans', 19],
                                         ['Sandshrew', 19]]],
                       ['Hiker', 735, [['Geodude', 21],
                                         ['Onix', 21]]],
                       ['Hiker', 700, [['Geodude', 20],
                                         ['Machop', 20],
                                         ['Geodude', 20]]],
                       ['Hiker', 700, [['Geodude', 20],
                                         ['Machop', 20],
                                         ['Geodude', 20]]]]
TRAINERS['ROCKET HIDEOUT'] = [['Rocket', 630, [['Drowzee', 21],
                                         ['Machop', 21]]],
                       ['Rocket', 630, [['Raticate', 21],
                                         ['Raticate', 21]]],
                       ['Rocket', 600, [['Grimer', 20],
                                         ['Koffing', 20],
                                         ['Koffing', 20]]],
                       ['Rocket', 570, [['Rattata', 19],
                                         ['Raticate', 19],
                                         ['Raticate', 19],
                                         ['Rattata', 19]]],
                       ['Rocket', 660, [['Grimer', 22],
                                         ['Koffing', 22]]],
                       ['Rocket', 630, [['Raticate', 20],
                                         ['Zubat', 20]]],
                       ['Rocket', 510, [['Zubat', 17],
                                         ['Koffing', 17],
                                         ['Grimer', 17],
                                         ['Zubat', 17],
                                         ['Raticate', 17]]],
                       ['Rocket', 630, [['Machop', 21],
                                         ['Machop', 21]]],
                       ['Rocket', 600, [['Rattata', 20],
                                         ['Raticate', 20],
                                         ['Drowzee', 20]]],
                       ['Rocket', 630, [['Koffing', 21],
                                         ['Zubat', 21]]],
                       ['Rocket', 690, [['Sandshrew', 23],
                                         ['Ekans', 23],
                                         ['Sandslash', 23]]],
                       ['Rocket', 690, [['Ekans', 23],
                                         ['Sandshrew', 23],
                                         ['Arbok', 23]]],
                       ['Rocket', 690, [['Ekans', 23],
                                         ['Sandshrew', 23],
                                         ['Arbok', 23]]]]
TRAINERS['S.S.ANNE'] = [['Gentleman', 1260, [['Growlithe', 18],
                                         ['Growlithe', 18]]],
                       ['Gentleman', 1330, [['Nidoran=', 19],
                                         ['Nidoran=', 19]]],
                       ['Lass', 270, [['Pidgey', 17],
                                         ['Nidoran=', 18]]],
                       ['Youngster', 315, [['Nidoran=', 21],
                                         ['Nidoran=', 21]]],
                       ['Sailor', 595, [['Shellder', 21],
                                         ['Shellder', 21]]],
                       ['Sailor', 510, [['Horsea', 17],
                                         ['Shellder', 17],
                                         ['Tentacool', 17]]],
                       ['Sailor', 510, [['Horsea', 17],
                                         ['Horsea', 17],
                                         ['Horsea', 17]]],
                       ['Sailor', 540, [['Tentacool', 18],
                                         ['Staryu', 18]]],
                       ['Fisherman', 595, [['Tentacool', 17],
                                         ['Staryu', 17],
                                         ['Shellder', 17]]],
                       ['Sailor', 600, [['Machop', 20],
                                         ['Machop', 20]]],
                       ['Fisherman', 530, [['Goldeen', 17],
                                         ['Tentacool', 17],
                                         ['Goldeen', 17]]],
                       ['Gentleman', 1640, [['Pikachu', 23],
                                         ['Pikachu', 23]]],
                       ['Gentleman', 1190, [['Growlithe', 17],
                                         ['Ponyta', 17]]],
                       ['Lass', 315, [['Rattata', 18],
                                         ['Pikachu', 18]]],
                       ['Sailor', 510, [['Machop', 17],
                                         ['Tentacool', 17]]],
                       ['Sailor', 510, [['Machop', 17],
                                         ['Tentacool', 17]]]]
TRAINERS['MT.MOON'] = [['Bug Catcher', 110, [['Weedle', 11],
                                         ['Kakuna', 11]]],
                       ['Lass', 210, [['Clefairy', 14],
                                         ['Clefairy', 14]]],
                       ['Super Nerd', 275, [['Magnemite', 11],
                                         ['Voltorb', 11]]],
                       ['Bug Catcher', 100, [['Caterpie', 10],
                                         ['Metapod', 10],
                                         ['Caterpie', 10]]],
                       ['Lass', 165, [['Oddish', 11],
                                         ['Bellsprout', 11]]],
                       ['Youngster', 150, [['Rattata', 10],
                                         ['Rattata', 10],
                                         ['Zubat', 10]]],
                       ['Hiker', 350, [['Geodude', 10],
                                         ['Geodude', 10],
                                         ['Onix', 10]]],
                       ['Rocket', 330, [['Sandshrew', 11],
                                         ['Rattata', 11],
                                         ['Zubat', 11]]],
                       ['Rocket', 360, [['Zubat', 12],
                                         ['Ekans', 12]]],
                       ['Rocket', 390, [['Raticate', 16],
                                         ['Raticate', 16]]],
                       ['Rocket', 390, [['Rattata', 13],
                                         ['Zubat', 13]]],
                       ['Rocket', 390, [['Rattata', 13],
                                         ['Zubat', 13]]]]
TRAINERS['VICTORY ROAD TRAINERS'] = [['Cooltrainer +', 1540, [['Persian', 44],
                                         ['Ninetales', 44]]],
                       ['Cooltrainer =', 1470, [['Ivysaur', 42],
                                         ['Wartortle', 42],
                                         ['Charmeleon', 42],
                                         ['Charizard', 42]]],
                       ['Blackbelt', 1075, [['Machoke', 43],
                                         ['Machop', 43],
                                         ['Machoke', 43]]],
                       ['Juggler', 1435, [['Drowzee', 41],
                                         ['Hypno', 41],
                                         ['Kadabra', 41],
                                         ['Kadabra', 41]]],
                       ['Tamer', 1365, [['Persian', 44],
                                         ['Golduck', 44]]],
                       ['Juggler', 1680, [['Mr. Mime', 48],
                                         ['Mr. Mime', 48]]],
                       ['Pok~maniac', 2000, [['Charmeleon', 40],
                                         ['Lapras', 40],
                                         ['Lickitung', 40]]],
                       ['Cooltrainer =', 1505, [['Exeggutor', 43],
                                         ['Cloyster', 43],
                                         ['Arcanine', 43]]],
                       ['Cooltrainer +', 1505, [['Parasect', 43],
                                         ['Dewgong', 43],
                                         ['Chansey', 43]]],
                       ['Cooltrainer +', 1505, [['Bellsprout', 43],
                                         ['Weepinbell', 43],
                                         ['Victreebel', 43]]],
                       ['Cooltrainer +', 1505, [['Bellsprout', 43],
                                         ['Weepinbell', 43],
                                         ['Victreebel', 43]]]]
TRAINERS['ROUTE 25'] = [['Hiker', 525, [['Machop', 15],
                                         ['Geodude', 15]]],
                       ['Hiker', 595, [['Onix', 17],
                                         ['Onix', 17]]],
                       ['Youngster', 225, [['Rattata', 15],
                                         ['Spearow', 15]]],
                       ['Youngster', 255, [['Slowpoke', 17],
                                         ['Slowpoke', 17]]],
                       ['Lass', 255, [['Nidoran=', 15],
                                         ['Nidoran+', 15]]],
                       ['Hiker', 545, [['Geodude', 13],
                                         ['Geodude', 13],
                                         ['Machop', 13],
                                         ['Geodude', 13]]],
                       ['Jr. Trainer =', 280, [['Rattata', 14],
                                         ['Ekans', 14]]],
                       ['Youngster', 210, [['Ekans', 14],
                                         ['Sandshrew', 14]]],
                       ['Youngster', 210, [['Ekans', 14],
                                         ['Sandshrew', 14]]]]
TRAINERS['ROUTE 24'] = [['Bug Catcher', 140, [['Caterpie', 14],
                                         ['Weedle', 14]]],
                       ['Lass', 210, [['Pidgey', 14],
                                         ['Nidoran+', 14]]],
                       ['Youngster', 210, [['Rattata', 14],
                                         ['Ekans', 14],
                                         ['Zubat', 14]]],
                       ['Lass', 240, [['Pidgey', 16],
                                         ['Nidoran+', 16]]],
                       ['Jr. Trainer =', 360, [['Mankey', 18],
                                         ['Mankey', 18]]],
                       ['Rocket', 450, [['Ekans', 15],
                                         ['Zubat', 15]]],
                       ['Rocket', 450, [['Ekans', 15],
                                         ['Zubat', 15]]]]
TRAINERS['ROCK TUNNEL'] = [['Pok~maniac', 1150, [['Cubone', 23],
                                         ['Slowpoke', 23]]],
                       ['Hiker', 665, [['Geodude', 19],
                                         ['Machop', 19],
                                         ['Geodude', 19],
                                         ['Geodude', 19]]],
                       ['Hiker', 700, [['Onix', 20],
                                         ['Onix', 20],
                                         ['Geodude', 20]]],
                       ['Hiker', 735, [['Geodude', 21],
                                         ['Graveler', 21]]],
                       ['Jr. Trainer +', 440, [['Bellsprout', 22],
                                         ['Clefairy', 22]]],
                       ['Jr. Trainer +', 380, [['Pidgey', 19],
                                         ['Rattata', 19],
                                         ['Rattata', 19],
                                         ['Bellsprout', 19]]],
                       ['Jr. Trainer +', 400, [['Meowth', 20],
                                         ['Oddish', 20],
                                         ['Pidgey', 20]]],
                       ['Pok~maniac', 1250, [['Slowpoke', 25],
                                         ['Slowpoke', 25]]],
                       ['Jr. Trainer +', 440, [['Oddish', 22],
                                         ['Bulbasaur', 22]]],
                       ['Pok~maniac', 700, [['Charmander', 22],
                                         ['Cubone', 22]]],
                       ['Hiker', 875, [['Geodude', 25],
                                         ['Geodude', 25]]],
                       ['Hiker', 700, [['Machop', 20],
                                         ['Onix', 20]]],
                       ['Jr. Trainer +', 420, [['Jigglypuff', 21],
                                         ['Pidgey', 21],
                                         ['Meowth', 21]]],
                       ['Hiker', 735, [['Geodude', 21],
                                         ['Geodude', 21],
                                         ['Graveler', 21]]],
                       ['Hiker', 735, [['Geodude', 21],
                                         ['Geodude', 21],
                                         ['Graveler', 21]]]]
TRAINERS['SEA ROUTE 21'] = [['Fisherman', 980, [['Seaking', 28],
                                         ['Goldeen', 28],
                                         ['Seaking', 28],
                                         ['Seaking', 28]]],
                       ['Fisherman', 945, [['Magikarp', 27],
                                         ['Magikarp', 27],
                                         ['Magikarp', 27],
                                         ['Magikarp', 27],
                                         ['Magikarp', 27],
                                         ['Magikarp', 27]]],
                       ['Cue Ball', 775, [['Tentacool', 31],
                                         ['Tentacool', 31],
                                         ['Tentacruel', 31]]],
                       ['Swimmer', 165, [['Seadra', 33],
                                         ['Tentacruel', 33]]],
                       ['Fisherman', 1085, [['Shellder', 31],
                                         ['Cloyster', 31]]],
                       ['Fisherman', 1155, [['Seaking', 33],
                                         ['Goldeen', 33]]],
                       ['Swimmer', 185, [['Starmie', 37],
                                         ['Starmie', 37]]],
                       ['Swimmer', 160, [['Poliwhirl', 32],
                                         ['Tentacool', 32],
                                         ['Seadra', 32]]],
                       ['Swimmer', 160, [['Poliwhirl', 32],
                                         ['Tentacool', 32],
                                         ['Seadra', 32]]]]
TRAINERS['SEA ROUTE 20'] = [['Beauty', 2170, [['Poliwag', 31],
                                         ['Seaking', 31]]],
                       ['Beauty', 2100, [['Shellder', 30],
                                         ['Shellder', 30],
                                         ['Cloyster', 30]]],
                       ['Jr. Trainer +', 620, [['Goldeen', 31],
                                         ['Seaking', 31]]],
                       ['Birdkeeper', 750, [['Fearow', 30],
                                         ['Fearow', 30],
                                         ['Pidgeotto', 30]]],
                       ['Swimmer', 175, [['Staryu', 35],
                                         ['Staryu', 35]]],
                       ['Beauty', 2100, [['Seadra', 30],
                                         ['Horsea', 30],
                                         ['Seadra', 30]]],
                       ['Swimmer', 155, [['Shellder', 31],
                                         ['Cloyster', 31]]],
                       ['Swimmer', 140, [['Horsea', 28],
                                         ['Horsea', 28],
                                         ['Seadra', 28],
                                         ['Horsea', 28]]],
                       ['Jr. Trainer +', 600, [['Tentacool', 30],
                                         ['Horsea', 30],
                                         ['Seel', 30]]],
                       ['Jr. Trainer +', 600, [['Tentacool', 30],
                                         ['Horsea', 30],
                                         ['Seel', 30]]]]
TRAINERS['VIRIDIAN CITY GYM'] = [['Blackbelt', 1000, [['Machop', 40],
                                         ['Machoke', 40]]],
                       ['Cooltrainer =', 1365, [['Sandslash', 39],
                                         ['Dugtrio', 39]]],
                       ['Tamer', 1720, [['Rhyhorn', 43],
                                         ['Rhyhorn', 43]]],
                       ['Cooltrainer =', 1505, [['Rhyhorn', 43],
                                         ['Rhyhorn', 43]]],
                       ['Blackbelt', 950, [['Machoke', 38],
                                         ['Machop', 38],
                                         ['Machoke', 38]]],
                       ['Tamer', 1365, [['Arbok', 39],
                                         ['Tauros', 39]]],
                       ['Blackbelt', 1075, [['Machoke', 43],
                                         ['Machoke', 43]]],
                       ['Blackbelt', 1075, [['Machoke', 43],
                                         ['Machoke', 43]]]]
TRAINERS['LAVENDER TOWN'] = [['Jr. Trainer +', 420, [['Pidgey', 21],
                                         ['Pidgeotto', 21]]],
                       ['Hiker', 735, [['Geodude', 21],
                                         ['Onix', 21]]],
                       ['Hiker', 665, [['Onix', 19],
                                         ['Graveler', 19]]],
                       ['Hiker', 665, [['Onix', 19],
                                         ['Graveler', 19]]]]
TRAINERS['SILPH COMPANY'] = [['Rocket', 750, [['Golbat', 25],
                                         ['Zubat', 25],
                                         ['Zubat', 25],
                                         ['Raticate', 25],
                                         ['Zubat', 25]]],
                       ['Rocket', 870, [['Cubone', 29],
                                         ['Zubat', 29]]],
                       ['Scientist', 1400, [['Magnemite', 28],
                                         ['Voltorb', 28],
                                         ['Magneton', 28]]],
                       ['Scientist', 1300, [['Grimer', 26],
                                         ['Weezing', 26],
                                         ['Koffing', 26],
                                         ['Weezing', 26]]],
                       ['Rocket', 840, [['Raticate', 28],
                                         ['Hypno', 28],
                                         ['Raticate', 28]]],
                       ['Scientist', 1450, [['Electrode', 29],
                                         ['Weezing', 29]]],
                       ['Rocket', 840, [['Ekans', 28],
                                         ['Zubat', 28],
                                         ['Cubone', 28]]],
                       ['Rocket', 870, [['Machop', 29],
                                         ['Drowzee', 29]]],
                       ['Scientist', 1650, [['Electrode', 33],
                                         ['Electrode', 33]]],
                       ['Rocket', 990, [['Hypno', 33],
                                         ['Hypno', 33]]],
                       ['Scientist', 1450, [['Magneton', 26],
                                         ['Koffing', 26],
                                         ['Weezing', 26],
                                         ['Magnemite', 26]]],
                       ['Juggler', 1015, [['Kadabra', 29],
                                         ['Mr. Mime', 29]]],
                       ['Rocket', 990, [['Arbok', 33],
                                         ['Arbok', 33]]],
                       ['Rocket', 870, [['Machop', 29],
                                         ['Machoke', 29]]],
                       ['Scientist', 1250, [['Voltorb', 25],
                                         ['Koffing', 25],
                                         ['Magneton', 25],
                                         ['Magnemite', 25],
                                         ['Koffing', 25]]],
                       ['Rocket', 840, [['Zubat', 28],
                                         ['Zubat', 28],
                                         ['Golbat', 28]]],
                       ['Rocket', 870, [['Cubone', 29],
                                         ['Cubone', 29]]],
                       ['Rocket', 780, [['Raticate', 26],
                                         ['Arbok', 26],
                                         ['Koffing', 26],
                                         ['Golbat', 26]]],
                       ['Rocket', 840, [['Sandshrew', 29],
                                         ['Sandslash', 29]]],
                       ['Scientist', 1450, [['Electrode', 29],
                                         ['Muk', 29]]],
                       ['Rocket', 780, [['Raticate', 26],
                                         ['Zubat', 26],
                                         ['Golbat', 26],
                                         ['Rattata', 26]]],
                       ['Rocket', 840, [['Weezing', 28],
                                         ['Golbat', 28],
                                         ['Koffing', 28]]],
                       ['Scientist', 1450, [['Grimer', 29],
                                         ['Electrode', 29]]],
                       ['Scientist', 1400, [['Voltorb', 28],
                                         ['Koffing', 28],
                                         ['Magneton', 28]]],
                       ['Rocket', 840, [['Golbat', 28],
                                         ['Drowzee', 28],
                                         ['Hypno', 28]]],
                       ['Rocket', 1400, [['Drowzee', 28],
                                         ['Grimer', 28],
                                         ['Machop', 28]]],
                       ['Scientist', 1450, [['Magnemite', 29],
                                         ['Koffing', 29]]],
                       ['Rocket', 840, [['Machoke', 33],
                                         ['Machoke', 33]]],
                       ['Rocket', 960, [['Cubone', 32],
                                         ['Drowzee', 32],
                                         ['Marowak', 32]]],
                       ['Giovanni', 4059, [['Nidorino', 37],
                                         ['Kangaskhan', 35],
                                         ['Rhyhorn', 37],
                                         ['Nidoqueen', 41]]],
                       ['Giovanni', 4059, [['Nidorino', 37],
                                         ['Kangaskhan', 35],
                                         ['Rhyhorn', 37],
                                         ['Nidoqueen', 41]]]]
TRAINERS['SEAFOAM ISLAND'] = [['Jr. Trainer =', 600, [['Tentacool', 30],
                                         ['Horsea', 30],
                                         ['Seel', 30]]],
                       ['Giovanni', 4059, [['Nidorino', 37],
                                         ['Kangaskhan', 35],
                                         ['Rhyhorn', 37],
                                         ['Nidoqueen', 41]]]]
TRAINERS['VIRIDIAN FOREST'] = [['Bug Catcher', 60, [['Weedle', 6],
                                         ['Caterpie', 6]]],
                       ['Bug Catcher', 70, [['Weedle', 7],
                                         ['Kakuna', 7],
                                         ['Weedle', 7]]],
                       ['Bug Catcher', 70, [['Weedle', 7],
                                         ['Kakuna', 7],
                                         ['Weedle', 7]]]]
TRAINERS['ROUTE 18'] = [['Birdkeeper', 725, [['Spearow', 29],
                                         ['Fearow', 29]]],
                       ['Birdkeeper', 650, [['Spearow', 26],
                                         ['Spearow', 26],
                                         ['Fearow', 26],
                                         ['Spearow', 26]]],
                       ['Birdkeeper', 650, [['Spearow', 26],
                                         ['Spearow', 26],
                                         ['Fearow', 26],
                                         ['Spearow', 26]]]]
TRAINERS['POK~MON MAN. TRAINERS'] = [['Scientist', 1450, [['Electrode', 29],
                                         ['Weezing', 29]]],
                       ['Burglar', 3060, [['Charmander', 34],
                                         ['Charmeleon', 34]]],
                       ['Burglar', 3420, [['Ninetales', 38],
                                         ['Ninetales', 38]]],
                       ['Scientist', 1650, [['Magneton', 33],
                                         ['Magnemite', 33],
                                         ['Voltorb', 33]]],
                       ['Burglar', 3060, [['Growlithe', 34],
                                         ['Ponyta', 34]]],
                       ['Burglar', 3060, [['Growlithe', 34],
                                         ['Ponyta', 34]]]]
TRAINERS['ROUTE 12'] = [['Fisherman', 770, [['Goldeen', 22],
                                         ['Poliwag', 22],
                                         ['Goldeen', 22]]],
                       ['Fisherman', 840, [['Tentacool', 24],
                                         ['Goldeen', 24]]],
                       ['Fisherman', 945, [['Goldeen', 27],
                                         ['Goldeen', 27]]],
                       ['Fisherman', 735, [['Poliwag', 21],
                                         ['Shellder', 21],
                                         ['Goldeen', 21],
                                         ['Horsea', 21]]],
                       ['Rocker', 725, [['Voltorb', 29],
                                         ['Electrode', 29]]],
                       ['Fisherman', 840, [['Magikarp', 24],
                                         ['Magikarp', 24]]],
                       ['Fisherman', 840, [['Magikarp', 24],
                                         ['Magikarp', 24]]]]
TRAINERS['ROUTE 13'] = [['Jr. Trainer =', 560, [['Goldeen', 28],
                                         ['Poliwag', 28],
                                         ['Horsea', 28]]],
                       ['Birdkeeper', 725, [['Pidgey', 29],
                                         ['Pidgeotto', 29]]],
                       ['Jr. Trainer =', 480, [['Pidgey', 24],
                                         ['Meowth', 24],
                                         ['Rattata', 24],
                                         ['Pikachu', 24],
                                         ['Meowth', 24]]],
                       ['Beauty', 1890, [['Rattata', 27],
                                         ['Pikachu', 27],
                                         ['Rattata', 27]]],
                       ['Beauty', 2030, [['Clefairy', 29],
                                         ['Meowth', 29]]],
                       ['Jr. Trainer =', 600, [['Poliwag', 30],
                                         ['Poliwag', 30]]],
                       ['Jr. Trainer =', 600, [['Poliwag', 30],
                                         ['Poliwag', 30]]]]
TRAINERS['ROUTE 10'] = [['Jr. Trainer +', 360, [['Pikachu', 20],
                                         ['Clefairy', 20]]],
                       ['Jr. Trainer =', 600, [['Poliwag', 30],
                                         ['Poliwag', 30]]]]
TRAINERS['ROUTE 11'] = [['Gambler', 1260, [['Poliwag', 18],
                                         ['Horsea', 18]]],
                       ['Youngster', 315, [['Ekans', 21],
                                         ['Ekans', 21]]],
                       ['Youngster', 285, [['Sandshrew', 19],
                                         ['Zubat', 19]]],
                       ['Youngster', 270, [['Nidoran=', 18],
                                         ['Nidorino', 18]]],
                       ['Gambler', 1260, [['Bellsprout', 18],
                                         ['Oddish', 18]]],
                       ['Gambler', 1260, [['Growlithe', 18],
                                         ['Vulpix', 18]]],
                       ['Engineer', 1050, [['Magnemite', 21],
                                         ['Magnemite', 21]]],
                       ['Youngster', 255, [['Rattata', 17],
                                         ['Rattata', 17],
                                         ['Raticate', 17]]],
                       ['Gambler', 1260, [['Voltorb', 18],
                                         ['Magnemite', 18]]],
                       ['Gambler', 1260, [['Voltorb', 18],
                                         ['Magnemite', 18]]]]
TRAINERS['ROUTE 16'] = [['Biker', 580, [['Grimer', 29],
                                         ['Koffing', 29]]],
                       ['Cue Ball', 700, [['Machop', 28],
                                         ['Mankey', 28],
                                         ['Machop', 28]]],
                       ['Cue Ball', 725, [['Mankey', 29],
                                         ['Machop', 28]]],
                       ['Biker', 660, [['Weezing', 33],
                                         ['Weezing', 33]]],
                       ['Cue Ball', 825, [['Machop', 33],
                                         ['Machop', 33]]],
                       ['Cue Ball', 825, [['Machop', 33],
                                         ['Machop', 33]]]]
TRAINERS['ROUTE 17'] = [['Biker', 560, [['Weezing', 28],
                                         ['Koffing', 28],
                                         ['Weezing', 28]]],
                       ['Cue Ball', 725, [['Machop', 29],
                                         ['Machoke', 29]]],
                       ['Cue Ball', 725, [['Mankey', 29],
                                         ['Primeape', 29]]],
                       ['Biker', 660, [['Muk', 33],
                                         ['Muk', 33]]],
                       ['Biker', 580, [['Voltorb', 29],
                                         ['Voltorb', 29]]],
                       ['Cue Ball', 825, [['Machoke', 33],
                                         ['Machoke', 33]]],
                       ['Cue Ball', 650, [['Mankey', 26],
                                         ['Mankey', 26],
                                         ['Machoke', 26],
                                         ['Machop', 26]]],
                       ['Cue Ball', 725, [['Primeape', 29],
                                         ['Machoke', 29]]],
                       ['Biker', 580, [['Weezing', 29],
                                         ['Muk', 29]]],
                       ['Biker', 580, [['Weezing', 29],
                                         ['Muk', 29]]]]
TRAINERS['ROUTE 14'] = [['Biker', 580, [['Koffing', 29],
                                         ['Muk', 29]]],
                       ['Birdkeeper', 825, [["Farfetch'd", 33],
                                         ["Farfetch'd", 33]]],
                       ['Biker', 560, [['Grimer', 28],
                                         ['Grimer', 28],
                                         ['Koffing', 28]]],
                       ['Biker', 580, [['Koffing', 29],
                                         ['Grimer', 29]]],
                       ['Biker', 520, [['Koffing', 26],
                                         ['Koffing', 26],
                                         ['Grimer', 26],
                                         ['Koffing', 26]]],
                       ['Biker', 520, [['Koffing', 26],
                                         ['Koffing', 26],
                                         ['Grimer', 26],
                                         ['Koffing', 26]]]]
TRAINERS['ROUTE 15'] = [['Jr. Trainer +', 580, [['Pikachu', 29],
                                         ['Raichu', 29]]],
                       ['Beauty', 2030, [['Pidgeotto', 29],
                                         ['Wigglytuff', 29]]],
                       ['Biker', 500, [['Koffing', 25],
                                         ['Koffing', 25],
                                         ['Weezing', 25],
                                         ['Koffing', 25],
                                         ['Grimer', 25]]],
                       ['Biker', 560, [['Koffing', 28],
                                         ['Grimer', 28],
                                         ['Weezing', 28]]],
                       ['Beauty', 2030, [['Bulbasaur', 29],
                                         ['Ivysaur', 29]]],
                       ['Jr. Trainer +', 560, [['Gloom', 28],
                                         ['Oddish', 28],
                                         ['Oddish', 28]]],
                       ['Jr. Trainer +', 660, [['Clefairy', 33],
                                         ['Clefairy', 33]]],
                       ['Birdkeeper', 725, [['Dodrio', 28],
                                         ['Doduo', 28],
                                         ['Doduo', 28]]],
                       ['Birdkeeper', 650, [['Pidgeotto', 26],
                                         ["Farfetch'd", 26],
                                         ['Doduo', 26],
                                         ['Pidgey', 26]]],
                       ['Birdkeeper', 650, [['Pidgeotto', 26],
                                         ["Farfetch'd", 26],
                                         ['Doduo', 26],
                                         ['Pidgey', 26]]]]

#TODO missing pokemon
#Aerodactyl
#Dratini
#Eevee
#Farfetch'd
#Goldeen
#Hitmonchan
#Hitmonlee
#Jynx
#Kabuto
#Lapras
#Lickitung
#Magikarp
#Mr. Mime
#Omanyte
#Poliwag
#Porygon

