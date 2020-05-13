import tensorflow as tf
from keras_vggface.vggface import VGGFace
from keras.layers import GlobalAveragePooling2D, GlobalMaxPooling2D, Concatenate
from keras.engine import Model
export_path = './vggface'

model = VGGFace(model='senet50', include_top=False, input_shape=(224, 224, 3), pooling=None)
#MODEL.summary()
output = model.get_layer('add_16').output
x1 = GlobalAveragePooling2D()(output)
x2 = GlobalMaxPooling2D()(output)
x = Concatenate()([x1,x2])
model = Model(model.input, x)

with tf.keras.backend.get_session() as sess:
    tf.saved_model.simple_save(
        sess,
        export_path,
        inputs={'input_image': model.input},
        outputs={t.name:t for t in model.outputs})