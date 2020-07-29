# Anki-Chinese-Vocabulary-Generator
Enter only simplified characters and create word meaning with Traditional, Pinyin, Meaning, Audio and example sentences offline.

## Demo
![demo](https://raw.githubusercontent.com/infinyte7/Anki-Chinese-Vocabulary-Generator/master/Images/demo.gif)

### Update 
V1.2
- Sentences, Sentences Pinyin and Translations in separate fields 

## Features
- Traditional, Pinyin, Meaning and Audio generated automatically
- Offline fetch meaning from ```data``` folder. (cedict)
- Fetch sentences from ```data.db``` offline 
- Fetch meaning using Google translate when not found in cedict
- Save audio file in using [gTTS](https://gtts.readthedocs.io/) or [DeepHorizons/tts](https://github.com/DeepHorizons/tts)
- Save list to text file, can be imported to Anki
- Edit / Delete 

## Quick start
 1. Install Python [https://www.python.org](https://www.python.org/)
 2. Download this repository 
 2. Install required library in ```requirements.txt```
 To install
```
pip install -r requirements.txt
```
```requirements.txt``` file contains following
```
jieba
gTTS
pinyin
pycedict
hanziconv
googletrans
git+https://github.com/DeepHorizons/tts
```

**Note: Install ```git``` also.**
https://git-scm.com/

3. Run ```main.py``` and start adding words

## To run Android using Pydroid 3
1. Install [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3) from play store
2. Download this repository
3. Install following using Pip inside Pydroid 3. It requires [Pydroid repository plugin](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3.quickinstallrepo)
```
jieba
gTTS
pinyin
pycedict
hanziconv
googletrans
```
4. Download this keyboard [搜狗输入法 sōugǒu shūrù fǎ sogou Input](https://play.google.com/store/apps/details?id=com.sohu.inputmethod.sogou) from play store
<br/>**Note: Other keyboard will not help in typing chinese characters** 
5. Open the ```main_for_android.py``` inside Pydroid 3
6. Run the script and start adding words

#### Image
<img src="Images/pydroid_3.PNG" height="400" width="390"></img>

### Demo
<img src="Images/demo_android.gif" height="528" width="265"></img>

# Note
Languages & voices for [DeepHorizons/tts](https://github.com/DeepHorizons/tts) may be needed to install.


# Data
### Dictionary
The ```json_data``` folder contains dictionary data of CC-CEDICT converted to individual ```.json``` file using [cedict-json](https://github.com/infinyte7/cedict-json).
<br>[CC-CEDICT](https://www.mdbg.net/chinese/dictionary?page=cedict)

### Sentences
The ```data.db``` contains sentences downloaded from https://tatoeba.org/eng/downloads. For accessing sentences matching the words offline.

### Audio
The ```audio_data``` folder contains audio taken from https://github.com/hugolpz/audio-cmn. <br>Those audio taken from http://shtooka.net/download.php

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

# Todo 
- Stop freezing when translating the sentences

# License
Read [License.md](/License.md)
