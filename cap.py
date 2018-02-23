import math
import os
import tensorflow as tf
from im2txt import configuration
from im2txt import inference_wrapper
from im2txt.inference_utils import caption_generator
from im2txt.inference_utils import vocabulary

checkpointpath = './model.ckpt-2000000' 
vocabfile =  './word_counts.txt'
imagefile = './test/*'

g = tf.Graph()
with g.as_default():
    model = inference_wrapper.InferenceWrapper()
    restore_fn = model.build_graph_from_config(configuration.ModelConfig(), checkpointpath)
g.finalize()
    
vocab = vocabulary.Vocabulary(vocabfile)

filenames = []
for file_pattern in imagefile.split(","):
    filenames.extend(tf.gfile.Glob(file_pattern))

with tf.Session(graph=g) as sess:
    restore_fn(sess)
    generator = caption_generator.CaptionGenerator(model, vocab)

    for filename in filenames:
        with tf.gfile.GFile(filename, "rb") as f:
           image = f.read()
        captions = generator.beam_search(sess, image)
        print("Captions for image %s:" % os.path.basename(filename))
        for i, caption in enumerate(captions):
            sentence = [vocab.id_to_word(w) for w in caption.sentence[1:-1]]
            sentence = " ".join(sentence)
            print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)))
