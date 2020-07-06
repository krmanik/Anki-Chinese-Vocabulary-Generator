# Anki-Chinese-Vocabulary-Generator
Enter only simplified characters and create word meaning with Traditional, Pinyin, Meaning and Audio

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
```
gTTS
pinyin
hanziconv
googletrans
git+https://github.com/DeepHorizons/tts
```
To install
```
pip install -r requirements.txt
```

3. Run ```main.py``` and start adding words

# Data
The dictionary data of CC-CEDICT converted to individual .json file using [cedict-json](https://github.com/infinyte7/cedict-json).

[CC-CEDICT](https://www.mdbg.net/chinese/dictionary?page=cedict)

# License
Read [License.md](/License.md)