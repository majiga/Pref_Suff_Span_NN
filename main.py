from data_utils import get_trimmed_glove_vectors, load_vocab, get_processing_word, CoNLLDataset
from model import NERModel
from config import Config


def main(config):
    # load vocabs
    vocab_words = load_vocab(config.words_filename)
    vocab_tags  = load_vocab(config.tags_filename)
    vocab_chars = load_vocab(config.chars_filename)
    vocab_pref_suff = load_vocab(config.PS_filename)  ############### For prefix and suffix
    vocab_pref_suff_2 = load_vocab(config.PS_filename_2)
    vocab_pref_suff_4 = load_vocab(config.PS_filename_4)
    # get processing functions
    processing_word = get_processing_word(vocab_words, vocab_chars,vocab_pref_suff,vocab_pref_suff_2,vocab_pref_suff_4,
                    lowercase=True, chars=config.chars, Pref_Suff=config.pref_suff)
    processing_tag  = get_processing_word(vocab_tags, 
                    lowercase=False)

    # get pre trained embeddings
    embeddings = get_trimmed_glove_vectors(config.trimmed_filename)

    # create dataset
    dev   = CoNLLDataset(config.dev_filename, processing_word,   ############ Here dev, test and train have the raw words and tags. Now we have to map these to corresponding word index
                        processing_tag, config.max_iter)         ############ and tags index. Therefore, when we do model.evaluate in below lines, it calls run_evaluate in run_epoch function
    test  = CoNLLDataset(config.test_filename, processing_word,
                        processing_tag, config.max_iter)
    train = CoNLLDataset(config.train_filename, processing_word,
                        processing_tag, config.max_iter)

    # build model
    model = NERModel(config, embeddings, ntags=len(vocab_tags),
                                         nchars=len(vocab_chars))
    model.build()

    # train, evaluate and interact
    model.train(train, dev, vocab_tags)
    model.evaluate(test, vocab_tags)
    #model.interactive_shell(vocab_tags, processing_word)


if __name__ == "__main__":
    # create instance of config
    config = Config()
    
    # load, train, evaluate and interact with model
    main(config)
