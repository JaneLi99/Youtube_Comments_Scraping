import jieba
from wordcloud.wordcloud import WordCloud
import matplotlib.pyplot as plt

def wordcloud_plot(content):
    words = jieba.lcut(content)
    cuted = ' '.join(words)
    fontpath = 'AdobeArabic-Regular.otf'

    wc = WordCloud(font_path=fontpath,
                   background_color="white",
                   max_words=1000,
                   max_font_size=500,
                   min_font_size=20,
                   random_state=42,
                   collocations=False,
                   width=1600, height=1200, margin=10,
                   )
    wc.generate(cuted)

    return wc

if __name__ == "__main__":
    text = ''
    with open('Copy_of_sentence_anaysis_product_edit_clear.txt', 'r', encoding='UTF-8') as f:
        text = f.read()
        f.close()

    wc = wordcloud_plot(text)
    plt.figure(dpi=100)
    plt.imshow(wc, interpolation='catrom', vmax=1000)
    plt.axis("off")
    plt.show()

