import tensorflow as tf
import cv2
import numpy as np

def generate_gradcam(model, img_tensor):
    seq_model = model
    base_model = seq_model.layers[0]

    gap_layer = seq_model.layers[1]
    dense1 = seq_model.layers[2]
    dropout = seq_model.layers[3]
    dense2 = seq_model.layers[4]

    conv_output = base_model.get_layer("Conv_1").output

    x = gap_layer(conv_output)
    x = dense1(x)
    x = dropout(x, training=False)
    preds = dense2(x)

    grad_model = tf.keras.Model(
        inputs=base_model.input,
        outputs=[conv_output, preds]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_tensor)
        class_idx = tf.argmax(predictions[0])
        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(conv_outputs * pooled_grads, axis=-1)
    heatmap = tf.maximum(heatmap, 0)
    heatmap /= tf.reduce_max(heatmap)

    heatmap = heatmap.numpy()
    heatmap = cv2.GaussianBlur(heatmap, (7, 7), 0)

    return heatmap
