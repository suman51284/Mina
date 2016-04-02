import os, sys, subprocess
import fontforge
from fontTools import ttLib
from shutil import copyfile, rmtree

print "[INFO] Resetting sources folder"
try:
    rmtree("sources/Mina-Regular.ufo")
    rmtree("sources/Mina-Bold.ufo")
except:
    pass

font_0= fontforge.open("sources/sfd/Mina-bengali-0.sfd")
font_1= fontforge.open("sources/sfd/Mina-bengali-1.sfd")

print "[INFO] Hinting fonts"
font_0.selection.all()
font_0.autoHint()

print "[INFO] Generating UFO files"

font_0.generate("sources/Mina-Regular.ufo")
font_1.generate("sources/Mina-Bold.ufo")

os.remove("sources/Mina-Bold.ufo/features.fea")
os.remove("sources/Mina-Regular.ufo/features.fea")

copyfile("features/regular/features.fea", "sources/Mina-Regular.ufo/features.fea")
copyfile("features/bold/features.fea", "sources/Mina-Bold.ufo/features.fea")

font_0= fontforge.open("sources/Mina-Regular.ufo")
font_1= fontforge.open("sources/Mina-Bold.ufo")

try:
    os.remove("FONTS/otf/Mina-Regular.otf")
    os.remove("FONTS/otf/Mina-Bold.otf")
    os.remove("FONTS/ttf/Mina-Regular.ttf")
    os.remove("FONTS/ttf/Mina-Bold.ttf")
except:
    pass

print "[INFO] Generating OTF"
font_0.generate("FONTS/otf/Mina-Regular.otf")
font_1.generate("FONTS/otf/Mina-Bold.otf")

print "[INFO] Generating TTF"
font_0.generate("FONTS/ttf/Mina-Regular.ttf")
font_1.generate("FONTS/ttf/Mina-Bold.ttf")

print "[INFO] Generating DSIG"
newDSIG = ttLib.newTable("DSIG")
newDSIG.ulVersion = 1
newDSIG.usFlag = 1
newDSIG.usNumSigs = 1
sig = ttLib.tables.D_S_I_G_.SignatureRecord()
sig.ulLength = 20
sig.cbSignature = 12
sig.usReserved2 = 0
sig.usReserved1 = 0
sig.pkcs7 = '\xd3M4\xd3M5\xd3M4\xd3M4'
sig.ulFormat = 1
sig.ulOffset = 20
newDSIG.signatureRecords = [sig]

f=ttLib.TTFont("FONTS/otf/Mina-Regular.otf")
f.tables["DSIG"] = newDSIG
f.save("FONTS/otf/Mina-Regular.otf")

f=ttLib.TTFont("FONTS/otf/Mina-Bold.otf")
f.tables["DSIG"] = newDSIG
f.save("FONTS/otf/Mina-Bold.otf")

f=ttLib.TTFont("FONTS/ttf/Mina-Regular.ttf")
f.tables["DSIG"] = newDSIG
f.save("FONTS/ttf/Mina-Regular.ttf")

f=ttLib.TTFont("FONTS/ttf/Mina-Bold.ttf")
f.tables["DSIG"] = newDSIG
f.save("FONTS/ttf/Mina-Bold.ttf")

print "[INFO] Done"
