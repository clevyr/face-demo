import tensorflow as tf
import mtcnn
export_path = './mtcnn'

model = mtcnn.MTCNN()
print(dir(model))

with tf.keras.backend.get_session() as sess:
    tf.saved_model.simple_save(
        sess,
        export_path,
        inputs={'input_image': model.input},
        outputs={t.name:t for t in model.outputs})