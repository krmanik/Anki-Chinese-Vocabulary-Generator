# Anki-Chinese-Vocabulary-Generator
Enter only simplified characters and create word meaning with Traditional, Pinyin, Meaning and Audio

## Demo
![demo](https://raw.githubusercontent.com/infinyte7/Anki-Chinese-Vocabulary-Generator/master/Images/demo.gif)

## Features
- Traditional, Pinyin, Meaning and Audio generated automatically
- Offline fetch meaning from ```data``` folder. (cedict)
- Fetch meaning using Google translate when not found in cedict
- Save audio file in using [gTTS](https://gtts.readthedocs.io/) or [DeepHorizons/tts](https://github.com/DeepHorizons/tts)
- Save list to text file, can be imported to Anki
- Edit / Delete 

## Quick start
 1. Install Python [https://www.python.org](https://www.python.org/)
 2. Install required library in ```requirements.txt```
 To install
```
pip install -r requirements.txt
```
```requirements.txt``` file contains following
```
gTTS
pinyin
hanziconv
googletrans
git+https://github.com/DeepHorizons/tts
```

3. Run ```main.py``` and start adding words

# Note
Languages & voices for [DeepHorizons/tts](https://github.com/DeepHorizons/tts) may be needed to install.


# Data
The dictionary data of CC-CEDICT converted to individual .json file using [cedict-json](https://github.com/infinyte7/cedict-json).

<br>[CC-CEDICT](https://www.mdbg.net/chinese/dictionary?page=cedict)

# Import in Anki 
Use Anki Desktop to import it for [Anki-xiehanzi](https://github.com/infinyte7/Anki-xiehanzi)
1. Copy ```xiehanzi``` to ```collection.media``` folder in Anki
2. Create a new deck
3. Import generated ```xiehanzi.txt``` file
4. Select ```Fields separated by: Tabs```
5. Map the fields to respective fields 
6. Then import

![Demo](https://raw.githubusercontent.com/infinyte7/Anki-Chinese-Vocabulary-Generator/master/Images/import_demo.gif)

# Contribute
Code optimization will be appreciated.

# License
Read [License.md](/License.md)