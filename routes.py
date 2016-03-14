ROUTES = {}
MAPLIST = [[273,613],[273,390],[273,277],[329,277],
           [385,215],[497,160],[600,160],[721,109],[775,60],[721,221],
           [721,499],[889,160],[945,215],[945,277],[889, 326],
           [610,326],[832,550],[439,326],[385,499],[497,774],
           [609,726],[609,726],[609,726],
           [609,726]]
MAPROUTE = ['ROUTE 1', 'ROUTE 2', 'VIRIDIAN FOREST', "DIGLETT's CAVE",
            'ROUTE 3', 'MT.MOON', 'ROUTE 4', 'ROUTE 24', 'ROUTE 25', 'ROUTE 5',
            'ROUTE 6', 'ROUTE 9', 'ROCK TUNNEL', 'ROUTE 10', 'ROUTE 8',
            'ROUTE 7', 'ROUTE 11', 'ROUTE 16', 'ROUTE 17', 'ROUTE 18',
            'SAFARI ZONE MAIN AREA','SAFARI ZONE AREA 1','SAFARI ZONE AREA 2',
            'SAFARI ZONE AREA 3']

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
	'Weedle': [[8],.15],
	'Caterpie': [[8],.15]
}
ROUTES['ROUTE 25'] = {
	'Bellsprout': [[12,14],.2],
	'Oddish': [[12,14],.2],
	'Abra': [[8,12],.15],
	'Pidgey': [[12,13],.15],
	'Weedle': [[8],.15],
	'Caterpie': [[8],.15]
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
	'Kangashkhan': [[25,25],.06],
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
	'Kangashkhan': [[28,28],.04]
}
