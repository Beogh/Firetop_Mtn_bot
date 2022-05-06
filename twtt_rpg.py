import tweepy
from secrets import *
from player_stats import *
import glob
import random
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

auth = tweepy.OAuthHandler(hidden_consumer_key, hidden_consumer_secret)
auth.set_access_token(hidden_access_token, hidden_access_token_secret)
api = tweepy.API(auth)
client = tweepy.Client(
    consumer_key=hidden_consumer_key,
    consumer_secret=hidden_consumer_secret,
    access_token=hidden_access_token,
    access_token_secret=hidden_access_token_secret)
last_tweet_id = ''
font_selected = ImageFont.truetype('cambriab.ttf', 14)
initial_skill = starting_skill
initial_stamina = starting_stamina
initial_luck = starting_skill
initial_gold = starting_gold
initial_provisions = starting_provisions
current_skill = 0
current_stamina = 0
current_luck = 0
current_gold = 0
current_provisions = 0
current_personality = ''
potion_chosen = ''
chosen_difficulty = ''
current_room = 0
won_last_round = 'no'
items = []
keys = []
past_rooms = []
fight_text = []
room_choices = {'0-2': ['Skill', 'Strength', 'Fortune'], 0: ['Easy', 'Medium', 'Hard', 'Very Hard'],
                '0-1': ['Soldier', 'Cook', 'Berserker', 'Noble'],
                1: [71, 278], 4: [46, 332], 5: [97, 292], 6: [294, 275, 148, 107], 7: [271, 104, 99],
                9: [31, 322], 21: [339, 293], 22: [46, 332], 23: [326, 229], 29: [97, 292],
                30: [67, 267], 35: [136, 361], 36: [263, 353], 37: [366, 11, 277], 42: [257, 113], 43: [354, 52],
                46: [4, 206], 48: [391, 60],
                54: [308, 179], 57: [16, 2, 119], 59: [222, 297, 133], 60: [391, 60], 62: [6, 89],
                63: [281, 10], 66: [104, 99], 67: [267, 177], 68: [128, 243],
                70: [312, 246, 79, 349], 73: [3, 386, 209, 316], 78: [159, 237], 79: [137, 267],
                80: [129, 123, 195, 140], 81: [254, 380], 84: [204, 280, 377], 85: [106, 373, 318, 59],
                87: [199, 251], 88: [216, 384],
                89: [294, 275, 148, 107], 94: [260, 329], 95: [254, 380], 97: [334, 247, 292],
                98: [142, 105, 389], 100: [346, 91], 102: [303, 19, 68], 103: [252, 359], 107: [148, 197],
                112: [142, 105], 113: [285, 78], 114: [190, 94, 121, 385], 115: [95, 313, 330], 117: [354, 308],
                120: [48, 295], 121: [103, 359], 122: [268, 282, 13], 124: [138, 76], 128: [210, 58],
                134: [202, 325, 87], 137: [308, 52, 14, 234], 138: [163, 351], 141: [66, 111], 146: [366, 11],
                149: [181, 265, 355], 150: [222, 297, 133],
                157: [4, 329], 160: [312, 246, 79, 349], 162: [23, 69], 164: [129, 236], 165: [141, 66, 249],
                167: [187, 359], 168: [372, 65, 293], 171: [337, 187], 172: [249, 141, 165], 175: [177, 267],
                176: [270, 375], 177: [52, 391, 175], 178: [23, 69], 180: [70, 329, 22], 184: [322, 34],
                187: [171, 308], 189: [90, 25], 190: [167, 359], 191: [308, 392, 46],
                193: [93, 338], 194: [142, 105], 197: [48, 295], 205: [254, 380], 207: [83, 154],
                208: [397, 363],
                210: [225, 357], 214: [271, 104, 99], 215: [142, 105], 218: [3, 386, 209, 316], 220: [337, 187],
                222: [106, 373, 318, 59], 223: [53, 300], 225: [77, 63], 226: [312, 246, 79, 349],
                228: [106, 373, 318, 59],
                229: [143, 399], 232: [97, 292], 235: [176, 5], 237: [213, 314], 238: [70, 180, 329],
                242: [379, 139], 246: [329, 180, 70],
                250: [89, 62], 252: [312, 226], 253: [328, 125, 73], 254: [352, 333, 279, 380], 255: [193, 93],
                256: [398, 197, 114], 257: [168, 293], 260: [359, 329], 261: [381, 311],
                262: [199, 251], 265: [216, 384], 267: [312, 246, 79, 349], 268: [13, 282], 269: [77, 63],
                270: [61, 394, 375], 271: [336, 214],
                274: [324, 356, 98], 277: [146, 366, 11], 278: [156, 92], 280: [305, 178, 108], 284: [46, 392],
                285: [213, 314], 286: [294, 275, 148, 107], 291: [315, 52, 227],
                293: [285, 78], 297: [150, 256], 299: [260, 359], 300: [102, 303], 301: [82, 208],
                303: [128, 243], 307: [134, 87],
                308: [187, 54, 160, 354], 311: [305, 178, 108], 312: [187, 54, 160, 354], 314: [223, 300],
                315: [306, 291], 318: [85, 228], 320: [370, 42],
                323: [8, 255], 324: [142, 105, 389], 326: [35, 229], 328: [73, 125], 329: [157, 392, 299, 238],
                332: [329, 4], 336: [66, 172, 249],
                337: [312, 246, 79, 349], 341: [46, 392, 220, 191], 345: [381, 311], 349: [267, 30],
                353: [223, 300], 354: [308, 52, 14, 234], 356: [142, 105, 389], 357: [269, 57],
                358: [142, 105, 389], 359: [190, 94, 121, 385], 360: [294, 275, 148, 107], 362: [52, 391, 175],
                363: [370, 42], 364: [256, 373], 366: [89, 62], 367: [235, 323],
                370: [116, 42], 373: [106, 373, 318, 59], 375: [97, 292], 378: [296, 42], 380: [366, 11, 277],
                381: [84, 280], 384: [262, 307], 385: [114, 297, 398], 386: [55, 166],
                391: [52, 362, 48], 392: [206, 329], 395: [322, 34], 397: [240, 363],
                398: [364, 12], 399: [3, 386, 209, 316], 2: [269, 16], 17: [327, 380, 144], 18: [261, 348],
                71: [301, 248], 74: [279, 118],
                83: [360, 154], 91: [131, 20], 92: [301, 248], 125: [73, 73], 144: [101, 217],
                275: [230, 230], 305: [162, 108], 379: [139, 139], 389: [289, 112], 8: [273, 189], 13: [115],
                16: [50, 269], 19: [317], 20: [376, 291], 24: [135, 360],
                33: [147, 320], 39: [396], 41: [310], 61: [29, 375], 75: [273, 189], 86: [259, 350],
                93: [273, 189], 108: [185], 111: [304, 66], 116: [378, 42], 140: [395], 142: [396],
                143: [44, 399], 148: [390, 64], 152: [371], 154: [310], 158: [218], 179: [258, 54],
                188: [342, 209], 199: [283], 230: [390, 64], 236: [395], 240: [145], 248: [301],
                249: [304, 66], 251: [344, 399], 282: [115], 283: [344, 399], 289: [396], 304: [203, 66],
                309: [203, 66], 331: [287], 333: [327, 6, 224], 338: [75, 93], 365: [183, 237], 372: [21],
                377: [196], 394: [232], 10: [345, 18], 26: [274], 28: [143, 399], 31: [253], 34: [207], 45: [253],
                58: [15, 367],
                69: [143, 399], 76: [143, 399], 77: [345, 18], 90: [253], 96: [207], 101: [380],
                106: [152, 126], 131: [291], 135: [360], 136: [143, 399], 216: [384], 244: [143, 399],
                258: [54], 266: [237], 281: [345, 18], 327: [380], 351: [143, 399], 371: [274], 374: [207],
                376: [291],
                388: [253], 390: [120, 393], 12: [256, 364], 14: [117], 161: [1], 234: [43], 295: [48], 306: [291],
                47: [298, 158], 53: [155, 300], 55: [7, 166], 123: [184, 164, 140], 156: [343, 92],
                166: [218, 158], 195: [140, 164, 9], 209: [47, 158], 213: [36, 314],
                243: [210, 58], 298: [7, 86],
                316: [151, 218], 339: [201], 361: [136], 3: [272, 127], 99: [80, 264, 129],
                105: [39, 382, 368, 194, 215], 126: [152, 26],
                127: [272, 188],
                204: [130, 280, 377], 279: [380, 17, 333], 287: [32, 309], 292: [239, 40],
                334: [292], 340: [388, 31, 241, 45], 348: [331, 51], 383: [80, 264, 129], 64: [], 118: [], 217: [],
                224: [], 139: [], 169: [], 174: [], 182: [], 186: [], 192: [], 198: [], 200: [], 231: [], 233: [],
                245: [], 276: [], 288: [], 290: [], 302: [], 321: [], 335: [], 347: [], 382: [242],
                387: [], 396: [242], 400: [], 11: [366, 250], 15: [235, 323], 25: [90, 340], 27: [221, 81],
                32: [138, 76],
                38: [104, 99], 40: [355, 265, 181], 44: [3, 386, 209, 316], 49: [268, 282, 13],
                50: [77, 63], 51: [287],
                52: [391, 362, 354, 291], 56: [3, 386, 209, 316], 65: [293, 372],
                72: [221, 81], 109: [120, 212], 82: [208, 147, 33], 104: [268, 282, 13],
                110: [221, 81], 119: [269], 129: [122], 130: [280], 132: [319],
                133: [391, 362, 354, 234, 291], 145: [370, 42], 147: [397, 363],
                151: [218, 86, 158], 153: [399], 155: [102, 303],
                159: [365, 237, 365], 163: [28, 351], 170: [221, 81], 173: [24, 135, 360],
                181: [355, 265], 183: [266, 237], 185: [23, 69], 196: [305, 178, 108], 201: [285, 78],
                202: [199, 251], 203: [38, 66],
                206: [284, 341], 211: [173, 360], 212: [369, 120], 221: [72, 132, 27, 110, 170],
                227: [131, 291, 100, 20], 239: [88, 149], 241: [90], 247: [292],
                259: [271, 104, 99], 263: [223, 300], 264: [80, 129], 272: [271, 104, 99],
                273: [90, 25],
                294: [275, 148, 107], 296: [257, 113],
                310: [173, 360], 313: [221], 317: [128, 243], 319: [221, 81], 322: [83, 154],
                325: [199, 251], 330: [254, 380], 344: [56, 153], 342: [271, 104, 99], 343: [301, 248],
                346: [131], 350: [218], 352: [74, 279], 355: [181, 265], 368: [142, 105],
                369: [120, 212],
                393: [212, 369]}
normal_room_choices = {1: [71, 278], 4: [46, 332], 5: [97, 292], 6: [294, 275, 148, 107], 7: [271, 104, 99],
                       9: [31, 322], 21: [339, 293], 22: [46, 332], 23: [326, 229], 29: [97, 292],
                       30: [67, 267], 35: [136, 361], 36: [263, 353], 37: [366, 11, 277], 42: [257, 113], 43: [354, 52],
                       46: [4, 206], 48: [391, 60],
                       54: [308, 179], 57: [16, 2, 119], 59: [222, 297, 133], 60: [391, 60], 62: [6, 89],
                       63: [281, 10], 66: [104, 99], 67: [267, 177], 68: [128, 243],
                       70: [312, 246, 79, 349], 73: [3, 386, 209, 316], 78: [159, 237], 79: [137, 267],
                       80: [129, 123, 195, 140], 81: [254, 380], 84: [204, 280, 377], 85: [106, 373, 318, 59],
                       87: [199, 251], 88: [216, 384],
                       89: [294, 275, 148, 107], 94: [260, 329], 95: [254, 380], 97: [334, 247, 292],
                       98: [142, 105, 389], 100: [346, 91], 102: [303, 19, 68], 103: [252, 359], 107: [148, 197],
                       112: [142, 105], 113: [285, 78], 114: [190, 94, 121, 385], 115: [95, 313, 330], 117: [354, 308],
                       120: [48, 295], 121: [103, 359], 122: [268, 282, 13], 124: [138, 76], 128: [210, 58],
                       134: [202, 325, 87], 137: [308, 52, 14, 234], 138: [163, 351], 141: [66, 111], 146: [366, 11],
                       149: [181, 265, 355], 150: [222, 297, 133],
                       157: [4, 329], 160: [312, 246, 79, 349], 162: [23, 69], 164: [129, 236], 165: [141, 66, 249],
                       167: [187, 359], 168: [372, 65, 293], 171: [337, 187], 172: [249, 141, 165], 175: [177, 267],
                       176: [270, 375], 177: [52, 391, 175], 178: [23, 69], 180: [70, 329, 22], 184: [322, 34],
                       187: [171, 308], 189: [90, 25], 190: [167, 359], 191: [308, 392, 46],
                       193: [93, 338], 194: [142, 105], 197: [48, 295], 205: [254, 380], 207: [83, 154],
                       208: [397, 363],
                       210: [225, 357], 214: [271, 104, 99], 215: [142, 105], 218: [3, 386, 209, 316], 220: [337, 187],
                       222: [106, 373, 318, 59], 223: [53, 300], 225: [77, 63], 226: [312, 246, 79, 349],
                       228: [106, 373, 318, 59],
                       229: [143, 399], 232: [97, 292], 235: [176, 5], 237: [213, 314], 238: [70, 180, 329],
                       242: [379, 139], 246: [329, 180, 70],
                       250: [89, 62], 252: [312, 226], 253: [328, 125, 73], 254: [352, 333, 279, 380], 255: [193, 93],
                       256: [398, 197, 114], 257: [168, 293], 260: [359, 329], 261: [381, 311],
                       262: [199, 251], 265: [216, 384], 267: [312, 246, 79, 349], 268: [13, 282], 269: [77, 63],
                       270: [61, 394, 375], 271: [336, 214],
                       274: [324, 356, 98], 277: [146, 366, 11], 278: [156, 92], 280: [305, 178, 108], 284: [46, 392],
                       285: [213, 314], 286: [294, 275, 148, 107], 291: [315, 52, 227],
                       293: [285, 78], 297: [150, 256], 299: [260, 359], 300: [102, 303], 301: [82, 208],
                       303: [128, 243], 307: [134, 87],
                       308: [187, 54, 160, 354], 311: [305, 178, 108], 312: [187, 54, 160, 354], 314: [223, 300],
                       315: [306, 291], 318: [85, 228], 320: [370, 42],
                       323: [8, 255], 324: [142, 105, 389], 326: [35, 229], 328: [73, 125], 329: [157, 392, 299, 238],
                       332: [329, 4], 336: [66, 172, 249],
                       337: [312, 246, 79, 349], 341: [46, 392, 220, 191], 345: [381, 311], 349: [267, 30],
                       353: [223, 300], 354: [308, 52, 14, 234], 356: [142, 105, 389], 357: [269, 57],
                       358: [142, 105, 389], 359: [190, 94, 121, 385], 360: [294, 275, 148, 107], 362: [52, 391, 175],
                       363: [370, 42], 364: [256, 373], 366: [89, 62], 367: [235, 323],
                       370: [116, 42], 373: [106, 373, 318, 59], 375: [97, 292], 378: [296, 42], 380: [366, 11, 277],
                       381: [84, 280], 384: [262, 307], 385: [114, 297, 398], 386: [55, 166],
                       391: [52, 362, 48], 392: [206, 329], 395: [322, 34], 397: [240, 363],
                       398: [364, 12], 399: [3, 386, 209, 316]}
lucky_room_choices = {2: [269, 16], 17: [327, 380, 144], 18: [261, 348], 71: [301, 248], 74: [279, 118],
                      83: [360, 154], 91: [131, 20], 92: [301, 248], 125: [73, 73], 144: [101, 217],
                      275: [230, 230], 305: [162, 108], 379: [139, 139], 389: [289, 112]}
fight_room_choices = {8: [273, 189], 13: [115], 16: [50, 269], 19: [317], 20: [376, 291], 24: [135, 360],
                      33: [147, 320], 39: [396], 41: [310], 61: [29, 375], 75: [273], 86: [259, 350],
                      93: [273, 189], 108: [185], 111: [304, 66], 116: [378, 42], 140: [395], 142: [396],
                      143: [44, 399], 148: [390, 64], 152: [371], 154: [310], 158: [218], 179: [258, 54],
                      188: [342, 209], 199: [283], 230: [390, 64], 236: [395], 240: [145], 248: [301],
                      249: [304, 66], 251: [344, 399], 282: [115], 283: [344, 399], 289: [396], 304: [203, 66],
                      309: [203, 66], 331: [287], 333: [327, 6, 224], 338: [75, 93], 365: [183, 237], 372: [21],
                      377: [196], 394: [232]}
provisions_room_choices = {10: [345, 18], 26: [274], 28: [143, 399], 31: [253], 34: [207], 45: [253], 58: [15, 367],
                           69: [143, 399], 76: [143, 399], 77: [345, 18], 90: [253], 96: [207], 101: [380],
                           106: [152, 126], 131: [291], 135: [360], 136: [143, 399], 216: [384], 244: [143, 399],
                           258: [54], 266: [237], 281: [345, 18], 327: [380], 351: [143, 399], 371: [274], 374: [207],
                           376: [291],
                           388: [253], 390: [120, 393]}
random_fight_room_choices = {12: [256, 364], 14: [117], 161: [1], 234: [43], 295: [48], 306: [291]}
roll_a_die_room_choices = {47: [298, 158], 53: [155, 300], 55: [7, 166], 123: [184, 164, 140], 156: [343, 92],
                           166: [218, 158], 195: [140, 164, 9], 209: [47, 158], 213: [36, 314],
                           243: [210, 58], 298: [7, 86],
                           316: [151, 218], 339: [201], 361: [136]}
item_dependent_room_choices = {3: [272, 127], 99: [80, 264, 129], 105: [39, 382, 368, 194, 215], 126: [152, 26],
                               127: [272, 188],
                               204: [130, 280, 377], 279: [380, 17, 333], 287: [32, 309], 292: [239, 40],
                               334: [292], 340: [388, 31, 241, 45], 348: [331, 51], 383: [80, 264, 129]}
dead_rooms_choices = {64: [], 118: [], 217: [], 224: []}
key_rooms_choices = {139: [], 169: [], 174: [], 182: [], 186: [], 192: [], 198: [], 200: [], 231: [], 233: [],
                     245: [], 276: [], 288: [], 290: [], 302: [], 321: [], 335: [], 347: [], 382: [242],
                     387: [], 396: [242], 400: []}
special_passage_rooms_choices = {11: [366, 250], 15: [235, 323], 25: [90, 340], 27: [221, 81], 32: [138, 76],
                                 38: [104, 99], 40: [355, 265, 181], 44: [3, 386, 209, 316], 49: [268, 282, 13],
                                 50: [77, 63], 51: [287],
                                 52: [391, 362, 354, 291], 56: [3, 386, 209, 316], 65: [293, 372],
                                 72: [221, 81], 109: [120, 212], 75: [273, 189], 82: [208, 147, 33],
                                 104: [268, 282, 13],
                                 110: [221, 81], 119: [269], 129: [122], 130: [280], 132: [319],
                                 133: [391, 362, 354, 291], 145: [370, 42], 147: [397, 363],
                                 151: [218, 86, 158], 153: [399], 155: [102, 303],
                                 159: [365, 237, 365], 163: [28, 351], 170: [221, 81], 173: [24, 135, 360],
                                 181: [355, 265], 183: [266, 237], 185: [23, 69], 196: [305, 178, 108], 201: [285, 78],
                                 202: [199, 251], 203: [38, 66],
                                 206: [284, 341], 211: [173, 360], 212: [369, 120], 221: [72, 132, 27, 110, 170],
                                 227: [131, 291, 100, 20], 239: [88, 149], 241: [90], 247: [292],
                                 259: [271, 104, 99], 263: [223, 300], 264: [80, 129], 272: [271, 104, 99],
                                 273: [90, 25],
                                 294: [275, 148, 107], 296: [257, 113],
                                 310: [173, 360], 313: [221], 317: [128, 243], 319: [221, 81], 322: [83, 154],
                                 325: [199, 251], 330: [254, 380], 344: [56, 153], 342: [271, 104, 99], 343: [301, 248],
                                 346: [131], 350: [218], 352: [74, 279], 355: [181, 265], 368: [142, 105],
                                 369: [120, 212],
                                 393: [212, 369]}
# monster dictionary, each monster has a list with Skill then Stamina
monster_dictionary = {'Barbarian8': [7, 6, 'Barbarian', 189], 'Ogre16': [8, 10, 'Ogre', 269],
                      'Goblin19a': [5, 5, 'Goblin A'],
                      'Goblin19b': [5, 6, 'Goblin B'],
                      'Dwarf20a': [7, 4, 'Dwarf A', 291], 'Dwarf20b': [6, 6, 'Dwarf B', 291],
                      'Dwarf20c': [7, 5, 'Dwarf C', 291],
                      'Dwarf20d': [7, 5, 'Dwarf D', 291], 'Orc33': [6, 4, 'Orc', 320],
                      'Warlock39': [11, 18, 'Warlock'], 'Wight41': [9, 6, 'Wight', 360],
                      'Giant Spider61': [7, 8, 'Giant Spider', 375], 'Crocodile86': [7, 6, 'Crocodile'],
                      'Hand108': [6, 4, 'Hand'], 'Orc116a': [5, 4, 'Orc A', 42], 'Orc116b': [5, 5, 'Orc B', 42],
                      'Skeleton140a': [7, 5, 'Skeleton Leader'],
                      'Skeleton140b': [6, 5, 'Skeleton 1-A'], 'Skeleton140c': [6, 6, 'Skeleton 1-B'],
                      'Skeleton140d': [5, 6, 'Skeleton 2-A'], 'Skeleton140e': [5, 5, 'Skeleton 2-B'],
                      'Warlock142': [11, 18, 'Warlock'], 'Giant Sandworm143': [7, 7, 'Giant Sandworm', 399],
                      'Dragon152': [10, 12, 'Dragon'], 'Piranhas158': [5, 5, 'Piranhas'],
                      'Goblin161a': [5, 3, 'Goblin'], 'Orc161b': [6, 3, 'Orc'],
                      'Gremlin161c': [6, 4, 'Gremlin'], 'Giant Rat161d': [5, 4, 'Giant Rat'],
                      'Skeleton161e': [6, 5, 'Skeleton'], 'Troll161f': [8, 4, 'Troll'],
                      'Giant163': [8, 9, 'Giant', 351], 'Minotaur179': [9, 9, 'Minotaur', 54],
                      'Wererat188': [8, 5, 'Wererat', 209],
                      'Caveman199a': [7, 6, 'Caveman A'],
                      'Caveman199b': [6, 4, 'Caveman B'], 'Ghoul230': [8, 7, 'Ghoul'],
                      'Skeleton236a': [6, 5, 'Skeleton A'],
                      'Skeleton236b': [6, 6, 'Skeleton B'],
                      'Skeleton236c': [5, 5, 'Skeleton C'], 'Snake240': [5, 2, 'Snake'], 'Orc248': [6, 5, 'Orc'],
                      'Dog249': [7, 6, 'Dog'],
                      'Giant Bats251': [6, 6, 'Giant Bats', 399], 'Zombie282a': [7, 6, 'Club Zombie'],
                      'Zombie282b': [6, 6, 'Scythe Zombie'], 'Zombie282c': [6, 6, 'Pick Zombie'],
                      'Zombie282d': [6, 5, 'Axe Zombie'], 'Warlock289': [7, 12, 'Warlock'],
                      'Werewolf304': [8, 8, 'Werewolf', 66],
                      'Rat309a': [5, 4, 'Rat A'], 'Rat309b': [6, 3, 'Rat B'],
                      'Rat309c': [5, 5, 'Rat C'], 'Troll331': [8, 8, 'Troll'], 'Vampire333': [10, 10, 'Vampire', 380],
                      'Iron Cyclops338': [10, 10, 'Iron Cyclops', 93],
                      'Piranhas350a': [5, 5, 'Piranhas'], 'Piranhas350b': [5, 1, 'Piranhas'],
                      'Orc365a': [6, 4, 'Orc 1', 237],
                      'Orc365b': [5, 3, 'Orc 2', 237],
                      'Orc365c': [6, 4, 'Orc 3', 237], 'Orc365d': [5, 2, 'Orc 4', 237], 'Orc365e': [4, 4, 'Orc 5', 237],
                      'Orc Chieftain372a': [7, 6, 'Orc Chieftain'],
                      'Servant372b': [5, 3, 'Orc Servant'], 'Winged Gremlin377': [5, 7, 'Winged Gremlin'],
                      'Giant Spider394': [7, 8, 'Giant Spider']}
room_monster_dictionary = {8: ['Barbarian8'], 13: ['Zombie282a', 'Zombie282b', 'Zombie282c', 'Zombie282d'],
                           16: ['Ogre16'], 19: ['Goblin19a', 'Goblin19b'],
                           20: ['Dwarf20a', 'Dwarf20b', 'Dwarf20c'], 24: ['Wight41'],
                           33: ['Orc33'], 39: ['Warlock39'], 41: ['Wight41'],
                           61: ['Giant Spider61'], 75: ['Barbarian8'],
                           86: ['Crocodile86'], 93: ['Barbarian8'], 108: ['Hand108'], 111: ['Dog249'],
                           116: ['Orc116a', 'Orc116b'],
                           140: ['Skeleton140a', 'Skeleton140b', 'Skeleton140c', 'Skeleton140d', 'Skeleton140e'],
                           142: ['Warlock142'], 143: ['Giant Sandworm143'], 148: ['Ghoul230'],
                           152: ['Dragon152'], 154: ['Wight41'], 158: ['Piranhas158'],
                           161: ['Goblin161a', 'Orc161b', 'Gremlin161c', 'Giant Rat161d', 'Skeleton161e', 'Troll161f'],
                           163: ['Giant163'], 179: ['Minotaur179'], 188: ['Wererat188'],
                           199: ['Caveman199a', 'Caveman199b'], 230: ['Ghoul230'],
                           236: ['Skeleton236a', 'Skeleton236b', 'Skeleton236c'], 240: ['Snake240'], 248: ['Orc248'],
                           249: ['Dog249'], 251: ['Giant Bats251'],
                           282: ['Zombie282a', 'Zombie282b', 'Zombie282c', 'Zombie282d'], 283: ['Giant Bats251'],
                           289: ['Warlock289'], 304: ['Werewolf304'],
                           309: ['Rat309a', 'Rat309b', 'Rat309c'], 331: ['Troll331'],  333: ['Vampire333'],
                           338: ['Iron Cyclops338'], 350: ['Piranhas350a', 'Piranhas350b'],
                           365: ['Orc365a', 'Orc365b', 'Orc365c', 'Orc365d', 'Orc365e'],
                           372: ['Orc Chieftain372a', 'Servant372b'], 377: ['Winged Gremlin377'],
                           394: ['Giant Spider394']
                           }
# normal rooms have exclusively room choices at the end of them, these are all the final choice in the 'combined' folder
normal_rooms = [1, 4, 5, 6, 7, 9, 21, 22, 23, 29, 30, 35, 36, 37, 42, 43, 46, 48,
                54, 57, 59, 60, 62, 63, 66, 67, 68, 70, 73, 78, 79, 80, 81, 84, 85, 87, 88,
                89, 94, 95, 97, 98, 100, 102, 103, 107, 112, 113, 114, 115, 117, 120, 121, 122, 124, 128,
                134, 137, 138, 141, 146, 149, 150, 157, 160, 162, 164, 165, 167, 168, 171, 172, 175,
                176, 177, 178, 180, 184, 187, 189, 190, 191, 193, 194, 197, 205, 207, 208,
                210, 214, 215, 218, 220, 222, 223, 225, 226, 228, 229, 232, 235, 237, 238, 242, 246,
                250, 252, 253, 254, 255, 256, 257, 260, 261, 262, 265, 267, 268, 269, 270, 271,
                274, 277, 278, 280, 284, 285, 286, 291, 293, 297, 299, 300, 301, 303, 307,
                308, 311, 312, 314, 315, 318, 320,  323, 324, 326, 328, 329, 332, 336,
                337, 341, 345, 349, 353, 354, 356, 357, 358, 359, 360, 362, 363, 364, 366, 367,
                370, 373, 375, 378, 380, 381, 384, 385, 386, 391, 392, 395, 397, 398, 399]
# luck dependent rooms require you to test luck and change their outcome accordingly
luck_dependent_rooms = [2, 17, 18, 71, 74, 83, 91, 92, 125, 144, 275, 305, 379, 389]
# fight dependent rooms have a fight, it might have escape options or require the whole fight
fight_dependent_rooms = [8, 13, 16, 19, 20, 24, 33, 39, 41, 61, 86, 93, 108, 111, 116, 140, 142, 143, 148,
                         152, 154, 158, 179, 188, 199, 230, 236, 240, 248, 251, 282, 283, 289, 304, 309, 331, 333,
                         338, 365, 372, 377, 394]
# provisions dependent rooms allow you the choice to eat before continuing, or has a passage choice of eating
provisions_dependent_rooms = [10, 26, 28, 31, 34, 45, 58, 69, 76, 77, 90, 96, 101, 106, 131, 135, 136, 216, 244,
                              258, 266, 281, 327, 351, 371, 374, 376, 388, 390]
# random fight rooms send you to passage 161 to fight a random enemy then return you to their room
random_fight_rooms = [12, 14, 161, 234, 295, 306]
# special passages are notably different, probably to 319 or causes loss of stamina with choice
special_passage_rooms = [11, 15, 25, 27, 32, 38, 40, 44, 49, 50, 51, 52, 56, 65, 72, 75, 82, 104, 109, 110,
                         119, 129, 130, 132, 133, 145, 147, 151, 153, 155,
                         159, 163,
                         170, 173, 181, 183, 185, 196, 201, 202,
                         203, 206, 211, 212, 221, 227, 239, 241, 247, 259, 263, 264, 272, 273, 294, 296, 310,
                         313, 317, 319, 322, 325, 330, 342, 343,
                         344, 346, 350, 352, 355, 368, 369, 393]
# roll a die rooms require you to roll to determine where you go
roll_a_die_rooms = [47, 53, 55, 123, 156, 166, 195, 209, 213, 243, 298, 316, 339, 361]
# item dependent rooms allow one passage if you have an item
item_dependent_rooms = [3, 99, 105, 126, 127, 204, 279, 287, 292, 334, 340, 348, 383]
# dead rooms if you end up here, there's nothing next
dead_rooms = [64, 118, 217, 224]
# key rooms supersede all others, for logistical purposes, just the key passages after beating the warlock
key_rooms = [139, 169, 174, 182, 186, 192, 198, 200, 231, 233, 245, 276, 288, 290, 302, 321, 335, 347, 382, 387, 396,
             400]


def adjust_stats_based_on_personality():
    global current_personality
    global current_provisions
    global initial_skill
    if current_personality == 'Cook':
        current_provisions += 4
        gain_gold(3)
    elif current_personality == 'Berserker':
        initial_skill += 1
        modify_skill(1)
    elif current_personality == 'Noble':
        gain_gold(6)


def build_your_character():
    status_update = 'The difficulties:'
    poll_status = 'Please select a difficulty.'
    create_poll_tweet(0, status_update, poll_status)
    update_last_tweet_id()
    set_current_room('0-1')


def check_to_eat():
    global current_stamina
    global initial_stamina
    global current_provisions
    baseline_stamina = initial_stamina - 4
    if current_stamina <= baseline_stamina and current_provisions >= 1:
        return 'hungry'
    else:
        return 'not hungry'


def create_dead_room(room_entered):
    status_update = 'Your tale is over. Make better choices next time!'
    create_media_tweet(room_entered, status_update)
    set_current_room(0)
    initialize_game()


def create_fight_dependent_room(room_entered):
    global current_stamina
    global current_skill
    global last_tweet_id
    global fight_text
    global won_last_round
    global items
    status_update = ''
    options = fight_room_choices[room_entered]
    enemy_list = pull_monsters(room_entered)
    # rooms where you just fight a monster or monsters
    if room_entered in [8, 16, 19, 20, 33, 61, 93, 108, 142, 143, 152, 179, 188, 199, 236, 240, 248, 251, 283,
                        289, 304, 309, 331, 333, 338, 365, 372, 196]:
        for monster in enemy_list:
            result = fight_monster(monster)
            status_update = status_update + result
        if current_stamina > 0:
            generate_combat_log_image()
            create_media_tweet(room_entered, status_update)
            set_current_room(fight_room_choices[room_entered][0])
    # rooms where you gain 2 luck after defeating the first zombie, otherwise normal
    if room_entered in [13, 282]:
        for monster in enemy_list:
            result = fight_monster(monster)
            status_update = status_update + result
            if monster == 'Zombie282a':
                modify_luck(2)
        if current_stamina > 0:
            generate_combat_log_image()
            create_media_tweet(room_entered, status_update)
            set_current_room(fight_room_choices[room_entered][0])
    # room where you're fighting the warlock, but are invisible at the start
    if room_entered in [39]:
        warlock_stamina = monster_dictionary[room_monster_dictionary[room_entered][0]][1]
        warlock_skill = monster_dictionary[room_monster_dictionary[room_entered][0]][0]
        fight_text = []
        warlock_wounds = 0
        while current_stamina > 0 and warlock_stamina > warlock_wounds:
            player_result = (random.randint(1, 6) + random.randint(1, 6) + current_skill + 2)
            warlock_result = (random.randint(1, 6) + random.randint(1, 6) + warlock_skill)
            if player_result > warlock_result:
                extra_damage_result = test_extra_damage((warlock_stamina - warlock_wounds), warlock_skill)
                if extra_damage_result == 'no test':
                    warlock_wounds += 3
                    fight_text.append('You slash the Warlock for 3 damage!')
                elif extra_damage_result == 'lucky':
                    warlock_wounds += 4
                    fight_text.append('You slash the Warlock and test your luck...success!')
                    fight_text.append('You deal 4 damage to the Warlock. You have ' + str(current_luck) + ' luck.')
                elif extra_damage_result == 'unlucky':
                    warlock_wounds += 3
                    fight_text.append('You slash the Warlock and test your luck...but fail')
                    fight_text.append('You deal 3 damage to the Warlock. You have ' + str(current_luck) + ' luck.')
            if player_result < warlock_result:
                invis_test = random.randint(1, 6)
                dice_result = random.randint(1, 6)
                if invis_test == 2 or invis_test == 4:
                    if 'magic shield' in items and dice_result == 6:
                        fight_text.append('Your shield catches a glancing blow, leaving you unharmed.')
                    else:
                        lose_stamina(1, room_entered, '')
                        fight_text.append('The warlock strikes you, but your invisibility helps. '
                                          'You have ' + str(current_stamina) + ' stamina.')
                if invis_test == 1 or invis_test == 3 or invis_test == 5:
                    if 'magic shield' in items and dice_result == 6:
                        lose_stamina(1, get_current_room(), '')
                        fight_text.append('The warlock lands a lucky blow through your invisibility, '
                                          'but your shield deflects some of the damage.')
                        fight_text.append('You now have ' + str(current_stamina) + ' stamina.')
                    else:
                        lose_stamina(2, room_entered, '')
                        fight_text.append('The warlock strikes you. '
                                          'You have ' + str(current_stamina) + ' stamina.')
        if current_stamina > 0:
            generate_combat_log_image()
            status_update = 'You deftly defeat the Warlock!!!'
            create_media_tweet(room_entered, status_update)
            set_current_room(fight_room_choices[room_entered][0])
    # fight the wight for one round
    if room_entered in [41, 154]:
        wight = room_monster_dictionary[room_entered][0]
        wight_skill = monster_dictionary[room_monster_dictionary[room_entered][0]][0]
        # wight_stamina = monster_dictionary[room_monster_dictionary[room_entered][0]][1]
        fight_value = fight_round_with_monster(wight, wight_skill)
        while fight_value == 'monster win' or fight_value == 'same':
            if fight_value == 'monster win':
                fight_text.append('The wight hits you! You have ' + str(current_stamina) + '.')
                lose_stamina(2, room_entered, '')
            fight_value = fight_round_with_monster(wight, wight_skill)
        if current_stamina > 0:
            generate_combat_log_image()
            status_update = 'You strike the wight hard and turn to passage 310.'
            create_media_tweet(room_entered, status_update)
            set_current_room(310)
            create_special_passage_room(310)
    # fight the croc 2 rounds then decide whether the turbulence will help
    if room_entered in [86]:
        croc_skill = monster_dictionary[room_monster_dictionary[room_entered][0]][0]
        croc_stamina = monster_dictionary[room_monster_dictionary[room_entered][0]][1]
        round_1 = fight_round_with_monster(enemy_list[0], croc_skill)
        round_2 = fight_round_with_monster(enemy_list[0], croc_skill)
        if round_1 == 'monster win':
            reduced_damage = test_reduce_damage(2, croc_skill)
            if reduced_damage == 'no test':
                lose_stamina(2, room_entered, '')
            if reduced_damage == 'lucky':
                lose_stamina(1, room_entered, '')
                fight_text.append('You test your luck to reduce the damage from the crocodile, and pass.')
                fight_text.append('You now have ' + str(current_stamina) + ' stamina.')
            if reduced_damage == 'unlucky':
                lose_stamina(2, room_entered, '')
                fight_text.append('You test your luck to reduce the damage from the crocodile, but fail.')
                fight_text.append('You now have ' + str(current_stamina) + ' stamina.')
        if round_2 == 'monster win':
            reduced_damage = test_reduce_damage(2, croc_skill)
            if reduced_damage == 'no test':
                lose_stamina(2, room_entered, '')
            if reduced_damage == 'lucky':
                lose_stamina(1, room_entered, '')
                fight_text.append('You test your luck to reduce the damage from the crocodile, and pass.')
                fight_text.append('You now have ' + str(current_stamina) + ' stamina.')
            if reduced_damage == 'unlucky':
                lose_stamina(2, room_entered, '')
                fight_text.append('You test your luck to reduce the damage from the crocodile, but fail.')
                fight_text.append('You now have ' + str(current_stamina) + ' stamina.')
        if round_1 == 'player win':
            croc_stamina -= 2
        if round_2 == 'player_win':
            croc_stamina -= 2
        status_update = 'Your stamina: ' + str(current_stamina) + '\n' + 'Crocodile stamina: ' + str(croc_stamina)
        next_path_choices = ['fight on!', 350]
        with open("adversary_stamina.txt", 'wt') as writing:
            writing.write(str(croc_stamina))
        poll_status = 'Try to kill the crocodile, or try to distract it for one round?'
        media_tweet = create_media_tweet(room_entered, status_update)
        poll_tweet = client.create_tweet(text=poll_status, in_reply_to_tweet_id=media_tweet.data['id'],
                                         poll_options=next_path_choices, poll_duration_minutes=359)
        last_tweet_id = poll_tweet.data['id']
    # fight dog before old man
    if room_entered in [111, 249]:
        dog_skill = monster_dictionary[room_monster_dictionary[room_entered][0]][0]
        dog_stamina = monster_dictionary[room_monster_dictionary[room_entered][0]][1]
        dog_wounds = 0
        while current_stamina > 0 and dog_stamina > dog_wounds:
            round_result = fight_round_with_monster(enemy_list[0], dog_skill)
            if round_result == 'player win':
                extra_damage_test = test_extra_damage((dog_stamina - dog_wounds), dog_skill)
                if extra_damage_test == 'no test':
                    dog_wounds += 2
                    fight_text.append('You strike the dog.')
                elif extra_damage_test == 'lucky':
                    dog_wounds += 3
                    fight_text.append('You test your luck and strike true, dealing 3 damage to the dog.')
                    fight_text.append('You have ' + str(current_luck) + ' luck.')
                elif extra_damage_test == 'unlucky':
                    dog_wounds += 2
                    fight_text.append('You test your luck to deal additional damage, but fail.')
                    fight_text.append('The dog takes 2 damage and you have ' + str(current_luck) + ' luck remaining.')
            breath = random.randint(1, 3)
            if breath == 1:
                reduced_damage_test = test_reduce_damage(1, dog_skill)
                if reduced_damage_test == 'no test':
                    fight_text.append('The dog singes you with fire!')
                    fight_text.append('You have ' + str(current_stamina) + ' stamina.')
                    lose_stamina(1, room_entered, '')
                elif reduced_damage_test == 'lucky':
                    fight_text.append('The dog spits fire at you, but you test luck and pass, taking no damage.')
                elif reduced_damage_test == 'unlucky':
                    lose_stamina(1, get_current_room(), '')
                    fight_text.append('The dog spits fire at you, and you attempt to use your luck to dodge, but fail.')
                    fight_text.append('You now have ' + str(current_stamina) + ' stamina.')
            elif round_result == 'monster win':
                reduced_damage_test = test_reduce_damage(2, dog_skill)
                if reduced_damage_test == 'no test':
                    fight_text.append('The dog bites you. You have ' + str(current_stamina) + ' stamina.')
                    lose_stamina(2, room_entered, '')
                elif reduced_damage_test == 'lucky':
                    lose_stamina(1, get_current_room(), '')
                    fight_text.append('The dog bites you, but you use your luck to dodge. Take 1 damage.')
                    fight_text.append('You have ' + str(current_stamina) +
                                      ' stamina and ' + str(current_luck) + ' luck.')
                elif reduced_damage_test == 'unlucky':
                    lose_stamina(2, get_current_room(), '')
                    fight_text.append('The dog bites you, you try to dodge but fail when you test your luck.')
                    fight_text.append('You have ' + str(current_stamina) +
                                      ' stamina and ' + str(current_luck) + ' luck.')
        if current_stamina > 0:
            generate_combat_log_image()
            status_update = 'The dog lies dead.'
            modify_luck(1)
            create_poll_tweet(room_entered, status_update, 'Escape or stay?')
    # fight orcs with +1 to die results
    if room_entered in [116]:
        current_skill += 1
        for monster in enemy_list:
            result = fight_monster(monster)
            status_update = status_update + result
        current_skill -= 1
        if current_stamina > 0:
            generate_combat_log_image()
            create_media_tweet(room_entered, status_update)
            set_current_room(fight_room_choices[room_entered][0])
    # skeleton fight, single then pairs
    if room_entered in [140]:
        fight_monster(enemy_list[0])
        target_stamina = monster_dictionary[enemy_list[1]][1]
        target_skill = monster_dictionary[enemy_list[1]][1]
        secondary_skill = monster_dictionary[enemy_list[2]][0]
        target_wounds = 0
        while target_stamina > target_wounds and current_stamina > 0:
            first_skeleton_result = fight_round_with_monster(enemy_list[1], target_skill)
            secondary_result = (random.randint(1, 6) + random.randint(1, 6) + secondary_skill)
            player_defense_result = (random.randint(1, 6) + random.randint(1, 6) + current_skill)
            if 'magic helmet' in items:
                player_defense_result += 1
            if current_personality == 'Noble' and won_last_round == 'yes':
                player_defense_result += 1
            if secondary_result > player_defense_result:
                reduce_damage_test = test_reduce_damage(2, secondary_skill)
                if reduce_damage_test == 'no test':
                    lose_stamina(2, room_entered, '')
                    fight_text.append("Skeleton B hits you while you're distracted with Skeleton A.")
                elif reduce_damage_test == 'lucky':
                    lose_stamina(1, room_entered, '')
                    fight_text.append("Skeleton B hits you while you're distracted with "
                                      "Skeleton A, but you use your luck to reduce the damage.")
                elif reduce_damage_test == 'unlucky':
                    lose_stamina(2, room_entered, '')
                    fight_text.append("Skeleton B hits you while you're distracted with "
                                      "Skeleton A, you test your luck to reduce the damage, but fail.")
                fight_text.append('You now have ' + str(current_stamina) + ' stamina.')
            if first_skeleton_result == 'player win':
                extra_damage_test = test_extra_damage((target_stamina - target_wounds), target_skill)
                if extra_damage_test == 'no test':
                    target_wounds += 2
                    fight_text.append('You bash Skeleton A for 2 damage.')
                if extra_damage_test == 'lucky':
                    target_wounds += 3
                    fight_text.append('You test your luck to hit the skeleton harder, and pass. You deal 3 damage.')
                    fight_text.append('You now have ' + str(current_luck) + ' luck.')
                if extra_damage_test == 'unlucky':
                    target_wounds += 2
                    fight_text.append('You test your luck to hit the skeleton harder, but fail, dealing 2 damage.')
                    fight_text.append('You now have ' + str(current_luck) + ' luck.')
            elif first_skeleton_result == 'monster win':
                reduced_damage_test = test_reduce_damage(2, target_skill)
                if reduced_damage_test == 'no test':
                    lose_stamina(2, room_entered, '')
                    fight_text.append('Skeleton A slashes you for 2 damage.')
                elif reduced_damage_test == 'lucky':
                    lose_stamina(1, room_entered, '')
                    fight_text.append('Skeleton A slashes you, but you test your luck and pass, '
                                      'reducing the damage to 1.')
                elif reduced_damage_test == 'unlucky':
                    lose_stamina(2, room_entered, '')
                    fight_text.append('You attempt to dodge Skeleton A by testing luck, but fail.')
                    fight_text.append('You now have ' +
                                      str(current_stamina) + ' stamina and ' + str(current_luck) + '.')
        fight_monster(enemy_list[2])
        target_stamina = monster_dictionary[enemy_list[4]][1]
        target_skill = monster_dictionary[enemy_list[4]][0]
        secondary_skill = monster_dictionary[enemy_list[3]][1]
        target_wounds = 0
        fight_text.append('You have defeated the first pair of skeletons.')
        while target_stamina > target_wounds and current_stamina > 0:
            third_skeleton_result = fight_round_with_monster(enemy_list[3], target_skill)
            secondary_result = (random.randint(1, 6) + random.randint(1, 6) + secondary_skill)
            player_defense_result = (random.randint(1, 6) + random.randint(1, 6) + current_skill)
            if 'magic helmet' in items:
                player_defense_result += 1
            if current_personality == 'Noble' and won_last_round == 'yes':
                player_defense_result += 1
            if secondary_result > player_defense_result:
                reduce_damage_test = test_reduce_damage(2, secondary_skill)
                if reduce_damage_test == 'no test':
                    lose_stamina(2, room_entered, '')
                    fight_text.append("Skeleton A hits you while you're distracted with Skeleton B.")
                elif reduce_damage_test == 'lucky':
                    lose_stamina(1, room_entered, '')
                    fight_text.append("Skeleton A hits you while you're distracted with "
                                      "Skeleton B, but you use your luck to reduce the damage.")
                elif reduce_damage_test == 'unlucky':
                    lose_stamina(2, room_entered, '')
                    fight_text.append("Skeleton A hits you while you're distracted with "
                                      "Skeleton B, you test your luck to reduce the damage, but fail.")
            extra_damage_test = test_extra_damage((target_stamina - target_wounds), target_skill)
            if extra_damage_test == 'no test':
                target_wounds += 2
                fight_text.append('You bash Skeleton B for 2 damage.')
            if extra_damage_test == 'lucky':
                target_wounds += 3
                fight_text.append('You test your luck to hit the skeleton harder, and pass. You deal 3 damage.')
                fight_text.append('You now have ' + str(current_luck) + ' luck.')
            if extra_damage_test == 'unlucky':
                target_wounds += 2
                fight_text.append('You test your luck to hit the skeleton harder, but fail, dealing 2 damage.')
                fight_text.append('You now have ' + str(current_luck) + ' luck.')
            elif third_skeleton_result == 'monster win':
                reduced_damage_test = test_reduce_damage(2, target_skill)
                if reduced_damage_test == 'no test':
                    lose_stamina(2, room_entered, '')
                    fight_text.append('Skeleton B slashes you for 2 damage.')
                elif reduced_damage_test == 'lucky':
                    lose_stamina(1, room_entered, '')
                    fight_text.append('Skeleton B slashes you, but you test your luck and pass, '
                                      'reducing the damage to 1.')
                elif reduced_damage_test == 'unlucky':
                    lose_stamina(2, room_entered, '')
                    fight_text.append('You attempt to dodge Skeleton B by testing luck, but fail.')
                    fight_text.append('You now have ' +
                                      str(current_stamina) + ' stamina and ' + str(current_luck) + '.')
        fight_monster(enemy_list[3])
        if current_stamina > 0:
            generate_combat_log_image()
            status_update = ('You defeat the skeletons, turn to passage ' + str(options[0]))
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
    # ghoul fight, checking wounds
    if room_entered in [148, 230]:
        ghoul_skill = monster_dictionary[enemy_list[0]][0]
        ghoul_stamina = monster_dictionary[enemy_list[0]][1]
        player_wounds = 0
        ghoul_wounds = 0
        while player_wounds < 4 and current_stamina > 0 and ghoul_stamina > ghoul_wounds:
            round_result_ghoul = fight_round_with_monster(enemy_list[0], ghoul_skill)
            if round_result_ghoul == 'player win':
                extra_damage_test = test_extra_damage((ghoul_stamina - ghoul_wounds), ghoul_skill)
                if extra_damage_test == 'no test':
                    ghoul_wounds += 2
                    fight_text.append('You slash the ghoul for 2 damage.')
                if extra_damage_test == 'lucky':
                    ghoul_wounds += 3
                    fight_text.append('You test your luck to hit the ghoul harder, and pass. You deal 3 damage.')
                    fight_text.append('You now have ' + str(current_luck) + ' luck.')
                if extra_damage_test == 'unlucky':
                    ghoul_wounds += 2
                    fight_text.append('You test your luck to hit the ghoul harder, but fail, dealing 2 damage.')
                    fight_text.append('You now have ' + str(current_luck) + ' luck.')
            elif round_result_ghoul == 'monster win':
                reduced_damage_test = test_reduce_damage(2, ghoul_skill)
                if reduced_damage_test == 'no test':
                    lose_stamina(2, room_entered, '')
                    fight_text.append('The ghoul hits you for 2 damage.')
                elif reduced_damage_test == 'lucky':
                    lose_stamina(1, room_entered, '')
                    fight_text.append('The ghoul hits, but you test your luck and pass, '
                                      'reducing the damage to 1.')
                elif reduced_damage_test == 'unlucky':
                    lose_stamina(2, room_entered, '')
                    player_wounds += 1
                    fight_text.append('You attempt to dodge the ghoul by testing luck, but fail.')
                    fight_text.append('You now have ' +
                                      str(current_stamina) + ' stamina and '
                                      + str(current_luck) + ' and ' + str(player_wounds) + ' wounds from the ghoul.')
                player_wounds += 1
        if player_wounds >= 4:
            status_update = ('You feel your limbs stiffening! Turn to passage ' + str(options[1]))
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
        else:
            generate_combat_log_image()
            status_update = 'You have slain the ghoul. Head to passage ' + str(options[0])
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
    # fight then a chance to eat
    if room_entered in [158]:
        for monster in enemy_list:
            result = fight_monster(monster)
            status_update = status_update + result
        hungry = check_to_eat()
        if hungry == 'hungry':
            eat_provisions()
            status_update = status_update + ' You eat some food and dry off. You have ' \
                                            + str(current_stamina) + ' stamina.'
        generate_combat_log_image()
        set_current_room(options[0])
        create_media_tweet(room_entered, status_update)
    # giant spider fight with sticky web reducing your rolls by 2
    if room_entered in [394]:
        current_skill -= 2
        for monster in enemy_list:
            result = fight_monster(monster)
            status_update = status_update + result
        current_skill += 2
        if current_stamina > 0:
            generate_combat_log_image()
            create_media_tweet(room_entered, status_update)
            set_current_room(fight_room_choices[room_entered][0])


def create_item_dependent_room(room_entered):
    global items
    global current_gold
    global last_tweet_id
    options = item_dependent_room_choices[room_entered]
    # rooms that require gold
    if room_entered in [3, 5]:
        if room_entered in [3]:
            if current_gold >= 3:
                status_update = 'Will you pay 3 gold to cross?'
                create_poll_tweet(room_entered, status_update, 'Make your choice.')
            if current_gold < 3:
                status_update = "You don't have the gold, so you decide to threaten him."
                create_media_tweet(room_entered, status_update)
                set_current_room(options[1])
        if room_entered in [5]:
            if current_gold >= 5:
                status_update = 'Is it worth 5 gold?'
                create_poll_tweet(room_entered, status_update, 'Can you really take him?')
            if current_gold < 5:
                status_update = "The threats don't work, and you don't have enough gold to pacify him."
                create_media_tweet(room_entered, status_update)
                set_current_room(options[1])
    # dependent on having the boat house key
    if room_entered in [99, 383]:
        if 'boat house key' in items:
            status_update = 'You have the key, but is that how you want to approach this?'
            poll_status = ''
            create_poll_tweet(room_entered, status_update, poll_status)
        else:
            room_options = [264, 129]
            status_update = 'You do not have the key, break down the door or head to the riverbank?'
            poll_status = 'The door looks pretty sturdy, but maybe you feel up to it.'
            media_tweet = create_media_tweet(room_entered, status_update)
            poll_tweet = client.create_tweet(text=poll_status, in_reply_to_tweet_id=media_tweet.data['id'],
                                             poll_options=room_options, poll_duration_minutes=359)
            last_tweet_id = poll_tweet.data['id']
    # five options
    if room_entered in [105]:
        status_update = ''
        available_passages = []
        if 'potion of invisibility' in items:
            available_passages.append(39)
        if 'the eye of the cyclops' in items:
            available_passages.append(382)
        if 'a piece of cheese' in items:
            available_passages.append(368)
        if 'bow with silver arrow' in items:
            available_passages.append(194)
        if 'Y-shaped stick' in items:
            available_passages.append(215)
        if len(available_passages) == 5:
            status_update = 'Your Y-shaped stick broke while in your rucksack. '
            available_passages.remove(215)
        status_update = status_update + 'what item will fare best?'
        media_tweet = create_media_tweet(room_entered, status_update)
        poll_status = 'You weigh your options...'
        poll_tweet = client.create_tweet(text=poll_status, in_reply_to_tweet_id=media_tweet.data['id'],
                                         poll_options=available_passages, poll_duration_minutes=359)
        last_tweet_id = poll_tweet.data['id']
    # check if you have the anti-dragon spell
    if room_entered in [126]:
        if 'fireball' in items:
            status_update = 'You recall the spell written on parchment.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
        if 'fireball' not in items:
            status_update = "The name doesn't ring a ball. Continue to passage " + str(options[0])
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
    # fight the guy at 127
    if room_entered in [127]:
        if current_gold >= 5:
            status_update = 'Maybe you bit off a little more than you can chew?'
            poll_status = 'Make your choice, quickly!'
            create_poll_tweet(room_entered, status_update, poll_status)
        else:
            status_update = "You don't have the gold to mollify him, prepare to fight... whatever he is."
            create_media_tweet(room_entered, status_update)
            set_current_room(188)
    # one poll if you have 1 gold, a different poll if you don't have gold
    if room_entered in [204]:
        if current_gold >= 1:
            status_update = 'You contemplate playing a game at passage ' + str(options[0]) + '.'
            poll_update = 'What will you do?'
            create_poll_tweet(room_entered, status_update, poll_update)
        if current_gold < 1:
            available_passages = [280, 377]
            status_update = 'You check your pockets, but find them bereft of gold.'
            poll_update = 'Leave, or attack the man?'
            media_tweet = create_media_tweet(room_entered, status_update)
            poll_tweet = client.create_tweet(text=poll_update, in_reply_to_tweet_id=media_tweet.data['id'],
                                             poll_options=available_passages, poll_duration_minutes=359)
            last_tweet_id = poll_tweet.data['id']
    # vampire choice room
    if room_entered in [279]:
        available_passages = []
        if 'crucifix' in items:
            available_passages.append(380)
        if 'wooden stake' in items:
            available_passages.append(17)
        available_passages.append(333)
        if len(available_passages) == 1:
            print(available_passages)
            status_update = 'You grimly draw your sword and move to passage ' + str(available_passages[0])
            create_media_tweet(room_entered, status_update)
            set_current_room(available_passages[0])
        else:
            status_update = 'You consider your options.'
            poll_update = "How to deal with the VAMPIRE?"
            vampire_poll_choices = []
            for each in available_passages:
                vampire_poll_choices.append(str(each))
            media_tweet = create_media_tweet(room_entered, status_update)
            poll_tweet = client.create_tweet(text=poll_update, in_reply_to_tweet_id=media_tweet.data['id'],
                                             poll_options=vampire_poll_choices, poll_duration_minutes=359)
            last_tweet_id = poll_tweet.data['id']
    # got the cheese for the rats or not
    if room_entered in [287]:
        if 'a piece of cheese' in items:
            status_update = 'You pull the cheese, and head to passage ' + str(options[0]) + '.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
        else:
            status_update = 'For want of some cheese, you steel your resolve at passage ' + str(options[1])
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
    # blue candle requisite
    if room_entered in [292]:
        if 'blue candle' in items:
            status_update = 'You thank the merchant for the candle and pull it out at passage ' + str(options[0]) + '.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
        else:
            status_update = 'You curse your lack of preparedness and scramble to passage ' + str(options[1]) + '.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
    # buying blue candle
    if room_entered in [334]:
        if current_gold >= 20:
            status_update = "You look over the candle, it doesn't look impressive."
            poll_update = 'But it could be worth it?'
            # this isn't right, shouldn't be a poll tweet for rooms
            create_poll_tweet(room_entered, status_update, poll_update)
        if current_gold < 20:
            status_update = "It's a very impressive candle, but you only have " + str(current_gold) + 'gold.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
    # up to 4 unique choices
    if room_entered in [340]:
        available_passages = [388]
        if 'the eye of the cyclops' in items:
            available_passages.append(31)
        if 'wooden stake' in items:
            available_passages.append(241)
        if 'a piece of cheese' in items:
            available_passages.append(45)
        if len(available_passages) == 1:
            status_update = 'With only your sword to wield, you slash at the painting.'
            create_media_tweet(room_entered, status_update)
            set_current_room(available_passages[0])
        else:
            status_update = 'Anger, fear, disgust, a mixture of emotions well up within you!'
            poll_update = 'How will you attack the painting?'
            media_tweet = create_media_tweet(room_entered, status_update)
            poll_tweet = client.create_tweet(text=poll_update, in_reply_to_tweet_id=media_tweet.data['id'],
                                             poll_options=available_passages, poll_duration_minutes=359)
            last_tweet_id = poll_tweet.data['id']
    # potion of invis to fight troll
    if room_entered in [348]:
        if 'potion of invisibility' in items:
            status_update = 'You quaff the potion and fade into passage ' + str(options[1])
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
        else:
            status_update = 'You wince and try to keep off your twisted ankle.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])


def create_key_room(room_entered):
    global current_stamina
    global key_rooms
    global last_tweet_id
    # room 139: build from keys
    if room_entered in [139]:
        if len(keys) >= 3:
            key_passage_choices = []
            key_list = tuple(keys)
            for key in key_list:
                running_sum = key
                second_digit_list = list(key_list)
                second_digit_list.remove(key)
                for second_key in second_digit_list:
                    running_sum += second_key
                    third_digit_list = list(key_list)
                    third_digit_list.remove(key)
                    third_digit_list.remove(second_key)
                    for third_key in third_digit_list:
                        running_sum += third_key
                        if running_sum not in key_passage_choices:
                            key_passage_choices.append(str(running_sum))
                        running_sum = key + second_key
                    running_sum = key
            if len(key_passage_choices) == 1:
                status_update = 'With only one combination of keys, you try each one in the chest.'
                create_media_tweet(room_entered, status_update)
                set_current_room(key_passage_choices[0])
            if 4 >= len(key_passage_choices) > 1:
                status_update = 'You pull out your keys and consider which will open the chest.'
                poll_update = 'Which passage will you head to?'
                media_tweet = create_media_tweet(room_entered, status_update)
                poll_tweet = client.create_tweet(text=poll_update, in_reply_to_tweet_id=media_tweet.data['id'],
                                                 poll_options=key_passage_choices, poll_duration_minutes=359)
                last_tweet_id = poll_tweet.data['id']
            if len(key_passage_choices) > 4:
                # status_update = 'You ponder the many keys in your rucksack.'
                # all possible choices
                # [174, 186, 200, 219, 233, 231, 245, 276, 290, 288, 302, 321, 335, 347]
                # all_three_wrong_rooms = 200
                two_keys_wrong_rooms = [174, 186, 233, 245, 290, 302]
                one_key_wrong_rooms = [182, 219, 231, 276, 288, 335, 347]
                options = []
                two_keys_options = []
                one_key_options = []
                if 321 in key_passage_choices:
                    options.append(321)
                if 200 in key_passage_choices:
                    options.append(200)
                for each in key_passage_choices:
                    if each in two_keys_wrong_rooms:
                        two_keys_options.append(each)
                    if each in one_key_wrong_rooms:
                        one_key_options.append(each)
                if len(one_key_options) > 0:
                    one_key_room_addition = random.choice(one_key_options)
                    options.append(one_key_room_addition)
                if len(two_keys_options) > 0:
                    two_key_room_addition = random.choice(two_keys_options)
                    options.append(two_key_room_addition)
                if len(options) < 4:
                    done = 0
                    while len(options) < 4 and done == 0:
                        for each in key_passage_choices:
                            if each not in options:
                                options.append(each)
                        done = 1

                status_update = 'The ' \
                                'first combinations you think of are ' + \
                                str(options[0]) + ', ' + str(options[1])
                if len(options) >= 3:
                    status_update = status_update + ', ' + str(options[2])
                if len(options) >= 4:
                    status_update = status_update + ' and ' + str(options[3]) + '.'
                poll_update = 'But which one is correct?'
                media_tweet = create_media_tweet(room_entered, status_update)
                if len(options) > 4:
                    options = [str(options[0]), str(options[1]), str(options[2]), str(options[3])]
                poll_tweet = client.create_tweet(text=poll_update, in_reply_to_tweet_id=media_tweet.data['id'],
                                                 poll_options=options, poll_duration_minutes=359)
                last_tweet_id = poll_tweet.data['id']
        else:
            if len(keys) == 2:
                status_update = 'You ' \
                            'only have ' + str(len(keys)) + ' keys. In frustration you try to move the chest but ' \
                                                            'it is too heavy, no doubt filled to the brim with ' \
                                                            'great treasure. Your journey ends.'
                create_media_tweet(room_entered, status_update)
                set_current_room(0)
                initialize_game()
            if len(keys) == 1:
                status_update = 'You ' \
                            'only have ' + str(len(keys)) + ' key. In frustration you try to move the chest but ' \
                                                            'it is too heavy, no doubt filled to the brim with ' \
                                                            'great treasure. Your journey ends.'
                create_media_tweet(room_entered, status_update)
                set_current_room(0)
                initialize_game()
            if len(keys) == 0:
                status_update = 'You cannot even recall finding a key. ' \
                                'The chest is too heavy to move, laden down with treasure no doubt. Your journey ends.'
                create_media_tweet(room_entered, status_update)
                set_current_room(0)
                initialize_game()
    # winning
    if room_entered in [169, 192, 321, 400]:
        status_update = 'Congratulations! You have defeated the Warlock of Firetop Mountain!!!'
        create_media_tweet(room_entered, status_update)
        set_current_room(0)
        initialize_game()
    # test luck to not die
    if room_entered in [174, 186, 198, 233, 245, 290, 302]:
        status_update = ''
        luck_test = test_your_luck()
        if luck_test == 'lucky':
            lose_stamina(2, room_entered, '')
            status_update = "Your luck stings, but at least you're alive."
            set_current_room(139)
        if luck_test == 'unlucky':
            status_update = 'Your luck fails you, You have died.'
            set_current_room(0)
            initialize_game()
        create_media_tweet(room_entered, status_update)
    # lose 2 then you can re-try keys
    if room_entered in [182, 219, 231, 276, 288, 335, 347]:
        # status_update = ''
        lose_stamina(2, room_entered, '')
        status_update = 'You survive the acid, with ' + str(current_stamina) + ' stamina remaining.'
        create_media_tweet(room_entered, status_update)
    # all three keys wrong, you have died
    if room_entered in [200, 387]:
        status_update = 'None of the three keys work. You must delve into Firetop Mountain again...'
        create_media_tweet(room_entered, status_update)
        set_current_room(0)
        initialize_game()
    # with at least two keys enter, else lose 5 stamina and move on
    if room_entered in [382, 396]:
        # status_update = ''
        if len(keys) >= 2:
            status_update = 'You pull out two keys and open the door to passage 242.'
            create_media_tweet(room_entered, status_update)
            set_current_room(242)
        elif current_stamina < 5:
            status_update = 'You bang your fists against the door, ' \
                            'but with no keys and ' + str(current_stamina) + ' stamina, your quest is at an end.'
            create_media_tweet(room_entered, status_update)
            set_current_room(0)
            initialize_game()
        else:
            lose_stamina(5, room_entered, '')
            status_update = 'You bash through the door with immense effort. ' \
                            'You have ' + str(current_stamina) + ' stamina as you head to passage 242.'
            create_media_tweet(room_entered, status_update)
            set_current_room(242)


def create_luck_dependent_room(room_entered):
    global current_stamina
    global last_tweet_id
    next_passage_choice = 0
    status_update = ''
    options = lucky_room_choices[room_entered]
    luck_result = test_your_luck()
    # lucky defeats vampire unlucky hurts vampire and gets choices
    if room_entered == 17:
        if luck_result == 'lucky':
            status_update = ("You have slain the vampire! turn to passage " + str(options[0]))
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
        if luck_result == 'unlucky':
            status_update = "Unluckily, the vampire is still standing..."
            next_path_choices = [options[1], options[2]]
            media_tweet = create_media_tweet(room_entered, status_update)
            poll_tweet = client.create_tweet(text='Do you fight on?', in_reply_to_tweet_id=media_tweet.data['id'],
                                             poll_options=next_path_choices, poll_duration_minutes=359)
            last_tweet_id = poll_tweet.data['id']
    else:
        # normal test your luck then move to a new passage
        if room_entered in [2, 71, 74, 83, 92, 144, 389]:
            if luck_result == 'lucky':
                next_passage_choice = options[0]
                status_update = ("Your luck holds, continue to passage " + str(options[0]))
            if luck_result == 'unlucky':
                next_passage_choice = options[1]
                status_update = ("Your luck fails you, continue to passage " + str(options[1]))
        # unlucky lose one stamina and move to new passage, if lucky move to different passage
        if room_entered == 18:
            if luck_result == 'lucky':
                next_passage_choice = options[0]
                status_update = ("Your luck holds, continue to passage " + str(options[0]))
            if luck_result == 'unlucky':
                lose_stamina(1, room_entered, '')
                next_passage_choice = options[1]
                status_update = ("Your luck fails you, you take 1 stamina damage and continue "
                                 "to passage " + str(options[1]))
        # cheating at cards with dwarves, test luck and if you pass get some gold, fail and fight
        if room_entered == 91:
            if luck_result == 'lucky':
                next_passage_choice = options[0]
                gold_gained = (random.randint(1, 6) + random.randint(1, 6))
                gain_gold(gold_gained)
                status_update = ("Your luck holds, you gain " + str(gold_gained) + " gold and continue "
                                                                                   "to passage " + str(options[0]))
            if luck_result == 'unlucky':
                next_passage_choice = options[1]
                status_update = ("The Dwarves notice your cheating! Continue to passage " + str(options[1]))
        # test luck several times to not get hurt by rope
        if room_entered == 125:
            if luck_result == 'lucky':
                next_passage_choice = options[0]
                status_update = ("You cut the rope! Continue to passage " + str(options[0]))
            if luck_result == 'unlucky':
                lose_stamina(1, room_entered, '')
                status_update = "The rope tightens, hurting you!"
                while luck_result == 'unlucky':
                    luck_result = test_your_luck()
                    status_update = status_update + " It tightens!"
                    lose_stamina(1, status_update, '')
                status_update = ("You slice the rope, continuing to passage " + str(options[0]))
                next_passage_choice = options[0]
        # if lucky move to passage, if unlucky then take 1 damage and move to same passage
        if room_entered == 275:
            if luck_result == 'lucky':
                next_passage_choice = options[0]
                status_update = ("You deftly dodge, continue to passage " + str(options[0]) + '.')
            if luck_result == 'unlucky':
                lose_stamina(1, room_entered, '')
                status_update = ("The corpse lands a swipe, take a damage and continue to passage " + str(options[0]))
                next_passage_choice = options[0]
        # test luck three times, any failure means going to one passage, all three success is another passage
        if room_entered == 305:
            if luck_result == 'lucky':
                luck_result = test_your_luck()
                if luck_result == 'unlucky':
                    next_passage_choice = options[1]
                    status_update = ("You are grabbed by a hand! Continue to passage " + str(options[1]))
                if luck_result == 'lucky':
                    luck_result = test_your_luck()
                    if luck_result == 'unlucky':
                        next_passage_choice = options[1]
                        status_update = ("You are grabbed by a hand! Continue to passage " + str(options[1]))
                    if luck_result == 'lucky':
                        next_passage_choice = options[0]
                        status_update = ("Your luck holds, continue to passage " + str(options[0]) + '.')
            if luck_result == 'unlucky':
                next_passage_choice = options[1]
                status_update = ("You are grabbed by a hand! Continue to passage " + str(options[1]))
        # if lucky not dead, can try keys, unlucky equals death
        if room_entered == 379:
            if luck_result == 'lucky':
                next_passage_choice = options[0]
                status_update = ("A broken sword... but an intact body! Try the keys at passage " + str(options[0]))
            if luck_result == 'unlucky':
                you_have_died()
        create_media_tweet(room_entered, status_update)
        set_current_room(next_passage_choice)


def create_media_tweet(room_entered, tweet_status):
    global last_tweet_id
    media_id_list = []
    status_update = tweet_status
    path = Path("images/combined/" + str(room_entered) + '/')
    total_path = path / '*.JPG'
    for image in glob.glob(str(total_path)):
        uploaded_image = api.media_upload(image)
        media_id_list.append(uploaded_image.media_id)
    if room_entered in fight_dependent_rooms:
        uploaded_image = api.media_upload('fight_result.jpg')
        media_id_list.append(uploaded_image.media_id)
    media_tweet = client.create_tweet(text=status_update, media_ids=media_id_list)
    last_tweet_id = media_tweet.data['id']
    update_last_tweet_id()
    return media_tweet


def create_normal_room(room_entered):
    global chosen_difficulty
    global current_personality
    global potion_chosen
    global past_rooms
    global current_skill
    global current_stamina
    global current_luck
    global current_gold
    global current_provisions
    status_choices = ['Stay focused here.', 'Maybe you should turn back, before things get worse.',
                      'Contemplation, not hesitation.', 'This reminds you of a funny story.',
                      'You whistle a jaunty tune.', 'You whistle a light tune.', 'You feel a bit lost.',
                      'What next?', 'You count to ten, then ten again.', 'Emotions swell within you.',
                      'What a curious place.', ' ', 'You feel a sense of foreboding.',
                      'How long have you been down here?', 'How big is this place?', 'What a day!',
                      'Will this place be the end of you?', "It feels like there's a frog in your throat.",
                      'Things could be better, but they could certainly be much worse too.',
                      'Your thoughts turn briefly to your family.', "You're starting to regret coming here.",
                      'You have ' + str(current_stamina) + ' stamina.', 'You have ' + str(current_skill) + ' skill.',
                      'You have ' + str(current_luck) + ' luck.', 'You have ' + str(current_gold) + ' gold.',
                      'You have ' + str(current_provisions) + ' provisions.']
    poll_choices = ['This one feels extra important.', 'What would your deity do?', 'Which one is right?',
                    'Dizzy with choices, you clear your head and choose with determination.',
                    'You mentally toss a coin and choose.', 'It feels like the fates guide you towards your choice.',
                    'Easy money, obviously one is the right choice.', 'Hmm...',
                    'If I recall correctly...', 'Oh! I think I know this one!', 'What was the right choice again?',
                    'Which one is this?', 'Have you been here before?', 'You rack your brain for what to do.',
                    'No false moves here.', 'Did you write down what to do here?', 'Can you really...?']
    status_update = ''
    # poll_update = ''
    if room_entered == 1:
        status_update = 'You are a ' + str(current_personality) + ' with a ' + str(potion_chosen) + ' playing on ' + \
                        str(chosen_difficulty) + '. ' 'You steel your resolve, check all your ' \
                                                 'equipment and venture into the mountain.'
        poll_update = 'The first choice, perhaps the most important?'
    else:
        if room_entered == 66:
            lose_stamina(2, room_entered, '')
        if room_entered == 293:
            populate_past_rooms()
            if str(65) in past_rooms:
                lose_stamina(2, room_entered, '')
                status_update = status_update + ' You escape, but take 2 damage. You now have ' + \
                                                str(current_stamina) + ' stamina remaining.'
        status_update = status_update + random.choice(status_choices)
        poll_update = random.choice(poll_choices)
    create_poll_tweet(room_entered, status_update, poll_update)


def create_poll_tweet(room_entered, tweet_status, poll_status):
    global last_tweet_id
    next_path_choices = []
    media_tweet = create_media_tweet(room_entered, tweet_status)
    for each_room in room_choices[room_entered]:
        next_path_choices.append(str(each_room))
    poll_tweet = client.create_tweet(text=poll_status, in_reply_to_tweet_id=media_tweet.data['id'],
                                     poll_options=next_path_choices, poll_duration_minutes=359)
    last_tweet_id = poll_tweet.data['id']
    update_last_tweet_id()


def create_provisions_dependent_room(room_entered):
    global current_stamina
    global current_skill
    global current_luck
    global current_gold
    global current_provisions
    global initial_skill
    global items
    global keys
    global past_rooms
    status_update = ''
    options = provisions_room_choices[room_entered]
    # eat provisions then get at least two choices
    if room_entered in [10, 77, 106, 281]:
        hunger = check_to_eat()
        if hunger == 'hungry':
            eat_provisions()
            status_update = 'You eat some provisions. With ' + str(current_provisions) + ' left, you think about ' \
                                                                                         "what's next."
        if hunger == 'not hungry':
            baseline_stamina = initial_stamina - 4
            if current_provisions == 0:
                status_update = 'With no more food, you cannot eat. Your stomach rumbles.'
            elif current_stamina > baseline_stamina:
                status_update = "You're not hungry enough to eat. You have " + str(current_stamina) + ' stamina.'
        create_poll_tweet(room_entered, status_update, "where to?")
    # gain something, then choose to eat, then one passage forward
    if room_entered in [26, 31, 34, 101, 216, 258, 266, 327, 371, 374, 376, 388]:
        if room_entered in [26, 371]:
            modify_luck(3)
            status_update = status_update + 'You gain 3 luck! '
        if room_entered in [31]:
            modify_skill(2)
            status_update = status_update + 'You gain 2 skill! '
        if room_entered in [34]:
            items.append('mallet and chisel')
            modify_luck(2)
            status_update = status_update + 'You gain 2 luck! '
        if room_entered in [96, 374]:
            modify_luck(2)
            status_update = status_update + 'You gain 2 luck! '
        if room_entered in [101, 327]:
            modify_gold(30)
            items.append('book')
            items.append('Y-shaped stick')
            modify_luck(3)
            status_update = 'You collect the gold, book and stick, feeling 3 points luckier! '
        if room_entered in [135]:
            modify_gold(18)
            modify_luck(2)
            status_update = 'You gain the gold and feel lucky. '
        if room_entered in [216]:
            modify_stamina(4)
            modify_skill(50)
            modify_luck(50)
            status_update = 'You feel so refreshed! '
        if room_entered in [258]:
            modify_gold(8)
            keys.append(111)
            modify_luck(2)
            status_update = 'You take the gold, the red key, and smile at your (+2) luck. '
        if room_entered in [266]:
            modify_luck(1)
            items.append('bow with silver arrow')
            status_update = 'You take the bow and arrow, and gain one luck. '
        if room_entered in [376]:
            modify_gold(4)
            modify_luck(3)
            status_update = 'You gather the gold and feel 3 points luckier. '
        if room_entered in [388]:
            lose_stamina(1, room_entered, '')
            modify_skill(-1)
            status_update = 'The warlock cowers you! '
            if (7 > current_skill or (initial_skill - current_skill) > 3) and ('Potion of Skill' in items or 'Half '
                                                                                                             'Potion '
                                                                                                             'of '
                                                                                                             'Skill'
                                                                               in items):
                current_skill = initial_skill
                status_update = status_update + ' You quaff some of your ' \
                                                'potion of skill. You now have ' + str(current_skill) + ' skill.'
                if 'Potion of Skill' in items:
                    status_update = status_update + ' You have of measure of the potion left.'
                    items.remove('Potion of Skill')
                    items.append('Half Potion of Skill')
                elif 'Half Potion of Skill' in items:
                    status_update = status_update + 'you have used the last of your potion.'
                    items.remove('Half Potion of Skill')
        hunger = check_to_eat()
        if hunger == 'hungry':
            eat_provisions()
            status_update = status_update + 'You munch on some provisions. With ' \
                                            + str(current_provisions) + " left, you think about what's next."
        if hunger == 'not hungry':
            baseline_stamina = initial_stamina - 4
            if current_provisions == 0:
                status_update = status_update + 'With no more food, you cannot eat. Your stomach rumbles. You have ' \
                                + str(current_stamina) + 'stamina remaining.'
            elif current_stamina > baseline_stamina:
                status_update = status_update + "You're not hungry enough to eat. You have " \
                                + str(current_stamina) + ' stamina.'
        create_media_tweet(room_entered, status_update)
        set_current_room(options[0])
    # gain something, then choose to eat, then at least two choices
    if room_entered in [28, 390]:
        if room_entered in [28]:
            modify_luck(2)
            modify_skill(2)
            status_update = status_update + 'You gain 2 luck and 2 skill points! '
        if room_entered in [390]:
            modify_gold(1)
            if 294 not in past_rooms:
                modify_gold(5)
            modify_luck(2)
        hunger = check_to_eat()
        if hunger == 'hungry':
            eat_provisions()
            status_update = status_update + 'You munch on some provisions. With ' \
                                            + str(current_provisions) + " left, you think about what's next."
        if hunger == 'not hungry':
            baseline_stamina = initial_stamina - 4
            if current_provisions == 0:
                status_update = status_update + 'With no more food, you cannot eat. Your stomach rumbles. You have ' \
                                + str(current_stamina) + 'stamina remaining.'
            elif current_stamina > baseline_stamina:
                status_update = status_update + "You're not hungry enough to eat. You have " \
                                + str(current_stamina) + ' stamina.'
        create_poll_tweet(room_entered, status_update, 'where next?')
    # choose to eat, then one choice forward
    if room_entered in [45, 90, 131]:
        hunger = check_to_eat()
        if hunger == 'hungry':
            eat_provisions()
            if room_entered == 131:
                lose_stamina(2, room_entered, '')
            status_update = status_update + 'You munch on some provisions. With ' \
                                            + str(current_provisions) + " left, you think about what's next."
        if hunger == 'not hungry':
            baseline_stamina = initial_stamina - 4
            if current_provisions == 0:
                status_update = status_update + 'With no more food, you cannot eat. Your stomach rumbles. You have ' \
                                + str(current_stamina) + 'stamina remaining.'
            elif current_stamina > baseline_stamina:
                status_update = status_update + "You're not hungry enough to eat. You have " \
                                + str(current_stamina) + ' stamina.'
        create_media_tweet(room_entered, status_update)
        set_current_room(options[0])
    # eating provisions is a passage choice
    if room_entered in [69, 76, 136, 244, 351]:
        if current_provisions >= 1:
            status_update = 'You have enough provisions to eat. Your stamina is ' \
                            + str(current_stamina) + ' and your initial stamina is ' + str(initial_stamina) + '.'
            create_poll_tweet(room_entered, status_update, "will you sit and eat?")
        if current_provisions <= 0:
            status_update = 'You do not have enough to eat. You continue on...'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])


def create_random_fight_room(room_entered):
    # multiple choices after fighting 161
    if room_entered in [12]:
        # options = random_fight_room_choices[room_entered]
        monster = fight_room_161()
        status_update = 'You defeat the ' + monster + '!'
        create_poll_tweet(room_entered, status_update, 'Where to next?')
    # one choice after fighting 161
    if room_entered in [14, 161, 234, 295, 306]:
        options = random_fight_room_choices[room_entered]
        monster = fight_room_161()
        status_update = 'You defeat the ' + monster + ' and continue to passage ' + str(options[0]) + '.'
        create_media_tweet(room_entered, status_update)
        set_current_room(options[0])


def create_roll_a_die_room(room_entered):
    global current_stamina
    global current_skill
    global current_luck
    global initial_skill
    options = roll_a_die_room_choices[room_entered]
    # roll a die then go to one of multiple places
    if room_entered in [47, 123, 166, 195, 209, 298]:
        die_result = random.randint(1, 6)
        if room_entered in [47]:
            if die_result == 6:
                status_update = 'You fail to regain your balance... SPLASH!'
                create_media_tweet(room_entered, status_update)
                set_current_room(options[1])
            if die_result in [1, 2, 3, 4, 5]:
                status_update = 'You manage to stay steady, continue to passage ' + str(options[0]) + '.'
                create_media_tweet(room_entered, status_update)
                set_current_room(options[0])
        if room_entered in [123]:
            if die_result in [1, 2, 3]:
                modify_luck(2)
                status_update = 'They believe you! Gain 2 luck and go to passage ' + str(options[0]) + '.'
                create_media_tweet(room_entered, status_update)
                set_current_room(options[0])
            if die_result in [4, 5]:
                status_update = 'Two skeletons shuffle off, head to passage ' + str(options[1]) + '.'
                create_media_tweet(room_entered, status_update)
                set_current_room(options[1])
            if die_result == 6:
                status_update = "they don't buy your bluff and are advancing! Turn to passage " + str(options[2])
                create_media_tweet(room_entered, status_update)
                set_current_room(options[2])
        if room_entered in [166]:
            if die_result in [5, 6]:
                status_update = 'You roll a ' + str(die_result) + \
                                '. You have attracted something, turn to passage ' + str(options[1])
                create_media_tweet(room_entered, status_update)
                set_current_room(options[1])
            if die_result in [1, 2, 3, 4]:
                status_update = 'You roll a ' + str(die_result) + ' and make it ' \
                                                                  'to shore, turn to passage ' + str(options[0]) + '.'
                create_media_tweet(room_entered, status_update)
                set_current_room(options[0])
        if room_entered in [195]:
            if die_result in [5, 6]:
                modify_luck(2)
                status_update = 'They believe you! Gain 2 luck and go to passage ' + str(options[2]) + '.'
                create_media_tweet(room_entered, status_update)
                set_current_room(options[2])
            if die_result in [3, 4]:
                status_update = 'Two skeletons shuffle off, head to passage ' + str(options[1]) + '.'
                create_media_tweet(room_entered, status_update)
                set_current_room(options[1])
            if die_result in [1, 2]:
                status_update = "they don't buy your bluff and are advancing! Turn to passage " + str(options[0])
                create_media_tweet(room_entered, status_update)
                set_current_room(options[0])
        if room_entered in [209, 298]:
            if die_result == 6:
                status_update = "You roll a six! You splash into passage " + str(options[1])
                create_media_tweet(room_entered, status_update)
                set_current_room(options[1])
            if die_result in [1, 2, 3, 4, 5]:
                status_update = "You roll a " + str(die_result) + '. Continue across the bridge to ' + str(options[0])
                create_media_tweet(room_entered, status_update)
                set_current_room(options[0])
    # roll two dice, can lose stamina or not depending on room
    if room_entered in [53, 213]:
        dice_result = (random.randint(1, 6) + random.randint(1, 6))
        if dice_result <= current_skill:
            status_update = 'You rolled a ' + str(dice_result) + ' and burst through the door.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
        if dice_result > current_skill:
            status_update = 'You rolled a ' + str(dice_result) + ' and bruise your ' \
                                                                 'shoulder. Continue to passage ' + str(options[1])
            lose_stamina(1, room_entered, '')
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
    # test luck and stamina, no penalty
    if room_entered in [55]:
        dice_result = (random.randint(1, 6) + random.randint(1, 6))
        if dice_result <= current_luck and dice_result <= current_stamina:
            status_update = 'You roll a ' + str(dice_result) + \
                            ' and hold on to the raft. Move to passage ' + str(options[0]) + '.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
        if dice_result > current_luck or dice_result > current_stamina:
            status_update = 'The dice were not kind, rolling a ' + str(dice_result) + ' you are flung from the raft.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
    # test skill then one of two passages
    if room_entered in [156, 361]:
        dice_result = (random.randint(1, 6) + random.randint(1, 6))
        if room_entered == 156:
            if dice_result <= current_skill:
                status_update = 'You bash through the door with a ' \
                                'roll of ' + str(dice_result) + '! Enter the room at passage ' + str(options[0])
                create_media_tweet(room_entered, status_update)
                set_current_room(options[0])
            if dice_result > current_skill:
                status_update = 'You fail to bash through, ' \
                                'rolling a ' + str(dice_result) + '. Continue at passage ' + str(options[1])
                create_media_tweet(room_entered, status_update)
                set_current_room(options[1])
        if room_entered == 361:
            keys.append(125)
            if dice_result <= current_skill:
                status_update = 'You hold your breath with a ' \
                                'roll of ' + str(dice_result) + '! Dart across to passage ' + str(options[0])
                create_media_tweet(room_entered, status_update)
                set_current_room(options[0])
            if dice_result > current_skill:
                modify_skill(-2)
                lose_stamina(3, room_entered, '')
                status_update = 'You hack and cough, ' \
                                'rolling a ' + str(dice_result) + '. Gasp for air at passage ' + str(options[0])
                if (7 > current_skill or (initial_skill - current_skill) > 3) and (
                        'Potion of Skill' in items or 'Half Potion of Skill' in items):
                    current_skill = initial_skill
                    status_update = status_update + ' You quaff some of your ' \
                                                    'potion of skill. You now have ' + str(current_skill) + ' skill.'
                    if 'Potion of Skill' in items:
                        status_update = status_update + ' You have of measure of the potion left.'
                        items.remove('Potion of Skill')
                        items.append('Half Potion of Skill')
                    elif 'Half Potion of Skill' in items:
                        status_update = status_update + 'you have used the last of your potion.'
                        items.remove('Half Potion of Skill')
                create_media_tweet(room_entered, status_update)
                set_current_room(options[0])
    # odds or evens
    if room_entered in [243]:
        die_result = random.randint(1, 6)
        if die_result in [1, 3, 5]:
            modify_skill(-3)
            lose_stamina(1, room_entered, '')
            status_update = 'Ouch! Your sword hand is badly cut. You now' \
                            ' have ' + str(current_stamina) + ' stamina and ' + str(current_skill) + ' skill.'
            if (7 > current_skill or (initial_skill - current_skill) > 3) and ('Potion of Skill' in items or 'Half '
                                                                                                             'Potion '
                                                                                                             'of '
                                                                                                             'Skill'
                                                                               in items):
                current_skill = initial_skill
                status_update = status_update + ' You quaff some of your ' \
                                                'potion of skill. You now have ' + str(current_skill) + ' skill.'
                if 'Potion of Skill' in items:
                    status_update = status_update + ' You have of measure of the potion left.'
                    items.remove('Potion of Skill')
                    items.append('Half Potion of Skill')
                elif 'Half Potion of Skill' in items:
                    status_update = status_update + 'you have used the last of your potion.'
                    items.remove('Half Potion of Skill')
            poll_status = 'Where to next?'
            create_poll_tweet(room_entered, status_update, poll_status)
        if die_result in [2, 4, 6]:
            modify_skill(-1)
            lose_stamina(2, room_entered, '')
            status_update = 'Oof, you slice open your off hand. You now' \
                            ' have ' + str(current_stamina) + ' stamina and ' + str(current_skill) + ' skill.'
            if (7 > current_skill or (initial_skill - current_skill) > 3) and ('Potion of Skill' in items or 'Half '
                                                                                                             'Potion '
                                                                                                             'of '
                                                                                                             'Skill'
                                                                               in items):
                current_skill = initial_skill
                status_update = status_update + ' You quaff some of your ' \
                                                'potion of skill. You now have ' + str(current_skill) + ' skill.'
                if 'Potion of Skill' in items:
                    status_update = status_update + ' You have of measure of the potion left.'
                    items.remove('Potion of Skill')
                    items.append('Half Potion of Skill')
                elif 'Half Potion of Skill' in items:
                    status_update = status_update + 'you have used the last of your potion.'
                    items.remove('Half Potion of Skill')
            poll_status = 'Where to next?'
            create_poll_tweet(room_entered, status_update, poll_status)
    # test stamina, two passages and a provisions choice
    if room_entered in [316]:
        dice_result = (random.randint(1, 6) + random.randint(1, 6))
        if dice_result <= current_stamina:
            status_update = 'You think you can make it with a ' \
                            'roll of ' + str(dice_result) + '. Swim to passage ' + str(options[0]) + '.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
        if dice_result > current_skill:
            status_update = 'Your strength wavers, ' \
                            'rolling a ' + str(dice_result) + '. You return to shore.'
            hunger = check_to_eat()
            if hunger == 'hungry':
                status_update = status_update + ' You decide to eat.'
                eat_provisions()
            if hunger == 'not hungry':
                status_update = status_update + " You're not hungry."
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
    # roll a die, lose stamina then go to a passage
    if room_entered in [339]:
        die_result = random.randint(1, 6)
        lose_stamina(die_result, room_entered, '')
        status_update = 'Ouch! You lose ' + str(die_result) + ' stamina.'
        create_media_tweet(room_entered, status_update)
        set_current_room(options[0])


def create_special_passage_room(room_entered):
    global current_skill
    global current_stamina
    global current_luck
    global initial_skill
    global initial_stamina
    global items
    global current_gold
    global past_rooms
    global current_provisions
    global last_tweet_id
    global fight_text
    options = room_choices[room_entered]
    status_update = ''
    # poll_status = ''
    # gain 2 stamina and 1 skill, then a poll
    if room_entered in [11]:
        modify_stamina(2)
        modify_skill(1)
        status_update = 'You now have ' + str(current_stamina) + ' stamina and ' + str(current_skill) + ' skill.'
        poll_status = 'North or south?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain two extra stamina by eating and 1 skill then a poll
    if room_entered in [15]:
        hunger_check = check_to_eat()
        if hunger_check == 'hungry':
            eat_provisions()
            modify_stamina(2)
            modify_skill(1)
            status_update = 'You relax your shoulders and rest a moment. You now have ' \
                            + str(current_stamina) + ' stamina and ' + str(current_skill) + ' skill.'
        if hunger_check == 'not hungry':
            modify_skill(1)
            status_update = 'You choose not to tarry, so you head on with ' \
                            + str(current_stamina) + ' stamina and ' + str(current_skill) + ' skill.'
        poll_status = 'You collect your things and head off to the west... or was it the east?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # room 24 updates you that the wight has drained a skill point and allows a choice to flee
    if room_entered in [24]:
        # wight_skill = int(room_monster_dictionary[get_current_room()][0])
        wight_stamina = int(room_monster_dictionary[get_current_room()][1])
        # wight_name = room_monster_dictionary[get_current_room()][2]
        modify_skill(-1)
        if (7 > current_skill or (initial_skill - current_skill) > 3) and (
                'Potion of Skill' in items or 'Half Potion of Skill' in items):
            current_skill = initial_skill
            status_update = status_update + ' You quaff some of your ' \
                                            'potion of skill. You now have ' + str(current_skill) + ' skill.'
            if 'Potion of Skill' in items:
                status_update = status_update + ' You have of measure of the potion left.'
                items.remove('Potion of Skill')
                items.append('Half Potion of Skill')
            elif 'Half Potion of Skill' in items:
                status_update = status_update + 'you have used the last of your potion.'
                items.remove('Half Potion of Skill')
        if current_stamina <= 2:
            status_update = status_update + 'You cannot flee with only ' + str(current_stamina) + ' stamina.'
        while current_stamina > 0 and wight_stamina > 0:
            fight_addtl_wight_rounds()
        if current_stamina > 0:
            status_update = status_update + ' You defeated the wight. You now have ' \
                                            + str(current_stamina) + ' stamina and ' + str(current_skill) + ' skill.'
            generate_combat_log_image()
            create_media_tweet(room_entered, status_update)
            set_current_room(135)
    # lose one skill, then choose between escaping and going to another passage
    if room_entered in [25]:
        current_skill -= 1
        status_update = 'You lose one skill point, you now have ' + str(current_skill) + '. '
        if current_stamina <= 2:
            status_update = status_update + 'You cannot afford to escape, with only ' + \
                            str(current_stamina) + ' stamina.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
        else:
            status_update = status_update + 'You consider the items in your rucksack and your ' + \
                            str(current_stamina) + ' stamina.'
            poll_status = 'Will you escape or search your pack?'
            create_poll_tweet(room_entered, status_update, poll_status)
    # gain magic sword and move to certain passage
    if room_entered in [27]:
        items.append('enchanted sword')
        if 'sword' in items:
            items.remove('sword')
        if 'magic sword' in items:
            items.remove('magic sword')
            modify_skill(-2)
        modify_luck(2)
        initial_skill += 2
        modify_skill(2)
        status_update = 'You take the enchanted sword and leave your plain sword.'
        enter_passage_two_two_one('enchanted sword', status_update)
    # lose cheese, add 2 luck, then a poll
    if room_entered in [32]:
        modify_luck(2)
        items.remove('a piece of cheese')
        status_update = 'Such hungry rats! You count your blessings that you found that cheese, ' \
                        'and feel ' + str(current_luck) + ' lucky.'
        poll_status = 'Having escaped the rats, where will you go next?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain 2 provisions then a poll
    if room_entered in [38]:
        current_provisions += 2
        if current_provisions > 10:
            current_provisions = 10
        status_update = 'You store the eggs. You now have ' + str(current_provisions) + ' provisions.'
        poll_status = 'Go to the middle of the rockface (104), or eastward along the riverbank (99) next?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # reduce skill by 1, then poll tweet
    if room_entered in [40]:
        modify_skill(-1)
        status_update = 'Your skill is dropped to ' + str(current_skill) + ' as you search for an exit.'
        if (7 > current_skill or (initial_skill - current_skill) > 3) and (
                'Potion of Skill' in items or 'Half Potion of Skill' in items):
            current_skill = initial_skill
            status_update = status_update + ' You quaff some of your ' \
                                            'potion of skill. You now have ' + str(current_skill) + ' skill.'
            if 'Potion of Skill' in items:
                status_update = status_update + ' You have of measure of the potion left.'
                items.remove('Potion of Skill')
                items.append('Half Potion of Skill')
            elif 'Half Potion of Skill' in items:
                status_update = status_update + 'you have used the last of your potion.'
                items.remove('Half Potion of Skill')
        poll_status = 'You eventually find an exit, where does it leave?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # finish eating provisions then a poll
    if room_entered in [44]:
        eat_provisions()
        status_update = 'Killing sandworms is hungry business. You restore up to ' + str(current_stamina) + ' stamina.'
        poll_status = 'How will you attempt to cross the river?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # lose 2 stamina then a poll
    if room_entered in [49, 104]:
        lose_stamina(2, room_entered, '')
        if current_stamina > 0:
            status_update = 'You now have ' + str(current_stamina) + " stamina."
            poll_status = 'How best to approach these undead?'
            create_poll_tweet(room_entered, status_update, poll_status)
    # gain bronze key 9 then a poll
    if room_entered in [50]:
        keys.append(9)
        status_update = 'It is a lovely key, numbered 9... but what does it mean?'
        poll_status = 'Is north (77) the path forward, or does west (63) hold more promise?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain 2 luck then move to a certain passage
    if room_entered in [51]:
        modify_luck(2)
        status_update = 'You feel a bit more lucky. In fact, you feel exactly ' + str(current_luck) + ' lucky.'
        create_media_tweet(room_entered, status_update)
        set_current_room(options[0])
    # crossroads at passage 52
    if room_entered in [52, 133]:
        status_update = 'You see a scrawling on the wall: (Do not trust ' \
                        'secret passages to the north). You heed this warning, and ' \
                        'decide not to investigate passage 234.'
        poll_status = 'That narrows things down... a bit.'
        create_poll_tweet(room_entered, status_update, poll_status)
    # lose regular sword then a poll
    if room_entered in [56]:
        items.remove('sword')
        status_update = 'It would be silly to keep two swords anyway!'
        poll_status = 'How best to cross the river?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # potential to fight, then fight or escape
    if room_entered in [65]:
        if current_stamina <= 2:
            status_update = status_update + 'You cannot afford to escape, with only ' + \
                            str(current_stamina) + ' stamina.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
        else:
            status_update = status_update + 'You reconsider your surroundings.'
            poll_status = 'Will you escape or stand and fight?'
            create_poll_tweet(room_entered, status_update, poll_status)
    # get armour then go to passage 319
    if room_entered in [72]:
        if 'armour' in items:
            status_update = 'This armour is no better than your current armour.'
        else:
            status_update = 'You don the fresh armour.'
        items.append('fresh armour')
        enter_passage_two_two_one('fresh armour', status_update)
    # gain key 111 and such then fight barbarian
    if room_entered in [75]:
        keys.append(111)
        gain_gold(50)
        status_update = 'You stow away the key marked 111 and the jewel, you now have ' + str(current_gold) + ' gold. '
        hunger_check = check_to_eat()
        if hunger_check == 'hungry':
            eat_provisions()
            status_update = status_update + 'You take a moment to eat. ' \
                                            'You now have ' + str(current_stamina) + ' stamina.'
        else:
            status_update = 'You decide not to eat, you have ' + str(current_stamina) + ' stamina.'
        modify_luck(3)
        status_update = status_update + ' You now have ' + str(current_luck) + ' luck.'
        enemy_list = pull_monsters(room_entered)
        for monster in enemy_list:
            result = fight_monster(monster)
            status_update = status_update + result
        if current_stamina > 0:
            generate_combat_log_image()
            create_media_tweet(room_entered, status_update)
            set_current_room(fight_room_choices[room_entered][0])
    # poll one thing or test your luck
    if room_entered in [82]:
        status_update = 'Could the box be worth it? You have ' + str(current_luck) + ' luck.'
        poll_status = 'Leave the room, or test your luck?'
        special_room_choices = ['208', 'Test your luck!']
        media_tweet = create_media_tweet(room_entered, status_update)
        poll_tweet = client.create_tweet(text=poll_status, in_reply_to_tweet_id=media_tweet.data['id'],
                                         poll_options=special_room_choices, poll_duration_minutes=359)
        last_tweet_id = poll_tweet.data['id']
    # passage 109 has holy water and such
    if room_entered in [109, 369]:
        modify_luck(4)
        status_update = 'You gain luck up to ' + str(current_luck) + ' total luck.'
        if current_stamina < (initial_stamina - 2):
            addition_result = (initial_stamina - 2) - current_stamina
            modify_stamina(addition_result)
            status_update = status_update + ' You regain ' + str(addition_result) + ' stamina.'
        else:
            status_update = status_update + ' You already have ' + str(current_stamina) + ' so you do not heal.'
        if current_skill < (initial_skill - 1):
            addition_result = (initial_skill - 1) - current_skill
            modify_skill(addition_result)
            status_update = status_update + ' You regain ' + str(addition_result) + ' skill.'
        else:
            status_update = status_update + ' You already have ' + str(current_skill) + ' so you do not gain any.'
        if 'maze parchment' in items:
            status_update = status_update + ' You already have the Maze Map so you head ' \
                                            'to passage ' + str(options[0]) + '.'
            create_media_tweet(room_entered, status_update)
        else:
            poll_status = 'You may look at the parchment or move to passage ' + str(options[0]) + '.'
            create_poll_tweet(room_entered, status_update, poll_status)
    # gain ten gold then go to passage 319
    if room_entered in [110]:
        gain_gold(10)
        status_update = 'You eagerly collect the gold. You now have ' + str(current_gold) + ' gold.'
        items.append('boot gold')
        enter_passage_two_two_one('boot gold', status_update)
    # build a list of items you can throw
    if room_entered in [119]:
        if len(items) == 0:
            if current_gold >= 1:
                status_update = 'you have no suitable items, so you toss a gold.'
                modify_gold(-1)
            if current_gold <= 0:
                status_update = "you haven't any gold or items, by GM fiat you find a suitable rock."
            create_media_tweet(room_entered, status_update)
            set_current_room(269)
        elif len(items) > 4:
            throwables = []
            while len(throwables) < 4:
                given_item = random.choice(items)
                if given_item not in throwables:
                    throwables.append(given_item)
            status_update = 'You scramble and pull out the first four items from your rucksack.'
            poll_status = 'Choose between the ' + throwables[0] + ', the ' + \
                          throwables[1] + ', the ' + throwables[2] + ' and the ' + throwables[3] + '.'
            media_tweet = create_media_tweet(room_entered, status_update)
            poll_tweet = client.create_tweet(text=poll_status, in_reply_to_tweet_id=media_tweet.data['id'],
                                             poll_options=throwables, poll_duration_minutes=359)
            last_tweet_id = poll_tweet.data['id']
        elif len(items) <= 4:
            throwables = items
            status_update = 'You scramble and pull out some items from your rucksack.'
            poll_status = 'Choose between the following:'
            media_tweet = create_media_tweet(room_entered, status_update)
            poll_tweet = client.create_tweet(text=poll_status, in_reply_to_tweet_id=media_tweet.data['id'],
                                             poll_options=throwables, poll_duration_minutes=359)
            last_tweet_id = poll_tweet.data['id']
    # lose two stamina then move to a certain passage
    if room_entered in [129, 247]:
        lose_stamina(2, room_entered, '')
        if current_stamina > 0:
            if room_entered in [129]:
                status_update = 'Ouch, you feel yourself fading into unconsciousness. ' \
                                'Your current stamina is ' + str(current_stamina) + '.'
                create_media_tweet(room_entered, status_update)
                set_current_room(122)
            if room_entered in [247]:
                status_update = 'Your current stamina is ' + str(current_stamina) + '.'
                create_media_tweet(room_entered, status_update)
                set_current_room(292)
    # gamble with an old man and then maybe win prizes
    if room_entered in [130]:
        # gamble gold and if you win then get skill stamina and luck
        bet = random.randint(1, current_gold)
        player_result = (random.randint(1, 6) + random.randint(1, 6))
        gambler_result = (random.randint(1, 6) + random.randint(1, 6))
        if player_result > gambler_result:
            gain_gold(bet)
            status_update = 'You bet ' + str(bet) + ' gold and won! You now have ' + str(current_gold) + ' gold.'
            modify_skill(2)
            modify_stamina(2)
            modify_luck(2)
            status_update = status_update + ' You gain up to ' + str(current_skill) + \
                                            ' skill, ' + str(current_stamina) + ' stamina and ' + \
                                            str(current_luck) + ' luck.'
        elif player_result < gambler_result:
            modify_gold(-1)
            status_update = 'You bet one gold, and lost! You now have ' + str(current_gold) + ' gold.'
        elif player_result == gambler_result:
            status_update = 'Your bet was ' + str(bet) + \
                            ' gold but you both rolled a ' + str(player_result) + '! You wisely decide to leave.'
        create_media_tweet(room_entered, status_update)
        set_current_room(280)
    # gain shield if you want it or whatever.
    if room_entered in [132]:
        if 'shield' in items:
            status_update = 'This shield is no better than your current one, so you leave it.'
        else:
            status_update = 'You take the shield and stop a moment, adjusting to the weight.'
        items.append('wooden shield')
        enter_passage_two_two_one('wooden shield', status_update)
    # gain one luck and a key, then a poll
    if room_entered in [145]:
        keys.append(99)
        modify_luck(1)
        status_update = 'A bronze key, what does the number inscribed mean? ' \
                        'At any rate, you have ' + str(current_luck) + ' luck.'
        poll_status = 'Is it worth investigating such a terrible noise?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain 1 gold and two luck then a poll
    if room_entered in [147]:
        gain_gold(1)
        modify_luck(2)
        status_update = "Mother always said it's lucky to let a mouse go... unless it's in the larder."
        poll_status = 'You now have ' + str(current_luck) + ' luck. Will you continue on, or try the door?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # one choice leads to -1 stamina just a normal poll otherwise, does not account for stamina loss right now!!!
    if room_entered in [151]:
        status_update = 'The turbulence, the reptilian eyes, or back to the safety of shore.'
        poll_status = 'Which will you choose?'
        options = ['218', '86', '158']
        media_tweet = create_media_tweet(room_entered, status_update)
        poll_tweet = client.create_tweet(text=poll_status, in_reply_to_tweet_id=media_tweet.data['id'],
                                         poll_options=options, poll_duration_minutes=359)
        last_tweet_id = poll_tweet.data['id']
    # lose new magic sword, lose 1 stamina, continue on
    if room_entered in [153]:
        items.remove('magic sword')
        initial_skill -= 2
        modify_skill(0)
        lose_stamina(1, room_entered, '')
        status_update = 'That stings! Nothing to do now but continue to passage ' \
                        + str(options[0]) + ' with ' + str(current_stamina) + 'stamina remaining.'
        create_media_tweet(room_entered, status_update)
        set_current_room(399)
    # gain iron shield, run a poll
    if room_entered in [155]:
        items.append('magic shield')
        status_update = 'You take a moment and admire your new shield.'
        poll_status = 'Screaming, could someone need your help?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # poll, then if trying to leave you must test luck
    if room_entered in [159]:
        # current_choices = ['attack', 'sneak out']
        status_update = 'Stay and fight, or try to sneak away? You current luck is ' + str(current_luck) + '.'
        poll_status = 'Can you take them on ' \
                      'with ' + str(current_skill) + ' skill and ' + str(current_stamina) + ' stamina?'
        media_tweet = create_media_tweet(room_entered, status_update)
        options = ['365', '237', '365']
        poll_tweet = client.create_tweet(text=poll_status, in_reply_to_tweet_id=media_tweet.data['id'],
                                         poll_options=options, poll_duration_minutes=359)
        last_tweet_id = poll_tweet.data['id']
    # test luck, maybe losing 1 stamina, then a fight with a giant
    if room_entered in [163]:
        luck_result = test_your_luck()
        if luck_result == 'lucky':
            status_update = 'You deftly dodge the giants meal. '
        if luck_result == 'unlucky':
            status_update = 'You are clipped by a pig hoof! '
            lose_stamina(1, room_entered, '')
        if current_stamina > 0:
            fight_result = fight_monster(room_monster_dictionary[room_entered][0])
            status_update = status_update + fight_result
            create_media_tweet(room_entered, status_update)
    # gain crucifix and 4 gold then go to passage 319
    if room_entered in [170]:
        gain_gold(4)
        status_update = 'You pocket the crucifix. You now have ' + str(current_gold) + ' gold.'
        items.append('crucifix')
        enter_passage_two_two_one('crucifix', status_update)
    # wight fight sucks annoying
    if room_entered in [173]:
        status_update = ''
        if 'bow and arrow' in items:
            luck_test = test_your_luck()
            status_update = 'You loose the arrow at the foul creature '
            if luck_test == 'lucky':
                status_update = status_update + 'and destroy the wight! You now have ' + str(current_luck) + ' luck.'
                create_media_tweet(room_entered, status_update)
                set_current_room(135)
            else:
                status_update = status_update + 'but miss! You now have ' + str(current_luck) + ' luck.'
                if 'crucifix' in items:
                    status_update = status_update + ' You find the silver crucifix and engage with the monster.'
                    fight_wight(status_update)
    # you chose wrong and the wailing causes -1 skill then a new poll
    if room_entered in [181, 355]:
        modify_skill(-1)
        status_update = 'Your skill is dropped to ' + str(current_skill) + ' as you search for an exit.'
        if (7 > current_skill or (initial_skill - current_skill) > 3) and (
                'Potion of Skill' in items or 'Half Potion of Skill' in items):
            current_skill = initial_skill
            status_update = status_update + ' You quaff some of your ' \
                                            'potion of skill. You now have ' + str(current_skill) + ' skill.'
            if 'Potion of Skill' in items:
                status_update = status_update + ' You have of measure of the potion left.'
                items.remove('Potion of Skill')
                items.append('Half Potion of Skill')
            elif 'Half Potion of Skill' in items:
                status_update = status_update + 'you have used the last of your potion.'
                items.remove('Half Potion of Skill')
        poll_status = 'You eventually find another path, where does it lead?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # add 1 skill 5 stamina then a poll
    if room_entered in [183]:
        modify_skill(1)
        modify_stamina(5)
        status_update = 'You wipe the sweat from your brow, ' \
                        'you have ' + str(current_skill) + ' skill and ' + str(current_stamina) + ' stamina.'
        poll_status = 'Open the case, or leave?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain two luck then a poll
    if room_entered in [185]:
        modify_luck(2)
        status_update = 'You gain luck up to ' + str(current_luck) + ' total.'
        poll_status = 'North or west?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain 5 gold then a poll
    if room_entered in [196]:
        gain_gold(5)
        status_update = 'You now have ' + str(current_gold) + ' gold pieces.'
        poll_status = 'How best to cross the room?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain gold and the invis potion, and may eat, then a poll
    if room_entered in [201]:
        gain_gold(25)
        items.append('potion of invisibility')
        hunger_result = check_to_eat()
        if hunger_result == 'hungry':
            eat_provisions()
            status_update = 'You eat some rations, bringing your stamina to ' + str(current_stamina) + '. You have ' \
                            + str(current_provisions) + ' provisions remaining.'
            poll_status = 'To the north, or eastwards?'
        else:
            status_update = "You aren't hungry enough to eat. You have " + str(current_stamina) + 'stamina and ' \
                            + str(current_provisions) + ' provisions remaining.' + " You stow your new potion. "
            poll_status = 'Which direction do you feel in your bones?'
        status_update = status_update + 'You now have ' + str(current_gold) + ' gold.'
        create_poll_tweet(room_entered, status_update, poll_status)
    # lose 1 skill for a shitty helmet then a poll
    if room_entered in [202]:
        modify_skill(-1)
        status_update = 'Your head is pounding, you now have ' + str(current_skill) + ' skill.'
        if (7 > current_skill or (initial_skill - current_skill) > 3) and (
                'Potion of Skill' in items or 'Half Potion of Skill' in items):
            current_skill = initial_skill
            status_update = status_update + ' You quaff some of your ' \
                                            'potion of skill. You now have ' + str(current_skill) + ' skill.'
            if 'Potion of Skill' in items:
                status_update = status_update + ' You have of measure of the potion left.'
                items.remove('Potion of Skill')
                items.append('Half Potion of Skill')
            elif 'Half Potion of Skill' in items:
                status_update = status_update + 'you have used the last of your potion.'
                items.remove('Half Potion of Skill')
        poll_status = 'The helmet eases its grip on you, just in time to find yourself at a junction.'
        create_poll_tweet(room_entered, status_update, poll_status)
    # add 1 luck, maybe eat provisions, take boat house keys then poll
    if room_entered in [203]:
        modify_luck(1)
        eating_test = check_to_eat()
        if eating_test == 'hungry':
            eat_provisions()
            status_update = 'You rest for a moment and eat some provisions. '
        if eating_test == 'not hungry':
            status_update = 'You choose not to eat some provisions. '
        items.append('boat keys')
        poll_status = 'West, or South?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # if you've been to this room before, go to one passage, else go to another.
    if room_entered in [206]:
        if room_entered in past_rooms:
            status_update = 'You HAVE been here before...'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
        else:
            status_update = "You haven't been here before."
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
    # more wight fight stuff, what a pain
    if room_entered in [211, 310]:
        fight_result = fight_round_with_monster('wight', 9)
        if fight_result == 'monster win':
            lose_stamina(2, room_entered, status_update)
            status_update = 'You cannot dodge the wight, it reduces your stamina to ' + str(current_stamina) + '. '
        if 'crucifix' in items:
            status_update = status_update + 'You have a crucifix made of silver, maybe that will do the trick!'
            create_media_tweet(room_entered, status_update)
            set_current_room(173)
        else:
            status_update = status_update + ' With no silver weapons to use, you beat a hasty retreat to passage 360.'
            lose_stamina(2, room_entered, status_update)
            status_update = status_update + ' You now have ' + str(current_stamina) + ' stamina.'
            create_media_tweet(room_entered, status_update)
            set_current_room(360)
    # if you haven't tested liquid, give a poll, else just move to certain passage
    if room_entered in [212]:
        if 369 in past_rooms:
            status_update = 'You continue to passage 120.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
        else:
            status_update = 'You consider whether to test the strange liquid.'
            poll_status = 'Which passage is next?'
            create_poll_tweet(room_entered, status_update, poll_status)
    # room 221 lets you look over certain items.
    if room_entered in [221]:
        poll_dictionary = {'fresh armour': 72, 'wooden shield': 132, 'enchanted sword': 27,
                           'boot gold': 110, 'crucifix': 170}
        poll_list = []
        for each in poll_dictionary:
            if each not in items:
                poll_list.append(poll_dictionary[each])
        status_update = 'You have made your first choice, now choose a second item.'
        poll_status = 'Which passage next?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # dwarf room, 4 choices but only if you haven't been there before
    if room_entered in [227]:
        if room_entered in past_rooms:
            status_update = 'The room is eerily void. You move on to passage 291.'
            create_media_tweet(room_entered, status_update)
            set_current_room(291)
        else:
            status_update = ''
            poll_status = 'How should you handle this situation?'
            create_poll_tweet(room_entered, status_update, poll_status)
    # add one luck, then get a poll
    if room_entered in [239]:
        modify_luck(1)
        status_update = 'You now have ' + str(current_luck) + ' luck.'
        poll_status = 'Leave through the door or stay and investigate?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # lose one skill and drop the stake, then go to another passage
    if room_entered in [241]:
        modify_skill(-1)
        items.remove('stake')
        status_update = 'You now have ' + str(current_skill) + ' skill and no stakes.'
        if (7 > current_skill or (initial_skill - current_skill) > 3) and (
                'Potion of Skill' in items or 'Half Potion of Skill' in items):
            current_skill = initial_skill
            status_update = status_update + ' You quaff some of your ' \
                                            'potion of skill. You now have ' + str(current_skill) + ' skill.'
            if 'Potion of Skill' in items:
                status_update = status_update + ' You have of measure of the potion left.'
                items.remove('Potion of Skill')
                items.append('Half Potion of Skill')
            elif 'Half Potion of Skill' in items:
                status_update = status_update + 'you have used the last of your potion.'
                items.remove('Half Potion of Skill')
        create_media_tweet(room_entered, status_update)
        set_current_room(90)
    # gain 1 skill 2 luck then a poll
    if room_entered in [259]:
        modify_skill(1)
        modify_luck(2)
        status_update = 'You now have ' + str(current_skill) + ' skill and ' + str(current_luck) + ' luck.'
        poll_status = 'Follow the riverbank? Or... maybe the door straight ahead?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain 1 luck, then a poll
    if room_entered in [263]:
        modify_luck(1)
        status_update = 'You try to commit what the old man says to your memory. You have ' + str(current_luck) + \
                        ' luck.'
        poll_status = 'A suspicious door, but is it safe?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # lose a skill, then an item dependent passage situation
    if room_entered in [264]:
        modify_skill(-1)
        status_update = 'Oof! That bruise will last a long while. Your skill is now ' + str(current_skill) + '.'
        if (7 > current_skill or (initial_skill - current_skill) > 3) and (
                'Potion of Skill' in items or 'Half Potion of Skill' in items):
            current_skill = initial_skill
            status_update = status_update + ' You quaff some of your ' \
                                            'potion of skill. You now have ' + str(current_skill) + ' skill.'
            if 'Potion of Skill' in items:
                status_update = status_update + ' You have of measure of the potion left.'
                items.remove('Potion of Skill')
                items.append('Half Potion of Skill')
            elif 'Half Potion of Skill' in items:
                status_update = status_update + 'you have used the last of your potion.'
                items.remove('Half Potion of Skill')
        if 'boathouse key' in items:
            status_update = status_update + ' You fumble around for the ' \
                                            'boathouse keys and move to passage ' + str(options[0]) + '.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[0])
        else:
            status_update = status_update + ' Without the boathouse keys, you head to passage ' + str(options[1]) + '.'
            create_media_tweet(room_entered, status_update)
            set_current_room(options[1])
    # lose 3 gold then a poll
    if room_entered in [272]:
        modify_gold(-3)
        status_update = 'You now have ' + str(current_gold) + ' gold.'
        poll_status = 'The north-west (271), the door (104) or maybe the riverbank (99)?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain wooden stakes then a poll
    if room_entered in [273]:
        items.append('wooden stake')
        status_update = 'You grab the mallet and stakes, then move on.'
        poll_status = 'Who could have built such an impressive room?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain 5 gold and 1 luck, then a poll
    if room_entered in [294]:
        modify_gold(5)
        modify_luck(1)
        status_update = 'You now have ' + str(current_gold) + ' gold and ' + str(current_luck) + ' luck.'
        poll_status = 'Search the bodies or move along?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain dragonfire then a poll tweet
    if room_entered in [296]:
        items.append('dragonfire')
        status_update = 'What an incredible find! You will not forget the name Farrigo Di Maggio'
        poll_status = 'Your mind is abuzz with the dragonfire spell. How will you proceed?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # smart take items, then add 1 luck and 1 skill and move on to look at them
    if room_entered in [313]:
        modify_luck(1)
        modify_skill(1)
        status_update = 'You consider some of the items first.'
        poll_status = 'Armour: 72, Shield: 132, Sword: 27, Gold: 110'
        media_tweet = create_media_tweet(room_entered, status_update)
        next_path_choices = ['72', '132', '27', '110']
        poll_tweet = client.create_tweet(text=poll_status, in_reply_to_tweet_id=media_tweet.data['id'],
                                         poll_options=next_path_choices, poll_duration_minutes=359)
        last_tweet_id = poll_tweet.data['id']
    # gain cheese then poll tweet
    if room_entered in [317]:
        items.append('a piece of cheese')
        status_update = 'The cheese does not look appetizing. You stow it away in your haversack.'
        poll_status = 'Which lever will you pull?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # 319 - go back to 212 to review second item
    if room_entered in [319]:
        play_next_room(221)
    # gain copper key 66 then may eat provisions and add 2 luck then poll tweet
    if room_entered in [322]:
        keys.append(66)
        hunger_result = check_to_eat()
        status_update = 'You stow the copper key inscribed 66 on your keyring.'
        if hunger_result == 'hungry':
            eat_provisions()
            modify_luck(2)
            status_update = status_update + ' You eat some rations. You now have ' + str(current_stamina) + \
                                            ' stamina and ' + str(current_luck) + ' luck.'
            poll_status = 'Is the box worth potentially waking this monster?'
            create_poll_tweet(room_entered, status_update, poll_status)
        else:
            modify_luck(2)
            status_update = status_update + ' You are not hungry enough to eat. You have ' + str(current_stamina) + \
                                            ' stamina and ' + str(current_luck) + ' luck.'
            poll_status = 'Is the box worth potentially waking this monster?'
            create_poll_tweet(room_entered, status_update, poll_status)
    # helmet grants + 1 to attack rolls then a poll
    if room_entered in [325]:
        items.append('magic helmet')
        status_update = 'What luck! You don the helmet and feel ferocious.'
        poll_status = 'Which way next, be-helmeted one?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # drink rum restore 6 stamina 1 luck then a poll
    if room_entered in [330]:
        modify_stamina(6)
        modify_luck(1)
        status_update = 'You now have ' + str(current_stamina) + \
                        ' stamina and ' + str(current_luck) + \
                        ' luck! You decide not to bring any rum along, in case you get too tipsy.'
        poll_status = 'The warmth of the rum quickly fades as you consider entering the crypt.'
        create_poll_tweet(room_entered, status_update, poll_status)
    # gain 2 gold and 2 luck then a poll
    if room_entered in [342]:
        modify_luck(2)
        gain_gold(2)
        status_update = 'You now have ' + str(current_luck) + ' luck and ' + str(current_gold) + ' gold.'
        poll_status = 'which way next?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # lose 1 stamina then test luck to not awaken guard
    if room_entered in [343]:
        next_passage_choice = 0
        lose_stamina(1, room_entered, '')
        luck_result = test_your_luck()
        if luck_result == 'lucky':
            next_passage_choice = options[0]
            status_update = ("Your luck holds, continue to passage " + str(options[0]))
        if luck_result == 'unlucky':
            next_passage_choice = options[1]
            status_update = ("Your luck fails you, continue to passage " + str(options[1]))
        create_media_tweet(room_entered, status_update)
        set_current_room(next_passage_choice)
    # gain magic sword and skill then a poll to keep the normal sword
    if room_entered in [344]:
        items.append('magic sword')
        modify_skill(1)
        status_update = 'What a wonderful sword! Your skill is now ' + str(current_skill) + '.'
        poll_status = 'Should you listen to the mysterious voice?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # working with the cards, their luck or yours
    if room_entered in [346]:
        if current_luck >= 9:
            luck_test = test_your_luck()
            dice_result = (random.randint(1, 6) + random.randint(1, 6))
            if luck_test == 'lucky':
                gain_gold(dice_result)
                status_update = status_update + 'You decide to test your luck and it pulls through! ' \
                                                'You gain ' + str(dice_result) + ' gold, up to ' + str(
                                                 current_gold) + '.'
            elif luck_test == 'unlucky':
                modify_gold(-dice_result)
                modify_luck(2)
                status_update = status_update + ' You decide to test your luck, but ' \
                                                'it fails you! You now have ' + \
                                                str(current_gold) + ' gold. You now have ' + \
                                                str(current_luck) + ' luck.'
            create_media_tweet(room_entered, status_update)
            set_current_room(131)
        else:
            die1_result = random.randint(1, 6)
            die2_result = random.randint(1, 6)
            total_gold = die1_result + die2_result
            status_update = "You don't trust your poor luck, so " \
                            "you try the cards. You roll a " + str(die1_result) + ' and a ' + str(die2_result) + '.'
            if total_gold in [2, 4, 6, 8, 10, 12]:
                modify_gold(-total_gold)
                status_update = status_update + ' You curse the cards and lose gold, down to ' + str(current_gold) + '.'
                create_media_tweet(room_entered, status_update)
                set_current_room(131)
            if total_gold in [1, 3, 5, 7, 9, 11]:
                modify_gold(total_gold)
                modify_luck(2)
                status_update = status_update + ' You thank the cards! You now have ' + \
                                                str(current_gold) + ' gold. You now have ' + \
                                                str(current_luck) + ' luck.'
                create_media_tweet(room_entered, status_update)
                set_current_room(131)
    # if croc wounded then enemy 2, else roll dice whether enemy 1 or two then eat and go to another passage.
    if room_entered in [350]:
        crocodile_round = fight_round_with_monster('crocodile', 7)
        die_result = random.randint(1, 6)
        if crocodile_round == 'player win' or 'same':
            status_update = 'You fend off the crocodile, just in time to fight ' \
                            'piranhas. You roll a ' + str(die_result) + '.'
        if crocodile_round == 'monster win':
            lose_stamina(2, room_entered, '')
            status_update = 'The crocodile gets one last chomp on you! You have ' + \
                            str(current_stamina) + ' stamina.' \
                            ' You rolled a ' + str(die_result) + '.'
        if die_result in [1, 2]:
            fight_monster(room_monster_dictionary[room_entered][0])
        elif die_result in [3, 4, 5, 6]:
            fight_monster(room_monster_dictionary[room_entered][0])
        modify_luck(1)
        status_update = status_update + ' You gain 1 luck after defeating the piranhas.'
        hunger_check = check_to_eat()
        if hunger_check == 'hungry':
            eat_provisions()
            status_update = status_update + ' You also sit down to rest, ' \
                                            'you now have ' + str(current_stamina) + ' stamina.'
        if hunger_check == 'not hungry':
            status_update = status_update + " You don't care to eat however, with " + str(current_stamina) + ' stamina.'
        create_media_tweet(room_entered, status_update)
        set_current_room(7)
    # lose one stamina then a poll
    if room_entered in [352]:
        lose_stamina(1, room_entered, '')
        status_update = 'You now have ' + str(current_stamina) + " stamina. The vampire's will is painful to resist."
        poll_status = 'Perhaps another avenue of attack?'
        create_poll_tweet(room_entered, status_update, poll_status)
    # lose 3 stamina then a poll
    if room_entered in [368]:
        lose_stamina(3, room_entered, '')
        if current_stamina > 0:
            status_update = 'This avenue was not successful. You now have ' + str(current_stamina) + ' stamina.'
            poll_status = 'Perhaps another approach?'
            create_poll_tweet(room_entered, status_update, poll_status)
    # gain 8 gold then a poll
    if room_entered in [393]:
        modify_gold(8)
        status_update = 'You gain 8 gold, you now have ' + str(current_gold) + ' gold.'
        poll_status = 'Which will you investigate?'
        create_poll_tweet(room_entered, status_update, poll_status)


def eat_provisions():
    global current_provisions
    global current_stamina
    modify_stamina(4)
    current_provisions -= 1


def enter_passage_two_two_one(item_acquired, tweet_status):
    global items
    global last_tweet_id
    passage_221_dict = {'fresh armour': '72', 'wooden shield': '132', 'enchanted sword': '27', 'boot gold': '110',
                        'crucifix': '170'}
    poll_221_choices = []
    for each in passage_221_dict:
        if each not in items:
            poll_221_choices.append(passage_221_dict[each])
    items.remove(item_acquired)
    increment = 0
    for each in ['fresh armour', 'wooden shield', 'enchanted sword', 'boot gold', 'crucifix']:
        if each in items:
            increment += 1
    items.append(item_acquired)
    if increment == 1:
        tweet_status = tweet_status + ' You move to passage 81.'
        create_media_tweet(get_current_room(), tweet_status)
        set_current_room(81)
    else:
        media_tweet = create_media_tweet(get_current_room(), tweet_status)
        poll_tweet = client.create_tweet(text='Choose your second item:', in_reply_to_tweet_id=media_tweet.data['id'],
                                         poll_options=poll_221_choices, poll_duration_minutes=359)
        last_tweet_id = poll_tweet.data['id']
        update_last_tweet_id()
        set_current_room(221)


def fight_addtl_wight_rounds():
    global fight_text
    global current_stamina
    global current_skill
    global initial_skill
    wight_skill = int(room_monster_dictionary[get_current_room()][0])
    wight_stamina = int(room_monster_dictionary[get_current_room()][1])
    wight_name = room_monster_dictionary[get_current_room()][2]
    wight_wounds = 0
    player_wounds = 0
    while current_stamina > 0 and wight_stamina > wight_wounds:
        round_result = fight_round_with_monster(wight_name, wight_skill)
        if round_result == 'player win':
            wight_wounds += 2
            fight_text.append('You slash the wight.')
        if round_result == 'monster win':
            fight_text.append('The wight hits you.')
            fight_text.append('You now have ' + str(current_stamina) + ' stamina.')
            lose_stamina(2, get_current_room(), '')
            player_wounds += 1
        if player_wounds >= 3:
            modify_skill(-1)
            fight_text.append('The wight drains your skill!')
            fight_text.append('You now have ' + str(current_skill) + ' skill.')
            if (7 > current_skill or (initial_skill - current_skill) > 3) and ('Potion of Skill' in items or 'Half '
                                                                                                             'Potion '
                                                                                                             'of '
                                                                                                             'Skill'
                                                                               in items):
                current_skill = initial_skill
                fight_text.append(' You quaff some of your '
                                  'potion of skill. You now have ' + str(current_skill) + ' skill.')
                if 'Potion of Skill' in items:
                    fight_text.append(' You have of measure of the potion left.')
                    items.remove('Potion of Skill')
                    items.append('Half Potion of Skill')
                elif 'Half Potion of Skill' in items:
                    fight_text.append('You have used the last of your potion.')
                    items.remove('Half Potion of Skill')
            player_wounds = 0


def fight_monster(monster_name):
    global current_stamina
    global items
    global fight_text
    global current_personality
    global won_last_round
    monster_stamina = monster_dictionary[monster_name][1]
    monster_skill = monster_dictionary[monster_name][0]
    monster_wounds = 0
    if monster_name in ['Goblin19a', 'Goblin19b', 'Warlock39', 'Crocodile86', 'Hand108', 'Skeleton140a',
                        'Skeleton140b', 'Skeleton140c', 'Skeleton140d', 'Skeleton140e', 'Warlock142', 'Dragon152',
                        'Piranhas158', 'Goblin161a', 'Orc161b', 'Gremlin161c', 'Giant Rat161d', 'Skeleton161e',
                        'Troll161f', 'Caveman199a', 'Caveman199B', 'Ghoul230', 'Skeleton236a', 'Skeleton236b',
                        'Skeleton236c', 'Snake240', 'Dog249', 'Zombie282a', 'Zombie282b', 'Zombie282c',
                        'Zombie282d',
                        'Warlock289', 'Rat309a', 'Rat309b', 'Rat309c', 'Troll331', 'Piranhas350a', 'Piranhas350b',
                        'Orc Chieftain372a', 'Servant372b', 'Winged Gremlin377', 'Giant Spider394']:
        can_flee = 'no'
    else:
        can_flee = 'yes'
    flee_counter = 0
    if monster_name in ['Ogre16', 'Giant Spider161']:
        flee_counter = 2
    if monster_name in ['Giant Sandworm143', 'Giant163', 'Minotaur179']:
        flee_counter = 3
    if monster_name == 'Vampire333':
        flee_counter = 6
    fled = 'no'
    won_last_round = 'no'
    while current_stamina > 0 and monster_stamina > monster_wounds and fled == 'no':
        if can_flee == 'yes' and flee_counter == 0:
            escape_test_results = test_to_escape(monster_skill)
            if escape_test_results == 'flee':
                if monster_name == 'Vampire333':
                    luck_test = test_your_luck()
                    if luck_test == 'lucky':
                        lose_stamina(2, get_current_room(), '')
                        generate_combat_log_image()
                        create_media_tweet(333, 'You barely escape the vampire with '
                                           + str(current_stamina) + 'stamina.')
                        set_current_room(380)
                    elif luck_test == 'unlucky':
                        fight_text.append('You attempt to escape, but fail. Your luck is '
                                          + str(current_luck) + ' and your stamina is ' + str(current_stamina) + '.')
                        flee_counter = 6
                else:
                    lose_stamina(2, get_current_room(), '')
                    status_update = 'You escape with ' + str(current_stamina) + ' stamina remaining.'
                    fight_text.append('You escape!')
                    generate_combat_log_image()
                    create_media_tweet(get_current_room(), status_update)
                    set_current_room(monster_dictionary[3])
                    fled = 'yes'
        result = fight_round_with_monster(monster_name, monster_skill)
        if result == 'player win':
            extra_damage_luck = test_extra_damage(monster_stamina, (monster_skill - monster_wounds))
            if monster_name in ['Barbarian8', 'Ogre16', 'Wight41', 'Orc33', 'Warlock39', 'Giant Spider61',
                                'Crocodile86',
                                'Hand108', 'Dog249', 'Warlock142', 'Giant Sandworm143', 'Ghoul230', 'Dragon152',
                                'Piranhas158', 'Goblin161a', 'Orc161b', 'Gremlin161c', 'Giant Rat161d', 'Skeleton161e',
                                'Troll161f', 'Giant163', 'Minotaur179', 'Wererat188', 'Ghoul230', 'Snake240', 'Orc248',
                                'Giant Bats251', 'Warlock289', 'Werewolf304', 'Troll331', 'Vampire333',
                                'Iron Cyclops338',
                                'Piranhas350a', 'Piranhas350b', 'Orc Chieftain372a', 'Servant372b', 'Winged Gremlin377',
                                'Giant Spider394']:
                fight_text.append('You hit the ' + str(monster_dictionary[monster_name][2]) + '.')
            else:
                fight_text.append('You hit ' + str(monster_dictionary[monster_name][2]) + '.')
            if extra_damage_luck == 'no test':
                monster_wounds += 2
            elif extra_damage_luck == 'lucky':
                monster_wounds += 3
                fight_text.append('You test luck to do extra damage, and succeed! You have '
                                  + str(current_luck) + ' luck.')
            elif extra_damage_luck == 'unlucky':
                monster_wounds += 2
                fight_text.append('You test luck to do extra damage, but fail! You have '
                                  + str(current_luck) + ' luck.')
            if current_personality == 'Noble':
                won_last_round = 'yes'
        if result == 'monster win':
            die_result = random.randint(1, 6)
            reduce_damage_luck = test_reduce_damage(2, monster_skill)
            if 'magic shield' in items and die_result == 6:
                if reduce_damage_luck == 'lucky':
                    if monster_name in ['Barbarian8', 'Ogre16', 'Wight41', 'Orc33', 'Warlock39', 'Giant Spider61',
                                        'Crocodile86',
                                        'Hand108', 'Dog249', 'Warlock142', 'Giant Sandworm143', 'Ghoul230', 'Dragon152',
                                        'Piranhas158', 'Goblin161a', 'Orc161b', 'Gremlin161c', 'Giant Rat161d',
                                        'Skeleton161e',
                                        'Troll161f', 'Giant163', 'Minotaur179', 'Wererat188', 'Ghoul230', 'Snake240',
                                        'Orc248',
                                        'Giant Bats251', 'Warlock289', 'Werewolf304', 'Troll331', 'Vampire333',
                                        'Iron Cyclops338',
                                        'Piranhas350a', 'Piranhas350b', 'Orc Chieftain372a', 'Servant372b',
                                        'Winged Gremlin377',
                                        'Giant Spider394']:
                        fight_text.append('The ' + str(monster_dictionary[monster_name][2]) +
                                          ' hits your magic shield. You test your luck to avoid the '
                                          'damage and succeed! ')
                    else:
                        fight_text.append(str(monster_dictionary[monster_name][2]) +
                                          ' hits your magic shield. You test your luck to avoid the damage '
                                          'and succeed! ')
                    fight_text.append('You now have ' + str(current_stamina) + ' stamina and ' + str(current_luck) +
                                      ' luck.')
                elif reduce_damage_luck == 'unlucky':
                    lose_stamina(1, get_current_room(), '')
                    if monster_name in ['Barbarian8', 'Ogre16', 'Wight41', 'Orc33', 'Warlock39', 'Giant Spider61',
                                        'Crocodile86',
                                        'Hand108', 'Dog249', 'Warlock142', 'Giant Sandworm143', 'Ghoul230', 'Dragon152',
                                        'Piranhas158', 'Goblin161a', 'Orc161b', 'Gremlin161c', 'Giant Rat161d',
                                        'Skeleton161e',
                                        'Troll161f', 'Giant163', 'Minotaur179', 'Wererat188', 'Ghoul230', 'Snake240',
                                        'Orc248',
                                        'Giant Bats251', 'Warlock289', 'Werewolf304', 'Troll331', 'Vampire333',
                                        'Iron Cyclops338',
                                        'Piranhas350a', 'Piranhas350b', 'Orc Chieftain372a', 'Servant372b',
                                        'Winged Gremlin377',
                                        'Giant Spider394']:
                        fight_text.append('The ' + str(monster_dictionary[monster_name][2]) +
                                          ' hits your magic shield. You test your luck to avoid the damage but fail! ')
                    else:
                        fight_text.append(str(monster_dictionary[monster_name][2]) +
                                          ' hits your magic shield. You test your luck to avoid the damage but fail! ')
                    fight_text.append('You now have ' + str(current_stamina) + ' stamina and ' + str(current_luck) +
                                      ' luck.')
                else:
                    lose_stamina(1, get_current_room(), '')
                    if monster_name in ['Barbarian8', 'Ogre16', 'Wight41', 'Orc33', 'Warlock39', 'Giant Spider61',
                                        'Crocodile86',
                                        'Hand108', 'Dog249', 'Warlock142', 'Giant Sandworm143', 'Ghoul230', 'Dragon152',
                                        'Piranhas158', 'Goblin161a', 'Orc161b', 'Gremlin161c', 'Giant Rat161d',
                                        'Skeleton161e',
                                        'Troll161f', 'Giant163', 'Minotaur179', 'Wererat188', 'Ghoul230', 'Snake240',
                                        'Orc248',
                                        'Giant Bats251', 'Warlock289', 'Werewolf304', 'Troll331', 'Vampire333',
                                        'Iron Cyclops338',
                                        'Piranhas350a', 'Piranhas350b', 'Orc Chieftain372a', 'Servant372b',
                                        'Winged Gremlin377',
                                        'Giant Spider394']:
                        fight_text.append('The ' + str(monster_dictionary[monster_name][2]) +
                                          ' hits you, but your shield blocks. You have ' +
                                          str(current_stamina) + ' stamina.')
                    else:
                        fight_text.append(str(monster_dictionary[monster_name][2]) +
                                          ' hits you, but your shield blocks. You have ' +
                                          str(current_stamina) + ' stamina.')
            else:
                if reduce_damage_luck == 'lucky':
                    lose_stamina(1, get_current_room(), '')
                    fight_text.append('You use your good luck to avoid the worst of the blow.')
                    fight_text.append('You now have ' + str(current_stamina) + ' stamina and '
                                      + str(current_luck) + ' luck.')
                elif reduce_damage_luck == 'unlucky':
                    lose_stamina(2, get_current_room(), '')
                    fight_text.append('You try to use your luck to avoid the blow, but fail.')
                    fight_text.append('You now have ' + str(current_stamina) + ' stamina and '
                                      + str(current_luck) + ' luck.')
                else:
                    lose_stamina(2, get_current_room(), '')
                    if monster_name in ['Barbarian8', 'Ogre16', 'Wight41', 'Orc33', 'Warlock39', 'Giant Spider61',
                                        'Crocodile86',
                                        'Hand108', 'Dog249', 'Warlock142', 'Giant Sandworm143', 'Ghoul230', 'Dragon152',
                                        'Piranhas158', 'Goblin161a', 'Orc161b', 'Gremlin161c', 'Giant Rat161d',
                                        'Skeleton161e',
                                        'Troll161f', 'Giant163', 'Minotaur179', 'Wererat188', 'Ghoul230', 'Snake240',
                                        'Orc248',
                                        'Giant Bats251', 'Warlock289', 'Werewolf304', 'Troll331', 'Vampire333',
                                        'Iron Cyclops338',
                                        'Piranhas350a', 'Piranhas350b', 'Orc Chieftain372a', 'Servant372b',
                                        'Winged Gremlin377',
                                        'Giant Spider394']:
                        fight_text.append('The ' + str(monster_dictionary[monster_name][2]) + ' hits you, You have ' +
                                          str(current_stamina) + ' stamina.')
                    else:
                        fight_text.append(str(monster_dictionary[monster_name][2]) + ' hits you, You have ' +
                                          str(current_stamina) + ' stamina.')
            if current_personality == 'Noble':
                won_last_round = 'no'
        if result == 'same' and current_personality == 'Noble':
            won_last_round = 'no'
        if flee_counter > 0:
            flee_counter -= 1
    if current_stamina > 0:
        if monster_name in ['Barbarian8', 'Ogre16', 'Wight41', 'Orc33', 'Warlock39', 'Giant Spider61', 'Crocodile86',
                            'Hand108', 'Dog249', 'Warlock142', 'Giant Sandworm143', 'Ghoul230', 'Dragon152',
                            'Piranhas158', 'Goblin161a', 'Orc161b', 'Gremlin161c', 'Giant Rat161d', 'Skeleton161e',
                            'Troll161f', 'Giant163', 'Minotaur179', 'Wererat188', 'Ghoul230', 'Snake240', 'Orc248',
                            'Giant Bats251', 'Warlock289', 'Werewolf304', 'Troll331', 'Vampire333', 'Iron Cyclops338',
                            'Piranhas350a', 'Piranhas350b', 'Orc Chieftain372a', 'Servant372b', 'Winged Gremlin377',
                            'Giant Spider394']:
            fight_text.append("You defeated the " + monster_dictionary[monster_name][2] + '. ')
            status_update = "You defeated the " + monster_dictionary[monster_name][2] + '. '
        else:
            fight_text.append("You defeated " + monster_dictionary[monster_name][2] + '. ')
            status_update = "You defeated " + monster_dictionary[monster_name][2] + '. '
    else:
        status_update = ''
    return status_update


def fight_round_with_monster(monster_name, monster_skill):
    global current_stamina
    global current_skill
    global items
    global won_last_round
    global current_personality
    global fight_text
    player_result = (random.randint(1, 6) + random.randint(1, 6) + current_skill)
    if 'magic helmet' in items:
        player_result += 1
    if current_personality == 'Noble' and won_last_round == 'yes':
        player_result += 1
    monster_result = (random.randint(1, 6) + random.randint(1, 6) + monster_skill)
    fight_text.append('You rolled: ' + str(player_result) + '. ' + monster_dictionary[monster_name][2] + ' rolled: '
                      + str(monster_result) + '.')
    if monster_result == player_result:
        return 'same'
    if monster_result < player_result:
        return 'player win'
    if monster_result > player_result:
        return 'monster win'


def fight_room_161():
    roll_index = (random.randint(1, 6) - 1)
    enemy = room_monster_dictionary[161][roll_index]
    fight_monster(enemy)
    return enemy


def fight_wight(tweet_status):
    global current_stamina
    wight_skill = int(room_monster_dictionary[get_current_room()][0])
    wight_stamina = int(room_monster_dictionary[get_current_room()][1])
    wight_name = room_monster_dictionary[get_current_room()][2]
    wight_wounds = 0
    options = room_choices[get_current_room()]
    while current_stamina > 0 and wight_stamina > 0 and wight_wounds < 3:
        round_result = fight_round_with_monster(wight_name, wight_skill)
        if round_result == 'player win':
            wight_stamina -= 2
        if round_result == 'monster win':
            lose_stamina(2, get_current_room(), tweet_status)
            wight_wounds += 1
    if wight_wounds >= 3:
        status_update = tweet_status + 'You fought hard, but the wight has hit you ' \
                                        'for a third time, turn to passage 24.'
        create_media_tweet(get_current_room(), status_update)
        set_current_room(options[0])
    else:
        status_update = tweet_status + 'You emerge victorious with ' \
                        + str(current_stamina) + ' stamina remaining and ' \
                        + str(wight_wounds) + ' wounds from the wight.'
        create_media_tweet(get_current_room(), status_update)
        set_current_room(options[1])


def gain_gold(gold_gained):
    global current_gold
    current_gold += gold_gained


def generate_combat_log_image():
    global font_selected
    global fight_text
    longest_string = 0
    increment = 20
    for each in fight_text:
        if len(each) > longest_string:
            longest_string = len(each)
    height = ((1 + len(fight_text)) * 22)
    width = (10 + (longest_string * 7))
    generated_image = Image.new('RGB', (width, height), color='white')
    added_text = ImageDraw.Draw(generated_image)
    for each in fight_text:
        added_text.text((10, increment), each, font=font_selected, fill=(0, 0, 0))
        increment += 20
    generated_image.save('fight_result.jpg')
    fight_text = []


def get_current_room():
    with open('room_path.txt', 'rt') as file:
        lines = file.readlines()
        last_room = lines[-1].strip('\n')
    return last_room


def get_poll_results(poll_id):
    client_bearer = tweepy.Client(bearer_token)
    poll_results_tweet = client_bearer.get_tweet(id=poll_id, expansions='attachments.poll_ids',
                                                 poll_fields=['options', 'voting_status'])
    poll_results_total = poll_results_tweet.includes["polls"][0].options
    to_beat = 0
    victor = 0
    for poll_choice in poll_results_total:
        challenger = poll_choice["votes"]
        if challenger > to_beat:
            victor = poll_choice['label']
            to_beat = challenger
    if to_beat == 0:
        victor = poll_results_total[random.randint(0, len(poll_results_total) - 1)]['label']
    return victor


def handle_passage_86():
    global current_stamina
    with open("adversary_stamina.txt", 'rt') as reading:
        croc_stamina = int(reading.read())
        while croc_stamina > 0 and current_stamina > 0:
            result = fight_round_with_monster('crocodile', 7)
            if result == 'player win':
                croc_stamina -= 2
            elif result == 'monster win':
                lose_stamina(2, get_current_room(), '')
        status_update = 'You defeat the crocodile, with ' + str(current_stamina) + \
                        ' stamina remaining and head for passage 259.'
        create_media_tweet(86, status_update)
        set_current_room(259)


def handle_special_results(result):
    global last_tweet_id
    global current_personality
    global chosen_difficulty
    global current_room
    global current_luck
    global items
    global potion_chosen
    if result == 'fight on!':
        handle_passage_86()
        set_current_room(259)
    if result == 'Test your luck!':
        luck_test = test_your_luck()
        if luck_test == 'lucky':
            set_current_room(147)
            play_next_room(147)
        else:
            set_current_room(33)
            play_next_room(33)
    # for passage 159
    elif result in ['attack', 'sneak out']:
        if result == 'attack':
            status_update = 'You rush the bickering orcs!'
            create_media_tweet(159, status_update)
            set_current_room(365)
        elif result == 'sneak out':
            luck_test = test_your_luck()
            if luck_test == 'lucky':
                status_update = 'You get lucky and the orcs do not notice you. Head to passage ' \
                                '237.'
                create_media_tweet(159, status_update)
                set_current_room(237)
            elif luck_test == 'unlucky':
                status_update = 'You bump into a chair while trying to leave! The orcs turn their attention to you.' \
                                'Prepare for combat at passage 365.'
                create_media_tweet(159, status_update)
                set_current_room(365)
    # chosen a character, now do room 401
    elif result in ['Soldier', 'Cook', 'Berserker', 'Noble']:
        current_personality = result
        initialize_character_personality()
        adjust_stats_based_on_personality()
        update_character_stats()
        update_initial_character_stats()
        poll_potion_to_bring(result)
        update_last_tweet_id()
        set_current_room('0-2')
    # for difficulty results
    elif result in ['Easy', 'Medium', 'Hard', 'Very Hard']:
        set_initial_stats(result)
        chosen_difficulty = result
        update_difficulty_choice()
        update_character_stats()
        update_initial_character_stats()
        poll_character_personality(result)
        update_last_tweet_id()
    # for results of potion question
    elif result in ['Skill', 'Strength', 'Fortune']:
        potion_chosen = 'Potion of ' + str(result)
        items.append(potion_chosen)
        initialize_potion_choice()
        set_current_room(1)
        play_next_room(1)
    # passage 119 has you throwing something to distract the ogre
    elif result in items:
        items.remove(result)
        status_update = 'You toss the ' + str(result) + ' to the far side of the cavern and quickly retreat. ' \
                                                        'You still have:'
        for each_item in items:
            if each_item not in ['armour']:
                status_update = status_update + ' A ' + str(each_item) + '.'
            elif each_item in ['armour']:
                status_update = status_update + ' An ' + str(each_item) + '.'
        poll_status = 'Your heart is racing after escaping the ogre, take a moment to catch your breath ' \
                      'and consider the next junction.'
        create_poll_tweet(269, status_update, poll_status)
        set_current_room(269)


def initialize_character_personality():
    global current_personality
    with open("character_personality.txt", 'wt') as file_to_update:
        file_to_update.write(current_personality)


def initialize_potion_choice():
    global potion_chosen
    with open("potion_chosen.txt", 'wt') as file_to_update:
        file_to_update.write(potion_chosen)


def initialize_game():
    to_wipe = ['items', 'keys', 'character_personality', 'current_character_stats', 'initial_character_stats',
               'last_tweet_id', 'room_path']
    basic_items = ['sword', 'armour', 'lantern']
    for each in to_wipe:
        with open(each + ".txt", 'wt') as wipe_clean:
            wipe_clean.close()
    with open('room_path.txt', 'at') as set_room_zero:
        set_room_zero.write('0\n')
    with open('items.txt' 'at') as create_item_list:
        for each in basic_items:
            create_item_list.write(each + '\n')


def lose_stamina(loss_amt, room_entered, tweet_status):
    global current_stamina
    global current_personality
    global initial_stamina
    global items
    global fight_text
    current_stamina -= loss_amt
    if current_stamina <= 0:
        if current_personality == 'Berserker':
            death_defy_result = test_to_defy_death()
            if death_defy_result == 'alive':
                current_stamina = 1
                fight_text.append('You defy death!! You are on the brink of '
                                  'death with ' + str(current_stamina) + ' stamina and ' + str(current_luck) + ' luck.')
                return 'not dead'
        else:
            if current_stamina < 4 and ('Potion of Strength' in items or 'Half Potion of Strength' in items):
                current_stamina = initial_stamina
                fight_text.append(' You quaff some of your '
                                  'potion of strength. You now have '
                                  + str(current_stamina) + ' stamina.')
                if 'Potion of Strength' in items:
                    fight_text.append(' You have one measure of the potion left.')
                    items.remove('Potion of Strength')
                    items.append('Half Potion of Strength')
                elif 'Half Potion of Strength' in items:
                    fight_text.append('You have used the last of your potion.')
                    items.remove('Half Potion of Strength')
            tweet_status = tweet_status + ' This has proven fatal. You will need to start over.'
            if len(tweet_status) > 280:
                tweet_status = 'You have met your end here, succumbing to your injuries. You will need to start over.'
            create_media_tweet(room_entered, tweet_status)
            set_current_room(0)
            initialize_game()
            return 'dead'
    else:
        return 'not dead'


def media_or_poll_result():
    global last_tweet_id
    if last_tweet_id == '':
        return 'no tweet'
    client_bearer = tweepy.Client(bearer_token)
    last_thing_tweeted = client_bearer.get_tweet(id=last_tweet_id, expansions='attachments.poll_ids',
                                                 poll_fields=['options', 'voting_status'])
    if len(last_thing_tweeted.includes) > 0:
        return 'poll tweet'
    else:
        return 'media tweet'


def modify_gold(amount_to_change):
    global current_gold
    current_gold += amount_to_change
    if current_gold < 0:
        current_gold = 0


def modify_luck(amount_to_change):
    global current_luck
    global initial_luck
    current_luck += amount_to_change
    if current_luck > initial_luck:
        current_luck = initial_luck
    if current_luck < 0:
        current_luck = 0


def modify_skill(amount_to_change):
    global current_skill
    global initial_skill
    current_skill += amount_to_change
    if current_skill > initial_skill:
        current_skill = initial_skill
    if current_skill < 0:
        current_skill = 0


def modify_stamina(amount_to_change):
    global current_stamina
    global initial_stamina
    current_stamina += amount_to_change
    if current_stamina > initial_stamina:
        current_stamina = initial_stamina


def play_next_room(room_entered):
    if room_entered in normal_rooms:
        create_normal_room(room_entered)
    elif room_entered in dead_rooms:
        create_dead_room(room_entered)
    elif room_entered in fight_dependent_rooms:
        create_fight_dependent_room(room_entered)
    elif room_entered in item_dependent_rooms:
        create_item_dependent_room(room_entered)
    elif room_entered in key_rooms:
        create_key_room(room_entered)
    elif room_entered in luck_dependent_rooms:
        create_luck_dependent_room(room_entered)
    elif room_entered in provisions_dependent_rooms:
        create_provisions_dependent_room(room_entered)
    elif room_entered in random_fight_rooms:
        create_random_fight_room(room_entered)
    elif room_entered in roll_a_die_rooms:
        create_roll_a_die_room(room_entered)
    elif room_entered in special_passage_rooms:
        create_special_passage_room(room_entered)


def poll_character_personality(difficulty_chosen):
    status_update = 'You have chosen to play on ' + str(difficulty_chosen) + '.'
    poll_status = 'Choose your class:'
    create_poll_tweet('0-1', status_update, poll_status)


def poll_potion_to_bring(class_chosen):
    status_update = 'You have chosen to play as a ' + str(class_chosen) + '.'
    poll_status = 'Choose your potion:'
    create_poll_tweet('0-2', status_update, poll_status)


def populate_past_rooms():
    global past_rooms
    with open("room_path.txt", 'rt') as room_file:
        past_rooms = room_file.read().splitlines()


def pull_monsters(room_entered):
    return room_monster_dictionary[room_entered]


def pull_last_tweet_id():
    global last_tweet_id
    with open("last_tweet_id.txt", 'rt') as file_to_read:
        last_tweet_id = file_to_read.read()


def set_character_stats():
    global current_stamina
    global current_skill
    global current_luck
    global current_gold
    global current_provisions
    global initial_skill
    global initial_stamina
    global initial_luck
    global initial_gold
    global initial_provisions
    global current_personality
    global potion_chosen
    global chosen_difficulty
    with open("current_character_stats.txt", 'rt') as file_to_read:
        stat_block = []
        line_to_read = file_to_read.readline()
        while line_to_read:
            stat_block.append(line_to_read)
            line_to_read = file_to_read.readline()
        current_skill = int(stat_block[0])
        current_stamina = int(stat_block[1])
        current_luck = int(stat_block[2])
        current_gold = int(stat_block[3])
        current_provisions = int(stat_block[4])
    with open("initial_character_stats.txt", 'rt') as file_to_read:
        stat_block = []
        line_to_read = file_to_read.readline()
        while line_to_read:
            stat_block.append(line_to_read)
            line_to_read = file_to_read.readline()
        initial_skill = int(stat_block[0])
        initial_stamina = int(stat_block[1])
        initial_luck = int(stat_block[2])
        initial_gold = int(stat_block[3])
        initial_provisions = int(stat_block[4])
    with open("character_personality.txt", 'rt') as file_to_read:
        line_to_read = file_to_read.readline()
        current_personality = line_to_read
    with open("potion_chosen.txt", 'rt') as file_to_read:
        line_to_read = file_to_read.readline()
        potion_chosen = line_to_read
    with open("difficulty_chosen.txt", 'rt') as file_to_read:
        line_to_read = file_to_read.readline()
        chosen_difficulty = line_to_read


def set_current_room(updated_room):
    global current_room
    with open("room_path.txt", 'at') as file:
        file.write(str(updated_room) + '\n')
    current_room = updated_room


def set_items_and_keys():
    global items
    global keys
    with open("items.txt", 'rt') as file_to_read:
        line_to_read = file_to_read.readline()
        while line_to_read:
            item_to_append = line_to_read.strip('\n')
            if item_to_append != '':
                items.append(item_to_append)
            line_to_read = file_to_read.readline()
    with open("keys.txt", 'rt') as file_to_read:
        line_to_read = file_to_read.readline()
        while line_to_read:
            key_to_append = line_to_read.strip('\n')
            if key_to_append != '':
                keys.append(int(key_to_append))
            line_to_read = file_to_read.readline()


def set_initial_stats(difficulty_chosen):
    global initial_skill
    global initial_stamina
    global initial_luck
    global initial_gold
    global initial_provisions
    global current_stamina
    global current_skill
    global current_luck
    global current_gold
    global current_provisions
    if difficulty_chosen == 'Easy':
        initial_skill = 11
        initial_stamina = 18
        initial_luck = 11
        initial_gold = 0
        initial_provisions = 10
    elif difficulty_chosen == 'Medium':
        initial_skill = 10
        initial_stamina = 16
        initial_luck = 10
        initial_gold = 0
        initial_provisions = 9
    elif difficulty_chosen == 'Hard':
        initial_skill = 9
        initial_stamina = 15
        initial_luck = 8
        initial_gold = 0
        initial_provisions = 7
    elif difficulty_chosen == 'Very Hard':
        initial_skill = 8
        initial_stamina = 14
        initial_luck = 8
        initial_gold = 0
        initial_provisions = 6
    current_skill = initial_skill
    current_stamina = initial_stamina
    current_luck = initial_luck
    current_gold = initial_gold
    current_provisions = initial_provisions
    update_initial_character_stats()
    update_character_stats()


def test_to_defy_death():
    global current_luck
    death_defied = (random.randint(1, 6) + random.randint(1, 6))
    if death_defied <= (current_luck + 4):
        current_luck -= 1
        return 'alive'
    else:
        current_luck -= 1
        return 'dead'


def test_extra_damage(enemy_stamina, enemy_skill):
    global current_personality
    global current_skill
    global current_luck
    global current_stamina
    if current_personality == 'Soldier':
        if current_luck > 8 or (current_luck > 5 > current_stamina):
            if (enemy_stamina % 2) == 1:
                if current_skill - enemy_skill > 2:
                    return 'no test'
                else:
                    return test_your_luck()
        return 'no test'
    elif current_personality == 'Cook':
        if (enemy_stamina % 2) == 1:
            if current_luck > 9:
                if current_skill - enemy_skill > 3:
                    return 'no test'
                else:
                    return test_your_luck()
            else:
                return 'no test'
        else:
            return 'no test'
    elif current_personality == 'Berserker':
        if current_skill - enemy_skill < 0:
            if (enemy_stamina % 2) == 1:
                if current_luck > 8:
                    return test_your_luck()
                else:
                    return 'no test'
            else:
                return 'no test'
        else:
            return 'no test'
    elif current_personality == 'Noble':
        if current_skill < enemy_skill and (enemy_stamina % 2) == 1 and current_luck > 10:
            return test_your_luck()
        else:
            return 'no test'


def test_reduce_damage(damage_to_take, enemy_skill):
    global current_personality
    global current_stamina
    global current_luck
    if damage_to_take >= current_stamina:
        return test_your_luck()
    elif current_personality == 'Soldier':
        if ((current_stamina - damage_to_take) % 2) == 0 and current_luck > 9 and enemy_skill > (current_skill + 1):
            return test_your_luck()
        else:
            return 'no test'
    elif current_personality == 'Cook':
        if current_luck > 10 and ((current_stamina - damage_to_take) % 2) == 0:
            return test_your_luck()
        else:
            return 'no test'
    elif current_personality == 'Berserker':
        return 'no test'
    elif current_personality == 'Noble':
        if current_luck > 6 and enemy_skill > (current_skill - 1):
            return test_your_luck()
        else:
            return 'no test'


def test_to_escape(enemy_skill):
    global current_stamina
    global current_personality
    global current_skill
    skill_diff = (enemy_skill - current_skill)
    if current_stamina <= 2:
        return 'no flee'
    elif current_personality in ['Soldier', 'Noble'] and skill_diff > 3:
        return 'flee'
    elif current_personality == 'Cook' and skill_diff > 0:
        return 'flee'
    elif current_personality == 'Berserker' and skill_diff > 5:
        return 'flee'
    else:
        return 'no flee'


def test_your_luck():
    global current_luck
    global items
    global initial_luck
    global fight_text
    dice_result = (random.randint(1, 6) + random.randint(1, 6))
    if dice_result <= current_luck:
        current_luck -= 1
        if current_luck < 7 and ('Potion of Fortune' in items or 'Half Potion of Fortune' in items):
            initial_luck += 1
            current_luck = initial_luck
            fight_text.append('You quaff a measure of your potion. You now have ' + str(current_luck) + ' luck.')
            if 'Potion of Fortune' in items:
                items.remove('Potion of Fortune')
                items.append('Half Potion of Fortune')
                fight_text.append('You have one measure of your potion remaining.')
            elif 'Half Potion of Fortune' in items:
                items.remove('Half Potion of Fortune')
                fight_text.append('You have used the last of your potion.')
        return 'lucky'
    if dice_result > current_luck:
        current_luck -= 1
        if current_luck < 7 and ('Potion of Fortune' in items or 'Half Potion of Fortune' in items):
            initial_luck += 1
            current_luck = initial_luck
            fight_text.append('You quaff a measure of your potion. You now have ' + str(current_luck) + ' luck.')
            if 'Potion of Fortune' in items:
                items.remove('Potion of Fortune')
                items.append('Half Potion of Fortune')
                fight_text.append('You have one measure of your potion remaining.')
            elif 'Half Potion of Fortune' in items:
                items.remove('Half Potion of Fortune')
                fight_text.append('You have used the last of your potion.')
        return 'unlucky'


def update_character_stats():
    global current_stamina
    global current_skill
    global current_luck
    global current_gold
    global current_provisions
    with open("current_character_stats.txt", 'wt') as wipe_clean:
        wipe_clean.close()
    with open("current_character_stats.txt", 'at') as file_to_update:
        for each in [current_skill, current_stamina, current_luck, current_gold, current_provisions]:
            file_to_update.write(str(each) + '\n')


def update_difficulty_choice():
    global chosen_difficulty
    with open('difficulty_chosen.txt', 'wt') as wipe_clean:
        wipe_clean.close()
    with open('difficulty_chosen.txt', 'at') as file_to_update:
        file_to_update.write(chosen_difficulty)


def update_initial_character_stats():
    global initial_stamina
    global initial_skill
    global initial_luck
    global initial_gold
    global initial_provisions
    with open("initial_character_stats.txt", 'wt') as wipe_clean:
        wipe_clean.close()
    with open("initial_character_stats.txt", 'at') as file_to_update:
        for each in [initial_skill, initial_stamina, initial_luck, initial_gold, initial_provisions]:
            file_to_update.write(str(each) + '\n')


def update_items_and_keys():
    global items
    global keys
    with open("items.txt", "w") as wipe_clean:
        wipe_clean.close()
    with open("items.txt", 'at') as file_to_update:
        for each in items:
            file_to_update.writelines(str(each))
            file_to_update.writelines(str('\n'))
    with open("keys.txt", "w") as wipe_clean:
        wipe_clean.close()
    with open("keys.txt", 'at') as file_to_update:
        for each in keys:
            file_to_update.writelines(str(each))
            file_to_update.writelines(str('\n'))
    items = []
    keys = []


def update_last_tweet_id():
    global last_tweet_id
    with open("last_tweet_id.txt", 'wt') as to_write:
        to_write.write(last_tweet_id)


def you_have_died():
    initialize_game()


def new_run_game():
    global current_room
    global last_tweet_id
    pull_last_tweet_id()
    temp_room_holding = get_current_room()
    if isinstance(temp_room_holding, str):
        chosen_room = temp_room_holding
    else:
        chosen_room = get_current_room()
    next_step(chosen_room)


def next_step(chosen_room):
    global current_room
    global last_tweet_id
    global items
    set_character_stats()
    set_items_and_keys()
    if chosen_room == '0':
        build_your_character()
    elif chosen_room == '0-1':
        difficulty_choice = get_poll_results(last_tweet_id)
        handle_special_results(difficulty_choice)
    elif chosen_room == '0-2':
        potion_choice = get_poll_results(last_tweet_id)
        handle_special_results(potion_choice)
    else:
        if chosen_room not in ['fight on!', 'Test your luck!']:
            chosen_room = int(chosen_room)
        work_from_tweet = media_or_poll_result()
        if work_from_tweet == 'poll tweet':
            results = get_poll_results(last_tweet_id)
        else:
            results = chosen_room
        if results in ['fight on!', 'Test your luck!'] or items:
            handle_special_results(results)
        else:
            results = int(results)
            set_current_room(results)
            play_next_room(results)
    update_character_stats()
    update_initial_character_stats()
    update_items_and_keys()
    update_last_tweet_id()


new_run_game()
