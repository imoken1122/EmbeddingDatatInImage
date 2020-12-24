# EmbeddingTextInImage


This repository for embedding any text or files(.zip,.exe ...) in images (.png) binary.   
<br>
このレポジトリのコードは画像(.png)のバイナリに任意のテキストやファイルを埋め込めます.

<br>

### Prerequisites
- python 3.7

### Usage

To embed text or file in a png image, set arguments and do the following: 
```bash
[text]
python embeding_text.py -t -in <image.png> -on <output.png>

[file]
python embeding_text.py -in <image.png> -on <output.png>
```


<br>
If you want to find the text or file embedded in the image, do the following:

```bash
[text]
python embeding_text.py -t -in <image.png>

[file]
python embeding_text.py -in <image.png>
```
