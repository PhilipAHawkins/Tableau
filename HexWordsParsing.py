import pandas as pd
from nltk.corpus import wordnet

# earlier today Jorge Camoes posted on Twitter that the word "bebada" is both a Portuguese word for a drunk woman and
# the hex code for a lightish purple color.
# supposing that Hex Codes use all 10 numbers and the letters A-F in a 6-character string,
# it's entirely possible that many words are also hex codes
# if we use 1337 speak to assume certain letters can be turned into numbers like so:
my_1337_dict = {"l":1,
                "s":5,
                "g":6,
                "t":7,
                "o":0}

# then feed A-F and the above letters into a Word Unscrambler like http://www.allscrabblewords.com/unscramble/abcdeflisgot,
# we get the following words that are 6 characters long and only use letters or 1337 letters that would be valid in a Hex Code.
# those words are:

bag_of_words = ['ablest', 'abodes', 'adobes','aglets','albedo','aldose','badges','bagels','basted','beclog','beflag','befogs',
                'beglad','belgas','blades','bleats','bloats','boated','boatel','bodega','bogles','bolted','botels','cabled',
                'cables','cablet','cadets','cadges','castle','clades','cleats','clefts','closed','closet','coaled','coated',
                'cobalt','cobles','colead','costae','costal','costed','debags','decafs','decals','defats','defogs',
                'delfts','deltas','desalt','doable','doblas','dosage','dotage','eclats','fabled','fables','facets','fadges',
                'falces','fasted','festal','floats','flotas','foaled','fodgel','foetal','folate','gabled','gables','gaoled',
                'gasted','gelato','glaces','glades','gloats','globed','globes','goaled','goblet','godets','golfed','lasted',
                'legato','loafed','lobate','locate','lodges','lofted','oblast','oblate','octads','oldest','osteal','salted',
                'scaled','seadog','slated','socage','solace','solate','stable','staged','staled','stodge','stoled','tabled',
                'tables','talced','telcos','togaed',]

# let's convert the above above list into the 1337 version and add a hex tag.
my_1337_words = []
my_hex_codes = []
# this _should_ be a trivial string replacement exercise so I won't focus too hard on optimization.
for y in bag_of_words:
    foo_word = []
    for x in y:
        if x in my_1337_dict:
            x = str(my_1337_dict.get(x))
        foo_word.append(x)
        print_word = "<color>#" + "".join(foo_word) + "</color>"
        hex_word = "".join(foo_word)
    my_1337_words.append(print_word)
    my_hex_codes.append(hex_word)
# now write this to a txt file we'll use to inject some XML into Preferences.tps
with open('Tableau_Preferences_changes.txt', 'w') as f:
    for item in my_1337_words:
        f.write("%s\n" % item)
# let's also build our scaffold for Tableau here.
my_row_iter = 4
my_row = []
my_col = []
meanings = [] # Let's also get definitions. Because.
for x,y in enumerate(bag_of_words):
    # rows:
    if x < my_row_iter:
        my_row.append(x//4) # who says you never use floor division?
    else:
        my_row_iter +=4
        my_row.append(x // 4)
    # columns:
    # I want 4 columns for shapes in Tableau.
    my_col.append(x % 4)
    syns = wordnet.synsets(y)
    if len(syns) > 0:
        definition = wordnet.synsets(y)[0].definition()
    else:
        definition = "No definition, probably not a word."
    meanings.append(definition)

df = pd.DataFrame({'Word':bag_of_words,
                   'XML':my_1337_words,
                   'Color':my_hex_codes,
                   'Column':my_col,
                   'Row':my_row,
                   'Definition':meanings})
writer = pd.ExcelWriter("HiddenColors.xlsx")
df.to_excel(writer, sheet_name="Colors", index=False, startrow=0, startcol=0)

# Now we're doing a separate dataframe of each hex code and its RGB values, but each value is a different row of data.
# This is a "tall not wide' strategy to assist Tableau in drawing a radar chart
# Hex to RGB logic
def hex_to_rgb(value):
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# loop the hex codes in my_hex_codes and return 3 rows of data- the code, if it's R, G, or B, and the int value.
# fake my_hex_code for testing. delete after testing.
# my_hex_codes = ["AAAAAA","BEC106",'57AB1E']
Red = []
Green = []
Blue = []
for x in my_hex_codes:
    this_color = hex_to_rgb(x)
    Red.append(this_color[0])
    Green.append(this_color[1])
    Blue.append(this_color[2])
RGB_df = pd.DataFrame({'Color': my_hex_codes, 'Red': Red, 'Green':Green,'Blue':Blue})
RGB_df['TopColor'] = RGB_df[['Red','Green','Blue']].idxmax(axis = 1)
RGB_df.to_excel(writer, sheet_name="RGB", index=False, startrow=0, startcol=0)
writer.save()